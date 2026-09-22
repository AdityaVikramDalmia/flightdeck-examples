# Private candidate: 2026-09-22

Eleven independent tool repositories provide thirteen command-line utilities.
This companion contains their portfolio case studies, a machine-readable catalog,
reproducible local workflows, and validation receipts.

All component commits in [the manifest](validation/component-commits.json) passed
their own suites on macOS and isolated Linux. Fresh private-remote clones passed
tests and installation/example checks and remained clean. The full composition
demo and all four additional recipes passed in Linux without networking.

Test cases, grouped regressions, and individual shell assertions are reported
separately. Four case-insensitive-filesystem tests are exercised on macOS and
skipped on Linux; they are not silently counted as Linux passes.

Every repository remains private. Redistribution licensing has not been selected.
The full original agent runtime, private infrastructure, source Git history,
personal transcripts, project roster, and operational ledgers are outside this
distribution. No portfolio site deployment or public visibility change was made.

Useful portfolio starting points are Gate Runner, Worktree Guard, Decision Ledger,
and Review Receipts: their examples expose concrete coordination, state, and
verification problems. The [portfolio index](docs/portfolio/README.md) contains
the complete set. Use each tool's own documented limits when presenting it;
none of the receipts certify semantic correctness or authenticate a reviewer.

Individual tool repositories contain manual GitHub workflows. They do not run on
push, and no cloud workflow was dispatched during preparation. Local validation
uses the [documented harness](validation/README.md).
