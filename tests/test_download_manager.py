import unittest

from native_helper.download_manager import DownloadTracker


class DownloadTrackerTests(unittest.TestCase):
    def test_track_start_and_completion_updates_active_count(self):
        tracker = DownloadTracker()
        tracker.on_download_started('a')
        tracker.on_download_started('b')
        self.assertEqual(tracker.active_downloads, 2)
        self.assertIn('a', tracker.active_downloads_by_id)
        self.assertIn('b', tracker.active_downloads_by_id)

        tracker.on_download_finished('a')
        self.assertEqual(tracker.active_downloads, 1)

        tracker.on_download_finished('b')
        self.assertEqual(tracker.active_downloads, 0)
        self.assertTrue(tracker.should_stop_sleep())

    def test_failed_downloads_are_removed_without_leaving_stale_state(self):
        tracker = DownloadTracker()
        tracker.on_download_started('x')
        tracker.on_download_failed('x')

        self.assertEqual(tracker.active_downloads, 0)
        self.assertNotIn('x', tracker.active_downloads_by_id)
        self.assertTrue(tracker.should_stop_sleep())


if __name__ == '__main__':
    unittest.main()
