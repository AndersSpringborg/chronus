import subprocess

import pytest

from chronus.SystemIntegration.hpcg import HpcgService
from tests.test_domain.fixtures import mock_subprocess_run

# 1. Find ud af hvordan jeg gerne vil kører hpcg -> hvordan skal hpcg.dat se ud
# 2. Hvordan får jeg hpcg til at kører det i en besstemt path
# ---- jeg vil gerne outputte i en makke 'hpcg_benchmark_output' i den mappe jeg er I, i mens jeg køer
# ---- Derefter slette mappen igen
# 3. Generere HPCG.DAT
# 4. Generer HPCG_BENCHMARK.SLURM
# Gem filerne i 'hpcg_benchmark_output'
# 5. Kør 'sbatch HPCG_BENCHMARK.SLURM' inde fra 'hpcg_benchmark_output'
# ---- returnere job id 'Submitted batch job 447'
# 6. Kør 'squeue -u <username>' og find ud af om der er en job der hedder 'hpcg_benchmark'
# 7. Find ud af om jobbet stadig kører med 'squeue -u <username>' og 'sacct -u <username>'
# 8. Hent output fra 'hpcg_benchmark_output' og gem det i 'hpcg_benchmark_output'
# 9. Parse outputtet og gem det i en database
# 10. Slet 'hpcg_benchmark_output' igen
# ---- Jeg ved at der kun er de filer, så jeg kan bare slette alt med HPCG i navnet
# 11. Gå til 1


@pytest.fixture
def make_file(tmpdir):
    def factory(file_name: str, content: str):
        file_name = tmpdir.join("hpcg_benchmark_output/" + file_name)
        with open(file_name, "w") as file:
            file.write(content)

    return factory


@pytest.fixture
def hpcg_service_temp_factory(tmpdir, mocker):
    mock_run = mocker.patch.object(
        subprocess,
        "run",
        return_value=subprocess.CompletedProcess(
            args="lscpu", returncode=0, stdout="Submitted batch job 449"
        ),
    )

    def factory():
        return HpcgService("/test/xhpcg", output_dir=str(tmpdir))

    return factory


def test_initiate_hpcg_service():
    app_runner = HpcgService("/test/xhpcg")

    assert app_runner is not None


def test_hpcg_makes_dir_running_folder(hpcg_service_temp_factory, tmpdir):
    # Arrange
    # Mock make dir call
    app_runner = hpcg_service_temp_factory()

    # Act
    app_runner.prepare()

    # Assert
    assert tmpdir.join("hpcg_benchmark_output").isdir()


def test_hpcg_makes_dat_file(hpcg_service_temp_factory, tmpdir):
    # Arrange
    # Mock make dir call
    app_runner = hpcg_service_temp_factory()

    # Act
    app_runner.prepare()

    # Assert
    assert tmpdir.join("hpcg_benchmark_output/hpcg.dat").isfile()


def test_hpcg_dat_file_contains_correct_content(hpcg_service_temp_factory, tmpdir):
    # Arrange
    # Mock make dir call
    app_runner = hpcg_service_temp_factory()

    # Act
    app_runner.prepare()

    # Assert
    assert tmpdir.join("hpcg_benchmark_output/hpcg.dat").read() == HPCG_DAT_FILE_CONTENT


def test_hpcg_makes_slurm_file(hpcg_service_temp_factory, tmpdir):
    # Arrange
    # Mock make dir call
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()

    # Act
    app_runner.run(cores=1, frequency=1)

    # Assert

    assert tmpdir.join("hpcg_benchmark_output/HPCG_BENCHMARK.slurm").isfile()


def test_hpcg_slurm_file_contains_correct_content(hpcg_service_temp_factory, tmpdir):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()

    # Act
    app_runner.run(cores=10, frequency=1_500_000)

    # Assert

    assert (
        tmpdir.join("hpcg_benchmark_output/HPCG_BENCHMARK.slurm").read() == HPCG_SLURM_FILE_CONTENT
    )


