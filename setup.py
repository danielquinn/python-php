import os
import re
from setuptools import setup

def get_version():
    version_file = os.path.join(
        os.path.dirname(__file__),
        'php',
        '__init__.py'
    )
    with open(version_file) as f:
        regex = re.compile("^__version__.*?(?P<version>[\d.]+).*")
        for line in f.readlines():
            m = regex.match(line)
            if m:
                return m.group("version")

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Get the long description from README.md
with open(os.path.join(os.path.dirname(__file__), "README.rst")) as description:
    setup(
        name="php",
        version=get_version(),
        license="AGPLv3",
        description="Handle some of the strange standards in PHP projects",
        long_description=description.read(),
        url="https://github.com/danielquinn/python-php",
        download_url="https://github.com/danielquinn/python-php",
        author="Daniel Quinn",
        author_email="code@danielquinn.org",
        maintainer="Daniel Quinn",
        maintainer_email="code@danielquinn.org",
        packages=["php"],
        classifiers=[
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: PHP",
            "Topic :: Internet :: WWW/HTTP",
        ],
    )

