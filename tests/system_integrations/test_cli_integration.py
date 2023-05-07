from chronus.cli.setup import get_optimizer
from chronus.SystemIntegration.optimizers.bruteforce_optmizer import BruteForceOptimizer
from chronus.SystemIntegration.optimizers.linear_regression import LinearRegressionOptimizer
from chronus.SystemIntegration.optimizers.random_tree_forrest import RandomTreeOptimizer


def test_get_optimizer_linear_regression():
    # Arrange

    # Act
    optimizer = get_optimizer("linear-regression")

    # Assert
    assert isinstance(optimizer, LinearRegressionOptimizer)


def test_get_optimizer_brute_force():
    # Arrange

    # Act
    optimizer = get_optimizer("brute-force")

    # Assert
    assert isinstance(optimizer, BruteForceOptimizer)


def test_get_optimizer_random_tree():
    # Arrange

    # Act
    optimizer = get_optimizer("random-tree")

    # Assert
    assert isinstance(optimizer, RandomTreeOptimizer)
