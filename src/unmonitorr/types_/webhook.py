from .base import SharedBaseModel

__all__ = (
    "RadarrWebhookPayload",
    "SonarrWebhookPayload",
    "WebhookEpisode",
    "WebhookMovie",
    "WebhookSeries",
)


class WebhookMovie(SharedBaseModel):
    id: int
    title: str
    year: int
    folder_path: str

    def __repr__(self) -> str:
        return f"<Movie, {self.__str__()}>"

    def __str__(self) -> str:
        return f"id={self.id}, title={self.title}, year={self.year}, path={self.folder_path}"


class RadarrWebhookPayload(SharedBaseModel):
    movie: WebhookMovie
    event_type: str
    instance_name: str
    application_url: str


class WebhookSeries(SharedBaseModel):
    id: int
    title: str
    path: str
    year: int

    def __repr__(self) -> str:
        return f"<Series, {self.__str__()}>"

    def __str__(self) -> str:
        return f"id={self.id}, title={self.title}, year={self.year}, path={self.path}"


class WebhookEpisode(SharedBaseModel):
    id: int
    episode_number: int
    season_number: int
    title: str
    series_id: int

    def __repr__(self) -> str:
        return f"<Episode, {self.__str__()}>"

    def __str__(self) -> str:
        return (
            f"id={self.id}, title={self.title}, episode_number={self.episode_number}, "
            f"season_number={self.season_number}, series_id={self.series_id}"
        )


class SonarrWebhookPayload(SharedBaseModel):
    series: WebhookSeries
    episodes: list[WebhookEpisode]
    event_type: str
    instance_name: str
    application_url: str

    def episode_ids_to_unmonitor(self) -> list[int]:
        """List the episode IDs to send to the unmonitor endpoint."""
        return [e.id for e in self.episodes]
