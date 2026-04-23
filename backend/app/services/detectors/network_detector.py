from detectors.base_detector import BaseDetector
from core.event_builder import EventBuilder
from utils.constants import SUSPICIOUS_PORTS
from utils.helpers import is_external_ip


class NetworkDetector(BaseDetector):

    def run(self, raw, processes):
        for n in raw.get("netscan", []):
            pid = n.get("PID")
            if pid not in processes:
                continue

            ip = n.get("ForeignAddr")
            port = n.get("ForeignPort")
            proc = processes[pid]

            proc["events"].append(
                EventBuilder.build(n.get("Created"), "network", f"{ip}:{port}")
            )

            proc["_net_count"] += 1

            if is_external_ip(ip):
                proc["detections"].append("external_connection")

            if port in SUSPICIOUS_PORTS:
                proc["detections"].append("suspicious_port")

            if proc["_net_count"] > 10:
                proc["detections"].append("beaconing")
