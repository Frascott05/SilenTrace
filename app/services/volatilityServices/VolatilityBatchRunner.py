from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from services.volatilityServices.VolatilityPluginRunner import VolatilityPluginRunner


class VolatilityBatchRunner:
    
    def __init__(self, volatility_path: str, memory_file: str, plugins: List[str], os: str = None):
        """
        :param volatility_path: Path to vol.py o vol.exe
        :param memory_file: Path to memory dump
        :param plugins: Lista of plugins to execute
        :param os: Operative system (windows, linux, mac)
        """
        self.volatility_path = volatility_path
        self.memory_file = memory_file
        self.plugins = plugins
        self.os = os
        self.results: Dict[str, Optional[dict]] = {}
        self._lock = threading.Lock()  # per thread safety

    def _run_single_plugin(self, plugin: str, json: bool) -> dict:
        """
        Esegue un singolo plugin
        """
        runner = VolatilityPluginRunner(
            self.volatility_path,
            self.memory_file,
            plugin=plugin,
            os=self.os,
            output_json=json
        )
        return runner.run()

    def run_all(self, json: bool, max_workers: int = 4):
        """
        Executes all plugins in parallel

        :param json: boolean to choose if we want the json result
        :param max_workers: number of parallel threads
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
        """
        Don't call before running all the plugins.
        Returns the result of a specific plugin
        """
        return self.results.get(plugin)
    
    def get_all_result(self) -> Dict[str, Optional[dict]]:
        """
        Returns all plugin results
        """
        return self.results
    
    def get_successful_results(self) -> Dict[str, dict]:
        """
        Returns only successful plugin results
        """
        return {
            k: v for k, v in self.results.items()
            if v is not None and "error" not in v
        }

    def get_failed_plugins(self) -> List[str]:
        """
        Returns plugins that failed
        """
        return [
            k for k, v in self.results.items()
            if v is None or (isinstance(v, dict) and "error" in v)
        ]


if __name__ == "__main__":
    # Example of use
    volatility_script = "/opt/volatility3/vol.py"
    memory_dump = "dumps/Snapshot1.vmem"
    plugin_name = ["pstree", "netscan", "hashdump", "psxview"]

    runner = VolatilityBatchRunner(
        volatility_script,
        memory_dump,
        plugin_name,
        os="windows"
    )

    runner.run_all(json=True, max_workers=4)

    result = runner.get_all_result()
    print("Successful results:")
    print(runner.get_successful_results())

    print("\nFailed plugins:")
    print(runner.get_failed_plugins())

    if result:
        print("\nAll results:")
        print(result)

if __name__ == "__main__":
    # Example of use
    volatility_script = "/opt/volatility3/vol.py"  # percorso a vol.py
    memory_dump = "dumps/Snapshot1.vmem"           # percorso al dump di memoria
    plugin_name = ["pstree", "netscan", "hashdump", "psxview"]  # plugin da eseguire

    runner = VolatilityBatchRunner(volatility_script, memory_dump, plugin_name, os="windows")
    result = runner.run_all(True)
    result = runner.get_all_result()
    print(runner.get_successful_results())

    if result:
        print("Risultato plugin (JSON):")
        print(result)