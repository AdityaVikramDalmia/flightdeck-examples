#!/usr/bin/env bash
# Deprecated reference example for new Claude Code integrations (2026-09-22).
# Compose all six tools against one disposable local fixture. No network or AI process is used.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: end-to-end-demo.sh [--tools-root DIR]

Resolve sibling tool checkouts from --tools-root, FLIGHTDECK_TOOLS_ROOT, or the
directory two levels above this script. All mutable state lives in one mktemp tree.
EOF
}
die() { printf 'end-to-end-demo: %s\n' "$*" >&2; exit 1; }

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
tools_root=${FLIGHTDECK_TOOLS_ROOT:-$(cd "$script_dir/../.." && pwd)}
while [ "$#" -gt 0 ]; do
  case "$1" in
    --tools-root) [ "$#" -ge 2 ] || die "--tools-root needs a directory"; tools_root=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done
tools_root=$(cd "$tools_root" 2>/dev/null && pwd -P) || die "cannot resolve tools root"

GATE="$tools_root/gate-runner/bin/gate-run"
MAILBOX="$tools_root/durable-mailbox/bin/mailbox"
LEDGER="$tools_root/session-ledger/bin/session-ledger"
SHRINK="$tools_root/agent-file-guards/bin/shrink-guard.sh"
NUL_LINT="$tools_root/agent-file-guards/bin/nul-lint.sh"
INTAKE="$tools_root/agent-file-guards/bin/untrusted-intake.sh"
WORKTREE_GUARD="$tools_root/worktree-guard/bin/worktree-guard"
SHELL_LOCK="$tools_root/shell-lock/bin/shell-lock"
REPO_HEALTH="$tools_root/repo-health/bin/repo-health"
for executable in "$GATE" "$MAILBOX" "$LEDGER" "$SHRINK" "$NUL_LINT" "$INTAKE" "$WORKTREE_GUARD" "$SHELL_LOCK"; do
  [ -x "$executable" ] || die "required executable is missing: $executable"
done
for dependency in git jq python3 make perl; do command -v "$dependency" >/dev/null 2>&1 || die "missing dependency: $dependency"; done

fixture=$(mktemp -d "${TMPDIR:-/tmp}/flightdeck-example.XXXXXX") || die "cannot create fixture"
case "$fixture" in "${TMPDIR:-/tmp}"/flightdeck-example.*) ;; *) die "unexpected fixture path" ;; esac
pids=
cleanup() {
  # These PIDs are direct children, never discovered from user-level state.
  for pid in $pids; do kill -TERM "$pid" 2>/dev/null || :; done
  for pid in $pids; do wait "$pid" 2>/dev/null || :; done
  # Gate Runner detaches its supervisor. On interruption, terminate only a
  # supervisor whose live argv names an attempt inside this exact fixture.
  python3 "$script_dir/cleanup-gate.py" "$fixture" || return 1
  rm -rf -- "$fixture"
}
trap cleanup EXIT
trap 'exit 130' HUP INT TERM

# Ignore caller Git routing, injected config, templates, and Make overrides.
# Runtime executables on PATH are trusted; this is a fixture, not a sandbox.
while IFS= read -r variable; do
  case "$variable" in GIT_*) unset "$variable" ;; esac
done < <(compgen -e)
unset MAKEFLAGS MFLAGS MAKEFILES GNUMAKEFLAGS MAILBOX_BY MAILBOX_FROM
export MAILBOX_LOCK_WAIT_S=5 SESSION_LEDGER_LOCK_WAIT_S=5
# Keep Git and Python from consulting or modifying user-level state or sibling checkouts.
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_TERMINAL_PROMPT=0
export GIT_AUTHOR_NAME='Fixture User'
export GIT_AUTHOR_EMAIL='fixture@example.invalid'
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
export PYTHONDONTWRITEBYTECODE=1
export GIT_TEMPLATE_DIR="$fixture/empty-template"
mkdir -p "$GIT_TEMPLATE_DIR"

main="$fixture/main project"
lane="$fixture/feature worktree"
ledger_dir="$fixture/ledger state"
mailbox_dir="$fixture/mailbox state"
lock_file="$fixture/locks/integration.lock"
mkdir -p "$main/docs"
git init -q -b main "$main" || die "git init failed"
git -C "$main" config core.hooksPath /dev/null
git -C "$main" config commit.gpgsign false
cat > "$main/.gitignore" <<'EOF'
.demo-output/
EOF
cat > "$main/docs/guide.md" <<'EOF'
# Release guide

