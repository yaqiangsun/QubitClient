# Ctrl.query_param 方法接口文档

## 概述

`query_param` 是 `QubitCtrlClient` 的实例方法，用于查询量子比特的参数值。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| qname | str | 是 | 量子比特名称，例如 "Q0" |
| key | str | 是 | 参数键名，例如 "frequency", "pi_amp" 等 |

### 调用示例

```python
# 查询量子比特 Q0 的频率参数
result = client.query_param(qname="Q0", key="frequency")
print(result)

# 查询量子比特 Q1 的 π 脉冲幅度
result = client.query_param(qname="Q1", key="pi_amp")
print(result)
```

## 返回值格式

返回的结果包含指定量子比特的参数值：

```json
{
  "qname": "Q0",
  "key": "frequency",
  "value": 6.539,
  "unit": "GHz"
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| qname | str | 量子比特名称 |
| key | str | 参数键名 |
| value | any | 参数值 |
| unit | str | 参数单位（如果有） |

## 应用场景

参数查询主要用于：
- 获取量子比特的当前配置参数
- 验证校准结果
- 在自动化脚本中读取参数进行后续处理