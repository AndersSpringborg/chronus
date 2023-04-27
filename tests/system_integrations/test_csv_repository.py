import datetime

import pytest

from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample
from chronus.SystemIntegration.csv_repository import CsvRunRepository


@pytest.fixture
def csv_file(tmp_path):
    return tmp_path / "test.csv"


def test_headers_are_written_on_create(csv_file):
    # Arrange
    repo = CsvRunRepository(csv_file)
    # Act

    # Assert
    assert csv_file.exists()
    assert csv_file.read_text() == "cpu,cores,frequency,gflops,energy_used\n"


def test_if_file_exists_move_it_to_backup(csv_file):
    # Arrange
    csv_file.write_text("test")
    repo = CsvRunRepository(csv_file)
    # Act

    # Assert
    assert csv_file.exists()
    assert csv_file.read_text() == "cpu,cores,frequency,gflops,energy_used\n"
    assert (csv_file.parent / "test.csv.bak").exists()
    assert (csv_file.parent / "test.csv.bak").read_text() == "test"


def test_save_run(csv_file):
    # Arrange
    repo = CsvRunRepository(csv_file)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=3.0)
    run.add_sample(
        SystemSample(timestamp=datetime.datetime(2021, 1, 1, 1, 1, 1), current_power_draw=1.2)
    )
    run.add_sample(
        SystemSample(timestamp=datetime.datetime(2021, 1, 1, 1, 1, 2), current_power_draw=1.2)
    )

    # Act
    repo.save(run)

    # Assert
    assert csv_file.read_text() == "cpu,cores,frequency,gflops,energy_used\ntest,2,1.5,3.0,1.2\n"
