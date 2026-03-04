<h1 align="center">
  <img src="asset/qubitclient.png" alt="QubitClient Logo" width="200"/>
  <br>
  QubitClient: 面向量子系统的AI客户端
</h1>

<p align="center">
  <a href="https://pypi.org/project/qubitclient/">
    <img src="https://img.shields.io/pypi/v/qubitclient?style=flat-square&logo=pypi&logoColor=white" alt="PyPI version">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/pypi/pyversions/qubitclient?style=flat-square&logoColor=white&logo=python" alt="Python versions">
  </a>
  <a href="https://pypi.org/project/qubitclient/">
    <img src="https://img.shields.io/pypi/dm/qubitclient?style=flat-square&logo=pypi&logoColor=white" alt="PyPI Downloads">
  </a>
  <!-- <a href="https://github.com/yaqiangsun/qubitclient/stargazers">
    <img src="https://img.shields.io/github/stars/yaqiangsun/qubitclient?style=flat-square&logo=github" alt="GitHub Stars">
  </a> -->
  <!-- <a href="https://github.com/yaqiangsun/qubitclient/fork">
    <img src="https://img.shields.io/github/forks/yaqiangsun/qubitclient?style=flat-square&logo=github" alt="GitHub Forks">
  </a> -->
  <!-- <a href="https://github.com/yaqiangsun/qubitclient/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/yaqiangsun/qubitclient?style=flat-square&logo=github" alt="Contributors">
  </a> -->
  <a href="https://github.com/yaqiangsun/qubitclient/issues">
    <img src="https://img.shields.io/github/issues/yaqiangsun/qubitclient?style=flat-square" alt="Issues">
  </a>
  <!-- <a href="https://github.com/yaqiangsun/qubitclient/pulls">
    <img src="https://img.shields.io/github/issues-pr/yaqiangsun/qubitclient?style=flat-square" alt="Pull Requests">
  </a> -->
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/yaqiangsun/qubitclient?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/yaqiangsun/qubitclient/commits/main">
    <img src="https://img.shields.io/github/last-commit/yaqiangsun/qubitclient?style=flat-square&logo=github" alt="Last Commit">
  </a>
  <!-- <a href="https://github.com/yaqiangsun/qubitclient/releases">
    <img src="https://img.shields.io/github/v/release/yaqiangsun/qubitclient?style=flat-square&logo=github" alt="GitHub Release">
  </a> -->
  <img src="https://img.shields.io/badge/Quantum-Computing-blue?style=flat-square&logo=ibm" alt="Quantum Computing">
  <img src="https://img.shields.io/badge/Machine_Learning-AI-green?style=flat-square&logo=machinelearn" alt="AI/ML">
  <br>
  <a href="#-介绍">介绍</a> •
  <a href="#-功能特性">功能特性</a> •
  <a href="#-安装">安装</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-支持的任务类型">任务类型</a> •
  <a href="#-文档与示例">文档</a> •
  <a href="#-许可证">许可证</a>
</p>

<p align="center">
  <b>中文</b> | <a href="README.en.md">English</a>
</p>

---

## 📖 介绍

**QubitClient** 是一个功能强大的 Python 客户端库，用于与 **Qubit 服务**进行高效交互。它封装了丰富的 API 接口，专为量子计算实验数据处理而设计，支持**曲线分割**、**参数拟合**等多种任务，帮助研究人员快速分析二维能谱、功率偏移曲线等关键实验数据。

## ✨ 功能特性

- 🧠 **智能数据分析**：支持二维能谱分析、功率偏移曲线分析等复杂任务。
- 🔬 **多种量子计算任务**：涵盖 S21 峰值检测、最优 π 脉冲、Rabi 振荡、T1/T2 拟合等常见实验分析。
- 📦 **灵活的数据输入**：可直接传入文件路径、NumPy 数组或字典，适配不同数据源。
- ⚡ **批量处理**：轻松同时处理多个数据文件，提高工作效率。
- 🔌 **易于集成**：简洁的 API 设计，可快速融入现有项目流程。
- 🤝 **MCP 协议支持**：基于 MCP 协议的实时量子测量任务控制，实现实验自动化。

