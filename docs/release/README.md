# Flightdeck Examples: release preparation

**Current:** [bounded release readiness, corrected candidates, receipts and later launch gates](readiness/README.md). The preparation snapshot below is historical; it does not describe the later corrected execution revisions.

Prepared on 2026-09-22. Apache-2.0 is applied at the owner's direction. The
repository remains private; adding a license is separate from public availability.
All twelve repositories are deprecated for new Claude Code integrations at the
maintainer's direction, effective 2026-09-22. They remain reference artifacts.

- [Source history and attribution](history.md)
- [Readiness and remaining launch work](readiness.md)
- [License](../../LICENSE) and [notice](../../NOTICE)
- [Component provenance](../../PROVENANCE.md)
- [Prepared macOS local-clone receipt](prepared-host.json)
- [Prepared isolated Linux receipt](prepared-linux.json)
- [Private remote and history-scan observations](prepared-repositories.json)

The original `validation/` files describe the extraction revisions. The receipts
above name the later preparation commits: all eleven component suites and the
companion smoke/demo checks passed, with zero macOS skips and four filesystem-case
skips on Linux. New fresh clones were **local clones**, since the preparation
commits have not been pushed. Do not describe them as new remote-clone checks.

The companion was tested at `3c6909d0b291218c442eb610f8792c5bce063147`.
A later evidence-only commit adds these receipts and this index; it changes no
implementation, test or demo source. Test counts retain their original units.
