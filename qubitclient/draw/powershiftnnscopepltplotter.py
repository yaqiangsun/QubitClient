import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter
import cv2


def convert_complex_map_to_image(iq_avg):
    # 检查并转置
    rows, cols = iq_avg.shape
    # if rows < cols:
    #     iq_avg = iq_avg.T  # 转置矩阵


    # 取相位
    phase = np.angle(iq_avg)
    phase_normalized = ((phase + np.pi) / (2 * np.pi)) * 255
    # 纵向归一化
    phase_mean = phase_normalized.mean(axis=0, keepdims=True)   # 形状(1,30)
    ppase_std = phase_normalized.std(axis=0, keepdims=True)     # 形状(1,30)
    phase_normalized = (phase_normalized - phase_mean) / (ppase_std+1e-8)
    # phase_normalized = phase_normalized.astype(np.uint8)

    # 全局归一化
    phase_normalized = cv2.normalize(phase_normalized, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # 取幅度
    iq_avg = np.abs(iq_avg)
    
    # iq_avg = phase_normalized
    # 纵向归一化
    # mean = iq_avg.mean(axis=0, keepdims=True)   # 形状(1,30)
    # std = iq_avg.std(axis=0, keepdims=True)     # 形状(1,30)
    # iq_avg = (iq_avg - mean) / (std+1e-8)
    # 幅度全局归一化

    # 将输入数组 iq_avg 按线性比例把最小值映射到 0、最大值映射到 255
    iq_avg_normalized = cv2.normalize(iq_avg, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # 取幅度的梯度（保留备用）
    gradient_y, gradient_x = np.gradient(iq_avg)
    gradient_y = np.abs(gradient_y)
    gradient_y_normalized = cv2.normalize(gradient_y, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # 将单通道灰度映射为彩色图（使用 Viridis），applyColorMap 返回 BGR，需要转换为 RGB
    try:
        color_img_bgr = cv2.applyColorMap(iq_avg_normalized, cv2.COLORMAP_VIRIDIS)
        iq_avg_normalized_rgb = cv2.cvtColor(color_img_bgr, cv2.COLOR_BGR2RGB)
    except Exception:
        iq_avg_normalized_rgb = cv2.merge([iq_avg_normalized, iq_avg_normalized, iq_avg_normalized])

    return iq_avg_normalized_rgb


# 将 keypoints 映射到当前图的 x,y 坐标系（支持 keypoints 为 索引 或 物理值）
def _map_kps_to_coords(kps, xarr, yarr):
    pts = []
    if kps is None:
        return pts
    # 如果 xarr,yarr 为一维坐标向量
    xarr = np.asarray(xarr)
    yarr = np.asarray(yarr)
    nx = len(xarr)
    ny = len(yarr)

    for kp in kps:
        if not (isinstance(kp, (list, tuple)) and len(kp) >= 2):
            continue
        try:
            kx = float(kp[0])
            ky = float(kp[1])
        except (TypeError, ValueError):
            continue
        # 如果 kx 落在 xarr 的实际坐标范围内，直接使用；否则当作索引映射到坐标数组
        if nx > 0 and np.min(xarr) <= kx <= np.max(xarr):
            cx = kx
        else:
            # 将索引或异常值映射到坐标区间（线性插值）
            cx = float(np.interp(kx, np.arange(nx), xarr)) if nx > 0 else kx
        if ny > 0 and np.min(yarr) <= ky <= np.max(yarr):
            cy = ky
        else:
            cy = float(np.interp(ky, np.arange(ny), yarr)) if ny > 0 else ky
        pts.append((cx, cy))
    return pts


class PowershiftNNScopeDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("powershitnnscope")

    def plot_result_npy(self, **kwargs):
        powershift_labels = {0:"cos_light", 1:"cos_dark", 2:"line_light", 3:"line_dark"}

        result = kwargs.get('results')
        data_ndarray = kwargs.get('data_ndarray')
        data = data_ndarray.item()
        image = data["image"]
        q_list = list(image.keys())

        # 虽然dict变list但是每次都是单个文件画图
        result = result[0]

        # 之前result = {'q_list': ['Q1', 'Q2', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'], 'keypoints_list': [[[[25.755, 6.516], [25.755, 10.325]]], [[[25.086, 0.89], [24.974, 14.963]]], [[[25.755, 13.48], [24.926, 21.0]]], [[[25.309, 4.842], [25.612, 15.401]]], [[[25.787, 13.512], [25.484, 20.875]]], [[[25.755, 3.025], [25.755, 10.277]]], [[[25.787, 13.911], [25.707, 20.852]]]], 'confs': [0.6827890276908875, 0.5798720121383667, 0.7707597613334656, 0.5687557458877563, 0.7479773163795471, 0.7710826396942139, 0.7577250599861145], 'class_num_list': [1, 1, 1, 1, 1, 1, 1]}
        # 目前result =  [{'q_list': ['Q0', 'Q1'], 'confs': [0.418, 0.683], 'class_num_list': [3, 1], 'keypoints_list': [[[17.3, 0.7], [23.9, 12.4], [23.9, 21.0]], [[25.755, 6.516], [25.755, 10.325]]]}, {'q_list': ['Q0']......}]

        # 数据提取
        items = []
        for q_name in q_list:
            image_q = image[q_name]

            # x, y = image_q[0], image_q[1]
            value = image_q[2]

            value = np.squeeze(value)
            data = image_q[2]
            data = np.array(data)
            data = cv2.flip(data, 0)

            iq_avg_normalized = convert_complex_map_to_image(iq_avg=data)

            # 获取当前量子比特对应的关键点、类别和配置
            idx = q_list.index(q_name)
            keypoints = result['keypoints_list'][idx] if idx < len(result['keypoints_list']) else []
            class_num = result['class_num_list'][idx] if idx < len(result['class_num_list']) else None
            conf = result['confs'][idx] if idx < len(result['confs']) else None
            
            items.append({
                'iq_avg_normalized': iq_avg_normalized,
                'value': value,
                'keypoints': keypoints,
                'q_name': q_name,
                'class_num': class_num,
                'conf': conf
            })

        # 结果数据（原代码保留）
        # confs = result['confs']
        # class_num_list = result['class_num_list']
        # keypoints_list = result['keypoints_list']

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
            values = item["value"]
            keypoints = item["keypoints"]
            q_name = item["q_name"]
            class_num = item["class_num"]
            conf = item["conf"]
            iq_avg_normalized = item["iq_avg_normalized"]
            
            # 绘制原始图像：使用归一化后的 IQ RGB 图像代替 pcolormesh
            # 使用 extent 将图像映射到 x/y 物理坐标范围，origin='lower' 保持与 pcolormesh 相同的方向
            x_min, x_max = (0, iq_avg_normalized.shape[1])
            y_min, y_max = (0, iq_avg_normalized.shape[0])
            im = ax.imshow(iq_avg_normalized, extent=(x_min, x_max, y_min, y_max), origin='lower', aspect='auto')

            if keypoints:
                sorted_keypoints = sorted(keypoints, key=lambda p: (-p[1], p[0]))
                kp_x = [p[0] for p in sorted_keypoints]
                kp_y = [p[1] for p in sorted_keypoints]
                ax.scatter(kp_x, kp_y, color='red', s=80, marker='*', label='Key Points')
                ax.plot(kp_x, kp_y, 'r--', linewidth=2)
            
            info_text = f"Qubit: {q_name}\n"
            if class_num is not None:
                info_text += f"Class: {class_num}\n"
            if conf is not None:
                info_text += f"Confidence: {conf:.2f}"
            
            ax.text(0.05, 0.95, info_text, transform=ax.transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            ax.set_title('Original Image')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                ax.legend()
        
        # 隐藏多余的子图
        for i in range(num_items, rows * cols):
            axes[i].axis('off')
        
        plt.tight_layout()
        return fig
