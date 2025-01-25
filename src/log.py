import logging
import logging.handlers
from pathlib import Path

import coloredlogs  # type: ignore

from config import LogConfig

# setup logging format
format_string: str = "%(asctime)s | %(module)s | %(levelname)s | %(message)s"
formatter: logging.Formatter = logging.Formatter(format_string)

# set stdout logger to INFO
logger: logging.Logger = logging.getLogger()
logger.setLevel(LogConfig.LOG_LEVEL)


stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(LogConfig.LOG_LEVEL)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# setup logging file
log_file = Path("logs/unmonitorr.log")
log_file.parent.mkdir(exist_ok=True)

# setup logger file handler
# starts a new log file each day at midnight, UTC
# keeps no more than 10 days worth of logs.
file_handler = logging.handlers.TimedRotatingFileHandler(
    log_file, "midnight", utc=True, backupCount=10, encoding="utf-8"
)

file_handler.setLevel(LogConfig.LOG_LEVEL)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

coloredlogs.DEFAULT_LEVEL_STYLES = {
    "info": {"color": coloredlogs.DEFAULT_LEVEL_STYLES["info"]},
    "critical": {"color": 9},
    "warning": {"color": 11},
}

logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)


# Apply coloredlogs to the stdout handler
coloredlogs.install(level=LogConfig.LOG_LEVEL, logger=logger, stream=stdout_handler.stream)  # type: ignore


def get_logger(name: str) -> logging.Logger:
    """Return a logger."""
    return logging.getLogger(name)
