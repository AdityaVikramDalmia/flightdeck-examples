# Revisions and completed coverage

## Exact source revisions

The following locally inspected HEADs matched the prepared revisions recorded in
all three examples release receipts. `git status --porcelain` emitted no tracked
or untracked changes for these three checkouts when inspected.

| Repository | Inspected HEAD |
| --- | --- |
| agent-file-guards | `7a83c380f1228a6978359723593443e50867fd04` |
| worktree-guard | `1efffa22329822d3cff063b9706a967b04229460` |
| repo-health | `f0c983339a927fedff397d6fc827749a203ee315` |

These are the private, locally Apache-2.0 licensed reference artifacts deprecated
for new Claude Code integrations. The prior receipts record passing suites; those
results were read as historical evidence and were not rerun or relabeled as this
review's validation.

## Read-only inspection performed

Release starting points were `flightdeck-examples/docs/release/README.md`,
`prepared-host.json`, `prepared-linux.json`, and `prepared-repositories.json`.
Each assigned repository's `AGENTS.md`, named maintainer `SKILL.md`, `README.md`,
`PROVENANCE.md`, and release index were read. Command implementations were read.
The three file-guard command contracts and their regression scripts were read.
The worktree-guard checks contract was read; both Python test modules' case names
were enumerated to identify existing coverage. This is not a claim of a complete
line-by-line audit of those Python test modules.

| Boundary | Code inspected at the revisions above | Evidence established |
| --- | --- | --- |
| Replacement and interrupted writes | `agent-file-guards/bin/shrink-guard.sh:103`, `:181`, `:190` | Candidate buffering, old/current checksum comparison, same-directory staging, rename, and signal cleanup paths were traced. No new runtime fault injection was executed. |
| Symlink replacement and enumeration failures | `agent-file-guards/bin/nul-lint.sh:76`, `:103`, `:126`, `:143` | Component checks, tracked/untracked manifests, staged blob pipeline, and output construction were traced. Existing tests cover static symlink ancestors, producer failures, and invalid UTF-8 reporting. |
| Static intake and carrier read failure | `agent-file-guards/bin/untrusted-intake.sh:52`, `:70`, `:103`, `:142` | Surface enumeration, component checks, carrier limits, read status, and JSON buffering were traced. Existing tests cover static/broken ancestor symlinks and failed find/grep. |
| Git records and false-ready paths | `worktree-guard/bin/worktree-guard:78`, `:111`, `:136` | Git execution, status/worktree parsing, split-index refusal, hidden index flags, operation state, ancestry, and exact branch checks were read. Existing case names include failed/truncated status and linked/nested split-index cases. |
| Unknown states and interrupted Git helpers | `repo-health/bin/repo-health:43`, `:46`, `:99`, `:155` | Transport restrictions, query ownership/timeout cleanup, split-index recursion, status parsing, and branch/upstream observation paths were read. Existing case names include malformed/truncated output, timeout/helper cleanup, and signal handoff cases. |

## Commands and outputs

Metadata was collected with `git rev-parse HEAD` and `git status --porcelain`
inside each assigned source checkout. Source inspection used `cat`, `rg --files`,
`rg -n`, and `wc -l`. No new component command, test suite, demo, or synthetic
reproducer was run by this lane. Thus there is no fresh synthetic execution
output or runtime pass/fail count to attach.

One broad source read was truncated by the tool output budget. Focused follow-up
reads supplied both complete Python commands and the three file-guard contracts,
intake implementation, and file-guard tests. The coverage table states the actual
inspection scope rather than implying every requested boundary was exercised.
