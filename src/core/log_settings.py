import sys
from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
    level="DEBUG",
)
