# Design Document: mac-info

## Overview

mac-info is a Python-based terminal monitoring tool for macOS that provides real-time system performance metrics in a clean, visually appealing interface. The tool leverages the `psutil` library for cross-platform system monitoring, the `rich` library for beautiful terminal output formatting, and platform-specific tools for macOS temperature monitoring.

The architecture follows a modular design with clear separation of concerns:
- **CLI Interface Layer**: Handles command parsing and user interaction
- **Metrics Collection Layer**: Gathers system data from various sources
- **Display Layer**: Formats and presents data to the terminal
- **Integration Layer**: Provides direct access to system tools like `top`

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Interface                            │
│  (Command Parser, Help System, Argument Handler)            │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                  Controller Layer                            │
│         (Orchestrates data collection and display)           │
└──────┬──────────────────────────────────┬───────────────────┘
       │                                   │
       ▼                                   ▼
┌─────────────────────┐          ┌────────────────────────────┐
│  Metrics Collector  │          │   System Integration       │
│  - CPU Monitor      │          │   - top command wrapper    │
│  - Memory Monitor   │          │   - powermetrics wrapper   │
│  - Process Monitor  │          │                            │
│  - Disk I/O Monitor │          │                            │
│  - Network Monitor  │          │                            │
│  - Temp Monitor     │          │                            │
└──────┬──────────────┘          └────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Display Formatter                           │
│  (Rich library: Tables, Colors, Layouts, Live Display)      │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Python 3.8+**: Core programming language
- **psutil**: Cross-platform system and process monitoring
- **rich**: Terminal formatting, tables, colors, and live display
- **subprocess**: For invoking system commands (top, osx-cpu-temp, powermetrics)
- **argparse**: Command-line argument parsing


## Components and Interfaces

### 1. CLI Interface Component

**Purpose**: Parse command-line arguments and route to appropriate handlers

**Main Class**: `MacInfoCLI`

**Methods**:
```python
class MacInfoCLI:
    def __init__(self):
        """
        初始化CLI接口
        Initialize CLI interface
        """
        pass
    
    def parse_arguments(self) -> argparse.Namespace:
        """
        解析命令行参数
        Parse command-line arguments
        
        Returns:
            Parsed arguments namespace
        """
        pass
    
    def show_help(self) -> None:
        """
        显示帮助信息
        Display help information
        """
        pass
    
    def show_list(self) -> None:
        """
        显示可用命令列表
        Display list of available commands
        """
        pass
    
    def run(self) -> int:
        """
        运行CLI应用程序
        Run the CLI application
        
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        pass
```

**Commands**:
- `mac-info` - Show default monitoring view
- `mac-info help` - Display help information
- `mac-info list` - List all available commands
- `mac-info top [args]` - Invoke system top command
- `mac-info monitor` - Start interactive monitoring mode
- `mac-info --refresh N` - Set refresh interval (default: 2 seconds)


### 2. Metrics Collector Component

**Purpose**: Collect system metrics from various sources

**Main Class**: `MetricsCollector`

**Methods**:
```python
class MetricsCollector:
    def get_cpu_info(self) -> dict:
        """
        获取CPU使用信息
        Get CPU usage information
        
        Returns:
            {
                'overall_percent': float,
                'per_core_percent': list[float],
                'count': int,
                'frequency': dict
            }
        """
        pass
    
    def get_memory_info(self) -> dict:
        """
        获取内存使用信息
        Get memory usage information
        
        Returns:
            {
                'total': int,
                'available': int,
                'used': int,
                'percent': float,
                'swap_total': int,
                'swap_used': int
            }
        """
        pass
    
    def get_disk_io_info(self) -> dict:
        """
        获取磁盘I/O信息
        Get disk I/O information
        
        Returns:
            {
                'read_bytes': int,
                'write_bytes': int,
                'read_count': int,
                'write_count': int
            }
        """
        pass
    
    def get_network_info(self) -> dict:
        """
        获取网络I/O信息
        Get network I/O information
        
        Returns:
            {
                'bytes_sent': int,
                'bytes_recv': int,
                'packets_sent': int,
                'packets_recv': int
            }
        """
        pass
    
    def get_temperature_info(self) -> dict:
        """
        获取系统温度信息
        Get system temperature information
        
        Returns:
            {
                'cpu_temp': float or None,
                'gpu_temp': float or None,
                'battery_temp': float or None,
                'sensors': dict,
                'available': bool
            }
        """
        pass
```


