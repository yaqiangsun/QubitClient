# QubitClient 配置指南

## 配置加载优先级

QubitClient 支持多种配置方式，优先级从低到高如下：

### 1. 默认配置文件 (最低优先级)
在项目根目录创建 `config.py` 文件：

```python
# config.py
API_URL = "https://your-api-server.com"
API_KEY = "your-api-key-here"
```

### 2. 用户目录配置文件
在用户主目录下创建 `qubitclient.json` 文件：

**Windows:**
```
C:\Users\你的用户名\qubitclient.json
```

**Linux/Mac:**
```
~/.qubitclient.json 或 /home/你的用户名/qubitclient.json
```

**文件内容:**
```json
{
  "url": "https://your-api-server.com",
  "api_key": "your-api-key-here"
}
```

### 3. 环境变量
在操作系统中设置环境变量：

**Windows (命令提示符):**
```cmd
set QUBITCLIENT_URL=https://your-api-server.com
set QUBITCLIENT_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:QUBITCLIENT_URL="https://your-api-server.com"
$env:QUBITCLIENT_API_KEY="your-api-key-here"
```

**Linux/Mac:**
```bash
export QUBITCLIENT_URL="https://your-api-server.com"
export QUBITCLIENT_API_KEY="your-api-key-here"
```

或在 `~/.bashrc`、`~/.zshrc` 等 shell 配置文件中添加。

### 4. 运行目录配置文件 (高优先级)
在你的项目运行目录下创建 `qubitclient.json` 文件：

```json
{
  "url": "https://your-api-server.com",
  "api_key": "your-api-key-here"
}
```

### 5. 构造函数参数 (最高优先级)
直接在代码中传递参数：

```python
from qubitclient import QubitScopeClient, QubitNNScopeClient

# 直接传入 url 和 api_key
client = QubitScopeClient(
    url="https://your-api-server.com",
    api_key="your-api-key-here"
)

# 或者只传一个参数，另一个从配置加载
client = QubitNNScopeClient(api_key="your-api-key-here")
# url 将从配置文件中加载
```

## 优先级示例

如果同时存在多种配置方式：

```python
# 假设 ~/qubitclient.json 中 url="http://config1.com"
# 假设 ./qubitclient.json 中 url="http://config2.com"
# 假设环境变量 QUBITCLIENT_URL="http://config3.com"

# 使用构造函数参数（优先级最高）
client = QubitScopeClient(url="http://config4.com", api_key="key4")
# 最终使用：url="http://config4.com", api_key="key4"

# 不传参数
client = QubitScopeClient()
# 最终使用：url="http://config3.com"(环境变量), api_key="key4"(运行目录配置)
```

## 配置文件模板

参考项目中的 `qubitclient.json.example` 文件：

```json
{
  "url": "https://your-api-server.com",
  "api_key": "your-secret-api-key"
}
```

## 错误处理

如果必需的配置（url 或 api_key）在所有来源中都未提供，将抛出 `ValueError` 异常：

```python
try:
    client = QubitScopeClient()
except ValueError as e:
    print(f"配置错误：{e}")
    # 请按照提示信息提供相应的配置
```

## 推荐实践

1. **开发环境**: 使用用户目录配置文件 (`~/qubitclient.json`)
2. **生产环境**: 使用环境变量或运行目录配置文件
3. **多项目场景**: 每个项目使用独立的运行目录配置文件
4. **敏感信息**: 优先使用环境变量，避免将 API Key 写入配置文件
5. **团队协作**: 复制 `qubitclient.json.example` 为 `qubitclient.json` 并填入实际配置

## 向后兼容

该配置系统完全向后兼容旧的使用方式：

```python
# 旧的用法仍然有效
client = QubitScopeClient(url="...", api_key="...")

# 新的用法 - 自动从配置加载
client = QubitScopeClient()
```
