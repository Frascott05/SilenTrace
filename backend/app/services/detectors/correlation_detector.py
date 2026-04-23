from detectors.base_detector import BaseDetector


class CorrelationDetector(BaseDetector):

    def run(self, raw, processes):
        for proc in processes.values():
            d = set(proc["detections"])

            if {"suspicious_command", "external_connection"} <= d:
                proc["detections"].append("command_and_control")

            if {"memory_injection", "external_connection"} <= d:
                proc["detections"].append("active_exploitation")

            if {"suspicious_parent_chain", "suspicious_command"} <= d:
                proc["detections"].append("macro_attack")
