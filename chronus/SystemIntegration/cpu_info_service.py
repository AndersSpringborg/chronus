from typing import List

import logging
import re
import subprocess

from chronus.domain.interfaces.cpu_info_service_interface import CpuInfo, CpuInfoServiceInterface


class LsCpuInfoService(CpuInfoServiceInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_cpu_info(self) -> CpuInfo:
        self.logger.debug("Running lscpu command to get CPU info")
        output = subprocess.run("lscpu", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if output.returncode != 0:
            raise RuntimeError(f"Failed to run lscpu: {output.stderr}")

        self.logger.debug("Parsing output of lscpu to get CPU model name")
        model_name = re.search(r"Model name:\s+(.*)", output.stdout)

        if model_name is None:
            return CpuInfo("Unknown")

        return CpuInfo(model_name.group(1))

    def get_frequencies(self) -> List[float]:
        self.logger.debug("Reading available CPU frequencies")
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

        self.logger.debug(f"Found available frequencies: {frequencies}")
        return frequencies

    def get_cores(self) -> int:
        self.logger.debug("Running lscpu command to get CPU cores")
        output = subprocess.run("lscpu", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if output.returncode != 0:
            raise RuntimeError(f"Failed to run lscpu: {output.stderr}")

        # Regex that finds Model Name: <model name>
        cores = re.search(r"CPU\(s\):\s+(.*)", output.stdout)

        if cores is None:
            return 0

        self.logger.debug(f"Found {cores.group(1)} CPU cores")
        return int(cores.group(1))
