"""
系统集成模块 - 提供系统命令和平台检查功能
System Integration Module - Provides system command and platform checking functionality

该模块提供与操作系统的集成功能，包括平台检查、命令可用性检查和系统命令调用。
This module provides integration with the operating system, including platform checking,
command availability checking, and system command invocation.
"""

import platform
import subprocess
import shutil
from typing import List, Optional


class SystemIntegration:
    """
    系统集成类 - 提供系统级操作的静态方法
    System Integration Class - Provides static methods for system-level operations

    该类提供了与操作系统交互的核心功能，包括：
    - 平台检测（确保在macOS上运行）
    - 命令可用性检查
    - 系统top命令调用

    This class provides core functionality for interacting with the operating system:
    - Platform detection (ensuring running on macOS)
    - Command availability checking
    - System top command invocation
    """

    @staticmethod
    def check_platform() -> bool:
        """
        检查是否运行在macOS上
        Check if running on macOS

        该方法检测当前操作系统是否为macOS（Darwin）。
        mac-info工具专为macOS设计，需要macOS特定的API和命令。

        This method detects if the current operating system is macOS (Darwin).
        The mac-info tool is designed specifically for macOS and requires
        macOS-specific APIs and commands.

        Returns:
            bool: 如果运行在macOS上返回True，否则返回False
                  True if running on macOS, False otherwise

        Example:
            >>> if SystemIntegration.check_platform():
            ...     print("Running on macOS")
            ... else:
            ...     print("Not running on macOS")
        """
        return platform.system() == "Darwin"

    @staticmethod
    def check_command_available(command: str) -> bool:
        """
        检查命令是否可用
        Check if command is available

        该方法检查指定的命令是否在系统PATH中可用。
        使用shutil.which()来查找命令的完整路径。

        This method checks if the specified command is available in the system PATH.
        Uses shutil.which() to find the full path of the command.

        Args:
            command (str): 要检查的命令名称（例如："top", "osx-cpu-temp"）
                          Command name to check (e.g., "top", "osx-cpu-temp")

        Returns:
            bool: 如果命令可用返回True，否则返回False
                  True if command is available, False otherwise

        Example:
            >>> if SystemIntegration.check_command_available("top"):
            ...     print("top command is available")
            >>> if SystemIntegration.check_command_available("osx-cpu-temp"):
            ...     print("osx-cpu-temp is installed")
        """
        return shutil.which(command) is not None

    @staticmethod
    def invoke_top(args: Optional[List[str]] = None) -> int:
        """
        调用系统top命令
        Invoke system top command

        该方法调用macOS的top命令，并可选地传递额外的参数。
        top命令在当前终端中运行，用户可以像直接运行top一样与其交互。

        This method invokes the macOS top command with optional additional arguments.
        The top command runs in the current terminal, allowing users to interact
        with it as if they ran top directly.

        Args:
            args (Optional[List[str]]): 传递给top命令的额外参数列表
                                       Additional arguments to pass to top command
                                       例如 / Example: ["-l", "1"] for one iteration
                                       例如 / Example: ["-n", "20"] for top 20 processes

        Returns:
            int: top命令的退出码（0表示成功，非零表示错误）
                 Exit code from top command (0 for success, non-zero for error)

        Raises:
            FileNotFoundError: 如果top命令不可用
                              If top command is not available
            subprocess.SubprocessError: 如果执行top命令时发生错误
                                       If an error occurs while executing top

        Example:
            >>> # 运行默认的top命令 / Run default top command
            >>> exit_code = SystemIntegration.invoke_top()
            >>>
            >>> # 运行top命令并只显示一次迭代 / Run top with one iteration
            >>> exit_code = SystemIntegration.invoke_top(["-l", "1"])
            >>>
            >>> # 运行top命令并按内存排序 / Run top sorted by memory
            >>> exit_code = SystemIntegration.invoke_top(["-o", "mem"])
        """
        # 构建完整的命令列表
        # Build the complete command list
        command = ["top"]

        # 如果提供了额外参数，添加到命令列表中
        # If additional arguments are provided, add them to the command list
        if args:
            command.extend(args)

        try:
            # 使用subprocess.run()执行top命令
            # 不捕获输出，让top直接在终端中显示
            # Use subprocess.run() to execute the top command
            # Don't capture output, let top display directly in the terminal
            result = subprocess.run(command, check=False)

            # 返回top命令的退出码
            # Return the exit code from the top command
            return result.returncode

        except FileNotFoundError:
            # top命令不存在（理论上不应该发生在macOS上）
            # top command doesn't exist (shouldn't happen on macOS)
            raise FileNotFoundError(f"Command 'top' not found in system PATH")

        except subprocess.SubprocessError as e:
            # 执行top命令时发生其他错误
            # Other error occurred while executing top
            raise subprocess.SubprocessError(f"Error executing top command: {e}")
