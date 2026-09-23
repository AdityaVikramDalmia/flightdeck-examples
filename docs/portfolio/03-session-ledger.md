# Session Ledger: append-only lifecycle reports

Deprecated reference material for new Claude Code integrations as of 2026-09-22.

Repository: `github.com/AdityaVikramDalmia/flightdeck-session-ledger`. Public reference implementation; Apache-2.0 licensed.

## Problem

Local automation needs durable lifecycle history without discovering processes globally or overwriting the prior state. Readers need both exact event history and a projection of sessions that callers currently report as live.

## Mechanism

Session Ledger appends validated JSONL rows under one storage-local lock, assigns contiguous sequence numbers, and reads back the exact new row before printing its receipt. `history` preserves reports for one exact ID. `live` merges metadata and uses the latest lifecycle event to decide whether the caller-reported session remains active.

The combined demo records `launched` before any work, records `finished` with the Gate Runner attempt afterward, validates the ledger, and checks that `live` emits no remaining row.

## Failure boundaries

Rows are caller reports, not proof of operating-system liveness. The ledger deliberately accepts lifecycle corrections and does not enforce a state machine. A process can die after append but before receipt output, so retrying blindly can add a duplicate event. Validation is whole-ledger and local-filesystem oriented; malformed storage blocks further operations rather than being silently repaired.

## Reproduce

```sh
session-ledger --dir ./state append launched demo-session --by supervisor project=example
session-ledger --dir ./state live
session-ledger --dir ./state append finished demo-session result=passed
session-ledger --dir ./state history demo-session
session-ledger --dir ./state validate
```

`make demo` ties the final row to evidence from the other tools.
