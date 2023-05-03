from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.Run import Run


class BruteForceOptimizer(OptimizerInterface):
    def make_model(self, runs: list[Run]) -> None:
        best_run = None
        best_efficiency = 0.0

        for run in runs:
            efficiency = energy_efficiency(run)
            if efficiency > best_efficiency:
                best_efficiency = efficiency
                best_run = run

        # print("Best configuration:")
        # print(f"Cores: {best_run.cores}")
        # print(f"Threads per core: {best_run.threads_per_core}")
        # print(f"Frequency: {best_run.frequency} Hz")
        # print(f"Energy efficiency: {best_efficiency} GFLOPS/Watt")


def energy_efficiency(run: Run) -> float:
    return run.gflops_per_watt
