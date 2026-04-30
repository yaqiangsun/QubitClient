# 安装指南

---

## 环境要求

- Python 3.10+（Client 和 Server 都需要）
- Docker 和 Docker Compose（仅 Server 端）

---

## Server 端安装

Server 端通过 Docker 容器化部署，包含代理服务、量化分析服务和 License 服务。

### 1. 初始化部署文件

```bash
qubitclient serve init
```

这会在当前目录下创建 `serve_templates/` 文件夹，包含：
- `docker-compose.yml` - 主服务编排配置
- `qubitserving/` - 量化分析服务（含 `model_zoo/` 模型目录、`license/` 许可证目录）
- `qubitscope/` - 轻量分析服务（含 `license/` 许可证目录）
- `proxy/` - 代理服务
- `modellock/` - License 服务
- `vllm/` - LLM 服务（需单独部署）

### 2. 下载模型

```bash
# 使用默认模型
qubitclient serve download
```

模型会下载到 `serve_templates/qubitserving/model_zoo/` 目录。

### 3. 申请许可证

```bash
# 配置 license token
# 编辑 qubitclient.json，添加：
# {
#   "license": {
#     "token": "your_token_here"
#   }
# }

qubitclient serve license
```

许可证文件会自动保存到 `serve_templates/qubitserving/license/license.json` 和 `serve_templates/qubitscope/license/license.json`。

### 4. 启动服务

```bash
# 前台运行
qubitclient serve up

# 后台运行（推荐）
qubitclient serve up -d
```

服务启动后可通过 qubitclient 访问服务。

### 5. 停止服务

```bash
cd serve_templates
docker-compose down
```

---

## LLM 服务部署

LLM 服务需要单独部署在具有 GPU 的机器上，仍需要先初始化服务模板：

```bash
qubitclient serve init
```

### 启动服务

在 GPU 服务器上进入 `serve_templates/vllm` 目录：

```bash
cd serve_templates/vllm
docker compose up -d
```

### 停止服务

```bash
cd serve_templates/vllm
docker compose down
```

---

## Client 端安装

Client 端是 Python 包，用于与 Server 端交互。

### 1. 安装 qubitclient

```bash
# 基础安装
pip install qubitclient
```

### 2. 安装可选依赖

```bash
# 完整功能
pip install qubitclient[full]
```

### 3. 初始化配置文件

```bash
# 在项目目录中初始化配置
qubitclient init
```

这会创建：
- `qubitclient.json` - 主配置文件
- `.mcp.json` - MCP 工具配置

### 4. 配置 qubitclient.json

编辑生成的 `qubitclient.json`：

```json
{
  "url": "http://localhost:9801",
  "api_key": "your_api_key",
  "llm": {
    "api_key": "your_vllm_api_key",
    "base_url": "http://xx.xx.xx.xx:9091/v1",
    "model": "nv-community/Ising-Calibration-1-35B-A3B"
  },
  "license": {
    "token": "your_license_token"
  }
}
```

配置项说明：
- `url` - Server 端 API 地址，对应 proxy 服务的地址和端口
- `api_key` - 访问 Server 端 API 的密钥，需与 proxy 配置中的密钥一致
- `llm.api_key` - LLM 服务的 API Key，用于调用 vllm 服务
- `llm.base_url` - LLM 服务的 base URL，格式为 `http://<vllm服务IP>:<端口>/v1`
- `llm.model` - 使用的模型名称，需与 vllm 部署的模型一致
- `license.token` - License 申请令牌，用于向 modellock 服务申请许可证

### Client 端配置与 Server 端服务的对应关系

| Client 端配置 | 对应 Server 端服务 | 说明 |
|--------------|------------------|------|
| `url` | proxy | proxy 服务的访问地址，通常为 `http://<服务器IP>:9801` |
| `api_key` | proxy | 需与 `serve_templates/proxy/config/proxy_config.json` 中的 `api_keys` 一致 |
| `llm.base_url` | vllm | vllm 服务的地址，通常为 `http://<GPU服务器IP>:9091/v1` |
| `llm.model` | vllm | 需与 vllm 容器中部署的模型名称一致 |

### 5. 验证安装

```bash
# 检查版本
qubitclient --version

# 查看帮助
qubitclient --help
```

---

## 快速开始

1. 启动 Server 端服务（参考 Server 端安装）

2. 部署 LLM 服务（参考 LLM 服务部署）

3. 配置 Client 端连接信息

4. 在 Python 代码中使用

```