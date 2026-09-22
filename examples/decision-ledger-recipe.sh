#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TOOLS_ROOT=${FLIGHTDECK_TOOLS_ROOT:-$(cd "$ROOT/.." && pwd)}
TOOL="$TOOLS_ROOT/decision-ledger/bin/decision-ledger"
[ -x "$TOOL" ] || { printf 'missing decision-ledger checkout\n' >&2; exit 1; }
export PYTHONDONTWRITEBYTECODE=1
fixture=$(mktemp -d "${TMPDIR:-/tmp}/decision-ledger-recipe.XXXXXX")
trap 'rm -rf -- "$fixture"' EXIT
trap 'exit 130' INT HUP TERM
store="$fixture/decision state"
"$TOOL" --dir "$store" init >/dev/null
printf 'Do not merge until review is complete.\r\nKeep these original words — exactly.\r\n\r\n' > "$fixture/original.txt"
"$TOOL" --dir "$store" record --words-file "$fixture/original.txt" \
  --source paste --actor operator --interpretation 'Review remains a separate requirement.' > "$fixture/decision.json"
decision_id=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])' < "$fixture/decision.json")
"$TOOL" --dir "$store" record 'Correction: require both tests and review before merge.' \
  --corrects "$decision_id" --actor operator --interpretation 'Both checks are required.' > "$fixture/correction.json"
"$TOOL" --dir "$store" history "$decision_id" > "$fixture/decision-history.json"
"$TOOL" --dir "$store" ask 'May the fixture proceed?' --actor worker > "$fixture/question.json"
question_id=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])' < "$fixture/question.json")
"$TOOL" --dir "$store" open > "$fixture/open-before.json"
"$TOOL" --dir "$store" answer "$question_id" 'Wait for the review result.' \
  --actor operator --interpretation 'Blocked pending review.' > "$fixture/first-answer.json"
"$TOOL" --dir "$store" answer "$question_id" 'Keep waiting; the review still rejects this version.' \
  --actor operator --interpretation 'Latest response remains a refusal.' > "$fixture/latest-answer.json"
"$TOOL" --dir "$store" history "$question_id" > "$fixture/question-history.json"
"$TOOL" --dir "$store" open > "$fixture/open-after.json"
"$TOOL" --dir "$store" validate > "$fixture/validation.json"
python3 - "$fixture" <<'PY'
import json,pathlib,sys
root=pathlib.Path(sys.argv[1])
def read(name):
    return json.loads((root/name).read_text())
decision=read("decision.json")
history=read("decision-history.json")
assert decision["words"]==(root/"original.txt").read_bytes().decode("utf-8")
assert decision["interpretation"]=="Review remains a separate requirement."
assert history["root"]==decision and history["events"][0]==decision
assert len(history["events"])==2 and history["current"]==read("correction.json")
question=read("question.json")
assert read("open-before.json")==[question]
answers=read("question-history.json")
assert answers["root"]==question and answers["events"]==[question,read("first-answer.json"),read("latest-answer.json")]
assert answers["current"]==read("latest-answer.json")
assert answers["current"]["words"]=="Keep waiting; the review still rejects this version."
assert read("open-after.json")==[]  # Answered does not mean approved.
assert read("validation.json")=={"valid":True,"records":5}
PY
printf 'PASS: original words and interpretation stay separate; corrections and both answers retain history; answered is not approved\n'
