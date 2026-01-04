# mac-info-tool

[English](#english) | [中文](#中文)

---

## English

### Overview

mac-info-tool is a macOS terminal monitoring tool that displays real-time system performance metrics in a clean, visually appealing interface. It provides comprehensive system information including CPU usage, memory consumption, process details, disk I/O, network statistics, and temperature monitoring.

### Features

- **Real-time System Monitoring**: View CPU, memory, disk I/O, and network statistics
- **Process Management**: Display detailed information about running processes
- **Temperature Monitoring**: Monitor CPU and system temperatures (requires additional tools)
- **Beautiful Terminal UI**: Clean, color-coded output using the Rich library
- **Command-Line Interface**: Easy-to-use CLI with help and list commands
- **Top Integration**: Direct access to macOS top command

### Requirements

- macOS (10.14 or later recommended)
- Python 3.8 or higher
- Optional: `osx-cpu-temp` for temperature monitoring (install via Homebrew)

### Installation

#### 1. Clone the repository

```bash
git clone <repository-url>
cd mac-info-tool
```

#### 2. Set up virtual environment

Run the automated setup script:

```bash
./setup_venv.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Install the package

```bash
pip install -e .
```

### Usage

#### Activate virtual environment

```bash
source venv/bin/activate
```

#### Basic commands

```bash
# Display help information
mac-info help

# List all available commands
mac-info list

# Start monitoring (default view)
mac-info

# Start interactive monitoring mode
mac-info monitor

# Set custom refresh interval (in seconds)
mac-info --refresh 5

# Invoke system top command
mac-info top
```


### Output Examples

#### Monitor Command Output

```
┌─────────────────────────────────────────────────────────────────┐
│                         CPU Information                          │
├─────────────────────────────────────────────────────────────────┤
│ Overall Usage:  45.2%                                           │
│ Core 0:         52.1%  Core 1:  38.4%                          │
│ Core 2:         47.8%  Core 3:  42.6%                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       Memory Information                         │
├─────────────────────────────────────────────────────────────────┤
│ Total:      16.0 GB                                             │
│ Used:       10.2 GB (63.8%)                                     │
│ Available:   5.8 GB                                             │
│ Swap Used:   0.5 GB                                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Top Processes (by CPU)                      │
├──────┬─────────────────┬──────────┬──────────┬─────────────────┤
│ PID  │ Name            │ CPU %    │ Memory   │ User            │
├──────┼─────────────────┼──────────┼──────────┼─────────────────┤
│ 1234 │ Chrome          │ 25.3%    │ 1.2 GB   │ user            │
│ 5678 │ Python          │ 15.7%    │ 512 MB   │ user            │
│ 9012 │ Terminal        │  8.2%    │ 256 MB   │ user            │
└──────┴─────────────────┴──────────┴──────────┴─────────────────┘
```

### Temperature Monitoring

For temperature monitoring, install `osx-cpu-temp`:

```bash
brew install osx-cpu-temp
```

Without this tool, temperature information will show as unavailable.

### Troubleshooting

#### Issue: "Platform not supported" error

**Solution**: This tool only works on macOS. Ensure you're running on a Mac system.

```bash
# Check your system
uname -s
# Should output: Darwin
```

#### Issue: Temperature information shows "N/A"

**Solution**: Install the temperature monitoring tool:

```bash
# Install via Homebrew
brew install osx-cpu-temp

# Verify installation
osx-cpu-temp
```

**Alternative**: Use powermetrics (requires sudo):

```bash
sudo powermetrics --samplers smc -n 1
```

#### Issue: "Permission denied" errors

**Solution**: Some system metrics require elevated permissions. Try:

```bash
# For temperature monitoring with powermetrics
sudo mac-info monitor
```

#### Issue: Virtual environment activation fails

**Solution**: Ensure Python 3.8+ is installed:

```bash
# Check Python version
python3 --version

# If needed, install Python via Homebrew
brew install python@3.11
```

#### Issue: Module not found errors

**Solution**: Reinstall dependencies:

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

#### Issue: Display formatting looks broken

**Solution**: Ensure your terminal supports Unicode and colors:

```bash
# Check terminal type
echo $TERM

# Try setting a compatible terminal
export TERM=xterm-256color
```

#### Issue: High CPU usage from mac-info itself

**Solution**: Increase the refresh interval:

```bash
# Use a longer refresh interval (e.g., 5 seconds)
mac-info --refresh 5
```

### Development

#### Running tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=mac_info --cov-report=html

# Run property-based tests
pytest -v -k property
```

#### Project Structure

```
mac-info-tool/
├── src/
│   └── mac_info/
│       ├── __init__.py
│       ├── cli.py                  # CLI interface
│       ├── metrics_collector.py    # System metrics collection
│       ├── process_manager.py      # Process management
│       ├── temperature_monitor.py  # Temperature monitoring
│       ├── display_formatter.py    # Output formatting
│       ├── system_integration.py   # System command integration
│       ├── models.py                # Data models
│       └── exceptions.py            # Custom exceptions
├── tests/
│   ├── test_cli.py
│   ├── test_metrics_collector.py
│   ├── test_process_manager.py
│   └── ...
├── docs/
├── requirements.txt
├── pyproject.toml
├── setup_venv.sh
└── README.md
```

### Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## 中文

### 概述

mac-info-tool 是一个 macOS 终端监控工具，以清晰美观的界面显示实时系统性能指标。它提供全面的系统信息，包括 CPU 使用率、内存消耗、进程详情、磁盘 I/O、网络统计和温度监控。

### 功能特性

- **实时系统监控**：查看 CPU、内存、磁盘 I/O 和网络统计信息
- **进程管理**：显示运行中进程的详细信息
- **温度监控**：监控 CPU 和系统温度（需要额外工具）
- **美观的终端界面**：使用 Rich 库实现清晰、彩色编码的输出
- **命令行界面**：易于使用的 CLI，支持 help 和 list 命令
- **Top 集成**：直接访问 macOS top 命令

### 系统要求

- macOS（推荐 10.14 或更高版本）
- Python 3.8 或更高版本
- 可选：`osx-cpu-temp` 用于温度监控（通过 Homebrew 安装）

### 安装

#### 1. 克隆仓库

```bash
git clone <repository-url>
cd mac-info-tool
```

#### 2. 设置虚拟环境

运行自动化设置脚本：

```bash
./setup_venv.sh
```

或手动设置：

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. 安装包

```bash
pip install -e .
```

### 使用方法

#### 激活虚拟环境

```bash
source venv/bin/activate
```

#### 基本命令

```bash
# 显示帮助信息
mac-info help

# 列出所有可用命令
mac-info list

# 开始监控（默认视图）
mac-info

# 启动交互式监控模式
mac-info monitor

# 设置自定义刷新间隔（秒）
mac-info --refresh 5

# 调用系统 top 命令
mac-info top
```

### 输出示例

#### 监控命令输出

```
┌─────────────────────────────────────────────────────────────────┐
│                         CPU 信息                                 │
├─────────────────────────────────────────────────────────────────┤
│ 总体使用率:  45.2%                                               │
│ 核心 0:      52.1%  核心 1:  38.4%                              │
│ 核心 2:      47.8%  核心 3:  42.6%                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       内存信息                                   │
├─────────────────────────────────────────────────────────────────┤
│ 总计:       16.0 GB                                             │
│ 已使用:     10.2 GB (63.8%)                                     │
│ 可用:        5.8 GB                                             │
│ 交换已使用:  0.5 GB                                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    热门进程（按 CPU 排序）                        │
├──────┬─────────────────┬──────────┬──────────┬─────────────────┤
│ PID  │ 名称            │ CPU %    │ 内存     │ 用户            │
├──────┼─────────────────┼──────────┼──────────┼─────────────────┤
│ 1234 │ Chrome          │ 25.3%    │ 1.2 GB   │ user            │
│ 5678 │ Python          │ 15.7%    │ 512 MB   │ user            │
│ 9012 │ Terminal        │  8.2%    │ 256 MB   │ user            │
└──────┴─────────────────┴──────────┴──────────┴─────────────────┘
```

### 温度监控

要使用温度监控功能，请安装 `osx-cpu-temp`：

```bash
brew install osx-cpu-temp
```

如果没有此工具，温度信息将显示为不可用。

### 故障排除

#### 问题："平台不支持"错误

**解决方案**：此工具仅适用于 macOS。请确保您在 Mac 系统上运行。

```bash
# 检查您的系统
uname -s
# 应该输出：Darwin
```

#### 问题：温度信息显示"N/A"

**解决方案**：安装温度监控工具：

```bash
# 通过 Homebrew 安装
brew install osx-cpu-temp

# 验证安装
osx-cpu-temp
```

**替代方案**：使用 powermetrics（需要 sudo）：

```bash
sudo powermetrics --samplers smc -n 1
```

#### 问题："权限被拒绝"错误

**解决方案**：某些系统指标需要提升的权限。尝试：

```bash
# 使用 powermetrics 进行温度监控
sudo mac-info monitor
```

#### 问题：虚拟环境激活失败

**解决方案**：确保已安装 Python 3.8+：

```bash
# 检查 Python 版本
python3 --version

# 如果需要，通过 Homebrew 安装 Python
brew install python@3.11
```

#### 问题：找不到模块错误

**解决方案**：重新安装依赖项：

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

#### 问题：显示格式看起来损坏

**解决方案**：确保您的终端支持 Unicode 和颜色：

```bash
# 检查终端类型
echo $TERM

# 尝试设置兼容的终端
export TERM=xterm-256color
```

#### 问题：mac-info 本身的 CPU 使用率很高

**解决方案**：增加刷新间隔：

```bash
# 使用更长的刷新间隔（例如 5 秒）
mac-info --refresh 5
```

### 开发

#### 运行测试

```bash
# 运行所有测试
pytest

# 运行并生成覆盖率报告
pytest --cov=mac_info --cov-report=html

# 运行基于属性的测试
pytest -v -k property
```

#### 项目结构

```
mac-info-tool/
├── src/
│   └── mac_info/
│       ├── __init__.py
│       ├── cli.py                  # CLI 接口
│       ├── metrics_collector.py    # 系统指标收集
│       ├── process_manager.py      # 进程管理
│       ├── temperature_monitor.py  # 温度监控
│       ├── display_formatter.py    # 输出格式化
│       ├── system_integration.py   # 系统命令集成
│       ├── models.py                # 数据模型
│       └── exceptions.py            # 自定义异常
├── tests/
│   ├── test_cli.py
│   ├── test_metrics_collector.py
│   ├── test_process_manager.py
│   └── ...
├── docs/
├── requirements.txt
├── pyproject.toml
├── setup_venv.sh
└── README.md
```

### 贡献

欢迎贡献！请随时提交问题或拉取请求。
