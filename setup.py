from setuptools import find_packages, setup
import versioneer
import sys
from os import path

# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (
    3,
    8,
)
if sys.version_info < min_version:
    error = """
gallop-moca does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(*(sys.version_info[:2] + min_version))
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as readme_file:
    readme = readme_file.read()
requirements = [
    # package requirements go here
]

with open(path.join(here, "requirements.txt")) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [
        line
        for line in requirements_file.read().splitlines()
        if not line.startswith("#")
    ]

setup(
    name="gallop-moca",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A python package used to handle motion capture data and functions to model human movement.",
    license="MIT",
    author="Jesse Charlton",
    author_email="57236497+jchar32@users.noreply.github.com",
    url="https://github.com/jchar32/gallop-moca",
    packages=find_packages(exclude=["docs", "tests"]),
    entry_points={"console_scripts": ["gallop=gallop.cli:cli"]},
    install_requires=requirements,
    keywords="gallop-moca",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
    ],
)
