from .pltplotter import QuantumDataPltPlotter
import matplotlib.pyplot as plt
import numpy as np


class OptPiPulseDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("optpipulse")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')      

        if not result or not dict_param:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data", ha='center', transform=ax.transAxes)
            plt.close(fig)
            return fig

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        if not qubit_names:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No qubits", ha='center', transform=ax.transAxes)
            plt.close(fig)
            return fig

        cols = min(3, len(qubit_names))
        rows = (len(qubit_names) + cols - 1) // cols

        fig = plt.figure(figsize=(5.8 * cols, 4.5 * rows))
        fig.suptitle("Opt-Pi-Pulse", fontsize=14, y=0.96)

        wave_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                       '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

        params_list = result.get("params", [])
        confs_list  = result.get("confs", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = fig.add_subplot(rows, cols, q_idx + 1)
            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            waveforms = np.asarray(item[0])
            x_axis    = np.asarray(item[1])

            for w_idx, wave in enumerate(waveforms):
                ax.plot(x_axis, wave,
                        color=wave_colors[w_idx % len(wave_colors)],
                        linewidth=1.2)

            if q_idx < len(params_list):
                peaks = params_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else []
                for p_idx, (peak, conf) in enumerate(zip(peaks, confs)):
                    ax.axvline(peak, color='red', linestyle='--', linewidth=1.8)
                    ax.annotate(f"x={peak:.4f}\nconf:{conf:.3f}",
                                (peak, ax.get_ylim()[1]),
                                xytext=(0, 8), textcoords='offset points',
                                ha='center', va='bottom',
                                fontsize=8, color='red',
                                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))

            ax.set_title(q_name, fontsize=11, pad=10)
            ax.set_xlabel("Time")
            ax.set_ylabel("Amp")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(['wave', 'peak'], fontsize=8, loc='upper right', framealpha=0.9)

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.close(fig)
        return fig