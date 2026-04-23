from detectors.base_detector import BaseDetector
from core.event_builder import EventBuilder


class RegistryDetector(BaseDetector):

    def run(self, raw, processes):
        for r in raw.get("registry.printkey", []):
            key = r.get("Key")

            if not key or "Run" not in key:
                continue

            for proc in processes.values():
                if proc["detections"]:
                    proc["events"].append(
                        EventBuilder.build(
                            r.get("Last Write Time"),
                            "registry",
                            f"Persistence: {key}"
                        )
                    )
                    proc["detections"].append("persistence")
