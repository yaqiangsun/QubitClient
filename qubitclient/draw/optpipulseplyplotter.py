from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class OptPiPulseDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("optpipulse")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

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
        cols = min(3, len(qubit_names))
        rows = (len(qubit_names) + cols - 1) // cols

        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=qubit_names,
            vertical_spacing=0.08,
            horizontal_spacing=0.08,
        )

        wave_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                       '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

        params_list = result.get("params", [])
        confs_list  = result.get("confs", [])

        wave_legend_shown = False
        peak_legend_shown = False

        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1

            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            waveforms = np.asarray(item[0])
            x_axis    = np.asarray(item[1])

            for w_idx, wave in enumerate(waveforms):
                fig.add_trace(
                    go.Scatter(x=x_axis, y=wave,
                               mode='lines',
                               line=dict(color=wave_colors[w_idx % len(wave_colors)]),
                               name='wave',
                               legendgroup='wave',
                               showlegend=not wave_legend_shown),
                    row=row, col=col
                )
                if not wave_legend_shown:
                    wave_legend_shown = True

            if q_idx < len(params_list):
                peaks = params_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else []
                for p_idx, (peak, conf) in enumerate(zip(peaks, confs)):
                    show_peak_legend = (not peak_legend_shown) and (p_idx == 0)

                    fig.add_trace(
                        go.Scatter(x=[peak, peak],
                                   y=[waveforms.min(), waveforms.max()],
                                   mode='lines',
                                   line=dict(color='red', width=2, dash='dash'),
                                   name='peak',
                                   legendgroup='peak',
                                   showlegend=show_peak_legend),
                        row=row, col=col
                    )
                    if not peak_legend_shown:
                        peak_legend_shown = True

                    fig.add_trace(
                        go.Scatter(x=[peak],
                                   y=[waveforms.max() * 1.08],
                                   mode='text',
                                   text=[f"x={peak:.4f}<br>conf:{conf:.3f}"],
                                   textposition="top center",
                                   showlegend=False,
                                   textfont=dict(size=10, color="red")),
                        row=row, col=col
                    )

            if row == rows:
                fig.update_xaxes(title_text="Time", row=row, col=col)
            if col == 1:
                fig.update_yaxes(title_text="Amp", row=row, col=col)

        fig.update_layout(
            height=400 * rows,
            width=520 * cols,
            title_text="Opt-Pi-Pulse",
            title_x=0.5,
            legend=dict(font=dict(size=10), bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        return fig