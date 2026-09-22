# Secret-scan observations

The [initial scan](initial-secret-scan.json) used Gitleaks 8.30.1 with an explicit
configuration extending its built-in default rules, no baseline, no ignore file,
and `--ignore-gitleaks-allow`. Logs/reports were redacted at 100%. Scanner environment
configuration overrides were removed. Git mode used `--log-opts=--all` in each
of the twelve local repositories, covering all reachable candidate history rather
than only the latest diff. Directory mode inspected each on-disk working tree.
The [final corrected candidate scan](final-secret-scan.json) is separate from
this initial observation and pins each candidate commit plus all ref tips. It
also scans the audit worktree documentation present at its timestamp.

Both initial and final scans gave the same adjudication. Eleven repositories
returned zero findings in both modes. Examples returned one
`generic-api-key` finding in history and one corresponding working-tree finding:
`docs/correctness-review/coordination/validation.md`, line 29. The value is the
synthetic Gate Runner `key` field in a retained failed scheduling-fixture status
JSON. Gate Runner derives that public result identifier as SHA-256 over declared
configuration and an input snapshot (`gate_runner/cli.py`, `digest` and `config`),
not from an authentication service or credential store. The surrounding receipt
records exit 17 and a failed assertion. Manual adjudication: one non-secret cache
identity, zero confirmed exposed credentials in these results.

The old evidence is preserved. The raw scanner count remains one rather than
being suppressed or represented as a clean zero. The same item is counted once
per scanner scope, not as two distinct credentials. Scanner output containing
candidate values was not printed or committed; only counts, location, rule and
adjudication are retained here.

Default recursive decoding depth is five; archive traversal is disabled by its
zero default. Directory symlinks are not followed. No tracked archives, vendored
binary distributions, or symlinks were identified by the file inventory. Novel
secret formats, private prose, excluded Git operational metadata, encrypted data,
or information outside these candidate repositories are not certified by this
scan. Original private Flightdeck history was deliberately not scanned or copied.
