import logging
import sqlite3

from chronus.domain.interfaces.benchmark_run_repository_interface import (
    BenchmarkRunRepositoryInterface,
)
from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample
from tests.fixtures import datetime_from_string

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

CREATE_SYSTEM_SAMPLES_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS system_samples (
    id INTEGER PRIMARY KEY,
    run_id INTEGER,
    timestamp TEXT,
    current_power_draw REAL,
    FOREIGN KEY(run_id) REFERENCES runs(id)
);
"""

INSERT_SYSTEM_SAMPLE_QUERY = """
INSERT INTO system_samples (
    run_id,
    timestamp,
    current_power_draw
) VALUES (?, ?, ?);
"""

GET_ALL_SYSTEM_SAMPLES_QUERY = "SELECT * FROM system_samples WHERE run_id = ?;"


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
                    run_id,
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
                run._samples = self._get_system_samples(run_id=run_id)
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
            run_id = cursor.lastrowid

            for sample in run._samples:
                cursor.execute(
                    INSERT_SYSTEM_SAMPLE_QUERY,
                    (run_id, sample.timestamp, sample.current_power_draw),
                )
            conn.commit()
        self.logger.info(f"Run data has been saved to {self.path}.")

    def _create_table(self) -> None:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_TABLE_QUERY)
            cursor.execute(CREATE_SYSTEM_SAMPLES_TABLE_QUERY)
        self.logger.info(f"Tables 'runs' and 'system_samples' have been created in {self.path}.")

    def _get_system_samples(self, run_id: int) -> list[SystemSample]:
        samples = []
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            for row in cursor.execute(GET_ALL_SYSTEM_SAMPLES_QUERY, (run_id,)):
                _, _, timestamp, current_power_draw = row
                sample = SystemSample(
                    timestamp=datetime_from_string(timestamp), current_power_draw=current_power_draw
                )
                samples.append(sample)
        return samples
