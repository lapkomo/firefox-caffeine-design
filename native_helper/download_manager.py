class DownloadTracker:
    def __init__(self):
        self.active_downloads_by_id = {}

    @property
    def active_downloads(self):
        return len(self.active_downloads_by_id)

    def on_download_started(self, download_id):
        self.active_downloads_by_id[download_id] = True

    def on_download_finished(self, download_id):
        self.active_downloads_by_id.pop(download_id, None)

    def on_download_failed(self, download_id):
        self.on_download_finished(download_id)

    def should_stop_sleep(self):
        return self.active_downloads == 0
