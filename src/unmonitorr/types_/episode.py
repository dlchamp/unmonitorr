from .base import SharedBaseModel

__all__ = (
    "Episode",
    "Series",
)


class SeriesStatistics(SharedBaseModel):
    season_count: int
    episode_count: int
    total_episode_count: int
    percent_of_episodes: float


class SeasonStatistics(SharedBaseModel):
    episode_count: int
    total_episode_count: int
    percent_of_episodes: float


class Season(SharedBaseModel):
    season_number: int
    monitored: bool
    statistics: SeasonStatistics


class Series(SharedBaseModel):
    id: int
    title: str
    status: str
    ended: bool
    seasons: list[Season]
    year: int
    path: str
    monitored: bool
    statistics: SeriesStatistics


class Episode(SharedBaseModel):
    id: int
    series_id: int
    season_number: int
    episode_number: int
    title: str
    has_file: bool
    monitored: bool
    series: Series