### 3. Process Manager Component

**Purpose**: Manage and retrieve process information

**Main Class**: `ProcessManager`

**Methods**:
```python
class ProcessManager:
    def get_processes(self, sort_by: str = 'cpu', limit: int = 10) -> list[dict]:
        """
        获取进程列表
        Get list of processes
        
        Args:
            sort_by: Sort criterion ('cpu', 'memory', 'pid', 'name')
            limit: Maximum number of processes to return
        
        Returns:
            List of process dictionaries with keys:
            {
                'pid': int,
                'name': str,
                'cpu_percent': float,
                'memory_percent': float,
                'memory_mb': float,
                'status': str,
                'username': str,
                'cmdline': str
            }
        """
        pass
    
    def get_process_by_pid(self, pid: int) -> dict or None:
        """
        根据PID获取进程信息
        Get process information by PID
        
        Args:
            pid: Process ID
        
        Returns:
            Process dictionary or None if not found
        """
        pass
```

### 4. Temperature Monitor Component

**Purpose**: Monitor system temperatures using macOS-specific tools

**Main Class**: `TemperatureMonitor`

**Implementation Strategy**:

The temperature monitoring will use a fallback approach:
1. **Primary**: Try `osx-cpu-temp` command (requires Homebrew installation)
2. **Secondary**: Try `powermetrics` command (requires sudo, built-in to macOS)
3. **Fallback**: Return unavailable status with helpful message

**Methods**:
```python
class TemperatureMonitor:
    def __init__(self):
        """
        初始化温度监控器并检测可用的温度读取方法
        Initialize temperature monitor and detect available temperature reading methods
        """
        pass
    
    def is_available(self) -> bool:
        """
        检查温度监控是否可用
        Check if temperature monitoring is available
        
        Returns:
            True if any temperature reading method is available
        """
        pass
    
    def get_cpu_temperature(self) -> float or None:
        """
        获取CPU温度（摄氏度）
        Get CPU temperature in Celsius
        
        Returns:
            Temperature in Celsius or None if unavailable
        """
        pass
    
    def get_all_temperatures(self) -> dict:
        """
        获取所有可用的温度传感器数据
        Get all available temperature sensor data
        
        Returns:
            Dictionary with sensor names and temperatures
        """
        pass
```


### 5. Display Formatter Component

**Purpose**: Format and display metrics using the Rich library

**Main Class**: `DisplayFormatter`

**Methods**:
```python
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.live import Live

class DisplayFormatter:
    def __init__(self):
        """
        初始化显示格式化器
        Initialize display formatter
        """
        self.console = Console()
    
    def create_cpu_panel(self, cpu_info: dict) -> Table:
        """
        创建CPU信息面板
        Create CPU information panel
        
        Args:
            cpu_info: CPU information dictionary
        
        Returns:
            Rich Table object
        """
        pass
    
    def create_memory_panel(self, memory_info: dict) -> Table:
        """
        创建内存信息面板
        Create memory information panel
        
        Args:
            memory_info: Memory information dictionary
        
        Returns:
            Rich Table object
        """
        pass
    
    def create_process_table(self, processes: list[dict]) -> Table:
        """
        创建进程信息表格
        Create process information table
        
        Args:
            processes: List of process dictionaries
        
        Returns:
            Rich Table object
        """
        pass
    
    def create_temperature_panel(self, temp_info: dict) -> Table:
        """
        创建温度信息面板
        Create temperature information panel
        
        Args:
            temp_info: Temperature information dictionary
        
        Returns:
            Rich Table object
        """
        pass
    
    def create_network_panel(self, network_info: dict) -> Table:
        """
        创建网络信息面板
        Create network information panel
        
        Args:
            network_info: Network information dictionary
        
        Returns:
            Rich Table object
        """
        pass
    
    def create_dashboard(self, all_metrics: dict) -> Layout:
        """
        创建完整的监控仪表板
        Create complete monitoring dashboard
        
        Args:
            all_metrics: Dictionary containing all collected metrics
        
        Returns:
            Rich Layout object
        """
        pass
    
    def get_color_for_percentage(self, percent: float) -> str:
        """
        根据百分比返回颜色
        Return color based on percentage
        
        Args:
            percent: Percentage value (0-100)
        
        Returns:
            Color name for Rich formatting
        """
        # Green: 0-60%, Yellow: 60-80%, Red: 80-100%
        pass
    
    def format_bytes(self, bytes_value: int) -> str:
        """
        格式化字节数为人类可读格式
        Format bytes to human-readable format
        
        Args:
            bytes_value: Number of bytes
        
        Returns:
            Formatted string (e.g., "1.5 GB", "256 MB")
        """
        pass
```


