# Rejected hypotheses and incomplete probes

## Not reported as defects

The source review considered the final checksum-to-rename window in shrink-guard
and the check-to-read symlink window in the scanners. The command contracts
explicitly require cooperating writers or a stable checkout and disclaim atomic
concurrent inspection. Merely rediscovering those admitted races would not meet
this review's requirement for reproduced defects.

Likewise, worktree-guard and repo-health explicitly describe their multiple Git
queries as observations rather than an atomic snapshot. An intervening writer
invalidating an earlier result was not promoted to a finding without a stronger
contract violation and a reproducer.

These are source-level dispositions, **not executed negative controls**. No
finding should cite them as experimental validation.

## Interrupted probe

A possible partial-clone/read-only boundary was identified for further
investigation, but an automated safety flag terminated the subagent turn before
fixture creation or execution. The parent then requested completed notes only;
the probe was not retried. No object fetch, repository mutation, network
operation, or reproduced defect was observed. The hypothesis remains unverified
and is deliberately excluded from findings.

## Remaining coverage gaps

There are no new executed tests in this lane for concurrent mutation, interrupted
writes, stale generations, malformed Git records, replacement symlinks, or
false-success paths. No source fix was proposed or validated. Existing passing
receipts cannot close those gaps. The final review must retain this limitation
even if other lanes have independently reproduced defects in their components.
