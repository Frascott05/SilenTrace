from detectors.base_detector import BaseDetector
from core.event_builder import EventBuilder
from utils.constants import SUSPICIOUS_PARENTS, LOLBINS


class ProcessDetector(BaseDetector):

    def run(self, raw, processes):
        for p in raw.get("pslist", []):
            pid = p.get("PID")
            if pid not in processes:
                continue

            if p.get("CreateTime"):
                processes[pid]["events"].append(
                    EventBuilder.build(p["CreateTime"], "start", "Process started")
                )

        for proc in processes.values():
            parent = processes.get(proc["ppid"])
            if not parent:
                continue

            if parent["name"] in SUSPICIOUS_PARENTS and proc["name"] in LOLBINS:
                proc["detections"].append("suspicious_parent_chain")
