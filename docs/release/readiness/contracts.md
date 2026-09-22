# Setup and contract review

The independent lane read all twelve READMEs, provenance records, repository
instructions and named maintainer skills; reviewed installation Makefiles,
executable dependency imports, storage/input entry points and failure exits; and
compared companion catalog/contracts against component responsibilities. Existing
correctness-review source notes supplied additional boundary context. This is a
focused documentation/implementation consistency review, not a claim to have
re-read every implementation or test line.

| Repository | Setup and implementation contract checked | Boundary retained |
| --- | --- | --- |
| Gate Runner | Launcher stays beside its Python module; explicit command/input identity and Git-local state; interrupted runs return tool error | Reuse covers declared inputs, not a hermetic build; C1 repair has fresh host/Linux regression evidence |
| Durable Mailbox | `bin/` and `lib/` stay together; storage is explicit by flag/environment; drain locks and retained bodies | Delivery does not prove processing; duplicate output and lack of power-loss guarantees remain documented |
| Session Ledger | `bin/` and `lib/` stay together; explicit ledger location; validated append/readback and locked projections | Caller lifecycle reports do not establish OS process state |
| Agent File Guards | Three independently installable scripts; documented Perl/Git dependencies and 0/1/2/3 exit family | Static inventory is not a security certification; stable paths/cooperating writers remain required |
| Worktree Guard | Self-contained installed Python command; Git 2.36+; explicit worktree/base/branch checks | Inspection is read-only observation; split-index/submodule refusal and non-atomic preflight remain explicit |
| Shell Lock | Self-contained Python command; `fcntl.flock`, explicit persistent lock path and inherited descriptor | Cooperating local writers only; command and wrapper codes can overlap; never delete lock inode |
| Repo Health | Self-contained command; explicit input paths; local refs and structured UNKNOWN/error states | Exit zero is successful inspection, not a clean-tree or remote-freshness assertion |
| Job Heartbeat | Explicit directory and generation; self-contained standard-library command; serialized updates | Fresh/late/terminal reports do not prove liveness or successful work |
| Config Baseline | Explicit named roots and external manifest; bounded descriptor-relative reads and publication | Matching bytes/modes do not establish a safe reference; incomplete inspection is an error |
| Review Receipts | Explicit root and independently supplied selected files; standard-library command | A matching rejecting review still rejects; hashes do not authenticate reviewer or authorize release |
| Decision Ledger | Explicit initialized SQLite store; standard-library command; transaction-ordered corrections | Original words remain caller reports; a committed write may lack a receipt after output failure |
| Flightdeck Examples | Six required sibling repositories, five optional recipe/inspection repositories; no runtime service | Synthetic fixture ownership and fail-closed final query have fresh E1/E2 regression evidence |

No setup/contract mismatch beyond the three already reported correctness findings
was established by this audit. This statement does not close unexplored race or
interruption hypotheses. The final execution receipts distinguish individual
unittest cases, grouped shell regressions, assertions, smoke tests, and demo stages.

Installer commands that use `$HOME/.local` in READMEs are user-selectable examples,
not baked-in author-machine paths. Validation must use disposable prefixes; it
must not install over the user's commands. The eleven component suites and
companion smoke/demo must run from clean local clones at explicit commits.
