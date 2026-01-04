"""
命令行接口模块
Command Line Interface Module

该模块提供mac-info工具的命令行接口，包括参数解析、命令路由和用户交互。
This module provides the command-line interface for the mac-info tool, including argument parsing, command routing, and user interaction.
"""

import argparse
import sys
from typing import Optional, List
import logging

from .metrics_collector import MetricsCollector
from .process_manager import ProcessManager
from .temperature_monitor import TemperatureMonitor
from .display_formatter import DisplayFormatter
from .system_integration import SystemIntegration
from .exceptions import PlatformError, MetricsCollectionError

# 配置日志记录器
# Configure logger
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MacInfoCLI:
    """
    命令行接口类
    Command Line Interface Class

    该类负责处理命令行参数解析、命令路由和用户交互。
    This class handles command-line argument parsing, command routing, and user interaction.
    """

    def __init__(self):
        """
        初始化CLI接口
        Initialize CLI interface
        """
        self.metrics_collector = MetricsCollector()
        self.process_manager = ProcessManager()
        self.temperature_monitor = TemperatureMonitor()
        self.display_formatter = DisplayFormatter()

    def parse_arguments(self) -> argparse.Namespace:
        """
        解析命令行参数
        Parse command-line arguments

        创建参数解析器并解析用户提供的命令行参数。
        支持的命令包括：help, list, top, monitor

        Creates argument parser and parses command-line arguments provided by the user.
        Supported commands include: help, list, top, monitor

        Returns:
            argparse.Namespace: 解析后的参数命名空间 / Parsed arguments namespace

        Example:
            >>> cli = MacInfoCLI()
            >>> args = cli.parse_arguments()
            >>> print(args.command)
        """
        parser = argparse.ArgumentParser(
            prog="mac-info",
            description="macOS系统监控工具 / macOS System Monitoring Tool",
            add_help=False,  # 我们将自定义help命令 / We will customize the help command
        )

        # 添加命令参数（位置参数）
        # Add command argument (positional argument)
        parser.add_argument(
            "command",
            nargs="?",  # 可选参数 / Optional argument
            default="monitor",  # 默认命令 / Default command
            help="要执行的命令 / Command to execute (help, list, top, monitor)",
        )

        # 添加刷新间隔选项
        # Add refresh interval option
        parser.add_argument(
            "--refresh",
            type=int,
            default=2,
            metavar="N",
            help="监控模式的刷新间隔（秒）/ Refresh interval for monitor mode (seconds)",
        )

        # 添加进程数量限制选项
        # Add process limit option
        parser.add_argument(
            "--limit",
            type=int,
            default=10,
            metavar="N",
            help="显示的进程数量 / Number of processes to display",
        )

        # 添加进程排序选项
        # Add process sorting option
        parser.add_argument(
            "--sort",
            type=str,
            default="cpu",
            choices=["cpu", "memory", "pid", "name"],
            help="进程排序方式 / Process sorting method",
        )

        # 解析已知参数，允许传递额外参数给top命令
        # Parse known arguments, allowing extra arguments to be passed to top command
        args, unknown = parser.parse_known_args()

        # 将未知参数存储为top_args
        # Store unknown arguments as top_args
        args.top_args = unknown

        return args

    def show_help(self) -> None:
        """
        显示帮助信息
        Display help information

        显示详细的帮助文本，包括所有可用命令、选项和使用示例。
        帮助信息以中英文双语形式呈现。

        Displays detailed help text including all available commands, options, and usage examples.
        Help information is presented in both Chinese and English.

        Example:
            >>> cli = MacInfoCLI()
            >>> cli.show_help()
        """
        help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          mac-info 帮助 / Help                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

名称 / NAME:
    mac-info - macOS系统监控工具 / macOS System Monitoring Tool

用法 / USAGE:
    mac-info [command] [options]

命令 / COMMANDS:
    help                显示此帮助信息
                        Display this help information
    
    list                列出所有可用命令
                        List all available commands
    
    monitor             启动实时监控模式（默认）
                        Start real-time monitoring mode (default)
    
    top [args]          调用系统top命令
                        Invoke system top command
                        可以传递额外参数给top命令
                        Additional arguments can be passed to top

