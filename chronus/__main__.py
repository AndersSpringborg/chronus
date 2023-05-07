import json
import logging
import os
from enum import Enum
from random import choice
from time import sleep

import typer
from rich.console import Console
from rich.logging import RichHandler

from chronus import version
from chronus.application.benchmark_service import BenchmarkService
from chronus.application.init_model_service import InitModelService
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.SystemIntegration.application_runners.hpcg import HpcgService
from chronus.SystemIntegration.cpu_info_services.cpu_info_service import LsCpuInfoService
from chronus.SystemIntegration.optimizers.bruteforce_optmizer import BruteForceOptimizer
from chronus.SystemIntegration.optimizers.linear_regression import LinearRegressionOptimizer
from chronus.SystemIntegration.optimizers.random_tree_forrest import RandomTreeOptimizer
from chronus.SystemIntegration.repositories.sqlite_repository import SqliteRepository
from chronus.SystemIntegration.system_service_interfaces.ipmi_system_service import (
    IpmiSystemService,
)

name = "chronus"


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


console = Console()
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(console=console)]
)

app = typer.Typer(
    name=name,
    help="A energy scheduling model, build for HPC.",
    add_completion=True,
)


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    version_string = (
        "\x1B[38;2;63;81;177mc\x1B[39m\x1B[38;2;90;85;174mh\x1B[39m\x1B[38;2;123;95;172mr\x1B[39m\x1B["
        "38;2;133;101;173mo\x1B[39m\x1B[38;2;143;106;174mn\x1B[39m\x1B[38;2;156;106;169mu\x1B[39m\x1B["
        "38;2;168;106;164ms\x1B[39m \x1B[38;2;186;107;153mv\x1B[39m\x1B[38;2;204;107;142me\x1B[39m\x1B["
        "38;2;223;119;128mr\x1B[39m\x1B[38;2;241;130;113ms\x1B[39m\x1B[38;2;242;147;109mi\x1B[39m\x1B["
        "38;2;243;164;105mo\x1B[39m\x1B[38;2;245;183;113mn\x1B[39m\x1B[38;2;247;201;120m:\x1B[39m"
    )

    if print_version:
        print(version_string + "\x1B[38;2;247;201;120m" + version + "\x1B[39m")
        raise typer.Exit()


class Config:
    frequency_max: int = 3_600_000
    frequency_min: int = 1_000_000
    frequency_step: int = 100_000
    frequency_default: int = 2_400_000
    cores_max: int = 128
    cores_min: int = 1
    cores_step: int = 1
    cores_default: int = 1
    fan_speed_max: int = 10_000
    fan_speed_min: int = 1_000
    fan_speed_step: int = 1_000
    fan_speed_default: int = 1_000


class StandardConfig:
    """Standard configuration for the suite."""

    def __init__(self):
        self._color = choice(list(Color))

    def __iter__(self):
        return range(2).__iter__()

    def color(self) -> str:
        """Get the color of the suite."""
        return self._color


FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("main")


@app.callback()
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the chronus package.",
    ),
) -> None:
    pass


class Model(str, Enum):
    brute_force = "brute_force"
    linear_regression = "linear_regression"
    random_tree = "random_tree"


def _choose_optimizer(model: Model) -> OptimizerInterface:
    switcher = {
        Model.brute_force: BruteForceOptimizer(),
        Model.linear_regression: LinearRegressionOptimizer(),
        Model.random_tree: RandomTreeOptimizer(),
    }
    return switcher.get(model, BruteForceOptimizer())


@app.command(name="init-model")
def init_model(
    model: Model = Model.linear_regression,
    db_path: str = typer.Option(
        "data.db",
        "--db",
        "--database",
        help="The path to the database.",
    ),
):
    logger.info("Initializing model of type %s", model.name)
    making_model = InitModelService(
        repository=SqliteRepository(db_path),
        optimizer=_choose_optimizer(model),
        system_info_provider=LsCpuInfoService(),
    )

    with console.status("training model", spinner="dots12"):
        new_model_id = making_model.run()

    logger.info("Model trained with id %s", new_model_id)


@app.command(name="slurm-config")
def get_config(cpu: str = typer.Argument(..., help="The cpu model to get the config for")):
    config = {
        "cores": 2,
        "frequency": 2_200_000,
    }

    print(json.dumps(config))


# add partician compute


@app.command(name="run")
def run(
    hpcg_path: str,
    cores: int = typer.Argument(..., help="The number of cores to run on."),
    frequency: int = typer.Argument(..., help="The frequency to run on."),
    threads_per_core: int = typer.Argument(..., help="The number of threads to run on."),
):
    hpcg = HpcgService(hpcg_path)
    import asyncio

    hpcg.run(cores, frequency, threads_per_core)
    while hpcg.is_running():
        sleep(1)

    print(hpcg.gflops)


@app.command(name="benchmark")
def benchmark(
    hpcg_path: str,
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the chronus package.",
    ),
    debug: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug information.",
    ),
    db_path: str = typer.Option(
        "data.db",
        "-db",
        "--database",
        help="The path to the database.",
    ),
):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    full_path = os.path.abspath(hpcg_path)
    called_from_dir = os.getcwd()
    benchmark_service = BenchmarkService(
        cpu_info_service=LsCpuInfoService(),
        application_runner=HpcgService(full_path),
        benchmark_repository=SqliteRepository(db_path),
        system_service=IpmiSystemService(),
    )

    benchmark_service.run()


# delete output dir if exception
# error if exists
# if job failed, continue

if __name__ == "__main__":
    app()
