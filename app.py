"""Demo Linux Server Monitoring — local Flask app (Phase 0)."""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def dashboard():
    """Placeholder read-only dashboard (no live metrics yet)."""
    placeholders = [
        {
            "hostname": "demo-host-01.local",
            "status": "placeholder",
            "cpu": "—",
            "memory": "— / — (—%)",
            "network_in": "—",
            "network_out": "—",
            "ports": [
                {"port": "22", "process": "sshd"},
                {"port": "80", "process": "nginx"},
            ],
        },
        {
            "hostname": "demo-host-02.local",
            "status": "placeholder",
            "cpu": "—",
            "memory": "— / — (—%)",
            "network_in": "—",
            "network_out": "—",
            "ports": [
                {"port": "22", "process": "sshd"},
                {"port": "5432", "process": "postgres"},
            ],
        },
    ]
    return render_template("dashboard.html", servers=placeholders)


if __name__ == "__main__":
    # Local demo only — never bind 0.0.0.0 for this app.
    # Debug may be enabled locally; do not put secrets in code or templates.
    app.run(host="127.0.0.1", port=5000, debug=True)
