# Contracts at the boundaries

| Tool | Result means | Caller still owns |
|---|---|---|
| Gate Runner | One identified command completed with a recorded exit, or an explicit in-progress/error state | Declaring result-affecting inputs, stable worktree, meaningful tests |
| Durable Mailbox | Local publication/drain/acknowledgment operations completed according to the queue contract | Handling duplicates and determining successful application processing |
| Session Ledger | A validated caller report was appended and can be projected into lifecycle state | Reporting truthfully; establishing actual OS process state |
| Agent File Guards | A size policy, NUL scan, or static instruction/configuration inventory produced its documented result | Semantic review, trusted stable paths, and selecting the right files/policy |
| Worktree Guard | Supported local Git preconditions passed at inspection time | Stopping unrelated writers and performing ordinary Git operations without force |
| Shell Lock | Cooperating commands share an exclusive local lock | Using the same lock and preserving its inherited descriptor/file identity |
| Repo Health | Local Git queries produced observations, with missing/unsafe information marked UNKNOWN | Remote freshness, atomic snapshots, and decisions based on those observations |
| Config Baseline | The selected inventory matches or differs from a supplied reference | Establishing reference authenticity and deciding which differences matter |
| Job Heartbeat | The latest cooperative report is fresh, late, missing, unknown, or terminal | Actual process liveness and recovery policy |
| Review Receipts | The expected selected file bytes and modes match or differ from a stored caller-authored review | Authenticating the review, interpreting its verdict, and deciding approval; a current rejecting review still rejects |
| Decision Ledger | Original reported words, separate interpretation, corrections, and linked question/answer history were retained | Attribution, authority, accurate interpretation, and policy; an answered question is not necessarily approved |

These 11 tool repositories expose 13 utilities: Agent File Guards contains three independent commands.

Each component's own documentation is authoritative for its exact exit codes,
storage format, platform requirements, and failure boundaries. Test counts in
the validation receipts mix individual assertions, unittest cases, and regression
groups; they are reported separately and are not a code-coverage percentage.

The components do not import the original operator's project roster, transcripts,
global agent rules, account proxies, or private infrastructure configuration.
Private GitHub visibility and pending redistribution licensing are intentional
release status, not runtime dependencies.
