from .base import SharedBaseModel

__all__ = ("RadarrAPIMovie",)


class RadarrAPIMovie(SharedBaseModel):
    title: str
    size_on_disk: int
    status: str
    year: int
    path: str
    monitored: bool
    id: int

    def unmonitor(self) -> None:
        """Unmonitor the movie by setting monitored to False."""
        self.monitored = False

    def __repr__(self) -> str:
        return f"<APIMovie, {self.__str__()}>"

    def __str__(self) -> str:
        return (
            f"id={self.id}, title={self.title}, path={self.path}, "
            f"size={self.size_on_disk}, monitored={self.monitored}"
        )
