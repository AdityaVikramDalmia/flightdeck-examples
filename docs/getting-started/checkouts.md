# Checkouts and prerequisites

All remotes below are private and require authorization. Their URLs identify
repositories, not public downloads. Use the short local names shown here so the
examples can resolve sibling checkouts without installation:

```text
flightdeck-tools/
  flightdeck-examples/   # this companion
  gate-runner/          # core demo
  durable-mailbox/      # core demo
  session-ledger/       # core demo
  agent-file-guards/    # core demo, three independent utilities
  worktree-guard/       # core demo
  shell-lock/           # core demo
  repo-health/          # optional observation in the core demo
  job-heartbeat/        # separate recipe
  config-baseline/      # separate recipe
  review-receipts/      # separate recipe
  decision-ledger/      # separate recipe
```

| Local directory | Private repository |
| --- | --- |
| `flightdeck-examples` | [Companion examples](https://github.com/AdityaVikramDalmia/flightdeck-examples) |
| `gate-runner` | [Gate Runner](https://github.com/AdityaVikramDalmia/flightdeck-gate-runner) |
| `durable-mailbox` | [Durable Mailbox](https://github.com/AdityaVikramDalmia/flightdeck-durable-mailbox) |
| `session-ledger` | [Session Ledger](https://github.com/AdityaVikramDalmia/flightdeck-session-ledger) |
| `agent-file-guards` | [Agent File Guards](https://github.com/AdityaVikramDalmia/flightdeck-agent-file-guards) |
| `worktree-guard` | [Worktree Guard](https://github.com/AdityaVikramDalmia/flightdeck-worktree-guard) |
| `shell-lock` | [Shell Lock](https://github.com/AdityaVikramDalmia/flightdeck-shell-lock) |
| `repo-health` | [Repo Health](https://github.com/AdityaVikramDalmia/flightdeck-repo-health) |
| `job-heartbeat` | [Job Heartbeat](https://github.com/AdityaVikramDalmia/flightdeck-job-heartbeat) |
| `config-baseline` | [Config Baseline](https://github.com/AdityaVikramDalmia/flightdeck-config-baseline) |
| `review-receipts` | [Review Receipts](https://github.com/AdityaVikramDalmia/flightdeck-review-receipts) |
| `decision-ledger` | [Decision Ledger](https://github.com/AdityaVikramDalmia/flightdeck-decision-ledger) |

Each remote is separate. A normal clone defaults to its longer remote name;
choose the destination explicitly, for example:

```sh
git clone https://github.com/AdityaVikramDalmia/flightdeck-review-receipts.git review-receipts
```

The core demo requires Bash 3.2+, Git 2.36+, jq, Python 3.9+, Perl, Make, and standard
macOS/Linux utilities including `ps`. Component READMEs remain authoritative for
platform requirements. The core demo needs its six marked checkouts. Repo Health
and the four separate recipe checkouts are optional for `make smoke`; when present,
their demonstrations run and must pass.

The default tools root is the companion's parent. For a different location:

```sh
FLIGHTDECK_TOOLS_ROOT=/path/to/tool-checkouts make smoke
bash examples/end-to-end-demo.sh --tools-root /path/to/tool-checkouts
```

The selected tools root still uses the short directory names above. The recipes
use trusted local executables and synthetic state; they are not sandboxes for
hostile tool checkouts.
