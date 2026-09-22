# Validation scope and remaining gaps

The initial audit verified Docker client/server 29.4.0 and the existing local
unprivileged Alpine image:
`sha256:95e1569a6674da61e3251c1f441edc5dc69699721a441250bd6fd6f1082bb7f7`.
No image rebuild, network package retrieval, paid runner, or cloud workflow is
needed. The companion harness runs eleven component suites; its execution must
be supplemented with companion `make test` and `make demo` against the same
snapshot. Fresh clones are local clones because fixes are unpushed.

Each component's `checks_or_groups` field must receive its actual unit: unittest
cases, grouped regressions, or shell assertions. Companion smoke tests and demo
stages are separate. Four filesystem-case-equivalence skips are expected on the
case-sensitive Linux fixture: two in Config Baseline, two in Review Receipts.
They are not Linux passes. Record actual shell/Python selection instead of
inferring Bash 3.2 from the platform.

The new component execution pass ran once per platform after the C1/E1/E2 fixes,
using the exact commits in [candidate-manifest.json](candidate-manifest.json).
Both eleven-component runs passed. Installation/example and companion results
are recorded separately. An initial disposable orchestration script had a Python
quoting syntax error before any cloning or tests; it was corrected before the
one successful harness invocation on each platform.

## Named limitations

- This audit does not complete the earlier safety-stopped adversarial review or
  retry its blocked probes. In particular the Gate Runner latest-pointer
  scheduling candidate, Mailbox malformed non-regular archive candidate, and
  filesystem partial-clone hypothesis remain unverified.
- Broader concurrent mutation, interrupted writes/publication, malformed records,
  stale projections and descriptor/symlink replacement schedules outside existing
  suites remain untested. A passing regression suite is not exhaustive coverage.
- macOS and one local Alpine image do not establish all supported minimum Python,
  Bash/Git versions, Linux distributions, filesystem types, Windows, network
  filesystems, power failure, or hardware-cache durability.
- Secret scanners and focused text/filename inventories cannot prove absence of
  arbitrary private text, novel secret formats, encrypted content or every
  transitive dependency/licensing issue. Record scanner version, configuration,
  exact history scope and working-tree scope separately.
- GitHub metadata is a point-in-time identity/privacy observation. Candidate
  commits may differ from private remote main until separately authorized push.
- No public release, deployment, release tag, remote installation, native-feature
  equivalence or renewed support commitment follows from these receipts.

## Fresh component results

The [host suite receipt](final-host-suites.json) records macOS arm64, Python
3.14.6, Bash 5.3.9, Git 2.51.0, and jq 1.7.1. This particular run is **not** a
fresh Bash 3.2 claim. The [Linux suite receipt](final-linux-suites.json) records
the exact existing image with Python 3.14.7, Bash 5.3.9, Git 2.54.0, jq 1.8.2 and
Perl 5.42.2. The host launcher Python field in that receipt is not the container
Python version; `container_tools` records the Linux runtime.

| Suite | Reported count | Unit | macOS skips | Linux skips |
| --- | ---: | --- | ---: | ---: |
| Gate Runner | 43 | unittest cases | 0 | 0 |
| Durable Mailbox | 18 | grouped regression cases | 0 | 0 |
| Session Ledger | 19 | grouped regression cases | 0 | 0 |
| Agent File Guards | 111 | shell assertions | 0 | 0 |
| Worktree Guard | 42 | unittest cases | 0 | 0 |
| Shell Lock | 24 | unittest cases | 0 | 0 |
| Repo Health | 43 | unittest cases | 0 | 0 |
| Config Baseline | 33 | unittest cases | 0 | 2 |
| Job Heartbeat | 25 | unittest cases | 0 | 0 |
| Decision Ledger | 32 | unittest cases | 0 | 0 |
| Review Receipts | 32 | unittest cases | 0 | 2 |

The counts are suite-reported totals; the Linux skipped cases are included in
their suite totals and are not executed passes. The four skipped methods are
Config Baseline's `test_case_alias_cannot_hide_manifest_self_inclusion` and
`test_case_alias_roots_cannot_overlap`, and Review Receipts'
`test_case_alias_receipt_cannot_overwrite_selected_artifact` and
`test_case_alias_destination_stays_protected_during_replacement`.

## Fresh setup, examples, and companion results

The [host setup/example receipt](final-host-setup-examples.json) and
[Linux setup/example receipt](final-linux-setup-examples.json) each contain 35
successful command records: installation/help checks for every component, all
documented component examples (including both file-guard examples), companion
`make test`, and companion `make demo`. These command records are not test-case
counts. Every installation used a separate disposable prefix containing spaces.
Gate Runner's documented fixture additionally checked one execution after two
starts and three distinct keys after source changes.

On each platform the companion reported **10 smoke unittest cases** and the demo
completed **7 stages**. The smoke suite independently exercised the newly added
failed-query controls, diagnostic decoy survival, ambiguous/incomplete identity
retention, and the existing real detached-supervisor cleanup control. It also
executed all four optional recipes because all eleven components were present.
These new cases are contained in the recorded fixed code; no blocked prior probe
was repeated. The two new Gate Runner unittest methods likewise ran within its
43-case suite on both platforms.

The host run used an isolated temporary HOME and disabled global/system Git
configuration. Linux used the existing non-root `tester` image, no network, a
read-only root filesystem and source bind mount, and executable writable `/tmp`
where checkouts were copied before execution. No user installation was changed.

[Clone cleanliness](clone-cleanliness.json) confirms all twelve snapshots had
unchanged HEADs and clean `git status --porcelain` before and after validation.
Ignored Python bytecode may be produced by explicit compile checks; it is not
tracked distribution data. The extra setup driver lived outside the cloned
repositories and is disposable orchestration, not a shipped dependency.

The final audit documentation is added after the frozen implementation snapshots.
Its catalog/document-link/portability tests are checked separately in the audit
worktree, recorded in [documentation validation](documentation-validation.json).
That distinction avoids pretending the snapshots already contained these receipts.