### 6. System Integration Component

**Purpose**: Provide direct access to system commands

**Main Class**: `SystemIntegration`

**Methods**:
```python
import subprocess

class SystemIntegration:
    @staticmethod
    def invoke_top(args: list[str] = None) -> int:
        """
        调用系统top命令
        Invoke system top command
        
        Args:
            args: Additional arguments to pass to top
        
        Returns:
            Exit code from top command
        """
        pass
    
    @staticmethod
    def check_platform() -> bool:
        """
        检查是否运行在macOS上
        Check if running on macOS
        
        Returns:
            True if running on macOS
        """
        pass
    
    @staticmethod
    def check_command_available(command: str) -> bool:
        """
        检查命令是否可用
        Check if command is available
        
        Args:
            command: Command name to check
        
        Returns:
            True if command is available
        """
        pass
```

## Data Models

### MetricsSnapshot

A complete snapshot of all system metrics at a point in time:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MetricsSnapshot:
    """
    系统指标快照
    System metrics snapshot
    """
    timestamp: float
    cpu: dict
    memory: dict
    disk_io: dict
    network: dict
    temperature: dict
    processes: list[dict]
    
    def to_dict(self) -> dict:
        """
        转换为字典
        Convert to dictionary
        """
        pass
```

### ProcessInfo

Information about a single process:

```python
@dataclass
class ProcessInfo:
    """
    进程信息
    Process information
    """
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    status: str
    username: str
    cmdline: str
    
    def to_dict(self) -> dict:
        """
        转换为字典
        Convert to dictionary
        """
        pass
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Acceptance Criteria Testing Prework

**Requirement 1: Command-Line Interface**

1.1 WHEN a user executes `mac-info help`, THE CLI_Interface SHALL display a comprehensive help message
Thoughts: This is testing that a specific command produces output containing help information. We can test this by executing the help command and verifying the output contains expected help text sections.
Testable: yes - example

1.2 WHEN a user executes `mac-info list`, THE CLI_Interface SHALL display a list of all available commands
Thoughts: This is testing that a specific command produces output. We can verify the output contains all expected command names.
Testable: yes - example

1.3 WHEN a user executes `mac-info` without arguments, THE CLI_Interface SHALL display a brief usage message
Thoughts: This is testing a specific case - no arguments. This is an example test.
Testable: yes - example

1.4 WHEN a user provides an invalid command, THE CLI_Interface SHALL display an error message
Thoughts: This is about error handling for any invalid input. We can generate random invalid commands and ensure they all produce error messages.
Testable: yes - property

**Requirement 2: System Monitoring Display**

2.1-2.6 WHEN a user executes the monitoring command, THE System_Monitor SHALL collect and display various metrics
Thoughts: These are testing that the monitoring function returns data structures with expected fields. We can verify that all required fields are present and have valid types.
Testable: yes - property

2.7 WHEN displaying metrics, THE System_Monitor SHALL refresh the display at regular intervals
Thoughts: This is about timing behavior which is difficult to test reliably in unit tests.
Testable: no

**Requirement 3: Top Command Integration**

3.1 WHEN a user executes `mac-info top`, THE System_Monitor SHALL invoke the macOS top command
Thoughts: This is testing that a specific command triggers a system call. We can mock the subprocess call and verify it was invoked.
Testable: yes - example

