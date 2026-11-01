import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / 'native_helper' / 'caffeinate_manager.py'


class CaffeinateManagerTests(unittest.TestCase):
    def test_caffeinate_manager_tracks_pid_and_stops_process(self):
        if not FILE.exists():
            self.fail('caffeinate_manager.py should exist')

        import importlib.util

        spec = importlib.util.spec_from_file_location('caffeinate_manager', FILE)
        mod = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(mod)

        manager = mod.CaffeinateManager()
        manager.start('sleep 30')
        self.assertIsNotNone(manager.pid)
        self.assertGreater(manager.pid, 0)

        manager.stop()
        self.assertIsNone(manager.pid)

    def test_caffeinate_manager_reports_missing_command(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location('caffeinate_manager', FILE)
        mod = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(mod)

        manager = mod.CaffeinateManager(binary='missing-caffeinate-command')
        result = manager.start('echo test')

        self.assertFalse(result['ok'])
        self.assertIn('error', result)


if __name__ == '__main__':
    unittest.main()
