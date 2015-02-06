import os
import re
from setuptools import setup

# Grab __version__ from the actual module
__version__ = None
with open("php.py") as module:
    version_regex = re.compile(r'^__version__ = "(?P<version>[0-9.]+)"')
    for line in module.readlines():
        m = re.match(version_regex, line)
        if m:
            __version__ = m.group("version")
            break

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Get the long description from README.md
with open(os.path.join(os.path.dirname(__file__), "README.rst")) as description:
    setup(
        name="php",
        version=__version__,
        license="AGPLv3",
        description="Handle some of the strange standards in PHP projects",
        long_description=description.read(),
        url="https://github.com/danielquinn/python-php",
        download_url="https://github.com/danielquinn/python-php",
        author="Daniel Quinn",
        author_email="code@danielquinn.org",
        maintainer="Daniel Quinn",
        maintainer_email="code@danielquinn.org",
        tests_require=["nose"],
        test_suite="nose.collector",
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

