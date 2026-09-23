# Job Heartbeat: generation-safe progress reports

Deprecated reference material for new Claude Code integrations as of 2026-09-22.

Repository: `github.com/AdityaVikramDalmia/flightdeck-job-heartbeat`. Public reference implementation; Apache-2.0 licensed.

## Problem

A shell job can keep reporting after an operator restarts its logical name. Without a run identity, that old process can overwrite the replacement's progress or completion. An observer also needs to distinguish an expired heartbeat from proof that a process died.

## Mechanism

Job Heartbeat creates an opaque generation token at start. Every touch and finish compares that token under a local advisory lock before publishing validated JSON by atomic rename. Restart compares the current generation too, so concurrent replacement requests have one winner. A terminal generation cannot be revived by a heartbeat.

Read reports distinguish fresh, late, finished, missing, and unknown. Future timestamps and corrupt records become unknown and block writes. A late or missing report never triggers an implicit kill or restart. Hashed filenames preserve exact case-sensitive names even on case-insensitive filesystems.

## Failure boundaries

These are caller reports, not operating-system liveness checks or verification of completed work. A forward clock jump can make a healthy job late; a rollback can make its timestamp unknown. Cooperating users must share the same persistent lock inode on a local filesystem. Atomic publication does not provide power-loss durability, event history, or authorization against other users able to edit the store. A published update can survive even when its receipt is lost.

## Reproduce

From the tool checkout:

```sh
make test
make demo
```

The synthetic demo starts one generation, replaces it, refuses the stale writer, finishes the replacement, and refuses a heartbeat after completion. See the [companion recipe](../../examples/heartbeat-recipe.sh) to run it through the sibling checkout layout.
