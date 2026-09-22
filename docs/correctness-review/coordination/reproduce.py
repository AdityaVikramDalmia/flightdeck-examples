#!/usr/bin/env python3
"""Synthetic, offline coordination boundary probes. No source checkout writes."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from types import SimpleNamespace

sys.dont_write_bytecode = True


def run(argv, cwd, env, codes=(0,)):
    result = subprocess.run(list(map(str, argv)), cwd=cwd, env=env, capture_output=True, text=True, timeout=20)
    assert result.returncode in codes, (argv, result.returncode, result.stdout, result.stderr)
    return result


def prepare(base):
    root = base / "project"
    root.mkdir()
    home = base / "home"
    home.mkdir()
    env = {"PATH": os.environ["PATH"], "HOME": str(home), "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": os.devnull, "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C"}
    run(["git", "init", "-q", root], base, env)
    (root / "input.txt").write_text("synthetic input\n")
    run(["git", "add", "."], root, env)
    run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], root, env)
    return root, env


def signal_after_command(tools, base):
    root, env = prepare(base)
    wrapper = base / "wrappers"
    wrapper.mkdir()
    marker = base / "command-finished"
    evidence = base / "signal-sent"
    real_git = shutil.which("git", path=env["PATH"])
    # Only the post-command snapshot sees the marker. Send an actual SIGTERM to
    # the calling supervisor during check_output(), after its interrupted guard.
    (wrapper / "git").write_text(
        "#!" + sys.executable + "\nimport os,signal,sys\nfrom pathlib import Path\n"
        + "marker=Path(" + repr(str(marker)) + ")\n"
        + "evidence=Path(" + repr(str(evidence)) + ")\n"
        + "if marker.exists() and not evidence.exists():\n"
        + " evidence.write_text(str(os.getppid()))\n os.kill(os.getppid(),signal.SIGTERM)\n"
        + "os.execv(" + repr(real_git) + ", [" + repr(real_git) + ", *sys.argv[1:]])\n")
    (wrapper / "git").chmod(0o755)
    env["PATH"] = str(wrapper) + os.pathsep + env["PATH"]
    tool = tools / "gate-runner/bin/gate-run"
    command = [sys.executable, "-c", "from pathlib import Path; Path(" + repr(str(marker)) + ").touch()"]
    argv = [tool, "--runs-dir", base / "state", "--json", "start", "--wait", "--", *command]
    first = run(argv, root, env)
    row = json.loads(first.stdout)
    assert evidence.exists() and row["state"] == "pass", first.stdout
    meta = json.loads((Path(row["path"]) / "meta.json").read_text())
    assert evidence.read_text() == str(meta["supervisor_pid"])
    cached = json.loads(run(argv, root, env).stdout)
    assert cached["attempt"] == row["attempt"] and cached["state"] == "pass"
    return {"finding": "C1", "actual_exit": first.returncode, "actual_state": row["state"],
            "signal": "SIGTERM delivered by final-snapshot Git shim to verified supervisor PID",
            "same_attempt_reused_as_pass": True, "expected": "error, exit 6"}


def latest_race(tools, base):
    root, env = prepare(base)
    spec = importlib.util.spec_from_file_location("review_gate", tools / "gate-runner/gate_runner/cli.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    saved_env = os.environ.copy()
    os.environ.clear()
    os.environ.update(env)
    store = base / "state"
    args = SimpleNamespace(command=[sys.executable, "-c", "pass"], env=[], env_key=[], shell=None,
                           salt="older-success", input=[], force=False, wait=True, timeout=10)
    key, request, command_env = module.config(args, root)
    ready, release = threading.Event(), threading.Event()
    original_atomic = module.atomic
    results, failures = [], []

    def delayed_atomic(path, value):
        if path.parent.name == "latest":
            ready.set()
            assert release.wait(10), "barrier timed out"
        return original_atomic(path, value)

    def older_start():
        try:
            results.append(module.start(args, store, key, request, command_env))
        except BaseException as exc:
            failures.append(repr(exc))

    module.atomic = delayed_atomic
    worker = threading.Thread(target=older_start)
    worker.start()
    try:
        assert ready.wait(10), "older attempt did not reach latest publication"
        tool = tools / "gate-runner/bin/gate-run"
        newer = json.loads(run([tool, "--runs-dir", store, "--json", "start", "--wait", "--salt", "newer-failure",
                                "--", sys.executable, "-c", "raise SystemExit(17)"], root, env, codes=(1,)).stdout)
        release.set()
        worker.join(15)
        assert not worker.is_alive() and not failures, failures
        default = json.loads(run([tool, "--runs-dir", store, "--json", "status"], root, env).stdout)
        older = results[0]
        old_time = json.loads((Path(older["path"]) / "meta.json").read_text())["started"]
        new_time = json.loads((Path(newer["path"]) / "meta.json").read_text())["started"]
        assert old_time < new_time and default["key"] == key and default["state"] == "pass"
        return {"finding": "C2", "older_created_before_newer": True, "newer_state": newer["state"],
                "newer_exit_code": newer["exit_code"], "default_status_state": default["state"],
                "default_selects_older_attempt": True,
                "expected": "default latest selects the newer-created failed attempt"}
    finally:
        release.set()
        worker.join(15)
        os.environ.clear()
        os.environ.update(saved_env)


def mailbox_bad_archives(tools, base):
    root, env = prepare(base)
    tool = tools / "durable-mailbox/bin/mailbox"
    state = base / "state"
    results = []
    for kind in ("broken-symlink", "directory", "fifo", "malformed-regular-control"):
        sent = run([tool, "--dir", state, "send", kind, "ask", "synthetic question"], root, env)
        name = Path(sent.stdout.strip()).name
        run([tool, "--dir", state, "drain", kind, "--format", "json"], root, env)
        archive = state / kind / "cur" / name
        # Preserve the body under a non-message suffix, then replace only the
        # synthetic archive entry. No concurrent hostile writer is required.
        archive.rename(archive.with_suffix(".saved"))
        if kind == "broken-symlink":
            archive.symlink_to("missing-synthetic-target")
        elif kind == "directory":
            archive.mkdir()
        elif kind == "fifo":
            os.mkfifo(archive)
        else:
            archive.write_text("{broken\n")
        expected_codes = (3,) if kind == "malformed-regular-control" else (0,)
        asks = run([tool, "--dir", state, "asks", kind], root, env, codes=expected_codes)
        history = run([tool, "--dir", state, "history", kind], root, env, codes=expected_codes)
        if kind != "malformed-regular-control":
            assert "no open asks" in asks.stdout and not history.stdout
        results.append({"entry_type": kind, "asks_exit": asks.returncode, "asks_stdout": asks.stdout.strip(),
                        "history_exit": history.returncode, "history_stdout": history.stdout.strip()})
    return {"finding": "C3", "expected": "nonzero rather than clean empty observations for invalid archived .json entries", "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools-root", type=Path, required=True)
    parser.add_argument("--case", choices=("all", "signal", "latest", "archives"), default="all")
    args = parser.parse_args()
    tools = args.tools_root.resolve()
    revisions = {name: subprocess.check_output(["git", "-C", str(tools / name), "rev-parse", "HEAD"], text=True).strip()
                 for name in ("gate-runner", "shell-lock", "durable-mailbox", "job-heartbeat")}
    probes = {"signal": signal_after_command, "latest": latest_race, "archives": mailbox_bad_archives}
    output = {"revisions": revisions, "probes": []}
    for name, probe in probes.items():
        if args.case in ("all", name):
            with tempfile.TemporaryDirectory(prefix="flightdeck-coordination-review-") as directory:
                output["probes"].append(probe(tools, Path(directory)))
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
