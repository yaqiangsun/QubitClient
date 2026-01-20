from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class RabiCosDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("rabicos")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        if not result or not dict_param:
            fig = go.Figure()
            fig.add_annotation(text="No data", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        if not qubit_names:
            fig = go.Figure()
            fig.add_annotation(text="No qubits", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        cols = min(3, len(qubit_names))
        rows = (len(qubit_names) + cols - 1) // cols

        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=qubit_names,
            vertical_spacing=0.08,
            horizontal_spacing=0.08,
        )

        peaks_list = result.get("peaks", [])
        confs_list = result.get("confs", [])

        show_legend = True
        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1

            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x = np.asarray(item[0])
            y = np.asarray(item[1])

            fig.add_trace(
                go.Scatter(x=x, y=y, mode='lines', name='Signal',
                           line=dict(color='blue'), showlegend=show_legend),
                row=row, col=col
            )
            if show_legend:
                show_legend = False

            if q_idx < len(peaks_list):
                peaks = peaks_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else []
                for p, c in zip(peaks, confs):
                    fig.add_trace(
                        go.Scatter(x=[p, p], y=[y.min(), y.max()],
                                   mode='lines', line=dict(color='red', dash='dash'),
                                   name='Peak', showlegend=(q_idx == 0)),
                        row=row, col=col
                    )
                    fig.add_trace(
                        go.Scatter(x=[p], y=[y.max() * 1.05],
                                   mode='text', text=[f"conf: {c:.3f}"],
                                   textposition="top center",
                                   showlegend=False, textfont=dict(color="red", size=10)),
                        row=row, col=col
                    )

            if row == rows:
                fig.update_xaxes(title_text="Time", row=row, col=col)
            if col == 1:
                fig.update_yaxes(title_text="Amp", row=row, col=col)

        fig.update_layout(
            height=400 * rows,
            width=520 * cols,
            title_text="RabiCos – Peak Detection",
            title_x=0.5,
        )
        return fig