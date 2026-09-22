# E2: cleanup treats command-line text as supervisor ownership

**Severity: medium. Status: reproduced with a neighboring-path control.**

[cleanup-gate.py](../../../examples/cleanup-gate.py), lines 21–25, accepts any
command line containing `_supervise <fixture>/main project/.git/gate-runner/runs/`.
Lines 39–42 repeat that same substring test and send SIGTERM. Neither check
establishes that the process is a Gate Runner supervisor, that the string is the
supervisor's argument, or that it corresponds to an existing attempt.

The reproducer starts an ordinary Python sleeper with a diagnostic argument
containing that string. It creates no Gate Runner attempt and starts no supervisor.
Running the real cleanup script terminates the sleeper with SIGTERM (exit -15)
and returns success. A second ordinary sleeper carrying a neighboring fixture
path survives. This isolates the ownership predicate from general process exit
or broad prefix matching. The harness terminates and reaps the surviving child.

Expected: an ordinary process that merely quotes an invocation is left alone.
Actual: text mentioning the exact fixture is enough to select it for termination.
The affected scenario requires a process command line to contain the exact
fixture path, such as a diagnostic or wrapper argument. This does not demonstrate
arbitrary process selection, a PID-reuse race, or any effect on a live user
process; all observed processes were synthetic children.

Exact revision, command and outputs are indexed in [README](README.md) and
[observed.json](observed.json), under `E2_cleanup_identity`.

Repair direction: retain explicit supervisor identities/attempt records and
verify the expected executable and argument structure before signalling; a raw
substring is insufficient proof of ownership. No patch was implemented or
validated. Any repair requires an isolated worktree and regression checks for
real interrupted supervisors as well as unrelated diagnostic processes.
