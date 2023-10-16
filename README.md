# Monitoring Plugins
Monitoring Plugins are tools to assist in the creation of monitoring checks for Icinga2 and Nagios.


## `MonitoringPlugin`
This class manages the state, output message and performance data of your check as well as returning this data and exiting the script.

It has been designed so you can add multiple tests and the class will intelligently manage the state and output for you. 

### API
#### Init
Plugin's can be initalized with a check `checktype`, this check type appears on the first line of the output along with the overall state.

```
from MonitoringPlugins import MonitoringPlugin

plugin = MonitoringPlugin()
```

#### Constants
State constants exist to make it easier to see what you code is doing
```
plugin.STATE_OK             
plugin.STATE_WARNING        
plugin.STATE_CRITICAL       
plugin.STATE_UNKNOWN        

```

#### State

State has helper functions to set the state only if the new state is more accurate than the previous state. eg: a check which is already CRITICAL won't become OK if you use the functions because a previous CRITICAL test result is still a failure in your testing. 
```
plugin.setOK()
plugin.setWarning()
plugin.setCritical()
plugin.setState(plugin.STATE_OK)
```

And helper functions to return human readable strings of the state
```
plugin.getStateLabel(plugin.state)
```

There are also getters and setters to set and read the current plugin state at any time. 
Note: the setter here can be used to override any previous state.
```
plugin.state = plugin.STATE_OK
print(plugin.state)
```
#### Message
Message has getters, setters and deleters to manage the output message. 
It is expected that you will manage newlines yourself.
```
plugin.message = "Hello world\n"
print(plugin.message)
del plugin.message
```

There are also a function that manages the message and state together. This function can prefix the message with the passed in or current state as well as change the state. 
This is particularly useful for plugins with multiple tests as it allows you to indicate which test failed.
```
plugin.setMessage("Hello World\n", state=plugin.STATE_OK, set_state=True, no_prefix=False)
```

#### Performance Data
The performance data is best managed via the available function, it provides a simple interface to create the performance data strings.
Only `label` and `value` are required.
```
plugin.setPerformanceData(label="foo", value=5, unit_of_measurement="", warn="", crit="", minimum="", maximum="")
```

There is a getter, setter and deleter for performance data
```
plugin.performance_data = "foo=5;;;; "
print(plugin.performance_data)
del performance_data
```

#### Success/Failure Summary
There are 2 values, `failure_summary` and `success_summary` that can be set to add more detail to the first output line of your check.
These values are lists that output unique values comma seperated on the first line of your check output.

Note: This is a list so you can add these to a loop and and output the same message multiple times but only display unique values. 

Each has a getter, setter and deleter
```
plugin.failure_summary = "Bad foo"
print(plugin.failure_summary)
del plugin.failure_summary

plugin.success_summary = "Good foo"
print(plugin.success_summary)
del plugin.success_summary
```




### Example
```
from MonitoringPlugins import MonitoringPlugin

# initalze the plugin
plugin = MonitoringPlugin("Test")



# add to the output message
plugin.message = "Info: Hello World\n"

is_bad = False
if not is_bad:
    plugin.setMessage("This is going well\n", plugin.STATE_OK, True)
    plugin.success_summary = "All is well"

is_bad = True
if is_bad:
    plugin.setMessage("Oh no\n", plugin.STATE_CRITICAL, True)
    plugin.success_summary = "Not so well"

is_bad = False
if not is_bad:
    plugin.setMessage("This one worked too\n", plugin.STATE_OK, True)
    plugin.success_summary = "All is well"

plugin.exit()
```
Exit code: 2
Output: 
```
CRITICAL: Test check Not so well

Ok: This is going well
Critical: Oh no
Ok: This one worked too
```

If all the `is_bad`'s above were True then we'd return
Exit code: 2
Output: 
```
OK: Test check All is well

Ok: This is going well
Ok: This one worked too
```
