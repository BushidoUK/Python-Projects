#!/usr/bin/env python

import argparse
import csv
import ipaddress
import requests
from datetime import datetime

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

def print_vt_report(ip, report, csv_writer):
    if "error" in report:
        return

    attributes = report["data"]["attributes"]
    ip_address = ip
    last_analysis_date = attributes.get("last_analysis_date", "N/A")
    if last_analysis_date != "N/A":
        last_analysis_date_utc = datetime.utcfromtimestamp(int(last_analysis_date)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        last_analysis_date_utc = "N/A"
    detected = attributes["last_analysis_stats"]["malicious"]
    tags = ", ".join(attributes.get("tags", []))
    country = attributes.get("country", "N/A")
    asn = attributes.get("asn", "N/A")
    
    csv_writer.writerow([ip_address, last_analysis_date_utc, detected, tags, country, asn])

def main():
    parser = argparse.ArgumentParser(description="Lookup IP addresses on VirusTotal and save the results to a CSV file.")
    parser.add_argument("input_file", help="Path to the input TXT file containing IP addresses.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    args = parser.parse_args()

    with open(args.input_file, "r") as input_file, open(args.output_file, "w", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(["IP Address", "Last Analysis Date (UTC)", "Detected", "Tags", "Country", "ASN"])

        for ip in input_file:
            ip = ip.strip()
            if not is_valid_ip(ip):
                print(f"Invalid IP address: {ip}")
                continue

            report = get_vt_report(ip)
            print_vt_report(ip, report, csv_writer)

if __name__ == "__main__":
    main()
