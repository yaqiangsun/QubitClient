# ExperimentType 实验类型

`ExperimentType` 枚举用于指定 QCalEval 数据集中的 87 个具体测试用例，主要用于 VLM 评估。

## 实验类型列表

| 枚举值 | 描述 |
|--------|------|
| `ExperimentType.COUPLER_FLUX_SUCCESS` | 耦合器光谱成功 |
| `ExperimentType.COUPLER_FLUX_FAILURE_BAD_FIT` | 耦合器光谱拟合失败 |
| `ExperimentType.CZ_BENCHMARKING_SUCCESS` | CZ 基准测试成功 |
| `ExperimentType.CZ_BENCHMARKING_FAILURE_MISCALIBRATED` | CZ 基准测试校准失败 |
| `ExperimentType.CZ_BENCHMARKING_FAILURE_NO_GATE` | CZ 基准测试无门 |
| `ExperimentType.DRAG_SUCCESS` | DRAG 成功 |
| `ExperimentType.DRAG_FAILURE_NO_SIGNAL` | DRAG 无信号 |
| `ExperimentType.DRAG_FAILURE_POSITION_FAR_OFFSET` | DRAG 位置偏移 |
| `ExperimentType.DRAG_FAILURE_POSITION_FIRST_QUARTER` | DRAG 位置在第一象限 |
| `ExperimentType.DRAG_FAILURE_POSITION_LAST_QUARTER` | DRAG 位置在最后一象限 |
| `ExperimentType.GMM_SUCCESS` | GMM 成功 |
| `ExperimentType.GMM_FAILURE_HIGH_POWER` | GMM 高功率失败 |
| `ExperimentType.GMM_FAILURE_NO_EXCITATION` | GMM 无激发 |
| `ExperimentType.GMM_FAILURE_NO_RES_RESPONSE` | GMM 无共振响应 |
| `ExperimentType.GMM_FAILURE_NO_SIGNAL` | GMM 无信号 |
| `ExperimentType.MICROWAVE_RAMSEY_SUCCESS` | 微波 Ramsey 成功 |
| `ExperimentType.MICROWAVE_RAMSEY_FAILURE_DETUNED` | 微波 Ramsey 失谐 |
| `ExperimentType.MICROWAVE_RAMSEY_FAILURE_LOW_CONTRAST` | 微波 Ramsey 低对比度 |
| `ExperimentType.MOT_LOADING_GOOD` | MOT 加载良好 |
| `ExperimentType.MOT_LOADING_NO_SIGNAL` | MOT 无信号 |
| `ExperimentType.MOT_LOADING_TAILED` | MOT 有拖尾 |
| `ExperimentType.PINCHOFF_SUCCESS` | Pinch-off 成功 |
| `ExperimentType.PINCHOFF_FAILURE_INCOMPLETE_TRANSITION` | Pinch-off 不完整转变 |
| `ExperimentType.PINCHOFF_FAILURE_NOISY_NO_TRANSITION` | Pinch-off 噪声无转变 |
| `ExperimentType.PINCHOFF_FAILURE_STABILIZE_NEGATIVE` | Pinch-off 负稳定 |
| `ExperimentType.PINCHOFF_FAILURE_STABILIZE_POSITIVE` | Pinch-off 正稳定 |
| `ExperimentType.PINGPONG_SUCCESS_WELL_CALIBRATED` | PingPONG 校准良好 |
| `ExperimentType.PINGPONG_FAILURE_LARGE_ERROR` | PingPONG 大误差 |
| `ExperimentType.PINGPONG_FAILURE_MODERATE_ERROR` | PingPONG 中等误差 |
| `ExperimentType.PINGPONG_FAILURE_NO_EXCITATION` | PingPONG 无激发 |
| `ExperimentType.QUBIT_FLUX_SPECTROSCOPY_SUCCESS` | 量子比特通量光谱成功 |
| `ExperimentType.QUBIT_FLUX_SPECTROSCOPY_FAILURE_BAD_FIT` | 量子比特通量光谱拟合差 |
| `ExperimentType.QUBIT_FLUX_SPECTROSCOPY_FAILURE_FIT_FAILED` | 量子比特通量光谱拟合失败 |
| `ExperimentType.QUBIT_FLUX_SPECTROSCOPY_FAILURE_NO_DATA` | 量子比特通量光谱无数据 |
| `ExperimentType.QUBIT_FLUX_SPECTROSCOPY_FAILURE_NO_RESPONSE` | 量子比特通量光谱无响应 |
| `ExperimentType.QUBIT_FLUX_SPECTROSCOPY_FAILURE_NOT_TUNABLE` | 量子比特通量光谱不可调 |
| `ExperimentType.QUBIT_SPECTROSCOPY_SUCCESS` | 量子比特光谱成功 |
| `ExperimentType.QUBIT_SPECTROSCOPY_FAILURE_MULTIPLE_PEAKS` | 量子比特光谱多峰 |
| `ExperimentType.QUBIT_SPECTROSCOPY_FAILURE_NO_PEAKS` | 量子比特光谱无峰 |
| `ExperimentType.QUBIT_SPECTROSCOPY_POWER_FREQUENCY_SUCCESS_F01_F02HALF_FULL_RANGE` | 功率频率光谱成功 |
| `ExperimentType.QUBIT_SPECTROSCOPY_POWER_FREQUENCY_SUCCESS_F01_LOW_AMP_SHARP` | 功率频率光谱低幅尖锐 |
| `ExperimentType.QUBIT_SPECTROSCOPY_POWER_FREQUENCY_SUCCESS_F01_ONLY_FULL_RANGE` | 功率频率光谱仅 f01 |
| `ExperimentType.QUBIT_SPECTROSCOPY_POWER_FREQUENCY_FAILURE_F01_F02HALF_AMP_TOO_HIGH` | 功率频率光谱 f01/f02 幅值过高 |
| `ExperimentType.QUBIT_SPECTROSCOPY_POWER_FREQUENCY_FAILURE_F01_ONLY_AMP_TOO_HIGH` | 功率频率光谱 f01 幅值过高 |
| `ExperimentType.QUBIT_SPECTROSCOPY_POWER_FREQUENCY_FAILURE_NO_SIGNAL` | 功率频率光谱无信号 |
| `ExperimentType.RABI_SUCCESS` | Rabi 成功 |
| `ExperimentType.RABI_SUCCESS_OFF_RESONANCE` | Rabi 离共振成功 |
| `ExperimentType.RABI_SUCCESSFUL_LIMITED_RANGE` | Rabi 有限范围成功 |
| `ExperimentType.RABI_FAILURE_DAMPED_OSCILLATIONS` | Rabi 阻尼振荡失败 |
| `ExperimentType.RABI_FAILURE_RANDOM_SIGNAL` | Rabi 随机信号失败 |
| `ExperimentType.RABI_FAILURE_TOO_FAST` | Rabi 太快失败 |
| `ExperimentType.RABI_FAILURE_TOO_SLOW` | Rabi 太慢失败 |
| `ExperimentType.RABI_HW_SUCCESS` | Rabi 硬件成功 |
| `ExperimentType.RABI_HW_FAILURE_INCORRECT_FIT` | Rabi 硬件拟合错误 |
| `ExperimentType.RABI_HW_FAILURE_INSUFFICIENT_AMPLITUDE_RANGE` | Rabi 硬件幅值范围不足 |
| `ExperimentType.RABI_HW_FAILURE_OFF_RESONANT_DRIVE` | Rabi 硬件离共振驱动 |
| `ExperimentType.RAMSEY_CHARGE_TOMOGRAPHY_CLEAN` | Ramsey 电荷层析干净 |
| `ExperimentType.RAMSEY_CHARGE_TOMOGRAPHY_FEW_BURSTS` | Ramsey 电荷层析少量突发 |
| `ExperimentType.RAMSEY_CHARGE_TOMOGRAPHY_MANY_BURSTS` | Ramsey 电荷层析多次突发 |
| `ExperimentType.RAMSEY_CHARGE_TOMOGRAPHY_NOISY` | Ramsey 电荷层析噪声 |
| `ExperimentType.RAMSEY_SUCCESS_FREQ_CAL` | Ramsey 频率校准成功 |
| `ExperimentType.RAMSEY_FAILURE_FREQ_CAL_BEATING` | Ramsey 频率校准拍频失败 |
| `ExperimentType.RAMSEY_FAILURE_FREQ_CAL_TOO_FEW_OSC` | Ramsey 频率校准振荡太少 |
| `ExperimentType.RAMSEY_FAILURE_FREQ_CAL_TOO_MANY_OSC` | Ramsey 频率校准振荡太多 |
| `ExperimentType.RAMSEY_SUCCESS_T2STAR` | Ramsey T2* 成功 |
| `ExperimentType.RAMSEY_FAILURE_T2STAR_BEATING` | Ramsey T2* 拍频失败 |
| `ExperimentType.RAMSEY_FAILURE_T2STAR_SAMPLING_TOO_COARSE` | Ramsey T2* 采样太粗 |
| `ExperimentType.RAMSEY_FAILURE_T2STAR_WINDOW_TOO_SHORT` | Ramsey T2* 窗口太短 |
| `ExperimentType.RAMSEY_FAILURE_T2STAR_ZERO_DETUNING` | Ramsey T2* 零失谐 |
| `ExperimentType.RES_SPEC_SUCCESS_WIDE_SCAN_RESONATOR` | 共振器光谱宽扫描成功 |
| `ExperimentType.RES_SPEC_SUCCESS_ZOOMED_RESONATOR` | 共振器光谱缩放成功 |
| `ExperimentType.RES_SPEC_SUCCESS_2QUBIT_WIDE_SCAN_RESONATOR` | 双量子比特共振器成功 |
| `ExperimentType.RES_SPEC_FAILURE_WIDE_SCAN_NO_SIGNAL` | 共振器宽扫描无信号 |
| `ExperimentType.RES_SPEC_FAILURE_ZOOMED_NO_SIGNAL` | 共振器缩放无信号 |
| `ExperimentType.RYDBERG_RAMSEY_SUCCESS` | Rydberg Ramsey 成功 |
| `ExperimentType.RYDBERG_RAMSEY_FAILURE_UNDERSAMPLED` | Rydberg Ramsey 欠采样 |
| `ExperimentType.RYDBERG_SPECTROSCOPY_SUCCESS` | Rydberg 光谱成功 |
| `ExperimentType.RYDBERG_SPECTROSCOPY_FAILURE_LOW_CONTRAST` | Rydberg 光谱低对比度 |
| `ExperimentType.T1_SUCCESS` | T1 成功 |
| `ExperimentType.T1_FAILURE_NO_SIGNAL` | T1 无信号 |
| `ExperimentType.T1_FAILURE_SAMPLING_TOO_COARSE` | T1 采样太粗 |
| `ExperimentType.T1_FAILURE_WINDOW_TOO_SHORT` | T1 窗口太短 |
| `ExperimentType.T1_FLUCTUATIONS_STABLE` | T1 涨落稳定 |
| `ExperimentType.T1_FLUCTUATIONS_TELEGRAPHIC_FLUCTUATIONS` | T1 涨落 telegraph |
| `ExperimentType.T1_FLUCTUATIONS_RANDOM_WALK` | T1 涨落随机游走 |
| `ExperimentType.TWEEZER_ARRAY_SUCCESS` | 光镊阵列成功 |
| `ExperimentType.TWEEZER_ARRAY_FAILURE_ABERRATED` | 光镊阵列像差 |

## 使用示例

```python
from qubitclient.llm.experiments import ExperimentType

# 使用 ExperimentType 进行评估
experiment_type = ExperimentType.RABI_SUCCESS
print(experiment_type.value)  # "rabi_success"
```