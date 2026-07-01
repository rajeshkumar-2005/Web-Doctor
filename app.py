from flask import Flask, request, jsonify, render_template, send_file
from scanner import run_scan
from db import init_db, save_scan, get_history
from report import generate_pdf

app = Flask(__name__)

# ---------- INIT DATABASE ----------
init_db()


# ---------- HOME ROUTE ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- SCAN ROUTE ----------
@app.route("/scan")
def scan():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = run_scan(url)

    # Save scan result
    save_scan(
        url,
        result["risk"]["score"],
        result["risk"]["risk"],
        result
    )

    return jsonify(result)


# ---------- HISTORY ROUTE ----------
@app.route("/history")
def history():
    rows = get_history()

    data = []
    for r in rows:
        data.append({
            "url": r[0],
            "score": r[1],
            "risk": r[2],
            "time": r[3]
        })

    return jsonify(data)


@app.route("/trend")
def trend():
    rows = get_history()

    data = []
    for r in rows:
        data.append({
            "score": r[1],   # Numeric score
            "time": r[3]     # Timestamp
        })

    return jsonify(data)


# ---------- REPORT ROUTE ----------
@app.route("/report")
def report():
    url = request.args.get("url")

    if not url:
        return "No URL provided", 400

    result = run_scan(url)
    file = generate_pdf(result)

    return send_file(file, as_attachment=True)


# ---------- PREDICTION ROUTE ----------
@app.route("/predict")
def predict():
    rows = get_history()

    if len(rows) < 2:
        return jsonify({
            "trend": "UNKNOWN",
            "prediction": "Not enough data"
        })

    # Get last few scores
    scores = [r[2] for r in rows[:5]]

    if scores[0] < scores[-1]:
        trend = "DOWN"
        prediction = "Security is degrading. Risk increasing."
    elif scores[0] > scores[-1]:
        trend = "UP"
        prediction = "Security improving."
    else:
        trend = "STABLE"
        prediction = "No major change."

    return jsonify({
        "trend": trend,
        "prediction": prediction,
        "latest_score": scores[0]
    })


# ---------- RUN SERVER ----------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
