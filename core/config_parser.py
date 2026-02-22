# Author cybalp
# PATH core/config_parser.py
# Description Read the YAML files written by the user and convert them into Python dictionaries that the system can understand.

import yaml
import logging

class ConfigParser:
    def __init__(self, config_path="config/settings.yaml", rules_path="rules/custom.rules"):
        self.config_path = config_path
        self.rules_path = rules_path
        self.settings = {}
        self.rules = []

    def load_settings(self):
        try:
            with open(self.config_path, 'r') as file:
                self.settings = yaml.safe_load(file)
                return self.settings
        except FileNotFoundError:
            logging.error(f"Configuration file not found at {self.config_path}")
            return None

    def load_rules(self):
        try:
            with open(self.rules_path, 'r') as file:
                data = yaml.safe_load(file)
                self.rules = data.get('rules', [])
                return self.rules
        except FileNotFoundError:
            logging.error(f"Rules file not found at {self.rules_path}")
            return []  