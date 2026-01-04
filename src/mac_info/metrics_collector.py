"""
指标收集器模块
Metrics Collector Module

该模块负责收集系统的各种性能指标，包括CPU、内存、磁盘I/O和网络统计信息。
This module is responsible for collecting various system performance metrics including CPU, memory, disk I/O, and network statistics.
"""

import psutil
from typing import Dict, Any
import logging

from .exceptions import MetricsCollectionError

# 配置日志记录器
# Configure logger
logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    指标收集器类，用于收集系统性能指标
    Metrics collector class for gathering system performance metrics
    """

    def __init__(self):
        """
        初始化指标收集器
        Initialize metrics collector
        """
        pass

    def get_cpu_info(self) -> Dict[str, Any]:
        """
        获取CPU使用信息
        Get CPU usage information

        使用psutil库收集CPU使用率、核心数和频率信息
        Uses psutil library to collect CPU usage, core count, and frequency information

        Returns:
            包含CPU信息的字典：
            Dictionary containing CPU information:
            {
                'overall_percent': float,      # 总体CPU使用率 / Overall CPU usage percentage
                'per_core_percent': list[float],  # 每个核心的使用率 / Per-core usage percentages
                'count': int,                  # CPU核心数 / Number of CPU cores
                'frequency': dict              # CPU频率信息 / CPU frequency information
            }

        Raises:
            MetricsCollectionError: 如果收集CPU指标失败 / If collecting CPU metrics fails
        """
        try:
            # 获取总体CPU使用率（1秒采样间隔）
            # Get overall CPU usage (1 second sampling interval)
            overall_percent = psutil.cpu_percent(interval=1)

            # 获取每个核心的CPU使用率
            # Get per-core CPU usage
            per_core_percent = psutil.cpu_percent(interval=0.1, percpu=True)

            # 获取CPU核心数（逻辑核心）
            # Get CPU core count (logical cores)
            count = psutil.cpu_count(logical=True)

            # 获取CPU频率信息
            # Get CPU frequency information
            freq = psutil.cpu_freq()
            frequency = {
                "current": freq.current if freq else 0,  # 当前频率 / Current frequency
                "min": freq.min if freq else 0,  # 最小频率 / Minimum frequency
                "max": freq.max if freq else 0,  # 最大频率 / Maximum frequency
            }

            return {
                "overall_percent": overall_percent,
                "per_core_percent": per_core_percent,
                "count": count,
                "frequency": frequency,
            }

        except Exception as e:
            # 记录错误并抛出自定义异常
            # Log error and raise custom exception
            logger.error(f"收集CPU指标失败 / Failed to collect CPU metrics: {e}")
            raise MetricsCollectionError(metric_type="CPU", original_error=e)

    def get_memory_info(self) -> Dict[str, Any]:
        """
        获取内存使用信息
        Get memory usage information

        使用psutil库收集物理内存和交换内存的使用情况
        Uses psutil library to collect physical and swap memory usage

        Returns:
            包含内存信息的字典：
            Dictionary containing memory information:
            {
                'total': int,        # 总内存（字节）/ Total memory (bytes)
                'available': int,    # 可用内存（字节）/ Available memory (bytes)
                'used': int,         # 已使用内存（字节）/ Used memory (bytes)
                'percent': float,    # 内存使用率 / Memory usage percentage
                'swap_total': int,   # 交换内存总量（字节）/ Total swap memory (bytes)
                'swap_used': int     # 已使用交换内存（字节）/ Used swap memory (bytes)
            }

        Raises:
            MetricsCollectionError: 如果收集内存指标失败 / If collecting memory metrics fails
        """
        try:
            # 获取虚拟内存信息
            # Get virtual memory information
            vm = psutil.virtual_memory()

            # 获取交换内存信息
            # Get swap memory information
            swap = psutil.swap_memory()

            return {
                "total": vm.total,
                "available": vm.available,
                "used": vm.used,
                "percent": vm.percent,
                "swap_total": swap.total,
                "swap_used": swap.used,
            }

        except Exception as e:
            # 记录错误并抛出自定义异常
            # Log error and raise custom exception
            logger.error(f"收集内存指标失败 / Failed to collect memory metrics: {e}")
            raise MetricsCollectionError(metric_type="memory", original_error=e)

    def get_disk_io_info(self) -> Dict[str, Any]:
        """
        获取磁盘I/O信息
        Get disk I/O information

        使用psutil库收集磁盘读写统计信息
        Uses psutil library to collect disk read/write statistics

        Returns:
            包含磁盘I/O信息的字典：
            Dictionary containing disk I/O information:
            {
                'read_bytes': int,   # 读取字节数 / Bytes read
                'write_bytes': int,  # 写入字节数 / Bytes written
                'read_count': int,   # 读取次数 / Read count
                'write_count': int   # 写入次数 / Write count
            }

        Raises:
            MetricsCollectionError: 如果收集磁盘I/O指标失败 / If collecting disk I/O metrics fails
        """
        try:
            # 获取磁盘I/O计数器
            # Get disk I/O counters
            disk_io = psutil.disk_io_counters()

            # 如果无法获取磁盘I/O信息，返回零值
            # If disk I/O information is unavailable, return zero values
            if disk_io is None:
                logger.warning(
                    "磁盘I/O信息不可用，返回零值 / Disk I/O information unavailable, returning zero values"
                )
                return {
                    "read_bytes": 0,
                    "write_bytes": 0,
                    "read_count": 0,
                    "write_count": 0,
                }

            return {
                "read_bytes": disk_io.read_bytes,
                "write_bytes": disk_io.write_bytes,
                "read_count": disk_io.read_count,
                "write_count": disk_io.write_count,
            }

        except Exception as e:
            # 记录错误并返回零值（优雅降级）
            # Log error and return zero values (graceful degradation)
            logger.error(
                f"收集磁盘I/O指标失败 / Failed to collect disk I/O metrics: {e}"
            )
            return {
                "read_bytes": 0,
                "write_bytes": 0,
                "read_count": 0,
                "write_count": 0,
            }

    def get_network_info(self) -> Dict[str, Any]:
        """
        获取网络I/O信息
        Get network I/O information

        使用psutil库收集网络发送和接收统计信息
        Uses psutil library to collect network send/receive statistics

        Returns:
            包含网络I/O信息的字典：
            Dictionary containing network I/O information:
            {
                'bytes_sent': int,     # 发送字节数 / Bytes sent
                'bytes_recv': int,     # 接收字节数 / Bytes received
                'packets_sent': int,   # 发送数据包数 / Packets sent
                'packets_recv': int    # 接收数据包数 / Packets received
            }

        Raises:
            MetricsCollectionError: 如果收集网络指标失败 / If collecting network metrics fails
        """
        try:
            # 获取网络I/O计数器
            # Get network I/O counters
            net_io = psutil.net_io_counters()

            # 如果无法获取网络I/O信息，返回零值
            # If network I/O information is unavailable, return zero values
            if net_io is None:
                logger.warning(
                    "网络I/O信息不可用，返回零值 / Network I/O information unavailable, returning zero values"
                )
                return {
                    "bytes_sent": 0,
                    "bytes_recv": 0,
                    "packets_sent": 0,
                    "packets_recv": 0,
                }

            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
            }

        except Exception as e:
            # 记录错误并返回零值（优雅降级）
            # Log error and return zero values (graceful degradation)
            logger.error(
                f"收集网络I/O指标失败 / Failed to collect network I/O metrics: {e}"
            )
            return {
                "bytes_sent": 0,
                "bytes_recv": 0,
                "packets_sent": 0,
                "packets_recv": 0,
            }
