"""
mac-info 主入口模块
mac-info Main Entry Module

该模块提供 python -m mac_info 执行方式的入口点。
This module provides the entry point for python -m mac_info execution.

使用方法 / Usage:
    python -m mac_info [command] [options]
    
示例 / Examples:
    python -m mac_info help
    python -m mac_info monitor --refresh 5
    python -m mac_info top
"""

import sys
from .cli import MacInfoCLI
from .system_integration import SystemIntegration
from .exceptions import PlatformError


def main():
    """
    主入口函数
    Main entry function

    该函数是使用 python -m mac_info 时的入口点。
    它首先检查平台兼容性，然后创建CLI实例并运行应用程序。

    This function is the entry point when using python -m mac_info.
    It first checks platform compatibility, then creates a CLI instance and runs the application.

    退出码 / Exit Codes:
        0 - 成功 / Success
        1 - 一般错误 / General error
        2 - 平台不兼容 / Platform incompatibility
        3 - 权限被拒绝 / Permission denied
        4 - 缺少依赖 / Missing dependencies
    """
    # 首先检查平台兼容性
    # First check platform compatibility
    try:
        if not SystemIntegration.check_platform():
            print("=" * 80)
            print("错误 / Error: 平台不兼容 / Platform Incompatibility")
            print("=" * 80)
            print()
            print("mac-info 只能在 macOS 系统上运行。")
            print("mac-info can only run on macOS systems.")
            print()
            print("当前系统 / Current system:", sys.platform)
            print()
            print("请在 macOS 设备上运行此工具。")
            print("Please run this tool on a macOS device.")
            print("=" * 80)
            sys.exit(2)
    except Exception as e:
        print(f"错误 / Error: 平台检查失败 / Platform check failed: {e}")
        sys.exit(2)

    # 创建CLI实例并运行
    # Create CLI instance and run
    try:
        cli = MacInfoCLI()
        exit_code = cli.run()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        # 用户按 Ctrl+C 中断
        # User interrupted with Ctrl+C
        print("\n\n已中断 / Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"错误 / Error: 启动失败 / Startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
