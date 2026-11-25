"""SSH connection helper — secrets never logged."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import paramiko
from flask import current_app

logger = logging.getLogger(__name__)

# Fixed allowlisted remote commands only (no user-controlled shell strings).
CMD_CPU = "grep '^cpu ' /proc/stat"
CMD_MEM = "cat /proc/meminfo"
CMD_NET = "cat /proc/net/dev"
CMD_PORTS = "ss -tlnp 2>/dev/null || ss -tln"


@dataclass
class SSHResult:
    ok: bool
    stdout: str = ""
    error: str = ""


def _connect(hostname: str) -> paramiko.SSHClient:
    cfg = current_app.config
    user = cfg.get("SSH_USER") or ""
    if not user:
        raise RuntimeError("SSH_USER is not configured")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    kwargs: dict[str, Any] = {
        "hostname": hostname,
        "port": int(cfg.get("SSH_PORT") or 22),
        "username": user,
        "timeout": int(cfg.get("SSH_TIMEOUT") or 8),
        "allow_agent": False,
        "look_for_keys": False,
    }
    key_path = (cfg.get("SSH_KEY_PATH") or "").strip()
    password = cfg.get("SSH_PASSWORD") or ""
    if key_path:
        kwargs["key_filename"] = key_path
    elif password:
        kwargs["password"] = password
    else:
        raise RuntimeError("Configure SSH_KEY_PATH or SSH_PASSWORD")

    client.connect(**kwargs)
    return client


def run_command(hostname: str, command: str) -> SSHResult:
    """Run an allowlisted command on hostname over SSH."""
    allowed = {CMD_CPU, CMD_MEM, CMD_NET, CMD_PORTS}
    if command not in allowed:
        return SSHResult(ok=False, error="Command not allowlisted")

    client = None
    try:
        client = _connect(hostname)
        _stdin, stdout, stderr = client.exec_command(
            command,
            timeout=int(current_app.config.get("SSH_TIMEOUT") or 8),
        )
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0 and not out.strip():
            return SSHResult(ok=False, error="Remote command failed")
        return SSHResult(ok=True, stdout=out, error=err.strip())
    except Exception:
        # Do not leak paths, usernames, or exception details to callers/logs with secrets
        logger.info("SSH connection or command failed for host %s", hostname)
        return SSHResult(ok=False, error="unreachable")
    finally:
        if client is not None:
            client.close()


def check_connection(hostname: str) -> SSHResult:
    """Open and close an SSH session (connectivity stub)."""
    client = None
    try:
        client = _connect(hostname)
        transport = client.get_transport()
        if transport is None or not transport.is_active():
            return SSHResult(ok=False, error="unreachable")
        return SSHResult(ok=True, stdout="ok")
    except Exception:
        logger.info("SSH check failed for host %s", hostname)
        return SSHResult(ok=False, error="unreachable")
    finally:
        if client is not None:
            client.close()
