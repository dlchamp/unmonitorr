from typing import Any

from config import Config
from types_ import Episode, Series
from . import BaseArrClient, HTTPException
import log

logger = log.get_logger(__name__)


class SonarrClient(BaseArrClient):
    """A client for interacting with Sonarr's API.

    Parameters
    ----------
    proto : str
        Protocol to use (http or https).
    host : str
        Hostname or IP address of the Sonarr server.
    port : int
        Port number of the Sonarr server.
    api_key : str
        API key for authenticating with the Sonarr server.
    """

    def __init__(self, uri: str, api_key: str) -> None:
        super().__init__()

        self.uri = uri
        self.api_key = api_key

        self.base_url = f"{uri}/api/v3"
        self.headers = {"X-API-Key": api_key, "Accept": "application/json"}

        logger.debug("Initialized SonarrClient with base_url: %s", self.base_url)

    async def get_episode(self, episode: Episode) -> dict[str, Any] | None:
        """Fetch details for a specific episode from Sonarr.

        Parameters
        ----------
        episode : Episode
            The episode to fetch details for.

        Returns
        -------
        dict[str, Any] | None
            The episode details if found, otherwise None.
        """
        logger.debug("Fetching episode details for episode: %s", episode)
        method = "GET"
        url = self.base_url + f"/episode/{episode.id}"

        try:
            response = await self.request(method, url, headers=self.headers)
            logger.debug("Successfully fetched episode details: %s", response)
            return response
        except HTTPException as e:
            logger.warning(
                "Unexpected error fetching episode from Sonarr: status=%s, reason=%s",
                e.status,
                e.reason,
            )
            return None

    async def delete_series(self, id: int) -> None:
        """Delete a series from Sonarr.

        Parameters
        ----------
        id : int
            The ID of the series to delete.
        """
        logger.info("Deleting series with ID: %s", id)
        url = self.base_url + f"/series/{id}"

        params: dict[str, Any] = {
            "deleteFiles": False,
            "addImportListExclusion": Config.EXCLUDE_SERIES,
        }

        try:
            await self.request("DELETE", url, headers=self.headers, params=params)
            logger.info("Successfully deleted series with ID: %s", id)
        except HTTPException as e:
            logger.warning(
                "Unexpected error during series deletion: status=%s, reason=%s",
                e.status,
                e.reason,
            )

    async def unmonitor_episodes(self, series: Series) -> None:
        """Unmonitor episodes for a given series in Sonarr.

        Parameters
        ----------
        series : Series
            The series whose episodes are to be unmonitored.
        """
        logger.info("Attempting to unmonitor episodes for series: %s", series)
        logger.debug("Series details: %s", series)

        url = self.base_url + f"/episode/monitor"
        params: dict[str, Any] = {"includeImages": "false"}

        json: dict[str, Any] = {
            "episodeIds": [e.id for e in series.episodes],
            "monitor": False,
        }

        try:
            await self.request("PUT", url, headers=self.headers, json=json, params=params)
            logger.info("Successfully unmonitored episodes for series: %s", series)
        except HTTPException as e:
            logger.warning(
                "Unexpected error during unmonitoring episodes: status=%s, reason=%s",
                e.status,
                e.reason,
            )

    async def get_series(self, id: int) -> dict[str, Any] | None:
        """Fetch details for a specific series from Sonarr.

        Parameters
        ----------
        id : int
            The ID of the series to fetch.

        Returns
        -------
        dict[str, Any] | None
            The series details if found, otherwise None.
        """
        logger.debug("Fetching series details for ID: %s", id)
        url = self.base_url + f"/series/{id}"

        try:
            response = await self.request("GET", url, headers=self.headers)
            logger.debug("Successfully fetched series details: %s", response)
            return response
        except HTTPException as e:
            logger.warning(
                "Unexpected error fetching series from Sonarr: status=%s, reason=%s",
                e.status,
                e.reason,
            )
            return None

    async def unmonitor_series(self, data: dict[str, Any]) -> None:
        """Mark a series as unmonitored

        Parameters
        ----------
        data: dict[str, Any]
            The complete series data from Sonarr.
        """
        url = f"{self.base_url}/series/{data['id']}"

        logger.info("Unmonitoring series with ID: %s", data["id"])
        logger.debug("Series data to update: %s", data)
        try:
            await self.request("PUT", url, headers=self.headers, json=data)
            logger.info("Successfully unmonitored series with ID: %s", data["id"])
        except HTTPException as e:
            logger.warning(
                "Unexpected error during unmonitoring series: status=%s, reason=%s",
                e.status,
                e.reason,
            )

    def series_is_ended(self, series: dict[str, Any]) -> bool:
        """
        Check if a series is marked as ended in Sonarr.

        Parameters
        ----------
        series : dict[str, Any]
            The series data to check.

        Returns
        -------
        bool
            True if the series is ended, otherwise False.
        """
        logger.debug("Checking if series is ended: %s", series)
        return series.get("ended", False)

    def series_is_complete(self, series: dict[str, Any]) -> bool:
        """
        Check if a series is 100% complete in Sonarr.

        Parameters
        ----------
        series : dict[str, Any]
            The series data to check.

        Returns
        -------
        bool
            True if the series is complete, otherwise False.
        """
        stats = series.get("statistics", {})
        logger.debug("Checking series completeness: %s", stats)
        return stats.get("percentOfEpisodes", 0) == 100
