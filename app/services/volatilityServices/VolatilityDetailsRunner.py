from VolatilityBatchRunner import VolatilityBatchRunner

class VolatilityDetailsRunner(VolatilityBatchRunner):

    """This class will allow you to execute specific plugins on a list of given processes (given by their PID)"""
    def __init__(self, volatility_path: str, memory_file: str,
                 ProcessesPlugins: list[str], processes: list[str], os: str = None):

        proc_str = " ".join(processes)

        options = f"{memory_file} -p {proc_str}"

        super().__init__(volatility_path, options, ProcessesPlugins, os=os)