3.2 WHEN invoking the top command, THE System_Monitor SHALL pass through any additional arguments
Thoughts: This is about argument forwarding for any set of arguments. We can generate random argument lists and verify they're passed correctly.
Testable: yes - property


**Requirement 4: Beautiful Output Formatting**

4.1-4.6 WHEN displaying metrics, THE Display_Formatter SHALL use various formatting features
Thoughts: These are about visual presentation which is subjective and difficult to test automatically. However, we can test that formatting functions produce valid Rich objects and contain expected content.
Testable: yes - property (for structure, not aesthetics)

**Requirement 5: Virtual Environment Setup**

5.1-5.4 THE mac-info SHALL include setup instructions and requirements
Thoughts: These are about documentation and project structure, not runtime behavior.
Testable: no

**Requirement 6: macOS System API Integration**

6.1-6.5 WHEN collecting metrics, THE Metrics_Collector SHALL use system APIs
Thoughts: These are testing that metric collection functions return valid data structures. We can verify all required fields are present and have valid types/ranges.
Testable: yes - property

6.6 IF a system API call fails, THEN THE Metrics_Collector SHALL handle the error gracefully
Thoughts: This is about error handling. We can simulate API failures and verify graceful handling.
Testable: yes - property

**Requirement 7: Code Documentation**

7.1-7.4 THE mac-info SHALL include bilingual comments
Thoughts: This is about code style and documentation, not runtime behavior.
Testable: no

**Requirement 8: Error Handling and Robustness**

8.1-8.5 Error handling requirements
Thoughts: These are about error handling across various failure scenarios. We can simulate different error conditions and verify appropriate responses.
Testable: yes - property

**Requirement 9: Detailed Process Information**

9.1-9.9 WHEN displaying process information, THE Process_Manager SHALL show various fields
Thoughts: This is testing that process information contains all required fields. We can verify the data structure for any process.
Testable: yes - property

**Requirement 10: Temperature Monitoring**

10.1-10.7 Temperature monitoring requirements
Thoughts: These are testing that temperature collection returns valid data structures with expected fields. We can verify structure and value ranges.
Testable: yes - property


### Property Reflection

After reviewing all testable properties, I've identified the following consolidations:

- Requirements 2.1-2.6 can be combined into a single property about metric collection completeness
- Requirements 4.1-4.6 can be combined into a property about display formatter output validity
- Requirements 6.1-6.5 can be combined into a property about metrics data structure validity
- Requirements 9.1-9.9 can be combined into a property about process information completeness
- Requirements 10.1-10.6 can be combined into a property about temperature data structure validity

This reduces redundancy while maintaining comprehensive coverage.

### Properties

**Property 1: Invalid command error handling**
*For any* string that is not a valid mac-info command, executing it should result in an error message being displayed and a non-zero exit code.
**Validates: Requirements 1.4**

**Property 2: Argument pass-through preservation**
*For any* list of command-line arguments provided to the top command wrapper, all arguments should be passed to the system top command in the same order.
**Validates: Requirements 3.2**

**Property 3: Metrics collection completeness**
*For any* call to collect system metrics, the returned data structure should contain all required fields (cpu, memory, disk_io, network, temperature) with valid types.
**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**

**Property 4: Display formatter output validity**
*For any* valid metrics dictionary, the display formatter should produce Rich objects (Table, Layout) without raising exceptions and the output should contain all metric values.
**Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6**

**Property 5: Metrics data structure validity**
*For any* metric collection function (CPU, memory, disk, network), the returned dictionary should have all expected keys and values should be within valid ranges (percentages 0-100, bytes >= 0, etc.).
**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

**Property 6: Error handling graceful degradation**
*For any* simulated API failure in metrics collection, the system should return a valid error indicator (None or error dict) without crashing and should log appropriate error information.
**Validates: Requirements 6.6, 8.1, 8.4, 8.5**

**Property 7: Process information completeness**
*For any* process returned by the process manager, the process dictionary should contain all required fields (pid, name, cpu_percent, memory_percent, memory_mb, status, username, cmdline) with valid types.
**Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.9**

