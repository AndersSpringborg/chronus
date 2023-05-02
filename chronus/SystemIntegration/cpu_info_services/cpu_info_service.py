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
        info = CpuInfo()

        info.name = self._get_cpu_model_name(output.stdout)
        info.cores = self._get_cores(output.stdout)
        info.frequencies = self._get_frequencies()
        info.threads_per_core = self._get_threads_per_core(output.stdout)

        return info

    def _get_frequencies(self) -> List[float]:
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

    def _get_cpu_model_name(self, stdout: str) -> str:
        self.logger.debug("Parsing output of lscpu to get CPU model name")
        model_name = re.search(r"Model name:\s+(.*)", stdout)

        if model_name is None:
            self.logger.debug("Failed to find CPU model name")
            return "Unknown"

        return model_name.group(1)

    def _get_cores(self, stdout: str) -> int:
        cores = re.search(r"Core\(s\) per socket:\s+(\d+)", stdout)

        if cores is None:
            self.logger.debug("Failed to find cores")
            return 0

        self.logger.debug(f"Found {cores.group(1)} CPU cores")
        return int(cores.group(1))

    def _get_threads_per_core(self, stdout: str) -> int:
        threads_per_core = re.search(r"Thread\(s\) per core:\s+(\d+)", stdout)

        if threads_per_core is None:
            self.logger.debug("Failed to find threads per core")
            return 0

        self.logger.debug(f"Found {threads_per_core.group(1)} threads per core")
        return int(threads_per_core.group(1))
