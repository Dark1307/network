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

## Project structure
