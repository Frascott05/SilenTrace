from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from VolatilityPluginRunner import VolatilityPluginRunner


class VolatilityBatchRunner:
    
    def __init__(
        self,
        volatility_path: str,
        memory_file: str,
        plugins: List[str],
        os: str = None,
        dumped_file: bool = False,
        process: int = None,
        address: str = None
    ):
        """
        :param volatility_path: Path to vol.py o vol.exe
        :param memory_file: Path to memory dump
        :param plugins: Lista of plugins to execute
        :param os: Operative system (windows, linux, mac)
        :param dumped_file: Enable dump option
        :param process: PID for plugins that support it
        :param offset: Offset for plugins that support it
        """
        self.volatility_path = volatility_path
        self.memory_file = memory_file
        self.plugins = plugins
        self.os = os

        self.dumped_file = dumped_file
        self.process = process
        self.offset = address

        self.results: Dict[str, Optional[dict]] = {}
        self._lock = threading.Lock()

    def _run_single_plugin(self, plugin: str, json: bool) -> dict:
        """
        Execute a single plugin
        """
        runner = VolatilityPluginRunner(
            self.volatility_path,
            self.memory_file,
            plugin=plugin,
            os=self.os,
            output_json=json,
            dumped_file=self.dumped_file,
            process=self.process,
            physaddr=self.offset
        )
        return runner.run()

    def run_all(self, json: bool, max_workers: int = 4):
        """
        Executes all plugins in parallel
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._run_single_plugin, plugin, json): plugin
                for plugin in self.plugins
            }

            for future in as_completed(futures):
                plugin = futures[future]
                try:
                    result = future.result()
                    with self._lock:
                        self.results[plugin] = result
                except Exception as e:
                    with self._lock:
                        self.results[plugin] = {"error": str(e)}

    def get_result(self, plugin: str) -> Optional[dict]:
        return self.results.get(plugin)
    
    def get_all_result(self) -> Dict[str, Optional[dict]]:
        return self.results
    
    def get_successful_results(self) -> Dict[str, dict]:
        return {
            k: v for k, v in self.results.items()
            if v is not None and "error" not in v
        }

    def get_failed_plugins(self) -> List[str]:
        return [
            k for k, v in self.results.items()
            if v is None or (isinstance(v, dict) and "error" in v)
        ]
    

if __name__ == "__main__":
    volatility_script = "/home/kali/volatility/volatility3/vol.py"
    memory_dump = "Snapshot1.vmem"

    plugins = ["vadinfo"]#, "pstree", "netscan", "handles"]

    runner = VolatilityBatchRunner(
        volatility_path=volatility_script,
        memory_file=memory_dump,
        plugins=plugins,
        os="windows",
        dumped_file=False,   # set True if testing dump plugins
        process=4,        # e.g. 1234 if needed
        address="0x7fffebd0000"          # e.g. "0xfffffa8001234560" if needed
    )

    print("Starting batch execution...\n")

    runner.run_all(json=True, max_workers=4)

    print("\n✅ Successful results:")
    for plugin, result in runner.get_successful_results().items():
        print(f"\n--- {plugin} ---")
        print(result)
"""
    print("\n❌ Failed plugins:")
    print(runner.get_failed_plugins())

    print("\n📦 All results:")
    print(runner.get_all_result())"""