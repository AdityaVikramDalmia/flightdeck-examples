# Run the examples

From the companion checkout:

```sh
make smoke
make demo
```

The smoke suite validates catalog/document consistency, runs the core workflow,
checks fixture isolation and interrupted process cleanup, and executes separate
recipes whose tool checkouts are present. The core workflow uses six repositories,
with an optional Repo Health observation. It is unchanged by the extra utilities.

| Command | Demonstrated contract |
| --- | --- |
| `bash examples/heartbeat-recipe.sh` | Generation replacement refuses a stale writer; completion cannot be revived by touch |
| `bash examples/config-baseline-recipe.sh` | A synthetic reference matches initially, then reports a content change and an added file |
| `bash examples/review-receipts-recipe.sh` | A rejecting review can still match current bytes; editing a selected file makes its binding stale |
| `bash examples/decision-ledger-recipe.sh` | Original words remain distinct from interpretation; questions and answers retain linked history |

Each recipe needs its matching sibling checkout and owns its temporary fixture.
Running a recipe directly with a missing checkout reports an error; optionality
means the smoke suite can omit that recipe when its checkout is absent. No recipe
requires a network connection, model, service credentials, or paid resource.

A matching Review Receipts check is not approval. A Decision Ledger entry is a
caller's attributed report, not authentication of the person named in it. The
[contract table](../architecture/contracts.md) separates observations from the
caller's responsibility for using them.
