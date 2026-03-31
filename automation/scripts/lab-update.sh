#!/usr/bin/env bash
# =============================================================================
# lab-update.sh — Lab update and commit helper
# Usage: bash automation/scripts/lab-update.sh
# =============================================================================

set -euo pipefail

REPO_DIR="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
DATE=$(date +%Y-%m-%d)
DAILY_LOG="$REPO_DIR/build-log/daily-log.md"
CHANGE_LOG="$REPO_DIR/build-log/change-log.md"

# --- Colours -----------------------------------------------------------------
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

divider() { echo -e "${CYAN}──────────────────────────────────────────${RESET}"; }
header()  { echo -e "\n${BOLD}${GREEN}$1${RESET}"; divider; }
prompt()  { echo -e "${YELLOW}$1${RESET}"; }

# --- Helpers -----------------------------------------------------------------
ask() {
    local __var=$1
    local __msg=$2
    local __default=${3:-}
    prompt "$__msg"
    [ -n "$__default" ] && echo -e "  (press Enter to skip)"
    read -r value
    eval "$__var='$value'"
}

confirm() {
    prompt "$1 [y/N]: "
    read -r ans
    [[ "$ans" =~ ^[Yy]$ ]]
}

# --- Menu --------------------------------------------------------------------
show_menu() {
    header "🧪 Lab Update Script"
    echo "  1) Daily log entry"
    echo "  2) Change log entry"
    echo "  3) Tick off a phase task"
    echo "  4) All of the above"
    echo "  5) Quick commit + push (no log changes)"
    echo "  q) Quit"
    divider
    prompt "Choose an option: "
    read -r choice
    echo "$choice"
}

# --- Daily log ---------------------------------------------------------------
daily_log_entry() {
    header "📓 Daily Log — $DATE"

    ask phase     "Phase (e.g. Phase 0 — Foundation):"
    ask time_spent "Time spent (e.g. ~2h):"
    ask worked_on  "What did you work on?"
    ask changed    "What did you change? (Enter to skip)"
    ask worked     "What worked?"
    ask failed     "What failed? (Enter to skip)"
    ask learned    "What did you learn?"
    ask next_step  "What is the next step?"

    cat >> "$DAILY_LOG" <<EOF

## $DATE

**Phase:** ${phase:-—}
**Time spent:** ${time_spent:-—}

### What I worked on
${worked_on:-—}

### What I changed
${changed:-n/a}

### What worked
${worked:-—}

### What failed
${failed:-n/a}

### What I learned
${learned:-—}

### Next step
${next_step:-—}
EOF

    echo -e "${GREEN}✔ Daily log updated${RESET}"
}

# --- Change log --------------------------------------------------------------
change_log_entry() {
    header "📋 Change Log — $DATE"

    ask added   "Added (Enter to skip):"
    ask changed "Changed (Enter to skip):"
    ask fixed   "Fixed (Enter to skip):"
    ask broke   "Broke (Enter to skip):"

    cat >> "$CHANGE_LOG" <<EOF

## $DATE

### Added
${added:-- n/a}

### Changed
${changed:-- n/a}

### Fixed
${fixed:-- n/a}

### Broke
${broke:-- n/a}
EOF

    echo -e "${GREEN}✔ Change log updated${RESET}"
}

# --- Phase task tick-off -----------------------------------------------------
tick_phase_task() {
    header "✅ Tick Off a Phase Task"

    echo "Available phase files:"
    local i=1
    local files=()
    while IFS= read -r f; do
        echo "  $i) $(basename "$f")"
        files+=("$f")
        ((i++))
    done < <(find "$REPO_DIR/phases" -name "*.md" | sort)

    prompt "Pick a phase file number: "
    read -r num
    local chosen="${files[$((num-1))]}"
    echo -e "File: ${CYAN}$(basename "$chosen")${RESET}\n"

    echo "Open tasks:"
    local j=1
    local tasks=()
    while IFS= read -r line; do
        echo "  $j) $line"
        tasks+=("$line")
        ((j++))
    done < <(grep -n '^\- \[ \]' "$chosen" | sed 's/^/Line /')

    if [ ${#tasks[@]} -eq 0 ]; then
        echo -e "${YELLOW}No open tasks found in this file.${RESET}"
        return
    fi

    prompt "Pick a task number to mark done: "
    read -r tnum
    local task_line="${tasks[$((tnum-1))]}"
    local lineno
    lineno=$(echo "$task_line" | grep -oP '^\d+')
    local task_text
    task_text=$(echo "$task_line" | sed 's/^[0-9]*: //')

    sed -i "${lineno}s/- \[ \]/- [x]/" "$chosen"
    echo -e "${GREEN}✔ Marked done: $task_text${RESET}"
}

# --- Commit and push ---------------------------------------------------------
commit_and_push() {
    header "🚀 Commit and Push"

    cd "$REPO_DIR"

    if git diff --quiet && git diff --cached --quiet; then
        echo -e "${YELLOW}Nothing to commit.${RESET}"
        return
    fi

    echo "Files changed:"
    git --no-pager diff --name-only
    git --no-pager diff --cached --name-only
    echo ""

    ask commit_msg "Commit message:"
    if [ -z "$commit_msg" ]; then
        commit_msg="Lab update: $DATE"
    fi

    git add -A
    git commit -m "$commit_msg

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

    echo -e "${CYAN}Pushing to origin/main...${RESET}"
    if git push; then
        echo -e "${GREEN}✔ Pushed successfully${RESET}"
    else
        echo -e "${YELLOW}⚠ Push failed. You may need to authenticate.${RESET}"
        echo "  Run: git push"
        echo "  Or store credentials: git config --global credential.helper store"
    fi
}

# --- Main --------------------------------------------------------------------
main() {
    choice=$(show_menu)

    case "$choice" in
        1) daily_log_entry;  commit_and_push ;;
        2) change_log_entry; commit_and_push ;;
        3) tick_phase_task;  commit_and_push ;;
        4)
            daily_log_entry
            change_log_entry
            if confirm "Do you want to tick off a phase task too?"; then
                tick_phase_task
            fi
            commit_and_push
            ;;
        5) commit_and_push ;;
        q|Q) echo "Bye!"; exit 0 ;;
        *) echo -e "${YELLOW}Invalid option${RESET}"; exit 1 ;;
    esac
}

main
