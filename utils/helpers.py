import logging

import settings
import requests_async as requests

QuestionIndex = "question"
ChoiceIndex = "choice"

def get_logger(name: str='__main__', handler=None, formatter=None):
    if not handler:
        handler = settings.LOG_HANDLER

    if not formatter:
        formatter = settings.LOF_FORMATTER

    if not handler.formatter:
        handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL)

    return logger

logger = get_logger(__name__)

async def addToElastic(index, id, data):
    url = f'{settings.ELASTIC_HOST}/{index}/_doc/{id}'
    
    logger.debug(f'url for add is {url}')

    await requests.post(url, json=data)

async def deleteFromElastic(index, id):
    url = f'{settings.ELASTIC_HOST}/{index}/_doc/{id}'

    logger.debug(f'url for add is {url}')

    await requests.delete(url)

async def getFromElastic(index, id):
    url = f'{settings.ELASTIC_HOST}/{index}/_doc/{id}'

    logger.debug(f'url for add is {url}')

    resp = await requests.get(url)
    resp_json = resp.json()

    return resp_json