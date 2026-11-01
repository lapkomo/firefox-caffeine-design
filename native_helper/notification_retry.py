class NotificationManager:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.handlers = {}

    def on_event(self, event_name, handler):
        self.handlers.setdefault(event_name, []).append(handler)

    def emit(self, event_name, message):
        for handler in self.handlers.get(event_name, []):
            handler(message)

    def retry(self, func, retries=None):
        attempts = retries if retries is not None else self.max_retries
        last_error = None

        for _ in range(attempts):
            try:
                return func()
            except Exception as exc:  # pragma: no cover - transient path
                last_error = exc

        raise last_error
