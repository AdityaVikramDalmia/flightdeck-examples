# Distribution, licensing, and private-data audit

The read-only GitHub queries in [repository-audit.json](repository-audit.json)
returned the expected `AdityaVikramDalmia/flightdeck-*` identity and private
visibility for all twelve repositories. Each local origin matched that identity.
These are timestamped observations, not a future visibility guarantee. Local
preparation and fix commits have not been pushed; a remote license response does
not establish what the local candidate contains.

All twelve local distributions contain the same Apache-2.0 LICENSE bytes and an
individual NOTICE naming Aditya Dalmia, copyright 2026. Each has PROVENANCE.md,
source-history documentation, a contributing guide, security contact, and a
named maintainer skill. The owner-selected licensing decision is consistently
dated 2026-09-22. This is an attribution inventory, not independent verification
of the author's complete chain of title or a legal opinion.

The tracked inventory has no vendored dependency source trees, Git submodules,
or tracked symlinks. Python tools import the standard library; shell tools invoke
the documented installed Bash, Git, jq, Perl, Make, and ordinary operating-system
utilities. No third-party code tree requiring an additional bundled notice was
identified. External executables retain their own licenses. The local Alpine
validation image is a test environment and is not shipped by these repositories.

README banners, release indexes, repository instructions, maintainer skills,
examples catalog, and companion status all retain private/deferred/deprecated
positioning. GitHub URLs are collaborator identifiers rather than public download
claims. The maintainer decision does not assert that native Claude Code features
replace every utility.

The [tracked-file audit](distribution-audit.json) looked for personal absolute
paths, private network endpoints, private-project references, runtime database or
JSONL/key/credential filenames, and vendored directories. No operational corpora,
ledgers, transcripts, credentials, or machine-specific runtime dependencies were
identified in the inspected distribution. The three private-project-name hits in
historical correctness-review documentation describe excluded scope; they do not
contain that project's data and were preserved as historical evidence. This
focused inventory does not prove absence of arbitrary private text.

Several existing local checkouts contain ignored Python bytecode left by earlier
checks. All ignored files observed were `__pycache__/*.pyc`; none are tracked or
copied by the fresh-clone validation procedure. These local caches are distinguished
from distribution contents rather than silently described as absent.

Original source access was limited to scoped Git history metadata for the named
mechanism paths. No original live runtime, ledger, transcript, credential, source
remote, or full private history was copied into the candidate.
