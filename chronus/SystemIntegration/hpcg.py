import re

from chronus.model.Run import Run

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

    def __init__(self, path: str = None):
        self._path = path

    def run(self) -> str:
        return "Final Summary::HPCG result is VALID with a GFLOP/s rating of=15.3024"
