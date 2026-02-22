# Author cybalp
# PATH core/rule_loader.py
# Description It reads the rules and prevents the system from crashing if there are any incorrect rules written.

import yaml
import logging

class RuleLoader:
    def __init__(self, rules_path="rules/custom.rules"):
        self.rules_path = rules_path
        self.rules = []

    def load_rules(self):
        try:
            with open(self.rules_path, 'r') as file:
                data = yaml.safe_load(file)
                self.rules = data.get('rules', [])
                logging.info(f"Successfully loaded {len(self.rules)} rules from {self.rules_path}.")
                return self.rules
        except FileNotFoundError:
            logging.error(f"Rule file not found: {self.rules_path}")
            return []
        except yaml.YAMLError as exc:
            logging.error(f"YAML parsing error in rule file: {exc}")
            return []