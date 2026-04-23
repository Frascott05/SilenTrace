from pydantic import BaseModel
from typing import List, Optional

class RunRequest(BaseModel):
    memory_file: str
    plugins: List[str]
    os: Optional[str] = "windows"
    address: Optional[str] = None
    dump: Optional[bool] = False
    process: Optional[int] = None 

class ListRequest(BaseModel):
    os: Optional[str] = "windows"

class TimelineRequest(RunRequest):
    memory_file: str
    plugins: List[str] = [
    # Core
    "pslist",
    "psscan",
    "pstree",
    "netscan",

    # User activity
    "cmdline",
    "consoles",

    # File / system
    "filescan",
    "handles",

    # Registry
    "registry.hivelist",
    "registry.printkey",

    # Malware
    "malfind",
    "ldrmodules",

    # Advanced
    "callbacks",
    "timers",
    "getsids",
    ]
    os: Optional[str] = "windows"
    address: Optional[str] = None
    dump: Optional[bool] = False
    process: Optional[int] = None
    job_type: str = "timeliner"