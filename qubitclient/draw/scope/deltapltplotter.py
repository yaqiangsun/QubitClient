from ..pltplotter import QuantumDataPltPlotter
import numpy as np


class DeltaDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("delta")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, axes, n_rows, n_cols = self.create_subplots(len(qubit_names))
        axs = axes.flatten()

        params_list = result.get("params", [])
        confs_list  = result.get("confs", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                ax.axis('off')
                continue

            waveforms = np.asarray(item[0])
            t_axis    = np.asarray(item[1])

            legend_handles = []
            legend_labels = []

            # 绘制波形
            if len(waveforms) > 0:
                first_wave_line, _ = self.add_line(
                    ax,
                    x=t_axis,
                    y=waveforms[0],
                    label="Waveform",
                    color_index=0,
                    line_style_index=0,
                )
                legend_handles.append(first_wave_line[0])
                legend_labels.append("Waveform")

                for w_idx in range(1, len(waveforms)):
                    self.add_line(
                        ax,
                        x=t_axis,
                        y=waveforms[w_idx],
                        color_index=w_idx % len(self.style.line_colors),
                        line_style_index=0,
                    )

            # 绘制 Delta 峰值（横坐标需 ×1e6）
            if q_idx < len(params_list) and params_list[q_idx]:
                peaks = params_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else [0.0] * len(peaks)

                if peaks:
                    first_peak_x = peaks[0] * 1e6                     # ×1e6
                    idx = np.argmin(np.abs(t_axis - first_peak_x))
                    px = t_axis[idx]
                    py = waveforms[-1][idx] if len(waveforms) > 0 else 0.0

                    self.add_vline(ax, px)
                    scatter = self.add_scatter(
                        ax,
                        x=[px],
                        y=[py],
                        marker_index=1,
                        color_index=0,
                    )

                    legend_handles.append(scatter)
                    legend_labels.append("Delta Peak")

                    for p, conf in zip(peaks, confs):
                        px = p * 1e6                                 # ×1e6
                        idx = np.argmin(np.abs(t_axis - px))
                        py = waveforms[-1][idx] if len(waveforms) > 0 else 0.0

                        self.add_vline(ax, px)
                        self.add_scatter(
                            ax,
                            x=[px],
                            y=[py],
                            marker_index=1,
                            color_index=0,
                        )

                        text_str = f"x = {px}\nconf = {conf:.3f}"
                        self.add_annotation(
                            ax,
                            text_str,
                            xy=(px, py),
                            annotation_xytext=(10, 10),
                            color_index=0
                        )

            if legend_handles:
                self.add_legend(
                    ax=ax,
                    handles=legend_handles,
                    labels=legend_labels,
                )

            xlabel = "X"
            ylabel = "Amp"
            self.configure_axis(ax, title=q_name, xlabel=xlabel, ylabel=ylabel)

        fig.tight_layout()
        return fig