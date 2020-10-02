from dotenv import load_dotenv

load_dotenv()

from os import curdir
from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import shutil
import subprocess
import os

org_name = os.environ.get('ORGANIZATION_NAME') or 'my-org'
illumidesk_mnt_root = '/mnt/efs/fs1/'

org_graders_root_path = Path(illumidesk_mnt_root).joinpath(org_name).joinpath('home')

pg_database_name_prefix = os.environ.get('POSTGRES_NBGRADER_DB_PREFIX') or 'illumidesk'
pg_database_user= os.environ.get('POSTGRES_NBGRADER_USER')
pg_database_pwd= os.environ.get('POSTGRES_NBGRADER_PASSWORD')
pg_database_host= os.environ.get('POSTGRES_NBGRADER_HOST')
base_postgres_url = f'postgresql://{pg_database_user}:{pg_database_pwd}@{pg_database_host}/'


def run_migration() -> None:
    """
    Migrates all the data from gradebooks files within the organization
    """
    if shutil.which('pgloader') is None:
        raise 'pgloader is not installed'

    print(f'using {org_graders_root_path} to find gradebooks...')
    for file_path in org_graders_root_path.glob('**/gradebook.db'):
        # do the migration with this gradebook file
        print(f'gradebook located in: {file_path}')
        course_id = file_path.parent.name
        print('course_id to use:', course_id)
        course_db_name = f'{pg_database_name_prefix}_{course_id}'
        os.environ['SQLITE_DB_PATH'] = f'{file_path}'
        os.environ['POSTGRES_DB_URL'] = f'{base_postgres_url}{course_db_name}'
        create_pg_database(course_db_name)
        migration_result = subprocess.check_output('pgloader migrate.load'.split(), cwd=f'{os.getcwd()}')

        print('result %s' % migration_result.decode())



def create_pg_database(db_name: str) -> None:
    """
    Creates new database on postgres
    """
    with psycopg2.connect(f'user={pg_database_user} password={pg_database_pwd} host={pg_database_host}') as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        try:
            with conn.cursor() as cur:
                cur.execute(f'CREATE DATABASE "{db_name}";')
        except Exception as e:
            # database exists?
            print('error creating database:', e)
            pass


if __name__ == '__main__':
    run_migration()
