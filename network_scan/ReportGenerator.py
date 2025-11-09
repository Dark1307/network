"""
ReportGenerator.py
Generate JSON and HTML reports from parsed Nmap data.
"""
import json
import os
import datetime
from typing import List, Dict, Any


class ReportGenerator:
    def __init__(self, out_dir: str = "reports"):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def save_json(self, parsed: List[Dict[str, Any]], filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
        print(f"[+] JSON written to {filename}")

    def generate_html(self, parsed: List[Dict[str, Any]], filename: str):
        """
        Create an HTML report file from parsed data.
        `parsed` should be the list returned from NmapParser.parse(...)
        """
        title = f"Network Scan Report — {datetime.datetime.utcnow().isoformat()}Z"
        html_lines = [
            "<!doctype html>",
            "<html>",
            "<head>",
            f"<meta charset='utf-8'><title>{title}</title>",
            "<style>",
            "body{font-family:Arial,Helvetica,sans-serif;margin:20px;background:#f7f7f8}",
            "h1{color:#222}",
            ".host{background:#fff;padding:14px;margin-bottom:12px;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,0.06)}",
            ".meta{color:#666;font-size:13px;margin-bottom:8px}",
            "table{width:100%;border-collapse:collapse;margin-top:8px}",
            "th,td{border:1px solid #ddd;padding:8px;text-align:left}",
            "th{background:#f0f0f0}",
            ".noports{color:#555;font-style:italic}",
            "</style>",
            "</head><body>",
            f"<h1>{title}</h1>"
        ]

        if not parsed:
            html_lines.append("<p><strong>No hosts found or no results to display.</strong></p>")
        else:
            for h in parsed:
                host_label = h.get("ip", "unknown")
                hostnames = ", ".join(h.get("hostnames", [])) or "N/A"
                status = h.get("status", "unknown")
                html_lines.append(f"<div class='host'><h2>Host: {host_label}</h2>")
                html_lines.append(f"<div class='meta'>Status: {status} | Hostnames: {hostnames}</div>")

                ports = h.get("ports", [])
                if not ports:
                    html_lines.append("<div class='noports'>No open ports found.</div>")
                else:
                    html_lines.append("<table><thead><tr><th>Port</th><th>Proto</th><th>State</th><th>Service</th><th>Product</th><th>Version</th></tr></thead><tbody>")
                    for p in ports:
                        html_lines.append(
                            "<tr>"
                            f"<td>{p.get('portid','')}</td>"
                            f"<td>{p.get('protocol','')}</td>"
                            f"<td>{p.get('state','')}</td>"
                            f"<td>{p.get('service','')}</td>"
                            f"<td>{p.get('product','')}</td>"
                            f"<td>{p.get('version','')}</td>"
                            "</tr>"
                        )
                    html_lines.append("</tbody></table>")

                html_lines.append("</div>")  # host

        html_lines.extend(["</body></html>"])

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(html_lines))

        print(f"[+] HTML written to {filename}")
        return filename
