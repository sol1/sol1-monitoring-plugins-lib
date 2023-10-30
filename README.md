# Monitoring Plugins
Monitoring Plugins are tools to assist in the creation of monitoring checks for Icinga2 and Nagios.


## MonitoringPlugin
```python
from MonitoringPlugins import MonitoringPlugin
```
This class manages the state, output message and performance data of your check as well as returning this data and exiting the script.

It has been designed so you can add multiple tests and the class will intelligently manage the state and output for you. 

__Documentation__
You can find documentation in the [`docs`](./docs/monitoring_plugins.md) folder. 
Code examples can be found in the [`examples`](./examples/check_day_of_the_week.py) folder.


# Development
Contributions are welcome, changes need to be backwards compatible as this library is used by 100's of monitoring checks.
## Setup
```
python3 -m pip install --upgrade pip setuptools wheel twine pytest
python3 -m pip install -r requirements.txt
```
## Build
```
python3 .\setup.py sdist bdist_wheel
```
## Tests
Install build package to current directory 
```
python3 -m pip install -e .
```
Run tests
```
python3 -m pytest tests/
```
## Deploy 
```
python3 -m twine upload dist/*
```
