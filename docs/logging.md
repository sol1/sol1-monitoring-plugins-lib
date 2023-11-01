# Monitoring Logging
This library provides utilities for initializing logging that is check friendly and simple to deploy and manage, the logger used is loguru.

## Constants
`DEFAULT_LOG_LEVELS = ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']`: List of valid logging levels used to validate logging level supplied. Append to this last and pass it to initization if you add custom logging levels.

## Functions
### initLogging()
Initization of the logging with sensible defaults and output format for monitoring checks.

The function performs the following tasks:

1. Removes existing loggers.
1. Adds a screen logger to standard error if `enable_screen_debug` is `True`.
1. Adds a file logger with rotation and retention policies if `enable_log_file` is `True`.
1. Logs an initialization message with the final configuration if `log_level` is `DEBUG`.

Log retention is short and log level is `WARNING` as by default so only problems are logged and they aren't kept for long.

```python
initLogging(debug=False,
            enable_screen_debug=False,
            enable_log_file=True,
            log_file='/var/log/icinga2/check_monitoring.log',
            log_rotate='1 day',
            log_retention='3 days',
            log_level='WARNING',
            available_log_levels=DEFAULT_LOG_LEVELS,
            **kwargs)
```
__Parameters:__
`debug` (optional): If True, sets the log level to `DEBUG`. Defaults to `False`.
`enable_screen_debug` (optional): If True, enables screen logging to standard error. Defaults to `False`.
`enable_log_file` (optional): If True, enables file logging. Defaults to `True`.
`log_file` (optional): The path to the log file. Defaults to `/var/log/icinga2/check_monitoring.log`.
`log_rotate` (optional): The log file rotation policy. Defaults to `1 day`.
`log_retention` (optional): The log file retention policy. Defaults to `3 days`.
`log_level` (optional): The logging level. Defaults to `WARNING`.
`available_log_levels` (optional): A list of available logging levels. Defaults to `DEFAULT_LOG_LEVELS`.
`**kwargs` : Legacy variables to override function arguments if they exist.


## initLoggingArgparse()
Adds Argparse arguments to be passed to `initLogging()`

```python
initLoggingArgparse(parser,
                    log_file='/var/log/icinga2/check_monitoring.log',
                    log_rotate='1 day',
                    log_retention='3 days',
                    log_level='WARNING',
                    available_log_levels=DEFAULT_LOG_LEVELS)
```

__Parameters:__
`log_file` (optional): The path to the log file. Defaults to `/var/log/icinga2/check_monitoring.log`.
`log_rotate` (optional): The log file rotation policy. Defaults to `1 day`.
`log_retention` (optional): The log file retention policy. Defaults to `3 days`.
`log_level` (optional): The logging level. Defaults to `WARNING`.
`available_log_levels` (optional): A list of available logging levels. Defaults to `DEFAULT_LOG_LEVELS`.

__Argparse Arguments Added:__
Flags
`--debug`
`--enable-screen-debug`
`--disable-log-file`
_Note: `--disable-log-file` should get inversly passed to the `enable_log_file`, this is done so the user is explictly disabling the log file, the opposite of the default which is enabled._

Keyword arguments
`--log-file`
`--log-rotate`
`--log-retention`
`--log-level`
_Note: there is no argument `--available-log-levels` added to argparse, the avaiable log levels are only used to provide choices for `--log-level`._