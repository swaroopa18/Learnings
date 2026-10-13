
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/triage-ticket", methods=["POST"])
def triage_ticket():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        data = {}

    ticket_text = data.get("ticket_text")

    if not isinstance(ticket_text, str) or not ticket_text.strip():
        return jsonify({
            "detail": "ticket_text is required"
        }), 400

    # Fixed placeholder response for mock testing only.
    return jsonify({
        "category": "damaged_item",
        "summary": (
            "Customer reports a damaged package and needs "
            "help with a replacement."
        )
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
