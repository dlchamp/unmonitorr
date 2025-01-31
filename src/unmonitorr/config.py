import json
from typing import Any, Final

try:
    import dotenv
except ModuleNotFoundError:
    pass
else:
    dotenv.load_dotenv(override=True)

import os

__all__ = (
    "Config",
    "LogConfig",
)

CONFIG_PATH: Final[str] = "unmonitorr/config-data"
os.makedirs(CONFIG_PATH, exist_ok=True)


class Config:

    def __init__(self) -> None:
        # RADARR Configuration
        self.radarr_uri: str = ""
        self.radarr_api_key: str = ""

        # sonarr configuration
        self.sonarr_uri: str = ""
        self.sonarr_api_key: str = ""

        # sonarr-specific unmonitor settings
        self.handle_episodes: bool = True
        self.handle_series: bool = False
        self.handle_series_ended_only: bool = True
        self.exclude_series: bool = True

        # general settings
        self.remove_media: bool = False

        self.load()

    @property
    def settings(self) -> str:
        return "Unmonitor Only" if not self.remove_media else "Remove Item"

    def save(self) -> None:
        """Dump the config to file."""
        with open(f"{CONFIG_PATH}/config.json", "w+") as fp:
            json.dump(self.to_dict(), fp, indent=4)

    def load(self) -> None:
        """Load the config from file."""
        try:
            with open(f"{CONFIG_PATH}/config.json") as fp:
                data = json.load(fp)
                self.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save()

    def from_dict(self, data: dict[str, Any]) -> None:
        """Update the configuration from a dictionary."""
        self.radarr_uri = data.get("radarr_uri", self.radarr_uri)
        self.radarr_api_key = data.get("radarr_api_key", self.radarr_api_key)
        self.sonarr_uri = data.get("sonarr_uri", self.sonarr_uri)
        self.sonarr_api_key = data.get("sonarr_api_key", self.sonarr_api_key)
        self.handle_episodes = data.get("handle_episodes", self.handle_episodes)
        self.handle_series = data.get("handle_series", self.handle_series)
        self.handle_series_ended_only = data.get(
            "handle_series_ended_only", self.handle_series_ended_only
        )
        self.exclude_series = data.get("exclude_series", self.exclude_series)
        self.remove_media = data.get("remove_media", self.remove_media)

    def to_dict(self) -> dict[str, Any]:
        return {
            "radarr_uri": self.radarr_uri,
            "radarr_api_key": self.radarr_api_key,
            "sonarr_uri": self.sonarr_uri,
            "sonarr_api_key": self.sonarr_api_key,
            "handle_episodes": self.handle_episodes,
            "handle_series": self.handle_series,
            "handle_series_ended_only": self.handle_series_ended_only,
            "exclude_series": self.exclude_series,
            "remove_media": self.remove_media,
        }


class LogConfig:
    # Logging configuration
    _LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    LOG_LEVEL_MAP: Final[dict[str, int]] = {
        "debug": 10,
        "info": 20,
        "warn": 30,
        "error": 40,
        "critical": 50,
    }

    LOG_LEVEL: int = LOG_LEVEL_MAP.get(_LOG_LEVEL, 20)
