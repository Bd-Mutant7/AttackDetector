# Author cybalp
# PATH core/matcher.py
# Description It compares the extracted package features with the user's YAML rules and performs detection in case of a match (attack).

import logging

class MatchingEngine:
    def __init__(self, rules):
        self.rules = rules

    def analyze(self, packet_features):
        if not packet_features or not packet_features.get("protocol"):
            return None

        for rule in self.rules:
            if rule.get("protocol") and rule["protocol"] != packet_features["protocol"]:
                continue

            ports = rule.get("ports", [])
            if ports:
                if packet_features["src_port"] not in ports and packet_features["dst_port"] not in ports:
                    continue

            payload_matches = rule.get("payload_match", [])
            if payload_matches and packet_features.get("payload"):
                for signature in payload_matches:
                    if signature.lower() in packet_features["payload"].lower():
                        logging.warning(f"ALERT! Threat Detected: {rule['name']} (Rule ID: {rule['id']})")
                        return rule 
            
        return None