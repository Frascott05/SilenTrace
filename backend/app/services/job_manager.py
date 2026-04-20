import uuid
import threading

from app.services.volatility_service import VolatilityService

class JobManager:

    def __init__(self):
        self.jobs = {}
        self.service = VolatilityService()

    def create_job(self, config):
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {"status": "running", "results": None}

        thread = threading.Thread(target=self._run_job, args=(job_id, config))
        thread.start()

        return job_id

    def _run_job(self, job_id, config):
        try:
            raw_results = self.service.run(config)

            # if is a timeliner request
            if getattr(config, "job_type", None) == "timeliner":
                processed = self.service.process_timeliner(raw_results)
            else:
                processed = raw_results

            # saves results
            self.jobs[job_id]["results"] = processed
            self.jobs[job_id]["status"] = "done"

        except Exception as e:
            self.jobs[job_id]["status"] = "error"
            self.jobs[job_id]["results"] = {"error": str(e)}

    def get_status(self, job_id):
        return {"status": self.jobs[job_id]["status"]}

    def get_results(self, job_id):
        return self.jobs[job_id]

job_manager = JobManager()