选项 / OPTIONS:
    --refresh N         设置监控刷新间隔（秒），默认为2秒
                        Set monitoring refresh interval (seconds), default is 2
    
    --limit N           设置显示的进程数量，默认为10
                        Set number of processes to display, default is 10
    
    --sort METHOD       设置进程排序方式：cpu, memory, pid, name
                        Set process sorting method: cpu, memory, pid, name
                        默认按CPU使用率排序
                        Default is sorted by CPU usage

示例 / EXAMPLES:
    # 启动默认监控模式
    # Start default monitoring mode
    mac-info
    
    # 显示帮助信息
    # Display help information
    mac-info help
    
    # 列出所有命令
    # List all commands
    mac-info list
    
    # 设置5秒刷新间隔
    # Set 5 second refresh interval
    mac-info monitor --refresh 5
    
    # 显示前20个进程，按内存排序
    # Display top 20 processes, sorted by memory
    mac-info monitor --limit 20 --sort memory
    
    # 调用系统top命令
    # Invoke system top command
    mac-info top
    
    # 调用top命令并传递参数
    # Invoke top with arguments
    mac-info top -l 1

说明 / NOTES:
    - 此工具仅支持macOS系统
      This tool only supports macOS
    
    - 温度监控需要安装osx-cpu-temp或使用powermetrics
      Temperature monitoring requires osx-cpu-temp or powermetrics
    
    - 某些功能可能需要管理员权限
      Some features may require administrator privileges

更多信息 / MORE INFORMATION:
    访问项目主页获取更多信息和文档
    Visit the project homepage for more information and documentation
