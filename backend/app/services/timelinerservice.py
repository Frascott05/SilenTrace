from core.process_builder import ProcessBuilder
from core.timeline_builder import TimelineBuilder
from detectors.process_detector import ProcessDetector
from detectors.network_detector import NetworkDetector
from detectors.command_detector import CommandDetector
from detectors.registry_detector import RegistryDetector
from detectors.malware_detector import MalwareDetector
from detectors.correlation_detector import CorrelationDetector
from scoring.scorer import Scorer


class TimelineAnalysisService:

    def __init__(self):
        self.process_builder = ProcessBuilder()
        self.timeline_builder = TimelineBuilder()

        self.detectors = [
            ProcessDetector(),
            NetworkDetector(),
            CommandDetector(),
            RegistryDetector(),
            MalwareDetector(),
            CorrelationDetector(),
        ]

        self.scorer = Scorer()

    def analyze(self, raw):
        processes = self.process_builder.build(raw)

        for detector in self.detectors:
            detector.run(raw, processes)

        for proc in processes.values():
            self.scorer.score(proc)

        return {
            "processes": list(processes.values()),
            "global_timeline": self.timeline_builder.build(processes)
        }
