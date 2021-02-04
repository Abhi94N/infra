import logging
import os
from os import curdir
from pathlib import Path
import shutil
import subprocess

from typing import List


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


load_dotenv()


class Utils:
    """Class used to migrate sqlite databases to postgres databases. These methods
    are primarily used for the nbgrader databases but can be adapted to any SQLite to
    Postgres database.

    If this class does not receive arguments to set attributes when instantiated it will
    create them from the values provided by the environment variables.

    Attributes:
      org: the organization name
      mnt_root: the path that designates the application's mount root, for example /mnt/efs/fs1
      org_graders_root_path: the shared grader account within the organization/home directory
      pg_user: the user for the postgres database. This user needs permissions to create databases.
      pg_pwd: the postgres database user's password.
      base_postgres_url: the connection string uri to connecto to the Postgres database without the database name
      gradebook_file_name: the sqlite database file name, for example gradebook.db
    """

    def __init__(
        self,
        org: str,
        mnt_root: str,
    ):
        if not org:
            self.org = os.getenv("ORGANIZATION_NAME")
        if not mnt_root:
            self.mnt_root = os.getenv("MNT_ROOT")

    def course_list(self) -> List[str]:
        """Creates a list of grader paths from the host

        Args:
            mnt_root: mount root for NFS/EFS on the host. Defaults to /mnt/efs/fs1.
            org_nam: the normalized organization name. Deafaults to an empty string.

        Returns:
            A list of strings for the full path for each grader folder for the organization.
        """
        course_list = []
        for dir in os.listdir(f"/{self.mnt_root}/{self.org_name}/home"):
            if "grader-" in dir:
                course_list += [course_list]
        return course_list
