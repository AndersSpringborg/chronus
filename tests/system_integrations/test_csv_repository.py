import freezegun
import pytest

from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample
from chronus.SystemIntegration.csv_repository import CsvRunRepository
from tests.fixtures import datetime_from_string

HEADERS = "cpu,cores,frequency,gflops,gflop,energy_used,gflops_per_watt,start_time,end_time\n"


@pytest.fixture
def csv_file(tmp_path):
    return tmp_path / "test.csv"


def test_headers_are_written_on_create(csv_file):
    # Arrange
    repo = CsvRunRepository(csv_file)
    # Act

    # Assert
    assert csv_file.exists()
    assert csv_file.read_text() == HEADERS


def test_if_file_exists_move_it_to_backup(csv_file):
    # Arrange
    csv_file.write_text("test")
    repo = CsvRunRepository(csv_file)
    # Act

    # Assert
    assert csv_file.exists()
    assert csv_file.read_text() == HEADERS
    assert (csv_file.parent / "test.csv.bak").exists()
    assert (csv_file.parent / "test.csv.bak").read_text() == "test"


@freezegun.freeze_time("2020-01-01 00:00:1")
def test_save_run(csv_file):
    # Arrange
    repo = CsvRunRepository(csv_file)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e+8)
    run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:1"), current_power_draw=10.0)
    )
    run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:2"), current_power_draw=10.0)
    )
    run.finish(datetime_from_string("2020-01-01 00:00:02"))

    # Act
    repo.save(run)

    # Assert
    # cpu=test, cores=2, frequency=1.5, gflops=30.0, flop=30.0+8 energy_used=10.0, gflops_per_watt=3.0
    assert (
        csv_file.read_text()
        == HEADERS + "test,2,1.5,30.0,30.0,10.0,3.0,2020-01-01 00:00:01,2020-01-01 00:00:02\n"
    )
