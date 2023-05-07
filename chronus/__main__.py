import json
import logging
import os
from enum import Enum
from random import choice
from time import sleep

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from chronus import version
from chronus.application.benchmark_service import BenchmarkService
from chronus.application.init_model_service import InitModelService
from chronus.application.load_model_service import LoadModelService
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.SystemIntegration.application_runners.hpcg import HpcgService
from chronus.SystemIntegration.cpu_info_services.cpu_info_service import LsCpuInfoService
from chronus.SystemIntegration.optimizers.bruteforce_optmizer import BruteForceOptimizer
from chronus.SystemIntegration.optimizers.linear_regression import LinearRegressionOptimizer
from chronus.SystemIntegration.optimizers.random_tree_forrest import RandomTreeOptimizer
from chronus.SystemIntegration.repositories.sqlite_repository import SqliteRepository
from chronus.SystemIntegration.settings_interface.etc_storage import EtcLocalStorage
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
    brute_force = BruteForceOptimizer.name()
    linear_regression = LinearRegressionOptimizer.name()
    random_tree = RandomTreeOptimizer.name()


def _choose_optimizer(model: str) -> OptimizerInterface:
    switcher = {
        BruteForceOptimizer.name(): BruteForceOptimizer(),
        LinearRegressionOptimizer.name(): LinearRegressionOptimizer(),
        RandomTreeOptimizer.name(): RandomTreeOptimizer(),
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
    system_id: int = typer.Option(
        -1,
        "--system",
        help="The id of the system to use.",
    ),
):
    repo = SqliteRepository(db_path)
    if system_id == -1:
        console.print("[yellow]You need to choose a system to train a model.[/yellow]")
        console.print("[green]Here are the available systems:[/green]")
        present_systems(repo)

        raise typer.Exit()

    logger.info("Initializing model of type %s", model.name)
    making_model = InitModelService(
        system_id=system_id,
        repository=repo,
        optimizer=_choose_optimizer(model),
    )

    with console.status("training model", spinner="dots12"):
        new_model_id = making_model.run()

    logger.info("Model trained with id %s", new_model_id)


def present_systems(repo):
    systems = repo.get_all_system_info()
    table = Table(title="Available Systems", style="green")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("DataClass", justify="center", style="magenta")
    for i, system in enumerate(systems):
        table.add_row(str(i), str(system))
    console.print(table)


def present_models(repo: RepositoryInterface):
    models = repo.get_all_models()
    table = Table(title="Available Models", style="green")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Type", justify="center", style="magenta")
    table.add_column("Created", justify="center", style="magenta")
    table.add_column("System", justify="center", style="magenta")
    for model in models:
        table.add_row(
            str(model.id), model.type, model.created_at.strftime("%d/%m/%Y"), str(model.system_info)
        )
    console.print(table)


@app.command(name="load-model")
def load_model(
    model_id: int = typer.Option(
        -1,
        "--model",
        help="The id of the model to use.",
    ),
    db_path: str = typer.Option(
        "data.db",
        "--db",
        "--database",
        help="The path to the database.",
    ),
):
    repo = SqliteRepository(db_path)
    if model_id == -1:
        console.print("[yellow]You need to choose a model to load.[/yellow]")
        console.print("[green]Here are the available models:[/green]")
        present_models(repo)

        console.print("[yellow]Specify the model id with --model <id>[/yellow]")

        raise typer.Exit()

    model = repo.get_model(model_id)

    load_model = LoadModelService(
        model_id=model_id,
        repository=repo,
        optimizer=_choose_optimizer(model.type),
        local_storage=EtcLocalStorage(),
    )
    load_model.run()


@app.command(name="slurm-config")
def get_config(cpu: str = typer.Argument(..., help="The cpu model to get the config for")):
    run_model = RunModelService(cpu=cpu, application_name="hpcg")


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
