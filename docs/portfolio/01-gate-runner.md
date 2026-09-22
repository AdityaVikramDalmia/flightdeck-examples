# Gate Runner: one durable verdict for one code state

Deprecated reference material for new Claude Code integrations as of 2026-09-22.

Private repository: `github.com/AdityaVikramDalmia/flightdeck-gate-runner` (authorized access required). Private candidate; Apache-2.0 licensed; public launch deferred.

## Problem

Two local workers can launch the same expensive check, lose its output when a terminal closes, or treat a reassuring log line as success despite a nonzero exit. A later caller also needs to know whether the inputs still match the earlier result.

## Mechanism

Gate Runner hashes the Git worktree state, staged entries, non-ignored untracked bytes, executable, command arguments, declared inputs, selected environment, and salt. A detached supervisor stores immutable attempt records, combined output, and the command's real exit code under the Git common directory. Concurrent starts for one key join its lock; a completed result for the same key is reused unless `--force` is explicit.

The combined demo runs a real fixture `make test` twice:

```sh
gate-run --json start --wait -- make test
gate-run --json start --wait -- make test
```

It compares the returned attempt identifiers and checks an ignored execution counter has one line.

## Failure boundaries

The worktree is live rather than snapshotted. Gate Runner hashes before and after execution, but a concurrent edit reverted between those observations can escape detection. Ignored files, undeclared environment variables, tool binaries, and external systems are outside the key unless supplied as inputs or salt. Commands that daemonize or close inherited coordination descriptors are unsupported. A cached pass proves the recorded command and selected inputs matched; it is not a general environment attestation.

## Reproduce

```sh
make demo
```

The fixture writes test output only to an ignored directory, so the command does not invalidate its own input identity.
