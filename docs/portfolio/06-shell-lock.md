# Shell Lock: local serialization around cooperating writers

Deprecated reference material for new Claude Code integrations as of 2026-09-22.

Repository: `github.com/AdityaVikramDalmia/flightdeck-shell-lock`. Public reference implementation; Apache-2.0 licensed.

## Problem

Separate shell processes can each pass a precondition and then mutate the same local resource concurrently. A PID file can also become stale or name a reused process after a crash.

## Mechanism

Shell Lock opens one persistent lock file and holds an operating-system advisory `flock` across a directly executed command. The child inherits the locked descriptor, command output streams remain attached, and the wrapper returns the command's status. A contender waits to a monotonic timeout or exits `75` without launching the command.

The combined demo starts two contenders against one lock and checks their `start`/`finish` records never overlap. It then uses that same lock contract to keep each Worktree Guard preflight adjacent to its Git merge or worktree removal.

## Failure boundaries

The lock coordinates only processes that use the same persistent path on the same local filesystem. It does not stop an uncooperative writer, provide a distributed transaction, or make the protected command durable. Deleting or replacing the lock file can split callers across different inodes. Descendants retaining the descriptor can extend lock ownership after the immediate command exits.

## Reproduce

```sh
shell-lock --timeout 10 .locks/repository.lock -- sh -c '
  worktree-guard merge-check ./main --base main --branch task || exit $?
  git -C ./main merge --ff-only task
'
```

Use `make demo` for the contention assertion and both guarded Git operations.
