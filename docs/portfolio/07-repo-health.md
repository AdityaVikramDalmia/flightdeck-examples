# Repo Health: distinguish observed state from missing evidence

Private repository: `github.com/AdityaVikramDalmia/flightdeck-repo-health` (authorized access required). Private candidate; redistribution license pending.

## Problem

An operator inspecting several Git projects needs to distinguish a clean checkout from a failed inspection, and a known upstream comparison from a repository with no upstream. Treating missing evidence as zero changed files or zero unpushed commits makes a summary misleading.

## Mechanism

Repo Health accepts explicit paths and returns ordered records for branch state, tracked and untracked changes, conflicts, and locally available upstream comparison. Missing upstream evidence produces `unknown` with null counts. A failed path or Git query produces an error while preserving results for the other inputs.

When this optional seventh checkout is available, the combined demo inspects its clean main checkout and a linked worktree containing one intentionally untracked file. It verifies clean and dirty states respectively, and verifies unknown sync because the synthetic project has no upstream.

## Failure boundaries

The scanner does not fetch: an equal local tracking ref does not prove the remote server is current. Exit zero means inspection succeeded; dirty and unknown states can still be present. Multiple Git queries are observations, not a snapshot. Git filters in a trusted repository can execute configured code, so the scanner is not a sandbox for hostile checkouts. Worktree Guard provides separate operation-specific preconditions.

## Reproduce

```sh
repo-health --json ./main './feature worktree'
```

Run `make demo` with `repo-health/` beside the six required tool checkouts to verify these states using synthetic paths. No remote or model is contacted.
