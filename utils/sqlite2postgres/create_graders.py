import json
import logging
import os
from typing import Dict

from tornado.httpclient import AsyncHTTPClient

import requests

from .migrator import Migrator
from . import common


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


migrator = Migrator()
course_list = migrator.course_list()
org = migrator.org


# course setup service name
INTENAL_SERVICE_NAME = os.environ.get('DOCKER_SETUP_COURSE_SERVICE_NAME') or 'setup-course'
# course setup service port
SERVICE_PORT = os.environ.get('DOCKER_SETUP_COURSE_PORT') or '8000'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


SERVICE_BASE_URL = f'http://{INTENAL_SERVICE_NAME}:{SERVICE_PORT}'
SERVICE_COMMON_HEADERS = {'Content-Type': 'application/json'}


def get_current_service_definitions() -> str:
    """
    Gets the file content that contains the new services and groups that are used as grader services

    Returns: the contents of configuration file
    """
    # get the response from service config endpoint
    response = requests.get(f'{SERVICE_BASE_URL}/config')
    # store course setup configuration
    config = response.json()
    return config


async def register_new_service(data: Dict[str, str]) -> str:
    """
    Helps to register (asynchronously) new course definition through the setup-course service

    Args:
        data: a dict with the org, course_id (label) and the domain.

    Example:
    ```await SetupCourseService.register_new_service(data = {
            'org': org,
            'course_id': course_id,
            'domain': handler.request.host,
        })```

    Returns: the response as json

    """
    client = AsyncHTTPClient()

    response = await client.fetch(
        SERVICE_BASE_URL,
        headers=SERVICE_COMMON_HEADERS,
        body=json.dumps(data),
        method='POST',
    )
    if not response.body:
        raise json.JSONDecodeError('The setup course response body is empty', '', 0)
    resp_json = json.loads(response.body)
    logger.debug(f'Setup-Course service response: {resp_json}')
    return resp_json
