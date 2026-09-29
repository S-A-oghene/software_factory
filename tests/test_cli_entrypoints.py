import os
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CLIEntrypointTests(unittest.TestCase):
    def run_cmd(self, *args):
        env = dict(os.environ)
        env['PYTHONPATH'] = str(ROOT)
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_package_entrypoint(self):
        r = self.run_cmd('-m', 'factory', 'self-test')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('SELF_TEST_PASS', r.stdout)

    def test_cli_module_entrypoint(self):
        r = self.run_cmd('-m', 'factory.cli', 'self-test')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('SELF_TEST_PASS', r.stdout)


if __name__ == '__main__':
    unittest.main()
