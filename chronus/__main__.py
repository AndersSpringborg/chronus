from typing import List

import json
import logging
import os
from enum import Enum
from random import choice, randrange, uniform
from time import sleep

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import pprint

from chronus import version
from chronus.model.Run import Run
from chronus.model.svm import config_model
from chronus.SystemIntegration.FileRepository import FileRepository
from chronus.SystemIntegration.hpcg import HpcgService
from chronus.SystemIntegration.repository import Repository

name_as_grad = "^[[38;2;244;59;71mc^[[39m^[[38;2;215;59;84mh^[[39m^[[38;2;186;59;97mr^[[39m^[[38;2;157;59;110mo^[[39m^[[38;2;127;58;122mn^[[39m^[[38;2;98;58;135mu^[[39m^[[38;2;69;58;148ms^[[39m"
name = "chronus"


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="chronus",
    help="A energy scheduling model, build for HPC.",
    add_completion=True,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]chronus[/] version: [bold blue]{version}[/]")
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


class Suite:
    config: Config = StandardConfig()
    hpcg: HpcgService
    _repository: Repository

    def __init__(self, path: str, repository: Repository):
        self.hpcg = HpcgService.with_path(path)
        self._path = path
        self._repository = repository

    def run(self) -> None:
        """Run the suite."""
        for conf in self.config:
            run = self.hpcg.run()
            logging.info(f"GFLOPS: {run.gflops}")
            self._repository.save(run)
            self.cooldown()

    def cooldown(self):
        logging.info("Cooling down...")
        sleep(1)


FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])


@app.command(name="")
def main(
    path: str = typer.Option(
        None,
        "-p",
        "--hpcg-path",
        "--xhpcg-path",
        case_sensitive=False,
        help="The path to hpcg or xhpcg binary.",
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the chronus package.",
    ),
) -> None:
    console.print(f"{name}")
    """Run a suite of tests on a HPCG installation."""
    suite = Suite(path, FileRepository("../out/chronus_run_save.json"))
    suite.run()


def fake_data() -> list[Run]:
    # check if data set is cached in file
    file_path = "/home/anders/projects/chronus/out/chronus_fake_run.json"
    if os.path.isfile(file_path):
        data = json.load(open(file_path))
        return [Run.from_dict(d) for d in data]

    runs = []
    fan_speeds = [1000, 1500, 2000, 2500]
    cpu_temps = [50.0, 60.0, 70.0, 80.0]
    cpu_cores = [1, 2, 4, 8, 16, 32, 48, 64]
    gflops_range = (10.0, 500.0)
    watts_range = (50, 250)
    for i in range(50):
        watts = randrange(*watts_range)
        core_count = choice(cpu_cores)
        core_frequency = uniform(1, 3.6)
        gflops = core_count * core_frequency
        runs.append(Run(0, 0, core_count, core_frequency, int(gflops), watts))

    # save data for caching
    json.dump([r.to_dict() for r in runs], open(file_path, "w"))

    return runs


@app.command(name="plot")
def plot():
    data = fake_data()
    # 3d plot with watt, gflops, cpu cores
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D

    x = [r.watts for r in data]
    y = [r.cpu_cores for r in data]
    z = [r.gflops for r in data]

    # Plot the 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, c=z, cmap="hot", marker="o")
    ax.set_xlabel("Watts")
    ax.set_ylabel("Core Count")
    ax.set_zlabel("GFLOPS")
    plt.show()


@app.command(name="solver")
def solver():
    data = fake_data()

    best_config = config_model(data)

    pprint(best_config)


if __name__ == "__main__":
    app()
