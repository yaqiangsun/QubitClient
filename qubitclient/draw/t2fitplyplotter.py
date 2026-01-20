# src/draw/t2fitplyplotter.py
from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class T2FitDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("t2fit")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')   # 统一使用 dict_param

        if not result or not dict_param:
            fig = go.Figure()
            fig.add_annotation(text="Missing data", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        if not image_dict:
            fig = go.Figure()
            fig.add_annotation(text="No image data", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        qubit_names = list(image_dict.keys())
        n_qubits = len(qubit_names)
        cols = min(3, n_qubits)
        rows = (n_qubits + cols - 1) // cols

        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f"{q}" for q in qubit_names],
            vertical_spacing=0.09,
            horizontal_spacing=0.09,
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

            fig.add_trace(go.Scatter(
                x=x_raw, y=y_raw,
                mode='markers',
                marker=dict(color='orange', size=7),
                name='Data', legendgroup='data',
                showlegend=not data_legend
            ), row=row, col=col)
            if not data_legend:
                data_legend = True

            if q_idx < len(fit_data_list):
                y_fit = np.asarray(fit_data_list[q_idx])
                if len(y_fit) != len(x_raw):
                    x_fit = np.linspace(x_raw.min(), x_raw.max(), len(y_fit))
                else:
                    x_fit = x_raw

                fig.add_trace(go.Scatter(
                    x=x_fit, y=y_fit,
                    mode='lines',
                    line=dict(color='blue', width=2.5),
                    name='Fit', legendgroup='fit',
                    showlegend=not fit_legend
                ), row=row, col=col)
                if not fit_legend:
                    fit_legend = True

            if q_idx < len(params_list):
                A, B, T1, T2, w, phi = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                txt = (f"A={A:.3f}<br>B={B:.3f}<br>T1={T1:.1f}µs<br>"
                       f"T2={T2:.1f}µs<br>ω={w/1e6:.2f}MHz<br>φ={phi:.3f}<br>R²={r2:.4f}")
                fig.add_annotation(
                    x=x_raw[0], y=max(y_raw) * 1.08,
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
            height=440 * rows,
            width=540 * cols,
            title_text="T2 Ramsey / Echo Fit",
            title_x=0.5,
            legend=dict(font=dict(size=10)),
            margin=dict(l=60, r=60, t=90, b=60)
        )
        return fig