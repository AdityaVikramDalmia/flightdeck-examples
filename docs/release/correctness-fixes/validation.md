# Validation and receipt interpretation

The exact historical defect demonstrator was run against examples base revision
`6ad9597e5ed481e4efaf0f89cd0b59aafac3c7db` before editing. It reproduced E1
(exit 0 with PASS after a live-query error), the validate-error control (exit 1,
no PASS), and E2 (diagnostic sleeper exited by SIGTERM; neighbor survived).
The original demonstrator intentionally asserts defective behavior and is not a
post-fix correctness test.

The new regression checks live in `tests/smoke.py`. Validation uses the sibling
tool collection explicitly through `FLIGHTDECK_TOOLS_ROOT`, because the isolated
release worktree is nested beneath that collection. Required commands are
`make test` and `make demo`. The smoke result counts unittest test methods;
subtests and the four optional recipes are recorded separately when available.

The first development suite ran 10 test methods and found one failure: macOS
framework Python's live interpreter name differed from `sys.executable`, so the
initial identity check conservatively retained the real-supervisor fixture.
After accounting for that platform behavior, the focused interrupted-supervisor
test passed (1 method). Final timestamped receipts are added in an evidence-only
commit and name the exact implementation revision and executed source hashes.
Fresh receipts describe this host only. Historical Linux receipts are not a
Linux validation of these fixes. No automated safety rejection occurred in this
fix lane; previously blocked review probes were not retried.

Final checks at implementation revision `cc4c615` passed on macOS:
`make test` ran **10 unittest methods, zero skips**, including three ledger
injection subcases and all four optional recipe executions; `make demo` passed
one full workflow invocation. Exact UTC timestamps, elapsed times, complete
command outputs, component revisions, and implementation/test hashes are in
[host-validation.json](host-validation.json). The newly timestamped baseline
[replay](baseline-reproduction.json) independently re-established both defects
and their controls at `6ad9597`; it is separate from the older review evidence.
