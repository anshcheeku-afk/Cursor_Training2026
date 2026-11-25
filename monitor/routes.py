"""HTTP routes — no login; CSRF on mutating forms."""

from __future__ import annotations

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from monitor.db import add_server, count_servers, delete_server, list_servers
from monitor.metrics import collect_host_metrics
from monitor.validators import validate_hostname

bp = Blueprint("main", __name__)


@bp.get("/")
def dashboard():
    servers = list_servers()
    metrics = []
    for row in servers:
        m = collect_host_metrics(row["hostname"])
        m["id"] = row["id"]
        metrics.append(m)
    return render_template(
        "dashboard.html",
        servers=metrics,
        server_count=len(servers),
    )


@bp.post("/servers")
def servers_add():
    raw = request.form.get("hostname", "")
    hostname = validate_hostname(raw)
    if not hostname:
        flash("Invalid hostname. Use a DNS name or IPv4 address.", "error")
        return redirect(url_for("main.dashboard"))

    max_servers = int(current_app.config["MAX_SERVERS"])
    if count_servers() >= max_servers:
        flash(f"Maximum of {max_servers} servers reached.", "error")
        return redirect(url_for("main.dashboard"))

    try:
        add_server(hostname)
        flash(f"Added {hostname}.", "ok")
    except Exception:
        flash("Could not add server (duplicate or database error).", "error")
    return redirect(url_for("main.dashboard"))


@bp.post("/servers/<int:server_id>/delete")
def servers_delete(server_id: int):
    if delete_server(server_id):
        flash("Server removed.", "ok")
    else:
        flash("Server not found.", "error")
    return redirect(url_for("main.dashboard"))
