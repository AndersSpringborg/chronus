from typing import List

from dataclasses import dataclass

import dataclasses_json


@dataclasses_json.dataclass_json
@dataclass
class SystemInfo:
    """Returns the number of cores in the system. If the system has hyperthreading, this method should return the
    number of physical cores"""

    cpu_name: str = ""
    cores: int = 0
    threads_per_core: int = 1
    frequencies: list[int] = None

    def __hash__(self):
        return hash((self.cpu_name, self.cores, self.threads_per_core, tuple(self.frequencies)))
