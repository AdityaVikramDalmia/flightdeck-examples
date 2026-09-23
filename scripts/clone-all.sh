#!/usr/bin/env bash
# Clone the eleven tool repositories beside this checkout under the short
# directory names in docs/getting-started/checkouts.md.
# Usage: scripts/clone-all.sh [parent-dir]   (default: this checkout's parent)
# FLIGHTDECK_CLONE_BASE replaces https://github.com/AdityaVikramDalmia/ as the URL base.
# An existing directory is never modified; a differing origin or non-Git
# directory is reported on stderr and skipped.
# Exit: 0 every directory present; 1 a clone failed (the rest are still
# attempted); 2 usage error.
set -eu

usage="usage: scripts/clone-all.sh [parent-dir]"
case "${1-}" in
  -h|--help) echo "$usage"; exit 0 ;;
  -*) echo "$usage" >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
  echo "$usage" >&2
  exit 2
fi

checkout=$(cd "$(dirname "$0")/.." && pwd)
parent=${1:-$(dirname "$checkout")}
base=${FLIGHTDECK_CLONE_BASE:-https://github.com/AdityaVikramDalmia/}
base=${base%/}
unset GIT_DIR GIT_WORK_TREE
# Fail fast instead of prompting when a repository is missing or private.
export GIT_TERMINAL_PROMPT=0

status=0
for name in gate-runner durable-mailbox session-ledger agent-file-guards worktree-guard shell-lock \
    repo-health job-heartbeat config-baseline review-receipts decision-ledger; do
  url="$base/flightdeck-$name.git"
  dir="$parent/$name"
  if [ -e "$dir" ] || [ -L "$dir" ]; then
    if [ ! -e "$dir/.git" ]; then
      echo "warning: $dir exists but is not a Git checkout; left unchanged" >&2
      continue
    fi
    origin=$(git -C "$dir" remote get-url origin 2>/dev/null || true)
    if [ "${origin%.git}" = "${url%.git}" ]; then
      echo "present $name"
    else
      echo "warning: $dir has origin '${origin:-none}', expected $url; left unchanged" >&2
    fi
  elif git clone --quiet -- "$url" "$dir"; then
    echo "cloned  $name"
  else
    echo "error: could not clone $url into $dir" >&2
    status=1
  fi
done
exit "$status"
