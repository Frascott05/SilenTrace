import subprocess
import json

class VolatilityPluginRunner:
    def __init__(self, volatility_path: str, memory_file: str, plugin: str, os: str = None, output_json: bool = False):
        """
        :param volatility_path: Path to vol.py o vol.exe file
        :param memory_file: Path to memory dump
        :param plugin: Plugin to execute name (es. 'pstree', 'pslist', ecc.)
        :param os: Operative Sistem (es. 'windows', 'linux', 'mac'), optional
        :param output_json: If true, it outputs the command in json
        """
        self.volatility_path = volatility_path
        self.memory_file = memory_file
        self.plugin = plugin
        self.os = os
        self.output_json = output_json

    def run(self):
        # Building the volatility command
        cmd = ["python3", self.volatility_path, "-f", self.memory_file]

        # Adding Json if required
        if self.output_json:
            cmd.extend(["-r", "json"])

        # Adding OS if specified
        if self.os:
            cmd.append(f"{self.os.value}.{self.plugin}")
        else:
            cmd.append(self.plugin)


        # Printing the command to execute (for debug purposes)
        print("Eseguo:", " ".join(cmd))

        # Execute the process
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
            if self.output_json:
                return json.loads(output)
            return output
        except subprocess.CalledProcessError as e:
            print("Error during the execution:", e.stderr)
            return None

