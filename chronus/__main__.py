# type: ignore[attr-defined]
from time import sleep
import logging
from rich.logging import RichHandler

from enum import Enum
from random import choice

import typer
from rich.console import Console

from chronus import version
from chronus.SystemIntegration.hpcg import HpcgService
from chronus.example import hello
from chronus.model.Run import Run


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

class StandardConfig():
    """Standard configuration for the suite."""

    def __init__(self):
        self._color = choice(list(Color))

    def __iter__(self):
        return range(2).__iter__()


    def color(self) -> str:
        """Get the color of the suite."""
        return self._color


class Repository:
    def __init__(self):
        pass

    def save(self, run: Run):
        raise NotImplementedError("This is an abstract class.")
        pass



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
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

@app.command(name="")
def main(
    path: str = typer.Option(
        None,
        "-p",
        "--hpcg-path",
        "--xhpcg-path",
        case_sensitive=False,
        help = "The path to hpcg or xhpcg binary."
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
    """Run a suite of tests on a HPCG installation."""
    suite = Suite(path)
    suite.run()


if __name__ == "__main__":
    app()
