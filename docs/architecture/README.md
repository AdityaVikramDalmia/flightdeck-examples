# How the tools fit together

The 11 tool repositories expose 13 independently usable utilities. The examples compose them through explicit
commands and local files; there is no shared hosted service to install.

| Guide | Purpose |
|---|---|
| [Getting started](../getting-started/README.md) | Checkout layout, prerequisites, and four separate recipes |
| [Workflow](workflow.md) | One reproducible work-and-review loop |
| [Contracts](contracts.md) | What each result establishes and what remains the caller's responsibility |
| [Portfolio case studies](../portfolio/README.md) | Individual engineering stories and reproduction commands |
| [Validation](../../validation/README.md) | macOS/Linux test harness and recorded evidence |

The end-to-end example uses deterministic shell work. It does not create an AI
agent or require a model account. An agent, CI job, or human can use the same
command interfaces in a larger workflow.