"""
        print(help_text)

    def show_list(self) -> None:
        """
        显示可用命令列表
        Display list of available commands

        显示所有可用命令的简洁列表，包括每个命令的简短描述。
        列表以中英文双语形式呈现。

        Displays a concise list of all available commands with brief descriptions.
        The list is presented in both Chinese and English.

        Example:
            >>> cli = MacInfoCLI()
            >>> cli.show_list()
        """
        list_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    mac-info 可用命令 / Available Commands                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

命令列表 / Command List:

  help          显示详细帮助信息
                Display detailed help information

  list          显示此命令列表
                Display this command list

  monitor       启动实时系统监控（默认命令）
                Start real-time system monitoring (default command)
                - 显示CPU、内存、进程、温度和网络信息
                - Displays CPU, memory, process, temperature, and network info

  top           调用系统top命令
                Invoke system top command
                - 可以传递额外参数
                - Additional arguments can be passed

提示 / TIP:
  使用 'mac-info help' 查看详细的使用说明和示例
  Use 'mac-info help' to see detailed usage instructions and examples
"""
        print(list_text)

    def _collect_all_metrics(self) -> dict:
        """
        收集所有系统指标
        Collect all system metrics

        从各个收集器获取所有系统指标数据。
        Gathers all system metrics data from various collectors.

        Returns:
            dict: 包含所有指标的字典 / Dictionary containing all metrics
        """
        return {
            "cpu": self.metrics_collector.get_cpu_info(),
            "memory": self.metrics_collector.get_memory_info(),
            "disk_io": self.metrics_collector.get_disk_io_info(),
            "network": self.metrics_collector.get_network_info(),
            "temperature": self.temperature_monitor.get_all_temperatures(),
            "processes": self.process_manager.get_processes(sort_by="cpu", limit=10),
        }

    def _show_default_usage(self) -> None:
        """
        显示默认使用提示
        Display default usage hint

        当用户不带参数运行mac-info时显示简短的使用提示。
        Displays a brief usage hint when user runs mac-info without arguments.
        """
        usage_text = """
mac-info: macOS系统监控工具 / macOS System Monitoring Tool

使用方法 / Usage:
    mac-info [command] [options]

常用命令 / Common Commands:
    mac-info help       显示详细帮助 / Display detailed help
    mac-info list       列出所有命令 / List all commands
    mac-info monitor    启动监控模式 / Start monitoring mode
    mac-info top        调用top命令 / Invoke top command

提示：使用 'mac-info help' 查看完整帮助信息
Tip: Use 'mac-info help' to see full help information
"""
        print(usage_text)

    def run(self) -> int:
        """
        运行CLI应用程序
        Run the CLI application

        这是CLI的主入口点，负责：
        1. 检查平台兼容性
        2. 解析命令行参数
        3. 路由到适当的命令处理器
        4. 处理错误并返回适当的退出码

        This is the main entry point for the CLI, responsible for:
        1. Checking platform compatibility
        2. Parsing command-line arguments
        3. Routing to appropriate command handlers
        4. Handling errors and returning appropriate exit codes

        Returns:
            int: 退出码 / Exit code
                 0 - 成功 / Success
                 1 - 一般错误 / General error
                 2 - 平台不兼容 / Platform incompatibility
                 3 - 权限被拒绝 / Permission denied
                 4 - 缺少依赖 / Missing dependencies

        Example:
            >>> cli = MacInfoCLI()
            >>> exit_code = cli.run()
            >>> sys.exit(exit_code)
        """
        # 首先检查平台兼容性
        # First check platform compatibility
        try:
            if not SystemIntegration.check_platform():
                raise PlatformError()
        except PlatformError as e:
            logger.error(f"平台错误 / Platform error: {e}")
            print(f"错误 / Error: {e.message}")
            print("\n提示 / Tip: mac-info只能在macOS系统上运行")
            print("Tip: mac-info can only run on macOS")
            return 2

        try:
            # 解析命令行参数
            # Parse command-line arguments
            args = self.parse_arguments()
            command = args.command.lower() if args.command else "monitor"

            # 路由到相应的命令处理器
            # Route to appropriate command handler
            if command == "help":
                self.show_help()
                return 0

            elif command == "list":
                self.show_list()
                return 0

            elif command == "top":
                # 调用系统top命令，传递额外参数
                # Invoke system top command with additional arguments
                try:
                    exit_code = SystemIntegration.invoke_top(args.top_args)
                    return exit_code
                except FileNotFoundError:
                    logger.error("top命令不可用 / top command not available")
                    print("错误 / Error: top命令不可用")
                    print("Error: top command not available")
                    return 4
                except Exception as e:
                    logger.error(
                        f"执行top命令失败 / Failed to execute top command: {e}"
                    )
                    print(f"错误 / Error: 执行top命令时出错: {e}")
                    print(f"Error: Failed to execute top command: {e}")
                    return 1

            elif command == "monitor":
                # 启动监控模式
                # Start monitoring mode
                return self._run_monitor_mode(args)

            else:
                # 无效命令
                # Invalid command
                logger.warning(f"未知命令 / Unknown command: {command}")
                print(f"错误 / Error: 未知命令 '{command}'")
                print(f"Error: Unknown command '{command}'")
                print("\n提示：使用 'mac-info help' 查看可用命令")
                print("Tip: Use 'mac-info help' to see available commands")
                return 1

        except KeyboardInterrupt:
            # 用户按Ctrl+C中断
            # User interrupted with Ctrl+C
            print("\n\n已中断 / Interrupted")
            logger.info("用户中断程序 / User interrupted program")
            return 0

        except MetricsCollectionError as e:
            # 指标收集错误
            # Metrics collection error
            logger.error(f"指标收集错误 / Metrics collection error: {e}")
            print(f"错误 / Error: {e.message}")
            print("\n提示 / Tip: 某些系统指标可能不可用")
            print("Tip: Some system metrics may be unavailable")
            return 1

        except Exception as e:
            # 捕获所有其他异常
            # Catch all other exceptions
            logger.exception(f"意外错误 / Unexpected error: {e}")
            print(f"错误 / Error: 发生意外错误: {e}")
            print(f"Error: An unexpected error occurred: {e}")
            print("\n提示 / Tip: 请检查日志以获取更多信息")
            print("Tip: Please check logs for more information")
            return 1

    def _run_monitor_mode(self, args: argparse.Namespace) -> int:
        """
        运行监控模式
        Run monitoring mode

        显示系统监控仪表板，包括CPU、内存、进程、温度和网络信息。
        使用Rich Live显示实现自动刷新功能。

        Displays system monitoring dashboard including CPU, memory, processes, temperature, and network info.
        Uses Rich Live display for auto-refresh functionality.

        Args:
            args: 解析后的命令行参数 / Parsed command-line arguments

        Returns:
            int: 退出码 / Exit code (0 for success)
        """
        from rich.live import Live
        import time

        try:
            # 显示启动信息
            # Display startup information
            print("正在启动监控模式... / Starting monitoring mode...")
            print(f"刷新间隔 / Refresh interval: {args.refresh} 秒 / seconds")
            print(f"进程数量 / Process count: {args.limit}")
            print(f"排序方式 / Sort by: {args.sort}")
            print("按 Ctrl+C 退出 / Press Ctrl+C to exit\n")

            # 使用Rich Live显示实现自动刷新
            # Use Rich Live display for auto-refresh
            with Live(
                self._generate_dashboard(args),
                console=self.display_formatter.console,
                refresh_per_second=1.0
                / args.refresh,  # 根据刷新间隔计算刷新率 / Calculate refresh rate based on interval
                screen=False,  # 不使用全屏模式，允许滚动 / Don't use full screen mode, allow scrolling
            ) as live:
                try:
                    while True:
                        # 等待刷新间隔
                        # Wait for refresh interval
                        time.sleep(args.refresh)

                        # 更新显示
                        # Update display
                        live.update(self._generate_dashboard(args))

                except KeyboardInterrupt:
                    # 用户按 Ctrl+C 中断
                    # User interrupted with Ctrl+C
                    pass

            # 显示退出信息
            # Display exit information
            print("\n监控已停止 / Monitoring stopped")
            return 0

        except KeyboardInterrupt:
            # 处理启动阶段的中断
            # Handle interruption during startup
            print("\n\n已中断 / Interrupted")
            return 0

        except Exception as e:
            logger.exception(f"监控模式运行失败 / Monitor mode failed: {e}")
            print(f"错误 / Error: 收集指标时出错: {e}")
            print(f"Error: Failed to collect metrics: {e}")
            return 1

    def _generate_dashboard(self, args: argparse.Namespace):
        """
        生成监控仪表板
        Generate monitoring dashboard

        收集所有系统指标并创建仪表板布局。
        该方法被Live显示循环调用以更新显示内容。

        Collects all system metrics and creates dashboard layout.
        This method is called by Live display loop to update the display content.

        Args:
            args: 解析后的命令行参数 / Parsed command-line arguments

        Returns:
            Rich Layout对象 / Rich Layout object
        """
        # 使用用户指定的参数收集进程信息
        # Collect process information using user-specified parameters
        try:
            processes = self.process_manager.get_processes(
                sort_by=args.sort, limit=args.limit
            )
        except Exception as e:
            logger.error(
                f"收集进程信息失败 / Failed to collect process information: {e}"
            )
            processes = []

        # 收集其他指标（使用优雅降级）
        # Collect other metrics (with graceful degradation)
        all_metrics = {}

        try:
            all_metrics["cpu"] = self.metrics_collector.get_cpu_info()
        except MetricsCollectionError as e:
            logger.error(f"CPU指标收集失败 / CPU metrics collection failed: {e}")
            all_metrics["cpu"] = None

        try:
            all_metrics["memory"] = self.metrics_collector.get_memory_info()
        except MetricsCollectionError as e:
            logger.error(f"内存指标收集失败 / Memory metrics collection failed: {e}")
            all_metrics["memory"] = None

        try:
            all_metrics["disk_io"] = self.metrics_collector.get_disk_io_info()
        except Exception as e:
            logger.error(
                f"磁盘I/O指标收集失败 / Disk I/O metrics collection failed: {e}"
            )
            all_metrics["disk_io"] = None

        try:
            all_metrics["network"] = self.metrics_collector.get_network_info()
        except Exception as e:
            logger.error(f"网络指标收集失败 / Network metrics collection failed: {e}")
            all_metrics["network"] = None

        try:
            all_metrics["temperature"] = self.temperature_monitor.get_all_temperatures()
        except Exception as e:
            logger.error(
                f"温度信息收集失败 / Temperature information collection failed: {e}"
            )
            all_metrics["temperature"] = {"available": False}

        all_metrics["processes"] = processes

        # 创建并返回仪表板
        # Create and return dashboard
        try:
            return self.display_formatter.create_dashboard(all_metrics)
        except Exception as e:
            logger.error(f"创建仪表板失败 / Failed to create dashboard: {e}")
            # 返回错误信息面板
            # Return error information panel
            from rich.panel import Panel

            return Panel(
                f"错误 / Error: 无法创建仪表板\nUnable to create dashboard\n\n{str(e)}",
                title="错误 / Error",
                border_style="red",
            )


def main():
    """
    主入口函数
    Main entry function

    创建CLI实例并运行应用程序。
    Creates CLI instance and runs the application.
    """
    cli = MacInfoCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
