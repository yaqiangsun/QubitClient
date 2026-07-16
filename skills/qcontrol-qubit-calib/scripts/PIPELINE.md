# 测量实验接口文档

本文档以 `pipeline/**_pipeline.py` 脚本和比特 `q1` 为例，讲解所有测量实验任务的接口与调用实例。

---

## 测量实验顺序

```
s21 → spectroscopy → spectroscopy_adaptive → drag →
singleshot → rb → ramsey → pi_pulse → pi_pulse_half → T1
```

---
