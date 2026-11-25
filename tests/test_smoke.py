"""Phase 1 — dashboard smoke tests (no login)."""

from __future__ import annotations


def test_dashboard_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "Server Monitor" in html
    assert "CPU" in html
    assert "Memory" in html
    assert "Network" in html
    assert "Ports" in html


def test_no_login_redirect(client):
    res = client.get("/", follow_redirects=False)
    assert res.status_code == 200
    assert "/login" not in (res.headers.get("Location") or "")


def test_no_login_routes(app):
    rules = {rule.rule for rule in app.url_map.iter_rules()}
    assert "/login" not in rules
    assert "/logout" not in rules


def test_response_does_not_leak_secrets(client, app):
    res = client.get("/")
    html = res.get_data(as_text=True)
    assert app.config["SECRET_KEY"] not in html
    assert "SSH_PASSWORD" not in html
    key = app.config.get("SSH_KEY_PATH") or ""
    if key:
        assert key not in html
