# Flightdeck Examples

Companion examples that run the 11 Flightdeck tool repositories (13 command-line utilities) together: a reproducible local demo, four separate recipes, and a portfolio case study per tool, for anyone evaluating how the tools compose.

> **Status:** public Apache-2.0 reference implementation, deprecated for new Claude Code
> integrations as of 2026-09-22. Not a claim that Claude Code replaces every capability; no
> ongoing feature work or support is promised.

## What it does

`make demo` creates a disposable Git project and runs six tool repositories against it as one work-and-review loop: it records a session, checks agent intake and file edits, runs the project's tests through Gate Runner, hands a verdict over a mailbox, and checks merge and worktree-removal preconditions under a shared lock. Repo Health adds an optional observation, four separate recipes demonstrate the remaining tools, and each tool has a [portfolio case study](docs/portfolio/README.md). Agent File Guards contributes three commands; each other tool repository contributes one ([all eleven](#the-eleven-tools)). The repository contains no service credentials, remote integration, model calls, or simulated performance claims.

## Why it exists

The tools are independently usable and share no hosted service, so each repository documents its contract on its own. This companion composes them through explicit commands and local files on synthetic state, so their boundaries are visible together: a matching review receipt is not approval, a Worktree Guard preflight is a point-in-time observation, and receiving a mailbox message does not prove it was processed. The [contracts table](docs/architecture/contracts.md) pairs each result with what the caller still owns. An agent, CI job, or human can use the same command interfaces in a larger workflow.

## Install

Requires Bash 3.2+, Git 2.36+, jq, Python 3.9+, Perl, Make, and standard macOS/Linux utilities (including `ps`).

```sh
mkdir flightdeck-tools && cd flightdeck-tools
git clone https://github.com/AdityaVikramDalmia/flightdeck-examples.git
cd flightdeck-examples
scripts/clone-all.sh   # clones the eleven tool repositories beside this checkout
```

[`scripts/clone-all.sh`](scripts/clone-all.sh) uses the short directory names the examples expect; they are deliberately shorter than the remote repository names (`gate-runner/`, not `flightdeck-gate-runner/`). It only clones what is missing and never modifies an existing directory. The core demo requires `gate-runner`, `durable-mailbox`, `session-ledger`, `agent-file-guards`, `worktree-guard`, and `shell-lock`. `repo-health/` adds an optional observation. The four other checkouts support separate recipes and are optional for the smoke suite. See [getting started](docs/getting-started/README.md) for the complete [checkout mapping and prerequisites](docs/getting-started/checkouts.md), including manual clones.

The examples default to this checkout's parent as the tools root. To use tool checkouts elsewhere (for example `scripts/clone-all.sh /path/to/tool-checkouts`):

```sh
bash examples/end-to-end-demo.sh --tools-root /path/to/tool-checkouts

# Equivalent environment form:
FLIGHTDECK_TOOLS_ROOT=/path/to/tool-checkouts make demo
```

## Quick use

```sh
make demo
```

The demo script creates one `mktemp` directory and mutates only that fixture. Within it, the script:

1. creates a Git project and linked feature worktree;
2. records a synthetic session launch;
3. statically detects an inert agent hook and proves its sentinel was not created;
4. rejects a destructive rewrite and a literal NUL, then installs a retained-size-checked document edit and scans the cleaned tracked text;
5. runs the project's actual `make test` through Gate Runner twice and verifies one attempt and one execution;
6. publishes a completion verdict, drains it, and acknowledges a question;
7. proves two commands do not overlap under Shell Lock, refuses removal with untracked work, optionally inspects both checkouts with Repo Health, then locks Worktree Guard preflight together with the merge and removal; and
8. records completion and validates that no live session remains.

It does not invoke a remote, create a real agent, call a paid service, or modify the six tool repositories. `PYTHONDONTWRITEBYTECODE=1` avoids Python cache writes in sibling checkouts. The demo clears inherited Git routing/configuration and Make includes, and disables Git hooks and global/system configuration in its fixture.

## Additional recipes

Each recipe needs its matching sibling checkout, and owns and removes its temporary state:

- `bash examples/heartbeat-recipe.sh` (`job-heartbeat/`) starts and replaces a generation, rejects a stale writer, and enforces terminal state.
- `bash examples/config-baseline-recipe.sh` (`config-baseline/`) publishes a synthetic configuration reference and checks content changes and added files.
- `bash examples/review-receipts-recipe.sh` (`review-receipts/`) verifies a rejecting review can match current bytes, then becomes stale after an edit.
- `bash examples/decision-ledger-recipe.sh` (`decision-ledger/`) preserves original words separately from interpretation and retains correction/answer history.

