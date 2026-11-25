"""Application configuration from environment."""

from __future__ import annotations

import os


class Config:
    """Default config for the local demo."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-only-change-me"
    WTF_CSRF_ENABLED = True
    MAX_SERVERS = 5
    SSH_USER = os.environ.get("SSH_USER", "")
    SSH_PORT = int(os.environ.get("SSH_PORT") or "22")
    SSH_KEY_PATH = os.environ.get("SSH_KEY_PATH", "")
    SSH_PASSWORD = os.environ.get("SSH_PASSWORD", "")
    SSH_TIMEOUT = 8
    # Bound only via app.run in app.py — documented as 127.0.0.1
