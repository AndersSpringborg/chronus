from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.SystemIntegration.optimizers.bruteforce_optmizer import BruteForceOptimizer
from chronus.SystemIntegration.optimizers.linear_regression import LinearRegressionOptimizer
from chronus.SystemIntegration.optimizers.random_tree_forrest import RandomTreeOptimizer


def get_optimizer(model_type: str) -> OptimizerInterface:
    print("model_type", model_type)
    print("LinearRegressionOptimizer.cpu_name", BruteForceOptimizer.name())
    if model_type == LinearRegressionOptimizer.name():
        return LinearRegressionOptimizer()
    elif model_type == BruteForceOptimizer.name():
        return BruteForceOptimizer()
    elif model_type == RandomTreeOptimizer.name():
        return RandomTreeOptimizer()
    else:
        raise Exception("Unknown optimizer type")
