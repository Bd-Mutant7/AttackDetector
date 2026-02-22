# 🛡️AttackDetector 🛡️

<div align="center">

![Cyber Security](https://img.shields.io/badge/Cyber-Security-blue?style=for-the-badge&logo=cloudera&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-Rules-cb171e?style=for-the-badge&logo=yaml&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-Network_Analysis-red?style=for-the-badge)
![Discord](https://img.shields.io/badge/Discord-Alerts-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
![Open%20Source](https://img.shields.io/badge/Open%20Source-3DA639?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

</div>
  
  ```mermaid
  graph TD
      A[Network Traffic / PCAP] -->|Raw Data| B(Packet Parser)
      B -->|Extracted Features| C{Matching Engine}
      D[YAML Rules] -->|Load| C
      C -->|No Match| E[Discard]
      C -->|Match Found| F[Alert Manager]
      F -->|Log| G[(detector.log)]
      F -->|Discord Notification| H[Discord Webhook]
      F -->|Console Alert| I[Terminal UI]
  ```

AttackDetector is a modular, "Plug-and-Play" Intrusion Detection System (IDS) prototype. It analyzes network traffic in real-time to detect cyber attacks using a custom, easily readable YAML-based rule engine.

Say goodbye to complex traditional rule structures. AttackDetector allows you to easily configure defenses against web, network, and system-level threats!

## Features

- **Custom YAML Rule Engine:** Write and read detection rules effortlessly.
- **Multi-threaded Core:** Fast packet processing optimized for high traffic.
- **Live & Offline Analysis:** Sniff live network interfaces or analyze `.pcap` files.
- **Real-time Alerting:** Get notified via console, log files, or Discord Webhooks.
- **Docker Support:** Containerized for easy deployment across any environment.

## Installation & Setup

### Method 1: Local Environment (Python) 🐍

**Clone the repository and set up a virtual environment:**

  ```bash
  git clone https://github.com/cybalp/AttackDetector
  cd AttackDetector
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
  ```

**Install dependencies:**

  ```py
  pip install -r requirements.txt
  ```

### Method 2: Docker 🐳

If you prefer using Docker, you can build and run the system without installing local dependencies:

  ```bash
  docker build -t attackdetector:v1.0 .
  # To run with a pcap file:
  docker run -v $(pwd)/tests:/app/tests attackdetector:v1.0 -r tests/test_attacks.pcap
  ```

## Usage

You can run AttackDetector in two main modes:

**1. Offline PCAP Analysis:**
  Analyze pre-captured traffic to test rules or investigate past events.

  ```bash
  python main.py -r test_attacks.pcap
  ```

**2. Live Network Sniffing:**
  Listen to an active network interface (requires admin/root privileges).
  
  ```bash
  sudo python main.py -i eth0
  ```

(If no argument is provided, it defaults to the interface specified in `config/settings.yaml`)

## Configuration (`config/settings.yaml`)

You can tweak the core engine settings in `config/settings.yaml`:

- `default_interface`: Default network interface for live listening (e.g., eth0, Wi-Fi)
- `threads`: Multi-threading processor power (Affects the packet processing speed per second)
- `logging`: Set log levels (INFO, DEBUG) and log file path.
- `discord`_webhook: Paste your webhook URL to receive critical alerts on Discord.
- `api`: Malicious IP analysis

## Rule Writing Guide (`rules/custom.rules`)

AttackDetector uses a simple YAML format for writing threat signatures. Here is how you can write your own rules:

### Rule Structure

- `id`: Unique identifier for the rule -> e.g. 1001
- `name`: Descriptive name of the attack.
- `protocol`: Target protocol -> `TCP`, `UDP`
- `ports`: List of target ports -> e.g. `[80, 443]`
- `payload_match`: List of strings/signatures to look for in the packet payload.
- `action`: What to do when triggered -> `alert`, `block`
- `severity`: Threat level -> `low`, `medium`, `high`, `critical`

**Example Rule: Cross-Site Scripting (XSS)**
  
  ```yaml
  - id: 1003
    name: "XSS Payload Detected"
    protocol: "TCP"
    ports: [80, 443]
    payload_match: ["<script>", "javascript:alert", "onerror="]
    action: "alert"
    severity: "medium"
  ```

Just add your new rules under the `rules:` section in `rules/custom.rules` and restart the engine!

## Logs and Alerts 🚨

Detected threats are instantly saved to `logs/detector.log` in JSON format for easy integration with SIEM tools. Critical and High severity alerts are printed to the console in color and sent to Discord (if configured).

---

### How to Contribute?

Your contributions make this project stronger! You can help by:

- Reporting bugs by opening an **Issue**.
- Suggesting new YAML rule sets to expand the threat library.
- Submitting a **Pull Request** for performance optimizations or new features.

**AttackDetector** is licensed under the [MIT License](LICENSE).

### Support Me 🤍

Help keep the project alive and motivate me to add new features by buying me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/cybalpxb)
[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/cybalp)