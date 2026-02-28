# src/draw/t2fitplyplotter.py
from ..plyplotter import QuantumDataPlyPlotter
import numpy as np


class T2FitDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("t2fit")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        n_qubits = len(qubit_names)

        fig, rows, cols = self.create_subplots(
            n_plots=n_qubits,
            titles=qubit_names,
            second_y=False
        )

        params_list   = result.get("params_list",   [])
        r2_list       = result.get("r2_list",       [])
        fit_data_list = result.get("fit_data_list", [])

        show_data_legend = True
        show_fit_legend  = True

        for q_idx, q_name in enumerate(qubit_names):
            row = (q_idx // cols) + 1
            col = (q_idx % cols) + 1

            item = image_dict.get(q_name)
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])

            # 原始数据散点
            self.add_scatter(
                fig,
                x=x_raw,
                y=y_raw,
                row=row, col=col,
                color_index=6,             # 橙色
                marker_index=0,            # circle
                name="Data" if show_data_legend else None,
                showlegend=show_data_legend,
                opacity=0.7
            )
            if show_data_legend:
                show_data_legend = False

            # 拟合曲线
            if q_idx < len(fit_data_list) and fit_data_list[q_idx] is not None:
                fit_y = np.asarray(fit_data_list[q_idx])

                x_plot = x_raw
                if len(fit_y) != len(x_raw):
                    x_plot = np.linspace(x_raw.min(), x_raw.max(), len(fit_y))

                self.add_line(
                    fig,
                    x=x_plot,
                    y=fit_y,
                    row=row, col=col,
                    color_index=0,             # 蓝色
                    line_style_index=0,
                    name="Fit" if show_fit_legend else None,
                    showlegend=show_fit_legend
                )
                if show_fit_legend:
                    show_fit_legend = False

            # 参数文本（左上角）
            if q_idx < len(params_list) and params_list[q_idx]:
                A, B, T1, T2, w, phi = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0

                text = (
                    f"A   = {A:.3f}<br>"
                    f"B   = {B:.3f}<br>"
                    f"T₁  = {T1:.1f} µs<br>"
                    f"T₂  = {T2:.1f} µs<br>"
                    f"ω   = {w/1e6:.2f} MHz<br>"
                    f"φ   = {phi:.3f}<br>"
                    f"R²  = {r2:.3f}"
                )

                self.add_annotation(
                    fig,
                    text=text,
                    row=row, col=col,
                    x=x_raw.min(),
                    y=max(y_raw) * 1.06 if len(y_raw) > 0 else 1.0,
                    xref="x", yref="y",
                    showarrow=False
                )

            # 坐标轴标签
            fig.update_xaxes(title_text="Time", row=row, col=col)
            fig.update_yaxes(title_text="Amp", row=row, col=col)

        self.update_layout(
            fig,
            rows=rows,
            cols=cols,
            showlegend=True
        )

        return fig