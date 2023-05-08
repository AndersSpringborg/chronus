class ApplicationRunnerInterface:
    gflops: float
    result: float

    def run(self, cores: int, frequency: float, thread_per_core=1):
        raise NotImplementedError()

    def is_running(self) -> bool:
        raise NotImplementedError()

    """
    This is called before the application is run.
    """

    def prepare(self):
        raise NotImplementedError()

    """
    This method is called after the application has finished running.
    """

    def cleanup(self):
        raise NotImplementedError()
