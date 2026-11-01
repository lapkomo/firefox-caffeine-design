import unittest

from native_helper.notification_retry import NotificationManager


class NotificationManagerTests(unittest.TestCase):
    def test_notifier_emits_start_and_finish_messages(self):
        manager = NotificationManager()
        events = []

        manager.on_event('download_started', lambda message: events.append(('start', message)))
        manager.on_event('download_finished', lambda message: events.append(('finish', message)))

        manager.emit('download_started', 'ダウンロード開始')
        manager.emit('download_finished', 'ダウンロード完了')

        self.assertEqual(events[0], ('start', 'ダウンロード開始'))
        self.assertEqual(events[1], ('finish', 'ダウンロード完了'))

    def test_retry_manager_retries_failed_action_up_to_limit(self):
        manager = NotificationManager(max_retries=2)
        attempts = {'count': 0}

        def flaky():
            attempts['count'] += 1
            if attempts['count'] < 2:
                raise RuntimeError('transient failure')
            return 'ok'

        result = manager.retry(flaky)
        self.assertEqual(result, 'ok')
        self.assertEqual(attempts['count'], 2)


if __name__ == '__main__':
    unittest.main()
