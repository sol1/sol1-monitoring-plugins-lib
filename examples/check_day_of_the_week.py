import argparse
from loguru import logger
from datetime import datetime

from sol1_monitoring_plugins_lib import MonitoringPlugin, initLogging, initLoggingArgparse

# it's nice to put the args at the top of the file as it is commonly referenced


def getArgs():
    parser = argparse.ArgumentParser(description='Check the day of the week.')
    parser.add_argument('--day', type=str, help='Day of the week', required=True)
    # Adding the logging arguments to argparse
    initLoggingArgparse(parser=parser)
    return parser.parse_args()


if __name__ == "__main__":
    args = getArgs()
    # Initalize the logging with the arguments from argparse
    initLogging(debug=args.debug, 
                enable_screen_debug=args.enable_screen_debug,
                enable_log_file=not args.disable_log_file, 
                log_file=args.log_file,
                log_rotate=args.log_rotate,
                log_retention=args.log_retention,
                log_level=args.log_level,
                available_log_levels=args.available_log_levels
                )

    # initalze the plugin
    plugin = MonitoringPlugin("Day of the week")

    # a little bit of setup
    current_day = datetime.now().strftime('%A')
    logger.info(f"today is {current_day}")
    day_to_number = {
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7,
    }

    # add to the output message
    plugin.message = f"Info: Today is {current_day}\n"

    # do a test
    if args.day.capitalize() == current_day.capitalize():
        # the result we want
        plugin.setMessage(f"We want it to be {args.day.capitalize()}\n", plugin.STATE_OK, True)
        plugin.success_summary = f"matches {args.day.capitalize()}"
    else:
        # not the result we want, but are we close
        plugin.failure_summary = f"{args.day.capitalize()} isn't today"
        if args.day.capitalize() not in day_to_number:
            plugin.failure_summary = f"invalid day {args.day.capitalize()}"
            # not even a real day
            plugin.setMessage(f"Day \"{args.day.capitalize()}\" isn't even a real day\n", plugin.STATE_CRITICAL, True)
            # instead of complex and deep if else statements once we reach a show stopper problem we just exit
            plugin.exit()

        target_day_num = day_to_number.get(args.day.capitalize())

        days_until_target = (target_day_num - datetime.now().isoweekday() + 7) % 7
        logger.debug(f"days till target day = {day_to_number}")
        state = plugin.STATE_CRITICAL
        if days_until_target == 1:
            state = plugin.STATE_WARNING
        plugin.setMessage(f"Day {args.day.capitalize()} is {days_until_target} day(s) away", state, True)

    # catch all for exiting
    plugin.exit()
