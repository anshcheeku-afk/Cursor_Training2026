"""Phase 3 — server inventory tests."""

from __future__ import annotations

from unittest.mock import patch


def test_add_valid_host(client):
    with patch("monitor.routes.collect_host_metrics") as mock_m:
        mock_m.return_value = {
            "hostname": "web01.lab",
            "status": "ok",
            "cpu": "1%",
            "memory": "1 / 2 (50%)",
            "network_in": "1 KiB",
            "network_out": "1 KiB",
            "ports": [],
            "error": None,
        }
        res = client.post("/servers", data={"hostname": "web01.lab"}, follow_redirects=True)
        assert res.status_code == 200
        assert b"web01.lab" in res.data


def test_reject_bad_hostname(client):
    res = client.post(
        "/servers",
        data={"hostname": "bad;rm -rf /"},
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert b"Invalid hostname" in res.data


def test_enforce_max_five(client, app):
    with patch("monitor.routes.collect_host_metrics") as mock_m:
        mock_m.side_effect = lambda h: {
            "hostname": h,
            "status": "ok",
            "cpu": "—",
            "memory": "—",
            "network_in": "—",
            "network_out": "—",
            "ports": [],
            "error": None,
        }
        for i in range(5):
            client.post("/servers", data={"hostname": f"host{i}.lab"})
        res = client.post(
            "/servers",
            data={"hostname": "host5.lab"},
            follow_redirects=True,
        )
        assert b"Maximum of 5" in res.data


def test_delete_server(client):
    with patch("monitor.routes.collect_host_metrics") as mock_m:
        mock_m.return_value = {
            "hostname": "db01.lab",
            "status": "ok",
            "cpu": "—",
            "memory": "—",
            "network_in": "—",
            "network_out": "—",
            "ports": [],
            "error": None,
        }
        client.post("/servers", data={"hostname": "db01.lab"})
        res = client.post("/servers/1/delete", follow_redirects=True)
        assert res.status_code == 200
        assert b"Server removed" in res.data


def test_csrf_required_when_enabled(client_csrf):
    res = client_csrf.post("/servers", data={"hostname": "web01.lab"})
    assert res.status_code == 400
