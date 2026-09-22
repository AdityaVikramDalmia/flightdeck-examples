# Revisions and validation record

Reviewed source revisions, read using `git rev-parse HEAD`:

| Repository | Revision |
| --- | --- |
| gate-runner | `587facdaff79fedadd1ea582f30ae5f8282874a2` |
| shell-lock | `1691f1b91b233a679b53277e035bcc20d82d3ef5` |
| durable-mailbox | `71604edb98abbd0d078eda1e48305aa9961beef4` |
| job-heartbeat | `b7b6fc619b12ecf9f6e19432f4404cad14c53967` |

## Single executed invocation

Working directory: the local `flightdeck-tools` collection root.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 .correctness-worktrees/flightdeck-examples/docs/correctness-review/coordination/reproduce.py --tools-root .
```

Observed: process exit 1 after approximately 2.6 seconds. The traceback reached
`latest_race` at its call to default `status`; `run` rejected return code 1 because
the probe expected 0. The returned status JSON contained:

```json
{
  "attempt": "1f76caaacc504c3a81b6cb2c4d7fd1bb",
  "ended": 1790070622.7207592,
  "exit_code": 17,
  "key": "527e95a0aa9b2e1571fa0522f1e96b2e84a9eb2eb3d4f856514aab7eea510cd4",
  "started": 1790070622.577909,
  "state": "fail"
}
```

Temporary absolute path fields have been omitted from this excerpt. It records
the actual failing fixture assertion, not validation of C2. C1 ran before C2 and
all C1 assertions completed; C3 did not run. No aggregate JSON was printed because
the script emits it only after every requested probe finishes.

## Isolation and artifact scope

The script creates only synthetic temporary fixtures and stores, disables Python
bytecode generation, replaces HOME with an empty fixture directory, disables
system/global Git config, and invokes only local tools. Its command, marker,
signal target, and Git repository are all fixture-owned. No source repositories
were intentionally modified. No final cleanliness scan or fresh suite run was
performed after the parent instructed that execution stop.

The reviewer wrote only this coordination subtree in the parent's examples
documentation worktree. It made no commits; the parent owns final review and the
documentation commit. No fix worktree was needed because no source fixes were
prepared.
