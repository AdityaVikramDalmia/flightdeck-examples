# Source coverage and limits

## Revisions

These are the prepared revisions recorded in both the host and Linux receipts.
The parent reviewer reported that the clean component HEADs matched them before
delegation. This subreview did not independently run a second Git status check.

| Component | Prepared revision |
| --- | --- |
| session-ledger | `f7ffb390974ed125de9917b6d83184a823dc0bbd` |
| config-baseline | `1fb79c714a02afe139202cd38fc0160e71eec8b8` |
| review-receipts | `135c0f13b38b478a68bb051869c6c6ab99613f14` |
| decision-ledger | `e6d51e42d937a333e55637a27a32793478bfadff` |

Read `flightdeck-examples/docs/release/README.md` and parsed the three
`prepared-*.json` receipts. Those receipts describe earlier validation runs;
their suite results are not new correctness-review execution evidence. The
remote privacy/license fields are receipt observations, not fresh network checks.

## Reviewed material

Read each assigned component's `AGENTS.md`, named maintainer `SKILL.md`, README,
provenance, and release index. Read the storage/schema/scope contracts listed
below, executable implementations, and relevant existing tests.

| Component | Contract and implementation areas inspected | Existing coverage inspected |
| --- | --- | --- |
| session-ledger | `docs/storage.md`, `docs/events.md`, `docs/commands.md`; all of `bin/session-ledger`, `lib/lock.sh`, `lib/schema.jq` | Full `tests/test.sh`: serialized append/read, incomplete tails, schema/identity validation, signal boundaries, readback errors, stdout failure |
| config-baseline | `docs/inventory.md`, `docs/manifest.md`; all of `bin/config-baseline`, particularly descriptor traversal, path identity, read signatures, manifest validation, publication | Test inventory and named boundary cases in `tests/test_config_baseline.py`; test bodies were not all read |
| review-receipts | `docs/storage.md`, `docs/scope.md`; `bin/review-receipts` schema, snapshot, alias protection, publication, result emission | Test inventory plus bodies for concurrent file changes, post-publication flush failure, artifact destination replacement and case aliases, hardlink obligations |
| decision-ledger | `docs/storage.md`, `docs/records.md`; all of `bin/decision-ledger`, particularly schema/row validation, transaction ordering, initialization, output | Test inventory in `tests/test_decision_ledger.py`; test bodies were not all read |

## Unexecuted boundary work

No new reproducer, negative control, race experiment, or interrupted-write test
executed before this subreview was stopped. Therefore there is no runtime
expected/actual pair, deterministic injection result, or naturally occurring
race result to report for this group.

The following remain gaps in this subreview, rather than suspected defects:

- Simultaneous mutation beyond the already recorded release suite scenarios.
- Interruption at initialization/publication and ledger append boundaries not
  already covered by the existing suites.
- Malformed record variants and stale/current projections beyond source reading.
- Symlink replacement at descriptor and publication boundaries.
- False-success results at storage, validation, and output boundaries.

## Scope constraints relevant to adjudication

The contracts explicitly delimit several properties. Source-level observations
within these limits cannot alone establish bugs:

- Session-ledger's lock is advisory. External mutations and unstable ancestors
  are operator responsibilities; no fsync or exactly-once retry guarantee exists.
- Config-baseline and review-receipts do not promise an atomic multi-file
  snapshot. They request writers be stopped where consistency matters and
  exclude hostile concurrent hierarchy replacement.
- Decision-ledger requires trusted stable ancestors/writers and excludes hostile
  concurrent path replacement. Its documented initialization recovery includes
  an extra hardlink left by interruption after publication.
- All four distinguish a missing success receipt from proof that no mutation
  occurred. Post-publication output failure must be evaluated accordingly.

No source edits or fix proposals were produced. Passing historical suites and
unverified suspicions are deliberately not promoted to findings.
