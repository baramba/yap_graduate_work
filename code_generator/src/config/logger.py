LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console']
TAG = 'worker_1'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': LOG_FORMAT,
            'level': 'DEBUG',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.UDPLogstashHandler',
            'host': 'logstash',
            'port': 5044,
            'version': 1,
            'tags': [TAG],  # список тег.
        },
    },

    'loggers': {
        '__main__': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'DEBUG',
            'propagate': False,
        },
    },

    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}