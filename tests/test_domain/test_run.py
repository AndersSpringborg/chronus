from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample
from tests.fixtures import create_datatime_with_seconds


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


def test_run_calculates_gflops_per_watt():
    # Arrange
    run = Run()

    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(0), current_power_draw=10.0))
    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(1), current_power_draw=10.0))
    run.gflops = 100.0

    # Act
    gflops_per_watt = run.gflops_per_watt

    # Assert
    assert gflops_per_watt == 10.0

def test_run_calculates_gflops_per_watt_with_fluctuated_power_draw():
    # Arrange
    run = Run()

    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(0), current_power_draw=10.0))
    run.add_sample(SystemSample(timestamp=create_datatime_with_seconds(1), current_power_draw=20.0))
    run.gflops = 15.0

    # Act
    gflops_per_watt = run.gflops_per_watt

    # Assert
    assert gflops_per_watt == 1.0

