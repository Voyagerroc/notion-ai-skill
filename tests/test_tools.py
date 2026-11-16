"""Offline installer/runner contracts; never invoke a real bridge or account."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import hybrid_runner, install_skill

ROOT = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="relay-tests-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.record = self.root / "record.txt"
        stub = self.root / "fake bridge.py"
        stub.write_text('''import json, os, pathlib, sys
record = pathlib.Path(sys.argv[1])
argv = sys.argv[2:]
prompt = pathlib.Path(argv[argv.index('-P') + 1])
record.write_text(str(prompt), encoding='utf-8')
if os.getenv('STUB_FAIL'):
    print('synthetic-private-value', file=sys.stderr)
    sys.exit(7)
print(json.dumps({'argv': argv, 'prompt': prompt.read_text(encoding='utf-8')}))
''', encoding="utf-8")
        self.command = [sys.executable, str(stub), str(self.record)]

    def test_selected_unicode_context_and_arguments_reach_real_stub(self):
        selected = self.root / "selected ü file.txt"
        selected.write_text("Türkçe selected context", encoding="utf-8")
        # The directory also contains an unselected credential-shaped file.
        (self.root / "accounts.json").write_text("must-not-read-this", encoding="utf-8")
        response = json.loads(hybrid_runner.run_hybrid_task(
            'Review & keep shell characters literal', [str(selected)], "auto", True,
            bridge_command=self.command))
        self.assertIn("Türkçe selected context", response["prompt"])
        self.assertNotIn("must-not-read-this", response["prompt"])
        self.assertTrue(response["prompt"].startswith("Review & keep shell characters literal"))
        self.assertEqual(response["argv"][:2], ["-m", "auto"])
        self.assertEqual(response["argv"][-1], "-t")
        self.assertFalse(Path(self.record.read_text(encoding="utf-8")).exists())

    def test_nonzero_bridge_does_not_echo_sensitive_stderr_and_cleans_prompt(self):
        with patch.dict(os.environ, {"STUB_FAIL": "1"}):
            with self.assertRaisesRegex(RuntimeError, "code 7") as error:
                hybrid_runner.run_hybrid_task("synthetic task", bridge_command=self.command)
        self.assertNotIn("synthetic-private-value", str(error.exception))
        self.assertFalse(Path(self.record.read_text(encoding="utf-8")).exists())

    def test_missing_file_stops_before_invoking_bridge(self):
        with self.assertRaises(FileNotFoundError):
            hybrid_runner.run_hybrid_task("task", [str(self.root / "missing.txt")],
                                          bridge_command=self.command)
        self.assertFalse(self.record.exists())

    def test_directory_context_stops_before_invoking_bridge(self):
        with self.assertRaisesRegex(ValueError, "regular file"):
            hybrid_runner.run_hybrid_task("task", [str(self.root)], bridge_command=self.command)
        self.assertFalse(self.record.exists())

    def test_unreadable_selected_file_stops_before_invoking_bridge(self):
        selected = self.root / "unreadable.txt"
        selected.write_text("synthetic", encoding="utf-8")
        with patch("pathlib.Path.open", side_effect=PermissionError("fixture denies reading")):
            with self.assertRaises(PermissionError):
                hybrid_runner.run_hybrid_task("task", [str(selected)], bridge_command=self.command)
        self.assertFalse(self.record.exists())

    def test_oversize_context_stops_before_invoking_bridge(self):
        with self.assertRaisesRegex(ValueError, "4 MiB"):
            hybrid_runner.run_hybrid_task("x" * (hybrid_runner.MAX_CONTEXT_BYTES + 1),
                                          bridge_command=self.command)
        self.assertFalse(self.record.exists())

    def test_timeout_cleans_prompt(self):
        seen = []

        def timeout(command, **kwargs):
            seen.append(Path(command[command.index("-P") + 1]))
            raise subprocess.TimeoutExpired(command, 1)

        with patch("scripts.hybrid_runner.subprocess.run", side_effect=timeout):
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                hybrid_runner.run_hybrid_task("task", bridge_command=self.command, timeout=1)
        self.assertEqual(len(seen), 1)
        self.assertFalse(seen[0].exists())

    def test_no_bridge_has_actionable_error_without_reading_context(self):
        with patch("scripts.hybrid_runner.shutil.which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "Install notion2api"):
                hybrid_runner.run_hybrid_task("task", [str(self.root / "missing.txt")])


class InstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="relay-install-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / "home with spaces"

    def test_complete_installation_has_runner_for_every_actual_target(self):
        files = install_skill.install(self.home, list(install_skill.TARGETS))
        self.assertEqual(len(files), 18)
        for path in files:
            self.assertTrue(path.is_file())
        for folder in install_skill.TARGETS.values():
            self.assertTrue((self.home / folder / "scripts/hybrid_runner.py").is_file())
        self.assertFalse((self.home / ".kimi").exists())

    def test_selected_target_is_idempotent_and_preserves_unrelated_files(self):
        install_skill.install(self.home, ["claude"])
        folder = self.home / install_skill.TARGETS["claude"]
        unrelated = folder / "operator-notes.txt"
        unrelated.write_text("preserve", encoding="utf-8")
        install_skill.install(self.home, ["claude"])
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "preserve")
        self.assertFalse((self.home / ".agents").exists())

    def test_dry_run_writes_nothing(self):
        paths = install_skill.install(self.home, ["agents"], dry_run=True)
        self.assertEqual(len(paths), 6)
        self.assertFalse(self.home.exists())

    def test_incomplete_source_fails_before_any_write(self):
        with patch.object(install_skill, "SOURCE", self.root / "missing-source"):
            with self.assertRaisesRegex(ValueError, "Incomplete checkout"):
                install_skill.install(self.home, ["agents"])
        self.assertFalse(self.home.exists())

    def test_symlinked_target_cannot_write_outside_selected_home(self):
        outside = self.root / "unrelated files"
        outside.mkdir()
        self.home.mkdir()
        try:
            (self.home / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Creating symlinks is unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "outside the selected home"):
            install_skill.install(self.home, ["agents"])
        self.assertEqual(list(outside.iterdir()), [])

    def test_installer_cli_does_not_require_or_run_bridge(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/install_skill.py"),
                                 "--home", str(self.home)], env=dict(os.environ, PATH=""),
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Bridge CLI not found", result.stdout)
        self.assertNotIn("all agents are ready", result.stdout)

    @unittest.skipUnless(os.name == "nt", "Windows wrapper is exercised on Windows CI")
    def test_powershell_wrapper_uses_requested_home(self):
        powershell = shutil.which("pwsh") or shutil.which("powershell")
        self.assertIsNotNone(powershell)
        result = subprocess.run([powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                                 str(ROOT / "install.ps1"), "-HomeDirectory", str(self.home),
                                 "-PythonExecutable", sys.executable],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / ".claude/skills/notion-ai/scripts/hybrid_runner.py").is_file())

    @unittest.skipIf(os.name == "nt", "Bash wrapper is exercised on Linux CI")
    def test_bash_wrapper_uses_requested_home(self):
        result = subprocess.run(["bash", str(ROOT / "install.sh"), "--home", str(self.home)],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / ".agents/skills/notion-ai/scripts/hybrid_runner.py").is_file())


if __name__ == "__main__":
    unittest.main()
