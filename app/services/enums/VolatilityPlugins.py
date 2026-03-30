from enum import Enum


class VolatilityPlugins(Enum):
    PSTREE = "pstree"
    PSLIST = "pslist"
    NETSCAN = "netscan"
    HASHDUMP = "hashdump"
    #PSXVIEW = "psxview"

    @classmethod
    def list(cls):
        return [plugin.value for plugin in cls]