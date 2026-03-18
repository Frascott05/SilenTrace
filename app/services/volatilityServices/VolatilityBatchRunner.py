
from typing import Dict, List, Optional
from VolatilityPluginRunner import VolatilityPluginRunner


class VolatilityBatchRunner:
    
    def __init__(self, volatility_path: str, memory_file: str, plugins: List[str], os:str=None):
        
        """
        :param volatility_path: Path to vol.py o vol.exe
        :param memory_file: Path to memory dump
        :param plugins: Lista of plugins to execute
        :param os: Operative sistem (windows, linux, mac)
        """
        self.volatility_path = volatility_path
        self.memory_file = memory_file
        self.plugins = plugins
        self.os = os
        self.results: Dict[str, Optional[dict]] = {}

    
    def run_all(self, json: bool):
        """
        This functions executes all the plugins in the given list

        :param json: boolean to choose if we want the json result
        """
        for plugin in self.plugins:

            runner = VolatilityPluginRunner(self.volatility_path, self.memory_file,
                                            plugin=plugin, os=self.os, output_json=json )
            result = runner.run()
            self.results[plugin] = result

    def get_result(self, plugin: str) -> Optional[dict]:
        """
        Don't call before running all the plugins.
        This function will give the result of the plugin specified
        after it was executed

        :param plugin: plugin to get the result
        :return: dict of the plugin result
        """
        return self.results.get(plugin)
    
    def get_all_result(self) -> Dict[str, Optional[dict]]:
        """
        Don't call before running all the plugins.
        This function will give the result of all the executed plugins

        :return: dict with other dict containing the plugins result
        """
        return self.results
    
    def get_successful_results(self) -> Dict[str, dict]:
        """
        Don't call before running all the plugins.
        This function will give the result of all the successful executed plugins

        :return: dict with other dict containing the plugins result
        """
        return {k: v for k, v in self.results.items() if v is not None}

    def get_failed_plugins(self) -> List[str]:
        """
        Don't call before running all the plugins.
        This function will give the result of all the plugins who failed to execute

        :return: dict with other dict containing the plugins result
        """
        return [k for k, v in self.results.items() if v is None]


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