Prepare the local fixture, validate the document bytes, run the project checks,
and retain receipts for the result. The example uses no remote services.
EOF
cat > "$main/Makefile" <<'EOF'
.PHONY: test
test:
	@test -s docs/guide.md
	@grep -q 'Reviewed through the guarded workflow' docs/guide.md
	@mkdir -p .demo-output
	@printf 'gate execution\n' >> .demo-output/count
EOF
git -C "$main" add .
git -C "$main" commit -qm 'initial fixture'
git -C "$main" worktree add -qb task "$lane" >/dev/null

printf '[1/7] record the synthetic session launch\n'
"$LEDGER" --dir "$ledger_dir" append launched demo-session --by example project=local-fixture >/dev/null \
  || die "ledger launch failed"

printf '[2/7] statically inspect an untrusted carrier without executing it\n'
incoming="$fixture/untrusted checkout"
sentinel="$fixture/MUST-NOT-EXIST"
mkdir -p "$incoming/.claude/hooks"
cat > "$incoming/.claude/hooks/on-open.sh" <<EOF
#!/bin/sh
touch "$sentinel"
EOF
chmod +x "$incoming/.claude/hooks/on-open.sh"
if intake_output=$("$INTAKE" "$incoming" 2>&1); then intake_rc=0; else intake_rc=$?; fi
[ "$intake_rc" -eq 3 ] || die "intake scan should report the carrier"
printf '%s' "$intake_output" | grep -q CARRIER || die "intake report omitted carrier"
[ ! -e "$sentinel" ] || die "untrusted checkout code was executed"

printf '[3/7] install a byte-checked edit and lint tracked text bytes\n'
tiny="$fixture/truncated candidate.md"
printf 'oops\n' > "$tiny"
if "$SHRINK" --min-percent 70 --discard-rejected --audit-log "$fixture/shrink-audit.tsv" --from "$tiny" "$lane/docs/guide.md" >"$fixture/rejection.log" 2>&1; then
  die "shrink guard accepted a destructive rewrite"
else
  [ "$?" -eq 3 ] || die "shrink guard failed for an unexpected reason"
fi
cmp "$main/docs/guide.md" "$lane/docs/guide.md" || die "rejected rewrite changed the target"
printf 'bad\000text\n' > "$lane/docs/nul-probe.txt"
if (cd "$lane" && "$NUL_LINT" --path docs/nul-probe.txt --quiet) >"$fixture/nul.log" 2>&1; then
  die "NUL lint accepted a literal NUL"
else
  [ "$?" -eq 3 ] || die "NUL lint failed for an unexpected reason"
fi
rm -f -- "$lane/docs/nul-probe.txt"
candidate="$fixture/guide candidate.md"
cp -f "$lane/docs/guide.md" "$candidate"
printf '\nReviewed through the guarded workflow.\n' >> "$candidate"
"$SHRINK" --min-percent 70 --from "$candidate" --label integration-demo "$lane/docs/guide.md" \
  || die "guarded edit failed"
(cd "$lane" && "$NUL_LINT" --quiet) || die "NUL lint failed"
git -C "$lane" add docs/guide.md
git -C "$lane" commit -qm 'guarded documentation edit'

printf '[4/7] run real project checks once and reuse the durable result\n'
first_gate=$(cd "$lane" && "$GATE" --json start --wait -- make test) || die "first gate run failed"
second_gate=$(cd "$lane" && "$GATE" --json start --wait -- make test) || die "cached gate lookup failed"
gate_attempt=$(printf '%s' "$first_gate" | python3 -c 'import json,sys; print(json.load(sys.stdin)["attempt"])') || die "cannot read gate receipt"
printf '%s\n%s\n' "$first_gate" "$second_gate" | jq -se 'all(.[]; .state == "pass" and .exit_code == 0)' >/dev/null \
  || die "gate receipts do not describe successful commands"
second_attempt=$(printf '%s' "$second_gate" | python3 -c 'import json,sys; print(json.load(sys.stdin)["attempt"])') || die "cannot read cached gate receipt"
[ "$gate_attempt" = "$second_attempt" ] || die "identical gate requests did not reuse one attempt"
[ "$(wc -l < "$lane/.demo-output/count" | tr -d ' ')" -eq 1 ] || die "cached gate command executed more than once"

printf '[5/7] publish completion evidence, drain it, and acknowledge the question\n'
"$MAILBOX" --dir "$mailbox_dir" send reviewer verdict 'Project checks passed.' --from demo \
  "receipt=gate:$gate_attempt" >/dev/null || die "verdict send failed"
ask_path=$("$MAILBOX" --dir "$mailbox_dir" send reviewer ask 'Acknowledge the completion receipt?' --from demo) \
  || die "ask send failed"
