import logging
import os

import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Populate the course list array with actual course names
graders = [
    "course-1",
    "course-2",
    "course-3",
]

ORG_NAME = os.environ.get('ORG_NAME')
GRADER_SERVICE_NAME = os.environ.get('GRADER_SERVICE_NAME')
GRADER_SERVICE_PORT = os.environ.get('GRADER_SERVICE_PORT')
GRADER_SERVICE_BASE_URL = f'http://{GRADER_SERVICE_NAME}:{GRADER_SERVICE_PORT}/services/{ORG_NAME}'
GRADER_SERVICE_COMMON_HEADERS = {'Content-Type': 'application/json'}

def add_grader(course_name: str) -> bytes:
    """Add a grader notebook by course and orge names

    Args:
      course_name: a string that represents the course name
      org_name: a string that represents the organization name

    Returns:
      True if successful, false otherwise

    Raises:
      json.JSONDecodeError if the response does not have a JSON body.
    """
    url = f'{GRADER_SERVICE_BASE_URL}/{course_name}'
    response = requests.post(url)
    if not response:
        raise ValueError('The setup course response body is empty')
    return response.content

def main():
    for course in graders:
        response = add_grader(course, f'{ORG_NAME}')
        logger.info(f'Reponse: {response}')

if __name__ == "__main__":
    main()
