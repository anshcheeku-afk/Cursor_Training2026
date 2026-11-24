# TODO: Demo Linux Server Monitoring

Small, AI-friendly increments. Each step should leave the app runnable (or tests green) and include **security** + **docs** notes. Demo runs locally only (`http://127.0.0.1:5000`). See [requirements.md](./requirements.md).

**Access:** no app login or password — open on `127.0.0.1` only.

---

## Phase 0 — Project init + basic UI

- [x] **0.1** Create project skeleton
  - Layout: `app.py` (or `app/` package), `templates/`, `static/`, `tests/`, `docs/`, `.gitignore`, `requirements.txt`
  - Pin Flask (+ later deps as needed); Python 3.11+
  - **Security:** `.gitignore` excludes `.env`, `*.db`, `venv/`, `__pycache__/`, secrets, SSH keys
  - **Docs:** one-line `README.md` — what the demo is + “local only”

- [x] **0.2** Minimal Flask hello + attractive shell UI
  - Route `/` renders a styled base layout (CSS variables, clean header “Server Monitor”, empty content area)
  - Bind to `127.0.0.1` only (not `0.0.0.0`)
  - **Security:** no debug exposure of secrets; document that demo uses Flask debug only locally if enabled
  - **Docs:** `README.md` — how to `pip install -r requirements.txt` and `python app.py`

- [x] **0.3** Placeholder dashboard page (no real data)
  - Read-only cards/sections labeled CPU, Memory, Network, Ports (static placeholders)
  - **Security:** no forms that accept untrusted input yet
  - **Docs:** screenshot or short “UI map” note in `README.md`

---

## Phase 1 — Baseline unit tests (no app login)

- [ ] **1.1** Add pytest + Flask test client
  - Depend on `pytest` in `requirements.txt` (or `requirements-dev.txt`)
  - Shared fixture that creates the app test client
  - **Security:** confirm app has **no** login/password routes; tests must not introduce credential handling
  - **Docs:** `README.md` — note “no login”; `pytest` one-liner

- [ ] **1.2** Smoke tests for dashboard
  - `GET /` returns 200; page contains “Server Monitor” and metric labels (CPU, Memory, Network, Ports)
  - No redirect to a login page
  - **Security:** assert response does not expose secrets/env values
  - **Docs:** keep test command in `README.md`

---

## Phase 2 — CI/CD (GitHub Actions)

- [ ] **2.1** GitHub Actions workflow
  - `.github/workflows/ci.yml`: on push/PR — install deps, run `pytest`, optional lint (`ruff` or `flake8`)
  - **Security:** no secrets in workflow logs; use env placeholders only in CI; do not publish artifacts containing `.env` or DB
  - **Docs:** note in `README.md` that CI runs tests on GitHub; local demo does not need Actions to run

- [ ] **2.2** Keep CI green as baseline
  - Ensure Phase 0–1 tests pass in CI before adding features
  - **Security:** pin action versions (`actions/checkout@v4`, etc.)
  - **Docs:** badge optional; brief “CI checks” bullet in `README.md`

---

## Phase 3 — SQLite server inventory

- [ ] **3.1** SQLite model for servers
  - Table: `id`, `hostname`, `created_at`; max **5** hosts enforced in app logic
  - DB path outside git (e.g. `instance/monitor.db`)
  - **Security:** parameterized queries / ORM; validate hostname format (no shell metacharacters)
  - **Docs:** where DB lives; how to reset DB for demo

- [ ] **3.2** Add / list / remove servers
  - UI form: hostname only; list registered hosts; delete action (no login gate)
  - **Security:** CSRF on add/delete; reject invalid hostnames; cap at 5; localhost-only remains the access control
  - **Docs:** update `README.md` — add hostname from the open UI

- [ ] **3.3** Unit tests for inventory
  - Add valid host; reject bad hostname; enforce max 5; delete
  - **Security:** cover CSRF failure paths where practical
  - **Docs:** mention new tests in CI still cover inventory

---

