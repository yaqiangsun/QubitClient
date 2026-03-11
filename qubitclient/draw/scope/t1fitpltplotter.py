from ..pltplotter import QuantumDataPltPlotter
import numpy as np


class T1FitDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("t1fit")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, axes, rows, cols = self.create_subplots(len(qubit_names))
        axs = axes.flatten()

        params_list   = result.get("params_list", [])
        r2_list       = result.get("r2_list", [])
        fit_data_list = result.get("fit_data_list", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict[q_name]

            if not isinstance(item, (list, tuple)) or len(item) < 2:
                ax.axis('off')
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])

            # 绘制原始数据（散点）
            data_scatter = self.add_scatter(
                ax,
                x_raw,
                y_raw,
                label="Data",
                marker_index=1,           # 'o'
                color_index=6,            # 橙色
                alpha=0.7
            )

            has_fit = False
            fit_line = None

            if (q_idx < len(fit_data_list) and 
                fit_data_list[q_idx] and                  # 非空（不是None也不是[]）
                len(fit_data_list[q_idx]) == len(x_raw)): # 长度必须匹配

                fit_y = np.asarray(fit_data_list[q_idx])
                fit_line, _ = self.add_line(
                    ax,
                    x_raw,
                    fit_y,
                    label="Fit",
                    color_index=0,
                    line_style_index=0
                )
                has_fit = True

            # 构建当前子图的图例 handles 和 labels
            legend_handles = [data_scatter]
            legend_labels = ["Data"]

            if has_fit and fit_line is not None:
                legend_handles.append(fit_line[0])
                legend_labels.append("Fit")

            # 添加图例（每个子图独立）
            if legend_handles:
                self.add_legend(
                    ax=ax,
                    handles=legend_handles,
                    labels=legend_labels,
                )

            # 添加拟合参数文本（左上角，axes fraction 坐标）
            if q_idx < len(params_list) and params_list[q_idx]:
                A, T1, B = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0

                text_str = (
                    f"A  = {A:.3f}\n"
                    f"T₁ = {T1*1e6:.1f} µs\n"
                    f"B  = {B:.3f}\n"
                    f"R² = {r2:.3f}"
                )

                self.add_annotation(
                    ax,
                    text_str,
                    xy=(0, 1),                 
                    annotation_xycoords="axes fraction",
                    annotation_textcoords="axes fraction",
                    annotation_xytext=(0, 1),
                    color_index=0,
                    showarrow=False,
                    ha='left',                      # 文字左对齐
                    va='top'                      # 文字顶部对齐
                )

            # 设置标题和坐标轴标签
            xlabel = "Time"
            ylabel = "Amp"
            self.configure_axis(
                ax,
                title=q_name,               
                xlabel=xlabel,
                ylabel=ylabel
            )

        fig.tight_layout()
        return fig