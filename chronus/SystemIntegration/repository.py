from chronus.domain.Run import Run


class Repository:
    def __init__(self):
        pass

    def save(self, run: Run):
        raise NotImplementedError("This is an abstract class.")
        pass
