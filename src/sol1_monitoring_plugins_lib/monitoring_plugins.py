#!/usr/bin/env python
# coding: utf-8

from loguru import logger


class MonitoringPlugin:
    """Parent Monitoring Plugin class used to manage state, output and performance data
    Can be used by itself or by a child class
    """

    def __init__(self, checktype=None):
        # The states of the server
        self.STATE_OK = 0            # We know it is OK and it isn't WARN or CRIT when set
        self.STATE_WARNING = 1       # We know it is WARN and isn't CRIT when set
        self.STATE_CRITICAL = 2      # We know it is CRIT
        self.STATE_UNKNOWN = 3       # We don't know anything yet
        self._current_state = self.STATE_UNKNOWN
        self._message = ""
        self._performance_data = ""
        self._type = checktype
        self._success_summary = []
        self._failure_summary = []

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def exit(self, exit_state=None, force_state=False, do_exit=True):
        """Exits the check outputing the correct state, message and perfdata
        or returns a tuple with (state, message, perfdata).

        Args:
            exit_state (int, optional): Lets you add a state on exit. Defaults to None.
            force_state (bool, optional): Forces the added state on exit to be used. Defaults to False.
            do_exit (bool, optional): Controls normal check exit or return of plugin exit data. Defaults to True.

        Returns:
            tuple: return state, message and performance data of check
        """
        # If we pass in a new exit state then only change to it if we at a start state
        if exit_state is not None:
            if self.state < exit_state or self.state == self.STATE_UNKNOWN or force_state:
                self.state = exit_state

        first_line = "\n"
        # add the summary to the top of the message
        if self.state == self.STATE_OK:
            if self.success_summary:
                first_line = f"{', '.join(list(set(self.success_summary)))}{first_line}"
        else:
            if self.failure_summary:
                first_line = f"{', '.join(list(set(self.failure_summary)))}{first_line}"

        # Add the check type to the top of the message
        if self._type:
            first_line = f"{self._type} check {first_line}"

        # Set the prefix for the message
        self._message = f"{self.getStateLabel(self.state)}: {first_line}{self.message}"

        # Print the message and perfdata, log the exit and exit with error code
        logger.info(f"Exiting check with state {self.state}")
        if do_exit:
            # Add the pipe '|' before perfdata if we have any
            if self.performance_data != "":
                self.performance_data = "|" + self.performance_data
            print(f"{self.message}{self.performance_data}")
            exit(self.state)
        else:
            return (self.state, self.message, self.performance_data)

    @property
    def state(self):
        return self._current_state

    @state.setter
    def state(self, new_state):
        logger.debug(f"State change from old {self.state} to new {new_state}")
        self._current_state = new_state

    def getStateLabel(self, state):
        """Returns a human readable equivalent of the passed in State

        Args:
            state (int): One of the 4 class STATE constants

        Returns:
            str: Human readable state text
        """
        label = "INVALID ({state})"
        if state == self.STATE_OK:
            label = "OK"
        elif state == self.STATE_WARNING:
            label = "WARNING"
        elif state == self.STATE_CRITICAL:
            label = "CRITICAL"
        elif state == self.STATE_UNKNOWN:
            label = "UNKNOWN"
        logger.debug(f"Return state label for state ({state}): {label}")
        return label

    def setOk(self):
        """Set the plugin state to OK if current state is UNKNOWN
        """
        logger.debug("setOk")
        if self.state == self.STATE_UNKNOWN:
            self.state = self.STATE_OK

    def setWarning(self):
        """Set the plugin state to WARNING if current state is not CRITICAL
        """
        logger.debug("setWarning")
        if self.state != self.STATE_CRITICAL:
            self.state = self.STATE_WARNING

    def setCritical(self):
        """Set the plugin state to CRITICAL
        """
        logger.debug("setCritical")
        self.state = self.STATE_CRITICAL

    def setState(self, state):
        """Requests the plugin state be updated based on set*() rules and 
        return the value of the plugin state afterwards

        Args:
            state (int): One of the 4 class STATE constants

        Returns:
            int: One of the 4 class STATE constants
        """
        logger.debug(f"setState({state})")
        if state == self.STATE_OK:
            self.setOk()
        elif state == self.STATE_WARNING:
            self.setWarning()
        elif state == self.STATE_CRITICAL:
            self.setCritical()
        return self.state

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg):
        # message only
        self._message += msg

    @message.deleter
    def message(self):
        self._message = ""

    def setMessage(self, msg, state=None, set_state=False, no_prefix=False):
        """Adds a message to the plugin output. 
        Optionally allows for a prefix based on state for the message and/or setting the state using setState.

        Args:
            msg (str): Line of text to the message output of your plugin
            state (int, optional): State for the msg text. Defaults to None.
            set_state (bool, optional): Uses setState to change the plugin's state. Defaults to False.
            no_prefix (bool, optional): Supress the prefix for msg text. Defaults to False.
        """
        # If state isn't set then use the current state
        if state is None:
            state = self.state
        # change state
        if set_state:
            self.setState(state)
        # message only
        if no_prefix:
            self._message += msg
        else:
            self._message += f"{self.getStateLabel(state).title()}: {msg}"

    @property
    def performance_data(self):
        return self._performance_data

    @performance_data.setter
    def performance_data(self, data):
        self._performance_data += data

    @performance_data.deleter
    def performance_data(self):
        self._performance_data = ""

    def setPerformanceData(self, label: str, value, unit_of_measurement: str = "", warn="", crit="", minimum="", maximum=""):
        """Renders a performance data string and appends it to the plugin's performance data

        Args:
            label (str): String for the label
            value (int): Numeric value only
            unit_of_measurement (str, optional): Unit of Measurement [s, us, ms, %, B, KB, MB, TB, c]. Defaults to "".
            warn (str, optional): Numeric value for warning value. Defaults to "".
            crit (str, optional): Numeric value for critical value. Defaults to "".
            minimum (str, optional): Numeric value for minimum value. Defaults to "".
            maximum (str, optional): Numeric value for maximum value. Defaults to "".

        UOM's:
            no unit specified - assume a number (int or float) of things (eg, users, processes, load averages)
            s - seconds (also us, ms)
            % - percentage
            B - bytes (also KB, MB, TB)
            c - a continous counter (such as bytes transmitted on an interface)
        """
        self.performance_data = f"{label}={value}{unit_of_measurement};{warn};{crit};{minimum};{maximum} "

    @property
    def failure_summary(self):
        return self._failure_summary

    @failure_summary.setter
    def failure_summary(self, data):
        self._failure_summary.append(str(data))

    @failure_summary.deleter
    def failure_summary(self):
        self._failure_summary = []

    @property
    def success_summary(self):
        return self._success_summary

    @success_summary.setter
    def success_summary(self, data):
        self._success_summary.append(str(data))

    @success_summary.deleter
    def success_summary(self):
        self._success_summary = []
