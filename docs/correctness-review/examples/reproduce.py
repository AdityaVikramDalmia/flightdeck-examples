#!/usr/bin/env python3
"""Synthetic failure-boundary probes; exit zero means observations reproduced."""
import argparse
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import tempfile
import time


def environment(root):
    home = root / "home"
    home.mkdir(exist_ok=True)
    return {"PATH": os.environ["PATH"], "HOME": str(home), "TMPDIR": str(root),
            "LANG": "C", "PYTHONDONTWRITEBYTECODE": "1"}


def demo_failure(tools, operation):
    with tempfile.TemporaryDirectory(prefix="correctness examples ") as name:
        root = Path(name).resolve()
        layout = root / "tools"
        layout.mkdir()
        for component in ("gate-runner", "durable-mailbox", "agent-file-guards",
                          "worktree-guard", "shell-lock", "repo-health"):
            (layout / component).symlink_to(tools / component, target_is_directory=True)
        wrapper = layout / "session-ledger/bin/session-ledger"
        wrapper.parent.mkdir(parents=True)
        real = tools / "session-ledger/bin/session-ledger"
        wrapper.write_text("#!/bin/sh\n" +
                           f'if [ "$3" = {shlex.quote(operation)} ]; then\n' +
                           "  echo 'synthetic ledger query failure' >&2\n  exit 75\nfi\n" +
                           "exec " + shlex.quote(str(real)) + ' "$@"\n')
        wrapper.chmod(0o755)
        result = subprocess.run(["bash", str(tools / "flightdeck-examples/examples/end-to-end-demo.sh"),
                                 "--tools-root", str(layout)], env=environment(root),
                                text=True, capture_output=True, timeout=60)
        observed = {"operation": operation, "exit_code": result.returncode,
                    "failure_injected": "synthetic ledger query failure" in result.stderr,
                    "printed_pass": "PASS: six repositories composed" in result.stdout,
                    "fixture_removed": not list(root.glob("flightdeck-example.*"))}
        assert observed["failure_injected"] and observed["fixture_removed"], observed
        if operation == "live":
            assert result.returncode == 0 and observed["printed_pass"], observed
        else:
            assert result.returncode != 0 and not observed["printed_pass"], observed
        return observed


def cleanup_identity(tools):
    with tempfile.TemporaryDirectory(prefix="correctness cleanup ") as name:
        root = Path(name).resolve()
        fixture = root / "flightdeck-example.identity"
        fixture.mkdir()
        prefix = "_supervise " + str(fixture / "main project/.git/gate-runner/runs") + "/"
        processes = []
        try:
            # These are ordinary Python sleepers, not Gate Runner supervisors.
            # One merely carries a diagnostic string containing the fixture path.
            for label, argument in (("decoy", "diagnostic: " + prefix + "unused/attempts/one"),
                                    ("control", "diagnostic: " + prefix.replace("identity/", "identity-neighbor/"))):
                ready = root / (label + ".ready")
                code = "from pathlib import Path; import sys,time; Path(sys.argv[1]).touch(); time.sleep(30)"
                proc = subprocess.Popen([sys.executable, "-c", code, str(ready), argument],
                                        env=environment(root), stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                processes.append(proc)
            deadline = time.monotonic() + 5
            while not all((root / (label + ".ready")).exists() for label in ("decoy", "control")):
                if time.monotonic() > deadline:
                    raise RuntimeError("synthetic children did not start")
                time.sleep(0.01)
            result = subprocess.run([sys.executable,
                                     str(tools / "flightdeck-examples/examples/cleanup-gate.py"),
                                     str(fixture)], env=environment(root), capture_output=True,
                                    text=True, timeout=10)
            decoy, control = processes
            decoy.wait(timeout=3)
            observed = {"cleanup_exit": result.returncode, "decoy_exit": decoy.returncode,
                        "decoy_is_supervisor": False, "neighbor_control_alive": control.poll() is None}
            assert result.returncode == 0 and decoy.returncode == -signal.SIGTERM, observed
            assert observed["neighbor_control_alive"], observed
            return observed
        finally:
            for proc in processes:
                if proc.poll() is None:
                    proc.terminate()
                proc.wait(timeout=5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools-root", type=Path, required=True)
    args = parser.parse_args()
    tools = args.tools_root.resolve()
    result = {"examples_revision": subprocess.check_output(
        ["git", "-C", str(tools / "flightdeck-examples"), "rev-parse", "HEAD"], text=True).strip(),
        "E1_live_failure": demo_failure(tools, "live"),
        "E1_validate_failure_control": demo_failure(tools, "validate"),
        "E2_cleanup_identity": cleanup_identity(tools)}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
