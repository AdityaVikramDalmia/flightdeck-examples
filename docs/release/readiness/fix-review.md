# Independent review of C1, E1, and E2 repairs

The corrected candidate is pinned in [candidate-manifest.json](candidate-manifest.json).
Gate Runner's implementation fix is
`3c246b7b831e7002afb7f6d353ca4ee8b5f8dafc`; its tested tip
`43583e250f84e273403dd3eb434a345d43e67edc` adds a documentation receipt.
Examples' implementation fix is
`cc4c615784e7e2336c2674997ab63e2d1641d2e1`; its tested tip
`1ff8feaaa0b31b634042372e2f04eb2346b0b10a` adds timestamped validation evidence.

## C1: cancellation at the completion boundary

The independent source review checked `supervise` and both new regression
methods. Signal handlers remain active through the final input snapshot. After
the foreground command is reaped, the child reference is cleared, so the final
validation stage no longer targets a historical process-group identifier.
`pthread_sigmask` then blocks TERM/INT/HUP before the final interruption check and
terminal publication. A cancellation accepted before this boundary yields error;
signals arriving after completion do not change the chosen verdict.

`test_final_snapshot_cancellation_cannot_be_reused_as_pass` exercises each of
TERM/INT/HUP against an owned synthetic supervisor while its final Git check runs.
It asserts tool exit 6, error state, retained actual command exit 0, matching
supervisor identity, and cached error reuse. The post-boundary test sends real
signals within an owned subprocess at publication, verifies they remain pending,
and verifies PASS. These are two unittest methods with subcases, not six new
standalone tests or a claim about every possible machine-failure boundary.

## E1: failed final ledger query

The final `live` query is now assigned with a checked command status before its
output is tested for emptiness. A query error therefore cannot be mistaken for
an empty live-session set and cannot reach the PASS line. The added smoke method
injects failed `live`, failed `validate`, and nonempty successful `live` output.
Each must fail, omit PASS, and clean its owned fixture. The ordinary demo remains
the successful empty-query control.

## E2: cleanup ownership

Cleanup now selects PIDs from its fixture's attempt metadata instead of scanning
all machine processes for a matching substring. It compares the complete live
interpreter, resolved Gate Runner script, exact attempt path and two numeric
file descriptors, then rechecks metadata/PID command identity immediately before
signalling. The macOS interpreter spelling is taken from the cleanup process's
own `ps` identity. Ambiguous ownership fails cleanup and retains the fixture.

The added smoke case retains both an exact-path diagnostic decoy and a neighboring
path control; it also checks misleading metadata. A separate startup smoke method checks
missing supervisor identity.
The existing detached-supervisor interruption test remains the positive cleanup
control. These cases create and terminate only their own subprocesses. They do
not replay the earlier blocked wider experiments.

Process inspection and signalling remain separate operations. Atomic PID-reuse
protection, malicious metadata writers, SIGKILL and machine failure are not
established by these tests. This repair narrows the documented trusted synthetic
fixture operation; it is not a general process-authentication mechanism.

The source review found no new blocker in these focused changes. All named regression methods passed in the independent fresh-clone runs on both
macOS and Linux. [Execution results](validation.md) retain exact platform, commit
and count units.
