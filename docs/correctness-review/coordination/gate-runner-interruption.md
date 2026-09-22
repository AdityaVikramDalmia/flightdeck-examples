# C1: SIGTERM during final input validation can become reusable success

**Severity: medium. Status: reproduced once; no independent replay.**

Revision: `587facdaff79fedadd1ea582f30ae5f8282874a2`.

`gate_runner/cli.py:318-322` installs a supervisor handler that records an
interruption. At lines 364-368 the supervisor chooses the command verdict, checks
the interruption flag, and then computes the final filesystem snapshot. A signal
received during that snapshot updates the flag after its last check. Lines
375-376 then publish the original pass verdict. There is no subsequent
interruption check before publication.

The lifecycle contract says SIGTERM/SIGINT/SIGHUP to the supervisor records
`error`. The executed synthetic command returned 0, but a real SIGTERM was
delivered to its supervisor while Git performed the final snapshot. `start
--wait` nevertheless returned 0 with state `pass`. A second identical start
reused that same successful attempt.

## Executed reproducer

The `signal_after_command` function in [reproduce.py](reproduce.py) creates a
fresh Git fixture and an external state directory. A fixture command writes an
external completion marker. A PATH-local Git shim sees that marker during the
supervisor's final snapshot, records its parent PID, sends SIGTERM to that PID,
then executes the real Git binary. The probe verifies the PID against the
attempt's `meta.json`, verifies pass/exit 0, and verifies same-attempt cache reuse.

This is deterministic timing injection through a synthetic executable wrapper;
it does not alter Gate Runner source or mock away signal delivery. It demonstrates
one legal signal arrival window, not its frequency under ordinary scheduling.
The command had already finished successfully: the finding concerns truthful
supervisor interruption state, not a claim that a failed command was made to pass.

The exact invocation was the combined command in [validation.md](validation.md).
Execution reached its second probe, proving every first-probe assertion completed.
The script buffers its final aggregate JSON until all probes finish, so no
standalone first-probe stdout receipt was produced. The first probe was not rerun
after the safety interruption.

## Repair direction, not an implemented fix

Recheck interruption after final snapshot computation and ensure interruption
cannot be accepted after the terminal decision while still publishing pass. The
precise completion/cancellation boundary should be documented and tested. No
source patch was prepared; any future patch requires its own isolated worktree.
