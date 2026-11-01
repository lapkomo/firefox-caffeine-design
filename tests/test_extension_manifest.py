import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'extension' / 'manifest.json'
BACKGROUND = ROOT / 'extension' / 'src' / 'background.js'


class ExtensionManifestTests(unittest.TestCase):
    def test_manifest_exists_and_uses_mv3(self):
        self.assertTrue(MANIFEST.exists(), 'manifest.json should exist')
        with MANIFEST.open('r', encoding='utf-8') as fh:
            manifest = json.load(fh)

        self.assertEqual(manifest.get('manifest_version'), 3)
        self.assertEqual(manifest.get('name'), 'Firefox Caffeine')
        self.assertIn('background', manifest)
        self.assertIn('scripts', manifest['background'])
        self.assertIn('src/background.js', manifest['background']['scripts'])

    def test_background_runtime_entry_exists(self):
        self.assertTrue(BACKGROUND.exists(), 'background.js should exist at extension/src/background.js')


if __name__ == '__main__':
    unittest.main()
