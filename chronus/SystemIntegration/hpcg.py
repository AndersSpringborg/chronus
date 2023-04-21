import logging
import os
import re
from pprint import pprint

from chronus.domain.Run import Run


class HpcgService:
    _output: str

    def __init__(self, runner=None):
        self._runner = runner or HpcgRunner()
        self._output = ""

    def run(self):
        self._output = self._runner.run()
        gflops = self._parse_output(self._output)
        return Run(gflops=gflops)

    def _parse_output(self, output: str) -> float:
        gflops_parser = re.compile(r"GFLOP/s rating of=(?P<gflops>\d+\.\d+)")
        match = gflops_parser.search(output)

        if match:
            return float(match.group("gflops"))

        return 0.0

    def gflops(self) -> float:
        return self._gflops

    @classmethod
    def with_path(cls, path: str) -> "HpcgService":
        runner = HpcgRunner(path)
        return cls(runner)


class HpcgRunner:
    _run_id: int

    def __init__(self, path: str = None):
        self._path = path
        self._run_id = 0

    def run(self) -> str:
        # run system command
        import subprocess

        output_path = "./../out/run_output" + str(self._run_id) + ".txt"
        output = subprocess.call(["sh", "./../hpcg_debug.sh", output_path])
        # print current working directory
        print(output)

        # check if file exists
        if os.path.exists(output_path):
            print("File exists")
        else:
            print("File does not exist")
        self._run_id += 1

        file_output = "".join(open(output_path, "r").readlines())
        return file_output
