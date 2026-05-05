#!/usr/bin/env python3
"""
Minecraft web admin panel.

Lets non-technical admins manage mods (upload / disable / delete),
control the server (start / stop / restart) and tail the journal —
all from a browser.

Configuration is read exclusively from environment variables so that
no credentials appear in this source file.  The systemd EnvironmentFile
(/etc/minecraft/mcweb.env) is the canonical place to set them.

Required env vars
-----------------
MC_SECRET_KEY     Flask session signing key  (random 32+ chars)
MC_PASSWORD_HASH  Werkzeug password hash — generate with:
                    python3 -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your_password'))"

Optional env vars (sensible defaults shown)
-------------------------------------------
MC_MODS_DIR        /srv/minecraft/data/mods
MC_DISABLED_DIR    /srv/minecraft/data/disabled-mods
MC_CTL_CMD         /usr/local/bin/minecraftctl
MC_BIND_IP         127.0.0.1
MC_PORT            8080
MC_MAX_UPLOAD_MB   64
"""

import hashlib
import hmac
import os
import subprocess
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

# ── Config ────────────────────────────────────────────────────────────────────

MODS_DIR = Path(os.environ.get("MC_MODS_DIR", "/srv/minecraft/data/mods"))
DISABLED_DIR = Path(os.environ.get("MC_DISABLED_DIR", "/srv/minecraft/data/disabled-mods"))
CTL_CMD = os.environ.get("MC_CTL_CMD", "/usr/local/bin/minecraftctl")
SECRET_KEY = os.environ["MC_SECRET_KEY"]
PASSWORD_HASH = os.environ["MC_PASSWORD_HASH"]
MAX_UPLOAD_MB = int(os.environ.get("MC_MAX_UPLOAD_MB", "64"))
BIND_IP = os.environ.get("MC_BIND_IP", "127.0.0.1")
BIND_PORT = int(os.environ.get("MC_PORT", "8080"))

_ALLOWED_EXT = frozenset({".jar"})

# ── App ───────────────────────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# ── Helpers ───────────────────────────────────────────────────────────────────


def _allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in _ALLOWED_EXT


def _safe_path(directory: Path, filename: str) -> "Path | None":
    """Resolve *filename* inside *directory* and reject path-traversal attempts."""
    target = (directory / filename).resolve()
    try:
        target.relative_to(directory.resolve())
        return target
    except ValueError:
        return None


def _mod_list(directory: Path) -> list:
    if not directory.exists():
        return []
    return sorted(
        [
            {"name": p.name, "size": f"{p.stat().st_size // 1024} KB"}
            for p in directory.glob("*.jar")
        ],
        key=lambda m: m["name"].lower(),
    )


