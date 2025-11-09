"""
app.py — Flask Web UI for Network Mapping & Vulnerability Scan
"""

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from network_scan.NmapRunner import NmapRunner
from network_scan.NmapParser import NmapParser
from network_scan.ReportGenerator import ReportGenerator
import os

app = Flask(__name__)
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        targets = request.form.get("targets")
        scan_type = request.form.get("scan_type")
        if not targets:
            return render_template("index.html", error="Please enter target IP or range.")

        runner = NmapRunner()
        parser = NmapParser()
        reporter = ReportGenerator()

        if scan_type == "discovery":
            xml = runner.discovery(targets)
        else:
            xml = runner.port_service_scan(targets, nse_safe=True)

        parsed = parser.parse(xml)
        base = os.path.join(REPORT_DIR, os.path.splitext(os.path.basename(xml))[0])
        reporter.save_json(parsed, base + ".json")
        reporter.generate_html(parsed, base + ".html")

        return redirect(url_for("reports"))
    return render_template("index.html")


@app.route("/reports")
def reports():
    files = [f for f in os.listdir(REPORT_DIR) if f.endswith(".html")]
    files.sort(reverse=True)
    return render_template("report_list.html", reports=files)


@app.route("/report/<path:filename>")
def report(filename):
    return send_from_directory(REPORT_DIR, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
