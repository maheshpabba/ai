from conf.constants import LOGLEVEL,logConfig
from logging.config import dictConfig
import logging
import uvicorn
import os

# log = logging.getLogger(__name__)
# log.propagate = True

dictConfig(logConfig)


if __name__ == "__main__":
    logging.info('starting the fastapi server')
    uvicorn.run("routes:app", host="0.0.0.0",port=5000,reload=True)
   