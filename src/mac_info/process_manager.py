"""
进程管理器模块
Process Manager Module

该模块负责管理和检索进程信息，包括进程列表、排序和单个进程查询。
This module is responsible for managing and retrieving process information, including process listing, sorting, and individual process lookup.
"""

import psutil
from typing import Dict, List, Any, Optional


class ProcessManager:
    """
    进程管理器类，用于管理和检索进程信息
    Process manager class for managing and retrieving process information
    """

    def __init__(self):
        """
        初始化进程管理器
        Initialize process manager
        """
        pass

    def get_processes(
        self, sort_by: str = "cpu", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        获取进程列表
        Get list of processes

        收集系统中运行的进程信息，支持按不同标准排序和限制返回数量
        Collects information about running processes in the system, with support for sorting by different criteria and limiting the number of results

        Args:
            sort_by: 排序标准 / Sort criterion ('cpu', 'memory', 'pid', 'name')
            limit: 返回的最大进程数 / Maximum number of processes to return

        Returns:
            进程字典列表，每个字典包含：
            List of process dictionaries, each containing:
            {
                'pid': int,              # 进程ID / Process ID
                'name': str,             # 进程名称 / Process name
                'cpu_percent': float,    # CPU使用率 / CPU usage percentage
                'memory_percent': float, # 内存使用率 / Memory usage percentage
                'memory_mb': float,      # 内存使用量(MB) / Memory usage in MB
                'status': str,           # 进程状态 / Process status
                'username': str,         # 进程所有者 / Process owner
                'cmdline': str           # 启动命令 / Command line
            }
        """
        processes = []

        # 遍历所有进程
        # Iterate through all processes
        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "cpu_percent",
                "memory_percent",
                "memory_info",
                "status",
                "username",
                "cmdline",
            ]
        ):
            try:
                # 获取进程信息
                # Get process information
                pinfo = proc.info

                # 计算内存使用量（MB）
                # Calculate memory usage in MB
                memory_mb = 0.0
                if pinfo["memory_info"] is not None:
                    memory_mb = pinfo["memory_info"].rss / (1024 * 1024)

                # 获取命令行，如果为空列表则使用进程名
                # Get command line, use process name if empty list
                cmdline = (
                    " ".join(pinfo["cmdline"]) if pinfo["cmdline"] else pinfo["name"]
                )

                # 构建进程信息字典
                # Build process information dictionary
                process_dict = {
                    "pid": pinfo["pid"],
                    "name": pinfo["name"] or "N/A",
                    "cpu_percent": pinfo["cpu_percent"] or 0.0,
                    "memory_percent": pinfo["memory_percent"] or 0.0,
                    "memory_mb": memory_mb,
                    "status": pinfo["status"] or "unknown",
                    "username": pinfo["username"] or "N/A",
                    "cmdline": cmdline or "N/A",
                }

                processes.append(process_dict)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # 优雅地处理进程访问错误
                # Gracefully handle process access errors
                # 进程可能在迭代过程中终止，或者没有访问权限
                # Process may have terminated during iteration, or we don't have access permissions
                continue

        # 根据指定标准排序
        # Sort by specified criterion
        sort_key_map = {
            "cpu": lambda p: p["cpu_percent"],
            "memory": lambda p: p["memory_percent"],
            "pid": lambda p: p["pid"],
            "name": lambda p: p["name"].lower(),
        }

        # 如果排序标准有效，则进行排序（CPU和内存按降序，PID和名称按升序）
        # If sort criterion is valid, perform sorting (CPU and memory descending, PID and name ascending)
        if sort_by in sort_key_map:
            reverse = sort_by in ["cpu", "memory"]
            processes.sort(key=sort_key_map[sort_by], reverse=reverse)

        # 限制返回的进程数量
        # Limit the number of processes returned
        return processes[:limit]

    def get_process_by_pid(self, pid: int) -> Optional[Dict[str, Any]]:
        """
        根据PID获取进程信息
        Get process information by PID

        查询指定PID的进程详细信息
        Queries detailed information for a process with the specified PID

        Args:
            pid: 进程ID / Process ID

        Returns:
            进程字典或None（如果未找到）：
            Process dictionary or None if not found:
            {
                'pid': int,              # 进程ID / Process ID
                'name': str,             # 进程名称 / Process name
                'cpu_percent': float,    # CPU使用率 / CPU usage percentage
                'memory_percent': float, # 内存使用率 / Memory usage percentage
                'memory_mb': float,      # 内存使用量(MB) / Memory usage in MB
                'status': str,           # 进程状态 / Process status
                'username': str,         # 进程所有者 / Process owner
                'cmdline': str           # 启动命令 / Command line
            }
        """
        try:
            # 创建进程对象
            # Create process object
            proc = psutil.Process(pid)

            # 获取进程信息
            # Get process information
            pinfo = proc.as_dict(
                attrs=[
                    "pid",
                    "name",
                    "cpu_percent",
                    "memory_percent",
                    "memory_info",
                    "status",
                    "username",
                    "cmdline",
                ]
            )

            # 计算内存使用量（MB）
            # Calculate memory usage in MB
            memory_mb = 0.0
            if pinfo["memory_info"] is not None:
                memory_mb = pinfo["memory_info"].rss / (1024 * 1024)

            # 获取命令行，如果为空列表则使用进程名
            # Get command line, use process name if empty list
            cmdline = " ".join(pinfo["cmdline"]) if pinfo["cmdline"] else pinfo["name"]

            # 构建进程信息字典
            # Build process information dictionary
            return {
                "pid": pinfo["pid"],
                "name": pinfo["name"] or "N/A",
                "cpu_percent": pinfo["cpu_percent"] or 0.0,
                "memory_percent": pinfo["memory_percent"] or 0.0,
                "memory_mb": memory_mb,
                "status": pinfo["status"] or "unknown",
                "username": pinfo["username"] or "N/A",
                "cmdline": cmdline or "N/A",
            }

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 优雅地处理进程访问错误
            # Gracefully handle process access errors
            # 进程不存在、没有访问权限或是僵尸进程
            # Process doesn't exist, we don't have access permissions, or it's a zombie process
            return None
