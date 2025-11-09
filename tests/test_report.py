from network_scan.ReportGenerator import ReportGenerator

def test_generate_reports(tmp_path):
    data = [{"address": "192.168.1.1", "hostname": "router", "ports": [{"port": "80", "protocol": "tcp", "state": "open", "service": "http"}]}]
    rg = ReportGenerator()
    json_path = tmp_path / "out.json"
    html_path = tmp_path / "out.html"
    rg.save_json(data, json_path)
    rg.generate_html(data, html_path)
    assert json_path.exists()
    assert html_path.exists()
