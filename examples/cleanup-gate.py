#!/usr/bin/env python3
# Deprecated reference example for new Claude Code integrations (2026-09-22).
"""Stop only detached Gate Runner supervisors recorded by this disposable demo."""
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time


def live_command(pid):
    result = subprocess.run(
        ["ps", "-ww", "-p", str(pid), "-o", "stat=", "-o", "command="],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError("cannot inspect recorded supervisor")
    fields = result.stdout.strip().split(None, 1)
    return fields[1] if len(fields) == 2 and not fields[0].startswith("Z") else None


def owned(command, attempt, gate_script, interpreters):
    # ps does not quote paths containing spaces. Compare the complete expected
    # invocation, not tokens reconstructed with shlex or a substring anywhere
    # in arbitrary diagnostic text. Gate Runner supplies two descriptor numbers.
    invocation = " ".join((str(gate_script), "_supervise", str(attempt)))
    return any(re.fullmatch(re.escape(interpreter + " " + invocation) + r" [0-9]+ [0-9]+", command)
               for interpreter in interpreters if interpreter)


def main():
    fixture = Path(sys.argv[1]).resolve()
    gate_script = (Path(sys.argv[2]) if len(sys.argv) > 2 else
                   Path(__file__).resolve().parents[2] / "gate-runner/gate_runner/cli.py").resolve()
    if not fixture.name.startswith("flightdeck-example."):
        raise SystemExit("refusing cleanup of an unexpected fixture")
    # Gate Runner starts its supervisor as [sys.executable, ...]. macOS framework
    # Python re-execs into Python.app and rewrites that argv[0]; ps reports this
    # process's own spelling. Accept either; the rest must still match exactly.
    interpreters = {sys.executable}
    if sys.platform == "darwin":
        interpreters.add(subprocess.check_output(
            ["ps", "-ww", "-p", str(os.getpid()), "-o", "comm="], text=True).strip())
    victims = []
    uncertain = False
    # Select PIDs from our own attempt records, never from a machine-wide ps
    # substring search. A missing identity during startup retains the fixture.
    for metadata in (fixture / "main project/.git/gate-runner/runs").glob("*/attempts/*/meta.json"):
        attempt = metadata.parent.resolve()
        if fixture not in attempt.parents or metadata.is_symlink():
            uncertain = True
            continue
        try:
            record = json.loads(metadata.read_text())
            pid = record.get("supervisor_pid")
            if type(pid) is not int or pid <= 1:
                uncertain |= not (attempt / "result.json").is_file()
                continue
            command = live_command(pid)
            if command is None:
                continue
            if not owned(command, attempt, gate_script, interpreters):
                uncertain = True
                continue
            # Recheck immediately before signalling, including the recorded PID.
            if json.loads(metadata.read_text()).get("supervisor_pid") != pid or live_command(pid) != command:
                uncertain = True
                continue
            os.kill(pid, signal.SIGTERM)
            victims.append((pid, command))
        except ProcessLookupError:
            pass
        except (OSError, ValueError, AttributeError, RuntimeError):
            uncertain = True
    deadline = time.monotonic() + 5
    while victims and time.monotonic() < deadline:
        victims = [(pid, command) for pid, command in victims if live_command(pid) == command]
        if victims:
            time.sleep(0.05)
    if victims or uncertain:
        raise SystemExit("Gate Runner cleanup could not verify completion; retaining fixture: " + str(fixture))


if __name__ == "__main__":
    main()
