import subprocess
from datetime import datetime

import pytest

from chronus.domain.benchmark import Benchmark
from chronus.domain.cpu_info import CpuInfo
from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample


@pytest.fixture
def mock_subprocess_run(mocker):
    mocked_subprocess_run = mocker.patch.object(
        subprocess,
        "run",
        return_value=subprocess.CompletedProcess(args="lscpu", returncode=0, stdout=ls_cpu_output),
    )

    def get_mock():
        return mocked_subprocess_run

    return get_mock


ls_cpu_output = """Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              64
On-line CPU(s) list: 0-63
Thread(s) per core:  2
Core(s) per socket:  32
Socket(s):           1
NUMA node(s):        1
Vendor ID:           AuthenticAMD
CPU family:          23
Model:               49
Model name:          AMD EPYC 7502P 32-Core Processor
Stepping:            0
CPU MHz:             2500.000
CPU max MHz:         2500.0000
CPU min MHz:         1500.0000
BogoMIPS:            4990.86
Virtualization:      AMD-V
L1d cache:           32K
L1i cache:           32K
L2 cache:            512K
L3 cache:            16384K
NUMA node0 CPU(s):   0-63
Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid aperfmperf pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpb cat_l3 cdp_l3 hw_pstate ssbd mba ibrs ibpb stibp vmmcall fsgsbase bmi1 avx2 smep bmi2 cqm rdt_a rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local clzero irperf xsaveerptr wbnoinvd arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold avic v_vmsave_vmload vgif v_spec_ctrl umip rdpid overflow_recov succor smca sme sev sev_es
"""


class FakeCpuInfoService(CpuInfoServiceInterface):
    def __init__(self, cores=4, frequencies=None):
        if frequencies is None:
            frequencies = [1.0, 2.0, 3.0]
        self.cores = cores
        self.frequencies = frequencies

    def get_cpu_info(self) -> CpuInfo:
        return CpuInfo(
            name="Fake CPU", cores=self.cores, frequencies=self.frequencies, threads_per_core=1
        )


class FakeSystemService(SystemServiceInterface):
    def __init__(self, power_draw=1.0):
        self.power_draw = power_draw

    def sample(self) -> SystemSample:
        return SystemSample(timestamp=datetime.now(), current_power_draw=self.power_draw)


class FakeApplication(ApplicationRunnerInterface):
    def run(self, cores: int, frequency: float, thread_per_core=1):
        pass

    def __init__(self, seconds: int = None, result: float = None, gflops: float = None):
        self.seconds = seconds or 0
        self.__counter = 0
        self.gflops = gflops or 10.0
        self.result = result or 100.0
        self.cleanup_called = 0
        self.prepare_called = 0

    def prepare(self):
        self.prepare_called += 1

    def cleanup(self):
        self.cleanup_called += 1

    def is_running(self) -> bool:
        is_running = self.__counter < self.seconds
        self.__counter += 1

        return is_running


class FakeBencmarkRepository(RepositoryInterface):
    called_save_run = 0
    runs: list[Run]

    called_save_benchmark = 0
    benchmarks: list[Benchmark]

    def __init__(self, benchmark: Benchmark = None):
        self.runs = []
        self.benchmarks = []
        self._benchmark = benchmark

    def save_run(self, run: Run) -> None:
        self.called_save_run += 1
        self.runs.append(run)

    def save_benchmark(self, benchmark: Benchmark) -> int:
        self.called_save_benchmark += 1
        self.benchmarks.append(benchmark)
        if self._benchmark is not None:
            return self._benchmark.id
        return benchmark.id
