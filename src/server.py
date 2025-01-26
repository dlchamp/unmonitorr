from typing import Any

from aiohttp import web
from pydantic import ValidationError

import log
from arrs.radarr import RadarrClient
from arrs.sonarr import SonarrClient
from config import Config
from types_ import RadarrWebhookPayload, SonarrWebhookPayload

logger = log.get_logger(__name__)


PayloadType = RadarrWebhookPayload | SonarrWebhookPayload


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
    ) -> web.Response:
        """
        Generic handler for webhook payloads.

        Parameters
        ----------
        request : web.Request
            The incoming HTTP request.

        Returns
        -------
        web.Response
            The HTTP response.
        """
        payload = await request.json()
        headers = request.headers.items()

        logger.debug("Received request headers: %s", headers)
        logger.debug("Received request payload: %s", payload)

        if not (validated_model := self.validate_payload(payload)):
            logger.warning(
                "Incoming payload could not be validated. "
                "Did it originate from Sonarr or Radarr?: headers=%s, payload=%s",
                headers,
                payload,
            )
            return web.Response()

        if "test" in validated_model.event_type.lower():
            # this is a test payload from sonarr or radarr.
            logger.info("Received valid test payload from %s", validated_model.instance_name)
            return web.Response()

        logger.info(
            "Received '%s' event payload from %s",
            validated_model.event_type,
            validated_model.instance_name,
        )

        if isinstance(validated_model, RadarrWebhookPayload):
            await self.handle_movie(validated_model)
        else:
            await self.handle_series(validated_model)

        logger.debug("Finished processing request.")
        return web.Response()

    def validate_payload(self, payload: dict[str, Any]) -> PayloadType | None:
        """
        Validate the payload received from the webhook.

        Parameters
        ----------
        payload : dict[str, Any]
            The JSON payload from the webhook.

        Raises
        ------
        pydantic.ValidationError
            Error raised if the payload does not validate against any models.

        Returns
        -------
        PayloadType
            A validated RadarrPayload, RadarrTestPayload, SonarrTestPayload, or SonarrPayload.
        """
        valid_models: list[type[PayloadType]] = [
            RadarrWebhookPayload,
            SonarrWebhookPayload,
        ]

        for model in valid_models:
            try:
                return model.model_validate(payload)
            except ValidationError:
                continue

        return None

    async def handle_movie(self, payload: RadarrWebhookPayload) -> None:
        """
        Handle movie-specific logic for Radarr webhooks.

        Parameters
        ----------
        payload: RadarrPayload
            A movie payload from Radarr's webhook notifications.
        """
        movie = payload.movie
        logger.info("Handling movie: %s", movie)
        logger.debug("Movie Details: %s", movie.model_dump())

        if self.config.REMOVE_MEDIA:
            logger.info("Configured to delete movie. Proceeding with deletion.")
            logger.debug("Deleting movie from Radarr: %s", movie)
            await self.radarr_api.delete_movie(movie.id)
        else:
            logger.info("Configured to unmonitor movie. Fetching movie details from Radarr")
            api_movie = await self.radarr_api.get_movie_by_id(movie.id)

            if not api_movie:
                logger.warning("Unable to fetch movie from Radarr: %s", movie)
                return

            logger.debug("Fetched movie from Radarr: %s", api_movie)

            api_movie.unmonitor()
            logger.info("Unmonitoring movie in Radarr: %s", movie)
            await self.radarr_api.put_updated_movie(api_movie)

    async def handle_series(self, payload: SonarrWebhookPayload) -> None:
        """Handle series-specific logic for Sonarr webhooks.

        Parameters
        ----------
        payload : SonarrPayload
            The sonarr payload to handle.
        """
        series = payload.series
        logger.info("Handling series: %s", series)

        if self.config.HANDLE_EPISODES:
            logger.info("Unmonitoring episodes for series: %s", payload.episodes)
            await self.sonarr_api.unmonitor_episodes(payload)
        else:
            logger.info("Episode handling is disabled. Skipping handling for individual episodes.")

        # Check if we are allowed to handle series
        if not self.config.HANDLE_SERIES:
            logger.info(
                "Series handling is disabled. Skipping further handling for series: %s", series
            )
            return

        logger.info("Fetching series data from Sonarr for series ID: %s", series.id)
        api_series = await self.sonarr_api.get_series_by_id(series.id)

        if not api_series:
            logger.warning("Series not found in Sonarr: %s", series)
            return

        # Figure out if the series can be handled based on status
        can_handle = True
        if self.config.HANDLE_SERIES_ENDED_ONLY:
            logger.info("Checking if series has ended: %s", series)
            if not api_series.is_ended:
                logger.info("Series is ongoing and cannot be handled: %s", series)
                can_handle = False
            else:
                logger.info("Series has ended: %s", series)

        if can_handle and api_series.is_complete:
            logger.info("Series is complete and ready to handle: %s", series)
            if self.config.REMOVE_MEDIA:
                logger.info("Removing series from Sonarr: %s", api_series)
                await self.sonarr_api.delete_series(series)
            else:
                api_series.unmonitor_series()
                await self.sonarr_api.put_updated_series(api_series)
            logger.info("Series handling complete: %s", api_series)
        else:
            logger.info("Series cannot be handled further: %s", api_series)

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
        return await self.generic_handler(request)

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
        return await self.generic_handler(request)


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
