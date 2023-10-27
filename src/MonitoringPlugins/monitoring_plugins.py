#!/usr/bin/env python
# coding: utf-8

from loguru import logger


class MonitoringPlugin:  
    """Parent Monitoring Plugin class used to manage state, output and performance data
    Can be used by itself or by a child class
    """    
    def __init__(self, checktype = None):
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

    def exit(self, exit_state = None, force_state = False, do_exit = True):
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

    def setState(self,state):
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

    def setMessage(self, msg, state = None, set_state = False, no_prefix = False):
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

    def setPerformanceData(self, label:str, value, unit_of_measurement:str = "", warn = "", crit = "", minimum = "", maximum = ""):
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
        self.performance_data += f"{label}={value}{unit_of_measurement};{warn};{crit};{minimum};{maximum} "

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


class MonitoringLine(MonitoringPlugin):
    """Child Monitoring Class with additional features to perform tests and manage output
    """    
    # a few handy similar methods to output a line of labelled data, optionally checking for something
    def _labelDataLine(self, label, data=None, extra=None, indent="", lookup = {}):
        """ Formats the label, data and extra info into a string and returns it

        Args:
            label (_type_): _description_
            data (_type_, optional): _description_. Defaults to None.
            extra (_type_, optional): _description_. Defaults to None.

        Returns:
            string: message string for line
        """        
        line = f"{indent}{label}"

        looked_up = data
        if lookup:
            lu = lookup.get(data,"Unexpected Value")
            looked_up = f"{lu} ({data})"
        else:
            looked_up = data

        if data != None and extra:
            line = f"%-31s %s" % (f"{indent}{label}:", f"{looked_up} {extra}")
        elif data != None:
            line = f"%-31s %s" % (f"{indent}{label}:", f"{looked_up}")
        elif extra:
            line = f"%-31s %s" % (f"{indent}{label}:", f"{extra}")
        return line

    def lineInfo(self, label, data=None, extra=None, indent='', lookup={}):
        """ Output message data prepended with `Info: `. 
        """
        self.message = f"Info:     {self._labelDataLine(label,data,extra,indent=indent,lookup=lookup)}\n"

    def _ifNot(self, state, label, data, acceptable, indent='', lookup={}):
        """ Output message if the `data` exactly matches the `acceptable` result.\n
            The Output line is prepended with the `state`.\n
            The plugin state is set to the `state`.
        """
        if data not in acceptable:
            if lookup:
                acceptable = map(lambda k: f"{lookup.get(k,'Unexpected Value')} ({k})", acceptable)
            self.setMessage(f"{self._labelDataLine(label,data,indent=indent,lookup=lookup)} (expected: {','.join(acceptable)})\n", state, set_state=True)
        else:
            self.setMessage(f"{self._labelDataLine(label,data,indent=indent,lookup=lookup)}\n", self.STATE_OK, set_state=True)

    def lineUnknown(self, label, data, extra="", indent="", lookup={}):
        """ Output message data prepended with `Unknown: ` and set plugin state to `UNKNOWN`.
        """
        self._lineState(self.STATE_UNKNOWN, label, data, extra, indent=indent, lookup=lookup)

    def lineCritical(self, label, data, extra="", indent="", lookup={}):
        """ Output message data prepended with `Critical: ` and set plugin state to `CRITICAL`. 
        """
        self._lineState(self.STATE_CRITICAL, label, data, extra, indent=indent, lookup=lookup)

    def lineWarning(self, label, data, extra="", indent="", lookup={}):
        """ Output message data prepended with `Warning: ` and set plugin state to `WARNING`. 
        """
        self._lineState(self.STATE_WARNING, label, data, extra, indent=indent, lookup=lookup)

    def lineOk(self, label, data, extra="", indent="", lookup={}):
        """ Output message data prepended with `Ok: ` and set plugin state to `OK`. 
        """
        self._lineState(self.STATE_OK, label, data, extra, indent=indent, lookup=lookup)

    def _lineState(self, state, label, data, extra, indent="", lookup={}):
        self.setMessage(f"{self._labelDataLine(label,data,extra, indent=indent, lookup=lookup)}\n", state, set_state=True)

    def lineUnknownIfNot(self, label, data, acceptable=[], indent="", lookup={}):
        """ Output message if the `data` exactly matches the `acceptable` result.\n
            The Output line is prepended with the `Unknown: `.\n
            The plugin state is set to the `UNKNOWN`.
        """
        self._ifNot(self.STATE_UNKNOWN, label, data, acceptable, indent=indent, lookup=lookup)

    def lineCriticalIfNot(self, label, data, acceptable=[], indent="", lookup={}):
        """ Output message if the `data` exactly matches the `acceptable` result.\n
            The Output line is prepended with the `Critical: `.\n
            The plugin state is set to the `CRITICAL`.
        """
        self._ifNot(self.STATE_CRITICAL, label, data, acceptable, indent=indent, lookup=lookup)

    def lineWarningIfNot(self, label, data, acceptable=[], indent="", lookup={}):
        """ Output message if the `data` exactly matches the `acceptable` result.\n
            The Output line is prepended with `Warning: `.\n
            The plugin state is set to the `WARNING`.
        """
        self._ifNot(self.STATE_WARNING, label, data, acceptable, indent=indent, lookup=lookup)


    def _parseSimpleThreshold(self, threshold):
        """Parses a simple threshold in the format <number>:<number>.
        10       Equals 10
        10:      Above 10
        10:20    Above 10 and Below 20
          :20    Below 20
        20:10    Above 20 or Below 10
        

        Args:
            threshold (string): Threshold matching <number>:<number>

        Returns:
            tuple: contains values for (above, below, equals) which can be passed to self.eval or read. 
        """        
        above = None
        below = None
        equals = None
        if ':' in threshold:
            above, below = threshold.split(':')
            if self._numericValue(above) is None or self._numericValue(below) is None:
                logger.error(f"Part of the threshold {threshold} isn't numeric: above ({above}), below ({below})")
        else:
            if self._numericValue(threshold):
                logger.error(f"The threshold {threshold} isn't numeric")
            equals=threshold
        return (above, below, equals)

    # following https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/#threshold-ranges
    def _parseIcingaThreshold(self, threshold):
        """Parses a Icinga threshold in the format [~,(@)<number>]:<number>.
        10       Above 0 and Below 10
        10:      Above 10
        10:20    Below 10 or Above 20
        10:10    Equals 10 ?? unclear
        @10:20   Above 10 and Below 20
         ~:20    Below 20
        20:10    This is invalid
        

        Args:
            threshold (string): Threshold matching [~,(@)<number>]:<number>

        Returns:
            tuple: contains values for (above, below, equals) which can be passed to self.eval or read. 
        """        
        above = None
        below = None
        equals = None
        inside = False
        if ':' in threshold:
            above, below = threshold.split(':')
            # ~ means infinity..end 
            if above[0] == '~':
                above = None
            elif above[0] == '@':
                above = above[1:]
                inside = True
            if self._numericValue(above) is None or self._numericValue(below) is None:
                logger.error(f"Part of the threshold {threshold} isn't numeric: start ({above}), end ({below})")
        else:
            if self._numericValue(threshold) is None:
                logger.warning(f"The threshold {threshold} isn't numeric")
            below = threshold
            above = 0
        if above == below:
            equals = above
            above = None
            below = None
        if inside:
            return (below, above, equals)
        else:
            # if we aren't doing a inside range test the values are reversed
            return (above, below, equals)
        
    @staticmethod            
    def _getIcingaThreadhold(above, below, equals):
        if equals:
            return f"{equals}:{equals}"
        if above and not below:
            return f"{above}:"
        if below and not above:
            return f"~:{below}"
        if above and below == 0:
            return f"{above}"
        if below and above: 
            if below < above:
                return f"@{above}:{below}"
            else:
                return f"{above}:{below}"


    @staticmethod            
    def _numericValue(value):
        """Get back a numeric value (float) if what is passed in can be consided a number

        Args:
            value (_type_): Pass in anything

        Returns:
            float: None or a float if the value is set and numeric
        """        
        if value and not str(value).isnumeric():
            return None
        else: 
            return float(value)
        
    @classmethod            
    def eval(cls, value, above = None, below = None, equals = None, equal_to: bool = False) -> bool:
        """Evaluate value against optional paramaters.
        equals = value equals
        above only = value must be more than 
        below only = value must be less than 
        above and below where below is less than above = value is between 
        above and below where below is more than above = value is outside

        Args:
            value (_type_): Test value, assumes a int or float
            above (_type_, optional): assumes a int or float. Defaults to None.
            below (_type_, optional): assumes a int or float. Defaults to None.
            equals (_type_, optional): assumes a int or float. Defaults to None.
            or_equal_to (bool, optional): Make the comparisions greater/less than or equal to. Defaults to False.

        Returns:
            bool: If value matches paramaters or not
        """        
        @staticmethod            
        def __greaterThan(a, b, equal_to = False) -> bool:
            """Is a greater than b

            Args:
                a (_type_): value that we are testing if it is greater than
                b (_type_): value we are comparing against
                equals_to (bool, optional): Make the comparisions greater/less than or equal to. Defaults to False.

            Returns:
                bool: True if a is greater than or equal to b
            """    
            if equal_to:
                return a >= b
            else:
                return a > b

        @staticmethod            
        def __lessThan(a, b, equal_to = False) -> bool:
            """Is a greater than b

            Args:
                a (_type_): value that we are testing if it is greater than
                b (_type_): value we are comparing against
                equals_to (bool, optional): Make the comparisions greater/less than or equal to. Defaults to False.

            Returns:
                bool: True if a is less than or equal to b
            """    
            if equal_to:
                return a <= b
            else:
                return a < b


        try:
            if equals:
                return (equals == value, f"")      # equals
            else:
                if below and above:
                    if __lessThan(above, below):
                        return (__greaterThan(value, above, equal_to) and __lessThan(value, below, equal_to))       # inside range
                    else: 
                        return (__lessThan(value, below, equal_to) or __greaterThan(value, above, equal_to))        # outside range
                elif below:
                    return (__lessThan(value, below, equal_to))     # At least    
                elif above:
                    return (__greaterThan(value, above, equal_to))        # At most
        except Exception as e:
            logger.error(f'Unable to evaluate value: {value} against end: {below}, start: {above}, equals: {equals} with error {e}')            
        return None                     # catch all 


    # following https://icinga.com/docs/icinga-2/latest/doc/05-service-monitoring/#threshold-ranges
    # based on https://github.com/NETWAYS/check_tinkerforge/blob/master/check_tinkerforge.py
    @staticmethod
    def parseThreshold(t):
        # ranges
        if ":" in t:
            parts= t.split(":")
            if parts[0] == '~':
                return t
            else:
                return parts
        else: # single number n means 0:n
            return [0,t]

    def evalThresholdGeneric(self, val, threshold):
        # handle @ to invert the range
        if threshold[0] == '@':
            invert = True
            threshold = threshold[1:]
        else:
            invert = False
        t_arr = self.parseThreshold(threshold)

        # if we only have one value, treat this as 0..value range
        if len(t_arr) == 1:
            self._logger.debug("Evaluating thresholds, single %s on value %s" % (" ".join(t_arr), val))

            if (val > (float(t_arr[0]))) != invert:
                return f"{val} > {t_arr[0]}"
        else:
            self._logger.debug("Evaluating thresholds, range %s on value %s" % (":".join(t_arr), val))

            if (t_arr[0] > t_arr[1]):
                raise ValueError("Range {':'.join(t_arr)} invalid because {t_arr[0]} > {t_arr[1]}")

            if (val < float(t_arr[0])) != invert:
                return f"{val} < {t_arr[0]}"
            elif (val > float(t_arr[1])) != invert:
                return f"{val} > {t_arr[0]}"

        return ""

    def evalThresholds(self, val, warning, critical):
        status = self.STATE_OK
        explanation = ""

        if warning:
            warn_exp = self.evalThresholdGeneric(val, warning)
            if warn_exp:
                status = self.STATE_WARNING
                explanation = warn_exp

        if critical:
            crit_exp = self.evalThresholdGeneric(val, critical)
            if crit_exp:
                status = self.STATE_CRITICAL
                explanation = crit_exp

        return (status,explanation)

    # crit/warn if there's a crit/warn range and it's not in it
    def lineInRange(self, label, data, warning=None, critical=None, perf=True, uom="", minimum = "", maximum= "", indent="", lookup={}):
        """Compares the `data` passed in against the `warning` and `critical` values\n
        to find values that are in the end and start bound values

        Args:
            label (_type_): _description_
            data (_type_): _description_
            warn (str, optional): _description_. Defaults to "".
            crit (str, optional): _description_. Defaults to "".
            perf (bool, optional): _description_. Defaults to True.
            uom (str, optional): _description_. Defaults to "".
            minimum (str, optional): _description_. Defaults to "".
            maximum (str, optional): _description_. Defaults to "".
        """        
        try:
            val = float(data)
            (state,exp) = self.evalThresholds(val, warning=warning, critical=critical)
        except:
            val = None
            state = self.STATE_OK
            exp = f"Could not get value from '{data}'"
            logger.warning(f"{label}: {exp}")
        if perf and not val == None:
            self.setPerfdata(label, data, uom, warning, critical, minimum, maximum)
        if state != None:
            self.setMessage(self._labelDataLine(label, data, uom, indent=indent, lookup=lookup) + (f" ({exp})\n" if len(exp) else "\n"), state, set_state=True)

