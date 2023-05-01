import logging
import sqlite3
from datetime import datetime

from chronus.domain.interfaces.benchmark_run_repository_interface import (
    BenchmarkRunRepositoryInterface,
)
from chronus.domain.Run import Run

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY,
    cpu TEXT,
    cores INTEGER,
    thread_per_core INTEGER,
    frequency REAL,
    gflops REAL,
    flop REAL,
    energy_used REAL,
    gflops_per_watt REAL,
    start_time TEXT,
    end_time TEXT
);
"""

INSERT_RUN_QUERY = """
INSERT INTO runs (
    cpu,
    cores,
    thread_per_core,
    frequency,
    gflops,
    flop,
    energy_used,
    gflops_per_watt,
    start_time,
    end_time
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

GET_ALL_RUNS_QUERY = "SELECT * FROM runs;"


class SqliteRepository(BenchmarkRunRepositoryInterface):
    def __init__(self, path: str):
        self.logger = logging.getLogger(__name__)
        self.path = path
        self._create_table()

    def get_all(self) -> list[Run]:
        runs = []
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            for row in cursor.execute(GET_ALL_RUNS_QUERY):
                (
                    _,
                    cpu,
                    cores,
                    thread_per_core,
                    frequency,
                    gflops,
                    flop,
                    energy_used,
                    gflops_per_watt,
                    start_time,
                    end_time,
                ) = row

                run = Run()
                run.cpu = cpu
                run.cores = int(cores)
                run.threads_per_core = int(thread_per_core)
                run.frequency = float(frequency)
                run.gflops = float(gflops)
                run.flop = float(flop)
                run._energy_used_joules = float(energy_used)
                run._gflops_per_watt = float(gflops_per_watt)
                runs.append(run)
        return runs

    def save(self, run: Run) -> None:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                INSERT_RUN_QUERY,
                (
                    run.cpu,
                    run.cores,
                    run.threads_per_core,
                    run.frequency,
                    run.gflops,
                    run.flop,
                    run.energy_used_joules,
                    run.gflops_per_watt,
                    run.start_time,
                    run.end_time,
                ),
            )
            conn.commit()
        self.logger.info(f"Run data has been saved to {self.path}.")

    def _create_table(self) -> None:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_TABLE_QUERY)
        self.logger.info(f"Table 'runs' has been created in {self.path}.")
