from typing import Any

import aiohttp

from unmonitorr import log

__all__ = (
    "BaseArrClient",
    "HTTPException",
)

logger = log.get_logger(__name__)


class HTTPException(Exception):
    def __init__(self, response: aiohttp.ClientResponse, message: str | None = None) -> None:
        self.status = response.status
        self.url = str(response.url)
        self.method = response.method
        self.headers = response.headers
        self.reason = response.reason

        self.message = message

        error_details = f"HTTP {self.status} {self.reason} for {self.method} {self.url}"
        if message:
            error_details += f" | Details: {message}"

        super().__init__(error_details)


class BaseArrClient:

    __slots__ = (
        "api_key",
        "uri",
    )

    def __init__(self, uri: str, api_key: str) -> None:
        self.uri = uri
        self.api_key = api_key

        if self.disabled:
            logger.warning(
                "%s is missing required configuration details -- Disabled.",
                self.__class__.__name__,
            )
            return

        logger.debug(
            "Initialized %s with base_url: %s",
            self.__class__.__name__,
            self.base_url,
        )

    @property
    def disabled(self) -> bool:
        """Return True if uri or api_key is missing."""
        return not self.uri or not self.api_key

    @property
    def base_url(self) -> str:
        """Sonarr and Radarr use `/api/v3` as part of the base URL."""
        return f"{self.uri}/api/v3"

    @property
    def headers(self) -> dict[str, str]:
        """Sonarr and Radarr also use the same headers."""
        return {"X-API-Key": self.api_key, "Accept": "application/json"}

    def update_client_config(self, uri: str, api_key: str) -> None:
        self.uri = uri
        self.api_key = api_key
        self.headers["X-API-Key"] = api_key

    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        logger.debug(
            "Performing %s request: URL=%s, headers=%s, json=%s, params=%s",
            method,
            url,
            headers,
            json,
            params,
        )

        async with (
            aiohttp.ClientSession() as session,
            session.request(method, url, headers=headers, params=params, json=json) as response,
        ):
            logger.debug(
                "Response received: URL=%s, status=%s",
                response.url,
                response.status,
            )
            try:
                return await response.json()
            except aiohttp.ContentTypeError as e:
                raise HTTPException(response, str(e)) from None
