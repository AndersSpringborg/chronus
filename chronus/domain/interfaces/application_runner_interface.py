class ApplicationRunnerInterface:
    gflops: float

    def run(self, cores: int, frequency: float):
        pass

    def is_running(self) -> bool:
        pass
