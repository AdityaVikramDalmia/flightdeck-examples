# Config Baseline: explicit configuration drift evidence

Private repository: `github.com/AdityaVikramDalmia/flightdeck-config-baseline` (authorized access required). Private candidate; redistribution license pending.

## Problem

A set of local configuration files can change in content, permissions, or link targets between reviews. A useful comparison must distinguish an actual match from an incomplete scan and must keep the reference outside the files being inventoried.

## Mechanism

Config Baseline inventories explicitly labeled roots and stores relative paths, entry types, permission modes, byte sizes, file hashes, and literal symlink targets. It reads files as bytes and never executes them or traverses symlink targets. Checks validate the reference first, then report added, removed, and changed entries. Missing selected roots are removals; invalid or unreadable input is an error.

The reference stores root labels rather than absolute locations, allowing deliberate relocation while preserving comparisons. Initial publication refuses to overwrite an existing reference, and scan budgets stop excessive entry counts, bytes, or depth before a partial scan can become a successful baseline.

## Failure boundaries

Matching recorded attributes is not a safety or malware certification. Ownership, ACLs, extended attributes, timestamps, and hard-link relationships are outside the inventory. Files can change between observations; stop writers when a consistent comparison matters. A schema-valid reference can still have been deliberately edited. Publication requests file and directory flushes but does not certify power-loss behavior. Explicit concurrent overwrites need caller coordination.

## Reproduce

From the tool checkout:

```sh
config-baseline snapshot --manifest ./references/config.json --root app=./app-config
config-baseline check --json --manifest ./references/config.json --root app=./app-config
```

The reference parent must already exist and be outside all selected roots. Run the [companion recipe](../../examples/config-baseline-recipe.sh) for an isolated example that creates and changes synthetic configuration, then verifies reported drift.
