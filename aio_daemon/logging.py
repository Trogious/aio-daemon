import logging
import os
from logging.handlers import RotatingFileHandler

from .env import getenv_path

AIO_DAEMON_LOGGER_NAME = 'aio_daemon_logger'
AIO_DAEMON_LOG_PATH = './aio_daemon.log'


class Logger:
    logger = None

    @staticmethod
    def get_logger(name=os.getenv('AIO_DAEMON_LOGGER_NAME', AIO_DAEMON_LOGGER_NAME),
                   path=getenv_path('AIO_DAEMON_LOG_PATH', AIO_DAEMON_LOG_PATH), level=logging.INFO, max_bytes=204800,
                   backup_count=4):
        if Logger.logger is None:
            Logger.logger = logging.getLogger(name)
            Logger.logger.setLevel(level)
            handler = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count)
            handler.setFormatter(logging.Formatter(
                '%(asctime)s|%(levelname)s|%(lineno)d|%(message)s', '%Y-%m-%d %H:%M:%S'))
            Logger.logger.addHandler(handler)
            logging.getLogger("asyncio").addHandler(handler)
        return Logger.logger
