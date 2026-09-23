# Flightdeck Examples

> **Deprecated for new Claude Code integrations — 2026-09-22.** Retained as an
> Apache-2.0 public reference implementation. This is a maintainer status
> decision, not a claim that Claude
> Code replaces every capability. No ongoing feature work or support is promised.

Public reference implementation (Apache-2.0 licensed; deprecated for new Claude Code integrations as of 2026-09-22): companion examples for **11 independent tool repositories exposing 13 utilities**. Agent File Guards contributes three commands; each other tool repository contributes one. This repository contains a reproducible composition demo and concise portfolio case studies. It contains no service credentials, remote integration, model calls, or simulated performance claims.

The repositories named below are public reference implementations, deprecated for new Claude Code integrations as of 2026-09-22:

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

Start with the [portfolio index](docs/portfolio/README.md) or the machine-readable [catalog](catalog.json).
The [architecture guide](docs/architecture/README.md) explains the workflow and each tool's contract.
The historical [2026-09-22 candidate summary](RELEASE-CANDIDATE.md) links the frozen commits and verification evidence.

## Checkout layout

The demo defaults to sibling repositories under one tools directory:

```text
flightdeck-tools/
  agent-file-guards/       # three utilities
  config-baseline/         # separate recipe
  decision-ledger/         # separate recipe
  durable-mailbox/
  flightdeck-examples/
  gate-runner/
  job-heartbeat/           # separate recipe
  repo-health/             # optional core-demo observation
  review-receipts/          # separate recipe
  session-ledger/
  shell-lock/
  worktree-guard/
```

Directory names are deliberately shorter than the remote repository names. An alternate layout can be selected explicitly:

```sh
bash examples/end-to-end-demo.sh --tools-root /path/to/tool-checkouts

# Equivalent environment form:
FLIGHTDECK_TOOLS_ROOT=/path/to/tool-checkouts make demo
```

The core demo requires `gate-runner`, `durable-mailbox`, `session-ledger`, `agent-file-guards`, `worktree-guard`, and `shell-lock`. `repo-health/` adds an optional observation. The four other checkouts support separate recipes and are optional for the smoke suite. See [getting started](docs/getting-started/README.md) for complete [checkout mapping and prerequisites](docs/getting-started/checkouts.md).

## End-to-end demo

```sh
make demo
```

The script creates one `mktemp` directory and mutates only that fixture. Within it, the script:

1. creates a Git project and linked feature worktree;
2. records a synthetic session launch;
3. statically detects an inert agent hook and proves its sentinel was not created;
4. rejects a destructive rewrite and a literal NUL, then installs a retained-size-checked document edit and scans the cleaned tracked text;
5. runs the project's actual `make test` through Gate Runner twice and verifies one attempt and one execution;
6. publishes a completion verdict, drains it, and acknowledges a question;
7. proves two commands do not overlap under Shell Lock, refuses removal with untracked work, optionally inspects both checkouts with Repo Health, then locks Worktree Guard preflight together with the merge and removal; and
8. records completion and validates that no live session remains.

It does not invoke a remote, create a real agent, call a paid service, or modify the six tool repositories. `PYTHONDONTWRITEBYTECODE=1` avoids Python cache writes in sibling checkouts. The demo clears inherited Git routing/configuration and Make includes, and disables Git hooks and global/system configuration in its fixture. It trusts installed executables and checkout code; it is not a sandbox.

## Additional recipes

With `job-heartbeat/` beside this checkout, run `bash examples/heartbeat-recipe.sh` to start and replace a generation, reject a stale writer, and enforce terminal state. It creates and removes its own fixture.

With `config-baseline/` beside this checkout, run `bash examples/config-baseline-recipe.sh` to publish a synthetic configuration reference and check content changes and added files. The recipe owns and removes all of its temporary state.

Run `bash examples/review-receipts-recipe.sh` with `review-receipts/` present to verify a rejecting review can match current bytes, then becomes stale after an edit. Run `bash examples/decision-ledger-recipe.sh` with `decision-ledger/` present to preserve original words separately from interpretation and retain correction/answer history. A matching review is not approval, and an answered question can still contain a refusal.

## Verification

```sh
make test
# Equivalent: make smoke
```

The smoke suite runs the complete demo with deliberately conflicting inherited Git/Make settings, validates all 11 catalog entries and 13 utilities, checks document links and missing-tool failure, interrupts an actual detached gate command to verify cleanup, and executes all four separate recipes when their checkouts are present. It uses temporary paths containing spaces. The demo requires Bash 3.2+, Git 2.36+, jq, Python 3.9+, Perl, Make, standard macOS/Linux utilities (including `ps`), and the six required sibling repositories.

The final ledger query must succeed and return no live sessions before the demo reports PASS. The EXIT trap waits for its direct workers and selects detached Gate Runner supervisors from this fixture's attempt metadata. It checks each recorded PID against the complete interpreter, resolved Gate Runner script, exact attempt path, and descriptor arguments before signalling. Diagnostic text merely quoting the fixture path is insufficient. Ambiguous ownership or incomplete startup metadata makes cleanup fail and retain the fixture; verified cleanup removes it. Process inspection and signalling are not atomic, and SIGKILL and machine failure cannot run cleanup traps. Shell Lock coordinates cooperating writers only; preflight checks and health reports are observations, not atomic snapshots.

Licensed under Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE).

## License and maintenance

Copyright 2026 Aditya Dalmia. Licensed under [Apache-2.0](LICENSE), with
[attribution](NOTICE) and [source provenance](PROVENANCE.md). This is a public
reference implementation, deprecated for new Claude Code integrations as of 2026-09-22. See the [release preparation index](docs/release/README.md),
[contributing guide](CONTRIBUTING.md), and [security contact](SECURITY.md).
