#!/usr/bin/env python3
"""Contract and fixture-isolation checks using only synthetic local state."""
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples/end-to-end-demo.sh"
TOOLS = Path(os.environ.get("FLIGHTDECK_TOOLS_ROOT", ROOT.parent)).resolve()
TOOL_NAMES = ("gate-runner", "durable-mailbox", "session-ledger", "agent-file-guards", "worktree-guard", "shell-lock")


class Smoke(unittest.TestCase):
    def test_catalog_and_documents(self):
        catalog = json.loads((ROOT / "catalog.json").read_text())
        self.assertEqual(catalog["visibility"], "private")
        self.assertFalse(catalog["public_availability_implied"])
        cases = catalog["case_studies"]
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertEqual(set(TOOL_NAMES) | {"repo-health", "job-heartbeat", "config-baseline", "review-receipts", "decision-ledger"}, {case["id"] for case in cases})
        self.assertEqual(catalog["tool_repository_count"], len(cases))
        self.assertEqual(catalog["utility_count"], sum(len(case["tools"]) for case in cases))
        self.assertEqual(catalog["tool_repository_count"], 11)
        self.assertEqual(catalog["utility_count"], 13)
        self.assertEqual(catalog["license_status"], "Apache-2.0")
        self.assertTrue((ROOT / "LICENSE").is_file())
        self.assertTrue((ROOT / "NOTICE").is_file())
        self.assertEqual(catalog["maintenance_status"], "deprecated")
        self.assertEqual(catalog["repository_count_including_companion"], len(cases) + 1)
        self.assertEqual(catalog["release_status"], "private-candidate")
        self.assertTrue((ROOT / catalog["integration_demo"]).is_file())
        index = (ROOT / "docs/portfolio/README.md").read_text()
        for case in cases:
            self.assertEqual(case["visibility"], "private")
            self.assertEqual(case["repository"], "https://github.com/AdityaVikramDalmia/flightdeck-" + case["id"])
            document = ROOT / case["document"]
            self.assertTrue(document.is_file())
            self.assertIn(document.name, index)
            self.assertIn("Apache-2.0", document.read_text())
            self.assertEqual(case["maintenance_status"], "deprecated")
        self.assertEqual(len(list((ROOT / "docs/portfolio").glob("[0-9][0-9]-*.md"))), len(cases))

    def test_artifact_links_and_portability(self):
        for base in (ROOT / "docs", ROOT / "examples"):
            for path in base.rglob("*"):
                if not path.is_file() or path.suffix not in (".md", ".sh", ".py"):
                    continue
                text = path.read_text()
                self.assertNotRegex(text, r"/Users/|/home/[^/]+/")
                if path.suffix == ".md":
                    for link in re.findall(r"\]\(([^)]+)\)", text):
                        if "://" not in link and not link.startswith("#"):
                            self.assertTrue((path.parent / link.split("#")[0]).exists(), (path, link))
        for script in (ROOT / "examples").glob("*.sh"):
            subprocess.run(["bash", "-n", str(script)], check=True)

    def test_complete_demo_and_cleanup(self):
        with tempfile.TemporaryDirectory(prefix="example smoke ") as temporary:
            env = dict(os.environ, TMPDIR=temporary)
            # Ambient Git routing/config and Make includes must not redirect
            # fixture work into another checkout or execute caller recipes.
            env.update(GIT_DIR=temporary + "/not-a-repo", GIT_WORK_TREE=temporary,
                       GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="invalid", GIT_CONFIG_VALUE_0="invalid",
                       MAKEFILES=temporary + "/must-not-load.mk")
            Path(env["MAKEFILES"]).write_text("$(error caller Makefile was loaded)\n")
            result = subprocess.run(["bash", str(DEMO), "--tools-root", str(TOOLS)],
                                    env=env, text=True, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS: six repositories composed", result.stdout)
            if (TOOLS / "repo-health/bin/repo-health").is_file():
                self.assertIn("optional seventh repository: health report verified", result.stdout)
            self.assertFalse(list(Path(temporary).glob("flightdeck-example.*")))
            self.assertFalse(Path(env["GIT_DIR"]).exists())

    def test_six_tool_layout_without_optional_scanner(self):
        with tempfile.TemporaryDirectory(prefix="example six tools ") as temporary:
            scratch = Path(temporary)
            layout = scratch / "tool checkouts"
            layout.mkdir()
            for name in TOOL_NAMES:
                (layout / name).symlink_to(TOOLS / name, target_is_directory=True)
            result = subprocess.run(["bash", str(DEMO)],
                                    env=dict(os.environ, TMPDIR=temporary, FLIGHTDECK_TOOLS_ROOT=str(layout)),
                                    text=True, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS: six repositories composed", result.stdout)
            self.assertNotIn("optional seventh repository", result.stdout)
            self.assertFalse(list(scratch.glob("flightdeck-example.*")))

    def test_additional_recipes_when_tools_are_present(self):
        recipes = {"job-heartbeat": "heartbeat-recipe.sh", "config-baseline": "config-baseline-recipe.sh",
                   "review-receipts": "review-receipts-recipe.sh", "decision-ledger": "decision-ledger-recipe.sh"}
        for tool, recipe in recipes.items():
            if not (TOOLS / tool).exists():
                continue
            self.assertTrue((TOOLS / tool / "bin" / tool).is_file(), "incomplete optional checkout: " + tool)
            with self.subTest(tool=tool), tempfile.TemporaryDirectory(prefix="example recipe ") as temporary:
                result = subprocess.run(["bash", str(ROOT / "examples" / recipe)],
                                        env=dict(os.environ, TMPDIR=temporary, FLIGHTDECK_TOOLS_ROOT=str(TOOLS)),
                                        text=True, capture_output=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                if tool == "review-receipts":
                    self.assertIn("rejecting verdict preserved", result.stdout)
                    self.assertIn("changed bytes stale", result.stdout)
                elif tool == "decision-ledger":
                    self.assertIn("original words and interpretation stay separate", result.stdout)
                    self.assertIn("both answers retain history", result.stdout)
                self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_invalid_root_creates_no_fixture(self):
        with tempfile.TemporaryDirectory(prefix="example missing ") as temporary:
            result = subprocess.run(["bash", str(DEMO), "--tools-root", temporary],
                                    env=dict(os.environ, TMPDIR=temporary), text=True,
                                    capture_output=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("required executable is missing", result.stderr)
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_final_ledger_query_checks_status_and_output(self):
        for operation, status, output in (("live", 75, ""), ("validate", 75, ""),
                                          ("live", 0, "unexpected-live-session")):
            with self.subTest(operation=operation, status=status), tempfile.TemporaryDirectory(prefix="example ledger failure ") as temporary:
                scratch = Path(temporary).resolve()
                home = scratch / "home"
                home.mkdir()
                layout = scratch / "tools"
                layout.mkdir()
                for name in TOOL_NAMES:
                    if name != "session-ledger":
                        (layout / name).symlink_to(TOOLS / name, target_is_directory=True)
                wrapper = layout / "session-ledger/bin/session-ledger"
                wrapper.parent.mkdir(parents=True)
                wrapper.write_text("#!/bin/sh\n" +
                                   f'if [ "$3" = {shlex.quote(operation)} ]; then\n' +
                                   "  echo 'synthetic ledger query injection' >&2\n" +
                                   f"  printf '%s' {shlex.quote(output)}\n  exit {status}\nfi\n" +
                                   "exec " + shlex.quote(str(TOOLS / "session-ledger/bin/session-ledger")) + ' "$@"\n')
                wrapper.chmod(0o755)
                result = subprocess.run(["bash", str(DEMO), "--tools-root", str(layout)],
                                        env={"PATH": os.environ["PATH"], "HOME": str(home), "TMPDIR": str(scratch),
                                             "LANG": "C", "PYTHONDONTWRITEBYTECODE": "1"},
                                        text=True, capture_output=True, timeout=60)
                self.assertIn("synthetic ledger query injection", result.stderr)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn("PASS: six repositories composed", result.stdout)
                self.assertFalse(list(scratch.glob("flightdeck-example.*")))

    def test_cleanup_preserves_diagnostic_decoys(self):
        with tempfile.TemporaryDirectory(prefix="example cleanup identity ") as temporary:
            scratch = Path(temporary).resolve()
            fixture = scratch / "flightdeck-example.identity"
            fixture.mkdir()
            home = scratch / "home"
            home.mkdir()
            env = {"PATH": os.environ["PATH"], "HOME": str(home), "TMPDIR": str(scratch),
                   "LANG": "C", "PYTHONDONTWRITEBYTECODE": "1"}
            attempt = fixture / "main project/.git/gate-runner/runs/fixture/attempts/one"
            gate_script = (TOOLS / "gate-runner/gate_runner/cli.py").resolve()
            processes = []
            try:
                for label, argument in (("decoy", "diagnostic: _supervise " + str(attempt)),
                                        ("neighbor", "diagnostic: _supervise " + str(attempt).replace("identity/", "identity-neighbor/"))):
                    ready = scratch / (label + ".ready")
                    code = "from pathlib import Path; import sys,time; Path(sys.argv[1]).touch(); time.sleep(30)"
                    processes.append(subprocess.Popen([sys.executable, "-c", code, str(ready), argument],
                                                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                deadline = time.monotonic() + 5
                while not all((scratch / (label + ".ready")).exists() for label in ("decoy", "neighbor")):
                    self.assertLess(time.monotonic(), deadline, "fixture children did not start")
                    time.sleep(0.01)
                cleanup = [sys.executable, str(ROOT / "examples/cleanup-gate.py"), str(fixture), str(gate_script)]
                result = subprocess.run(cleanup, env=env, text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(all(proc.poll() is None for proc in processes))
                # Even a stale record naming the decoy PID cannot authorize a
                # signal when the complete interpreter/script/arguments differ.
                attempt.mkdir(parents=True)
                (attempt / "meta.json").write_text(json.dumps({"supervisor_pid": processes[0].pid}))
                result = subprocess.run(cleanup, env=env, text=True, capture_output=True, timeout=10)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("retaining fixture", result.stderr)
                self.assertTrue(all(proc.poll() is None for proc in processes))
            finally:
                for proc in processes:
                    if proc.poll() is None:
                        proc.terminate()
                    proc.wait(timeout=5)

    def test_cleanup_retains_attempt_without_supervisor_identity(self):
        with tempfile.TemporaryDirectory(prefix="example startup identity ") as temporary:
            fixture = Path(temporary) / "flightdeck-example.startup"
            metadata = fixture / "main project/.git/gate-runner/runs/fixture/attempts/one/meta.json"
            metadata.parent.mkdir(parents=True)
            metadata.write_text(json.dumps({"starter_pid": os.getpid()}))
            result = subprocess.run([sys.executable, str(ROOT / "examples/cleanup-gate.py"), str(fixture)],
                                    text=True, capture_output=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("retaining fixture", result.stderr)
            self.assertTrue(metadata.is_file())

    def test_interruption_reaps_detached_gate(self):
        with tempfile.TemporaryDirectory(prefix="example signal ") as temporary:
            scratch = Path(temporary)
            tools = scratch / "tools"
            tools.mkdir()
            for name in TOOL_NAMES[1:]:
                (tools / name).symlink_to(TOOLS / name, target_is_directory=True)
            binary = tools / "gate-runner/bin/gate-run"
            binary.parent.mkdir(parents=True)
            (binary.parent.parent / "gate_runner").symlink_to(TOOLS / "gate-runner/gate_runner", target_is_directory=True)
            binary.write_text("#!/bin/sh\nexec " + shlex.quote(str(TOOLS / "gate-runner/bin/gate-run")) +
                              " --json start --wait -- sh -c 'sleep 30; make test'\n")
            binary.chmod(0o755)
            output = scratch / "output.log"
            with output.open("w") as log:
                child = subprocess.Popen(["bash", str(DEMO), "--tools-root", str(tools)],
                                         env=dict(os.environ, TMPDIR=temporary), stdout=log,
                                         stderr=log, start_new_session=True)
                metadata = None
                try:
                    deadline = time.monotonic() + 20
                    while time.monotonic() < deadline and child.poll() is None:
                        for path in scratch.glob("flightdeck-example.*/main project/.git/gate-runner/runs/*/attempts/*/meta.json"):
                            record = json.loads(path.read_text())
                            if record.get("command_pid"):
                                metadata = record
                                break
                        if metadata:
                            break
                        time.sleep(0.05)
                    self.assertIsNotNone(metadata, output.read_text())
                    os.killpg(child.pid, signal.SIGTERM)
                    child.wait(timeout=15)
                    self.assertNotEqual(child.returncode, 0)
                    self.assertFalse(list(scratch.glob("flightdeck-example.*")), output.read_text())
                    for key in ("command_pid", "supervisor_pid"):
                        result = subprocess.run(["ps", "-p", str(metadata[key]), "-o", "stat="],
                                                text=True, capture_output=True)
                        self.assertTrue(not result.stdout.strip() or result.stdout.strip().startswith("Z"), key)
                finally:
                    if child.poll() is None:
                        os.killpg(child.pid, signal.SIGTERM)
                        child.wait(timeout=15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
