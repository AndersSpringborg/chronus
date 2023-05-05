import json
import logging
import os
from enum import Enum
from random import choice

import typer
from rich.console import Console
from rich.logging import RichHandler

from chronus import version
from chronus.application.benchmark_service import BenchmarkService
from chronus.application.model_service import ModelService
from chronus.SystemIntegration.application_runners.hpcg import HpcgService
from chronus.SystemIntegration.cpu_info_services.cpu_info_service import LsCpuInfoService
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


class FileWithTimeStampHandlerAndLevel(logging.FileHandler):
    def emit(self, record: logging.LogRecord) -> None:
        from datetime import datetime
        record.msg = f"[{datetime.now().strftime('%H:%M:%S')}] {record.levelname: <7} {record.msg}"
        super().emit(record)


FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(), FileWithTimeStampHandlerAndLevel("chronus.log")])


app = typer.Typer(
    name=name,
    help="A energy scheduling model, build for HPC.",
    add_completion=True,
)
console = Console()


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


@app.command(name="init-model")
def init_model(
    model_path: str = typer.Argument(..., help="The path to the model directory."),
    data_path: str = typer.Argument(..., help="The path to the data directory."),
):
    abs_model_path = os.path.abspath(model_path)
    abs_data_path = os.path.abspath(data_path)
    model_service = ModelService(
        model_repository=ModelRepository(abs_model_path),
        data_repository=DataRepository(abs_data_path),
        model_implementations=LinearRegression(),
    )
    model = model_service.init_model()
    model_service.save_model(model)
    logging.info("Model saved.")


@app.command(name="slurm-config")
def get_config(cpu: str = typer.Argument(..., help="The cpu model to get the config for")):
    config = {
        "cores": 2,
        "frequency": 2_200_000,
    }

    print(json.dumps(config))


# add partician compute


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
