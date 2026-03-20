import numpy as np
from ..pltplotter import QuantumDataPltPlotter


class PowerShiftDataPltPlotter(QuantumDataPltPlotter):

    def __init__(self):
        # 调用父类初始化，指定任务类型
        super().__init__("powershift")

    def plot_result_npy(self, **kwargs):
        """实现基类的抽象方法，绘制powershift结果"""
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

        # 合并所有item的图像到一张图中（使用父类的create_subplots方法）
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
            
            # 绘制原始图像（使用父类的add_2dmap方法）
            im = self.add_2dmap(ax, x, y, np.abs(values), shading_index=0, cmap_index=0)
            fig.colorbar(im, ax=ax)


            keypoints_segments=[]
            if class_num==1:
                keypoints_segments.append(keypoints)
            if class_num==2:
                keypoints_segments.append([keypoints[0],keypoints[1]])
                keypoints_segments.append([keypoints[1],keypoints[2]])
                keypoints_segments.append([keypoints[2],keypoints[3]])
            if class_num==3:
                keypoints_segments.append([keypoints[0],keypoints[1]])
                keypoints_segments.append([keypoints[1],keypoints[2]])
            if class_num==4:
                keypoints_segments.append(keypoints)
            if class_num==5:
                keypoints_segments.append(keypoints)
            # 绘制关键点（使用父类的add_scatter和add_line方法）
            j=0
            for seg in keypoints_segments:

                if seg:
                    sorted_seg = sorted(seg, key=lambda p: (-p[1], p[0]))
                    kp_x = [p[0] for p in sorted_seg]
                    kp_y = [p[1] for p in sorted_seg]

                    # 添加散点
                    self.add_scatter(ax, kp_x, kp_y, marker_index=0, color_index=0)
                    # 添加连线
                    self.add_line(ax, kp_x, kp_y, line_style_index=0, color_index=j)
                j+=1

            
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
                xy=(0, 1),annotation_xytext=(0.05, 0.95),annotation_xycoords="axes fraction",
                annotation_textcoords="axes fraction",
                showarrow=False  # 不显示箭头
            )

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
        

        
        # 调整布局
        fig.tight_layout()
        return fig