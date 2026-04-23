from datetime import datetime


class EventBuilder:

    @staticmethod
    def build(ts, event_type, description):
        return {
            "timestamp": EventBuilder.normalize(ts),
            "type": event_type,
            "description": description
        }

    @staticmethod
    def normalize(ts):
        if not ts:
            return None
        if isinstance(ts, datetime):
            return ts.isoformat()
        return str(ts)
