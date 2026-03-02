import numpy as np
import matplotlib.pyplot as plt
from ..pltplotter import QuantumDataPltPlotter
import cv2
import logging


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
        # logging.warning("plt----------- kwargs: %s", kwargs)
        result = kwargs.get('result')
        data_ndarray = kwargs.get('dict_param')
        data = data_ndarray.item()

        powershift_labels = {0:"cos_light", 1:"cos_dark", 2:"line_light", 3:"line_dark"}

        image = data["image"]
        q_list = list(image.keys())

        # 数据提取
        items = []
        for q_name in q_list:
            image_q = image[q_name]
            x, y, value = image_q[0], image_q[1], image_q[2]

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
                'x': x,
                'y': y,
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
        
        # 使用父类方法创建子图布局（自动适配style配置）
        fig, axes, rows, cols = self.create_subplots(num_items)
        axs = axes.flatten()

        # 为每个item绘制内容
        for i, item in enumerate(items):
            ax = axs[i]
            x = item["x"]
            y = item["y"]
            values = item["value"]
            keypoints = item["keypoints"]
            q_name = item["q_name"]
            class_num = item["class_num"]
            conf = item["conf"]
            iq_avg_normalized = item["iq_avg_normalized"]
            height = iq_avg_normalized.shape[0]
            
            # x范围与关键点不一致
            # im = self.add_2dmap(ax, x, y, values, shading_index=0, cmap_index=0)
            # fig.colorbar(im, ax=ax)

            x_min, x_max = (0, iq_avg_normalized.shape[1])
            y_min, y_max = (0, iq_avg_normalized.shape[0])
            im = ax.imshow(iq_avg_normalized, extent=(x_min, x_max, y_min, y_max), origin='upper', aspect='auto')

            
            # 绘制关键点（使用父类的add_scatter和add_line方法）
            if keypoints:
                sorted_keypoints = sorted(keypoints, key=lambda p: (-p[1], p[0]))
                kp_x = [p[0] for p in sorted_keypoints]
                # kp_y = [p[1] for p in sorted_keypoints]
                kp_y = [height - p[1] for p in sorted_keypoints]
                
                # 添加散点
                self.add_scatter(ax, kp_x, kp_y, label='Key Points', marker_index=0, color_index=0)
                # 添加连线
                self.add_line(ax, kp_x, kp_y, label='Key Line', line_style_index=0, color_index=0)
            
            # 组装信息文本
            info_text = f"Qubit: {q_name}\n"
            if class_num is not None:
                info_text += f"Class: {class_num}\n"
            if conf is not None:
                # 格式化置信度为两位小数
                info_text += f"Confidence: {conf:.2f}"
            
            # 添加文本注释（使用父类的add_annotation方法）
            self.add_annotation(
                ax, 
                info_text, 
                xy=(0.05, 0.95),
                annotation_textcoords="axes fraction",  # 基于轴坐标的文本位置
                annotation_xytext=(0, 0),
                showarrow=False  # 不显示箭头
            )
            
            # 配置坐标轴（使用父类的configure_axis方法）
            self.configure_axis(
                ax,
                title=f"{q_name}",
                xlabel="X",
                ylabel="Y",
                show_legend=True
            )
            
            # 添加图例（使用父类的add_legend方法）
            handles, labels = ax.get_legend_handles_labels()
            self.add_legend(ax, handles, labels)
        
        # 隐藏多余的子图
        for i in range(num_items, len(axs)):
            axs[i].axis('off')
        
        # 调整布局
        fig.tight_layout()
        return fig