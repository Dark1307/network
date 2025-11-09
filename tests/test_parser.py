from network_scan.NmapParser import NmapParser

def test_parse_sample_xml(tmp_path):
    sample = """<nmaprun><host><address addr="192.168.1.1"/><ports>
    <port protocol="tcp" portid="80"><state state="open"/><service name="http"/></port>
    </ports></host></nmaprun>"""
    xml_path = tmp_path / "test.xml"
    xml_path.write_text(sample)

    parser = NmapParser()
    result = parser.parse(str(xml_path))
    assert result[0]['address'] == "192.168.1.1"
    assert result[0]['ports'][0]['service'] == "http"
