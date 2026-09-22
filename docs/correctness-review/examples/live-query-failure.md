# E1: failed final ledger query still prints PASS

**Severity: medium. Status: reproduced with a failing-query control.**

At [end-to-end-demo.sh](../../../examples/end-to-end-demo.sh), line 227 puts the
`session-ledger live` invocation inside a string-emptiness test. A failed query
with empty stdout makes that test succeed. Its exit status is discarded; Bash's
`set -e` does not propagate it through the successful outer test. The next line
prints the overall PASS message and the script exits zero.

The reproducer substitutes a fixture-local CLI wrapper that delegates every
operation to the real Session Ledger except `live`. That query emits a diagnostic
and exits 75, without claiming an empty successful result. The complete demo
still exits 0 and prints PASS. The same wrapper failing `validate` instead makes
the demo exit 1 without PASS, establishing that the injection is reached and that
other verification failures do propagate. Both runs remove their fixtures.

This is deterministic dependency-failure injection. It proves the caller loses
the exit status; it does not claim a naturally occurring storage failure was
observed or that Session Ledger itself is defective. An I/O or malformed-state
error between validation and the final query must not mean there are no live
sessions.

Exact revision, command and outputs are indexed in [README](README.md) and
[observed.json](observed.json), under `E1_live_failure` and
`E1_validate_failure_control`.

Repair direction: capture the query output in an assignment whose return status
is checked, then test whether the successful output is empty. This is a review
recommendation only; no implementation fix was created. Any fix belongs in an
isolated worktree with this error-propagation case as a regression check.
