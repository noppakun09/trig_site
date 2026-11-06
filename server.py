"""Serves the setup page and receives Trig Protocol (1) from it.

Run:   pip install flask
       python server.py
Open:  http://localhost:5000
"""
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

AGE = ["Pediatric", "Adult", "Geriatric"]
DIFFICULTY = ["Easy", "Medium", "Hard"]
CASE_TYPE = ["Basic", "Emer/Trauma"]
MODE = ["Tutorial", "Guide", "Blind"]


def decode_trig1(data: int) -> dict:
    """Trig Protocol (1): 7-bit INT, layout 0b AA DD C MM."""
    if not 0 <= data < 128:
        raise ValueError("Trig1 must fit in 7 bits (0-127)")
    age = (data >> 5) & 0b11
    diff = (data >> 3) & 0b11
    case = (data >> 2) & 0b1
    mode = data & 0b11
    if age > 2 or diff > 2 or mode > 2:
        raise ValueError("0b11 is not a valid value for this field")
    return {
        "age": AGE[age],
        "difficulty": DIFFICULTY[diff],
        "case_type": CASE_TYPE[case],
        "mode": MODE[mode],
    }


@app.get("/")
def index():
    return send_file("index.html")


@app.post("/api/trig1")
def trig1():
    body = request.get_json(silent=True) or {}
    value = body.get("value")
    if not isinstance(value, int) or isinstance(value, bool):
        return jsonify(error="value must be an integer"), 400
    try:
        settings = decode_trig1(value)
    except ValueError as err:
        return jsonify(error=str(err)), 400

    print(f"Trig1 = 0b{value:07b} ({value}) -> {settings}")
    # TODO: pass `settings` on to the 3D simulation / user tracking here
    return jsonify(ok=True, settings=settings)


if __name__ == "__main__":
    app.run(debug=True)
