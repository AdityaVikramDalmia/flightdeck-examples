# Review Receipts: bind review words to exact selected files

Private repository: [flightdeck-review-receipts](https://github.com/AdityaVikramDalmia/flightdeck-review-receipts) (authorized access required). Private candidate; redistribution license pending.

## Problem

A document can change after someone reviews it while the old review still appears applicable. Timestamp comparisons can miss changed bytes or conflate a matching review with approval. An incomplete receipt can also silently narrow the intended review scope unless the checker independently supplies the expected files.

## Mechanism

Review Receipts stores the caller's reviewer identity, label, verdict, notes, and evidence references with each selected file's SHA-256, byte size, and POSIX mode. Check requires the expected file set again and compares every entry through descriptor-relative reads that refuse symlinks. Publication uses a complete JSON record and atomic no-clobber creation; intentional replacement requires an explicit flag.

The companion recipe authors a rejecting review over two files. A matching check exits zero while preserving `reject`: that result means the reviewed bytes are current, not approved. Changing one file produces stale exit 3 while retaining the original review words.

## Failure boundaries

A checksum does not prove review quality, authenticate the reviewer, or enforce a verdict policy. Someone able to edit a receipt can forge a consistent reference. Only explicitly selected files are covered; additional files are outside scope. Modes are bound, but ownership, ACLs, timestamps, and parent-directory permissions are not. Multi-file reads are observations rather than an atomic snapshot. A failed output stream can follow successful publication, so callers must inspect before retrying.

## Reproduce

```sh
bash examples/review-receipts-recipe.sh
```

Run from this companion checkout with `review-receipts/` beside it. The recipe creates and removes its own fixture, preserves notes and a rejecting verdict, and proves a content edit invalidates the prior binding.
