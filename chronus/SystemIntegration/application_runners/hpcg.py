import logging
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
            self._output_dir = "../"
        else:
            if output_dir[-1] != "/":
                output_dir += "/"

        self._output_dir = output_dir
        self._output = ""
        self.logger = logging.getLogger(__name__)

    def prepare(self):
        if self._output_dir_exists():
            raise FileExistsError("Output dir already exists")
        self._prepare_output_dir()
        self._prepare_hpcg_dat_file()
        self.logger.info("Prepared HPCG Service")

    def run(self, cores: int = 1, frequency: int = 1_500_000, thread_per_core=1):
        slurm_file_content = self._generate_slurm_file_content(cores, frequency, thread_per_core)

        with open(
            self._output_dir + "hpcg_benchmark_output/HPCG_BENCHMARK.slurm", "w"
        ) as slurm_file:
            slurm_file.write(slurm_file_content)

        job: subprocess.CompletedProcess = subprocess.run(
            ["sbatch", "HPCG_BENCHMARK.slurm"],
            cwd=self._output_dir + "hpcg_benchmark_output",
            stdout=subprocess.PIPE,
        )

        stdout = str(job.stdout)
        # Regex for getting job id in: Submitted batch job 449
        job_id_str = re.search(r"Submitted batch job (\d+)", stdout).group(1)

        self._job_id = int(job_id_str)
        self.logger.info(f"Job started with id: {self._job_id}")

    def is_running(self) -> bool:
        cmd = subprocess.run(["scontrol", "show", "job", str(self._job_id)], stdout=subprocess.PIPE)

        is_running = re.search(r"JobState=COMPLETED", str(cmd.stdout)) is None

        return is_running

    @property
    def gflops(self) -> float:
        output_file_content = self._get_output_file_content()
        gflops = self._parse_gflops(output_file_content)
        self.logger.debug(f"GFlops calculated: {gflops}")
        return gflops

    def _get_output_file_content(self):
        files = os.listdir(self._output_dir + "hpcg_benchmark_output")
        output_file = [f for f in files if re.match(r"HPCG-Benchmark_", f)][0]
        output_file_content = open(
            self._output_dir + "hpcg_benchmark_output/" + output_file, "r"
        ).read()
        return output_file_content

    @property
    def result(self) -> float:
        output_file_content = self._get_output_file_content()
        results = self._parse_result(output_file_content)
        self.logger.debug(f"Results parsed: {results}")
        return results

    def cleanup(self):
        # Delte all files in outpur dir, and then delete the dir
        os.system(f"rm -rf {self._output_dir}hpcg_benchmark_output")
        self.logger.info("HPCG Service cleaned up")

    def _generate_slurm_file_content(self, cores, frequency, thread_per_core) -> str:
        return f"""#!/bin/bash
#SBATCH --job-name=HPCG_BENCHMARK
#SBATCH --output=HPCG_BENCHMARK.out
#SBATCH --error=HPCG_BENCHMARK.err
#SBATCH --nodes=1
#SBATCH --ntasks={cores}
#SBATCH --cpu-freq={frequency}

srun --mpi=pmix_v4 --ntasks-per-core={thread_per_core} {self._hpcg_path}"""

    def _parse_gflops(self, output: str) -> float:
        gflops_parser = re.compile(r"GFLOP/s rating of=(?P<gflops>\d+\.\d+)")
        match = gflops_parser.search(output)

        if match:
            gflops = float(match.group("gflops"))
            self.logger.info(f"GFLOP/s rating found: {gflops}")
            return gflops

        self.logger.warning("GFLOP/s rating not found in output")
        return 0.0

    def _parse_result(self, output_file_content: str) -> float:
        # parse Floating Point Operations Summary::Total=1.36952e+08 to 136952000.0
        result_parser = re.compile(
            r"Floating Point Operations Summary::Total=(?P<result>\d+\.\d+e\+\d+)"
        )
        match = result_parser.search(output_file_content)
        if match:
            result = float(match.group("result"))
            self.logger.info(f"Result found: {result}")
            return result
        self.logger.warning("Result not found in output")
        return 0.0

    def _prepare_output_dir(self):
        output_dir = self._output_dir + "hpcg_benchmark_output"
        os.mkdir(output_dir)
        self.logger.info(f"Created directory: {output_dir}")

    def _prepare_hpcg_dat_file(self):
        output_dir = self._output_dir + "hpcg_benchmark_output"
        dat_file_path = output_dir + "/hpcg.dat"
        with open(dat_file_path, "w") as dat_file:
            dat_file.write(hpcg_dat_file_content)
        self.logger.info(f"Created file: {dat_file_path}")

    def _output_dir_exists(self):
        output_dir = self._output_dir + "hpcg_benchmark_output"
        if os.path.exists(output_dir):
            self.logger.info(f"Directory exists: {output_dir}")
            return True
        self.logger.warning(f"Directory does not exist: {output_dir}")
        return False
