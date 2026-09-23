# Independent correctness review

Historical review snapshot retained. Later [fixes and independent release validation](../release/readiness/README.md) resolve C1/E1/E2 without relabelling the partial coverage recorded below.

2026-09-23: an unrelated private project's name was redacted from three files in this review (`README.md`, `coordination/README.md` and a key in `revisions.json`); no finding changed.

Reviewed on 2026-09-22. **Partial runtime coverage; three reproduced findings.**
Source/contract review covered all twelve repositories: eleven standalone
projects containing thirteen tools, plus this examples repository. All remain
private, locally Apache-2.0 licensed, and deprecated for new Claude Code
integrations. This review changes no implementation or release status.

The review began with the [release index](../release/README.md) and its
[host](../release/prepared-host.json), [Linux](../release/prepared-linux.json), and
[repository](../release/prepared-repositories.json) receipts. Those passing
historical suites are distinct from this review's new experiments.

| ID | Severity | Reproduced behavior | Evidence strength |
| --- | --- | --- | --- |
| [C1](coordination/gate-runner-interruption.md) | Medium | Gate Runner accepts SIGTERM during final input checking, then publishes and reuses PASS | One completed subagent case; source/contract adjudicated by parent; no independent replay or standalone result receipt |
| [E1](examples/live-query-failure.md) | Medium | Examples demo prints PASS after its final ledger query fails | Parent execution with validate-failure control and retained result JSON |
| [E2](examples/cleanup-identity.md) | Medium | Cleanup terminates a non-supervisor whose diagnostic argument quotes the fixture supervisor path | Parent execution with neighboring-path control and retained result JSON |

No finding says a failed gate command passed: C1 concerns an interruption after
the command had completed. No unexecuted hypothesis is counted as a finding.
Repair directions are documented, but no source fix was prepared or applied.

- [Method, execution limits and validation](method.md)
- [Exact reviewed/prepared revisions and input hashes](revisions.json)
- [Coordination: four repositories](coordination/README.md)
- [Filesystem/Git: three repositories, five utilities](filesystem-git/README.md)
- [Evidence/state: four repositories](evidence-state/README.md)
- [Examples: fault injection, controls and output](examples/README.md)
- [Final checks and checkout state](validation.json)

Three bounded Astra reviewers were assigned the requested groups, without
recursive delegation. Their investigation turns were automatically terminated
with a possible-cybersecurity-risk flag. Completed work was preserved; blocked
probes were not retried. Consequently **this is not a completed experimental
review of all requested boundaries**, nor a finding of no defects in repositories
without reproduced issues. The group coverage notes identify what remains open.

Only this review directory is committed. There was no publishing, pushing,
history rewriting/backdating, original Flightdeck runtime access, live ledger or
credential access, or access to any unrelated private project. The work was assembled in an isolated
examples worktree; all eleven component sources were left unchanged.
