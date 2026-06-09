# QubitClient 服务部署模板

本目录包含 QubitClient 服务的 Docker 部署模板，用于一键启动量子计算分析服务。

## 环境要求

- Python 3.10+
- Docker 和 Docker Compose

## 目录结构

```
serve_templates/
├── docker-compose.yml              # 主编排文件（启动所有服务）
├── qubitscope/                     # qubitscope 服务
│   ├── docker-compose.yml
│   └── license/
│       └── license.json            # 授权文件
├── qubitserving/                   # qubitserving 服务
│   ├── docker-compose.yml
│   ├── license/
│   │   └── license.json            # 授权文件
│   └── model_zoo/                  # 模型目录
│       └── README.md
├── proxy/                          # API 代理服务
│   ├── docker-compose.yml
│   └── config/
│       └── proxy_config.json       # 代理配置
├── modellock/                      # License 服务
│   ├── docker-compose.yml
│   └── .env.production
└── vllm/                           # LLM 服务（需单独部署）
    ├── docker-compose.yml
    ├── .env
    └── test.sh
```

## 快速开始

### 1. 初始化部署文件

```bash
qubitclient serve init
```

这会在当前目录下创建 `serve_templates/` 文件夹，包含所有服务配置文件。

### 2. 下载模型

```bash
qubitclient serve download
```

模型会下载到 `serve_templates/qubitserving/model_zoo/` 目录。

### 3. 申请许可证

首先在 `qubitclient.json` 中配置 license token：

```json
{
  "license": {
    "token": "your_token_here"
  }
}
```

然后执行：

```bash
qubitclient serve license
```

许可证文件会自动保存到：
- `serve_templates/qubitserving/license/license.json`
- `serve_templates/qubitscope/license/license.json`

### 4. 启动服务

```bash
# 前台运行
qubitclient serve up

# 后台运行（推荐）
qubitclient serve up -d
```

### 5. 停止服务

```bash
qubitclient serve down
```

或者进入目录手动停止：

```bash
cd serve_templates
docker-compose down
```

## 授权文件说明

### qubitscope/license/license.json

QubitScope 服务的授权文件，包含以下字段：

| 字段 | 类型 | 描述 |
|------|------|------|
| `license_key` | string | 授权密钥 |
| `customer` | string | 客户名称 |
| `expiry_date` | string | 过期日期 (YYYY-MM-DD) |

### qubitserving/license/license.json

QubitServing 服务的授权文件，字段同上。

## 模型目录

### qubitserving/model_zoo/

将模型文件放入此目录，供 QubitServing 服务使用。也可以使用 `qubitclient serve download` 命令自动下载默认模型。

## 服务说明

### Proxy (API 代理)

地址: `http://localhost:8000`

Proxy 作为统一的 API 网关，将请求路由到后端服务。

#### proxy_config.json 配置

```json
{
  "TARGET_URLS": {
    "default": "http://0.0.0.0:9000",
    "api/v1/tasks/scope": "http://0.0.0.0:9001",
    "api/v1/tasks/nnscope": "http://0.0.0.0:9000"
  },
  "TARGET_FILE_KEYS": {
    "default": "files",
    "api/v1/tasks/scope": "files",
    "api/v1/tasks/nnscope": "request"
  },
  "API_KEY": "SELF-DEFINED-API_KEY",
  "SAVE_FILES": true
}
```

**配置说明：**

| 字段 | 描述 |
|------|------|
| `TARGET_URLS` | 路由配置，将不同 API 路径映射到对应的后端服务 |
| `TARGET_FILE_KEYS` | 文件上传时使用的请求字段名 |
| `API_KEY` | API 认证密钥，请求时需要在 Header 中提供 `X-API-Key` |
| `SAVE_FILES` | 是否保存上传的文件到本地 |

**路由规则：**
- `api/v1/tasks/scope` → qubitscope 服务 (端口 9001)
- `api/v1/tasks/nnscope` → qubitserving 服务 (端口 9000)
- 其他路径 → 默认服务 (端口 9000)

### QubitScope

地址: `http://localhost:9001`

传统拟合分析服务，提供 S21 峰值检测、最优 π 脉冲、T1/T2 拟合等功能。

### QubitServing

地址: `http://localhost:9000`

基于深度学习的神经网络分析服务，提供二维能谱分析、功率偏移曲线分割等功能。

## LLM 服务部署

LLM 服务需要单独部署在具有 GPU 的机器上。

### 1. 初始化服务模板

```bash
qubitclient serve init
```

### 2. 启动 LLM 服务

在 GPU 服务器上进入 `serve_templates/vllm` 目录：

```bash
cd serve_templates/vllm
docker compose up -d
```

### 3. 停止 LLM 服务

```bash
cd serve_templates/vllm
docker compose down
```

## API 使用示例

```python
from qubitclient import QubitScopeClient, QubitNNScopeClient

# Scope 服务
scope_client = QubitScopeClient(
    url="http://localhost:9001",
    api_key="SELF-DEFINED-API_KEY"
)

# NNScope 服务
nnscope_client = QubitNNScopeClient(
    url="http://localhost:9000",
    api_key="SELF-DEFINED-API_KEY"
)
```