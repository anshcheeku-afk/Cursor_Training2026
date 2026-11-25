"""Phase 4 — mocked SSH tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from monitor.ssh_client import CMD_CPU, check_connection, run_command


def test_check_connection_success(app):
    mock_client = MagicMock()
    mock_transport = MagicMock()
    mock_transport.is_active.return_value = True
    mock_client.get_transport.return_value = mock_transport

    with app.app_context():
        with patch("monitor.ssh_client._connect", return_value=mock_client):
            result = check_connection("web01.lab")
    assert result.ok is True
    mock_client.close.assert_called()


def test_check_connection_auth_failure(app):
    with app.app_context():
        with patch(
            "monitor.ssh_client._connect",
            side_effect=Exception("auth failed with password secret123"),
        ):
            result = check_connection("web01.lab")
    assert result.ok is False
    assert result.error == "unreachable"
    assert "secret123" not in result.error
    assert "password" not in result.error.lower() or result.error == "unreachable"


def test_run_command_rejects_non_allowlisted(app):
    with app.app_context():
        result = run_command("web01.lab", "cat /etc/shadow")
    assert result.ok is False
    assert "allowlisted" in result.error.lower()


def test_run_command_success(app):
    mock_client = MagicMock()
    stdout = MagicMock()
    stdout.read.return_value = b"cpu  1 2 3 4 5 6 7"
    stdout.channel.recv_exit_status.return_value = 0
    stderr = MagicMock()
    stderr.read.return_value = b""
    mock_client.exec_command.return_value = (MagicMock(), stdout, stderr)

    with app.app_context():
        with patch("monitor.ssh_client._connect", return_value=mock_client):
            result = run_command("web01.lab", CMD_CPU)
    assert result.ok is True
    assert "cpu" in result.stdout
