from datetime import datetime

from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample


def create_datatime_with_seconds(seconds):
    return datetime(year=2020, month=1, day=1, hour=0, minute=0, second=seconds)


def test_run_calculate_energy_used():
    # Arrange
    run = Run()

    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(0), current_power_draw=10.0))
    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(1), current_power_draw=10.0))

    # Act
    energy_used = run.energy_used_joules

    # Assert
    assert energy_used == 10.0


def test_run_calculate_energy_used_with_2_seconds():
    # Arrange
    run = Run()

    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(0), current_power_draw=10.0))
    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(2), current_power_draw=10.0))

    # Act
    energy_used = run.energy_used_joules

    # Assert
    assert energy_used == 20.0


def test_run_calculate_energy_used_with_2_seconds_and_different_power_draw():
    # Arrange
    run = Run()

    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(0), current_power_draw=10.0))
    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(2), current_power_draw=20.0))

    # Act
    energy_used = run.energy_used_joules

    # Assert
    assert energy_used == 30.0


def test_run_calculate_energy_one_sample_return_zero():
    # Arrange
    run = Run()

    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(0), current_power_draw=10.0))

    # Act
    energy_used = run.energy_used_joules

    # Assert
    assert energy_used == 0.0


def create_datatime_with_seconds(seconds):
    return datetime(year=2020, month=1, day=1, hour=0, minute=0, second=seconds)