def _run_ctl(action: str) -> "tuple[int, str]":
    if action not in {"start", "stop", "restart", "status", "logs", "backup"}:
        return 1, "Invalid action"
    try:
        result = subprocess.run(
            ["sudo", CTL_CMD, action],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode, (result.stdout + result.stderr).strip()
    except Exception as exc:
        return 1, str(exc)


def _csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = os.urandom(24).hex()
    return session["csrf_token"]


def _check_csrf() -> bool:
    token = request.form.get("csrf_token", "")
    if not hmac.compare_digest(token, session.get("csrf_token", "")):
        flash("Invalid request (CSRF check failed).", "danger")
        return False
    return True


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


# ── HTML templates ────────────────────────────────────────────────────────────
# All pages share a single base string; page-specific content is substituted
# via Python str.replace() at module load time so there are no Jinja2 block
# conflicts.  Only the substituted strings are processed by Flask/Jinja2.

_BASE = """\
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Minecraft Admin</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
        crossorigin="anonymous">
  <style>
    body  { background: #0d1117; }
    .card { background: #161b22; border-color: #30363d; }
    .table-dark { --bs-table-bg: #161b22; }
    .navbar-brand { letter-spacing: .03em; }
    pre { background: #0a0a0a; border-radius: 6px; padding: .75rem;
          max-height: 400px; overflow-y: auto; font-size: .8rem; }
  </style>
</head>
<body class="text-light">

<nav class="navbar navbar-dark px-3 py-2" style="background:#238636">
  <span class="navbar-brand fw-bold">&#x26CF; Minecraft Admin</span>
  <div class="d-flex gap-2">
    {% if session.get('authenticated') %}
    <a class="btn btn-sm btn-outline-light" href="{{ url_for('index') }}">Dashboard</a>
    <a class="btn btn-sm btn-outline-light" href="{{ url_for('mods_page') }}">Mods</a>
    <a class="btn btn-sm btn-outline-light" href="{{ url_for('logs_page') }}">Logs</a>
    <a class="btn btn-sm btn-outline-danger"  href="{{ url_for('logout') }}">Logout</a>
    {% endif %}
  </div>
</nav>

<div class="container py-4">
  {% with messages = get_flashed_messages(with_categories=true) %}
  {% for cat, msg in messages %}
  <div class="alert alert-{{ cat if cat != 'message' else 'info' }} alert-dismissible fade show" role="alert">
    {{ msg }}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  </div>
  {% endfor %}
  {% endwith %}

  %%CONTENT%%

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmAqL/E8Ru2QFbv7MzW/V1Xk5aI7"
        crossorigin="anonymous"></script>
</body>
</html>
"""

# ── Login ─────────────────────────────────────────────────────────────────────

_LOGIN = _BASE.replace("%%CONTENT%%", """\
<div class="row justify-content-center mt-5">
  <div class="col-sm-8 col-md-5 col-lg-4">
    <div class="card shadow">
      <div class="card-body p-4">
        <h4 class="mb-3">&#128274; Sign in</h4>
        <form method="post">
          <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
          <div class="mb-3">
            <label class="form-label">Admin password</label>
            <input type="password" name="password"
                   class="form-control bg-dark text-light border-secondary"
                   autofocus required>
          </div>
          <button class="btn btn-success w-100">Sign in</button>
        </form>
      </div>
    </div>
  </div>
</div>
""")

# ── Dashboard ─────────────────────────────────────────────────────────────────

_DASHBOARD = _BASE.replace("%%CONTENT%%", """\
<div class="row g-4">

  <!-- Server status card -->
  <div class="col-md-7">
    <div class="card h-100 shadow">
      <div class="card-body">
        <h5 class="card-title mb-3">Server status</h5>
        <pre class="text-{{ 'success' if status_ok else 'danger' }} mb-3">{{ status_out }}</pre>
        <form method="post" action="{{ url_for('server_action') }}"
              class="d-flex flex-wrap gap-2">
          <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
          <button name="action" value="start"
                  class="btn btn-success">&#9654; Start</button>
          <button name="action" value="stop"
                  class="btn btn-danger">&#9632; Stop</button>
          <button name="action" value="restart"
                  class="btn btn-warning text-dark">&#8635; Restart</button>
          <button name="action" value="backup"
                  class="btn btn-outline-light">&#128190; Backup now</button>
        </form>
      </div>
    </div>
  </div>

  <!-- Mod count card -->
  <div class="col-md-5">
    <div class="card h-100 shadow">
      <div class="card-body">
        <h5 class="card-title">Installed mods</h5>
        <p class="display-4 fw-bold text-success mb-1">{{ mod_count }}</p>
        {% if disabled_count %}
        <p class="text-muted small mb-3">{{ disabled_count }} disabled</p>
        {% else %}
        <p class="mb-3"></p>
        {% endif %}
        <a href="{{ url_for('mods_page') }}" class="btn btn-primary">
          Manage mods &#8594;
        </a>
      </div>
    </div>
  </div>

</div>
""")

# ── Mods ──────────────────────────────────────────────────────────────────────

_MODS = _BASE.replace("%%CONTENT%%", """\
<div class="d-flex align-items-center mb-4 gap-3">
  <h4 class="mb-0">Mod manager</h4>
  <a href="{{ url_for('index') }}" class="btn btn-sm btn-outline-secondary">
    &#8592; Dashboard
  </a>
</div>

<!-- Upload form -->
<div class="card shadow mb-4">
  <div class="card-body">
    <h6>Upload a mod</h6>
    <p class="text-warning small mb-2">
      Only <code>.jar</code> files are accepted.
      <strong>Restart the server after adding or removing mods.</strong>
    </p>
    <form method="post" action="{{ url_for('upload_mod') }}"
          enctype="multipart/form-data">
      <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
      <div class="input-group">
        <input type="file" name="mod_file" accept=".jar"
               class="form-control bg-dark text-light border-secondary" required>
        <button class="btn btn-success">&#11014; Upload</button>
      </div>
    </form>
  </div>
</div>

<!-- Active mods table -->
<h5>Active mods ({{ mods | length }})</h5>
<div class="table-responsive mb-4">
  <table class="table table-dark table-hover align-middle mb-0">
    <thead class="table-active">
      <tr>
        <th>Filename</th>
        <th>Size</th>
        <th class="text-end">Actions</th>
      </tr>
    </thead>
    <tbody>
    {% for mod in mods %}
    <tr>
      <td class="font-monospace">{{ mod.name }}</td>
      <td class="text-muted">{{ mod.size }}</td>
      <td class="text-end">
        <form method="post" action="{{ url_for('disable_mod') }}" class="d-inline">
          <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
          <input type="hidden" name="filename"   value="{{ mod.name }}">
          <button class="btn btn-sm btn-outline-warning" title="Disable without deleting">
            &#9646;&#9646; Disable
          </button>
        </form>
        <form method="post" action="{{ url_for('delete_mod') }}" class="d-inline"
              onsubmit="return confirm('Permanently delete {{ mod.name }}?')">
          <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
          <input type="hidden" name="filename"   value="{{ mod.name }}">
          <button class="btn btn-sm btn-danger" title="Permanently delete">
            &#128465; Delete
          </button>
        </form>
      </td>
    </tr>
    {% else %}
    <tr>
      <td colspan="3" class="text-muted text-center py-3">
        No mods installed.
      </td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</div>

<!-- Disabled mods table -->
{% if disabled %}
<h5>Disabled mods ({{ disabled | length }})</h5>
<p class="text-muted small">These files are kept in the disabled-mods folder
   and do not load at runtime.</p>
<div class="table-responsive">
  <table class="table table-dark table-hover align-middle mb-0">
    <thead class="table-active">
      <tr>
        <th>Filename</th>
        <th>Size</th>
        <th class="text-end">Actions</th>
      </tr>
    </thead>
    <tbody>
    {% for mod in disabled %}
    <tr>
      <td class="font-monospace text-muted">{{ mod.name }}</td>
      <td class="text-muted">{{ mod.size }}</td>
      <td class="text-end">
        <form method="post" action="{{ url_for('enable_mod') }}" class="d-inline">
          <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
          <input type="hidden" name="filename"   value="{{ mod.name }}">
          <button class="btn btn-sm btn-outline-success">&#9654; Enable</button>
        </form>
        <form method="post" action="{{ url_for('delete_disabled_mod') }}" class="d-inline"
              onsubmit="return confirm('Permanently delete {{ mod.name }}?')">
          <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
          <input type="hidden" name="filename"   value="{{ mod.name }}">
          <button class="btn btn-sm btn-danger">&#128465; Delete</button>
        </form>
      </td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% endif %}
""")

# ── Logs ──────────────────────────────────────────────────────────────────────

_LOGS = _BASE.replace("%%CONTENT%%", """\
<div class="d-flex align-items-center mb-3 gap-3">
  <h4 class="mb-0">Server logs</h4>
  <a href="{{ url_for('index') }}" class="btn btn-sm btn-outline-secondary">
    &#8592; Dashboard
  </a>
  <a href="{{ url_for('logs_page') }}" class="btn btn-sm btn-outline-light">
    &#8635; Refresh
  </a>
</div>
<pre class="text-success">{{ log_output }}</pre>
""")

# ── Routes ────────────────────────────────────────────────────────────────────


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        csrf_ok = hmac.compare_digest(
            request.form.get("csrf_token", ""), _csrf_token()
        )
        pw_ok = check_password_hash(PASSWORD_HASH, request.form.get("password", ""))
        if csrf_ok and pw_ok:
            session["authenticated"] = True
            session.permanent = False
            return redirect(url_for("index"))
        flash("Invalid password.", "danger")
    return render_template_string(_LOGIN, csrf_token=_csrf_token())


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    rc, out = _run_ctl("status")
    return render_template_string(
        _DASHBOARD,
        status_ok=(rc == 0),
        status_out=out[:3000],
        mod_count=len(_mod_list(MODS_DIR)),
        disabled_count=len(_mod_list(DISABLED_DIR)),
        csrf_token=_csrf_token(),
    )


@app.route("/server", methods=["POST"])
@login_required
def server_action():
    if not _check_csrf():
        return redirect(url_for("index"))
    action = request.form.get("action", "")
    if action not in {"start", "stop", "restart", "backup"}:
        flash("Unknown action.", "danger")
        return redirect(url_for("index"))
    rc, out = _run_ctl(action)
    if rc == 0:
        flash(f"Server {action} completed successfully.", "success")
    else:
        flash(f"Server {action} failed: {out[:300]}", "danger")
    return redirect(url_for("index"))


@app.route("/mods")
@login_required
def mods_page():
    return render_template_string(
        _MODS,
        mods=_mod_list(MODS_DIR),
        disabled=_mod_list(DISABLED_DIR),
        csrf_token=_csrf_token(),
    )


@app.route("/mods/upload", methods=["POST"])
@login_required
def upload_mod():
    if not _check_csrf():
        return redirect(url_for("mods_page"))
    f = request.files.get("mod_file")
    if not f or not f.filename:
        flash("No file selected.", "warning")
        return redirect(url_for("mods_page"))
    filename = secure_filename(f.filename)
    if not _allowed_file(filename):
        flash("Only .jar files are allowed.", "danger")
        return redirect(url_for("mods_page"))
    MODS_DIR.mkdir(parents=True, exist_ok=True)
    dest = _safe_path(MODS_DIR, filename)
    if dest is None:
        flash("Invalid filename.", "danger")
        return redirect(url_for("mods_page"))
    f.save(dest)
    flash(f"Uploaded {filename}. Restart the server to apply changes.", "success")
    return redirect(url_for("mods_page"))


@app.route("/mods/delete", methods=["POST"])
@login_required
def delete_mod():
    if not _check_csrf():
        return redirect(url_for("mods_page"))
    filename = secure_filename(request.form.get("filename", ""))
    if not filename or not filename.lower().endswith(".jar"):
        flash("Invalid filename.", "danger")
        return redirect(url_for("mods_page"))
    target = _safe_path(MODS_DIR, filename)
    if target and target.exists():
        target.unlink()
        flash(f"Deleted {filename}.", "success")
    else:
        flash("File not found.", "warning")
    return redirect(url_for("mods_page"))


@app.route("/mods/disable", methods=["POST"])
@login_required
def disable_mod():
    if not _check_csrf():
        return redirect(url_for("mods_page"))
    filename = secure_filename(request.form.get("filename", ""))
    if not filename or not filename.lower().endswith(".jar"):
        flash("Invalid filename.", "danger")
        return redirect(url_for("mods_page"))
    src = _safe_path(MODS_DIR, filename)
    if src and src.exists():
        DISABLED_DIR.mkdir(parents=True, exist_ok=True)
        dst = _safe_path(DISABLED_DIR, filename)
        if dst:
            src.rename(dst)
            flash(f"Disabled {filename}. Restart to apply.", "success")
    else:
        flash("File not found.", "warning")
    return redirect(url_for("mods_page"))


@app.route("/mods/enable", methods=["POST"])
@login_required
def enable_mod():
    if not _check_csrf():
        return redirect(url_for("mods_page"))
    filename = secure_filename(request.form.get("filename", ""))
    if not filename or not filename.lower().endswith(".jar"):
        flash("Invalid filename.", "danger")
        return redirect(url_for("mods_page"))
    src = _safe_path(DISABLED_DIR, filename)
    if src and src.exists():
        dst = _safe_path(MODS_DIR, filename)
        if dst:
            src.rename(dst)
            flash(f"Enabled {filename}. Restart to apply.", "success")
    else:
        flash("File not found.", "warning")
    return redirect(url_for("mods_page"))


@app.route("/mods/delete-disabled", methods=["POST"])
@login_required
def delete_disabled_mod():
    if not _check_csrf():
        return redirect(url_for("mods_page"))
    filename = secure_filename(request.form.get("filename", ""))
    if not filename or not filename.lower().endswith(".jar"):
        flash("Invalid filename.", "danger")
        return redirect(url_for("mods_page"))
    target = _safe_path(DISABLED_DIR, filename)
    if target and target.exists():
        target.unlink()
        flash(f"Deleted {filename}.", "success")
    else:
        flash("File not found.", "warning")
    return redirect(url_for("mods_page"))


@app.route("/logs")
@login_required
def logs_page():
    try:
        result = subprocess.run(
            ["sudo", CTL_CMD, "logs"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        log_output = (result.stdout + result.stderr).strip()[-10000:]
    except Exception as exc:
        log_output = f"Error reading logs: {exc}"
    return render_template_string(_LOGS, log_output=log_output)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host=BIND_IP, port=BIND_PORT)
