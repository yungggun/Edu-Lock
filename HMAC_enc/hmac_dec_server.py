from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

SECRET = b"my_shared_secret_123"


def calc_hmac(message: str) -> str:
    h = hmac.new(SECRET, message.encode("utf-8"), hashlib.sha256)
    return h.hexdigest()


@app.route("/", methods=["GET"])
def index():
    token = request.args.get("token")
    token_hash = request.args.get("hash")

    if not token or not token_hash:
        return "Bitte ?token=<text>&hash=<hex> angeben\n", 400

    expected = calc_hmac(token)

    print("Empfangenes Token:", token)
    print("Erwarteter HMAC :", expected)
    print("Gesendeter Hash  :", token_hash)
    if hmac.compare_digest(expected.lower(), token_hash.lower()):
        print("Verifikation: OK\n")
        return "HMAC OK\n", 200
    else:
        print("Verifikation: FEHLER\n")
        return "HMAC FEHLER\n", 401


if __name__ == "__main__":
    app.run(host="192.168.137.1", port=5000, debug=True)
