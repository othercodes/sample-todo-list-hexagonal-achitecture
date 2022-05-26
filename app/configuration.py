from os import getenv
from typing import Dict, Any


def main() -> Dict[str, Any]:
    return {
        'name': getenv('APP_NAME', 'Sample TO-DO List'),
        'timezone': getenv('APP_TIMEZONE', 'UTC')
    }


def database() -> Dict[str, Any]:
    return {
        'uri': getenv('DB_URI', 'sqlite:///to_do_list.db'),
    }


def logger() -> Dict[str, Any]:
    return {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'NOTSET',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'WARNING',
                'propagate': False
            },
            getenv('APP_NAME', 'health-monitor'): {
                'handlers': ['default'],
                'level': getenv('LOG_LEVEL', 'INFO'),
                'propagate': False
            },
        }
    }