## Phase 4 — SSH config (no metrics yet)

- [ ] **4.1** Shared SSH settings from env
  - `SSH_USER`, `SSH_PORT` (default 22), `SSH_KEY_PATH` and/or `SSH_PASSWORD` (prefer key)
  - Connection helper stub that opens/closes SSH (Paramiko or similar) without collecting metrics
  - **Security:** never log passwords/keys; key file permissions note; prefer key over password; secrets only in `.env`
  - **Docs:** `.env.example` SSH vars; “hosts must allow SSH from this machine”

- [ ] **4.2** Unit tests with mocked SSH
  - Mock transport: success + auth failure; ensure secrets not present in logs/assertions
  - **Security:** no real network SSH in CI
  - **Docs:** note that CI uses mocks only

---

## Phase 5 — Metrics collection (SSH)

Implement one metric family per step (keeps diffs small).

- [ ] **5.1** CPU % via SSH
  - Remote command(s) → parse CPU %; attach to server on dashboard
  - **Security:** fixed allowlisted commands only (no user-controlled shell strings); timeout SSH
  - **Docs:** which remote command is used for CPU

- [ ] **5.2** Memory used/total/% via SSH
  - Same pattern as CPU
  - **Security:** allowlisted commands; sanitize/parse numeric output only
  - **Docs:** document memory source command

- [ ] **5.3** Network in/out via SSH
  - Bytes/s or KB/s display
  - **Security:** allowlisted commands; timeouts
  - **Docs:** document network source command

- [ ] **5.4** Listening ports (+ process name if available) via SSH
  - Read-only list in UI
  - **Security:** allowlisted commands; truncate huge output; no arbitrary port scans from user input
  - **Docs:** document ports command (`ss`/`lsof` as chosen)

- [ ] **5.5** Per-host error handling
  - Unreachable/auth failure → status message on that host card; other hosts still render
  - **Security:** do not leak SSH exception internals (paths, usernames) to UI beyond safe message
  - **Docs:** what “unreachable” looks like

- [ ] **5.6** Unit tests for parsers + collector (mocked SSH)
  - Parse sample command output for each metric; unreachable path returns error object
  - **Security:** no real SSH in tests
  - **Docs:** keep `pytest` instructions current

---

## Phase 6 — Dashboard polish + 30s refresh

- [ ] **6.1** Wire live metrics into read-only UI
  - Attractive per-host cards; no edit of metric values
  - **Security:** no open CORS; bind remains `127.0.0.1`
  - **Docs:** short UI walkthrough in `README.md`

- [ ] **6.2** Auto-refresh every 30 seconds
  - Meta-refresh or light JS fetch
  - **Security:** no credentials in query strings; CSRF on mutating routes only
  - **Docs:** note 30s interval matches PRD

---

## Phase 7 — Hardening + final demo docs

- [ ] **7.1** Security pass
  - Confirm: bind `127.0.0.1`, **no app password/login**, CSRF on mutations, `.gitignore`, no secrets in git, allowlisted SSH commands, hostname validation
  - **Docs:** add `docs/SECURITY.md` (short checklist for the demo)

- [ ] **7.2** Final README polish
  - Minimal steps: install → copy `.env.example` → set SSH → run → add hostname (no login)
  - Link PRD + this TODO
  - **Security:** remind not to commit `.env` / keys / DB; demo has no app auth

- [ ] **7.3** CI confirmation
  - All tests + lint pass on GitHub Actions
  - **Docs:** “green CI” called out in README

---

## Suggested default order (summary)

1. Phase 0 — init + basic UI  
2. Phase 1 — baseline unit tests (no login)  
3. Phase 2 — GitHub Actions CI  
4. Phase 3 — SQLite inventory  
5. Phase 4 — SSH config  
6. Phase 5 — metrics (CPU → memory → network → ports)  
7. Phase 6 — dashboard + 30s refresh  
8. Phase 7 — hardening + docs  

Work **one checkbox at a time**; keep PRs/commits small and tests green before moving on.
