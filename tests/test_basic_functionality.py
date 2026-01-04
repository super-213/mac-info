"""
基本功能测试
Basic Functionality Tests

验证核心模块可以正常导入和实例化
Verifies that core modules can be imported and instantiated correctly
"""

import pytest
from src.mac_info.metrics_collector import MetricsCollector
from src.mac_info.temperature_monitor import TemperatureMonitor
from src.mac_info.process_manager import ProcessManager


def test_metrics_collector_instantiation():
    """
    测试MetricsCollector可以正常实例化
    Test that MetricsCollector can be instantiated
    """
    collector = MetricsCollector()
    assert collector is not None


def test_temperature_monitor_instantiation():
    """
    测试TemperatureMonitor可以正常实例化
    Test that TemperatureMonitor can be instantiated
    """
    monitor = TemperatureMonitor()
    assert monitor is not None


def test_process_manager_instantiation():
    """
    测试ProcessManager可以正常实例化
    Test that ProcessManager can be instantiated
    """
    manager = ProcessManager()
    assert manager is not None


def test_metrics_collector_cpu_info():
    """
    测试CPU信息收集返回正确的数据结构
    Test that CPU info collection returns correct data structure
    """
    collector = MetricsCollector()
    cpu_info = collector.get_cpu_info()
    
    # 验证返回的是字典
    # Verify that a dictionary is returned
    assert isinstance(cpu_info, dict)
    
    # 验证包含所有必需的键
    # Verify that all required keys are present
    assert 'overall_percent' in cpu_info
    assert 'per_core_percent' in cpu_info
    assert 'count' in cpu_info
    assert 'frequency' in cpu_info
    
    # 验证数据类型
    # Verify data types
    assert isinstance(cpu_info['overall_percent'], (int, float))
    assert isinstance(cpu_info['per_core_percent'], list)
    assert isinstance(cpu_info['count'], int)
    assert isinstance(cpu_info['frequency'], dict)
    
    # 验证值在合理范围内
    # Verify values are in reasonable ranges
    assert 0 <= cpu_info['overall_percent'] <= 100
    assert cpu_info['count'] > 0


def test_metrics_collector_memory_info():
    """
    测试内存信息收集返回正确的数据结构
    Test that memory info collection returns correct data structure
    """
    collector = MetricsCollector()
    memory_info = collector.get_memory_info()
    
    # 验证返回的是字典
    # Verify that a dictionary is returned
    assert isinstance(memory_info, dict)
    
    # 验证包含所有必需的键
    # Verify that all required keys are present
    assert 'total' in memory_info
    assert 'available' in memory_info
    assert 'used' in memory_info
    assert 'percent' in memory_info
    assert 'swap_total' in memory_info
    assert 'swap_used' in memory_info
    
    # 验证数据类型
    # Verify data types
    assert isinstance(memory_info['total'], int)
    assert isinstance(memory_info['available'], int)
    assert isinstance(memory_info['used'], int)
    assert isinstance(memory_info['percent'], (int, float))
    
    # 验证值在合理范围内
    # Verify values are in reasonable ranges
    assert memory_info['total'] > 0
    assert 0 <= memory_info['percent'] <= 100


def test_metrics_collector_disk_io_info():
    """
    测试磁盘I/O信息收集返回正确的数据结构
    Test that disk I/O info collection returns correct data structure
    """
    collector = MetricsCollector()
    disk_io_info = collector.get_disk_io_info()
    
    # 验证返回的是字典
    # Verify that a dictionary is returned
    assert isinstance(disk_io_info, dict)
    
    # 验证包含所有必需的键
    # Verify that all required keys are present
    assert 'read_bytes' in disk_io_info
    assert 'write_bytes' in disk_io_info
    assert 'read_count' in disk_io_info
    assert 'write_count' in disk_io_info
    
    # 验证数据类型和值范围
    # Verify data types and value ranges
    assert isinstance(disk_io_info['read_bytes'], int)
    assert isinstance(disk_io_info['write_bytes'], int)
    assert disk_io_info['read_bytes'] >= 0
    assert disk_io_info['write_bytes'] >= 0


