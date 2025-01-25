from typing import Any, Callable
from aiohttp import web
from arrs.radarr import RadarrClient
from arrs.sonarr import SonarrClient
from types_ import Movie, Series

from config import Config
import log

logger = log.get_logger(__name__)


class WebhookHandler:
    """
    Handles webhook requests for Radarr and Sonarr.

    Parameters
    ----------
    config : Config
        Configuration object containing API credentials and settings.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.radarr_api = RadarrClient(
            config.RADARR_URI,
            config.RADARR_API_KEY,
        )
        self.sonarr_api = SonarrClient(
            config.SONARR_URI,
            config.SONARR_API_KEY,
        )
        logger.debug("Initialized WebhookHandler")

    async def generic_handler(
        self,
        request: web.Request,
        processor: Callable[[dict[str, Any]], Any],
    ) -> web.Response:
        """
        Generic handler for webhook payloads.

        Parameters
        ----------
        request : web.Request
            The incoming HTTP request.
        processor : Callable[[dict[str, Any]], Any]
            A function to process the webhook payload and return an item.

        Returns
        -------
        web.Response
            The HTTP response.
        """
        payload = await request.json()
        headers = request.headers.items()

        logger.debug("Received request headers: %s", headers)
        logger.debug("Received request payload: %s", payload)

        payload_status = self.validate_payload(payload)
        if payload_status == 0:
            logger.warning("Received invalid payload: %s", headers)
            logger.debug("Payload content: %s", payload)
            return web.Response(status=400)

        if payload_status == 2:
            logger.info('Received "Test" payload')
            return web.Response()

        item = processor(payload)
        logger.info("Processing item: %s", item)
        logger.debug("Item details: %s", item)

        if isinstance(item, Movie):
            logger.info("Identified item as a Movie.")
            await self.handle_movie(item)
        elif isinstance(item, Series):
            logger.info("Identified item as a Series.")
            await self.handle_series(item)

        logger.debug("Finished processing request.")
        return web.Response()

    def validate_payload(self, payload: dict[str, Any]) -> int:
        """
        Validate the payload received from the webhook.

        Parameters
        ----------
        payload : dict[str, Any]
            The JSON payload from the webhook.

        Returns
        -------
        int
            Payload status: 0 for invalid, 1 for valid, 2 for test.
        """
        event_type = payload.get("eventType")
        logger.debug("Validating payload with eventType: %s", event_type)

        if not event_type:
            logger.warning("Payload missing 'eventType'.")
            return 0

        if event_type == "Test":
            return 2

        return 1

    async def handle_movie(self, movie: Movie) -> None:
        """
        Handle movie-specific logic for Radarr webhooks.

        Parameters
        ----------
        movie : Movie
            The movie object to handle.
        """
        logger.info("Handling movie: %s", movie)
        logger.debug("Movie details: %s", movie)

        if self.config.REMOVE_MEDIA:
            logger.info("Configured to delete movie. Proceeding with deletion.")
            logger.debug("Deleting movie from Radarr: %s", movie)
            await self.radarr_api.delete_movie(movie.id)
        else:
            logger.info("Configured to unmonitor movie. Fetching details.")
            movie_data = await self.radarr_api.get_movie(movie.id)

            if not movie_data:
                logger.warning("Movie not found in Radarr: %s", movie)
                return

            logger.debug("Fetched movie data: %s", movie_data)

            movie_data["monitored"] = False
            logger.info("Unmonitoring movie in Radarr: %s", movie)
            await self.radarr_api.unmonitor_movie(movie_data)

    async def handle_series(self, series: Series) -> None:
        """
        Handle series-specific logic for Sonarr webhooks.

        Parameters
        ----------
        series : Series
            The series object to handle.
        """
        logger.info("Handling series: %s", series)

        if self.config.HANDLE_EPISODES:
            logger.info("Unmonitoring episodes for series: %s", series.episodes)
            await self.sonarr_api.unmonitor_episodes(series)
        else:
            logger.info("Episode handling is disabled. Skipping handling for individual episodes.")

        # Check if we are allowed to handle series
        if not self.config.HANDLE_SERIES:
            logger.info(
                "Series handling is disabled. Skipping further handling for series: %s", series
            )
            return

        logger.info("Fetching series data from Sonarr for series ID: %s", series.id)
        series_data = await self.sonarr_api.get_series(series.id)

        if not series_data:
            logger.warning("Series not found in Sonarr: %s", series)
            return

        # Figure out if the series can be handled based on status
        can_handle = True
        if self.config.HANDLE_SERIES_ENDED_ONLY:
            logger.info("Checking if series has ended: %s", series)
            if not self.sonarr_api.series_is_ended(series_data):
                logger.info("Series is ongoing and cannot be handled: %s", series)
                can_handle = False
            else:
                logger.info("Series has ended: %s", series)

        if can_handle and self.sonarr_api.series_is_complete(series_data):
            logger.info("Series is complete and ready to handle: %s", series)
            if self.config.REMOVE_MEDIA:
                logger.info("Removing series from Sonarr: %s", series)
                await self.sonarr_api.delete_series(series.id)
            else:
                series_data["monitored"] = False
                await self.sonarr_api.unmonitor_series(series_data)
            logger.info("Series handling complete: %s", series)
        else:
            logger.info("Series cannot be handled further: %s", series)

    async def sonarr_endpoint(self, request: web.Request) -> web.Response:
        """
        Handle Sonarr webhook requests.

        Parameters
        ----------
        request : web.Request
            The incoming HTTP request.

        Returns
        -------
        web.Response
            The HTTP response.
        """
        logger.info("Handling Sonarr webhook request.")
        return await self.generic_handler(request, Series.from_payload)

    async def radarr_endpoint(self, request: web.Request) -> web.Response:
        """
        Handle Radarr webhook requests.

        Parameters
        ----------
        request : web.Request
            The incoming HTTP request.

        Returns
        -------
        web.Response
            The HTTP response.
        """
        logger.info("Handling Radarr webhook request.")
        return await self.generic_handler(request, Movie.from_payload)


def init_web_application() -> web.Application:
    """
    Initialize the web application with configured routes.

    Returns
    -------
    web.Application
        The aiohttp web application instance.
    """
    logger.debug("Initializing web application.")
    handler = WebhookHandler(Config())
    app = web.Application()
    app.add_routes(
        [
            web.post("/radarr", handler.radarr_endpoint),
            web.post("/sonarr", handler.sonarr_endpoint),
        ],
    )

    logger.debug("Routes added to the application.")
    return app
