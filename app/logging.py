import logging
import sys

DEBUG_LEVEL = logging.getLevelName(logging.DEBUG)
INFO_LEVEL = logging.getLevelName(logging.INFO)


def get_logging_config(log_level: str = INFO_LEVEL) -> dict:
    main_logger = 'console'
    main_logger_config = {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
        'stream': sys.stdout,
        'level': log_level,
    }

    log_format = (
        '%(log_color)s%(asctime)s [%(levelname)s] [%(name)s] %(message)s (%(filename)s:%(lineno)d)'
    )

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': log_format,
                '()': 'colorlog.ColoredFormatter',
                'log_colors': {
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
            },
        },
        'handlers': {
            main_logger: {**main_logger_config},
            'blackhole': {'level': DEBUG_LEVEL, 'class': 'logging.NullHandler'},
        },
        'loggers': {
            'fastapi': {'level': INFO_LEVEL, 'handlers': [main_logger]},
            'uvicorn': {'level': INFO_LEVEL, 'handlers': [main_logger], 'propagate': False},
            '': {
                'level': log_level,
                'handlers': [main_logger],
                'propagate': True,
            },
        },
    }
