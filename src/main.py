import asyncio
import signal
from typing import Any

from aiohttp import web

import log
from config import Config
from server import init_web_application

logger = log.get_logger(__name__)


async def main() -> None:
    config = Config()

    logger.info("Config loaded.")

    app = init_web_application(config)
    logger.debug("Initializing web application.")

    runner = web.AppRunner(app)
    await runner.setup()
    host = "0.0.0.0"  # noqa: S104
    port = 8080
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()

    logger.info("Server starting. Listening on %s:%s", host, port)

    # Use an event to wait for a shutdown signal
    stop_event = asyncio.Event()

    def handle_shutdown(signum: Any, _: Any) -> None:  # noqa: ANN401
        logger.info("Received shutdown signal: %s", signal.Signals(signum).name)
        stop_event.set()

    # Register signal handlers
    for signame in ("SIGINT", "SIGTERM"):
        signal.signal(getattr(signal, signame), handle_shutdown)

    try:
        await stop_event.wait()
    except (KeyboardInterrupt, asyncio.CancelledError) as e:
        logger.warning("Server shutdown started: %s", e.__class__.__name__)
    finally:
        logger.info("Cleaning up resources.")
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
