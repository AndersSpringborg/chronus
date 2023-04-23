from typing import List

import re
import subprocess

from chronus.domain.interfaces.cpu_info_service_interface import CpuInfo, CpuInfoServiceInterface


class LsCpuInfoService(CpuInfoServiceInterface):
    def get_cpu_info(self) -> CpuInfo:
        # Run lscpu and parse the model name
        output = subprocess.run("lscpu", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if output.returncode != 0:
            print(output.returncode)
            raise RuntimeError("Failed to run lscpu")
        # Regex that finds Model Name: <model name>
        model_name = re.search(r"Model name:\s+(.*)", output.stdout)

        if model_name is None:
            return CpuInfo("Unknown")

        return CpuInfo(model_name.group(1))

    def get_frequencies(self) -> List[float]:

        try:
            file = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies", "r")
            output = file.read()
            file.close()
        except IOError:
            raise RuntimeError(
                "Failed to read /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies"
            )

        # Regex that finds all frequencies
        frequencies = re.findall(r"(\d+)", output)

        frequencies = [float(frequency) for frequency in frequencies]
        frequencies.sort()

        return frequencies

    def get_cores(self) -> int:
        output = subprocess.run("lscpu", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if output.returncode != 0:
            raise RuntimeError("Failed to run lscpu")

        # Regex that finds Model Name: <model name>
        cores = re.search(r"CPU\(s\):\s+(.*)", output.stdout)

        if cores is None:
            return 0

        return int(cores.group(1))
