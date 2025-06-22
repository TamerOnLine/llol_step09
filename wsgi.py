"""
WSGI entry point for deploying the Flask application.
"""

from run import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=40514, debug=True)
