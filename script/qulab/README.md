# 数据采集 和 可视化 脚本

## 数据采集并分类保存
运行命令：
```
python data_classify.py
```
功能：通过get_report接口获取数据，并解析，将其中的量子数据保存在对应文件夹。

路径为：'./tmp/dataset' + ‘run/S21/tmp0a14b0ab_59362.npy’其中59362为get_report中填的索引，run/S21/tmp0a14b0ab是从数据中解析出来的信息。


## 数据可视化脚本
对于69种数据的可视化，下面举例一种：

运行命令示例：
```
python plot_S21_matplotlib.py
```
功能：将指定数据文件夹
root_folder = f'./tmp/dataset/run/{data_type}'

下的npy文件 读取、解析、绘图，

将图片保存在指定的路径中：
plot_save_folder = f'./tmp/visual/plot_{data_type}_matplotlib'