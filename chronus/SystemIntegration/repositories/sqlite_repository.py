import logging
import sqlite3
from datetime import datetime

from chronus.domain.benchmark import Benchmark
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample

CREATE_BENCHMARKS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS benchmarks (
    id INTEGER PRIMARY KEY,
    system_info TEXT,
    application TEXT,
    created_at TEXT
);
"""


CREATE_RUNS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY,
    benchmark_id INTEGER,
    cpu TEXT,
    cores INTEGER,
    thread_per_core INTEGER,
    frequency REAL,
    gflops REAL,
    flop REAL,
    energy_used REAL,
    gflops_per_watt REAL,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY(benchmark_id) REFERENCES benchmarks(id)
);
"""

CREATE_SYSTEM_SAMPLES_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS system_samples (
    id INTEGER PRIMARY KEY,
    run_id INTEGER,
    timestamp TEXT,
    current_power_draw REAL,
    cpu_power REAL,
    cpu_temp REAL,
    FOREIGN KEY(run_id) REFERENCES runs(id)
);
"""


INSERT_BENCHMARK_QUERY = """
INSERT INTO benchmarks (
    system_info,
    application,
    created_at
) VALUES (?, ?, ?);
"""


INSERT_RUN_QUERY = """
INSERT INTO runs (
    benchmark_id,
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
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


INSERT_SYSTEM_SAMPLE_QUERY = """
INSERT INTO system_samples (
    run_id,
    timestamp,
    current_power_draw,
    cpu_power,
    cpu_temp
) VALUES (?, ?, ?, ?, ?);
"""

GET_ALL_BENCHMARKS_QUERY = "SELECT * FROM benchmarks;"
GET_BENCHMARK_RUNS_QUERY = "SELECT * FROM runs WHERE benchmark_id = ?;"
GET_ALL_RUNS_QUERY = "SELECT * FROM runs;"
GET_ALL_SYSTEM_SAMPLES_QUERY = "SELECT * FROM system_samples WHERE run_id = ?;"


class SqliteRepository(RepositoryInterface):
    def save_benchmark(self, benchmark: Benchmark) -> int:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                INSERT_BENCHMARK_QUERY,
                (
                    str(benchmark.system_info),
                    benchmark.application,
                    benchmark.created_at.isoformat(),
                ),
            )
            benchmark_id = cursor.lastrowid
            conn.commit()

            # Save runs associated with the benchmark
            for run in benchmark.runs:
                self.save_run(run)

        self.logger.info(f"Benchmark data has been saved to {self.path}.")
        return benchmark_id

    def get_all_benchmarks(self) -> list[Benchmark]:
        benchmarks = []
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            for row in cursor.execute(GET_ALL_BENCHMARKS_QUERY):
                benchmark_id, system_info, application, created_at = row
                benchmark = Benchmark(
                    system_info=system_info,
                    application=application,
                    id=benchmark_id,
                    created_at=datetime.fromisoformat(created_at),
                )
                benchmark.runs = self.get_all_runs(benchmark_id)
                benchmarks.append(benchmark)
        return benchmarks

    def __init__(self, path: str):
        self.logger = logging.getLogger(__name__)
        self.path = path
        self._create_table()

    def get_all_runs(self, benchmark_id: int = None) -> list[Run]:
        runs = []

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            if benchmark_id is None:
                rows = cursor.execute(GET_ALL_RUNS_QUERY)
            else:
                rows = cursor.execute(GET_BENCHMARK_RUNS_QUERY, (benchmark_id,))
            for row in rows:
                (
                    run_id,
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
                run._samples = self._get_system_samples(run_id=run_id)
                runs.append(run)
        return runs

    def save_run(self, run: Run) -> None:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                INSERT_RUN_QUERY,
                (
                    run.benchmark_id,
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

            # Save system samples associated with the run
            for sample in run._samples:
                cursor.execute(
                    INSERT_SYSTEM_SAMPLE_QUERY,
                    (
                        run_id,
                        sample.timestamp,
                        sample.current_power_draw,
                        sample.cpu_power,
                        sample.cpu_temp,
                    ),
                )
            conn.commit()
        self.logger.info(f"Run data has been saved to {self.path}.")

    def _create_table(self) -> None:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_BENCHMARKS_TABLE_QUERY)
            cursor.execute(CREATE_RUNS_TABLE_QUERY)
            cursor.execute(CREATE_SYSTEM_SAMPLES_TABLE_QUERY)
        self.logger.info(
            f"Tables 'benchmarks', 'runs', and 'system_samples' have been created in {self.path}."
        )

    def _get_system_samples(self, run_id: int) -> list[SystemSample]:
        samples = []
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            for row in cursor.execute(GET_ALL_SYSTEM_SAMPLES_QUERY, (run_id,)):
                _, _, timestamp, current_power_draw, cpu_power, cpu_temp = row
                sample = SystemSample(
                    timestamp=datetime.fromisoformat(timestamp),
                    current_power_draw=current_power_draw,
                    cpu_power=cpu_power,
                    cpu_temp=cpu_temp,
                )
                samples.append(sample)
        return samples
