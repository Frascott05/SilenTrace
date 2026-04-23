class ProcessBuilder:

    def build(self, raw):
        index = {}

        for source in ["pslist", "psscan", "pstree"]:
            for p in raw.get(source, []):
                pid = p.get("PID")
                if pid:
                    index[pid] = p

        processes = {}

        for pid, p in index.items():
            processes[pid] = {
                "pid": pid,
                "name": (p.get("ImageFileName") or "").lower(),
                "ppid": p.get("PPID"),
                "events": [],
                "detections": [],
                "score": 0,
                "risk": "LOW",
                "_net_count": 0,
            }

        return processes
