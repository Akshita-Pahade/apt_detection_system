"""
SecureBank APT Detection Engine — Flask REST API Server (standalone launcher)
=============================================================================
Receives security event logs from client machines, runs live C++ analysis,
and exposes endpoints for the SOC dashboard.

Run:  python server.py
Port: 5000

Note: The same Flask API is embedded in app.py and starts automatically
when you run `streamlit run app.py`. Use this launcher only if you need
the API without the Streamlit dashboard.
"""

import os

os.environ["SECUREBANK_SERVER_ONLY"] = "1"

from app import flask_app, EVENT_SERVER_PORT  # noqa: E402

if __name__ == "__main__":
    print(f"SecureBank Event Server starting on http://0.0.0.0:{EVENT_SERVER_PORT}")
    flask_app.run(host="0.0.0.0", port=EVENT_SERVER_PORT, debug=False)
