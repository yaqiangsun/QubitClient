# QubitClient 服务部署模板

本目录包含 QubitClient 服务的 Docker 部署模板，用于一键启动量子计算分析服务。

## 目录结构

```
serve_templates/
├── docker-compose.yml          # 主编排文件（启动所有服务）
├── qubitscope/                 # qubitscope 服务
│   ├── docker-compose.yml
│   └── license/
│       └── license.json        # 授权文件
├── qubitserving/               # qubitserving 服务
│   ├── docker-compose.yml
│   ├── license/
│   │   └── license.json        # 授权文件
│   └── model_zoo/              # 模型目录
│       └── README.md
└── proxy/                      # API 代理服务
    ├── docker-compose.yml
    └── config/
        └── proxy_config.json   # 代理配置
```

## 快速开始

### 1. 初始化部署文件

```bash
qubitclient serve init
```

这会将 `serve_templates` 目录复制到当前目录。

### 2. 配置授权文件

#### qubitscope/license/license.json

QubitScope 服务的授权文件，包含以下字段：

| 字段 | 类型 | 描述 |
|------|------|------|
| `license_key` | string | 授权密钥 |
| `customer` | string | 客户名称 |
| `expiry_date` | string | 过期日期 (YYYY-MM-DD) |

#### qubitserving/license/license.json

QubitServing 服务的授权文件，字段同上。

### 3. 配置模型

#### qubitserving/model_zoo/

将模型文件放入此目录，供 QubitServing 服务使用。

### 4. 启动服务

```bash
# 启动所有服务
qubitclient serve init


# 查看服务状态
docker ps

# 查看日志
docker-compose logs -f
```

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

基于深度学习的神经망分析服务，提供二维能谱分析、功率偏移曲线分割等功能。

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