ask_id=${ask_path##*/}
mail_batch=$("$MAILBOX" --dir "$mailbox_dir" drain reviewer --format json) || die "mailbox drain failed"
printf '%s' "$mail_batch" | jq -se --arg receipt "gate:$gate_attempt" --arg ask "$ask_id" '
  length == 2 and any(.[]; .kind == "verdict" and .receipt == $receipt) and any(.[]; .kind == "ask" and .id == $ask)
' >/dev/null || die "drain omitted a message or changed its receipt"
"$MAILBOX" --dir "$mailbox_dir" history reviewer | jq -se 'length == 2' >/dev/null || die "drain did not retain both messages"
"$MAILBOX" --dir "$mailbox_dir" ack reviewer "$ask_id" --from reviewer >/dev/null || die "ack failed"
open_asks=$("$MAILBOX" --dir "$mailbox_dir" asks reviewer) || die "open-ask query failed"
case "$open_asks" in *"$ask_id"*) die "acknowledged ask remains open" ;; esac

printf '[6/7] serialize preflight, merge, removal, and a contention probe\n'
rm -rf -- "$lane/.demo-output"
serial_log="$fixture/serialization.log"
pids=
for worker in one two; do
  "$SHELL_LOCK" --timeout 5 "$lock_file" -- sh -c \
    'printf "start %s\n" "$1" >> "$2"; sleep 0.1; printf "finish %s\n" "$1" >> "$2"' \
    _ "$worker" "$serial_log" &
  pids="$pids $!"
done
for pid in $pids; do wait "$pid" || die "serialized worker failed"; done
pids=
awk '
  $1 == "start" { if (open != "") exit 1; open=$2; starts++ }
  $1 == "finish" { if (open != $2) exit 1; open=""; finishes++ }
  END { if (open != "" || starts != 2 || finishes != 2) exit 1 }
' "$serial_log" || die "locked commands overlapped"

"$SHELL_LOCK" --timeout 5 "$lock_file" -- sh -c '
  guard=$1; main=$2
  "$guard" merge-check "$main" --base main --branch task --json >/dev/null || exit $?
  git -C "$main" -c core.hooksPath=/dev/null merge --ff-only task >/dev/null
' _ "$WORKTREE_GUARD" "$main" || die "guarded merge failed"

printf 'keep me\n' > "$lane/untracked-work.txt"
if "$WORKTREE_GUARD" remove-check "$lane" --base main --json >"$fixture/remove-refusal.json"; then
  die "removal preflight accepted untracked work"
else
  [ "$?" -eq 3 ] || die "removal preflight failed for an unexpected reason"
fi
[ -f "$lane/untracked-work.txt" ] || die "preflight mutated the worktree"
if [ -x "$REPO_HEALTH" ]; then
  "$REPO_HEALTH" --json "$main" "$lane" >"$fixture/health.json" || die "repository health inspection failed"
  jq -e 'length == 2 and .[0].cleanliness == "clean" and .[1].cleanliness == "dirty" and all(.[]; .sync == "unknown")' \
    "$fixture/health.json" >/dev/null || die "repository health report missed fixture states"
  printf '      optional seventh repository: health report verified\n'
fi
rm -f -- "$lane/untracked-work.txt"

"$SHELL_LOCK" --timeout 5 "$lock_file" -- sh -c '
  guard=$1; main=$2; lane=$3
  "$guard" remove-check "$lane" --base main --json >"$main/../remove-approval.json" || exit $?
  git -C "$main" worktree remove "$lane"
' _ "$WORKTREE_GUARD" "$main" "$lane" || die "guarded worktree removal failed"
[ ! -e "$lane" ] || die "linked worktree still exists"
grep -q 'Reviewed through the guarded workflow' "$main/docs/guide.md" || die "merge did not retain guarded edit"

printf '[7/7] finish and validate the lifecycle record\n'
"$LEDGER" --dir "$ledger_dir" append finished demo-session --by example result=passed \
  "gate_attempt=$gate_attempt" >/dev/null || die "ledger finish failed"
"$LEDGER" --dir "$ledger_dir" validate >/dev/null || die "ledger validation failed"
"$LEDGER" --dir "$ledger_dir" history demo-session | jq -se --arg attempt "$gate_attempt" '
  length == 2 and .[0].event == "launched" and .[1].event == "finished" and .[1].gate_attempt == $attempt
' >/dev/null || die "ledger history lost lifecycle or gate evidence"
[ -z "$("$LEDGER" --dir "$ledger_dir" live)" ] || die "finished session remains live"

printf 'PASS: six repositories composed in one isolated local workflow\n'
