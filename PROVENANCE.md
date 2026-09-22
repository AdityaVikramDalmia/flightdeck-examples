# Provenance

The case studies and integration example were derived from the documented command contracts and tests in sibling standalone repositories. Those repositories were themselves extracted or adapted from source revision `494799eea3b9e7ce8686506a288c297ccf96be8d`.

Inputs are referenced only by relative checkout name:

- `../gate-runner`
- `../durable-mailbox`
- `../session-ledger`
- `../agent-file-guards`
- `../worktree-guard`
- `../shell-lock`
- `../repo-health` (optional demo inspection)
- `../job-heartbeat` (separate recipe)
- `../config-baseline` (separate recipe)
- `../review-receipts` (separate recipe)
- `../decision-ledger` (separate recipe)

The end-to-end scenario is new composition code. It uses only synthetic local state and makes no claims about production impact or performance.

These artifacts are private candidates; redistribution license pending.

No private source remote or local user path is recorded here.
