import pytest

from chronus.SystemIntegration.hpcg import HpcgService


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
    test_runner = TestHPCGRunner.from_string(summary)
    hpcg_service = HpcgService(test_runner)
    hpcg_service.run()

    assert len(hpcg_service._output.split("\n")) == 127


def test_parse_gflops_from_file():
    test_runner = TestHPCGRunner.from_string(summary)
    hpcg_service = HpcgService(test_runner)
    run = hpcg_service.run()

    assert run.gflops == 15.3024


summary = """HPCG-Benchmark
version=3.1
Release date=March 28, 2019
Machine Summary=
Machine Summary::Distributed Processes=64
Machine Summary::Threads per processes=1
Global Problem Dimensions=
Global Problem Dimensions::Global nx=416
Global Problem Dimensions::Global ny=416
Global Problem Dimensions::Global nz=416
Processor Dimensions=
Processor Dimensions::npx=4
Processor Dimensions::npy=4
Processor Dimensions::npz=4
Local Domain Dimensions=
Local Domain Dimensions::nx=104
Local Domain Dimensions::ny=104
Local Domain Dimensions::Lower ipz=0
Local Domain Dimensions::Upper ipz=3
Local Domain Dimensions::nz=104
########## Problem Summary  ##########=
Setup Information=
Setup Information::Setup Time=7.07119
Linear System Information=
Linear System Information::Number of Equations=71991296
Linear System Information::Number of Nonzero Terms=1934434936
Multigrid Information=
Multigrid Information::Number of coarse grid levels=3
Multigrid Information::Coarse Grids=
Multigrid Information::Coarse Grids::Grid Level=1
Multigrid Information::Coarse Grids::Number of Equations=8998912
Multigrid Information::Coarse Grids::Number of Nonzero Terms=240641848
Multigrid Information::Coarse Grids::Number of Presmoother Steps=1
Multigrid Information::Coarse Grids::Number of Postsmoother Steps=1
Multigrid Information::Coarse Grids::Grid Level=2
Multigrid Information::Coarse Grids::Number of Equations=1124864
Multigrid Information::Coarse Grids::Number of Nonzero Terms=29791000
Multigrid Information::Coarse Grids::Number of Presmoother Steps=1
Multigrid Information::Coarse Grids::Number of Postsmoother Steps=1
Multigrid Information::Coarse Grids::Grid Level=3
Multigrid Information::Coarse Grids::Number of Equations=140608
Multigrid Information::Coarse Grids::Number of Nonzero Terms=3652264
Multigrid Information::Coarse Grids::Number of Presmoother Steps=1
Multigrid Information::Coarse Grids::Number of Postsmoother Steps=1
########## Memory Use Summary  ##########=
Memory Use Information=
Memory Use Information::Total memory used for data (Gbytes)=51.4963
Memory Use Information::Memory used for OptimizeProblem data (Gbytes)=0
Memory Use Information::Bytes per equation (Total memory / Number of Equations)=715.313
Memory Use Information::Memory used for linear system and CG (Gbytes)=45.3161
Memory Use Information::Coarse Grids=
Memory Use Information::Coarse Grids::Grid Level=1
Memory Use Information::Coarse Grids::Memory used=5.41691
Memory Use Information::Coarse Grids::Grid Level=2
Memory Use Information::Coarse Grids::Memory used=0.678227
Memory Use Information::Coarse Grids::Grid Level=3
Memory Use Information::Coarse Grids::Memory used=0.0850727
########## V&V Testing Summary  ##########=
Spectral Convergence Tests=
Spectral Convergence Tests::Result=PASSED
Spectral Convergence Tests::Unpreconditioned=
Spectral Convergence Tests::Unpreconditioned::Maximum iteration count=11
Spectral Convergence Tests::Unpreconditioned::Expected iteration count=12
Spectral Convergence Tests::Preconditioned=
Spectral Convergence Tests::Preconditioned::Maximum iteration count=2
Spectral Convergence Tests::Preconditioned::Expected iteration count=2
Departure from Symmetry |x'Ay-y'Ax|/(2*||x||*||A||*||y||)/epsilon=
Departure from Symmetry |x'Ay-y'Ax|/(2*||x||*||A||*||y||)/epsilon::Result=PASSED
Departure from Symmetry |x'Ay-y'Ax|/(2*||x||*||A||*||y||)/epsilon::Departure for SpMV=2.97342e-10
Departure from Symmetry |x'Ay-y'Ax|/(2*||x||*||A||*||y||)/epsilon::Departure for MG=3.3165e-10
########## Iterations Summary  ##########=
Iteration Count Information=
Iteration Count Information::Result=PASSED
Iteration Count Information::Reference CG iterations per set=50
Iteration Count Information::Optimized CG iterations per set=50
Iteration Count Information::Total number of reference iterations=50
Iteration Count Information::Total number of optimized iterations=50
########## Reproducibility Summary  ##########=
Reproducibility Information=
Reproducibility Information::Result=PASSED
Reproducibility Information::Scaled residual mean=0.00435157
Reproducibility Information::Scaled residual variance=0
########## Performance Summary (times in sec) ##########=
Benchmark Time Summary=
Benchmark Time Summary::Optimization phase=9e-08
Benchmark Time Summary::DDOT=1.86118
Benchmark Time Summary::WAXPBY=2.01013
Benchmark Time Summary::SpMV=12.5437
Benchmark Time Summary::MG=70.6899
Benchmark Time Summary::Total=87.1193
Floating Point Operations Summary=
Floating Point Operations Summary::Raw DDOT=2.17414e+10
Floating Point Operations Summary::Raw WAXPBY=2.17414e+10
Floating Point Operations Summary::Raw SpMV=1.97312e+11
Floating Point Operations Summary::Raw MG=1.10316e+12
Floating Point Operations Summary::Total=1.34396e+12
Floating Point Operations Summary::Total with convergence overhead=1.34396e+12
GB/s Summary=
GB/s Summary::Raw Read B/W=95.027
GB/s Summary::Raw Write B/W=21.9599
GB/s Summary::Raw Total B/W=116.987
GB/s Summary::Total with convergence and optimization phase overhead=116.045
GFLOP/s Summary=
GFLOP/s Summary::Raw DDOT=11.6815
GFLOP/s Summary::Raw WAXPBY=10.8159
GFLOP/s Summary::Raw SpMV=15.73
GFLOP/s Summary::Raw MG=15.6057
GFLOP/s Summary::Raw Total=15.4266
GFLOP/s Summary::Total with convergence overhead=15.4266
GFLOP/s Summary::Total with convergence and optimization phase overhead=15.3024
User Optimization Overheads=
User Optimization Overheads::Optimization phase time (sec)=9e-08
User Optimization Overheads::Optimization phase time vs reference SpMV+MG time=5.39059e-08
DDOT Timing Variations=
DDOT Timing Variations::Min DDOT MPI_Allreduce time=0.258737
DDOT Timing Variations::Max DDOT MPI_Allreduce time=5.74576
DDOT Timing Variations::Avg DDOT MPI_Allreduce time=2.05643
Final Summary=
Final Summary::HPCG result is VALID with a GFLOP/s rating of=15.3024
Final Summary::HPCG 2.4 rating for historical reasons is=15.4266
Final Summary::Reference version of ComputeDotProduct used=Performance results are most likely suboptimal
Final Summary::Reference version of ComputeSPMV used=Performance results are most likely suboptimal
Final Summary::Reference version of ComputeMG used=Performance results are most likely suboptimal
Final Summary::Reference version of ComputeWAXPBY used=Performance results are most likely suboptimal
Final Summary::Results are valid but execution time (sec) is=87.1193
Final Summary::Official results execution time (sec) must be at least=1800
"""
