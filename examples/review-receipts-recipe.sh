#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TOOLS_ROOT=${FLIGHTDECK_TOOLS_ROOT:-$(cd "$ROOT/.." && pwd)}
TOOL="$TOOLS_ROOT/review-receipts/bin/review-receipts"
[ -x "$TOOL" ] || { printf 'missing review-receipts checkout\n' >&2; exit 1; }
export PYTHONDONTWRITEBYTECODE=1
fixture=$(mktemp -d "${TMPDIR:-/tmp}/review-receipts-recipe.XXXXXX")
trap 'rm -rf -- "$fixture"' EXIT
trap 'exit 130' INT HUP TERM
mkdir "$fixture/project"
printf 'A proposed retry policy.\n' > "$fixture/project/design.txt"
printf 'retries=3\n' > "$fixture/project/settings.conf"
printf 'Reject this version.\nThe timeout behavior still needs review.\n\n' > "$fixture/notes.txt"
"$TOOL" author --root "$fixture/project" --file design.txt --file settings.conf \
  --receipt "$fixture/review.json" --reviewer 'Synthetic reviewer' --label 'Retry policy' \
  --verdict 'reject' --notes-file "$fixture/notes.txt" --evidence 'fixture:timeout-question' --json >/dev/null
"$TOOL" check --root "$fixture/project" --file design.txt --file settings.conf \
  --receipt "$fixture/review.json" --json > "$fixture/current.json"
python3 - "$fixture/current.json" "$fixture/notes.txt" <<'PY'
import json,pathlib,sys
result=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert result["status"]=="valid" and result["checked_files"]==2
assert result["review"]["verdict"]=="reject"
assert result["review"]["notes"]==pathlib.Path(sys.argv[2]).read_text()
PY
# Exit zero above established a matching binding, not reviewer approval.
printf 'retries=4\n' > "$fixture/project/settings.conf"
if "$TOOL" check --root "$fixture/project" --file design.txt --file settings.conf \
  --receipt "$fixture/review.json" --json > "$fixture/stale.json"; then
  printf 'modified settings incorrectly matched the review\n' >&2; exit 1
else
  [ "$?" -eq 3 ]
fi
python3 - "$fixture/stale.json" <<'PY'
import json,pathlib,sys
result=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert result["status"]=="stale" and result["review"]["verdict"]=="reject"
assert any(row["path"]=="settings.conf" and "sha256" in row["fields"] for row in result["findings"])
PY
printf 'PASS: rejecting verdict preserved; matching bytes are current, changed bytes stale; no approval inferred\n'
