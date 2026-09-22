# Decision Ledger: keep original words distinct from interpretation

Deprecated reference material for new Claude Code integrations as of 2026-09-22.

Private repository: [flightdeck-decision-ledger](https://github.com/AdityaVikramDalmia/flightdeck-decision-ledger) (authorized access required). Private candidate; Apache-2.0 licensed; public launch deferred.

## Problem

A paraphrase can replace what someone actually said, and a later correction can erase the history needed to understand a decision. A question also needs an explicit answer relationship: removing it from an unanswered list should not imply the answer granted permission.

## Mechanism

Decision Ledger appends caller-reported decisions, questions, and answers in a local SQLite store. Original UTF-8 words remain in their own field; an optional one-line interpretation is stored separately. Corrections append records linked to the original decision. Answers link to their question, and history returns the original, all related events, and the latest committed answer or correction.

The companion recipe preserves original words including CRLF and trailing newlines, records an interpretation and a later correction, then asks a question and records two answers. It verifies that the original decision and first answer remain unchanged. The question leaves the unanswered list even though the latest answer still refuses permission.

## Failure boundaries

Actor and source labels are caller assertions, not authenticated identities or proof that the named person said those words. An interpretation can be wrong while still being faithfully stored. A current history item is selected by committed sequence, not authority or approval. The store and its schema must remain trusted; direct database changes are outside the cooperative append-only interface. A transaction can commit before stdout fails, so inspect history before retrying a write.

## Reproduce

```sh
bash examples/decision-ledger-recipe.sh
```

Run from this companion checkout with `decision-ledger/` beside it. The recipe initializes its own disposable store and verifies five linked events without contacting another person, a model, or a network service.
