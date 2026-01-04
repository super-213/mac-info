"""
数据模型模块
Data Models Module

该模块定义了mac-info工具使用的数据类和类型定义。
This module defines data classes and type definitions used by the mac-info tool.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time


@dataclass
class ProcessInfo:
    """
    进程信息数据类
    Process information data class

    该类表示单个进程的详细信息。
    This class represents detailed information about a single process.

    Attributes:
        pid: 进程ID / Process ID
        name: 进程名称 / Process name
        cpu_percent: CPU使用率百分比 / CPU usage percentage
        memory_percent: 内存使用率百分比 / Memory usage percentage
        memory_mb: 内存使用量（MB）/ Memory usage in MB
        status: 进程状态 / Process status (e.g., 'running', 'sleeping')
        username: 进程所有者用户名 / Process owner username
        cmdline: 启动进程的命令行 / Command line that started the process
    """

    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    status: str
    username: str
    cmdline: str

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        Convert to dictionary

        将ProcessInfo对象转换为字典格式，便于序列化和传输。
        Converts ProcessInfo object to dictionary format for serialization and transmission.

        Returns:
            包含所有进程信息的字典 / Dictionary containing all process information
        """
        return {
            "pid": self.pid,
            "name": self.name,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_mb": self.memory_mb,
            "status": self.status,
            "username": self.username,
            "cmdline": self.cmdline,
        }


@dataclass
class MetricsSnapshot:
    """
    系统指标快照数据类
    System metrics snapshot data class

    该类表示某一时刻的完整系统指标快照，包括CPU、内存、磁盘I/O、
    网络、温度和进程信息。

    This class represents a complete snapshot of system metrics at a point in time,
    including CPU, memory, disk I/O, network, temperature, and process information.

    Attributes:
        timestamp: 快照时间戳（Unix时间）/ Snapshot timestamp (Unix time)
        cpu: CPU信息字典 / CPU information dictionary
        memory: 内存信息字典 / Memory information dictionary
        disk_io: 磁盘I/O信息字典 / Disk I/O information dictionary
        network: 网络信息字典 / Network information dictionary
        temperature: 温度信息字典 / Temperature information dictionary
        processes: 进程信息列表 / Process information list
    """

    timestamp: float = field(default_factory=time.time)
    cpu: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, Any] = field(default_factory=dict)
    disk_io: Dict[str, Any] = field(default_factory=dict)
    network: Dict[str, Any] = field(default_factory=dict)
    temperature: Dict[str, Any] = field(default_factory=dict)
    processes: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        Convert to dictionary

        将MetricsSnapshot对象转换为字典格式，便于序列化和传输。
        Converts MetricsSnapshot object to dictionary format for serialization and transmission.

        Returns:
            包含所有系统指标的字典 / Dictionary containing all system metrics
        """
        return {
            "timestamp": self.timestamp,
            "cpu": self.cpu,
            "memory": self.memory,
            "disk_io": self.disk_io,
            "network": self.network,
            "temperature": self.temperature,
            "processes": self.processes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetricsSnapshot":
        """
        从字典创建MetricsSnapshot对象
        Create MetricsSnapshot object from dictionary

        从字典数据创建MetricsSnapshot实例，用于反序列化。
        Creates a MetricsSnapshot instance from dictionary data for deserialization.

        Args:
            data: 包含指标数据的字典 / Dictionary containing metrics data

        Returns:
            MetricsSnapshot对象 / MetricsSnapshot object
        """
        return cls(
            timestamp=data.get("timestamp", time.time()),
            cpu=data.get("cpu", {}),
            memory=data.get("memory", {}),
            disk_io=data.get("disk_io", {}),
            network=data.get("network", {}),
            temperature=data.get("temperature", {}),
            processes=data.get("processes", []),
        )
