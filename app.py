"""진단검사 확률 실험실 Flask 애플리케이션."""

from pathlib import Path
import sys
import webbrowser
from threading import Timer

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
if VENDOR.exists():
    sys.path.insert(0, str(VENDOR))

from flask import Flask, jsonify, request, send_from_directory

from backend import DiagnosticApi

app = Flask(__name__)
api = DiagnosticApi()
HTML_FILE = "6. 진단검사 확률 실험실_최종수정본.html"


@app.get("/")
def index():
    return send_from_directory(HERE, HTML_FILE)


@app.get("/frontend.js")
def frontend_script():
    return send_from_directory(HERE, "frontend.js", mimetype="application/javascript")


@app.post("/api/bayes")
def calculate_bayes():
    data = request.get_json(force=True)
    return jsonify(api.bayes(float(data["prevalence"]), float(data["sensitivity"]), float(data["specificity"])))


@app.post("/api/retest")
def calculate_retest():
    data = request.get_json(force=True)
    try:
        values = [float(data[key]) for key in
                  ("prevalence", "sensitivity", "specificity", "sensitivity2", "specificity2")]
        return jsonify(api.retest(*values))
    except (KeyError, TypeError, ValueError, OverflowError):
        return jsonify(error="확률 입력값을 확인해 주세요."), 400


@app.post("/api/reconstruct")
def calculate_reconstruction():
    data = request.get_json(force=True)
    return jsonify(api.reconstruct(str(data["year"])))


@app.post("/api/roc")
def calculate_roc():
    data = request.get_json(force=True)
    return jsonify(api.roc(float(data["separation"]), float(data["cutoff"]), float(data["prevalence"]), float(data["fn_weight"])))


@app.post("/api/bias")
def calculate_bias():
    data = request.get_json(force=True)
    return jsonify(api.bias(float(data["lead"]), float(data["slow"]), float(data["nonprogressive"]), float(data["effect"])))


if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
