# Examples failure-boundary review

Reviewed revision: `82a1c018410cc9c0c745296119c7137cc2787f45`.
The executable sources are unchanged from the prepared examples revision
`3c6909d0b291218c442eb610f8792c5bce063147`; intervening commits concern evidence.

- [E1: final ledger query failure is reported as PASS](live-query-failure.md)
- [E2: cleanup mistakes diagnostic text for process ownership](cleanup-identity.md)
- [Executable synthetic reproducer](reproduce.py)
- [Observed result from the completed invocation](observed.json)

From this repository, with the sibling collection at `..`:

```sh
python3 docs/correctness-review/examples/reproduce.py --tools-root ..
```

The script exits zero when both defects and their controls reproduce. It is a
defect demonstrator, not a passing correctness test. Each case creates a new
temporary root and empty HOME; the command wrappers, state, and signalled children
belong to that fixture. Components are invoked from their clean source checkouts,
with bytecode writes disabled. No runtime implementation is patched.

The first invocation completed both E1 cases but failed to exercise E2 because
the macOS temporary path had the `/var` spelling while cleanup canonicalized it
to `/private/var`. The fixture was corrected to use its resolved path. A complete
subsequent invocation exited 0 and produced `observed.json`. This initial fixture
failure is not a product defect. All children were reaped in both invocations.

Review also read the smoke suite, all four recipe wrappers, validation harness,
catalog contracts, and release receipts. No finding is asserted about the
validation harness merely because its cleanliness field describes the starting
checkout; release receipts separately record before/after state. No Linux replay
or machine-failure durability experiment was performed.
