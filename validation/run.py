#!/usr/bin/env python3
"""Run standalone component suites locally or in an isolated Linux container."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

COMPONENTS = ["gate-runner", "durable-mailbox", "session-ledger", "agent-file-guards",
              "worktree-guard", "shell-lock", "repo-health", "config-baseline", "job-heartbeat",
              "decision-ledger", "review-receipts"]


def capture(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return {"exit_code": result.returncode, "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()}


def count_checks(output):
    python = re.findall(r"Ran (\d+) tests? in", output)
    if python:
        return sum(map(int, python))
    tap = re.findall(r"^1\.\.(\d+)\s*$", output, re.MULTILINE)
    if tap:
        return sum(map(int, tap))
    tallies = re.findall(r"(\d+) passed, (\d+) failed", output)
    if tallies:
        return sum(int(passed) + int(failed) for passed, failed in tallies)
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--platform", choices=("host", "linux"), default="host")
    parser.add_argument("--image", default="flightdeck-validation:local")
    parser.add_argument("--only", action="append", choices=COMPONENTS)
    parser.add_argument("--output", type=Path, help="Write a structured receipt; no raw logs or environment values.")
    args = parser.parse_args()
    root = args.tools_root.resolve()
    names = args.only or COMPONENTS
    results = []
    versions = {"host_system": platform.system(), "host_machine": platform.machine(),
                "python": platform.python_version()}
    if args.platform == "linux":
        versions["image"] = capture(["docker", "image", "inspect", args.image, "--format", "{{.Id}}"])
        versions["container_tools"] = capture([
            "docker", "run", "--rm", "--network", "none", "--read-only", args.image,
            "sh", "-c", "python3 --version; git --version; jq --version; bash --version | head -1; perl -e 'print qq(Perl $^V\\n)'"])
    else:
        for name, command in (("git", ["git", "--version"]), ("jq", ["jq", "--version"]),
                              ("bash", ["bash", "--version"])):
            result = capture(command)
            result["stdout"] = result["stdout"].split("\n")[0]
            versions[name] = result
    for name in names:
        repo = root / name
        if not (repo / "Makefile").is_file():
            parser.error("missing component Makefile: " + name)
        head = capture(["git", "rev-parse", "HEAD"], repo)
        status = capture(["git", "status", "--porcelain"], repo)
        if args.platform == "linux":
            command = ["docker", "run", "--rm", "--network", "none", "--read-only",
                       "--tmpfs", "/tmp:rw,exec,mode=1777", "--mount",
                       "type=bind,source=" + str(repo) + ",target=/source,readonly", args.image,
                       "sh", "-c", "set -eu; cp -R /source /tmp/component; cd /tmp/component; make test"]
        else:
            command = ["make", "test"]
        started = time.monotonic()
        result = subprocess.run(command, cwd=repo, capture_output=True, text=True)
        output = result.stdout + "\n" + result.stderr
        row = {"component": name, "platform": args.platform, "exit_code": result.returncode,
               "checks_or_groups": count_checks(output), "seconds": round(time.monotonic() - started, 3),
               "skipped": sum(map(int, re.findall(r"\bskipped=(\d+)", output))),
               "commit": head["stdout"] if head["exit_code"] == 0 else None,
               "clean_checkout": status["exit_code"] == 0 and not status["stdout"]}
        results.append(row)
        print(json.dumps(row), flush=True)
        if result.returncode:
            # The terminal gets diagnostics; the durable receipt never copies raw logs.
            print(output[-18000:], file=sys.stderr)
    receipt = {"schema": 1, "recorded_at": datetime.now(timezone.utc).isoformat(),
               "platform": args.platform, "versions": versions, "results": results,
               "all_passed": all(item["exit_code"] == 0 for item in results)}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    return 0 if receipt["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
