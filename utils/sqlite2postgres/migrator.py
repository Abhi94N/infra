import logging
import os
from os import curdir
from pathlib import Path
import shutil
import subprocess

from typing import List

from dotenv import load_dotenv

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2

from .utils import course_list


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


load_dotenv()


class Migrator:
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
        pg_user: str,
        pg_pwd: str,
        pg_host: str,
        pg_port: int,
        gradebook_file_name: str,
    ):
        if not org:
            self.org = os.getenv("ORGANIZATION_NAME")
        if not mnt_root:
            self.mnt_root = os.getenv("MNT_ROOT")
        if not pg_user:
            self.pg_user = os.getenv("POSTGRES_USER")
        if not pg_pwd:
            self.pg_pwd = os.getenv("POSTGRES_PASSWORD")
        if not pg_port:
            self.pg_port = os.getenv("POSTGRES_PORT")
        if not pg_host:
            self.pg_host = os.getenv("POSTGRES_HOST")
        if not gradebook_file_name:
            self.gradebook_file_name = os.getenv("SQLITE_DB_FILENAME")

        self.org_graders_root_path = (
            Path(self.mnt_root).joinpath(self.org).joinpath("home")
        )
        self.base_postgres_url = f"postgresql://{pg_user}:{pg_pwd}@{pg_host}:{pg_port}"

    def run_migration(self) -> None:
        """
        Migrates all the data from gradebooks files within the organization
        """
        if shutil.which("pgloader") is None:
            raise "pgloader is not available in PATH"
        logger.info(f"Using {self.org_graders_root_path} to find gradebooks...")
        course_list = course_list
        for course_name in course_list:
            course_path = Path(f"{self.mnt_root}/{self.org}/home/grader-{course_name}")
            grader_path = Path(course_path)
            gradebook_path = grader_path.joinpath(course_name).joinpath(
                self.gradebook_file_name
            )
            logger.info("Gradebook path for SQLite file location: %s", gradebook_path)
            # do the migration with gradebook file fetched from a path item in the directory list
            if gradebook_path.exists():
                logger.info("Gradebook file located in: %s", gradebook_path)
                course_db_name = f"{self.org}_{course_name}"
                os.environ["SQLITE_DB_PATH"] = f"{gradebook_path}"
                os.environ[
                    "POSTGRES_DB_URL"
                ] = f"{self.base_postgres_url}/{course_db_name}"
                self.create_pg_database(course_db_name)
                migration_result = subprocess.check_output(
                    "pgloader migrate.tmpl".split(), cwd=f"{os.getcwd()}"
                )
                logger.info("Result %s" % migration_result.decode())

    def create_pg_database(self, db_name: str) -> None:
        """
        Creates new database within the Postgres database instance.

        Args:
          db_name: the database name
        """
        with psycopg2.connect(
            f"user={self.pg_user} password={self.pg_pwd} host={self.pg_host}"
        ) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            try:
                with conn.cursor() as cur:
                    cur.execute(f'CREATE DATABASE "{db_name}";')
                    logger.info("Created database: %s", db_name)
            except Exception as e:
                # database exists?
                logger.debug("Error creating database: %s", e)
                pass
