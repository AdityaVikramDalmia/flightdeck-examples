# Source history and attribution

Standalone composition and case studies were prepared on **2026-09-22**,
commit `d739eeccfffeabeb6621a5e02811cd79ea0a7fc5`. Component origins are recorded in their
respective PROVENANCE.md and docs/release/history.md files.


The source mechanism's earlier date does not date every feature in the standalone
implementation. `PROVENANCE.md` distinguishes retained behavior, rewritten code,
and newly added contracts. In particular, portability and hardening work belongs
to the September extraction. Source history was not imported: it contains private
operational material outside this package.

Aditya Dalmia designed and maintains this work, with AI coding assistance during
implementation, extraction, and review. Upstream runtimes, language libraries, Git,
and operating-system facilities remain their authors' work. No authorship of
Claude Code or its native messaging feature is claimed.

On **2026-09-22**, the owner selected Apache-2.0 and requested private preparation
for a later public launch. This change adds the license, copyright notice, and
maintenance guidance in a new commit with its actual date. Existing history and
author/committer timestamps are preserved; the timeline is not a reconstructed
contribution graph.

The maintainer also marked all twelve repositories deprecated for new Claude Code
integrations on **2026-09-22**. This is a present maintenance decision, not a
historical claim that all utilities were replaced by native features.
