from unmonitorr import log
from unmonitorr.types_ import RadarrAPIMovie

from .arrbase import BaseArrClient, HTTPException

logger = log.get_logger(__name__)


class RadarrClient(BaseArrClient):
    """
    A client for interacting with Radarr's API.

    Parameters
    ----------
    proto : str
        Protocol to use (http or https).
    host : str
        Hostname or IP address of the Radarr server.
    port : int
        Port number of the Radarr server.
    api_key : str
        API key for authenticating with the Radarr server.
    """

    def __init__(self, uri: str, api_key: str) -> None:
        super().__init__()

        self.uri = uri
        self.api_key = api_key

        if self.is_disabled:
            logger.info("Radarr configuration missing. Client disabled.")

        self.base_url = f"{uri}/api/v3"
        self.headers = {"X-API-Key": api_key, "Accept": "application/json"}

        logger.debug("Initialized RadarrClient with base_url: %s", self.base_url)

    @property
    def is_disabled(self) -> bool:
        """Returns True if client is missing URL or API key."""
        return not self.uri or not self.api_key

    async def get_movie_by_id(self, id: int) -> RadarrAPIMovie | None:
        """
        Fetch details for a specific movie from Radarr.

        Parameters
        ----------
        id : int
            The ID of the movie to fetch.

        Returns
        -------
        dict[str, Any] | None
            The movie details if found, otherwise None.
        """
        url = self.base_url + f"/movie/{id}"

        logger.debug("Fetching movie details for ID: %s", id)
        try:
            response = await self.request("GET", url, headers=self.headers)
            logger.debug("Successfully fetched movie details: %s", response)
        except HTTPException as e:
            logger.warning(
                "Unexpected error fetching movie from Radarr: status=%s, reason=%s",
                e.status,
                e.reason,
            )
            return None
        else:
            return RadarrAPIMovie.model_validate(response)

    async def delete_movie(self, id: int) -> None:
        """
        Delete a movie from Radarr.

        Parameters
        ----------
        id : int
            The ID of the movie to delete.
        """
        url = f"{self.base_url}/movie/{id}"

        logger.info("Deleting movie with ID: %s", id)
        try:
            await self.request("DELETE", url, headers=self.headers)
            logger.info("Successfully deleted movie with ID: %s", id)
        except HTTPException as e:
            logger.warning(
                "Unexpected error during movie deletion: status=%s, reason=%s",
                e.status,
                e.reason,
            )

    async def put_updated_movie(self, movie: RadarrAPIMovie) -> None:
        """
        Unmonitor a specific movie in Radarr.

        Parameters
        ----------
        movie: RadarAPIMovie
            The movie data containing the ID and updated monitoring status.
        """
        url = f"{self.base_url}/movie/{movie.id}"

        logger.info("Unmonitoring movie: %s", movie)
        logger.debug("Movie data to update: %s", movie.model_dump())
        try:
            await self.request(
                "PUT", url, headers=self.headers, json=movie.model_dump(by_alias=True)
            )
            logger.info("Successfully unmonitored movie: %s", movie)
        except HTTPException as e:
            logger.warning(
                "Unexpected error during unmonitoring movie: status=%s, reason=%s",
                e.status,
                e.reason,
            )
