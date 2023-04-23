from typing import IO, Callable

import io
from pprint import pprint

from chronus.domain.Run import Run
from chronus.SystemIntegration.repository import Repository


class FileRepository(Repository):
    _path: str

    def _file_factory(self, path, mode):
        return open(path, mode)

    def __init__(self, path: str):
        super().__init__()
        self._prepare_file(path)
        self._path = path

    def save(self, run: Run) -> None:
        """Save the run to the repository."""

        insert_comma = True
        with self._file_factory(self._path, "r") as f:
            first_two_chars = f.read(2)
            if first_two_chars == "[]":
                insert_comma = False

        # remove trailing ']'
        with self._file_factory(self._path, "rb+") as f:
            f.seek(-1, 2)
            f.truncate()

        with self._file_factory(self._path, "a") as f:
            if insert_comma:
                f.write(",")
            f.write(run.to_json())
            f.write("]")

    def _prepare_file(self, path):
        with self._file_factory(path, "x") as f:
            f.write("[]")
