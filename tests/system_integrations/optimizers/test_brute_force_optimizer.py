from chronus.domain.configuration import Configuration
from chronus.domain.cpu_info import SystemInfo
from chronus.domain.Run import Run
from chronus.SystemIntegration.optimizers.bruteforce_optmizer import BruteForceOptimizer


def test_saves_and_loads_the_values_from_file(tmp_path):
    # Arrange
    run = Run(cores=1, threads_per_core=1, frequency=1, gflops=1)
    run.__gflops_per_watt = 1.0
    runs = [run]
    expected_best_run = Configuration(cores=1, threads_per_core=1, frequency=1)
    optimizer = BruteForceOptimizer()
    optimizer.make_model(runs)
    system = SystemInfo(cores=1, threads_per_core=1, frequencies=[1])
    path = str(tmp_path / str(hash(system)))
    path_local_model = str(tmp_path / "local_model")

    # Act
    optimizer.save(path)
    optimizer.load(path, path_local_model)
    best_run = optimizer.run(path_local_model)

    # Assert
    assert best_run == expected_best_run
