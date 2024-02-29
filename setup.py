import os
from setuptools import setup, find_packages


# # Utility function to read the README file.
# # Used for the long_description.  It's nice, because now 1) we have a top level
# # README file and 2) it's easier to type in the README file than to put a raw
# # string in below ...
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("README.md", "r") as fh:
    long_description = fh.read()

# Read dependencies from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="sol1-monitoring-plugins-lib",
    version="1.1.1",
    author='Matthew Smith',
    author_email='matthew.smith@sol1.com.au',
    description='Simple Library to manage the output for Nagios and Icinga Monitoring Plugins',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sol1/sol1-monitoring-plugins-lib',
    project_urls={
        "Bug Tracker": "https://github.com/sol1/sol1-monitoring-plugins-lib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=requirements,
    test_suite='tests',
)
