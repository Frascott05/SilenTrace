from typing import List, Dict, Any
from datetime import datetime


class TimelineAnalysisService:

    # -----------------------------
    # 🎯 ENTRYPOINT
    # -----------------------------
    def analyze(self, raw: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        process_index = self._build_process_index(raw)
        processes = self._build_process_timeline(raw, process_index)

        return {
            "processes": processes,
            "global_timeline": self._build_global_timeline(processes)
        }

    # -----------------------------
    # 🧱 PROCESS INDEX
    # -----------------------------
    def _build_process_index(self, raw):
        index = {}

        for source in ["pslist", "psscan", "pstree"]:
            for p in raw.get(source, []):
                pid = p.get("PID")
                if pid:
                    index[pid] = p

        return index

    # -----------------------------
    # 🧠 BUILD PROCESS TIMELINE
    # -----------------------------
    def _build_process_timeline(self, raw, index):
        processes = {}

        # init process objects
        for pid, p in index.items():
            processes[pid] = {
                "pid": pid,
                "name": p.get("ImageFileName"),
                "ppid": p.get("PPID"),
                "events": [],
                "score": 0,
                "risk": "LOW",
                "detections": []
            }

        # attach events
        self._attach_process_events(raw, processes)
        self._attach_network_events(raw, processes)
        self._attach_cmd_events(raw, processes)
        self._attach_registry_events(raw, processes)
        self._attach_malware_events(raw, processes)

        # scoring + detection
        for proc in processes.values():
            self._score_process(proc)

        return list(processes.values())

    # -----------------------------
    # 🖥️ PROCESS EVENTS
    # -----------------------------
    def _attach_process_events(self, raw, processes):
        for p in raw.get("pslist", []):
            pid = p.get("PID")

            if pid not in processes:
                continue

            if p.get("CreateTime"):
                processes[pid]["events"].append(self._event(
                    p["CreateTime"], "start", "Process started"
                ))

            if p.get("ExitTime"):
                processes[pid]["events"].append(self._event(
                    p["ExitTime"], "exit", "Process exited"
                ))

    # -----------------------------
    # 🌐 NETWORK
    # -----------------------------
    def _attach_network_events(self, raw, processes):
        for n in raw.get("netscan", []):
            pid = n.get("PID")
            if pid not in processes:
                continue

            ip = n.get("ForeignAddr")

            processes[pid]["events"].append(self._event(
                n.get("Created"),
                "network",
                f"Connection to {ip}"
            ))

            # detection: external IP
            if ip and not ip.startswith(("127.", "0.", "192.168")):
                processes[pid]["detections"].append("external_connection")

    # -----------------------------
    # 💻 CMDLINE
    # -----------------------------
    def _attach_cmd_events(self, raw, processes):
        for c in raw.get("cmdline", []):
            pid = c.get("PID")
            if pid not in processes:
                continue

            cmd = c.get("Args")

            processes[pid]["events"].append(self._event(
                None,
                "command",
                cmd
            ))

            # detection
            if cmd and ("powershell" in cmd.lower() or "enc" in cmd.lower()):
                processes[pid]["detections"].append("suspicious_command")

    # -----------------------------
    # 🧾 REGISTRY
    # -----------------------------
    def _attach_registry_events(self, raw, processes):
        for r in raw.get("registry.printkey", []):
            key = r.get("Key")

            # naive association: attach to all processes
            for proc in processes.values():
                if key and "Run" in key:
                    proc["events"].append(self._event(
                        r.get("Last Write Time"),
                        "registry",
                        f"Persistence key modified: {key}"
                    ))
                    proc["detections"].append("persistence")

    # -----------------------------
    # 🧬 MALWARE
    # -----------------------------
    def _attach_malware_events(self, raw, processes):
        for m in raw.get("malfind", []):
            pid = m.get("PID")
            if pid not in processes:
                continue

            processes[pid]["events"].append(self._event(
                None,
                "malware",
                "Suspicious memory region"
            ))

            processes[pid]["detections"].append("memory_injection")

    # -----------------------------
    # 📊 SCORING
    # -----------------------------
    def _score_process(self, proc):
        score = 0

        detections = set(proc["detections"])

        if "memory_injection" in detections:
            score += 50
        if "external_connection" in detections:
            score += 20
        if "persistence" in detections:
            score += 30
        if "suspicious_command" in detections:
            score += 20

        proc["score"] = score

        if score >= 70:
            proc["risk"] = "HIGH"
        elif score >= 30:
            proc["risk"] = "MEDIUM"
        else:
            proc["risk"] = "LOW"

        # ordina eventi
        proc["events"] = sorted(proc["events"], key=lambda x: x["timestamp"] or "")

    # -----------------------------
    # 🌍 GLOBAL TIMELINE
    # -----------------------------
    def _build_global_timeline(self, processes):
        timeline = []

        for proc in processes:
            for e in proc["events"]:
                timeline.append({
                    "timestamp": e["timestamp"],
                    "pid": proc["pid"],
                    "process": proc["name"],
                    "type": e["type"],
                    "description": e["description"],
                    "risk": proc["risk"]
                })

        return sorted(timeline, key=lambda x: x["timestamp"] or "")

    # -----------------------------
    # 🔧 EVENT BUILDER
    # -----------------------------
    def _event(self, ts, event_type, description):
        return {
            "timestamp": self._normalize(ts),
            "type": event_type,
            "description": description
        }

    # -----------------------------
    # 🕒 NORMALIZE
    # -----------------------------
    def _normalize(self, ts):
        if not ts:
            return None

        if isinstance(ts, datetime):
            return ts.isoformat()

        return str(ts)