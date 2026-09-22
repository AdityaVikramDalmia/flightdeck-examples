#!/usr/bin/env python3
# Deprecated reference example for new Claude Code integrations (2026-09-22).
"""Stop only detached Gate Runner supervisors owned by this disposable demo."""
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def live_command(pid):
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "stat=", "-o", "command="],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    fields = result.stdout.strip().split(None, 1)
    return fields[1] if len(fields) == 2 and not fields[0].startswith("Z") else None


def owned(command, fixture):
    # ps renders paths with spaces without shell quoting. Match the absolute
    # attempt prefix between the supervisor mode and its descriptor argument.
    prefix = "_supervise " + str(fixture / "main project/.git/gate-runner/runs") + "/"
    return prefix in command


def main():
    fixture = Path(sys.argv[1]).resolve()
    if not fixture.name.startswith("flightdeck-example."):
        raise SystemExit("refusing cleanup of an unexpected fixture")
    processes = subprocess.check_output(["ps", "-ax", "-o", "pid=", "-o", "command="], text=True)
    victims = []
    for line in processes.splitlines():
        fields = line.strip().split(None, 1)
        if len(fields) != 2 or not owned(fields[1], fixture):
            continue
        pid = int(fields[0])
        command = live_command(pid)
        if command and owned(command, fixture):
            try:
                os.kill(pid, signal.SIGTERM)
                victims.append((pid, command))
            except ProcessLookupError:
                pass
    deadline = time.monotonic() + 5
    while victims and time.monotonic() < deadline:
        victims = [(pid, command) for pid, command in victims if live_command(pid) == command]
        if victims:
            time.sleep(0.05)
    if victims:
        raise SystemExit("owned Gate Runner supervisor did not stop; retaining fixture: " + str(fixture))


if __name__ == "__main__":
    main()
