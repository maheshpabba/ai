from conf.models import JsonFile
import os
import logging
import json

PNG = 'png'
PDF = 'pdf'
JSON = 'json'

APPLICATION_JSON = "application/json"
APPLICATION_PDF = "application/pdf"
IMAGE_PNG = "image/png"

MONGO_COLL_FOR_USERS="Users"
MONGO_COLL_FOR_SESSIONS="Sessions"
MONGO_COLL_FOR_FILES="Files"
MONGO_COLL_FOR_STATISTICS="Statistics"
MONGO_COLL_FOR_CHATS="Chats"

# MONGO_COLL_FOR_USER_TRANSACTIONS = "UserTransactions"

LOGLEVEL= os.environ.get('WEBEXBOT_LOG_LEVEL','DEBUG').upper()

logConfig={   "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s | [%(levelname)s] | [%(module)s.%(name)s.%(funcName)s]:%(lineno)s >>> %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": getattr(logging,LOGLEVEL), "handlers": ["console"]},
        }


with open('/app/secrets/configs/config1.json') as f:
    c=json.load(f)

CONF=JsonFile(**c)


