# Actual source dates and adaptation scope

[provenance-audit.json](provenance-audit.json) records a fresh metadata-only check
against extraction source revision
`494799eea3b9e7ce8686506a288c297ccf96be8d`. For fourteen explicitly named mechanism
paths, `git log --follow` confirmed the first source commit, first author date,
and latest source edit date recorded by each component. Author and committer
dates are retained separately. All recorded source dates match. Git metadata is
historical evidence, not an independent timestamp service.

All twelve standalone extraction/composition commits have actual author dates
of 2026-09-22. These dates were verified in each standalone repository. Earlier
July/August mechanism dates do not date standalone features or imply continuous
maintenance since that date. No commit was backdated or history rewritten.

| Component | Source starting point | Standalone adaptation attribution |
| --- | --- | --- |
| Gate Runner | `gate-run.sh`, first 2026-07-27 | Reimplemented Python coordinator; immutable attempts, OS locks, stronger declared-input identity; omitted private notifications/integration |
| Durable Mailbox | `mailbox.sh`, first 2026-07-26; `lane-say.sh`, 2026-07-25 | Explicit store/literal recipients, synthetic fixtures and closed contention failure; no registry discovery or private state |
| Session Ledger | `registry.sh`, first 2026-07-25 | Explicit ledger, exact identifiers and stricter schema/calendar validation; no transcripts or global roster |
| Agent File Guards | Shrink guard 2026-07-30; NUL/intake scanners 2026-08-01 | Rewritten interfaces, selection, audit and portability contracts; removed private defaults/fixtures |
| Worktree Guard | `merge-preflight.sh`, first 2026-07-26 | Independent Python checks and JSON; omitted merges, network synchronization and private operational rules |
| Shell Lock | `lib/lock.sh`, first 2026-07-25 | Python kernel advisory locks replace Bash mkdir/PID takeover; inherited descriptors are standalone work |
| Repo Health | `project-status.sh`, first 2026-07-25 | Python observations and explicit UNKNOWN states; omitted rosters, private roots and issue/session integrations |
| Job Heartbeat | `lane-state.sh`, first 2026-07-26 | New Python generations, bounded/validated state and atomic updates; omitted session discovery/transcripts/patrol |
| Config Baseline | `config-sweep.sh`, first 2026-07-31 | Substantial Python adaptation with explicit named roots, modes, JSON and bounded no-follow reads |
| Review Receipts | `grill-brief.sh`, first 2026-07-31 | Replaces timestamp/existence mechanism with selected-byte/mode binding; omitted reviewer automation and private policies |
| Decision Ledger | `directive.sh`, first 2026-07-27 | SQLite transaction/history adaptation; no authentic operator words or historical records copied |
| Flightdeck Examples | Standalone composition, 2026-09-22 | New synthetic integration and case studies derived from component contracts |

Per-component PROVENANCE.md remains authoritative for supporting helper/test
inputs and deliberate omissions. Mechanism history and standalone adaptation are
credited to Aditya Dalmia with AI coding assistance; upstream runtimes, libraries,
Git and OS facilities remain their authors' work. No authorship of Claude Code or
its native messaging implementation is claimed.
