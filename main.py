# Author cybalp
# PATH main.py
# Description Created for the test environment.
# Version 1.0

import logging
import argparse
from core.config_parser import ConfigParser
from core.rule_loader import RuleLoader
from core.engine import NetworkEngine

def main():
    config_parser = ConfigParser()
    settings = config_parser.load_settings() or {}

    log_level_str = settings.get('logging', {}).get('level', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting AttackDetector Initialization...")

    parser = argparse.ArgumentParser(description="AttackDetector - Custom Network IDS")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on (e.g., eth0, Wi-Fi)")
    parser.add_argument("-r", "--read", help="Read packets from a .pcap file")
    args = parser.parse_args()
    
    rule_loader = RuleLoader()
    rules = rule_loader.load_rules()

    if not rules:
        logging.error("No rules were loaded! Please check your rules/custom.rules file. Exiting...")
        return

    engine = NetworkEngine(rules, settings)

    if args.read:
        engine.start(pcap_file=args.read)
    elif args.interface:
        engine.start(interface=args.interface)
    else:
        default_iface = settings.get('network', {}).get('default_interface', 'eth0')
        logging.warning(f"No input source provided. Defaulting to interface: {default_iface}")
        engine.start(interface=default_iface)

if __name__ == "__main__":
    main()