#!/bin/bash

# ============================================================================
# mac-info-tool 虚拟环境设置脚本
# Virtual environment setup script for mac-info-tool
#
# 此脚本将：
# This script will:
# 1. 检查 Python 版本 / Check Python version
# 2. 创建虚拟环境 / Create virtual environment
# 3. 安装依赖项 / Install dependencies
# 4. 安装 mac-info-tool 包 / Install mac-info-tool package
# ============================================================================

set -e  # 遇到错误时退出 / Exit on error

# 颜色定义 / Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息 / Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在 macOS 上运行 / Check if running on macOS
print_info "检查操作系统... / Checking operating system..."
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "此工具仅支持 macOS / This tool only supports macOS"
    exit 2
fi
print_success "运行在 macOS 上 / Running on macOS"

# 检查 Python 版本 / Check Python version
print_info "检查 Python 版本... / Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "未找到 Python 3 / Python 3 not found"
    print_info "请安装 Python 3.8 或更高版本 / Please install Python 3.8 or higher"
    print_info "推荐使用 Homebrew 安装: / Recommended installation via Homebrew:"
    echo "  brew install python@3.11"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

print_info "找到 Python 版本: $PYTHON_VERSION / Found Python version: $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "需要 Python 3.8 或更高版本 / Python 3.8 or higher required"
    print_info "当前版本: $PYTHON_VERSION / Current version: $PYTHON_VERSION"
    exit 1
fi
print_success "Python 版本符合要求 / Python version meets requirements"

# 检查虚拟环境是否已存在 / Check if virtual environment already exists
if [ -d "venv" ]; then
    print_warning "虚拟环境已存在 / Virtual environment already exists"
    read -p "是否删除并重新创建? (y/N) / Delete and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "删除现有虚拟环境... / Removing existing virtual environment..."
        rm -rf venv
    else
        print_info "使用现有虚拟环境 / Using existing virtual environment"
    fi
fi

# 创建虚拟环境 / Create virtual environment
if [ ! -d "venv" ]; then
    print_info "正在创建虚拟环境... / Creating virtual environment..."
    python3 -m venv venv
    print_success "虚拟环境创建成功 / Virtual environment created successfully"
fi

# 激活虚拟环境 / Activate virtual environment
print_info "正在激活虚拟环境... / Activating virtual environment..."
source venv/bin/activate

# 升级 pip / Upgrade pip
print_info "正在升级 pip... / Upgrading pip..."
pip install --upgrade pip --quiet

# 安装依赖项 / Install dependencies
print_info "正在安装依赖项... / Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    print_success "依赖项安装成功 / Dependencies installed successfully"
else
    print_error "未找到 requirements.txt / requirements.txt not found"
    exit 1
fi

# 安装 mac-info-tool 包 / Install mac-info-tool package
print_info "正在安装 mac-info-tool 包... / Installing mac-info-tool package..."
pip install -e . --quiet
print_success "mac-info-tool 包安装成功 / mac-info-tool package installed successfully"

# 检查可选工具 / Check optional tools
echo ""
print_info "检查可选工具... / Checking optional tools..."

if command -v osx-cpu-temp &> /dev/null; then
    print_success "osx-cpu-temp 已安装 / osx-cpu-temp is installed"
else
    print_warning "osx-cpu-temp 未安装 / osx-cpu-temp not installed"
    print_info "温度监控需要此工具 / Temperature monitoring requires this tool"
    print_info "安装命令: / Installation command:"
    echo "  brew install osx-cpu-temp"
fi

# 完成 / Complete
echo ""
print_success "============================================"
print_success "设置完成！/ Setup complete!"
print_success "============================================"
echo ""
print_info "要激活虚拟环境，请运行: / To activate the virtual environment, run:"
echo -e "  ${GREEN}source venv/bin/activate${NC}"
echo ""
print_info "然后可以使用以下命令: / Then you can use the following commands:"
echo "  mac-info help      # 显示帮助 / Show help"
echo "  mac-info list      # 列出命令 / List commands"
echo "  mac-info monitor   # 开始监控 / Start monitoring"
echo ""
print_info "运行测试: / Run tests:"
echo "  pytest"
echo ""