def test_hpcg_run_calls_sbatch(hpcg_service_temp_factory, tmpdir, mocker):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()

    # Act
    app_runner.run(cores=10, frequency=1_500_000)

    # Assert
    assert (
        mocker.call(
            ["sbatch", "HPCG_BENCHMARK.slurm"],
            cwd=str(tmpdir.join("hpcg_benchmark_output")),
            stdout=subprocess.PIPE,
        )
        in subprocess.run.call_args_list
    )


def test_hpcg_is_running_is_when_scontrol_running(hpcg_service_temp_factory, mock_subprocess_run):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()
    job_id = 449
    mocked_subprocess_run = mock_subprocess_run()
    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=f"Submitted batch job {job_id}"
    )

    # Act
    app_runner.run(cores=10, frequency=1_500_000)

    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=SCONTROL_IS_RUNNING_OUTPUT
    )
    is_running = app_runner.is_running()

    # Assert
    assert is_running is True
    mocked_subprocess_run.assert_called_with(
        ["scontrol", "show", "job", str(job_id)], stdout=subprocess.PIPE
    )


def test_hpcg_is_not_running_when_scontrol_completed(
    hpcg_service_temp_factory, mock_subprocess_run
):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()
    job_id = 449
    mocked_subprocess_run = mock_subprocess_run()
    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=f"Submitted batch job {job_id}"
    )

    # Act
    app_runner.run(cores=10, frequency=1_500_000)

    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=SCONTROL_IS_COMPLETED_OUTPUT
    )
    is_running = app_runner.is_running()

    # Assert
    assert is_running is False
    mocked_subprocess_run.assert_called_with(
        ["scontrol", "show", "job", str(job_id)], stdout=subprocess.PIPE
    )


def test_hpcg_is_getting_the_job_id_from_scontrol(hpcg_service_temp_factory, mock_subprocess_run):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()
    job_id = 300
    mocked_subprocess_run = mock_subprocess_run()
    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=f"Submitted batch job {job_id}"
    )

    # Act
    app_runner.run(cores=10, frequency=1_500_000)
    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=SCONTROL_IS_COMPLETED_OUTPUT
    )
    app_runner.is_running()

    # Assert
    mocked_subprocess_run.assert_called_with(
        ["scontrol", "show", "job", str(job_id)], stdout=subprocess.PIPE
    )


def test_hpcg_gives_correct_result_when_scontrol_completed(
    hpcg_service_temp_factory, mock_subprocess_run, make_file
):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()
    job_id = 449
    mocked_subprocess_run = mock_subprocess_run()
    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=f"Submitted batch job {job_id}"
    )
    make_file("hpcg20230424T041652.txt", HPCG_LOG)
    make_file("HPCG-Benchmark_3.1_2023-04-24_04-16-52.txt", HPCG_OUTPUT)

    # Act
    app_runner.run(cores=10, frequency=1_500_000)
    # Fake is finished running
    mocked_subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=SCONTROL_IS_COMPLETED_OUTPUT
    )

    # Assert
    assert app_runner.gflops == 1.51085


@pytest.mark.parametrize(
    ("gflops"),
    [
        0.0,
        15.3024,
        123456.123456,
    ],
)
def test_parse_gflops(gflops, hpcg_service_temp_factory, mock_subprocess_run, make_file):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()

    make_file("hpcg20230424T041652.txt", HPCG_LOG)
    make_file(
        "HPCG-Benchmark_3.1_2023-04-24_04-16-52.txt",
        f"Final Summary::HPCG result is VALID with a GFLOP/s rating of={gflops}",
    )

    # Act
    gflops_from_app_runner = app_runner.gflops

    # Assert
    assert gflops_from_app_runner == gflops


