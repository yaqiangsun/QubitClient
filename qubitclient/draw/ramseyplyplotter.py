from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class RamseyDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("ramsey")

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

            fig.add_trace(go.Scatter(x=x_raw, y=y_raw, mode='markers',
                                    marker=dict(color='orange', size=7),
                                    name='Data', showlegend=not data_legend), row=row, col=col)
            if not data_legend:
                data_legend = True

            if q_idx < len(fit_data_list):
                y_fit = np.asarray(fit_data_list[q_idx])
                x_fit = x_raw if len(y_fit) == len(x_raw) else np.linspace(x_raw.min(), x_raw.max(), len(y_fit))
                fig.add_trace(go.Scatter(x=x_fit, y=y_fit, mode='lines',
                                        line=dict(color='blue', width=2.5),
                                        name='Fit', showlegend=not fit_legend), row=row, col=col)
                if not fit_legend:
                    fit_legend = True

            if q_idx < len(params_list):
                A, B, freq, phi, T2 = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                txt = f"A={A:.3f}<br>B={B:.3f}<br>freq={freq/1e6:.3f}MHz<br>φ={phi:.3f}<br>T2={T2:.1f}µs<br>R²={r2:.4f}"
                fig.add_annotation(x=x_raw[0], y=max(y_raw)*1.08, text=txt, showarrow=False,
                                  font=dict(size=9), align="left",
                                  bgcolor="rgba(255,255,255,0.8)", row=row, col=col)

            if row == rows:
                fig.update_xaxes(title_text="Time (ns)", row=row, col=col)
            if col == 1:
                fig.update_yaxes(title_text="P(|1>)", row=row, col=col)

        fig.update_layout(height=420*rows, width=540*cols, title_text="Ramsey Oscillation Fit", title_x=0.5)
        return fig