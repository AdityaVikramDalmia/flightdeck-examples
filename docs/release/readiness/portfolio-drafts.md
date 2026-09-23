# Portfolio drafts and publication boundary

The portfolio uses its existing Astro blog collection and portfolio-blog skill. Four existing articles were reviewed and improved; no article-per-command expansion was added. Withdrawal source `3a309a26e91e4cba7ce3fd07cddcefd8d01bbc39` sets all four to `draft: true`; later draft-only refinement `df772e225c8e331af3701189b6702486cb6082c5` explains the independently verified fixes. All 77 generated site files remain byte-identical to the deployed withdrawal build. Their actual publication date, 2026-09-22, and July–August source / September extraction work periods are preserved.

| Article slug | Engineering focus and claims |
| --- | --- |
| `agent-tooling-extracting-the-useful-parts` | Complete mechanisms, explicit dependencies, historical versus current validation; eleven projects/thirteen tools/twelve repositories; truthful provenance |
| `agent-tooling-state-that-survives-the-terminal` | Delivery/acknowledgement, lifecycle reports, generations, original decision words; retry and idempotency limits |
| `agent-tooling-guarding-local-change` | Declared-input checks, final cancellation boundary, cooperating mutation, cleanup ownership; C1/E2 observed failures |
| `agent-tooling-evidence-without-green-lights` | Unknown inspection states, bounded comparisons, freshness versus approval; E1 failed query versus empty answer |

Claims are grounded in per-component contracts, PROVENANCE.md, [provenance audit](provenance.md), [exact fix review](fix-review.md), and retained historical receipts. No adoption/performance metrics or universal native replacements are asserted. The drafts describe the reproduced failures and verified repair boundaries at Gate Runner `3c246b7` and Examples `cc4c615`, with independent execution at the receipt-bearing tips pinned in the manifest. Final editorial review must reconcile any later fix wording before republication.

The portfolio's `docs/project-stories/agent-tooling/readiness/` records claim mapping, actual source revisions, artifact/browser checks and withdrawal evidence. Its artifact check excludes these four routes and every draft link from generated HTML/XML/JSON, including homepage, blog index, product archive, tags, series navigation, RSS and sitemap; it retains the other sixteen published article routes. The case study stays published and the product archive may remain with zero articles.

All four previously live article URLs were withdrawn through the portfolio's existing deployment workflow from withdrawal source `3a309a2`. Forty-one normal TLS-verifying public-edge checks confirm the four articles return 404 (three URL forms each) and the other sixteen published article routes return 200. Fresh workstation browser navigation still encounters a certificate warning; no bypass occurred. This browser-path gap remains separate from the passing edge HTTP checks.

Public repository links must work before articles are enabled. No source visibility or article publication change is executed by this readiness record.
