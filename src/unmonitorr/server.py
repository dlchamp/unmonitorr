from typing import Any

from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from pydantic import ValidationError

from unmonitorr import log
from unmonitorr.arrs import HTTPException, RadarrClient, SonarrClient
from unmonitorr.config import Config
from unmonitorr.types_ import RadarrWebhookPayload, SonarrWebhookPayload

logger = log.get_logger(__name__)


PayloadTypeT = RadarrWebhookPayload | SonarrWebhookPayload


class WebhookHandler:
    """Handles webhook requests for Radarr and Sonarr.

    Parameters
    ----------
    config : Config
        Configuration object containing API credentials and settings.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.radarr_api = RadarrClient(
            config.radarr_uri,
            config.radarr_api_key,
        )
        self.sonarr_api = SonarrClient(
            config.sonarr_uri,
            config.sonarr_api_key,
        )
        logger.debug("Initialized WebhookHandler")

    async def generic_handler(
        self,
        request: web.Request,
    ) -> web.Response:
        """Generic handler for webhook payloads.

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

    def validate_payload(self, payload: dict[str, Any]) -> PayloadTypeT | None:
        """Validate the payload received from the webhook.

        Parameters
        ----------
        payload : dict[str, Any]
            The JSON payload from the webhook.


        Returns
        -------
        PayloadType | None
            A validated RadarrPayload, SonarrWebhookPayload, or None if not a valid payload.
        """
        valid_models: list[type[PayloadTypeT]] = [
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
        """Handle movie-specific logic for Radarr webhooks.

        Parameters
        ----------
        payload: RadarrWebhookPayload
            A movie payload from Radarr's webhook notifications.
        """
        if self.radarr_api.disabled:
            logger.info("Radarr client is missing a valid configuration -- Cannot access API.")
            return

        movie = payload.movie
        logger.info("Handling movie: %s", movie)
        logger.debug("Movie Details: %s", movie.model_dump())

        if self.config.remove_media:
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
        payload : SonarrWebhookPayload
            The series payload from Sonarr's webhook notifications.
        """
        if self.sonarr_api.disabled:
            logger.info("Sonarr client is missing a valid configuration -- Cannot access API.")
            return

        series = payload.series
        logger.info("Handling series: %s", series)

        # Check if we are allowed to handle the series.
        if self.config.handle_episodes:
            logger.info("Unmonitoring episodes for series: %s", payload.episodes)
            await self.sonarr_api.unmonitor_episodes(payload)
        else:
            logger.info("Episode handling is disabled. Skipping handling for individual episodes.")

        # Check if we are allowed to handle series
        if not self.config.handle_series:
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
        if self.config.handle_series_ended_only:
            logger.info("Checking if series has ended: %s", series)
            if not api_series.is_ended:
                logger.info("Series is ongoing and cannot be handled: %s", series)
                can_handle = False
            else:
                logger.info("Series has ended: %s", series)

        if can_handle and api_series.is_complete:
            logger.info("Series is complete and ready to handle: %s", series)
            if self.config.remove_media:
                logger.info("Removing series from Sonarr: %s", api_series)
                await self.sonarr_api.delete_series(series, exclude=self.config.exclude_series)
            else:
                api_series.unmonitor_series()
                await self.sonarr_api.put_updated_series(api_series)
            logger.info("Series handling complete: %s", api_series)
        else:
            logger.info("Series cannot be handled further: %s", api_series)

    async def sonarr_endpoint(self, request: web.Request) -> web.Response:
        """Handle Sonarr webhook requests.

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


class Configurator:
    """Represents the configurator that handles changing Unmonitorr's config."""

    def __init__(self, config: Config, webhook_handler: WebhookHandler) -> None:
        self.config = config
        self.webhook_handler = webhook_handler

    def update_radarr_client(self, radarr_uri: str, radarr_api_key: str) -> None:
        self.webhook_handler.radarr_api.update_client_config(radarr_uri, radarr_api_key)

        logger.info("Radarr configuration updated.")
        logger.debug(
            "RadarrClient has been updated: URI=%s, API=%s",
            radarr_uri,
            radarr_api_key,
        )
        if self.webhook_handler.radarr_api.disabled:
            logger.info("Radarr client missing required configuration -- API requests disabled.")

    def update_sonarr_client(self, sonarr_uri: str, sonarr_api_key: str) -> None:
        self.webhook_handler.sonarr_api.update_client_config(sonarr_uri, sonarr_api_key)

        logger.info("Sonarr configuration updated.")
        logger.debug(
            "SonarrClient has been updated: URI=%s, API=%s",
            sonarr_uri,
            sonarr_api_key,
        )
        if self.webhook_handler.sonarr_api.disabled:
            logger.info("Sonarr client missing required configuration -- API requests disabled.")

    async def setup_page(self, _: web.Request) -> web.Response:

        env = Environment(loader=FileSystemLoader("unmonitorr/static"), autoescape=True)
        html = env.get_template("index.html")
        config_dict = self.config.to_dict()
        rendered = html.render(config_dict)
        return web.Response(text=rendered, content_type="text/html")

    async def save_config(self, request: web.Request) -> web.Response:
        logger.info("Received request to update the config.")
        if request.method == "POST":
            data = await request.post()
            logger.debug("Configuration Data: %s", data)
            radarr_uri = str(data.get("radarr_uri", "")).strip()
            radarr_api_key = str(data.get("radarr_api_key", "")).strip()
            sonarr_uri = str(data.get("sonarr_uri", "")).strip()
            sonarr_api_key = str(data.get("sonarr_api_key", "")).strip()
            handle_episodes = data.get("handle_episodes") == "on"
            handle_series = data.get("handle_series") == "on"
            exclude_series = data.get("exclude_series") == "on"
            handle_series_ended_only = data.get("handle_series_ended_only") == "on"
            remove_media = data.get("remove_media") == "on"

            is_updated = False

            if radarr_uri != self.config.radarr_uri or radarr_api_key != self.config.radarr_api_key:
                logger.info("Received new Radarr config - Updating client")
                self.config.radarr_uri = radarr_uri
                self.config.radarr_api_key = radarr_api_key
                self.update_radarr_client(radarr_uri, radarr_api_key)
                is_updated = True

            if sonarr_uri != self.config.sonarr_uri or sonarr_api_key != self.config.sonarr_api_key:
                logger.info("Received new Sonarr config -- Updating client.")
                self.config.sonarr_uri = sonarr_uri
                self.config.sonarr_api_key = sonarr_api_key
                self.update_sonarr_client(sonarr_uri, sonarr_api_key)
                is_updated = True

            if (
                self.config.handle_episodes != handle_episodes
                or self.config.handle_series != handle_series
                or self.config.exclude_series != exclude_series
                or self.config.handle_series_ended_only != handle_series_ended_only
                or self.config.remove_media != remove_media
            ):
                logger.info("Updating handling rules.")
                self.config.handle_episodes = handle_episodes
                self.config.handle_series = handle_series
                self.config.exclude_series = exclude_series
                self.config.handle_series_ended_only = handle_series_ended_only
                self.config.remove_media = remove_media
                is_updated = True

            if is_updated:
                logger.info("New configuration has been saved.")
                self.config.save()

            return web.Response()

        return web.Response(status=405)

    async def ping_arr_server(self, request: web.Request) -> web.Response:
        """Ping the arr server, proxy for the JS validation."""
        data = await request.json()
        uri = data.get("uri") or "MISSING"
        api_key = data.get("api_key") or "MISSING"
        client = data.get("client")

        if "MISSING" in (uri, api_key):
            logger.info(
                "Could not test %s with missing values: uri=%s, key=%s",
                client,
                uri,
                api_key,
            )
            return web.Response(status=401, text="URI or API KEY missing.")

        url = f"{uri}/api"
        headers: dict[str, str] = {"Content-Type": "application/json", "X-API-Key": api_key}

        logger.info("Pinging %s: url=%s", client, url)

        try:
            response = await self.webhook_handler.radarr_api.request("GET", url, headers=headers)
        except HTTPException as e:
            logger.info("Validation Response: status=%s, reason=%s", e.status, e.reason)
            return web.Response(status=e.status, text=e.reason)

        logger.info("%s validation success", client)
        logger.debug("Validation Response: %s", response)
        return web.json_response(response)


def init_web_application(config: Config) -> web.Application:
    """Initialize the web application with configured routes.

    Returns
    -------
    web.Application
        The aiohttp web application instance.
    """
    logger.debug("Initializing web application.")
    handler = WebhookHandler(config)
    configurator = Configurator(config, handler)
    app = web.Application()
    app.router.add_static("/static/", path="unmonitorr/static", name="static")
    app.add_routes(
        [
            web.post("/radarr", handler.radarr_endpoint),
            web.post("/sonarr", handler.sonarr_endpoint),
            web.get("/setup", configurator.setup_page),
            web.post("/save-config", configurator.save_config),
            web.post("/test-arr", configurator.ping_arr_server),
        ],
    )

    logger.debug("Routes added to the application.")
    return app
