import subprocess

import pytest

from chronus.SystemIntegration.cpu_info_service import LsCpuInfoService


# pytest fixture to mock the subprocess.run method
@pytest.fixture
def mock_subprocess_run(mocker):
    return mocker.patch.object(subprocess, "run", return_value=subprocess.CompletedProcess(args="lscpu", returncode=0,
                                                                                           stdout=ls_cpu_output))


def test_parses_model_number_cpu(mock_subprocess_run):
    # Arrange

    # Act
    cpu_info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert cpu_info.cpu == "AMD EPYC 7502P 32-Core Processor"


def test_no_model_number_cpu(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args="lscpu", returncode=0, stdout="")

    # Act
    cpu_info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert cpu_info.cpu == "Unknown"


def test_throws_exception_when_lscpu_fails(mock_subprocess_run):
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args="lscpu", returncode=1, stdout="")

    try:
        LsCpuInfoService().get_cpu_info()
    except Exception as e:
        assert e.args[0] == "Failed to run lscpu"


def test_get_cores(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args="lscpu", returncode=0, stdout=ls_cpu_output)
    expected_cores = 64

    # Act
    cores = LsCpuInfoService().get_cores()

    # Assert
    assert cores == expected_cores


def test_get_cores_throws_exception_when_lscpu_fails(mock_subprocess_run):
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args="lscpu", returncode=1, stdout="")

    try:
        LsCpuInfoService().get_cores()
    except Exception as e:
        assert e.args[0] == "Failed to run lscpu"


def test_get_cores_return_zero_when_no_cores_found(mock_subprocess_run):
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args="lscpu", returncode=0, stdout="")

    cores = LsCpuInfoService().get_cores()

    assert cores == 0


def test_get_frequencies(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args="cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies", returncode=0,
        stdout=cat_sys_devices_system_cpu_cpu_cpufreq_scaling_available_frequencies_output)
    expected_frequencies = [1_500_000, 2_200_000, 2_500_000]

    # Act
    frequencies = LsCpuInfoService().get_frequencies()

    # Assert
    assert frequencies == expected_frequencies


def test_get_frequencies_throws_exception_when_cat_fails(mock_subprocess_run):
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args="cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies", returncode=1, stdout="")

    try:
        LsCpuInfoService().get_frequencies()
    except Exception as e:
        assert e.args[0] == "Failed to read /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies"


def test_get_frequency_when_cores_have_different_frequencies(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args="cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies", returncode=0,
        stdout="1500000 2200000 2500000\n1600000 2200000 2500000")
    expected_frequencies = [2_200_000, 2_500_000]

    # Act
    frequencies = LsCpuInfoService().get_frequencies()

    # Assert
    assert frequencies == expected_frequencies


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

cat_sys_devices_system_cpu_cpu_cpufreq_scaling_available_frequencies_output = """2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000
2500000 2200000 1500000"""
