# Portfolio case studies

These eleven case studies describe observed tool behavior and explicit failure boundaries. Together they cover 11 tool repositories and 13 utilities. Each points to the core workflow or a separate disposable recipe.

1. [Gate Runner: one durable verdict for one code state](01-gate-runner.md)
2. [Durable Mailbox: retained local handoff with explicit acknowledgment](02-durable-mailbox.md)
3. [Session Ledger: append-only lifecycle reports](03-session-ledger.md)
4. [Agent File Guards: safer intake and file rewrites](04-agent-file-guards.md)
5. [Worktree Guard: preflight before merge and removal](05-worktree-guard.md)
6. [Shell Lock: local serialization around cooperating writers](06-shell-lock.md)
7. [Repo Health: distinguish observed state from missing evidence](07-repo-health.md)
8. [Job Heartbeat: generation-safe progress reports](08-job-heartbeat.md)
9. [Config Baseline: explicit configuration drift evidence](09-config-baseline.md)

10. [Review Receipts: bind review words to exact selected files](10-review-receipts.md)
11. [Decision Ledger: keep original words distinct from interpretation](11-decision-ledger.md)

All referenced GitHub repositories are private candidates with redistribution licenses pending. The URLs in this repository identify expected remotes for authorized collaborators; availability is not implied.

Run the six required tools together from the repository root; the seventh health inspection runs when its checkout is present:

```sh
make demo
```

The [recipe guide](../getting-started/recipes.md) lists the four separate demonstrations.