## 📦 安装

推荐使用 `pip` 进行安装：

```bash
pip install qubitclient
```

如果需要绘图等额外功能，可以安装完整版：

```bash
pip install qubitclient[full]
```

### 源码安装

如果你想使用最新开发版本，也可以从源码安装：

```bash
git clone https://github.com/yaqiangsun/qubitclient.git
cd qubitclient
pip install -e .
```

## 🚀 快速开始

### 1️⃣ 配置

首先，复制配置文件模板并根据实际情况修改：

```bash
cp config.py.example config.py
```

编辑 `config.py`，填入您的服务器地址和 API 密钥：

```python
API_URL = "http://your-server-address:port"
API_KEY = "your-api-key"
```

### 2️⃣ 使用示例

#### 🧠 NNScope 功能（曲线分割）

```python
from qubitclient import QubitNNScopeClient, NNTaskName, CurveType
import numpy as np

# 初始化客户端
client = QubitNNScopeClient(url="http://your-server-address:port", api_key="your-api-key")

# 方式1：使用文件路径
file_path_list = ["data/file1.npz", "data/file2.npz"]
response = client.request(
    file_list=file_path_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# 方式2：使用 NumPy 数组字典
data_ndarray = np.load("data/file1.npz", allow_pickle=True)
dict_list = [data_ndarray]
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.POLY
)

# 获取结果
results = client.get_result(response=response)
```

#### 🔬 Scope 功能（参数拟合）

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient(url="http://your-server-address:port", api_key="your-api-key")

# 准备数据（示例）
dict_list = [{
    "x_data": np.array([...]),
    "y_data": np.array([...])
}]

response = client.request(
    file_list=dict_list,
    task_type=TaskName.OPTPIPULSE  # 可选任务见下方列表
)

results = client.get_result(response=response)
```

#### 🤖 Ctrl 功能（MCP 协议测量任务）

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()

# 执行 S21 腔频测量实验
result = client.run(
    task_type=CtrlTaskName.S21,
    qubits_use=["Q0", "Q1"],
    frequency_start=-40e6,
    frequency_end=40e6,
    frequency_sample_num=101
)

print(result)
```

## 📋 支持的任务类型

### 🧠 NNScope 任务（曲线分割）

| 任务名称 | 描述 | 详细文档 |
|---------|------|---------|
| `NNTaskName.SPECTRUM2D` | 二维频谱数据曲线分割 | [文档](docs/nnscope/SPECTRUM2D.md) |
| `NNTaskName.POWERSHIFT` | 功率偏移曲线分割 | [文档](docs/nnscope/POWERSHIFT.md) |
| `NNTaskName.S21VFLUX` | S21 vs Flux 参数曲线分割 | [文档](docs/nnscope/S21VFLUX.md) |
| `NNTaskName.SPECTRUM` | 频谱分析 | [文档](docs/nnscope/SPECTRUM.md) |
| `NNTaskName.S21PEAK` | S21 峰值检测 | [文档](docs/nnscope/S21PEAK.md) |

### 🔬 Scope 任务（参数拟合）

| 任务名称 | 描述 | 详细文档 |
|---------|------|---------|
| `TaskName.S21PEAK` | S21 参数峰值检测 | [文档](docs/scope/S21PEAK.md) |
| `TaskName.OPTPIPULSE` | 最优 π 脉冲计算 | [文档](docs/scope/OPTPIPULSE.md) |
| `TaskName.RABICOS` | Rabi 振荡余弦第一峰检测 | [文档](docs/scope/RABICOS.md) |
| `TaskName.RAMSEY` | RAMSY 衰减震荡余弦拟合 | [文档](docs/scope/RAMSEY.md) |
| `TaskName.S21VFLUX` | S21 vs Flux 分析 | [文档](docs/scope/S21VFLUX.md) |
| `TaskName.SINGLESHOT` | 单次测量分析 | [文档](docs/scope/SINGLESHOT.md) |
| `TaskName.SPECTRUM` | 频谱分析 | [文档](docs/scope/SPECTRUM.md) |
| `TaskName.T1FIT` | T1 时间拟合 | [文档](docs/scope/T1FIT.md) |
| `TaskName.T2FIT` | T2 时间拟合 | [文档](docs/scope/T2FIT.md) |
| `TaskName.POWERSHIFT` | 功率偏移曲线分析 | [文档](docs/scope/POWERSHIFT.md) |
| `TaskName.SPECTRUM2D` | 二维频谱数据曲线分割 | [文档](docs/scope/SPECTRUM2D.md) |
| `TaskName.DRAG` | DRAG 免交叉点分析 | [文档](docs/scope/DRAG.md) |

