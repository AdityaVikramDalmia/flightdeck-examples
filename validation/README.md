# Component validation

## Recorded candidate evidence

| Receipt | Scope |
|---|---|
| [component-commits.json](component-commits.json) | Exact clean commits for all eleven tool repositories |
| [fresh-clone-host.json](fresh-clone-host.json) | First five private remotes: fresh macOS clones, tests, install/demo checks |
| [fresh-clone-host-remaining.json](fresh-clone-host-remaining.json) | Next four private remotes, using the same protocol |
| [fresh-clone-host-final.json](fresh-clone-host-final.json) | Review Receipts and Decision Ledger private remotes |
| [linux-results.json](linux-results.json) | First nine frozen component commits in isolated Linux |
| [linux-additional-results.json](linux-additional-results.json) | Final two frozen component commits in isolated Linux |
| [integration-linux.json](integration-linux.json) | Full composition demo, seven smoke groups, and all four separate recipes |

All recorded suites passed. Four filesystem-case-equivalence tests are skipped
on the case-sensitive Linux fixture filesystem and pass on macOS. Private
visibility was checked against GitHub during the fresh-clone runs. These receipts
do not claim public availability, finalized licensing, or a cloud CI run.

## Reproduce

The harness runs each standalone repository's `make test` and records its exit,
test/group count, commit, cleanliness, and tool versions. Counts are not equivalent
units: Python unittest cases, TAP regression groups, and shell assertions differ.
Each result remains named rather than presenting a misleading single coverage score.

```sh
python3 validation/run.py --platform host --output validation/host-results.json

docker build -t flightdeck-validation:local validation/
python3 validation/run.py --platform linux --output validation/linux-results.json
```

By default sibling repos live next to this examples checkout. Use `--tools-root`
for a different layout and repeat `--only COMPONENT` to select a subset. The Docker
image build retrieves public OS packages; test containers have no network. Images
are built locally; no cloud CI or paid model calls are involved.

Linux tests run as a non-root user, against a copy of the component in an executable
temporary filesystem. The root filesystem and source mount are read-only. `exec`
on `/tmp` is necessary because the fixtures launch scripts; an ordinary noexec
tmpfs would only test the mount restriction.

The Dockerfile starts with Alpine's current local/tagged image. Receipts record
the built image ID and exact runtime versions, not a universal claim across all
Linux distributions or package versions. Dependencies are Bash, Python 3, Git, jq,
Perl, Make, and Unix utilities; each component documents its smaller runtime set.

Run against a clean committed checkout when producing a release receipt. Generated
raw logs are printed on failure but not persisted in JSON receipts, avoiding
accidental publication of environment values or unrelated diagnostic paths.
