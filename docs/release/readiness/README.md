# Independent release audit, 2026-09-22

This directory records a bounded release-readiness audit of eleven component
repositories exposing thirteen utilities, plus the twelfth examples repository.
At the audit all were private Apache-2.0 reference artifacts, deprecated for new Claude Code
integrations as of 2026-09-22. This audit lane performs no public launch, push, visibility change, cloud CI,
or original-runtime mutation. Any later private push by the coordinating parent
is a separate action with separate remote verification.

- [Exact twelve-repository candidate manifest](candidate-manifest.json)
- [Verdict and remaining gates](remaining-gates.md)
- [Four portfolio drafts and withdrawal](portfolio-drafts.md)
- [Ordered later release](release-sequence.md)
- [Repository identity and privacy observations](repository-audit.json)
- [Distribution and attribution audit](distribution.md), with [inventory observations](distribution-audit.json)
- [Secret-scan scope and adjudication](secret-scan.md)
- [Contracts and setup review](contracts.md)
- [Source dates and adaptation boundaries](provenance.md), with [metadata evidence](provenance-audit.json)
- [Independent review of the three repairs](fix-review.md)
- [Validation method and remaining gaps](validation.md)

The earlier `prepared-*.json` and `validation/` receipts remain unchanged. Their
passing results do not validate later code. The prior
[correctness review](../../correctness-review/README.md) is also preserved as a
partial investigation, including its three findings and automatic safety stop.
This audit does not replay its blocked experiments or claim complete adversarial
coverage. The corrected candidate passed one fresh local-clone component-suite run per
platform, fresh disposable installation/example checks, ten companion smoke
tests, and the seven-stage demo on macOS and isolated Linux. There were zero
macOS skips and four expected Linux case-equivalence skips. See the
[execution scope and results](validation.md); this is not a security certification.
