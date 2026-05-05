# CI/CD Workflow

This repository now uses a split pipeline model:

- CI on GitHub-hosted runners for static validation.
- CD on a self-hosted runner on `ws1` for controlled production deploys.

## Why this split exists

The Minecraft production deploy path depends on:

- local Ansible inventory
- local vault password helper at `automation/ansible/scripts/get-vault-pass.sh`
- the encrypted vault file at `automation/ansible/inventories/lab/vault.yml`
- direct network access from `ws1` to `media1`

That means production deploys are not realistic from a generic GitHub-hosted runner.

## CI: what runs on every PR and push

Workflow file:

- `.github/workflows/ci.yml`

Checks:

- `yamllint` across repo YAML, excluding the encrypted vault file
- `shellcheck` for automation shell scripts
- `ansible-playbook --syntax-check` for key playbooks

Purpose:

- catch broken YAML before merge
- catch shell script regressions before merge
- catch Ansible syntax errors before merge

## CD: how production deploys work

Workflow file:

- `.github/workflows/deploy-minecraft-production.yml`

Trigger:

- manual `workflow_dispatch`

Execution model:

1. Run syntax validation on a GitHub-hosted runner.
2. Require a self-hosted runner labeled `ws1`.
3. Optionally add a protected GitHub `production` environment in repository settings.
4. Optionally run `--check --diff` before deploy.
5. Run `./scripts/deploy-media1.sh` on `ws1`.
6. Run post-deploy service/log verification.

## Recommended branch and promotion flow

1. Create a feature branch.
2. Make changes locally.
3. Run local validation before pushing.
4. Open a pull request.
5. Let CI pass.
6. Review and merge to `main`.
7. Trigger the production deploy workflow manually.
8. Approve the `production` environment if you have enabled it in repository settings.
9. Review health checks after deploy.

## Recommended local pre-push checks

From `automation/ansible`:

```bash
ansible-playbook -i inventories/lab/hosts.yml playbooks/deploy-minecraft.yml --limit media1 --syntax-check
ansible-playbook -i inventories/lab/hosts.yml playbooks/diagnose-minecraft.yml --limit media1 --syntax-check
```

From repo root if tools are installed:

```bash
yamllint -c .yamllint.yml .
find automation -type f \( -name '*.sh' -o -path '*/scripts/*' \) -print0 | xargs -0 -r shellcheck
```

## Self-hosted runner requirements

The `ws1` runner should have:

- GitHub Actions runner installed and registered with labels `self-hosted` and `ws1`
- Ansible available
- access to `~/.config/homelab-secrets/ansible-vault-pass.txt`
- access to `~/.config/homelab-secrets/ansible-vault-pass.sha256`
- SSH/network reachability to `media1`

## Production safety notes

- Keep production deploys manual, not auto-triggered on merge.
- Add GitHub environment protection for `production` once the environment is created in repository settings.
- Keep `run_check_mode` enabled by default.
- Treat `./scripts/deploy-media1.sh` as the only supported production deploy entrypoint.
- If a live incident requires direct host fixes, convert them back into Ansible before the next deploy.