from typing import Any
import aiohttp
import log

logger = log.get_logger(__name__)


class HTTPException(Exception):
    def __init__(self, response: aiohttp.ClientResponse, message: Any | None = None) -> None:
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

    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        json: dict[str, Any] | None = None,
        params: dict[str, str | int | float] | None = None,
    ) -> dict[str, Any]:

        logger.debug(
            "Performing %s request: URL=%s, headers=%s, json=%s, params=%s",
            method,
            url,
            headers,
            json,
            params,
        )

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, headers=headers, params=params, json=json
            ) as response:
                logger.debug(
                    "Response received: URL=%s, status=%s",
                    response.url,
                    response.status,
                )
                try:

                    return await response.json()
                except aiohttp.ContentTypeError as e:
                    raise HTTPException(response, e) from None
