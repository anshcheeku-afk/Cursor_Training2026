# Server Monitor (local demo)

Flask demo for Linux server metrics (CPU, memory, network, listening ports) over SSH.

- **Local only** — `http://127.0.0.1:5000`
- **No login or password** — open the URL and use the UI
- Inventory in SQLite (`instance/monitor.db`); max **5** hosts

See [docs/requirements.md](docs/requirements.md), [docs/TODO.md](docs/TODO.md), [docs/SECURITY.md](docs/SECURITY.md).

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set SECRET_KEY, SSH_USER, SSH_KEY_PATH (or SSH_PASSWORD)
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Add a hostname; metrics refresh every **30 seconds**.

Monitored hosts must allow SSH from this machine with the configured credentials.

## Tests

```bash
pytest -q
```

CI (GitHub Actions) runs `ruff` + `pytest` on push/PR. You do **not** need Actions to run the local demo.

## UI map

| Area | Purpose |
|------|---------|
| Header | Brand + auto-refresh note |
| Manage | Add hostname (CSRF-protected); count `n / 5` |
| Cards | Per-host CPU, memory, network totals, ports; Remove button |
| Unreachable | Red status if SSH fails — other hosts still render |

## Metric sources (allowlisted SSH commands)

| Metric | Remote source |
|--------|----------------|
| CPU | `grep '^cpu ' /proc/stat` |
| Memory | `cat /proc/meminfo` |
| Network | `cat /proc/net/dev` (RX/TX byte totals, excludes `lo`) |
| Ports | `ss -tlnp` (fallback `ss -tln`) |

## Reset demo DB

```bash
rm -f instance/monitor.db
```

Flask `debug=True` is for local demo only. Never commit `.env`, SSH keys, or the database.
