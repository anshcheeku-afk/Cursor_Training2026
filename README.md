# Server Monitor (local demo)

Demo Flask app for viewing Linux server metrics (CPU, memory, network, ports). **Local only** — binds to `127.0.0.1`. **No login or password** — open the URL and use the UI.

## Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Flask `debug=True` is for local demo only. Do not put secrets in code or templates.

## UI map (Phase 0)

| Area | What you see |
|------|----------------|
| Header | Brand **Server Monitor** + “Read-only view” |
| Hero | “Infrastructure overview” intro |
| Cards | Two placeholder hosts with CPU, Memory, Network, Ports sections (static `—` values) |
| Footer | Reminder that the app is localhost-only |

Auth, live SSH metrics, and server CRUD come in later TODO phases. See [docs/requirements.md](docs/requirements.md) and [docs/TODO.md](docs/TODO.md).
