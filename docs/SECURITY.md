# Security checklist (local demo)

This app is a **localhost-only demo** with **no application login or password**.

## Confirm before sharing the machine

- [x] Binds to `127.0.0.1` only (see `app.py`) — not `0.0.0.0`
- [x] No app username/password / no `/login`
- [x] CSRF tokens on add/delete server forms (Flask-WTF)
- [x] Hostname validation rejects shell metacharacters
- [x] Max 5 registered servers
- [x] SSH commands are fixed allowlists only (no user-controlled shell)
- [x] SSH failures return a safe “unreachable” message (no key paths / passwords in UI)
- [x] Secrets live in `.env` (see `.env.example`); never commit `.env`, keys, or `*.db`
- [x] `.gitignore` covers `venv/`, `.env`, `instance/`, `*.db`, SSH key filenames

## SSH credentials

Prefer `SSH_KEY_PATH` over `SSH_PASSWORD`. Keep key files mode `600`. Do not log credentials.

## CI

GitHub Actions runs lint + mocked tests only — no real SSH and no published secrets/DB artifacts.
