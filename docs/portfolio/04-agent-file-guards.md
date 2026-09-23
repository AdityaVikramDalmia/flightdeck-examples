# Agent File Guards: safer intake and file rewrites

Deprecated reference material for new Claude Code integrations as of 2026-09-22.

Repository: `github.com/AdityaVikramDalmia/flightdeck-agent-file-guards`. Public reference implementation; Apache-2.0 licensed.

## Problem

Agent-assisted file work has three separate hazards: an unfamiliar checkout can carry instructions or hooks, a generated rewrite can silently discard much of a durable document, and a literal NUL can make a text file appear binary to Git and review tools.

## Mechanism

- `untrusted-intake.sh` statically inventories known agent instruction, hook, and configuration surfaces without sourcing or running checkout files.
- `shrink-guard.sh` buffers candidate bytes, rejects empty or unexpectedly small content, stages in the target directory, checks for an intervening content change, and replaces by rename.
- `nul-lint.sh` scans bytes directly in tracked worktree files, staged index blobs, or explicitly selected untracked paths, independent of Git's binary heuristic.

The combined demo plants an executable hook whose only action would create a sentinel. Intake reports the carrier while the sentinel stays absent. It rejects a deliberately truncated candidate without changing the target, detects a planted literal NUL, removes that probe, then grows a tracked document through Shrink Guard and runs NUL Lint before committing. The original truncated candidate remains outside the worktree for the duration of the fixture; `--discard-rejected` avoids a second retained copy inside the worktree.

## Failure boundaries

Static intake patterns are triage signals, not security or malware certification. Shrink Guard detects volume loss, not same-size semantic damage; its final checksum narrows but cannot remove the race before rename, and it provides no inter-process lock. NUL Lint scans only the selected extensions and paths. Binary formats are intentionally outside its default text list.

## Reproduce

```sh
untrusted-intake ./downloaded-checkout
shrink-guard --from ./candidate.md ./docs/guide.md
nul-lint --staged
```

Run `make demo` to exercise all three outcomes without executing the planted hook.
