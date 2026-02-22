# Author cybalp
# PATH core/engine.py
# Description Snort/Suricata integration and traffic monitoring (Multi-threaded, dynamic settings)

from scapy.all import sniff
import logging
import threading
import queue
from core.packet_parser import PacketParser
from core.matcher import MatchingEngine
from core.alert_manager import AlertManager

class NetworkEngine:
    def __init__(self, rules, settings):
        self.settings = settings
        self.matcher = MatchingEngine(rules)
        self.parser = PacketParser()
        self.alert_manager = AlertManager(settings)
        self.packet_queue = queue.Queue()
        self.num_threads = self.settings.get('engine', {}).get('threads', 4)
        self.workers = []
        
        for _ in range(self.num_threads):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            self.workers.append(t)
            
        logging.info(f"Initialized {self.num_threads} worker threads for fast packet processing.")
    
    def _worker_loop(self):
        while True:
            packet = self.packet_queue.get()
            try:
                features = self.parser.extract_features(packet)
                match = self.matcher.analyze(features)
                if match:
                    self.alert_manager.trigger_alert(match, features)
            except Exception as e:
                logging.debug(f"Error processing packet: {e}")
            finally:
                self.packet_queue.task_done()

    def enqueue_packet(self, packet):
        self.packet_queue.put(packet)

    def start(self, interface=None, pcap_file=None):
        try:
            if pcap_file:
                logging.info(f"Starting offline analysis on: {pcap_file}")
                sniff(offline=pcap_file, prn=self.enqueue_packet, store=False)
                self.packet_queue.join() 
                logging.info("Offline pcap analysis completed.")
            elif interface:
                logging.info(f"Starting live capture on interface: {interface}")
                # Buradaki sniff artık daha güvenli
                sniff(iface=interface, prn=self.enqueue_packet, store=False)
            else:
                logging.error("No input source provided.")
        except PermissionError:
            logging.error("❌ [CRITICAL] Permission Denied! Live sniffing requires root/admin privileges (use sudo).")
        except OSError as e:
            logging.error(f"❌ [ERROR] Interface issue: {e}. Please check your interface name.")
        except Exception as e:
            logging.error(f"❌ [FATAL] Engine crashed unexpectedly: {e}")