class TimelineBuilder:

    def build(self, processes):
        timeline = []

        for proc in processes.values():
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
