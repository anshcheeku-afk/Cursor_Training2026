# PRD: Demo Linux Server Monitoring

## 1. Overview

Local demo web app to view real-time Linux server metrics (CPU, memory, network, listening ports) without SSH-ing into each host manually.

| Item | Value |
|------|--------|
| Audience | Internal L1 / L2 / L3 and app/infra teams |
| Mode | Demo only — run on the machine where Cursor is running |
| Stack | Python, Flask, attractive read-oriented UI |
| Access | **No app login / no password** — open on localhost |
| Scale | 1–5 Linux servers |

## 2. Problem

Today, teams log into each Linux server to check live CPU, memory, network, and port usage. This is slow and inconsistent for day-to-day checks.

## 3. Goals

- Show the four metrics above in a simple browser UI
- Allow registering Linux hosts by hostname
- Collect metrics over SSH from the Flask app (no per-host agent in this demo)
- Auto-refresh every **30 seconds**
- Keep setup and run steps minimal for local demo use

## 4. Non-goals

- App username/password login, SSO, or multi-user roles
- Alerts, paging, or threshold notifications
- Historical charts / long-term retention
- Windows / non-Linux hosts
- Docker packaging (optional later)
- Lightweight agents on monitored hosts

## 5. Users & access

Anyone with browser access to the local demo (`127.0.0.1`) can view metrics and manage the server inventory.

- **No sign-in screen**
- **No application password**
- Security relies on **localhost-only** binding (not exposed on the network)

## 6. Features

### 6.1 Add / manage Linux servers

- Add a server by **hostname** only (UI field)
- SSH connection details (user, port, key path or password) come from **local config / environment**, not the add-server form
- List and remove registered servers
- Target capacity: **1–5** hosts

### 6.2 Metrics dashboard (read-only)

For each registered server, show:

| Metric | Display |
|--------|---------|
| CPU | Usage % |
| Memory | Used / total and % |
| Network | In / out (e.g. bytes/s or KB/s) |
| Ports | Listening ports (port + process name if available) |

- UI auto-refreshes every **30 seconds**
- Friendly, clear layout; no edit controls on metric values
- If a host is unreachable over SSH, show a clear error/status for that host (do not crash the whole page)

### 6.3 Metric collection

- Flask app connects to each host over **SSH** and gathers the four metrics
- No agent install required on monitored servers for this demo
- Collection triggered on the 30s refresh cycle (and optionally on first page load)

## 7. Tech & data

| Area | Choice |
|------|--------|
| Backend / UI | Python + Flask (server-rendered and/or light JS for refresh) |
| Auth | None (no app login or password) |
| Inventory | **SQLite** local file |
| Secrets | SSH credentials via env or local config (not committed) |
| Run | Localhost only, e.g. `http://127.0.0.1:5000` |

## 8. Minimal local run (demo)

1. Install Python deps (e.g. `pip install -r requirements.txt`)
2. Set config/env: SSH user/key (or password), optional SSH port
3. Start app: `python app.py` (or equivalent Flask entrypoint)
4. Open `http://127.0.0.1:5000`, add hostnames, view dashboard (no login)

Monitored hosts must allow SSH from the Cursor/demo machine with the configured credentials.

## 9. Success criteria

- App opens with no login or password prompt
- Users can add/remove Linux servers by hostname
- Dashboard shows CPU, memory, network, and listening ports per host
- Values refresh about every 30 seconds
- App runs locally with a short setup; unreachable hosts fail gracefully per row/card

## 10. Out of scope for later (not this demo)

App login, multi-user RBAC, agents, alerting, history, Docker, cloud deploy.
