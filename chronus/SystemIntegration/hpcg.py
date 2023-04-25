import os
import re
import subprocess
from time import sleep

from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.Run import Run

hpcg_dat_file_content = """HPCG benchmark input file
Benchmarked on 2020-11-24 14:00:00
104 104 104
900"""


class HpcgService(ApplicationRunnerInterface):
    _output: str
    _job_id: int

    def __init__(self, hpcg_path, output_dir: str = ""):
        self._hpcg_path = hpcg_path
        if output_dir == "":
            self._output_dir = "./"
        else:
            if output_dir[-1] != "/":
                output_dir += "/"

        self._output_dir = output_dir
        self._output = ""

    def prepare(self):
        self._prepare_output_dir()
        self._prepare_hpcg_dat_file()

    def run(self, cores: int = 1, frequency: int = 1_500_000):
        slurm_file_content = self._generate_slurm_file_content(cores, frequency)

        with open(
            self._output_dir + "hpcg_benchmark_output/HPCG_BENCHMARK.slurm", "w"
        ) as slurm_file:
            slurm_file.write(slurm_file_content)

        job: subprocess.CompletedProcess = subprocess.run(
            ["sbatch", "HPCG_BENCHMARK.slurm"], cwd=self._output_dir + "hpcg_benchmark_output"
        )
        # Regex for getting job id in: Submitted batch job 449
        job_id_str = re.search(r"Submitted batch job (\d+)", job.stdout).group(1)

        self._job_id = int(job_id_str)

    def is_running(self) -> bool:
        cmd = subprocess.run(["scontrol", "show", "job", self._job_id], stdout=subprocess.PIPE)

        is_running = re.search(r"JobState=COMPLETED", cmd.stdout) is None

        return is_running

    @property
    def gflops(self) -> float:
        files = os.listdir(self._output_dir + "hpcg_benchmark_output")
        output_file = [f for f in files if re.match(r"HPCG-Benchmark_", f)][0]
        output_file_content = open(
            self._output_dir + "hpcg_benchmark_output/" + output_file, "r"
        ).read()
        gflops = self._parse_output(output_file_content)
        return gflops

    def cleanup(self):
        # Delte all files in outpur dir, and then delete the dir
        os.system(f"rm -rf {self._output_dir}hpcg_benchmark_output")

    def _generate_slurm_file_content(self, cores, frequency) -> str:
        return f"""#!/bin/bash
#SBATCH --job-name=HPCG_BENCHMARK
#SBATCH --output=HPCG_BENCHMARK.out
#SBATCH --error=HPCG_BENCHMARK.err
#SBATCH --n={cores}
#SBATCH --cpu-freq={frequency}

srun --mpi=pmix_v4 {self._hpcg_path}"""

    def _parse_output(self, output: str) -> float:
        gflops_parser = re.compile(r"GFLOP/s rating of=(?P<gflops>\d+\.\d+)")
        match = gflops_parser.search(output)

        if match:
            return float(match.group("gflops"))

        return 0.0

    def _prepare_output_dir(self):
        os.mkdir(self._output_dir + "hpcg_benchmark_output")

    def _prepare_hpcg_dat_file(self):
        dat_file = open(self._output_dir + "hpcg_benchmark_output/hpcg.dat", "w")
        dat_file.write(hpcg_dat_file_content)
        dat_file.close()
