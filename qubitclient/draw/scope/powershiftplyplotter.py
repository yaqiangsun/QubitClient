import numpy as np
import plotly.graph_objects as go
from ..plyplotter import QuantumDataPlyPlotter

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

        # 数据预处理：提取并格式化所有量子比特数据
        items = []
        for q_name in q_list:
            image_q = image[q_name]
            x, y, value = image_q[0], image_q[1], image_q[2]
            value = np.abs(value)
            
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
        if num_items == 0:
            raise ValueError("没有可可视化的数据项")

        # 构建子图标题
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

        # 复用父类创建子图的方法
        fig, rows, cols = self.create_subplots(
            n_plots=num_items,
            titles=subplot_titles
        )

        # 统一颜色条范围：预处理所有value数据
        all_values = np.concatenate([item['value'].flatten() for item in items])
        z_min, z_max = np.min(all_values), np.max(all_values)

        # 遍历数据项绘制子图
        for i, item in enumerate(items):
            row = (i // cols) + 1
            col = (i % cols) + 1
            x = item["x"]
            y = item["y"]
            values = item["value"]
            keypoints = item["keypoints"]

            # 归一化value值以实现统一颜色映射（解决add_2dmap无法传zmin/zmax的问题）
            norm_values = (values - z_min) / (z_max - z_min) if z_max != z_min else values
            
            # 调用父类方法添加热力图
            self.add_2dmap(
                fig=fig,
                z=norm_values,
                x=x,
                y=y,
                row=row,
                col=col,
                showscale=(i == num_items - 1),  # 仅最后一个子图显示颜色条
                colorscale_index=0  # 使用Viridis配色（对应父类color_scale[0]）
            )

            # 关键点绘制
            if keypoints and len(keypoints) > 0:
                keypoints = np.array(keypoints).reshape(-1, 2)
                # 按y从高到低排序关键点
                sorted_keypoints = sorted(keypoints, key=lambda p: (-p[1], p[0]))
                kp_x = [p[0] for p in sorted_keypoints]
                kp_y = [p[1] for p in sorted_keypoints]

                # 调用父类方法添加关键点散点
                self.add_scatter(
                    fig=fig,
                    x=kp_x,
                    y=kp_y,
                    row=row,
                    col=col,
                    color_index=0,  # 红色（对应父类marker_color_palette[0]）
                    marker_index=0,  # 星形标记（对应父类marker_styles[0]）
                    name='Key Points',
                    showlegend=False
                )

                # 关键点连接线（调用父类add_line方法）
                if len(kp_x) > 1:
                    self.add_line(
                        fig=fig,
                        x=kp_x,
                        y=kp_y,
                        row=row,
                        col=col,
                        color_index=0,  # 红色线条
                        line_style_index=1,  # 虚线样式（对应父类line_styles[1]）
                        name='Key Points Line',
                        showlegend=False
                    )

        # 配置坐标轴
        self.configure_axis(fig, rows, cols, xlable="X", ylable="Y")
        
        # 更新整体布局
        self.update_layout(
            fig=fig,
            rows=rows,
            cols=cols,
            title_text="Power Shift Data Visualization",
            title_font=dict(size=16, weight='bold')
        )

        return fig