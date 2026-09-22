# Changes and regression boundaries

## E1: preserve the final query status

The demo captures `session-ledger live` in a checked assignment before inspecting
its output. A failed query cannot satisfy the empty-live-session assertion or
print the workflow PASS. Regressions inject an empty failed live query, a failed
validate query as control, and a successful but nonempty live query. All must
exit nonzero, omit PASS, and remove their disposable fixtures.

## E2: require a recorded supervisor identity

Cleanup reads only supervisor PIDs in its fixture attempt records, replacing the
machine-wide process-list substring search. Each candidate must match the entire
expected interpreter, resolved Gate Runner script path, `_supervise` operation,
exact attempt path, and two descriptor arguments. It rechecks metadata and the
live command immediately before signalling. On macOS, framework Python can
re-exec into its application executable; cleanup obtains its own live interpreter
name from `ps` rather than assuming `sys.executable` is that name.

The decoy regression starts ordinary fixture-owned Python sleepers carrying the
exact historical diagnostic text and a neighboring-path control. Both survive.
It then points synthetic stale metadata at the decoy PID: the invocation mismatch
still prevents signalling and makes cleanup retain the fixture with an error.
The existing interrupted-demo regression verifies a real supervisor and its
command stop and the fixture is removed. A separate startup regression verifies
missing supervisor identity retains the fixture.

## Limits

The fixture, installed executables, and checkout code remain trusted; this is
not a hostile-process authentication boundary. `ps` observation and `kill` are
not one atomic operation, so the immediate recheck does not eliminate PID reuse
races. Incomplete startup metadata or an unrecognized interpreter/invocation
retains the fixture instead of guessing. This can require manual inspection of
that fixture and its recorded process before disposal. SIGKILL and machine
failure bypass shell traps. The new tests do not exercise those races or failures.
All signals used in reproductions and regressions target their own synthetic
children; no real runtime, credential, ledger, or unrelated process is targeted.
