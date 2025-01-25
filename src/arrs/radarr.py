from typing import Any

from types_ import Movie
from . import BaseArrClient, HTTPException
import log

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

    def __init__(self, proto: str, host: str, port: int, api_key: str) -> None:
        super().__init__()

        self.proto = proto
        self.host = host
        self.port = port
        self.api_key = api_key

        self.base_url = f"{proto}://{host}:{port}/api/v3"
        self.headers = {"X-API-Key": api_key, "Accept": "application/json"}

        logger.debug("Initialized RadarrClient with base_url: %s", self.base_url)

    async def get_movie(self, id: int) -> dict[str, Any] | None:
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
            return response
        except HTTPException as e:
            logger.warning(
                "Unexpected error fetching movie from Radarr: status=%s, reason=%s",
                e.status,
                e.reason,
            )
            return None

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

    async def unmonitor_movie(self, data: dict[str, Any]) -> None:
        """
        Unmonitor a specific movie in Radarr.

        Parameters
        ----------
        data : dict[str, Any]
            The movie data containing the ID and updated monitoring status.
        """
        url = f"{self.base_url}/movie/{data['id']}"

        logger.info("Unmonitoring movie with ID: %s", data["id"])
        logger.debug("Movie data to update: %s", data)
        try:
            await self.request("PUT", url, headers=self.headers, json=data)
            logger.info("Successfully unmonitored movie with ID: %s", data["id"])
        except HTTPException as e:
            logger.warning(
                "Unexpected error during unmonitoring movie: status=%s, reason=%s",
                e.status,
                e.reason,
            )
