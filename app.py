"""Demo Linux Server Monitoring — local entrypoint."""

from monitor import create_app

app = create_app()

if __name__ == "__main__":
    # Local demo only — never bind 0.0.0.0 for this app.
    # Debug may be enabled locally; do not put secrets in code or templates.
    app.run(host="127.0.0.1", port=5000, debug=True)
