from .base import SharedBaseModel

__all__ = ("SonarrAPISeries",)


class SeasonStatistics(SharedBaseModel):
    episode_count: int
    total_episode_count: int
    size_on_disk: int
    percent_of_episodes: float

    @property
    def is_complete(self) -> bool:
        """Return True if the series has 100% of available episodes."""
        return self.percent_of_episodes == 100  # noqa: PLR2004


class Season(SharedBaseModel):
    season_number: int
    monitored: bool
    statistics: SeasonStatistics

    @property
    def is_complete(self) -> bool:
        """Return True if the season has 100% of available episodes."""
        return self.statistics.percent_of_episodes == 100  # noqa: PLR2004

    def unmonitor(self) -> None:
        """Unmonitor the season"""
        self.monitored = False


class SeriesStatistics(SharedBaseModel):
    season_count: int
    episode_count: int
    total_episode_count: int
    size_on_disk: int
    percent_of_episodes: float


class SonarrAPISeries(SharedBaseModel):
    title: str
    status: str
    ended: bool
    seasons: list[Season]
    year: int
    path: str
    monitored: bool
    monitor_new_items: str
    statistics: SeriesStatistics
    id: int

    @property
    def is_complete(self) -> bool:
        """Return True if the series has 100% of available episodes."""
        return self.statistics.percent_of_episodes == 100  # noqa: PLR2004

    @property
    def is_ended(self) -> bool:
        """Return True if the series has ended."""
        return self.ended

    def unmonitor_series(self) -> None:
        """Set the series to unmonitored."""
        self.monitored = False

    def __repr__(self) -> str:
        return f"<APISeries, {self.__str__()}>"

    def __str__(self) -> str:
        return (
            f"id={self.id}, title={self.title}, year={self.year}, "
            f"seasons={len(self.seasons)}, complete={self.is_complete}, monitored={self.monitored}"
        )
