#!/usr/bin/env python3
"""Native messaging host for Firefox Caffeine."""

import json
import platform
import shutil
import sys


def build_environment() -> dict:
    return {
        'python_version': platform.python_version(),
        'caffeinate_available': shutil.which('caffeinate') is not None,
    }


def main() -> int:
    """Read a JSON message from stdin and respond with status information."""
    raw = sys.stdin.buffer.read()
    if not raw:
        return 0

    try:
        message = json.loads(raw.decode('utf-8'))
    except json.JSONDecodeError:
        message = {'status': 'error', 'message': 'Invalid JSON payload'}

    action = message.get('action', 'probe')
    env = build_environment()
    status = 'ok'
    if not env['caffeinate_available']:
        status = 'error'

    response = {
        'status': status,
        'message': 'Firefox Caffeine helper ready',
        'environment': env,
        'payload': {
            'action': action,
            'received': message,
        },
    }

    if status == 'error':
        response['message'] = 'caffeinate is not installed or not available on PATH'

    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
