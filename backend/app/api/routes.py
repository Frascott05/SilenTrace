from fastapi import APIRouter
from app.services.job_manager import job_manager
from app.services.volatilityPluginsList import VolatilityPluginList
from app.models.schemas import RunRequest, ListRequest, TimelineRequest

router = APIRouter()

@router.post("/run")
def run_plugins(req: RunRequest):
    job_id = job_manager.create_job(req)
    return {"job_id": job_id}

@router.get("/status/{job_id}")
def status(job_id: str):
    return job_manager.get_status(job_id)

@router.get("/results/{job_id}")
def results(job_id: str):
    return job_manager.get_results(job_id)["results"]

@router.post("/plugin-list")
def plugin_list(req: ListRequest):
    r = VolatilityPluginList()
    return r.get_plugins_by_os(req.os)

@router.post("/timeline")
def timeline_parser(req: TimelineRequest):
    job_id = job_manager.create_job(req)
    return {"job_id": job_id}