### 🤖 Ctrl 任务（MCP 协议）

| 任务名称 | 描述 | 详细文档 |
|---------|------|---------|
| `CtrlTaskName.S21` | S21 腔频测量实验 | [文档](docs/ctrl/S21.md) |
| `CtrlTaskName.DRAG` | DRAG 免交叉点测量 | [文档](docs/ctrl/DRAG.md) |
| `CtrlTaskName.DELTA` | 频率偏移校准测量 | [文档](docs/ctrl/DELTA.md) |
| `CtrlTaskName.OPT_PIPULSE` | 最优 π 脉冲测量 | [文档](docs/ctrl/OPT_PIPULSE.md) |
| `CtrlTaskName.POWERSHIFT` | 功率偏移曲线测量 | [文档](docs/ctrl/POWERSHIFT.md) |
| `CtrlTaskName.RABI` | Rabi 振荡测量 | [文档](docs/ctrl/RABI.md) |
| `CtrlTaskName.RAMSEY` | Ramsey 干涉测量 | [文档](docs/ctrl/RAMSEY.md) |
| `CtrlTaskName.S21VSFLUX` | S21 vs Flux 测量 | [文档](docs/ctrl/S21VSFLUX.md) |
| `CtrlTaskName.SINGLESHOT` | 单次测量分析 | [文档](docs/ctrl/SINGLESHOT.md) |
| `CtrlTaskName.SPECTRUM` | 频谱分析测量 | [文档](docs/ctrl/SPECTRUM.md) |
| `CtrlTaskName.SPECTRUM_2D` | 二维频谱测量 | [文档](docs/ctrl/SPECTRUM_2D.md) |
| `CtrlTaskName.T1` | T1 弛豫时间测量 | [文档](docs/ctrl/T1.md) |

## 📁 数据格式说明

不同任务对输入/输出数据格式有不同要求，请参考对应任务的详细文档（上面链接）获取具体说明。

## 🧪 运行测试示例

项目提供了丰富的测试示例，位于 [`tests`](tests) 目录下：

```bash
# 运行 NNScope 测试
python tests/test_nnscope.py

# 运行 Scope 测试
python tests/test_scope.py

# 运行 Ctrl 测试
python tests/test_ctrl_mcp.py
```

## 🔧 格式转换与工具集成

如需将数据转换为特定格式或集成其他工具，请参考 [`resources`](resources) 目录下的实用脚本。

## 📝 更新日志

### v0.4.0 (近期更新)
- 🎨 **优化绘制功能**：统一结果绘制风格
- 🤝 **增加 Ctrl 功能包**：基于 MCP 协议的实时测量任务
- 📈 **增加 DRAG 分析功能**：支持 DRAG 任务数据分析
- 🧩 **增加 scope 功能包**：新增多种拟合任务
- 📐 **增加曲线类型**：支持余弦类型曲线拟合
- 🏗️ **构建基础项目**：完成基础功能与结构搭建

## 🤝 贡献指南

欢迎通过 [Issues](https://github.com/yaqiangsun/qubitclient/issues) 提交问题或建议。如果您想贡献代码，请 Fork 本仓库并提交 Pull Request。

## 📄 许可证

本项目采用 **GPL-3.0 许可证**。详情请参阅 [LICENSE](LICENSE) 文件。

---

<!-- <p align="center">
  Made with ❤️ by yaqiangsun
</p> -->