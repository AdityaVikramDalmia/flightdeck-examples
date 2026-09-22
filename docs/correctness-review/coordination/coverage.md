# Coverage and limits

Read each component's `AGENTS.md`, named maintainer `SKILL.md`, README,
PROVENANCE, release index, relevant command/storage contracts, implementation, and
existing test names plus focused boundary-test bodies. Existing passing receipts
were contextual evidence, not proof of the additional boundaries investigated.

| Component | Source review focus | New execution result |
| --- | --- | --- |
| Gate Runner | Terminal evidence validation, lock inheritance, supervisor signals, publication, per-worktree latest pointer | One late-signal boundary reproduced; latest-pointer fixture failed before establishing the claimed behavior |
| Shell Lock | Final-component symlinks, inode checks after acquisition, inherited descriptors, signal forwarding, closed stdio | No fresh execution; no confirmed new defect |
| durable-mailbox | Envelope screening, archive enumeration, non-replacing moves, acknowledgment, print-before-consume, drain locks | Candidate probe authored but never executed; no confirmed new defect |
| Job Heartbeat | Serialization, generation comparison, terminal state, duplicate keys, bounded reads, anchored directory operations, atomic publication | No fresh execution; no confirmed new defect |

## C2: latest-pointer candidate not established

The code publishes each worktree's latest pointer while holding only that key's
lock (`gate_runner/cli.py:263-280`). A scheduling hypothesis was that an older
attempt delayed before latest publication could overwrite a pointer for a newer
attempt using another key. The contract describes latest as the most recently
created attempt.

The authored probe delayed the older start at `atomic(latest, ...)`, let a second
CLI start finish with exit 17, then resumed the older start. The fixture imported
the module directly with a temporary root spelled `/var/...`, while the CLI
canonicalized its root to `/private/var/...` on macOS. Consequently the two starts
did not address the same latest pointer. Default status returned the newer failed
run (exit 1), failing the probe's expectation of exit 0. This execution does not
prove the hypothesized race. The fixture was not repaired or rerun after the
parent's safety instruction.

## C3: malformed archive candidate not executed

`durable-mailbox/bin/mailbox:198` and `lib/core.sh:107-108` enumerate only `-f`
archive entries before validation. The authored candidate would replace synthetic
archived message entries with a dangling symlink, directory, or FIFO and compare
`asks`/`history` against a malformed regular-file control. This probe was never
reached. No runtime outcome or confirmed finding is asserted.

## Rejected or constrained hypotheses

- Gate Runner's non-atomic live-tree snapshot and changes reverted before its
  final check are explicitly documented limitations. They were not reported as
  newly discovered defects.
- Shell Lock verifies inode identity after acquiring the lock. Replacing an inode
  after that check requires violating its persistent-lock-path contract; hostile
  concurrent directory replacement is explicitly outside its trust model.
- Job Heartbeat checks generations under the store lock, refuses terminal
  resurrection, validates duplicate JSON keys, and opens record files with
  `O_NOFOLLOW` plus regular-file/single-link checks. No source-level path to a
  stale-generation overwrite was established.
- Mailbox documents possible duplicates between output and archive publication,
  lack of fsync durability, stale locks after SIGKILL, and last-writer attribution
  for concurrent acknowledgments. Those expected behaviors were not findings.
- Mailbox's multi-object JSON files were considered, then rejected as a new
  hypothesis because its `jq -se` validator requires exactly one object and its
  existing suite covers this boundary.

## Unfinished work

Fresh suite execution, independent reproduction, interruption around every
publication stage, and broader concurrent mutation schedules remain incomplete.
The review stopped because of the explicitly reported automated safety flag,
not because untested paths were judged safe. No whole-collection assurance can be
inferred from this bounded partial pass.
