# Ctrl.update_param 方法接口文档

## 概述

`update_param` 是 `QubitCtrlClient` 的实例方法，用于更新量子比特的参数值。

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
| task_type | str | 是 | 任务类型，例如 "rabi", "t1" 等 |
| values | dict | 是 | 要更新的参数键值对，例如 `{"pi_amp": 0.5}` |

### 调用示例

```python
# 更新量子比特 Q0 的 π 脉冲幅度
result = client.update_param(
    qname="Q0",
    task_type="rabi",
    values={"pi_amp": 0.5}
)
print(result)

# 更新量子比特 Q1 的频率参数
result = client.update_param(
    qname="Q1",
    task_type="s21",
    values={"frequency": 6.539}
)
print(result)
```

## 返回值格式

返回的结果包含更新操作的确认信息：

```json
{
  "qname": "Q0",
  "task_type": "rabi",
  "updated": true,
  "keys": ["pi_amp"]
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| qname | str | 量子比特名称 |
| task_type | str | 任务类型 |
| updated | bool | 更新是否成功 |
| keys | List[str] | 已更新的参数键名列表 |

## 应用场景

参数更新主要用于：
- 修改量子比特的校准参数
- 在自动化流程中批量更新配置
- 调整量子门操作参数