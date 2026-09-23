# Worktree Guard: preflight before merge and removal

Deprecated reference material for new Claude Code integrations as of 2026-09-22.

Repository: `github.com/AdityaVikramDalmia/flightdeck-worktree-guard`. Public reference implementation; Apache-2.0 licensed.

## Problem

Removing the wrong linked worktree can discard untracked or unmerged work. Merging from the wrong checkout or branch can apply a valid command to the wrong target. Ordinary status output can also omit files hidden by index flags.

## Mechanism

Worktree Guard performs read-only Git checks for two operations. `merge-check` requires the main worktree, expected base branch, clean state, and a local incoming branch with unmerged commits. `remove-check` requires a registered, unlocked linked worktree with no unfinished operation, changes, concealed index entries, or unretained commits. Structured refusals use stable reason codes.

The combined demo checks the main checkout immediately before a fast-forward merge, then checks that the linked worktree is clean and its HEAD is retained by `main` immediately before ordinary removal.

## Failure boundaries

The checks are observations, not a transaction. They do not run tests, predict merge conflicts, fetch remote state, perform the merge, or remove the worktree. Another writer can invalidate the result after inspection. Squash integration may be refused because commit ancestry, rather than patch equivalence, is the evidence. The demo therefore places each check and its following mutation under a cooperating Shell Lock.

## Reproduce

```sh
worktree-guard merge-check ./main --base main --branch task --json
git -C ./main merge --ff-only task
worktree-guard remove-check ./task-worktree --base main --json
git -C ./main worktree remove ./task-worktree
```

`make demo` creates and removes both checkouts entirely under a temporary directory.