def test_files_are_deleted_after_is_running_is_returning_false(
    hpcg_service_temp_factory, tmpdir, mock_subprocess_run, make_file
):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()

    # Act
    app_runner.cleanup()

    # Assert
    assert not tmpdir.join("hpcg_benchmark_output").isdir()


def test_if_dir_exists_throw_error(
    hpcg_service_temp_factory, tmpdir, mock_subprocess_run, make_file
):
    # Arrange
    app_runner = hpcg_service_temp_factory()
    app_runner.prepare()
    # tmpdir.mkdir("hpcg_benchmark_output")
    # Act
    with pytest.raises(FileExistsError):
        app_runner.prepare()

    # Assert
    assert tmpdir.join("hpcg_benchmark_output").isdir()


HPCG_DAT_FILE_CONTENT = """HPCG benchmark input file
Benchmarked on 2020-11-24 14:00:00
104 104 104
900"""

HPCG_SLURM_FILE_CONTENT = """#!/bin/bash
#SBATCH --job-name=HPCG_BENCHMARK
#SBATCH --output=HPCG_BENCHMARK.out
#SBATCH --error=HPCG_BENCHMARK.err
#SBATCH --ntasks=10
#SBATCH --cpu-freq=1500000

srun --mpi=pmix_v4 /test/xhpcg"""

SCONTROL_IS_RUNNING_OUTPUT = b"""JobId=450 JobName=RUN_CPU.slurm
   UserId=aaen(1000) GroupId=aaen(1000) MCS_label=N/A
   Priority=4294901754 Nice=0 Account=(null) QOS=(null)
   JobState=RUNNING Reason=None Dependency=(null)
   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
   RunTime=00:00:52 TimeLimit=01:00:00 TimeMin=N/A
   SubmitTime=2023-04-24T08:20:30 EligibleTime=2023-04-24T08:20:30
   AccrueTime=2023-04-24T08:20:30
   StartTime=2023-04-24T08:20:31 EndTime=2023-04-24T09:20:31 Deadline=N/A
   SuspendTime=None SecsPreSuspend=0 LastSchedEval=2023-04-24T08:20:31 Scheduler=Backfill
   Partition=debug AllocNode:Sid=host114:46562
   ReqNodeList=(null) ExcNodeList=(null)
   NodeList=host114.grid.aau.dk
   BatchHost=host114.grid.aau.dk
   NumNodes=1 NumCPUs=2 NumTasks=2 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
   TRES=cpu=2,mem=257393M,node=1,billing=2
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=1 MinMemoryNode=0 MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null)
   Command=./RUN_CPU.slurm
   WorkDir=/home/aaen/slurm-chronus
   StdErr=/home/aaen/slurm-chronus/out/cpu-info.err
   StdIn=/dev/null
   StdOut=/home/aaen/slurm-chronus/out/cpu-info.out
   CPU_min_freq=2200000 CPU_max_freq=2200000
   Power=

                              """
SCONTROL_IS_COMPLETED_OUTPUT = b"""JobId=450 JobName=RUN_CPU.slurm
   UserId=aaen(1000) GroupId=aaen(1000) MCS_label=N/A
   Priority=4294901754 Nice=0 Account=(null) QOS=(null)
   JobState=COMPLETED Reason=None Dependency=(null)
   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
   RunTime=00:01:43 TimeLimit=01:00:00 TimeMin=N/A
   SubmitTime=2023-04-24T08:20:30 EligibleTime=2023-04-24T08:20:30
   AccrueTime=2023-04-24T08:20:30
   StartTime=2023-04-24T08:20:31 EndTime=2023-04-24T08:22:14 Deadline=N/A
   SuspendTime=None SecsPreSuspend=0 LastSchedEval=2023-04-24T08:20:31 Scheduler=Backfill
   Partition=debug AllocNode:Sid=host114:46562
   ReqNodeList=(null) ExcNodeList=(null)
   NodeList=host114.grid.aau.dk
   BatchHost=host114.grid.aau.dk
   NumNodes=1 NumCPUs=2 NumTasks=2 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
   TRES=cpu=2,mem=257393M,node=1,billing=2
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=1 MinMemoryNode=0 MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null)
   Command=./RUN_CPU.slurm
   WorkDir=/home/aaen/slurm-chronus
   StdErr=/home/aaen/slurm-chronus/out/cpu-info.err
   StdIn=/dev/null
   StdOut=/home/aaen/slurm-chronus/out/cpu-info.out
   CPU_min_freq=2200000 CPU_max_freq=2200000
   Power=

"""

