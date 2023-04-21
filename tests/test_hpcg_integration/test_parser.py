import pytest

from chronus.SystemIntegration.hpcg import HpcgService
from tests.test_hpcg_integration.outputs.hpcg_summary import hpcg_summary


class TestHPCGRunner:
    def __init__(self):
        self._output = ""

    def run(self):
        return self._output

    @staticmethod
    def from_string(output: str) -> "TestHPCGRunner":
        runner = TestHPCGRunner()
        runner._output = output
        return runner

    @staticmethod
    def from_file(file_path: str) -> "TestHPCGRunner":
        runner = TestHPCGRunner()
        with open(file_path) as f:
            runner._output = f.read()
        return runner


def test_import_works():
    """Example test with parametrization."""
    hpcg_service = HpcgService()
    assert hpcg_service


@pytest.mark.parametrize(
    ("gflops"),
    [
        0.0,
        15.3024,
        123456.123456,
    ],
)
def test_parse_gflops(gflops):
    test_runner = TestHPCGRunner.from_string(
        f"Final Summary::HPCG result is VALID with a GFLOP/s rating of={gflops}"
    )
    hpcg_service = HpcgService(test_runner)
    run = hpcg_service.run()

    assert run.gflops == gflops


def test_reads_full_output():
    test_runner = TestHPCGRunner.from_string(hpcg_summary)
    hpcg_service = HpcgService(test_runner)
    hpcg_service.run()

    assert len(hpcg_service._output.split("\n")) == 127


def test_parse_gflops_from_file():
    test_runner = TestHPCGRunner.from_string(hpcg_summary)
    hpcg_service = HpcgService(test_runner)
    run = hpcg_service.run()

    assert run.gflops == 15.3024
