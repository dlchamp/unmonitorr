from dataclasses import dataclass
from typing import Any, Self

import utils

ALLOWED_MOVIE_KEYS: set[str] = {
    "id",
    "title",
    "tmdbId",
    "year",
    "folderPath",
    "tags",
}

ALLOWED_SERIES_KEYS: set[str] = {
    "id",
    "title",
    "path",
    "year",
    "tags",
}

ALLOWED_EPISODE_KEYS: set[str] = {
    "id",
    "episodeNumber",
    "seasonNumber",
    "seriesId",
    "title",
    "overview",
    "airDate",
}


@dataclass
class Movie:
    id: int
    title: str
    tmdb_id: int
    year: int
    tags: list[str]
    folder_path: str

    @classmethod
    def from_payload(cls, data: dict[str, Any]) -> Self:
        movie_data = data["movie"]
        kwargs: dict[str, Any] = {
            utils.to_snake_case(k): v for k, v in movie_data.items() if k in ALLOWED_MOVIE_KEYS
        }
        return cls(**kwargs)


@dataclass
class Episode:
    id: int
    episode_number: int
    season_number: int
    series_id: int
    title: str
    overview: str
    air_date: str
    series_id: int

    @classmethod
    def from_payload(cls, data: dict[str, Any]) -> Self:
        kwargs: dict[str, Any] = {
            utils.to_snake_case(k): v for k, v in data.items() if k in ALLOWED_EPISODE_KEYS
        }
        return cls(**kwargs)


@dataclass
class Series:
    id: int
    tags: list[str]
    title: str
    year: int
    path: str
    episodes: list[Episode]

    @classmethod
    def from_payload(cls, data: dict[str, Any]) -> Self:
        series_data = data["series"]
        episodes_data = data["episodes"]
        kwargs: dict[str, Any] = {
            utils.to_snake_case(k): v for k, v in series_data.items() if k in ALLOWED_SERIES_KEYS
        }
        kwargs["episodes"] = [Episode.from_payload(item) for item in episodes_data]
        return cls(**kwargs)