HPCG_LOG = """WARNING: PERFORMING UNPRECONDITIONED ITERATIONS
Call [0] Number of Iterations [11] Scaled Residual [2.71587e-14]
WARNING: PERFORMING UNPRECONDITIONED ITERATIONS
Call [1] Number of Iterations [11] Scaled Residual [2.71587e-14]
Call [0] Number of Iterations [2] Scaled Residual [3.19854e-17]
Call [1] Number of Iterations [2] Scaled Residual [3.19854e-17]
Departure from symmetry (scaled) for SpMV abs(x'*A*y - y'*A*x) = 1.39376e-05
Departure from symmetry (scaled) for MG abs(x'*Minv*y - y'*Minv*x) = 4.35551e-07
SpMV call [0] Residual [0]
SpMV call [1] Residual [0]
Call [0] Scaled Residual [7.53688e-32]"""

HPCG_OUTPUT = """HPCG-Benchmark
version=3.1
Release date=March 28, 2019
Machine Summary=
Machine Summary::Distributed Processes=2
Machine Summary::Threads per processes=1
Global Problem Dimensions=
Global Problem Dimensions::Global nx=32
Global Problem Dimensions::Global ny=16
Global Problem Dimensions::Global nz=16
Processor Dimensions=
Processor Dimensions::npx=2
Processor Dimensions::npy=1
Processor Dimensions::npz=1
Local Domain Dimensions=
Local Domain Dimensions::nx=16
Local Domain Dimensions::ny=16
Local Domain Dimensions::Lower ipz=0
Local Domain Dimensions::Upper ipz=0
Local Domain Dimensions::nz=16
########## Problem Summary  ##########=
Setup Information=
Setup Information::Setup Time=0.0280216
Linear System Information=
Linear System Information::Number of Equations=8192
Linear System Information::Number of Nonzero Terms=198904
Multigrid Information=
Multigrid Information::Number of coarse grid levels=3
Multigrid Information::Coarse Grids=
Multigrid Information::Coarse Grids::Grid Level=1
Multigrid Information::Coarse Grids::Number of Equations=1024
Multigrid Information::Coarse Grids::Number of Nonzero Terms=22264
Multigrid Information::Coarse Grids::Number of Presmoother Steps=1
Multigrid Information::Coarse Grids::Number of Postsmoother Steps=1
Multigrid Information::Coarse Grids::Grid Level=2
Multigrid Information::Coarse Grids::Number of Equations=128
Multigrid Information::Coarse Grids::Number of Nonzero Terms=2200
Multigrid Information::Coarse Grids::Number of Presmoother Steps=1
Multigrid Information::Coarse Grids::Number of Postsmoother Steps=1
Multigrid Information::Coarse Grids::Grid Level=3
Multigrid Information::Coarse Grids::Number of Equations=16
Multigrid Information::Coarse Grids::Number of Nonzero Terms=160
Multigrid Information::Coarse Grids::Number of Presmoother Steps=1
Multigrid Information::Coarse Grids::Number of Postsmoother Steps=1
########## Memory Use Summary  ##########=
Memory Use Information=
Memory Use Information::Total memory used for data (Gbytes)=0.0058683
Memory Use Information::Memory used for OptimizeProblem data (Gbytes)=0
Memory Use Information::Bytes per equation (Total memory / Number of Equations)=716.345
Memory Use Information::Memory used for linear system and CG (Gbytes)=0.0051611
Memory Use Information::Coarse Grids=
Memory Use Information::Coarse Grids::Grid Level=1
Memory Use Information::Coarse Grids::Memory used=0.000618752
Memory Use Information::Coarse Grids::Grid Level=2
Memory Use Information::Coarse Grids::Memory used=7.8144e-05
Memory Use Information::Coarse Grids::Grid Level=3
Memory Use Information::Coarse Grids::Memory used=1.0304e-05
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
Departure from Symmetry |x'Ay-y'Ax|/(2*||x||*||A||*||y||)/epsilon::Departure for SpMV=1.39376e-05
Departure from Symmetry |x'Ay-y'Ax|/(2*||x||*||A||*||y||)/epsilon::Departure for MG=4.35551e-07
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
Reproducibility Information::Scaled residual mean=7.53688e-32
Reproducibility Information::Scaled residual variance=0
########## Performance Summary (times in sec) ##########=
Benchmark Time Summary=
Benchmark Time Summary::Optimization phase=2.5e-07
Benchmark Time Summary::DDOT=0.00151852
Benchmark Time Summary::WAXPBY=0.00104237
Benchmark Time Summary::SpMV=0.0160683
Benchmark Time Summary::MG=0.069181
Benchmark Time Summary::Total=0.0878437
Floating Point Operations Summary=
Floating Point Operations Summary::Raw DDOT=2.47398e+06
Floating Point Operations Summary::Raw WAXPBY=2.47398e+06
Floating Point Operations Summary::Raw SpMV=2.02882e+07
Floating Point Operations Summary::Raw MG=1.11716e+08
Floating Point Operations Summary::Total=1.36952e+08
Floating Point Operations Summary::Total with convergence overhead=1.36952e+08
GB/s Summary=
GB/s Summary::Raw Read B/W=9.63268
GB/s Summary::Raw Write B/W=2.22757
GB/s Summary::Raw Total B/W=11.8602
GB/s Summary::Total with convergence and optimization phase overhead=11.4936
GFLOP/s Summary=
GFLOP/s Summary::Raw DDOT=1.6292
GFLOP/s Summary::Raw WAXPBY=2.37342
GFLOP/s Summary::Raw SpMV=1.26262
GFLOP/s Summary::Raw MG=1.61484
GFLOP/s Summary::Raw Total=1.55904
GFLOP/s Summary::Total with convergence overhead=1.55904
GFLOP/s Summary::Total with convergence and optimization phase overhead=1.51085
User Optimization Overheads=
User Optimization Overheads::Optimization phase time (sec)=2.5e-07
User Optimization Overheads::Optimization phase time vs reference SpMV+MG time=0.000136308
DDOT Timing Variations=
DDOT Timing Variations::Min DDOT MPI_Allreduce time=0.000313095
DDOT Timing Variations::Max DDOT MPI_Allreduce time=0.000478965
DDOT Timing Variations::Avg DDOT MPI_Allreduce time=0.00039603
Final Summary=
Final Summary::HPCG result is VALID with a GFLOP/s rating of=1.51085
Final Summary::HPCG 2.4 rating for historical reasons is=1.55904
Final Summary::Reference version of ComputeDotProduct used=Performance results are most likely suboptimal
Final Summary::Reference version of ComputeSPMV used=Performance results are most likely suboptimal
Final Summary::Reference version of ComputeMG used=Performance results are most likely suboptimal
Final Summary::Reference version of ComputeWAXPBY used=Performance results are most likely suboptimal
Final Summary::Results are valid but execution time (sec) is=0.0878437
Final Summary::You have selected the QuickPath option=Results are official for legacy installed systems with confirmation from the HPCG Benchmark leaders.
Final Summary::After confirmation please upload results from the YAML file contents to=http://hpcg-benchmark.org"""