**Property 8: Temperature data structure validity**
*For any* call to get temperature information, the returned dictionary should have the 'available' field and if available is True, should contain valid temperature values (floats or None) within reasonable ranges (-50 to 150 Celsius).
**Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7**

**Property 9: Byte formatting consistency**
*For any* non-negative integer byte value, formatting it to human-readable form and parsing the unit should preserve the magnitude within reasonable precision (< 1% error for values > 1KB).
**Validates: Requirements 4.4**

**Property 10: Color coding consistency**
*For any* percentage value, the color returned by get_color_for_percentage should be consistent: green for 0-60%, yellow for 60-80%, red for 80-100%.
**Validates: Requirements 4.3**


## Error Handling

### Error Categories

1. **Platform Errors**
   - Running on non-macOS system
   - Missing required system commands
   - Insufficient permissions

2. **API Errors**
   - System API unavailable
   - Permission denied for system calls
   - Timeout reading system metrics

3. **Data Errors**
   - Invalid metric values
   - Missing expected data fields
   - Parsing errors from system commands

4. **User Input Errors**
   - Invalid command arguments
   - Unknown commands
   - Invalid option values

### Error Handling Strategy

**Graceful Degradation**:
- If temperature monitoring is unavailable, display message and continue with other metrics
- If specific metrics fail, show "N/A" for that metric and continue
- If process information is incomplete, show available fields only

**Clear Error Messages**:
```python
class MacInfoError(Exception):
    """
    基础错误类
    Base error class for mac-info
    """
    pass

class PlatformError(MacInfoError):
    """
    平台不兼容错误
    Platform incompatibility error
    """
    pass

class PermissionError(MacInfoError):
    """
    权限不足错误
    Insufficient permission error
    """
    pass

class MetricsCollectionError(MacInfoError):
    """
    指标收集错误
    Metrics collection error
    """
    pass
```

**Error Recovery**:
- Log errors to stderr with timestamps
- Continue operation when possible
- Provide actionable suggestions (e.g., "Install osx-cpu-temp with: brew install osx-cpu-temp")
- Exit gracefully with appropriate exit codes

**Exit Codes**:
- 0: Success
- 1: General error
- 2: Platform incompatibility
- 3: Permission denied
- 4: Missing dependencies


## Testing Strategy

### Dual Testing Approach

We will use both unit tests and property-based tests to ensure comprehensive coverage:

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Test help command output contains expected sections
- Test list command output contains all commands
- Test specific metric values are formatted correctly
- Test error messages for known failure scenarios
- Test integration with mocked system commands

**Property-Based Tests**: Verify universal properties across all inputs
- Test invalid commands always produce errors
- Test metric collection always returns complete data structures
- Test display formatting works for any valid metrics
- Test byte formatting preserves magnitude
- Test color coding is consistent across all percentages

### Property-Based Testing Framework

We will use **Hypothesis** for property-based testing in Python.

**Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with: `# Feature: mac-info-tool, Property N: [property description]`
- Use custom strategies for generating valid metric dictionaries
- Use Hypothesis's `assume()` to filter invalid test cases

**Example Test Structure**:
```python
from hypothesis import given, strategies as st
import pytest

# Feature: mac-info-tool, Property 5: Metrics data structure validity
@given(st.floats(min_value=0, max_value=100))
def test_cpu_percent_in_valid_range(cpu_percent):
    """
    测试CPU百分比在有效范围内
    Test CPU percentage is in valid range
    """
    collector = MetricsCollector()
    # Mock psutil to return our test value
    with patch('psutil.cpu_percent', return_value=cpu_percent):
        cpu_info = collector.get_cpu_info()
        assert 0 <= cpu_info['overall_percent'] <= 100
```

### Test Coverage Goals

- **Unit Test Coverage**: 80%+ of code lines
- **Property Test Coverage**: All 10 correctness properties implemented
- **Integration Tests**: CLI commands, system integration
- **Edge Cases**: Empty data, extreme values, missing permissions

### Testing Tools

- **pytest**: Test runner and framework
- **hypothesis**: Property-based testing
- **pytest-cov**: Coverage reporting
- **unittest.mock**: Mocking system calls and external dependencies
