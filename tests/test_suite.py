from typing import List

from chronus.__main__ import StandardConfig, Suite
from chronus.model.Run import Run
from chronus.SystemIntegration.repository import Repository


class TestRepository(Repository):
    saved_runs: list[Run]

    def __init__(self):
        super().__init__()
        self.saved_runs = []

    def save(self, run: Run):
        self.saved_runs.append(run)


def test_suite_runs_over_all_configurations(mocker):
    """Test that the suite runs over all configurations."""
    # Arrange
    suite = Suite("bin/xhpcg", TestRepository())
    hpcg_run = mocker.spy(suite.hpcg, "run")

    # Act
    suite.run()

    # Assert
    assert hpcg_run.call_count == 2


def test_suite_saves_run_in_between_files(mocker):
    """Test that the suite saves a run in between files."""
    # Arrange
    suite = Suite("bin/xhpcg", TestRepository())
    save_function = mocker.patch.object(suite._repository, "save")

    # Act
    suite.run()

    # Assert
    assert save_function.call_count == 2
