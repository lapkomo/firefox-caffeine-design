import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'native-helper' / 'firefox_caffeine.py'
BACKGROUND = ROOT / 'extension' / 'src' / 'background.js'


class NativeMessagingIntegrationTests(unittest.TestCase):
    def test_helper_returns_production_status_for_probe(self):
        completed = subprocess.run(
            ['python3', str(HELPER)],
            input='{"action": "probe"}',
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        response = json.loads(completed.stdout)
        self.assertEqual(response.get('status'), 'ok')
        self.assertIn('python_version', response.get('environment', {}))
        self.assertIn('caffeinate_available', response.get('environment', {}))
        self.assertEqual(response.get('payload', {}).get('action'), 'probe')

    def test_background_script_exposes_native_host_check(self):
        source = BACKGROUND.read_text(encoding='utf-8')

        self.assertIn('browserApi.runtime.sendNativeMessage', source)
        self.assertIn('checkHelperAvailability', source)
        self.assertIn('setup-check', source)


if __name__ == '__main__':
    unittest.main()
