import logging
import logging.config


ERROR_LOG_FILENAME = 'chat_app.log'

FORMAT = "%(asctime)s:%(name)s:%(lineno)d " "%(levelname)s %(message)s"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOG_FILENAME,
            "backupCount": 2
        },
        "console": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "chat_app": {
            "level": "DEBUG",
            "handlers": [
                "logfile",
                "console",
            ],
        },
    },
}


def setup_logger():
    logging.config.dictConfig(LOGGING_CONFIG)
