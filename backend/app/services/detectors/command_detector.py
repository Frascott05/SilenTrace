from detectors.base_detector import BaseDetector
from core.event_builder import EventBuilder
from utils.constants import SUSPICIOUS_CMD_PATTERNS


class CommandDetector(BaseDetector):

    def run(self, raw, processes):
        for c in raw.get("cmdline", []):
            pid = c.get("PID")
            if pid not in processes:
                continue

            cmd = (c.get("Args") or "").lower()

            processes[pid]["events"].append(
                EventBuilder.build(None, "command", cmd)
            )

            if any(p in cmd for p in SUSPICIOUS_CMD_PATTERNS):
                processes[pid]["detections"].append("suspicious_command")
