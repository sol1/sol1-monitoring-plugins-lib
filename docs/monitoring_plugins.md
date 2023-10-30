# `MonitoringPlugin` Class

The `MonitoringPlugin` class is designed for accumlatively managing the state, output, and performance data in monitoring applications. It can function independently or be extended by child classes. 

This allows you to perform multiple tests in your check and the class will return the worst state as well as a message that outlines which tests worked and which failed. The check type and success/failure summaries can also be used to set a first line summary of the result in the message.

_Note: The class relies on the loguru library for logging, and proper setup of this library is required for logging to work as expected._

## Constructor

```python
__init__(checktype=None)
```

__Description__: Initializes a new instance of MonitoringPlugin, setting up the initial state and other attributes.

__Parameters:__
`checktype` (optional): A string indicating the type of check being performed. Default is None.

__Attributes:__
`_current_state`: Stores the current state of the plugin. Initialized to STATE_UNKNOWN.
`_message`: Stores the output message.
`_performance_data`: Stores the performance data.
`_type`: Stores the type of check being performed.
`_success_summary`: A list to store summary of successful checks.
`_failure_summary`: A list to store summary of failed checks.

_Note you should be using the methods to change attributes rather than changing them directly._

## Constants

`STATE_OK = 0`: Indicates a successful state.
`STATE_WARNING = 1`: Indicates a state that requires attention.
`STATE_CRITICAL = 2`: Indicates a critical state that needs immediate attention.
`STATE_UNKNOWN = 3`: Indicates an unknown state.

## Methods
### exit()
Manages the exit process of the plugin, setting the appropriate state, printing the output message, and exiting the program.

The output messages first line is formatted based on the plugin state, check type and success/failure summaries.

Optionally you can not exit the program and instead return the current plugin data as a tuple which is useful for applications that need to set passive checks.

```python
exit(exit_state=None, force_state=False, do_exit=True)
```
__Parameters:__
`exit_state` (optional): An integer representing the state on exit. Defaults to `None`.
`force_state` (optional): A boolean that determines if the exit_state should be forcefully set. Defaults to `False`.
`do_exit` (optional): A boolean that controls whether the program should exit or return plugin exit data. Defaults to `True`.

__Returns:__ A tuple `(state, message, performance_data)` if do_exit is False.

### getStateLabel()
Converts a state constant to its human-readable form.

```python
getStateLabel(state)
```
__Parameters:__
`state`: An integer representing one of the plugin's states.

__Returns:__ A string representing the human-readable equivalent of the given state.

### setOk()

Sets the plugin state to OK if the current state is `UNKNOWN`.

```python 
setOk()
```

### setWarning()

Sets the plugin state to `WARNING` if the current state is not `CRITICAL`.

```python 
setWarning()
```

### setCritical()

Sets the plugin state to `CRITICAL`.

```python 
setCritical()
```

### setState()

Sets the plugin state using the rules in `setOk`, `setWarning` and `setCritical` and return the new plugin state.

```python 
setState(state)
```
__Parameters:__
`state`: An integer representing one of the plugin's states.
__Returns:__ The updated state of the plugin.

### setMessage()
Adds a message to the plugin's output, with optional state-based prefix and state updating.

```python
setMessage(msg, state=None, set_state=False, no_prefix=False)
```

__Parameters:__
`msg`: A string representing the message to be added.
`state` (optional): An integer representing one of the plugin's states. Defaults to None.
`set_state` (optional): A boolean indicating whether to update the plugin's state. Defaults to False.
`no_prefix` (optional): A boolean indicating whether to suppress the prefix for the message text. Defaults to False.

### setPerformanceData()

Renders a performance data string and appends it to the plugin's performance data.

```python
setPerformanceData(label, value, 
unit_of_measurement="", warn="", crit="", minimum="", maximum="")
```
__Parameters:__
`label`: A string representing the performance data label.
`value`: The numeric value for the performance data.
`unit_of_measurement` (optional): A string representing the unit of measurement. Defaults to "".
`warn` (optional): Warning threshold
`crit` (optional): Critical threshold
`minimum` (optional): Minimum threshold
`maximum` (optional): Maximum threshold

## Properties

### state
Convience method to get or set the current state of the plugin. 

_This is explict in setting the state, you generally want to use a method._

### message
Convience method to get, set or delete the output message of the plugin. When setting the message that input appends to the end of the existing message.

### performance_data
Convience method to get, set or delete the performance data of the plugin. When setting the performance data that input appends to the end of the existing performance data.

_This doesn't format the performance data, you generally want to use a `setPerformanceData()` method._

### failure_summary
Convience method to get, set or delete the summary of failed checks. When setting the failed summary the input appends list.

### success_summary
Convience method to get, set or delete the summary of successful checks. When setting the successful summary the input appends list.