from VolatilityBatchRunner import VolatilityBatchRunner
from app.services.timelinerservice import TimelineAnalysisService
from app.core.config import settings
import os

class VolatilityService:

    def __init__(self):
        """
        API service for using volatility plugins
        """
        self.timeline_analyzer = TimelineAnalysisService()

    def run(self, config):
        runner = VolatilityBatchRunner(
            volatility_path=settings.VOLATILITY_PATH,
            memory_file= os.path.join(settings.DUMPS_PATH, config.memory_file),
            plugins=config.plugins,
            os=config.os,
            process=config.process,
            address=config.address,
            dumped_file= config.dump
        )
        print("sent")

        runner.run_all(json=True)
        return runner.get_all_result()
    
    def process_timeliner(self, raw_results):
        events = raw_results
        if not events:
            return {}

        return self.timeline_analyzer.analyze(events)