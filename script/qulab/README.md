# qulab 数据采集与可视化

## 数据采集并分类保存

运行命令：
```bash
python dataset_parser.py
```

功能：通过 `get_report` 接口获取数据，解析并保存到 `./tmp/dataset` 目录。

## 数据可视化脚本

每个 `plot_*.py` 脚本对应一种数据类型：

```bash
python visualization/plot_S21_matplotlib.py
```

会将 `./tmp/dataset/run/{data_type}/` 下的 npy 文件读取、解析、绘图，保存到 `./plot_{data_type}_matplotlib/` 目录。

## 数据类型列表

| 脚本 | 数据类型 |
|------|----------|
| plot_S21_matplotlib.py | S21 |
| plot_t1_1d_matplotlib.py | t1_1d |
| plot_t1_2d_matplotlib.py | t1_2d |
| plot_t1_repeat_matplotlib.py | t1_repeat |
| plot_spectrum_matplotlib.py | spectrum |
| plot_ramsey_matplotlib.py | ramsey |
| plot_spin_echo_matplotlib.py | spin_echo |
| plot_rabi_1d_align_matplotlib.py | rabi_1d_align |
| plot_rabi_2d_matplotlib.py | rabi_2d |
| plot_cphase_1d_matplotlib.py | cphase_1d |
| plot_singleshot_matplotlib.py | singleshot |
| ... | ... |

完整列表请查看 `visualization/` 目录。