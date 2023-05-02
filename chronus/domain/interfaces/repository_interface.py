from chronus.domain.Run import Run


class RepositoryInterface:
    def save(self, run: Run) -> None:
        pass

    def get_all(self) -> list[Run]:
        pass