def test_metrics_collector_network_info():
    """
    测试网络信息收集返回正确的数据结构
    Test that network info collection returns correct data structure
    """
    collector = MetricsCollector()
    network_info = collector.get_network_info()
    
    # 验证返回的是字典
    # Verify that a dictionary is returned
    assert isinstance(network_info, dict)
    
    # 验证包含所有必需的键
    # Verify that all required keys are present
    assert 'bytes_sent' in network_info
    assert 'bytes_recv' in network_info
    assert 'packets_sent' in network_info
    assert 'packets_recv' in network_info
    
    # 验证数据类型和值范围
    # Verify data types and value ranges
    assert isinstance(network_info['bytes_sent'], int)
    assert isinstance(network_info['bytes_recv'], int)
    assert network_info['bytes_sent'] >= 0
    assert network_info['bytes_recv'] >= 0


def test_temperature_monitor_availability():
    """
    测试温度监控可用性检查
    Test temperature monitoring availability check
    """
    monitor = TemperatureMonitor()
    available = monitor.is_available()
    
    # 验证返回布尔值
    # Verify that a boolean is returned
    assert isinstance(available, bool)


def test_temperature_monitor_get_all_temperatures():
    """
    测试获取所有温度信息返回正确的数据结构
    Test that getting all temperatures returns correct data structure
    """
    monitor = TemperatureMonitor()
    temp_info = monitor.get_all_temperatures()
    
    # 验证返回的是字典
    # Verify that a dictionary is returned
    assert isinstance(temp_info, dict)
    
    # 验证包含所有必需的键
    # Verify that all required keys are present
    assert 'cpu_temp' in temp_info
    assert 'gpu_temp' in temp_info
    assert 'battery_temp' in temp_info
    assert 'sensors' in temp_info
    assert 'available' in temp_info
    
    # 验证数据类型
    # Verify data types
    assert isinstance(temp_info['available'], bool)
    assert isinstance(temp_info['sensors'], dict)
    
    # 如果可用，验证温度值在合理范围内
    # If available, verify temperature values are in reasonable ranges
    if temp_info['available'] and temp_info['cpu_temp'] is not None:
        assert -50 <= temp_info['cpu_temp'] <= 150


def test_process_manager_get_processes():
    """
    测试获取进程列表返回正确的数据结构
    Test that getting process list returns correct data structure
    """
    manager = ProcessManager()
    processes = manager.get_processes(limit=5)
    
    # 验证返回的是列表
    # Verify that a list is returned
    assert isinstance(processes, list)
    
    # 验证列表长度不超过限制
    # Verify list length doesn't exceed limit
    assert len(processes) <= 5
    
    # 如果有进程，验证数据结构
    # If there are processes, verify data structure
    if len(processes) > 0:
        process = processes[0]
        assert isinstance(process, dict)
        
        # 验证包含所有必需的键
        # Verify that all required keys are present
        assert 'pid' in process
        assert 'name' in process
        assert 'cpu_percent' in process
        assert 'memory_percent' in process
        assert 'memory_mb' in process
        assert 'status' in process
        assert 'username' in process
        assert 'cmdline' in process
        
        # 验证数据类型
        # Verify data types
        assert isinstance(process['pid'], int)
        assert isinstance(process['name'], str)
        assert isinstance(process['cpu_percent'], (int, float))
        assert isinstance(process['memory_percent'], (int, float))


def test_process_manager_get_process_by_pid():
    """
    测试根据PID获取进程信息
    Test getting process info by PID
    """
    manager = ProcessManager()
    
    # 获取当前进程的PID
    # Get current process PID
    import os
    current_pid = os.getpid()
    
    # 获取当前进程信息
    # Get current process info
    process = manager.get_process_by_pid(current_pid)
    
    # 验证返回的是字典
    # Verify that a dictionary is returned
    assert isinstance(process, dict)
    assert process['pid'] == current_pid
    
    # 测试不存在的PID
    # Test non-existent PID
    invalid_process = manager.get_process_by_pid(999999)
    assert invalid_process is None
