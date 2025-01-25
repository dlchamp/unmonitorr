from config import Config
from server import init_web_application
import asyncio
from aiohttp import web
import log


logger = log.get_logger(__name__)


async def main() -> None:
    Config.validate()
    logger.debug("Configuration validated successfully")

    app = init_web_application()
    logger.debug("Initializing web application.")

    runner = web.AppRunner(app)
    await runner.setup()
    host = "0.0.0.0"
    port = 8080
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()

    logger.info("Server starting. Listening on %s:%s", host, port)

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, asyncio.CancelledError) as e:
        logger.warning("Server shutdown started: %s", e.__class__.__name__)

    await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
