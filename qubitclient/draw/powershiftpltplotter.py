import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter

class PowerShiftDataPltPlotter(QuantumDataPltPlotter):

    def __init__(self):
        super().__init__("powershift")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item()
        image = data["image"]
        q_list = list(image.keys())  # 确保q_list是列表形式，便于索引
        num_qubits = len(q_list)

        # 数据提取
        items = []
        for q_name in q_list:
            image_q = image[q_name]
            x, y, value = image_q[0], image_q[1], image_q[2]
            
            # 获取当前量子比特对应的关键点、类别和配置
            idx = q_list.index(q_name)
            keypoints = result['keypoints_list'][idx] if idx < len(result['keypoints_list']) else []
            class_num = result['class_num_list'][idx] if idx < len(result['class_num_list']) else None
            conf = result['confs'][idx] if idx < len(result['confs']) else None
            
            items.append({
                'x': x,
                'y': y,
                'value': value,
                'keypoints': keypoints,
                'q_name': q_name,
                'class_num': class_num,
                'conf': conf
            })

        # 结果数据（原代码保留）
        confs = result['confs']
        class_num_list = result['class_num_list']
        keypoints_list = result['keypoints_list']

        # 合并所有item的图像到一张图中（多行多列布局）
        num_items = len(items)
        if num_items == 0:
            raise ValueError("没有可合并的item数据")
        
        # 配置每行最多显示的子图数量
        max_cols = 4
        # 计算需要的行数和列数
        rows = (num_items + max_cols - 1) // max_cols  # 向上取整计算行数
        cols = min(num_items, max_cols)                # 列数不超过max_cols
        
        # 创建多行多列布局的画布
        fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 6 * rows))
        # 将axes转换为一维数组（方便统一处理单一行/列的情况）
        axes = axes.flatten() if rows * cols > 1 else [axes]
        
        # 为每个item绘制内容
        for i, item in enumerate(items):
            ax = axes[i]
            x = item["x"]
            y = item["y"]
            values = item["value"]
            keypoints = item["keypoints"]
            q_name = item["q_name"]
            class_num = item["class_num"]
            conf = item["conf"]
            
            # 绘制原始图像
            im = ax.pcolormesh(x, y, values, cmap='viridis', shading='auto')
            fig.colorbar(im, ax=ax)
            
            # 绘制关键点
            if keypoints:
                sorted_keypoints = sorted(keypoints, key=lambda p: (-p[1], p[0]))
                kp_x = [p[0] for p in sorted_keypoints]
                kp_y = [p[1] for p in sorted_keypoints]
                ax.scatter(kp_x, kp_y, color='red', s=50, marker='*', label='Key Points')
                ax.plot(kp_x, kp_y, 'r--', linewidth=2)
            
            # 添加class和confs信息
            info_text = f"Qubit: {q_name}\n"
            if class_num is not None:
                info_text += f"Class: {class_num}\n"
            if conf is not None:
                # 格式化置信度为两位小数
                info_text += f"Confidence: {conf:.2f}"
            
            # 在图中添加文本信息
            ax.text(0.05, 0.95, info_text, transform=ax.transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            ax.set_title('Original Image')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.legend()
        
        # 隐藏多余的子图
        for i in range(num_items, rows * cols):
            axes[i].axis('off')
        
        # 调整布局
        plt.tight_layout()
        return fig