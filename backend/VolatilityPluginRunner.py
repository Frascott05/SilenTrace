import subprocess
import json
from typing import Optional, Union


class VolatilityPluginRunner:
    def __init__(
        self,
        volatility_path: str,
        memory_file: str,
        plugin: str,
        os: Optional[str] = None,
        output_json: bool = False,
        dumped_file: bool = False,
        process: Optional[int] = None,
        physaddr: Optional[str] = None
    ):
        """
        :param volatility_path: Path to vol.py or vol.exe
        :param memory_file: Path to memory dump
        :param plugin: Plugin name (e.g., 'pstree', 'pslist')
        :param os: Operating system (e.g., 'windows', 'linux', 'mac'), optional
        :param output_json: If True, output will be parsed as JSON
        :param dumped_file: If True, enables dump-related options
        :param process: PID for plugin execution (if supported)
        :param phyaddr: Physical address / offset for analysis
        """
        self.volatility_path = volatility_path
        self.memory_file = memory_file
        self.plugin = plugin
        self.os = os
        self.output_json = output_json
        self.dumped_file = dumped_file
        self.process = process
        self.physaddr = physaddr

    def _build_command(self) -> list:
        cmd = ["python3", self.volatility_path, "-f", self.memory_file]

        # Output format
        if self.output_json:
            cmd.extend(["-r", "json"])

        # Plugin name (with OS prefix if provided)
        plugin_cmd = f"{self.os}.{self.plugin}" if self.os else self.plugin
        cmd.append(plugin_cmd)

        # Optional parameters
        if self.process is not None:
            cmd.extend(["--pid", str(self.process)])

        if self.physaddr is not None:
            cmd.extend(["--address", str(self.physaddr)])

        if self.dumped_file:
            cmd.append("--dump")

        return cmd

    def run(self) -> Optional[Union[str, dict]]:
        cmd = self._build_command()

        # Debug print
        print("Executing:", " ".join(cmd))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout.strip()

            if self.output_json:
                try:
                    return json.loads(output)
                except json.JSONDecodeError:
                    print("JSON parsing error. Raw output returned.")
                    return output

            return output

        except subprocess.CalledProcessError as e:
            print("Error during execution:")
            print(e.stderr)
            return None