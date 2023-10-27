import pytest
from MonitoringPlugins import MonitoringPlugin
# from monitoring_plugins.src.MonitoringPlugins import MonitoringPlugin, MonitoringLine

# class TestSimpleThreasholds(unittest.TestCase):
#     def testEquals():
#         plugin = MonitoringLine()
#         assert plugin._parseSimpleThreshold(10) == (None, None, float(10))


def test_initialization():
    plugin = MonitoringPlugin()
    assert plugin.state == plugin.STATE_UNKNOWN
    assert plugin.message == ""
    assert plugin.performance_data == ""
    assert plugin.failure_summary == []
    assert plugin.success_summary == []

def test_initialization_with_type():
    plugin = MonitoringPlugin("Example")
    assert plugin._type == "Example"

def test_states():
    plugin = MonitoringPlugin()
    assert plugin.STATE_OK == 0
    assert plugin.STATE_WARNING == 1
    assert plugin.STATE_CRITICAL == 2
    assert plugin.STATE_UNKNOWN == 3

def test_state_transitions():
    plugin = MonitoringPlugin()
    
    plugin.setOk()
    assert plugin.state == plugin.STATE_OK
    
    plugin.setWarning()
    assert plugin.state == plugin.STATE_WARNING
    
    plugin.setCritical()
    assert plugin.state == plugin.STATE_CRITICAL
    
    plugin.setOk()  # Should not override CRITICAL
    assert plugin.state == plugin.STATE_CRITICAL

def test_message_setting_and_deletion():
    plugin = MonitoringPlugin()
    plugin.message = "Test Message"
    assert plugin.message == "Test Message"
    del plugin.message
    assert plugin.message == ""

def test_performance_data_setting_and_deletion():
    plugin = MonitoringPlugin()
    plugin.setPerformanceData(label='test', value=5)
    assert plugin.performance_data == "test=5;;;; "
    plugin.setPerformanceData(label='test2', value=5, unit_of_measurement="s", minimum=1, maximum=10, warn=3, crit=6)
    assert plugin.performance_data == "test=5;;;; test2=5s;3;6;1;10 "
    del plugin.performance_data
    assert plugin.performance_data == ""

def test_summary_functionality():
    plugin = MonitoringPlugin()
    plugin.success_summary = "Success 1"
    plugin.success_summary = "Success 2"
    plugin.failure_summary = "Failure 1"
    
    assert plugin.success_summary == ["Success 1", "Success 2"]
    assert plugin.failure_summary == ["Failure 1"]

def test_exit_functionality():
    plugin = MonitoringPlugin("Test")
    plugin.setMessage("Test Message", plugin.STATE_OK, True, False)
    plugin.setPerformanceData(label='test', value=5)
    assert plugin.exit(do_exit=False) == (0, 'OK: Test check \nOk: Test Message', 'test=5;;;; ')
    
