try:
    import dotenv
except ModuleNotFoundError:
    pass
else:
    dotenv.load_dotenv(override=True)

import os


class Config:
    # RADARR Configuration
    RADARR_PROTOCOL: str = os.getenv("RADARR_PROTOCOL", "http")
    RADARR_HOST: str = os.getenv("RADARR_HOST", "")
    RADARR_PORT: int = int(os.getenv("RADARR_PORT", 7878))
    RADARR_API_KEY: str = os.getenv("RADARR_API_KEY", "")

    # SONARR Configuration
    SONARR_PROTOCOL: str = os.getenv("SONARR_PROTOCOL", "http")
    SONARR_HOST: str = os.getenv("SONARR_HOST", "")
    SONARR_PORT: int = int(os.getenv("SONARR_PORT", 8989))
    SONARR_API_KEY: str = os.getenv("SONARR_API_KEY", "")

    # Sonarr-specific unmonitor settings
    HANDLE_EPISODES: bool = os.getenv("HANDLE_EPISODES", "true").lower() == "true"
    HANDLE_SERIES: bool = os.getenv("HANDLE_SERIES", "false").lower() == "true"
    HANDLE_SERIES_ENDED_ONLY: bool = os.getenv("HANDLE_SERIES_ENDED_ONLY", "true").lower() == "true"
    EXCLUDE_SERIES: bool = os.getenv("EXCLUDE_SERIES", "true").lower() == "true"

    # General settings
    REMOVE_MEDIA: bool = os.getenv("REMOVE_MEDIA", "false").lower() == "true"

    @staticmethod
    def validate():
        """Validate required configuration values and raise errors if necessary."""
        missing: list[str] = []
        if not Config.RADARR_HOST:
            missing.append("RADARR_HOST")
        if not Config.RADARR_API_KEY:
            missing.append("RADARR_API_KEY")
        if not Config.SONARR_HOST:
            missing.append("SONARR_HOST")
        if not Config.SONARR_API_KEY:
            missing.append("SONARR_API_KEY")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    @property
    def settings(self) -> str:
        return f"Unmonitor Only" if not self.REMOVE_MEDIA else "Remove Item"


class LogConfig:
    # Logging configuration
    _LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    LOG_LEVEL_MAP: dict[str, int] = {
        "debug": 10,
        "info": 20,
        "warn": 30,
        "error": 40,
        "critical": 50,
    }

    LOG_LEVEL: int = LOG_LEVEL_MAP.get(_LOG_LEVEL, 20)
