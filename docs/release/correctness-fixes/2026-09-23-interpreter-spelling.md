# 2026-09-23: cleanup interpreter spelling

**Symptom.** On macOS with a non-framework Python first on `PATH` (measured with conda; pyenv and uv were not tested), `test_interruption_reaps_detached_gate` failed: cleanup reported "could not verify completion; retaining fixture", and the detached supervisor kept running until its synthetic command ended.

**Root cause.** At `698367b`, `examples/cleanup-gate.py:39-43` took the expected interpreter from `ps -o comm=`, which is argv[0]. The demo starts cleanup as a bare `python3` (`examples/end-to-end-demo.sh:50`), while Gate Runner starts its supervisor as `[sys.executable, …]` (`gate_runner/cli.py:290`), a full path. Only framework Python agreed, because it re-execs into `Python.app` and rewrites argv[0] for both processes.

**Fix.** Cleanup accepts exactly its own interpreter's two spellings: `sys.executable`, and on macOS its own `ps` argv[0]. The script path, `_supervise` operation, exact attempt path, descriptor arguments, metadata-only PID selection and pre-signal recheck are unchanged. Linux behaviour is identical.

**Regression test.** `test_cleanup_reaps_supervisor_named_by_sys_executable` runs cleanup through a bare-named interpreter symlink against a synthetic supervisor whose command starts with `sys.executable`. It runs in `make test`, or alone:
`PYTHONDONTWRITEBYTECODE=1 python3 tests/smoke.py Smoke.test_cleanup_reaps_supervisor_named_by_sys_executable`

**Receipts (macOS arm64).** Against the old cleanup the new test failed (`1 != 0 … retaining fixture`) under conda Python 3.13.5 and Homebrew framework Python 3.14.6. With the fix, full `make test` ran 11 tests, OK, under conda 3.13.5, framework 3.14.6 and `/usr/bin/python3` 3.9.6. Linux was not re-run for this change.

[host-validation.json](host-validation.json), [changes.md](changes.md) and the readiness [fix review](../readiness/fix-review.md) remain the 2026-09-22 record for `cc4c615` and are not edited.
