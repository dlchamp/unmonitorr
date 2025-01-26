from typing import Any

import log
from config import Config
from types_ import SonarrAPISeries, SonarrWebhookPayload, WebhookSeries

from . import BaseArrClient, HTTPException

logger = log.get_logger(__name__)


COMPLETE_PERCENT = 100


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

    async def delete_series(self, series: WebhookSeries) -> None:
        """Delete a series from Sonarr.

        Parameters
        ----------
        id : int
            The ID of the series to delete.
        """
        logger.info("Deleting series from Sonarr: %s", series)
        url = f"{self.base_url}/series/{series.id}"

        params: dict[str, Any] = {
            "deleteFiles": False,
            "addImportListExclusion": Config.EXCLUDE_SERIES,
        }

        try:
            await self.request("DELETE", url, headers=self.headers, params=params)
            logger.info("Successfully deleted series from Sonarr: %s", series)
        except HTTPException as e:
            logger.warning(
                "Unexpected error during series deletion: status=%s, reason=%s",
                e.status,
                e.reason,
            )

    async def unmonitor_episodes(self, payload: SonarrWebhookPayload) -> None:
        """Unmonitor episodes for a given series in Sonarr.

        Parameters
        ----------
        payload: SonarrWebhookPayload
            Webhook payload from Sonarr that contains the episodes.
        """
        logger.info("Attempting to unmonitor episodes for series: %s", payload.series)
        logger.debug("Series details: %s", payload.series.model_dump())

        url = f"{self.base_url}/episode/monitor"
        params: dict[str, Any] = {"includeImages": "false"}

        json: dict[str, Any] = {
            "episodeIds": [e.id for e in payload.episodes],
            "monitor": False,
        }

        try:
            await self.request("PUT", url, headers=self.headers, json=json, params=params)
            logger.info("Successfully unmonitored episodes: %s", payload.episodes)
        except HTTPException as e:
            logger.warning(
                "Unexpected error during unmonitoring episodes: status=%s, reason=%s",
                e.status,
                e.reason,
            )

    async def get_series_by_id(self, id: int) -> SonarrAPISeries | None:
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
        except HTTPException as e:
            logger.warning(
                "Unexpected error fetching series from Sonarr: status=%s, reason=%s",
                e.status,
                e.reason,
            )
            return None

        else:
            return SonarrAPISeries.model_validate(response)

    async def put_updated_series(self, series: SonarrAPISeries) -> None:
        """Mark a series as unmonitored

        Parameters
        ----------
        series: SonarrAPISeries
            The complete series data from Sonarr.
        """
        url = f"{self.base_url}/series/{series.id}"

        logger.info("Unmonitoring series: %s", series)
        logger.debug("Series data to update: %s", series.model_dump())
        try:
            await self.request(
                "PUT", url, headers=self.headers, json=series.model_dump(by_alias=True)
            )
            logger.info("Successfully unmonitored series: %s", series)
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
        return stats.get("percentOfEpisodes", 0) == 100  # noqa: PLR2004
