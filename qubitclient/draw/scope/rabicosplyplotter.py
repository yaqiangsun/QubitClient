from ..plyplotter import QuantumDataPlyPlotter
import numpy as np

class RabiCosDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("rabicos")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        titles = [name for name in qubit_names]

        fig, n_rows, n_cols = self.create_subplots(
            n_plots=len(qubit_names),
            titles=titles,
            second_y=False
        )

        peaks_list = result.get("peaks", [])
        confs_list = result.get("confs", [])

        show_legend_global = True

        for q_idx, q_name in enumerate(qubit_names):
            row = (q_idx // n_cols) + 1
            col = (q_idx % n_cols) + 1

            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x = np.asarray(item[0])          
            y = np.asarray(item[1])          

            self.add_line(
                fig, x=x, y=y,
                row=row, col=col,
                color_index=0,
                line_style_index=0,
                name="Signal",
                showlegend=show_legend_global
            )
            if show_legend_global:
                show_legend_global = False

            if q_idx < len(peaks_list):
                peaks = peaks_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else [0.0] * len(peaks)

                peak_x = []
                peak_y = []
                peak_texts = []

                for peak_time, conf in zip(peaks, confs):
                    idx = np.argmin(np.abs(x - peak_time))
                    px = x[idx]
                    py = y[idx]

                    peak_x.append(px)
                    peak_y.append(py)

                    text_str = f"t={px:.3f}<br>conf={conf:.3f}"
                    peak_texts.append(text_str)

                    self.add_vline(
                        fig, x=px,
                        row=row, col=col,
                        color_index=3,          
                        line_style_index=1      
                    )

                    self.add_annotation(
                        fig,
                        text=text_str,
                        row=row, col=col,
                        x=px, y=py,
                    )

                if peak_x:
                    self.add_scatter(
                        fig,
                        x=peak_x,
                        y=peak_y,
                        row=row,
                        col=col,
                        color_index=0,
                        marker_index=0,
                        name="Peak",
                        showlegend=(q_idx == 0),
                        text=peak_texts,
                        textposition="top center",
                        textfont=dict(
                            size=10,
                            color="darkred"
                        ),
                        texttemplate="%{text}",
                    )
                    
            fig.update_xaxes(title_text="Time", row=row, col=col)
            fig.update_yaxes(title_text="Amp", row=row, col=col)

        self.update_layout(
            fig,
            rows=n_rows,
            cols=n_cols,
            showlegend=True
        )


        return fig