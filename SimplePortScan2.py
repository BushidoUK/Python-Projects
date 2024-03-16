#!/usr/bin/python

import socket as sk

# Create a file to store the open ports
output_file = "open_ports.txt"

with open(output_file, "w") as f:
    for port in range(1, 1024):  # The Range of Ports Scanned
        try:
            s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)  # Address Family IPv4 and TCP Socket
            s.settimeout(1)  # Scan for 1 second (not 1000 seconds)
            s.connect(('192.168.85.255', port))  # Localhost is the default IP to be scanned from Port 1-1024
            print('%d:OPEN' % (port))  # The open ports are printed to the console
            f.write('%d:OPEN\n' % (port))  # Write the open port to the file
            s.close()  # Close the socket
        except:
            continue

print(f"Open ports saved to {output_file}")
