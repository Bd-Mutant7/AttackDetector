# Author cybalp
# PATH core/alert_manager.py
# Description Logs detected threats and reports critical ones to Discord (dynamic settings).

import logging
import json
from datetime import datetime
import os
import requests

COLORS = {
    "CRITICAL": "\033[91m",  # red
    "HIGH": "\033[93m",      # yellow
    "MEDIUM": "\033[94m",    # blue
    "LOW": "\033[92m",       # green
    "RESET": "\033[0m"       # color restart
}

class AlertManager:
    def __init__(self, settings):
        self.settings = settings
        
        self.log_file = self.settings.get('logging', {}).get('file', 'logs/detector.log')
        self.webhook_url = self.settings.get('notifications', {}).get('discord_webhook', '')
        
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        self.file_logger = logging.getLogger("AlertManager_File")
        
        log_level_str = self.settings.get('logging', {}).get('level', 'INFO').upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        self.file_logger.setLevel(log_level)
        
        if not self.file_logger.handlers:
            file_handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)
            self.file_logger.addHandler(file_handler)

    def send_discord_alert(self, alert_data):
        if not self.webhook_url:
            return
            
        payload = {
            "content": f"🚨 **THREAT DETECTED** 🚨\n**Rule:** {alert_data['rule_name']}\n**Severity:** {alert_data['severity'].upper()}\n**Source:** {alert_data['src_ip']}:{alert_data['src_port']}\n**Destination:** {alert_data['dst_ip']}:{alert_data['dst_port']}\n**Protocol:** {alert_data['protocol']}"
        }
        try:
            requests.post(self.webhook_url, json=payload, timeout=3)
        except Exception as e:
            logging.error(f"Failed to send Discord webhook: {e}")

    def trigger_alert(self, rule, packet_features):
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "rule_id": rule.get("id"),
            "rule_name": rule.get("name"),
            "severity": rule.get("severity", "unknown"),
            "src_ip": packet_features.get("src_ip", "Unknown"),
            "dst_ip": packet_features.get("dst_ip", "Unknown"),
            "src_port": packet_features.get("src_port", "Unknown"),
            "dst_port": packet_features.get("dst_port", "Unknown"),
            "protocol": packet_features.get("protocol", "Unknown")
        }
        self.file_logger.info(json.dumps(alert_data))

        severity = alert_data['severity'].upper()
        color = COLORS.get(severity, COLORS["RESET"])
        print(f"{color}[!] THREAT DETECTED [{severity}]: {alert_data['rule_name']} | {alert_data['src_ip']}:{alert_data['src_port']} -> {alert_data['dst_ip']}:{alert_data['dst_port']}{COLORS['RESET']}")

        # Only send critical and high-level alerts to Discord
        if severity in ["CRITICAL", "HIGH"]:
           self.send_discord_alert(alert_data)