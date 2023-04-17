import io
import os
from os import remove

import pytest

from chronus.model.Run import Run
from chronus.SystemIntegration.FileRepository import FileRepository


@pytest.fixture
def file_for_testing():
    yield
    """Clean up the test file."""
    if os.path.exists("test.json"):
        remove("test.json")


def test_run_is_serialized_to_json_in_file(file_for_testing):
    """Test that the run is serialized to json in the file."""
    # Arrange
    file_repository = FileRepository("test.json")

    # Act
    file_repository.save(Run())

    # Assert
    file_output = open("test.json").read()
    assert (
        '{"fan_speed_rpm": 0, "cpu_temp_c": 0.0, "cpu_cores": 0, "cpu_clock": 0.0, "cpu_load": 0.0, "gflops": 0.0, "watts": 0.0}'
        in file_output
    )


def test_multiple_runs_is_serialized_to_json(file_for_testing):
    """Test that multiple runs are serialized to json."""
    # Arrange
    file_repository = FileRepository("test.json")

    # Act
    file_repository.save(Run())
    file_repository.save(Run())

    # Assert
    file_output = open("test.json").read()
    run_as_json = '{"fan_speed_rpm": 0, "cpu_temp_c": 0.0, "cpu_cores": 0, "cpu_clock": 0.0, "cpu_load": 0.0, "gflops": 0.0, "watts": 0.0}'

    assert file_output == f"[{run_as_json},{run_as_json}]"


def test_file_is_created_if_not_exists(file_for_testing):
    """Test that the file is created if it does not exist."""
    # Arrange
    file_repository = FileRepository("test.json")

    # Act
    file_repository.save(Run())

    # Assert
    assert os.path.exists("test.json")


def test_file_is_created(file_for_testing):
    """Test that the file is not created if it exists."""
    # Arrange
    file_repository = FileRepository("test.json")

    # Act
    file_repository.save(Run())

    # Assert
    assert os.path.exists("test.json")


def test_throw_exception_if_file_already_exists(file_for_testing):
    """Test that the file is not created if it exists."""
    # Arrange
    open("test.json", "w").close()

    # Act
    # Assert
    with pytest.raises(FileExistsError):
        FileRepository("test.json")
