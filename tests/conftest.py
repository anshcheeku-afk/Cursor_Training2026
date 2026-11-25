"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from monitor import create_app


@pytest.fixture()
def app(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "DATABASE": str(tmp_path / "test.db"),
            "SECRET_KEY": "test-secret",
            "SSH_USER": "testuser",
            "SSH_KEY_PATH": "/tmp/fake_key",
            "SSH_PASSWORD": "",
        }
    )
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_csrf(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": True,
            "DATABASE": str(tmp_path / "test_csrf.db"),
            "SECRET_KEY": "test-secret-csrf",
            "SSH_USER": "testuser",
            "SSH_KEY_PATH": "/tmp/fake_key",
        }
    )
    yield application


@pytest.fixture()
def client_csrf(app_csrf):
    return app_csrf.test_client()
