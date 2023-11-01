
import os
import sys
from loguru import logger

DEFAULT_LOG_LEVELS = ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']


def initLoggingArgparse(parser,
                        log_file='/var/log/icinga2/check_monitoring.log',
                        log_rotate='1 day',
                        log_retention='3 days',
                        log_level='WARNING',
                        available_log_levels=DEFAULT_LOG_LEVELS,
                        ):
    """
    Initalize argparse arguments for logging, you can change the argparse argument defaults with the function arguments

    Args:
        parser (obj): Argparse parser object
        log_file (str, optional): Override default argument value for --log-file. Defaults to '/var/log/icinga2/check_monitoring.log'.
        log_rotate (str, optional): Override default argument value for --log-rotate. Defaults to '1 day'.
        log_retention (str, optional): Override default argument value for --log-retention. Defaults to '3 days'.
        log_level (str, optional): Override default argument value for --log-level. Defaults to 'WARNING'.
        available_log_levels (list, optional): Override default argument value for --available-log-levels. Defaults to DEFAULT_LOG_LEVELS.
    """
    parser.add_argument('--debug', action="store_true", help="Sets the log level to DEBUG.")
    parser.add_argument('--enable-screen-debug', action="store_true", help="Enables screen logging to standard error.")
    parser.add_argument('--disable-log-file', action="store_true", help="Disables file logging")
    parser.add_argument('--log-file', type=str, default=log_file, help="The path to the log file")
    parser.add_argument('--log-rotate', type=str, default=log_rotate, help="The log file rotation policy")
    parser.add_argument('--log-retention', type=str, default=log_retention, help="The log file retention policy")
    parser.add_argument('--log-level', type=str, choices=available_log_levels,
                        default=log_level, help="The logging level")


def initLogging(debug=False,
                enable_screen_debug=False,
                enable_log_file=True,
                log_file='/var/log/icinga2/check_monitoring.log',
                log_rotate='1 day',
                log_retention='3 days',
                log_level='WARNING',
                available_log_levels=DEFAULT_LOG_LEVELS,
                **kwargs
                ):
    """
    Initalize logging for monitoring checks.
    It defaults to logging to file for WARNING level and above, the log files autorotate with compression and retention.
    The log format includes the date and process id so you can identify all log entries from the same run.

    Args:
        debug (bool, optional): If True, sets the log level to DEBUG. Defaults to False.
        enable_screen_debug (bool, optional): If True, enables screen logging to standard error. Defaults to False.
        enable_log_file (bool, optional): If True, enables file logging. Defaults to True.
        log_file (str, optional): The path to the log file. Defaults to '/var/log/icinga2/check_monitoring.log'.
        log_rotate (str, optional): The log file rotation policy. Defaults to '1 day'.
        log_retention (str, optional): The log file retention policy. Defaults to '3 days'.
        log_level (str, optional): The logging level. Defaults to 'WARNING'.
        available_log_levels (list, optional): A list of available logging levels. Aliased as available_log_levels. Defaults to DEFAULT_LOG_LEVELS.

    """
    #
    # Legacy vars, will override function args if they exist
    # If true screen logging is added to standard error
    enable_screen_debug = kwargs.get('enableScreenDebug', enable_screen_debug)
    enable_log_file = kwargs.get('enableLogFile', enable_log_file)
    log_file = kwargs.get('logFile', log_file)
    log_rotate = kwargs.get('logRotate', log_rotate)
    log_retention = kwargs.get('logRetention', log_retention)
    log_level = str(kwargs.get('logLevel', log_level)).upper()
    available_log_levels = kwargs.get('availableLogLevels', available_log_levels)

    if debug:
        log_level = 'DEBUG'

    if log_level not in available_log_levels:
        log_level = 'INFO'

    # Because the library comes with a logger to std.err initalized and we get rid of that
    logger.remove()
    # Now add the screen std.err logger back using the right log level
    if enable_screen_debug:
        logger.add(sys.stderr, colorize=True,
                   level='DEBUG',
                   backtrace=True,
                   diagnose=True,
                   format="<blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</blue> <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> <level>{level}</level>: {message}"
                   )

    # Add file logging if required
    if enable_log_file:
        if os.path.isfile(log_file):
            if not os.access(log_file, os.W_OK):
                print("Permissions error, unable to write to log file ({})".format(log_file))
                sys.exit(os.EX_CONFIG)

        logger.add(log_file, colorize=True,
                   format="<blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</blue> <yellow>({process.id})</yellow> <level>{level}</level>: {message}",
                   level=log_level,
                   rotation=log_rotate,
                   retention=log_retention,
                   compression="gz"
                   )
    
    logger.debug(
        f"Log initalized with level: {log_level}, enable screen debug: {enable_screen_debug}, enable log file: {enable_log_file}, file: {log_file}, rotate: {log_rotate}, retention: {log_retention}")