The [recipe guide](docs/getting-started/recipes.md) summarizes the contract each one demonstrates.

## The eleven tools

| Tool | Repository | Demonstration |
| --- | --- | --- |
| Gate Runner | [flightdeck-gate-runner](https://github.com/AdityaVikramDalmia/flightdeck-gate-runner) | Runs and deduplicates project checks |
| Durable Mailbox | [flightdeck-durable-mailbox](https://github.com/AdityaVikramDalmia/flightdeck-durable-mailbox) | Publishes a verdict and acknowledges a question |
| Session Ledger | [flightdeck-session-ledger](https://github.com/AdityaVikramDalmia/flightdeck-session-ledger) | Records launch and completion lifecycle events |
| Agent File Guards | [flightdeck-agent-file-guards](https://github.com/AdityaVikramDalmia/flightdeck-agent-file-guards) | Scans intake, protects a rewrite, and detects NUL bytes |
| Worktree Guard | [flightdeck-worktree-guard](https://github.com/AdityaVikramDalmia/flightdeck-worktree-guard) | Checks merge and worktree removal preconditions |
| Shell Lock | [flightdeck-shell-lock](https://github.com/AdityaVikramDalmia/flightdeck-shell-lock) | Serializes cooperating commands around checks and mutations |
| Config Baseline | [flightdeck-config-baseline](https://github.com/AdityaVikramDalmia/flightdeck-config-baseline) | Separate recipe for configuration drift detection |
| Job Heartbeat | [flightdeck-job-heartbeat](https://github.com/AdityaVikramDalmia/flightdeck-job-heartbeat) | Separate recipe for generation-safe progress reports |
| Repo Health | [flightdeck-repo-health](https://github.com/AdityaVikramDalmia/flightdeck-repo-health) | Optionally inspects clean and dirty fixture checkouts |
| Review Receipts | [flightdeck-review-receipts](https://github.com/AdityaVikramDalmia/flightdeck-review-receipts) | Separate recipe distinguishes current bytes from approval |
| Decision Ledger | [flightdeck-decision-ledger](https://github.com/AdityaVikramDalmia/flightdeck-decision-ledger) | Separate recipe preserves original words and linked history |

Each tool repository is an Apache-2.0 reference implementation with the same status as this one.

Start with the [portfolio index](docs/portfolio/README.md) or the machine-readable [catalog](catalog.json).
The [architecture guide](docs/architecture/README.md) explains the workflow and each tool's contract.
The historical [2026-09-22 candidate summary](RELEASE-CANDIDATE.md) links the frozen commits and verification evidence.

## Limits

- The demo trusts installed executables and checkout code; it is not a sandbox.
- A matching review is not approval, and an answered question can still contain a refusal.
- Shell Lock coordinates cooperating writers only; preflight checks and health reports are observations, not atomic snapshots.
- The EXIT trap waits for its direct workers and selects detached Gate Runner supervisors from this fixture's attempt metadata. It checks each recorded PID against the complete interpreter, resolved Gate Runner script, exact attempt path, and descriptor arguments before signalling. Diagnostic text merely quoting the fixture path is insufficient. Ambiguous ownership or incomplete startup metadata makes cleanup fail and retain the fixture; verified cleanup removes it.
- Process inspection and signalling are not atomic, and SIGKILL and machine failure cannot run cleanup traps.

## Test

```sh
make test
# Equivalent: make smoke
```

`make test` first checks `scripts/clone-all.sh` against synthetic local repositories. The smoke suite then runs the complete demo with deliberately conflicting inherited Git/Make settings, validates all 11 catalog entries and 13 utilities, checks document links and missing-tool failure, interrupts an actual detached gate command to verify cleanup, and executes all four separate recipes when their checkouts are present. It uses temporary paths containing spaces and needs the six required sibling repositories and the prerequisites under [Install](#install). The final ledger query must succeed and return no live sessions before the demo reports PASS.

## License and maintenance

Copyright 2026 Aditya Dalmia. Licensed under [Apache-2.0](LICENSE), with
[attribution](NOTICE) and [source provenance](PROVENANCE.md). This is a public
reference implementation, deprecated for new Claude Code integrations as of 2026-09-22. See the [release preparation index](docs/release/README.md),
[contributing guide](CONTRIBUTING.md), and [security contact](SECURITY.md).
