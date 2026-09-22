# Method and validation scope

The parent inventoried all twelve clean checkouts before delegation. Eleven
component HEADs exactly matched both prepared execution receipts. Examples HEAD
was `82a1c018410cc9c0c745296119c7137cc2787f45`, later than the prepared
`3c6909d0b291218c442eb610f8792c5bce063147`; the executable sources were unchanged.
[revisions.json](revisions.json) records full revisions, platform information,
local license hashes and release-input hashes. Remote privacy was taken from
the owner's instruction and the prior receipt, without a fresh remote request.

Work was grouped into coordination, filesystem/Git, and evidence/state, with the
parent reviewing examples and adjudicating results. Each subagent had at most
four primary findings, a roughly twenty-minute initial bound, and no recursive
delegation. Local source search was used; no paid retrieval service or model
gateway was invoked. The requested Astra subagents used the session's agent
facility; this is not an accounting assertion that model inference is free.

Each group read its repository instructions, named maintainer skills, command
contracts, implementation and relevant existing tests. A documented exclusion
(for example, non-atomic inspection of a live tree) was not itself a new defect.
New findings require a concrete executed outcome contrary to the relevant
contract. Deterministic dependency/scheduling injection is labelled separately
from natural race frequency or machine-failure testing.

## What executed

- Coordination's first case injected SIGTERM during Gate Runner's final Git
  snapshot, verified the signal recipient against its synthetic attempt, and
  verified the resulting PASS was reused. The next case failed a fixture
  assertion, so the aggregate command exited 1 and emitted no final result JSON.
  C1 is supported by completed assertions and parent source review, not by a
  successful aggregate run or independent replay.
- Parent examples probes completed two query-failure cases and one ownership
  case after correcting a temporary-path spelling in the harness. Their output
  is [retained](examples/observed.json). Parent source review checked the precise
  shell and cleanup paths against those observations.
- Required companion `make test` and `make demo` were run for the documentation
  change; exact results are in [validation.json](validation.json). These are
  integration/portability checks, not new experimental coverage of every tool.

Every executed fixture used disposable synthetic state and explicit paths. No
source fix was made. The examples worktree isolates all durable review edits.
The macOS host is the only platform freshly exercised; the prior Linux receipt
does not establish Linux reproduction of these findings.

## Interrupted coverage

All three investigator turns were terminated by an automated safety flag. The
parent requested only finalization of already-completed work and did not retry
the blocked probes. Source review is available across all repositories, but
runtime probes of concurrent mutation, interrupted writes, stale generations,
malformed records and symlink replacement remain incomplete as described in
the [coordination](coordination/coverage.md),
[filesystem/Git](filesystem-git/limitations.md), and
[evidence/state](evidence-state/coverage.md) notes.

There is no experimental clean bill of health for Shell Lock, Job Heartbeat,
Durable Mailbox, Agent File Guards, Worktree Guard, Repo Health, Session Ledger,
Config Baseline, Review Receipts, or Decision Ledger. Historical passing suites
and source-level defenses are not substitutes for those missing experiments.
