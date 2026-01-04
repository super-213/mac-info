"""
显示格式化器模块
Display formatter module

该模块负责使用Rich库格式化和显示系统指标
This module is responsible for formatting and displaying system metrics using the Rich library
"""

from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from typing import Dict, List, Any


class DisplayFormatter:
    """
    显示格式化器类
    Display formatter class

    使用Rich库创建美观的终端输出
    Creates beautiful terminal output using the Rich library
    """

    def __init__(self):
        """
        初始化显示格式化器
        Initialize display formatter
        """
        self.console = Console()

    def format_bytes(self, bytes_value: int) -> str:
        """
        格式化字节数为人类可读格式
        Format bytes to human-readable format

        Args:
            bytes_value: 字节数 / Number of bytes

        Returns:
            格式化的字符串（例如："1.5 GB", "256 MB"）
            Formatted string (e.g., "1.5 GB", "256 MB")
        """
        if bytes_value < 0:
            return "0 B"

        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        unit_index = 0
        value = float(bytes_value)

        while value >= 1024.0 and unit_index < len(units) - 1:
            value /= 1024.0
            unit_index += 1

        if unit_index == 0:
            return f"{int(value)} {units[unit_index]}"
        else:
            return f"{value:.2f} {units[unit_index]}"

    def get_color_for_percentage(self, percent: float) -> str:
        """
        根据百分比返回颜色
        Return color based on percentage

        Args:
            percent: 百分比值（0-100）/ Percentage value (0-100)

        Returns:
            Rich格式化的颜色名称
            Color name for Rich formatting
        """
        if percent < 60:
            return "green"
        elif percent < 80:
            return "yellow"
        else:
            return "red"

    def create_cpu_panel(self, cpu_info: Dict[str, Any]) -> Table:
        """
        创建CPU信息面板
        Create CPU information panel

        Args:
            cpu_info: CPU信息字典 / CPU information dictionary

        Returns:
            Rich Table对象 / Rich Table object
        """
        table = Table(
            title="CPU 信息 / CPU Information",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("指标 / Metric", style="cyan", no_wrap=True)
        table.add_column("值 / Value", style="white")

        # 总体CPU使用率 / Overall CPU usage
        overall_percent = cpu_info.get("overall_percent", 0)
        color = self.get_color_for_percentage(overall_percent)
        table.add_row(
            "总体使用率 / Overall Usage", f"[{color}]{overall_percent:.1f}%[/{color}]"
        )

        # CPU核心数 / CPU core count
        cpu_count = cpu_info.get("count", 0)
        table.add_row("核心数 / Core Count", str(cpu_count))

        # 每核心使用率 / Per-core usage
        per_core = cpu_info.get("per_core_percent", [])
        if per_core:
            for i, core_percent in enumerate(per_core):
                color = self.get_color_for_percentage(core_percent)
                table.add_row(
                    f"核心 {i} / Core {i}", f"[{color}]{core_percent:.1f}%[/{color}]"
                )

        # CPU频率 / CPU frequency
        frequency = cpu_info.get("frequency", {})
        if frequency:
            current_freq = frequency.get("current", 0)
            if current_freq > 0:
                table.add_row("当前频率 / Current Frequency", f"{current_freq:.0f} MHz")

        return table

    def create_memory_panel(self, memory_info: Dict[str, Any]) -> Table:
        """
        创建内存信息面板
        Create memory information panel

        Args:
            memory_info: 内存信息字典 / Memory information dictionary

        Returns:
            Rich Table对象 / Rich Table object
        """
        table = Table(
            title="内存信息 / Memory Information",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("指标 / Metric", style="cyan", no_wrap=True)
        table.add_column("值 / Value", style="white")

        # 总内存 / Total memory
        total = memory_info.get("total", 0)
        table.add_row("总内存 / Total Memory", self.format_bytes(total))

        # 已使用内存 / Used memory
        used = memory_info.get("used", 0)
        percent = memory_info.get("percent", 0)
        color = self.get_color_for_percentage(percent)
        table.add_row(
            "已使用 / Used",
            f"[{color}]{self.format_bytes(used)} ({percent:.1f}%)[/{color}]",
        )

        # 可用内存 / Available memory
        available = memory_info.get("available", 0)
        table.add_row("可用 / Available", self.format_bytes(available))

        # 交换内存 / Swap memory
        swap_total = memory_info.get("swap_total", 0)
        swap_used = memory_info.get("swap_used", 0)
        if swap_total > 0:
            swap_percent = (swap_used / swap_total * 100) if swap_total > 0 else 0
            swap_color = self.get_color_for_percentage(swap_percent)
            table.add_row("交换内存总量 / Swap Total", self.format_bytes(swap_total))
            table.add_row(
                "交换内存已使用 / Swap Used",
                f"[{swap_color}]{self.format_bytes(swap_used)} ({swap_percent:.1f}%)[/{swap_color}]",
            )

        return table

    def create_process_table(self, processes: List[Dict[str, Any]]) -> Table:
        """
        创建进程信息表格
        Create process information table

        Args:
            processes: 进程字典列表 / List of process dictionaries

        Returns:
            Rich Table对象 / Rich Table object
        """
        table = Table(
            title="进程信息 / Process Information",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("PID", style="cyan", no_wrap=True)
        table.add_column("名称 / Name", style="white")
        table.add_column("CPU %", style="yellow", justify="right")
        table.add_column("内存 / Memory", style="green", justify="right")
        table.add_column("状态 / Status", style="blue")
        table.add_column("用户 / User", style="magenta")

        for proc in processes:
            pid = str(proc.get("pid", ""))
            name = proc.get("name", "N/A")
            cpu_percent = proc.get("cpu_percent", 0)
            memory_mb = proc.get("memory_mb", 0)
            status = proc.get("status", "unknown")
            username = proc.get("username", "N/A")

            # 限制名称长度 / Limit name length
            if len(name) > 30:
                name = name[:27] + "..."

            # CPU颜色编码 / CPU color coding
            cpu_color = self.get_color_for_percentage(cpu_percent)

            table.add_row(
                pid,
                name,
                f"[{cpu_color}]{cpu_percent:.1f}[/{cpu_color}]",
                f"{memory_mb:.1f} MB",
                status,
                username,
            )

        return table

    def create_temperature_panel(self, temp_info: Dict[str, Any]) -> Table:
        """
        创建温度信息面板
        Create temperature information panel

        Args:
            temp_info: 温度信息字典 / Temperature information dictionary

        Returns:
            Rich Table对象 / Rich Table object
        """
        table = Table(
            title="温度信息 / Temperature Information",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("传感器 / Sensor", style="cyan", no_wrap=True)
        table.add_column("温度 / Temperature", style="white")

        available = temp_info.get("available", False)

        if not available:
            table.add_row(
                "状态 / Status",
                "[yellow]温度监控不可用 / Temperature monitoring unavailable[/yellow]",
            )
            return table

        # CPU温度 / CPU temperature
        cpu_temp = temp_info.get("cpu_temp")
        if cpu_temp is not None:
            color = self._get_temperature_color(cpu_temp)
            table.add_row("CPU", f"[{color}]{cpu_temp:.1f}°C[/{color}]")

        # GPU温度 / GPU temperature
        gpu_temp = temp_info.get("gpu_temp")
        if gpu_temp is not None:
            color = self._get_temperature_color(gpu_temp)
            table.add_row("GPU", f"[{color}]{gpu_temp:.1f}°C[/{color}]")

        # 电池温度 / Battery temperature
        battery_temp = temp_info.get("battery_temp")
        if battery_temp is not None:
            color = self._get_temperature_color(battery_temp)
            table.add_row("电池 / Battery", f"[{color}]{battery_temp:.1f}°C[/{color}]")

        # 其他传感器 / Other sensors
        sensors = temp_info.get("sensors", {})
        for sensor_name, sensor_temp in sensors.items():
            if sensor_temp is not None:
                color = self._get_temperature_color(sensor_temp)
                table.add_row(sensor_name, f"[{color}]{sensor_temp:.1f}°C[/{color}]")

        return table

    def _get_temperature_color(self, temp: float) -> str:
        """
        根据温度返回颜色
        Return color based on temperature

        Args:
            temp: 温度（摄氏度）/ Temperature in Celsius

        Returns:
            颜色名称 / Color name
        """
        if temp < 60:
            return "green"
        elif temp < 80:
            return "yellow"
        else:
            return "red"

    def create_network_panel(self, network_info: Dict[str, Any]) -> Table:
        """
        创建网络信息面板
        Create network information panel

        Args:
            network_info: 网络信息字典 / Network information dictionary

        Returns:
            Rich Table对象 / Rich Table object
        """
        table = Table(
            title="网络信息 / Network Information",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("指标 / Metric", style="cyan", no_wrap=True)
        table.add_column("值 / Value", style="white")

        # 发送字节数 / Bytes sent
        bytes_sent = network_info.get("bytes_sent", 0)
        table.add_row("已发送 / Bytes Sent", self.format_bytes(bytes_sent))

        # 接收字节数 / Bytes received
        bytes_recv = network_info.get("bytes_recv", 0)
        table.add_row("已接收 / Bytes Received", self.format_bytes(bytes_recv))

        # 发送数据包数 / Packets sent
        packets_sent = network_info.get("packets_sent", 0)
        table.add_row("发送数据包 / Packets Sent", f"{packets_sent:,}")

        # 接收数据包数 / Packets received
        packets_recv = network_info.get("packets_recv", 0)
        table.add_row("接收数据包 / Packets Received", f"{packets_recv:,}")

        return table

    def create_dashboard(self, all_metrics: Dict[str, Any]) -> Layout:
        """
        创建完整的监控仪表板
        Create complete monitoring dashboard

        Args:
            all_metrics: 包含所有收集的指标的字典 / Dictionary containing all collected metrics

        Returns:
            Rich Layout对象 / Rich Layout object
        """
        # 创建布局 / Create layout
        layout = Layout()

        # 分割布局为上下两部分 / Split layout into top and bottom
        layout.split_column(Layout(name="top", ratio=2), Layout(name="bottom", ratio=3))

        # 上半部分分为左右两列 / Split top into left and right columns
        layout["top"].split_row(
            Layout(name="cpu", ratio=1), Layout(name="memory", ratio=1)
        )

        # 下半部分分为三列 / Split bottom into three columns
        layout["bottom"].split_row(
            Layout(name="processes", ratio=2), Layout(name="right_column", ratio=1)
        )

        # 右列分为上下两部分 / Split right column into top and bottom
        layout["right_column"].split_column(
            Layout(name="temperature", ratio=1), Layout(name="network", ratio=1)
        )

        # 填充各个面板 / Fill each panel
        cpu_info = all_metrics.get("cpu", {})
        memory_info = all_metrics.get("memory", {})
        processes = all_metrics.get("processes", [])
        temp_info = all_metrics.get("temperature", {})
        network_info = all_metrics.get("network", {})

        layout["cpu"].update(
            Panel(self.create_cpu_panel(cpu_info), border_style="blue")
        )
        layout["memory"].update(
            Panel(self.create_memory_panel(memory_info), border_style="green")
        )
        layout["processes"].update(
            Panel(self.create_process_table(processes), border_style="yellow")
        )
        layout["temperature"].update(
            Panel(self.create_temperature_panel(temp_info), border_style="red")
        )
        layout["network"].update(
            Panel(self.create_network_panel(network_info), border_style="cyan")
        )

        return layout
