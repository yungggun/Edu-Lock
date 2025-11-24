from flask import Flask, request, abort
import hmac
import hashlib

app = Flask(__name__)

# Shared secret (wie im C-Code)
SECRET = b"my_shared_secret_123"

# Für Demo: Liste von möglichen Nachrichten (der Server kennt sie)
MESSAGES = [
    "Hello from client!",
    "Test message 1",
    "Another message",
]

def verify_hmac(message: str, token_hex: str) -> bool:
    """HMAC-SHA256 prüfen"""
    h = hmac.new(SECRET, message.encode(), hashlib.sha256)
    return h.hexdigest() == token_hex.lower()

@app.route("/")
def index():
    token = request.args.get("token")
    if not token:
        return "Bitte ?token=<hex> angeben"

    # Suche durch alle bekannten Messages
    for msg in MESSAGES:
        if verify_hmac(msg, token):
            return f"Entschlüsselte Nachricht: {msg}"

    return "Ungültiger Token oder Nachricht nicht gefunden"

if __name__ == "__main__":
    app.run(debug=True)
