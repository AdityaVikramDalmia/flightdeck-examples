#!/usr/bin/env python3
"""scripts/clone-all.sh against eleven synthetic local bare repositories."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/clone-all.sh"
NAMES = ("gate-runner", "durable-mailbox", "session-ledger", "agent-file-guards", "worktree-guard", "shell-lock",
         "repo-health", "job-heartbeat", "config-baseline", "review-receipts", "decision-ledger")


class CloneAll(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "missing " + str(SCRIPT))
        self.scratch = Path(tempfile.mkdtemp(prefix="clone all ")).resolve()
        self.addCleanup(shutil.rmtree, self.scratch)
        (self.scratch / "home").mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.scratch / "home"), "LANG": "C",
                    "GIT_CONFIG_NOSYSTEM": "1", "GIT_AUTHOR_NAME": "Fixture", "GIT_COMMITTER_NAME": "Fixture",
                    "GIT_AUTHOR_EMAIL": "fixture@example.invalid", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"}
        seed = self.scratch / "seed"
        self.git("init", "-q", str(seed))
        (seed / "README").write_text("fixture\n")
        self.git("-C", str(seed), "add", "README")
        self.git("-C", str(seed), "commit", "-q", "-m", "fixture")
        self.base = self.scratch / "remote base"
        for name in NAMES:
            self.git("clone", "-q", "--bare", str(seed), str(self.base / ("flightdeck-" + name + ".git")))
        # A copy inside a synthetic companion checkout exercises the default parent directory.
        self.tools = self.scratch / "tools root"
        self.script = self.tools / "flightdeck-examples/scripts/clone-all.sh"
        self.script.parent.mkdir(parents=True)
        shutil.copy2(SCRIPT, self.script)

    def git(self, *args):
        return subprocess.run(["git", *args], env=self.env, check=True, text=True, capture_output=True).stdout.strip()

    def clone_all(self, *args, base=None):
        env = dict(self.env, FLIGHTDECK_CLONE_BASE=base if base is not None else str(self.base) + "/")
        return subprocess.run(["bash", str(self.script), *args], env=env, text=True, capture_output=True, timeout=60)

    def origin(self, name):
        return self.git("-C", str(self.tools / name), "remote", "get-url", "origin")

    def expected(self, name):
        return str(self.base) + "/flightdeck-" + name + ".git"

    def test_clones_eleven_short_names_then_second_run_is_noop(self):
        first = self.clone_all()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        for name in NAMES:
            self.assertEqual(self.origin(name), self.expected(name))
            self.git("-C", str(self.tools / name), "rev-parse", "--verify", "HEAD")
        (self.tools / "gate-runner/untracked").write_text("keep\n")
        before = sorted(str(path) for path in self.tools.rglob("*"))
        second = self.clone_all(str(self.tools), base=str(self.base))
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(second.stderr, "")
        self.assertNotIn("cloned", second.stdout)
        self.assertEqual(sorted(str(path) for path in self.tools.rglob("*")), before)

    def test_existing_directories_are_reported_and_left_alone(self):
        other = "https://example.invalid/other.git"
        self.git("init", "-q", str(self.tools / "gate-runner"))
        self.git("-C", str(self.tools / "gate-runner"), "remote", "add", "origin", other)
        (self.tools / "shell-lock").mkdir()
        (self.tools / "shell-lock/notes").write_text("keep\n")
        result = self.clone_all()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("gate-runner", result.stderr)
        self.assertIn("shell-lock", result.stderr)
        self.assertEqual(self.origin("gate-runner"), other)
        self.assertEqual(os.listdir(self.tools / "shell-lock"), ["notes"])
        for name in NAMES:
            if name not in ("gate-runner", "shell-lock"):
                self.assertEqual(self.origin(name), self.expected(name))

    def test_failed_clone_and_usage_errors_exit_nonzero(self):
        shutil.rmtree(self.base / "flightdeck-decision-ledger.git")
        result = self.clone_all()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("decision-ledger", result.stderr)
        self.assertFalse((self.tools / "decision-ledger").exists())
        self.assertTrue(all((self.tools / name).is_dir() for name in NAMES if name != "decision-ledger"))
        usage = self.clone_all(str(self.scratch / "a"), str(self.scratch / "b"))
        self.assertEqual(usage.returncode, 2, usage.stdout + usage.stderr)
        self.assertFalse((self.scratch / "a").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
