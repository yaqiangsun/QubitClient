# Installation Guide

---

## Environment Requirements

- Python 3.10+ (required for both Client and Server)
- Docker and Docker Compose (Server only)

---

## Server Installation

The Server is deployed via Docker containers, including proxy service, quantization analysis service, and License service.

### 1. Initialize Deployment Files

```bash
qubitclient serve init
```

This creates a `serve_templates/` directory in the current directory, containing:
- `docker-compose.yml` - Main service orchestration configuration
- `qubitserving/` - Quantization analysis service (includes `model_zoo/` model directory and `license/` license directory)
- `qubitscope/` - Lightweight analysis service (includes `license/` license directory)
- `proxy/` - Proxy service
- `modellock/` - License service
- `vllm/` - LLM service (requires separate deployment)

### 2. Download Models

```bash
# Use default model
qubitclient serve download
```

Models will be downloaded to `serve_templates/qubitserving/model_zoo/` directory.

### 3. Apply for License

```bash
# Configure license token
# Edit qubitclient.json, add:
# {
#   "license": {
#     "token": "your_token_here"
#   }
# }

qubitclient serve license
```

License files will be automatically saved to `serve_templates/qubitserving/license/license.json` and `serve_templates/qubitscope/license/license.json`.

### 4. Start Services

```bash
# Run in foreground
qubitclient serve up

# Run in detached mode (recommended)
qubitclient serve up -d
```

Services can be accessed via qubitclient after startup.

### 5. Stop Services

```bash
cd serve_templates
docker-compose down
```

---

## LLM Service Deployment

The LLM service needs to be deployed separately on a machine with GPU. You still need to initialize the service template first:

```bash
qubitclient serve init
```

### Start Service

On the GPU server, navigate to the `serve_templates/vllm` directory:

```bash
cd serve_templates/vllm
docker compose up -d
```

### Stop Service

```bash
cd serve_templates/vllm
docker compose down
```

---

## Client Installation

The Client is a Python package used to interact with the Server.

### 1. Install qubitclient

```bash
# Basic installation
pip install qubitclient
```

### 2. Install Optional Dependencies

```bash
# Full features
pip install qubitclient[full]
```

### 3. Initialize Configuration Files

```bash
# Initialize configuration in project directory
qubitclient init
```

This creates:
- `qubitclient.json` - Main configuration file
- `.mcp.json` - MCP tool configuration

### 4. Configure qubitclient.json

Edit the generated `qubitclient.json`:

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

Configuration说明:
- `url` - Server API address, corresponds to proxy service address and port
- `api_key` - Server API access key, must match the key in proxy configuration
- `llm.api_key` - LLM service API key, used to call vllm service
- `llm.base_url` - LLM service base URL, format is `http://<vllm_service_IP>:<port>/v1`
- `llm.model` - Model name to use, must match the model deployed in vllm
- `license.token` - License application token, used to apply for license from modellock service

### Client Configuration to Server Service Mapping

| Client Config | Corresponding Server Service | Description |
|--------------|------------------------------|-------------|
| `url` | proxy | Proxy service address, typically `http://<server_IP>:9801` |
| `api_key` | proxy | Must match `api_keys` in `serve_templates/proxy/config/proxy_config.json` |
| `llm.base_url` | vllm | vllm service address, typically `http://<GPU_server_IP>:9091/v1` |
| `llm.model` | vllm | Must match the model name deployed in vllm container |

### 5. Verify Installation

```bash
# Check version
qubitclient --version

# View help
qubitclient --help
```

---

## Quick Start

1. Start Server services (see Server Installation)

2. Deploy LLM service (see LLM Service Deployment)

3. Configure Client connection information

4. Use in Python code:

```python
from qubitclient import Scope

scope = Scope()
result = scope.t1_fit(data)
```