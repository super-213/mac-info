"""
温度监控模块
Temperature Monitor Module

该模块负责监控macOS系统的温度信息，包括CPU、GPU和其他传感器的温度数据。
This module is responsible for monitoring macOS system temperatures including CPU, GPU, and other sensor data.
"""

import subprocess
import re
from typing import Dict, Any, Optional
import logging

from .exceptions import MetricsCollectionError, PermissionError

# 配置日志记录器
# Configure logger
logger = logging.getLogger(__name__)


class TemperatureMonitor:
    """
    温度监控器类，用于收集系统温度信息
    Temperature monitor class for gathering system temperature information
    """

    def __init__(self):
        """
        初始化温度监控器并检测可用的温度读取方法
        Initialize temperature monitor and detect available temperature reading methods
        """
        self._osx_cpu_temp_available = self._check_osx_cpu_temp()
        self._powermetrics_available = self._check_powermetrics()

    def _check_osx_cpu_temp(self) -> bool:
        """
        检查osx-cpu-temp命令是否可用
        Check if osx-cpu-temp command is available

        Returns:
            如果osx-cpu-temp可用则返回True / True if osx-cpu-temp is available
        """
        try:
            result = subprocess.run(
                ["which", "osx-cpu-temp"], capture_output=True, text=True, timeout=2
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False

    def _check_powermetrics(self) -> bool:
        """
        检查powermetrics命令是否可用
        Check if powermetrics command is available

        Returns:
            如果powermetrics可用则返回True / True if powermetrics is available
        """
        try:
            result = subprocess.run(
                ["which", "powermetrics"], capture_output=True, text=True, timeout=2
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False

    def is_available(self) -> bool:
        """
        检查温度监控是否可用
        Check if temperature monitoring is available

        Returns:
            如果任何温度读取方法可用则返回True / True if any temperature reading method is available
        """
        return self._osx_cpu_temp_available or self._powermetrics_available

    def _get_temp_from_osx_cpu_temp(self) -> Optional[float]:
        """
        使用osx-cpu-temp命令获取CPU温度
        Get CPU temperature using osx-cpu-temp command

        Returns:
            CPU温度（摄氏度）或None / CPU temperature in Celsius or None
        """
        try:
            result = subprocess.run(
                ["osx-cpu-temp"], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                # osx-cpu-temp输出格式: "XX.X°C"
                # osx-cpu-temp output format: "XX.X°C"
                output = result.stdout.strip()
                match = re.search(r"([\d.]+)°?C", output)
                if match:
                    return float(match.group(1))
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError, Exception):
            pass

        return None

    def _get_temp_from_powermetrics(self) -> Optional[float]:
        """
        使用powermetrics命令获取CPU温度（需要sudo权限）
        Get CPU temperature using powermetrics command (requires sudo)

        Returns:
            CPU温度（摄氏度）或None / CPU temperature in Celsius or None
        """
        try:
            # powermetrics需要sudo权限，这里尝试不使用sudo运行
            # powermetrics requires sudo, attempting to run without sudo
            result = subprocess.run(
                ["powermetrics", "--samplers", "smc", "-i", "1", "-n", "1"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                # 解析powermetrics输出中的CPU温度
                # Parse CPU temperature from powermetrics output
                output = result.stdout
                match = re.search(r"CPU die temperature:\s*([\d.]+)\s*C", output)
                if match:
                    return float(match.group(1))
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError, Exception):
            pass

        return None

    def get_cpu_temperature(self) -> Optional[float]:
        """
        获取CPU温度（摄氏度）
        Get CPU temperature in Celsius

        使用回退策略：首先尝试osx-cpu-temp，然后尝试powermetrics
        Uses fallback strategy: first try osx-cpu-temp, then try powermetrics

        Returns:
            CPU温度（摄氏度）或None（如果不可用）/ Temperature in Celsius or None if unavailable
        """
        # 首先尝试osx-cpu-temp（更快，不需要sudo）
        # First try osx-cpu-temp (faster, doesn't require sudo)
        if self._osx_cpu_temp_available:
            temp = self._get_temp_from_osx_cpu_temp()
            if temp is not None:
                return temp

        # 回退到powermetrics
        # Fallback to powermetrics
        if self._powermetrics_available:
            temp = self._get_temp_from_powermetrics()
            if temp is not None:
                return temp

        # 如果所有方法都失败，返回None
        # If all methods fail, return None
        return None

    def get_all_temperatures(self) -> Dict[str, Any]:
        """
        获取所有可用的温度传感器数据
        Get all available temperature sensor data

        Returns:
            包含温度信息的字典：
            Dictionary containing temperature information:
            {
                'cpu_temp': float or None,      # CPU温度 / CPU temperature
                'gpu_temp': float or None,      # GPU温度 / GPU temperature
                'battery_temp': float or None,  # 电池温度 / Battery temperature
                'sensors': dict,                # 其他传感器 / Other sensors
                'available': bool               # 温度监控是否可用 / Whether monitoring is available
            }
        """
        try:
            # 检查温度监控是否可用
            # Check if temperature monitoring is available
            available = self.is_available()

            if not available:
                logger.warning("温度监控不可用 / Temperature monitoring unavailable")
                logger.info(
                    "提示：安装osx-cpu-temp以启用温度监控 / Tip: Install osx-cpu-temp to enable temperature monitoring"
                )
                logger.info("安装命令 / Install command: brew install osx-cpu-temp")
                return {
                    "cpu_temp": None,
                    "gpu_temp": None,
                    "battery_temp": None,
                    "sensors": {},
                    "available": False,
                }

            # 获取CPU温度
            # Get CPU temperature
            cpu_temp = self.get_cpu_temperature()

            # 注意：GPU和电池温度需要更复杂的解析，这里暂时返回None
            # Note: GPU and battery temperatures require more complex parsing, returning None for now
            # 可以通过解析powermetrics的完整输出来获取更多传感器数据
            # More sensor data can be obtained by parsing full powermetrics output

            return {
                "cpu_temp": cpu_temp,
                "gpu_temp": None,  # 需要额外实现 / Requires additional implementation
                "battery_temp": None,  # 需要额外实现 / Requires additional implementation
                "sensors": {},  # 可以添加其他传感器数据 / Can add other sensor data
                "available": True,
            }

        except Exception as e:
            # 记录错误并返回不可用状态（优雅降级）
            # Log error and return unavailable status (graceful degradation)
            logger.error(
                f"收集温度信息失败 / Failed to collect temperature information: {e}"
            )
            return {
                "cpu_temp": None,
                "gpu_temp": None,
                "battery_temp": None,
                "sensors": {},
                "available": False,
            }
