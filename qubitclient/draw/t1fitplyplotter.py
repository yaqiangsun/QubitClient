# src/draw/t1fitplyplotter.py
from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class T1FitDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("t1fit")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        if not result or not dict_param:
            fig = go.Figure()
            fig.add_annotation(text="Missing data", xref="paper", yref="paper",
                               x=0.5, y=0.5, showarrow=False)
            return fig

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        if not image_dict:
            fig = go.Figure()
            fig.add_annotation(text="No image data", xref="paper", yref="paper",
                               x=0.5, y=0.5, showarrow=False)
            return fig

        qubit_names = list(image_dict.keys())
        cols = min(3, len(qubit_names))
        rows = (len(qubit_names) + cols - 1) // cols

        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=qubit_names,
            vertical_spacing=0.08,
            horizontal_spacing=0.08,
        )

        params_list   = result.get("params_list", [])
        r2_list       = result.get("r2_list", [])
        fit_data_list = result.get("fit_data_list", [])

        data_legend = False
        fit_legend  = False

        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1

            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])

            # 原始数据点
            fig.add_trace(
                go.Scatter(x=x_raw, y=y_raw, mode='markers',
                           marker=dict(color='orange', size=6),
                           name='Data', legendgroup='data',
                           showlegend=not data_legend),
                row=row, col=col
            )
            if not data_legend:
                data_legend = True

            # 拟合曲线
            if q_idx < len(fit_data_list):
                fit_y = np.asarray(fit_data_list[q_idx])
                fig.add_trace(
                    go.Scatter(x=x_raw, y=fit_y, mode='lines',
                               line=dict(color='blue', width=2),
                               name='Fit', legendgroup='fit',
                               showlegend=not fit_legend),
                    row=row, col=col
                )
                if not fit_legend:
                    fit_legend = True

            # 参数标注
            if q_idx < len(params_list):
                A, T1, B = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                txt = f"A={A:.3f}<br>T1={T1:.1f}µs<br>B={B:.3f}<br>R²={r2:.3f}"
                fig.add_annotation(
                    x=x_raw[0], y=max(y_raw) * 1.05,
                    text=txt, showarrow=False,
                    font=dict(size=9), align="left",
                    bgcolor="rgba(255,255,255,0.8)", bordercolor="gray",
                    row=row, col=col
                )

            if row == rows:
                fig.update_xaxes(title_text="Time", row=row, col=col)
            if col == 1:
                fig.update_yaxes(title_text="Amp", row=row, col=col)

        fig.update_layout(
            height=420 * rows,
            width=520 * cols,
            title_text="T1-Fit",
            title_x=0.5,
            legend=dict(font=dict(size=10), bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        return fig