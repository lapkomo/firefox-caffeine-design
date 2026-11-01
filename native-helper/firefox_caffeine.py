#!/usr/bin/env python3
"""Minimal native messaging host stub for the Firefox Caffeine project."""

import json
import os
import sys


def main() -> int:
    """Read a JSON message from stdin and acknowledge it."""
    raw = sys.stdin.buffer.read()
    if not raw:
        return 0

    try:
        message = json.loads(raw.decode('utf-8'))
    except json.JSONDecodeError:
        message = {'status': 'error', 'message': 'Invalid JSON payload'}

    response = {
        'status': 'ok',
        'message': 'Firefox Caffeine helper ready',
        'payload': message,
    }

    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
