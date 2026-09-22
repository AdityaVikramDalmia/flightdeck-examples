# Durable Mailbox: retained local handoff with explicit acknowledgment

Private repository: `github.com/AdityaVikramDalmia/flightdeck-durable-mailbox` (authorized access required). Private candidate; redistribution license pending.

## Problem

A shell workflow needs to hand a result to a named consumer without a server, while keeping evidence after the consumer drains its inbox. Questions need a distinct acknowledgment rather than assuming that output reaching a pipe means it was acted on.

## Mechanism

Durable Mailbox publishes complete JSON messages through a same-filesystem rename. Drains serialize per recipient, move emitted messages from `new/` to retained `cur/`, and preserve history. An `ask` remains open until `ack` writes an action marker. Verdict messages require an opaque receipt so the caller can point at the evidence it chose.

The combined demo sends the Gate Runner attempt as a verdict receipt, sends an acknowledgment question, drains both as JSONL, acknowledges the question by message ID, and confirms it is no longer open.

## Failure boundaries

Delivery is not exactly once. Interruption after printing and before archiving can produce a duplicate on the next drain. A successful drain says bytes were emitted, not that downstream processing succeeded. Locks are advisory and local; no automatic stale-lock deletion or cross-host guarantee exists. The tool does not interpret or fetch receipt references.

## Reproduce

With an explicit local store:

```sh
mailbox --dir ./mail send reviewer ask 'Review the receipt?' --from demo
mailbox --dir ./mail drain reviewer --format json
mailbox --dir ./mail ack reviewer MESSAGE_ID --from reviewer
mailbox --dir ./mail history reviewer
```

`make demo` performs the same round trip under a disposable directory.
