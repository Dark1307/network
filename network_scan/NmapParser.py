"""
NmapParser.py
Robust parser for Nmap XML output. Returns a list of hosts with ports and service info.
"""

import xml.etree.ElementTree as ET
import os
from typing import List, Dict, Any


class NmapParser:
    def __init__(self):
        pass

    def parse(self, xml_path: str) -> List[Dict[str, Any]]:
        """
        Parse nmap XML file and return list of host dicts:
        [
          {
            "ip": "192.168.1.1",
            "addrtype": "ipv4",
            "status": "up",
            "hostnames": ["router.local"],
            "ports": [
               {"portid":"80","protocol":"tcp","state":"open","service":"http","product":"...","version":"..."},
               ...
            ]
          },
          ...
        ]
        """
        if not os.path.isfile(xml_path):
            raise FileNotFoundError(f"Nmap XML not found: {xml_path}")

        tree = ET.parse(xml_path)
        root = tree.getroot()

        hosts = []
        for host in root.findall("host"):
            status_el = host.find("status")
            status = status_el.attrib.get("state") if status_el is not None else "unknown"

            # address (prefer ipv4)
            addr = None
            addrtype = None
            for a in host.findall("address"):
                if a.attrib.get("addrtype") == "ipv4":
                    addr = a.attrib.get("addr")
                    addrtype = "ipv4"
                    break
            if not addr:
                # fallback to first address element
                a = host.find("address")
                if a is not None:
                    addr = a.attrib.get("addr")
                    addrtype = a.attrib.get("addrtype", None)

            # hostnames
            hostnames = [hn.attrib.get("name") for hn in host.findall("hostnames/hostname") if hn.attrib.get("name")]

            # ports
            ports_list = []
            ports_el = host.find("ports")
            if ports_el is not None:
                for p in ports_el.findall("port"):
                    portid = p.attrib.get("portid")
                    protocol = p.attrib.get("protocol")
                    state_el = p.find("state")
                    state = state_el.attrib.get("state") if state_el is not None else ""
                    service_el = p.find("service")
                    service = service_el.attrib.get("name") if service_el is not None else ""
                    product = service_el.attrib.get("product") if (service_el is not None and "product" in service_el.attrib) else ""
                    version = service_el.attrib.get("version") if (service_el is not None and "version" in service_el.attrib) else ""
                    ports_list.append({
                        "portid": portid,
                        "protocol": protocol,
                        "state": state,
                        "service": service,
                        "product": product,
                        "version": version
                    })

            hosts.append({
                "ip": addr or "unknown",
                "addrtype": addrtype,
                "status": status,
                "hostnames": hostnames,
                "ports": ports_list
            })

        return hosts
