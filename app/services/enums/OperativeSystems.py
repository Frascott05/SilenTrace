from enum import Enum


class OperativeSystems(Enum):
    WINDOWS = "windows"
    MAC_OS = "mac"
    LINUX = "linux"
    DEFAULT = WINDOWS
    
    @classmethod
    def list(cls):
        return [system.value for system in cls]