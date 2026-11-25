"""Parse remote command output and collect per-host metrics."""

from __future__ import annotations

from typing import Any

from monitor.ssh_client import (
    CMD_CPU,
    CMD_MEM,
    CMD_NET,
    CMD_PORTS,
    run_command,
)


def parse_cpu(stat_line: str) -> str:
    """Parse first /proc/stat cpu line into approximate busy %."""
    parts = stat_line.strip().split()
    if len(parts) < 5 or parts[0] != "cpu":
        return "—"
    try:
        vals = [int(x) for x in parts[1:8]]
    except ValueError:
        return "—"
    total = sum(vals)
    if total <= 0:
        return "—"
    idle = vals[3] + (vals[4] if len(vals) > 4 else 0)
    busy = max(0.0, (total - idle) / total * 100.0)
    return f"{busy:.1f}%"


def parse_memory(meminfo: str) -> str:
    data: dict[str, int] = {}
    for line in meminfo.splitlines():
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        num = rest.strip().split()[0]
        try:
            data[key] = int(num)
        except ValueError:
            continue
    total = data.get("MemTotal")
    avail = data.get("MemAvailable")
    if not total:
        return "— / — (—%)"
    used = total - avail if avail is not None else data.get("MemFree", 0)
    if avail is not None:
        used = total - avail
    pct = used / total * 100.0
    return f"{_kb_to_human(used)} / {_kb_to_human(total)} ({pct:.0f}%)"


def parse_network(netdev: str) -> tuple[str, str]:
    rx = tx = 0
    for line in netdev.splitlines():
        if ":" not in line:
            continue
        name, rest = line.split(":", 1)
        iface = name.strip()
        if iface == "lo":
            continue
        cols = rest.split()
        if len(cols) < 9:
            continue
        try:
            rx += int(cols[0])
            tx += int(cols[8])
        except ValueError:
            continue
    return _bytes_human(rx), _bytes_human(tx)


def parse_ports(ss_out: str, limit: int = 20) -> list[dict[str, str]]:
    ports: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in ss_out.splitlines():
        if not line.strip() or line.startswith("State") or line.startswith("Netid"):
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[3]
        port = local.rsplit(":", 1)[-1]
        if not port.isdigit() or port in seen:
            continue
        seen.add(port)
        process = "—"
        if "users:(" in line:
            # users:(("sshd",pid=...,fd=...))
            try:
                inner = line.split("users:((", 1)[1]
                process = inner.split('"', 2)[1]
            except (IndexError, ValueError):
                process = "—"
        ports.append({"port": port, "process": process[:40]})
        if len(ports) >= limit:
            break
    return ports


def _kb_to_human(kb: int) -> str:
    mb = kb / 1024.0
    if mb >= 1024:
        return f"{mb / 1024.0:.1f} GiB"
    return f"{mb:.0f} MiB"


def _bytes_human(n: int) -> str:
    if n >= 1024**3:
        return f"{n / 1024**3:.1f} GiB"
    if n >= 1024**2:
        return f"{n / 1024**2:.1f} MiB"
    if n >= 1024:
        return f"{n / 1024:.0f} KiB"
    return f"{n} B"


def collect_host_metrics(hostname: str) -> dict[str, Any]:
    """Collect CPU, memory, network, ports for one host over SSH."""
    result: dict[str, Any] = {
        "hostname": hostname,
        "status": "ok",
        "cpu": "—",
        "memory": "— / — (—%)",
        "network_in": "—",
        "network_out": "—",
        "ports": [],
        "error": None,
    }

    cpu_res = run_command(hostname, CMD_CPU)
    if not cpu_res.ok:
        result["status"] = "unreachable"
        result["error"] = "Host unreachable or SSH failed"
        return result

    result["cpu"] = parse_cpu(cpu_res.stdout.splitlines()[0] if cpu_res.stdout else "")

    mem_res = run_command(hostname, CMD_MEM)
    if mem_res.ok:
        result["memory"] = parse_memory(mem_res.stdout)

    net_res = run_command(hostname, CMD_NET)
    if net_res.ok:
        nin, nout = parse_network(net_res.stdout)
        result["network_in"] = nin
        result["network_out"] = nout

    ports_res = run_command(hostname, CMD_PORTS)
    if ports_res.ok:
        result["ports"] = parse_ports(ports_res.stdout)

    return result
