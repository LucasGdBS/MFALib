from loguru import logger

logger.add("logs/debug.log", level="ERROR", rotation="100 MB")
