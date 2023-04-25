class ApplicationRunnerInterface:
    gflops: float

    def run(self, cores: int, frequency: float):
        pass

    def is_running(self) -> bool:
        pass

    """
    This is called before the application is run.
    """

    def prepare(self):
        pass

    """
    This method is called after the application has finished running.
    """

    def cleanup(self):
        pass
