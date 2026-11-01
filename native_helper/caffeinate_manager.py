import subprocess
import sys


class CaffeinateManager:
    def __init__(self, binary='caffeinate', command='sleep 30'):
        self.binary = binary
        self.command = command
        self.pid = None
        self.process = None

    def start(self, command=None):
        cmd = command or self.command
        if not self._is_available():
            return {'ok': False, 'error': f'{self.binary} is not available on PATH'}

        try:
            self.process = subprocess.Popen(
                [self.binary, '-u', 'bash', '-lc', cmd],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            self.pid = self.process.pid
            return {'ok': True, 'pid': self.pid}
        except OSError as exc:
            return {'ok': False, 'error': str(exc)}

    def stop(self):
        if self.pid is None:
            return {'ok': True, 'pid': None}

        try:
            self.process.terminate()
            self.process.wait(timeout=5)
        except Exception:
            try:
                self.process.kill()
                self.process.wait(timeout=5)
            except Exception:
                pass
        finally:
            self.pid = None
            self.process = None
        return {'ok': True, 'pid': None}

    def _is_available(self):
        return subprocess.run(['bash', '-lc', f'command -v {self.binary}'], capture_output=True, text=True).returncode == 0
