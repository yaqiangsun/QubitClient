from ..plyplotter import QuantumDataPlyPlotter
import numpy as np

class OptPiPulseDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("optpipulse")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        n_plots = len(qubit_names)
        fig, rows, cols = self.create_subplots(
            n_plots=n_plots,
            titles=qubit_names,
            second_y=False
        )

        params_list = result.get("params", [])
        confs_list  = result.get("confs", [])

        show_wave_legend = True
        show_peak_legend = True

        for q_idx, q_name in enumerate(qubit_names):
            row = (q_idx // cols) + 1
            col = (q_idx % cols) + 1

            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            waveforms = np.asarray(item[0])
            t_axis    = np.asarray(item[1])

            for w_idx, wave in enumerate(waveforms):
                self.add_line(
                    fig,
                    x=t_axis,
                    y=wave,
                    row=row,
                    col=col,
                    color_index=w_idx,
                    line_style_index=0,
                    name="Waveform" if show_wave_legend else None,
                    showlegend=show_wave_legend
                )
                if show_wave_legend:
                    show_wave_legend = False

            if q_idx < len(params_list) and params_list[q_idx]:
                peaks = params_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else [0.0] * len(peaks)

                for p, conf in zip(peaks, confs):
                    idx = np.argmin(np.abs(t_axis - p))
                    px = t_axis[idx]
                    py = waveforms[-1][idx]   

                    self.add_vline(
                        fig, x=px,
                        row=row, col=col,
                        color_index=3,
                        line_style_index=1
                    )

                    self.add_scatter(
                        fig,
                        x=[px],
                        y=[py],
                        row=row,
                        col=col,
                        color_index=0,
                        marker_index=0,
                        name="Peak" if show_peak_legend else None,
                        showlegend=show_peak_legend
                    )
                    if show_peak_legend:
                        show_peak_legend = False

                    self.add_annotation(
                        fig,
                        text=f"x={px:.4f}<br>conf={conf:.3f}",
                        row=row,
                        col=col,
                        x=px,
                        y=py * 1.08,   
                        xref="x",
                        yref="y",
                        showarrow=True,
                        arrowhead=2,
                        ax=10,
                        ay=-30
                    )
                    
            fig.update_xaxes(title_text="X", row=row, col=col)
            fig.update_yaxes(title_text="Amp", row=row, col=col)

        self.update_layout(
            fig,
            rows=rows,
            cols=cols,
            showlegend=True
        )

        return fig