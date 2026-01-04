"""
mac-info-tool: macOS 终端监控工具
mac-info-tool: macOS terminal monitoring tool

A beautiful terminal-based system monitoring tool for macOS.
"""

__version__ = "0.1.0"
__author__ = "mac-info-tool contributors"

from .models import ProcessInfo, MetricsSnapshot
from .exceptions import (
    MacInfoError,
    PlatformError,
    PermissionError,
    MetricsCollectionError,
)

__all__ = [
    "ProcessInfo",
    "MetricsSnapshot",
    "MacInfoError",
    "PlatformError",
    "PermissionError",
    "MetricsCollectionError",
]
