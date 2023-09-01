import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='MonitoringPlugins',
    packages=['MonitoringPlugins'],  # this must be the same as the name above
    package_data={'MonitoringPlugins': ['*/*', '*']},
    include_package_data=True,
    version='1.0.0',
    description='Simple API to manage the output for Nagios and Icinga Monitoring Plugins',
    author='Matthew Smith',
    author_email='matthew.smith@sol1.com.au',
    url='https://github.com/sol1-matt/MonitoringPlugins',  # use the URL to the github repo
    keywords=['Nagios', 'Icinga2', 'Monitoring', 'Plugins', 'Checks'],  # arbitrary keywords
    classifiers=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)