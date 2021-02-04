import os
import sys

from setuptools import setup
from setuptools import find_packages


v = sys.version_info
if v[:2] < (3, 6):
    error = "ERROR: This package requires Python version 3.6 or above."
    print(error, file=sys.stderr)
    sys.exit(1)

shell = False
if os.name in ("nt", "dos"):
    shell = True
    warning = "WARNING: Windows is not officially supported"
    print(warning, file=sys.stderr)

# Get the current package version.
here = os.path.abspath(os.path.dirname(__file__))
version_ns = {}
with open(os.path.join("_version.py")) as f:
    exec(f.read(), {}, version_ns)

setup(
    name="sqlite2docker",
    version=version_ns["__version__"],
    description="sqlite2docker utility package based on pgloader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/illumidesk/infra",
    author="The IllumiDesk Team",
    author_email="hello@illumidesk.com",
    license="MIT",
    packages=find_packages(exclude="./tests"),
    install_requires=[
        "docker==4.3.1",
        "psycopg2-binary==2.8.6",
        "python-dotenv==0.14.0",
        "tornado==6.1",
    ],  # noqa: E231
    package_data={
        "": ["*.html"],
    },  # noqa: E231
)
