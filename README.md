# Network Scan Project

**Network mapper & port scanner** — A project implemented in **Python** that wraps `nmap` to discover hosts, enumerate open ports/services, and produce JSON/HTML reports. A minimal **Flask** web UI allows local demo and report browsing.

> ⚠️ **Important:** This tool executes network scans. Only run it against networks and hosts you own or have explicit written permission to test.

---

## Features
- Host discovery (ping sweep)
- TCP SYN port & service detection (via `nmap`)
- Option to run safe NSE scripts
- Parse Nmap XML and export JSON + human-friendly HTML report
- Simple Flask web UI to launch scans and view reports
- Modular code: `NmapRunner`, `NmapParser`, `ReportGenerator`

---


## Requirements
- Python 3.8+
- `nmap` binary installed on the system (https://nmap.org)
- Recommended virtualenv usage

Install Python dependencies:
```bash
pip install -r requirements.txt




## CLI usage examples

python network_scanner_cli.py discover --targets "192.168.1.0/24"
python network_scanner_cli.py scan --targets "192.168.1.10-20" --nse false
python network_scanner_cli.py report --nmap-xml reports/fullscan_... .xml


## Development & Testing
pip install -r requirements.txt
pytest -q
