"""
异常类模块
Exceptions Module

该模块定义了mac-info工具使用的自定义异常类。
This module defines custom exception classes used by the mac-info tool.
"""


class MacInfoError(Exception):
    """
    基础错误类
    Base error class for mac-info

    所有mac-info特定异常的基类。
    Base class for all mac-info specific exceptions.

    Attributes:
        message: 错误消息 / Error message
    """

    def __init__(self, message: str):
        """
        初始化基础错误
        Initialize base error

        Args:
            message: 错误消息 / Error message
        """
        self.message = message
        super().__init__(self.message)


class PlatformError(MacInfoError):
    """
    平台不兼容错误
    Platform incompatibility error

    当工具在非macOS平台上运行时抛出此异常。
    Raised when the tool is run on a non-macOS platform.

    Example:
        >>> if not is_macos():
        ...     raise PlatformError("mac-info requires macOS")
    """

    def __init__(
        self,
        message: str = "mac-info只能在macOS系统上运行 / mac-info can only run on macOS",
    ):
        """
        初始化平台错误
        Initialize platform error

        Args:
            message: 错误消息 / Error message (默认提供 / default provided)
        """
        super().__init__(message)


class PermissionError(MacInfoError):
    """
    权限不足错误
    Insufficient permission error

    当工具需要但缺少必要权限时抛出此异常。
    Raised when the tool requires but lacks necessary permissions.

    Example:
        >>> if not has_permission():
        ...     raise PermissionError("需要管理员权限 / Administrator privileges required")
    """

    def __init__(self, message: str = "权限不足 / Insufficient permissions"):
        """
        初始化权限错误
        Initialize permission error

        Args:
            message: 错误消息 / Error message (默认提供 / default provided)
        """
        super().__init__(message)


class MetricsCollectionError(MacInfoError):
    """
    指标收集错误
    Metrics collection error

    当收集系统指标时发生错误时抛出此异常。
    Raised when an error occurs while collecting system metrics.

    Attributes:
        metric_type: 指标类型 / Metric type (e.g., 'cpu', 'memory', 'temperature')
        original_error: 原始异常 / Original exception (if any)

    Example:
        >>> try:
        ...     collect_cpu_metrics()
        ... except Exception as e:
        ...     raise MetricsCollectionError("CPU", original_error=e)
    """

    def __init__(
        self,
        metric_type: str = None,
        message: str = None,
        original_error: Exception = None,
    ):
        """
        初始化指标收集错误
        Initialize metrics collection error

        Args:
            metric_type: 指标类型 / Metric type (可选 / optional)
            message: 自定义错误消息 / Custom error message (可选 / optional)
            original_error: 原始异常 / Original exception (可选 / optional)
        """
        self.metric_type = metric_type
        self.original_error = original_error

        # 构建错误消息
        # Build error message
        if message:
            error_message = message
        elif metric_type:
            error_message = (
                f"收集{metric_type}指标时出错 / Error collecting {metric_type} metrics"
            )
        else:
            error_message = "收集系统指标时出错 / Error collecting system metrics"

        # 如果有原始异常，添加到消息中
        # If there's an original exception, add it to the message
        if original_error:
            error_message += f": {str(original_error)}"

        super().__init__(error_message)
