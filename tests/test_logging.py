from __future__ import print_function

import pytest
import argparse
import pytest
from sol1_monitoring_plugins_lib import initLogging, initLoggingArgparse, DEFAULT_LOG_LEVELS


def test_initLoggingArgparse():
    parser = argparse.ArgumentParser()
    initLoggingArgparse(parser)
    args = parser.parse_args([])
    assert args.debug == False
    assert args.enable_screen_debug == False
    assert args.disable_log_file == False
    assert args.log_file == '/var/log/icinga2/check_monitoring.log'
    assert args.log_rotate == '1 day'
    assert args.log_retention == '3 days'
    assert args.log_level == 'WARNING'
    assert args.available_log_levels == DEFAULT_LOG_LEVELS

    args = parser.parse_args(['--debug', '--enable-screen-debug', '--disable-log-file', '--log-file', 'test.log'])
    assert args.debug == True
    assert args.enable_screen_debug == True
    assert args.disable_log_file == True
    assert args.log_file == 'test.log'

def test_initLogging(capfd):
    initLogging(debug=True, enable_screen_debug=True, enable_log_file=False)
    out, err = capfd.readouterr()
    assert "enable log file: False" in err
    assert "debug: True" in err
    assert "Log initalized with level: DEBUG" in err

