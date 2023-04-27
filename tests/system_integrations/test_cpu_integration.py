import subprocess

import pytest

from chronus.SystemIntegration.cpu_info_service import LsCpuInfoService
from tests.test_domain.fixtures import mock_subprocess_run, ls_cpu_output


@pytest.fixture
def mock_system_calls(mocker):
    mocked_lscpu = mocker.patch.object(
        subprocess,
        "run",
        return_value=subprocess.CompletedProcess(args="lscpu", returncode=0, stdout=ls_cpu_output),
    )

    mocked_etc_release_data = mocker.mock_open(read_data="2500000 2200000 1500000 \n")
    mocked_frequency_file = mocker.patch("builtins.open", mocked_etc_release_data)

    def get_mock(choice):
        if choice == "lscpu":
            return mocked_lscpu
        elif choice == "frequency_file":
            return mocked_frequency_file

    return get_mock


def test_parses_model_number_cpu(mock_system_calls):
    # Arrange

    # Act
    cpu_info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert cpu_info.cpu == "AMD EPYC 7502P 32-Core Processor"


def test_no_model_number_cpu(mock_system_calls):
    # Arrange
    mock_system_calls("lscpu").return_value = subprocess.CompletedProcess(
        args="lscpu", returncode=0, stdout=""
    )

    # Act
    cpu_info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert cpu_info.cpu == "Unknown"


def test_throws_exception_when_lscpu_fails(mock_system_calls):
    mock_system_calls("lscpu").return_value = subprocess.CompletedProcess(
        args="lscpu", returncode=1, stdout="", stderr="Not found"
    )

    with pytest.raises(Exception) as exc_info:
        LsCpuInfoService().get_cpu_info()
    assert exc_info.value.args[0] == "Failed to run lscpu: Not found"


def test_get_cores(mock_system_calls):
    # Arrange
    expected_cores = 32

    # Act
    info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert info.cores == expected_cores


def test_get_cores_return_zero_when_no_cores_found(mock_system_calls):
    mock_system_calls("lscpu").return_value = subprocess.CompletedProcess(
        args="lscpu", returncode=0, stdout=""
    )

    info = LsCpuInfoService().get_cpu_info()

    assert info.cores == 0


def test_get_frequencies(mock_system_calls):
    # Arrange
    expected_frequencies = [1_500_000, 2_200_000, 2_500_000]

    # Act
    info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert info.frequencies == expected_frequencies


def test_get_frequencies_throws_exception_when_cat_fails(mocker):
    mocker.patch("builtins.open", side_effect=IOError("Failed to open file"))
    try:
        LsCpuInfoService()._get_frequencies()
    except Exception as e:
        assert (
            e.args[0]
            == "Failed to read /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies"
        )


def test_get_threads_per_core(mock_system_calls):
    # Arrange
    expected_threads_per_core = 2

    # Act
    info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert info.threads_per_core == expected_threads_per_core
