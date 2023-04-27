import subprocess

import pytest

from chronus.SystemIntegration.cpu_info_service import LsCpuInfoService
from tests.test_domain.fixtures import mock_subprocess_run

# pytest fixture to mock the subprocess.run method


@pytest.fixture
def mock_frequency_file(mocker):
    # Read a mocked /etc/release file
    mocked_etc_release_data = mocker.mock_open(read_data="2500000 2200000 1500000 \n")
    mocker.patch("builtins.open", mocked_etc_release_data)


def test_parses_model_number_cpu(mock_subprocess_run):
    # Arrange

    # Act
    cpu_info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert cpu_info.cpu == "AMD EPYC 7502P 32-Core Processor"


def test_no_model_number_cpu(mock_subprocess_run):
    # Arrange
    mock_subprocess_run().return_value = subprocess.CompletedProcess(
        args="lscpu", returncode=0, stdout=""
    )

    # Act
    cpu_info = LsCpuInfoService().get_cpu_info()

    # Assert
    assert cpu_info.cpu == "Unknown"


def test_throws_exception_when_lscpu_fails(mock_subprocess_run):
    mock_subprocess_run().return_value = subprocess.CompletedProcess(
        args="lscpu", returncode=1, stdout="", stderr="Not found"
    )

    with pytest.raises(Exception) as exc_info:
        LsCpuInfoService().get_cpu_info()
    assert exc_info.value.args[0] == "Failed to run lscpu: Not found"


def test_get_cores(mock_subprocess_run):
    # Arrange
    expected_cores = 64

    # Act
    cores = LsCpuInfoService().get_cores()

    # Assert
    assert cores == expected_cores


def test_get_cores_throws_exception_when_lscpu_fails(mock_subprocess_run):
    mock_subprocess_run().return_value = subprocess.CompletedProcess(
        args="lscpu", returncode=1, stdout="", stderr="Not found"
    )

    with pytest.raises(Exception) as exc_info:
        LsCpuInfoService().get_cores()
    assert exc_info.value.args[0] == "Failed to run lscpu: Not found"


def test_get_cores_return_zero_when_no_cores_found(mock_subprocess_run):
    mock_subprocess_run().return_value = subprocess.CompletedProcess(
        args="lscpu", returncode=0, stdout=""
    )

    cores = LsCpuInfoService().get_cores()

    assert cores == 0


def test_get_frequencies(mock_frequency_file):
    # Arrange
    expected_frequencies = [1_500_000, 2_200_000, 2_500_000]

    # Act
    frequencies = LsCpuInfoService().get_frequencies()

    # Assert
    assert frequencies == expected_frequencies


def test_get_frequencies_throws_exception_when_cat_fails(mocker):
    mocker.patch("builtins.open", side_effect=IOError("Failed to open file"))
    try:
        LsCpuInfoService().get_frequencies()
    except Exception as e:
        assert (
            e.args[0]
            == "Failed to read /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies"
        )


def xtest_get_frequency_when_cores_have_different_frequencies(mock_frequency_file):
    # Arrange
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args="cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies",
        returncode=0,
        stdout="1500000 2200000 2500000\n1600000 2200000 2500000",
    )
    expected_frequencies = [2_200_000, 2_500_000]

    # Act
    frequencies = LsCpuInfoService().get_frequencies()

    # Assert
    assert frequencies == expected_frequencies
