import sys
import datetime
from abc import ABC

from loguru import logger


class Logger(ABC):
    def __init__(self) -> None:
        self.logger = logger
        self.logger.remove()
        
        logger_format = (
            "<green><bold>{time:YYYY-MM-DD HH:mm:ss}</bold></green> | "
            "<level><bold>{level: <8}</bold></level> | "
            # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )
        self.logger.add(sys.stdout, format=logger_format)
        date = datetime.datetime.now().date()
        self.logger.add(
            f"./logs/{date}.log",
            rotation="100 MB",
            level="DEBUG",
            format=logger_format,
        )

    def __getattr__(self, name):
        return getattr(self.logger, name)

logger = Logger()