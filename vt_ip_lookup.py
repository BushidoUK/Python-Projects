#!/usr/bin/env python

import ipaddress
import requests

VT_API_URL = "https://www.virustotal.com/api/v3/ip_addresses/"
VT_API_KEY = "$API_KEY"

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_vt_report(ip):
    headers = {
        "x-apikey": VT_API_KEY
    }
    response = requests.get(VT_API_URL + ip, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {"error": "IP not found in VirusTotal database."}
    else:
        return {"error": "Failed to fetch data from VirusTotal."}

def print_vt_report(report):
    print("VirusTotal report:")
    if "error" in report:
        print("Error:", report["error"])
        return

    attributes = report.get("data", {}).get("attributes", {})
    ip_address = attributes.get("ip")
    if ip_address:
        print("IP Address:", ip_address)
    else:
        print("IP Address: N/A")

    last_analysis_date = attributes.get("last_analysis_date")
    if last_analysis_date:
        print("Last Analysis Date:", last_analysis_date)
    else:
        print("Last Analysis Date: N/A")

    detected = attributes.get("last_analysis_stats", {}).get("malicious")
    if detected is not None:
        print("Detected:", detected)
    else:
        print("Detected: N/A")

    tags = attributes.get("tags", [])
    if tags:
        print("Tags:", ", ".join(tags))
    else:
        print("Tags: N/A")

    country = attributes.get("country")
    if country:
        print("Country:", country)
    else:
        print("Country: N/A")

    asn = attributes.get("asn")
    if asn:
        print("ASN:", asn)
    else:
        print("ASN: N/A")

def main():
    ip_address = input("Enter the IP address to lookup: ").strip()

    if not is_valid_ip(ip_address):
        print("Invalid IP address.")
        return

    report = get_vt_report(ip_address)
    print_vt_report(report)

if __name__ == "__main__":
    main()
