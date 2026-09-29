import os
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CLIInvocationTests(unittest.TestCase):
    def _run(self, module: str):
        env = dict(os.environ)
        env['PYTHONPATH'] = str(ROOT)
        return subprocess.run(
            [sys.executable, '-m', module, 'self-test'],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_package_entrypoint(self):
        result = self._run('factory')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SELF_TEST_PASS', result.stdout)

    def test_cli_module_entrypoint(self):
        result = self._run('factory.cli')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SELF_TEST_PASS', result.stdout)


if __name__ == '__main__':
    unittest.main()
