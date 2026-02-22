# Author cybalp
# PATH core/packet_parser.py
# Description It breaks down captured complex network packets; converts critical parts such as IP, Port, Protocol, and Payload into a clean dictionary.

from scapy.all import IP, TCP, UDP, Raw
import logging

class PacketParser:
    @staticmethod
    def extract_features(packet):
        features = {
            "src_ip": None,
            "dst_ip": None,
            "src_port": None,
            "dst_port": None,
            "protocol": None,
            "payload": ""
        }

        try:
            if IP in packet:
                features["src_ip"] = packet[IP].src
                features["dst_ip"] = packet[IP].dst
            if TCP in packet:
                features["protocol"] = "TCP"
                features["src_port"] = packet[TCP].sport
                features["dst_port"] = packet[TCP].dport
            elif UDP in packet:
                features["protocol"] = "UDP"
                features["src_port"] = packet[UDP].sport
                features["dst_port"] = packet[UDP].dport
            if Raw in packet:
                features["payload"] = packet[Raw].load.decode('utf-8', errors='ignore')

            return features
        except Exception as e:
            logging.debug(f"Error parsing packet: {e}")
            return features