import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .plyplotter import QuantumDataPlyPlotter

class PowerShiftDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("powershift")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item()
        image = data["image"]
        q_list = list(image.keys())
        if not q_list:
            raise ValueError("没有找到量子比特数据")

        items = []
        for q_name in q_list:
            image_q = image[q_name]
            x, y, value = image_q[0], image_q[1], image_q[2]
            
            idx = q_list.index(q_name)
            keypoints = result['keypoints_list'][idx] if idx < len(result['keypoints_list']) else []
            class_num = result['class_num_list'][idx] if idx < len(result['class_num_list']) else None
            conf = result['confs'][idx] if idx < len(result['confs']) else None
            
            # 数据格式处理
            x = np.squeeze(x)
            y = np.squeeze(y)
            value = np.squeeze(value)
            
            # 热力图网格与坐标匹配处理
            if value.shape[0] == len(y) - 1 and value.shape[1] == len(x) - 1:
                pass
            else:
                value = value[:len(y), :len(x)]
            
            items.append({
                'x': x,
                'y': y,
                'value': value,
                'keypoints': keypoints,
                'q_name': q_name,
                'class_num': class_num,
                'conf': conf
            })

        num_items = len(items)
        max_cols = 4  # 保持每行4个子图，平衡宽度和可读性
        rows = (num_items + max_cols - 1) // max_cols
        cols = min(num_items, max_cols)

        # 1. 增大子图基础尺寸，按数量动态调整（优先保证显示完整）
        base_size = 320  # 基础尺寸从250提升到320，显著增大子图
        if num_items > 30:
            base_size = 280  # 30个以上子图适当缩小，但仍比之前200大
        elif num_items > 15:
            base_size = 300  # 15-30个子图微调
        fig_height = base_size * rows
        fig_width = base_size * cols

        # 2. 调整间距：增大垂直/水平间距，避免内容挤压
        vertical_spacing = 0.08  # 从0.02提升到0.06，增加上下子图间隙
        horizontal_spacing = 0.08  # 从0.03提升到0.08，增加左右子图间隙
        # 子图数量过多时，间距适度缩小（但仍大于之前的最小间距）
        if num_items > 35:
            vertical_spacing = 0.06
            horizontal_spacing = 0.06
        
        subplot_titles = []
        for item in items:
            q_name = item['q_name']
            class_num = item['class_num']
            conf = item['conf']
            
            # 构建标题基础部分
            title_parts = [f"Qubit: {q_name}"]
            
            # 添加class信息（如果存在）
            if class_num is not None:
                title_parts.append(f"class: {class_num}")
            
            # 添加conf信息（如果存在，保留两位小数）
            if conf is not None:
                title_parts.append(f"conf: {conf:.2f}")
            
            # 拼接所有部分为最终标题
            subplot_titles.append("_".join(title_parts))

        # 创建子图
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=subplot_titles,
            vertical_spacing=vertical_spacing,
            horizontal_spacing=horizontal_spacing,
            shared_yaxes=False,
            shared_xaxes=False
        )

        # 统一颜色条范围
        all_values = np.concatenate([item['value'].flatten() for item in items])
        z_min, z_max = np.min(all_values), np.max(all_values)

        for i, item in enumerate(items):
            row = (i // cols) + 1
            col = (i % cols) + 1
            x = item["x"]
            y = item["y"]
            values = item["value"]
            keypoints = item["keypoints"]
            q_name = item["q_name"]
            class_num = item["class_num"]
            conf = item["conf"]

            # 绘制热力图（保持颜色条配置正确）
            heatmap = go.Heatmap(
                z=values,
                x=x,
                y=y,
                zmin=z_min,
                zmax=z_max,
                colorscale='Viridis',
                colorbar=dict(
                    thickness=12,  # 增大颜色条厚度，提升可读性
                    title=dict(
                        text="Value",
                        side="right",
                        font=dict(size=10)  # 颜色条标题字体
                    )
                ) if i == (num_items - 1) else None,
                showscale=(i == num_items - 1),
                transpose=False
            )
            fig.add_trace(heatmap, row=row, col=col)

            # 关键点连线按y从高到低排序
            if keypoints and len(keypoints) > 0:
                keypoints = np.array(keypoints).reshape(-1, 2)
                sorted_keypoints = sorted(keypoints, key=lambda p: (-p[1], p[0]))
                kp_x = [p[0] for p in sorted_keypoints]
                kp_y = [p[1] for p in sorted_keypoints]

                # 关键点散点（增大尺寸，避免看不清）
                scatter = go.Scatter(
                    x=kp_x, y=kp_y,
                    mode='markers',
                    marker=dict(color='red', size=11, symbol='star', line=dict(width=1.2, color='white')),
                    name='Key Points',
                    showlegend=False  
                )
                fig.add_trace(scatter, row=row, col=col)

                # 关键点连接线（加粗线条）
                if len(kp_x) > 1:
                    line = go.Scatter(
                        x=kp_x, y=kp_y,
                        mode='lines',
                        line=dict(color='red', dash='dash', width=1.8),
                        showlegend=False
                    )
                    fig.add_trace(line, row=row, col=col)

            # 4. 坐标轴优化：增大字体，避免刻度/标题看不清
            fig.update_xaxes(
                title_text="X",
                row=row, col=col,
                range=[np.min(x), np.max(x)],
                title_font=dict(size=11),  # 轴标题字体增大
                tickfont=dict(size=9),     # 刻度字体增大
                ticklen=4  # 增大刻度长度，提升可读性
            )
            fig.update_yaxes(
                title_text="Y",
                row=row, col=col,
                range=[np.min(y), np.max(y)],
                title_font=dict(size=11),
                tickfont=dict(size=9),
                ticklen=4
            )

        # 整体布局优化：增大边距，避免边缘内容被截断
        fig.update_layout(
            height=fig_height,
            width=fig_width,
            title_text="Power Shift Data Visualization",
            title_font=dict(size=16, weight='bold'),
            margin=dict(l=40, r=60, t=60, b=40)  # 增大右/上/左/下边距，适配颜色条和标题
        )

        return fig