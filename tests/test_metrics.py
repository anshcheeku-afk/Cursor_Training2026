"""Phase 5 — parser and collector tests (mocked SSH)."""

from __future__ import annotations

from unittest.mock import patch

from monitor.metrics import (
    collect_host_metrics,
    parse_cpu,
    parse_memory,
    parse_network,
    parse_ports,
)
from monitor.ssh_client import SSHResult


SAMPLE_MEM = """
MemTotal:       8048232 kB
MemFree:        1000000 kB
MemAvailable:   4024116 kB
"""

SAMPLE_NET = """
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets
  eth0: 1048576  1 0 0 0 0 0 0 2097152 1 0 0 0 0 0 0
    lo: 100 1 0 0 0 0 0 0 100 1 0 0 0 0 0 0
"""

SAMPLE_SS = """
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process
LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=1,fd=3))
LISTEN 0      128          0.0.0.0:80         0.0.0.0:*    users:(("nginx",pid=2,fd=3))
"""


def test_parse_cpu():
    assert parse_cpu("cpu  100 0 0 100 0 0 0").endswith("%")


def test_parse_memory():
    out = parse_memory(SAMPLE_MEM)
    assert "GiB" in out or "MiB" in out
    assert "%" in out


def test_parse_network():
    rx, tx = parse_network(SAMPLE_NET)
    assert "MiB" in rx
    assert "MiB" in tx


def test_parse_ports():
    ports = parse_ports(SAMPLE_SS)
    assert {"port": "22", "process": "sshd"} in ports
    assert any(p["port"] == "80" for p in ports)


def test_collect_unreachable(app):
    with app.app_context():
        with patch(
            "monitor.metrics.run_command",
            return_value=SSHResult(ok=False, error="unreachable"),
        ):
            m = collect_host_metrics("missing.lab")
    assert m["status"] == "unreachable"
    assert m["error"]


def test_collect_ok(app):
    def fake_run(hostname, command):
        if "stat" in command:
            return SSHResult(ok=True, stdout="cpu  10 0 0 90 0 0 0\n")
        if "meminfo" in command:
            return SSHResult(ok=True, stdout=SAMPLE_MEM)
        if "net/dev" in command:
            return SSHResult(ok=True, stdout=SAMPLE_NET)
        return SSHResult(ok=True, stdout=SAMPLE_SS)

    with app.app_context():
        with patch("monitor.metrics.run_command", side_effect=fake_run):
            m = collect_host_metrics("web01.lab")
    assert m["status"] == "ok"
    assert m["cpu"].endswith("%")
    assert m["ports"]
