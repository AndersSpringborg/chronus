import subprocess

import pytest


@pytest.fixture
def mock_subprocess_run(mocker):
    mocked_subprocess_run = mocker.patch.object(
        subprocess,
        "run",
        return_value=subprocess.CompletedProcess(args="lscpu", returncode=0, stdout=""),
    )

    def get_mock():
        return mocked_subprocess_run

    return get_mock
