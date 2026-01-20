from .pltplotter import QuantumDataPltPlotter
import matplotlib.pyplot as plt
import numpy as np


class RamseyDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("ramsey")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        if not result or not dict_param:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data", ha='center', transform=ax.transAxes)
            plt.close(fig)
            return fig

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get('image', {})
        qubit_names = list(image_dict.keys())
        cols = min(3, len(qubit_names))
        rows = (len(qubit_names) + cols - 1) // cols

        fig = plt.figure(figsize=(5.8 * cols, 4.8 * rows))
        fig.suptitle("Ramsey Oscillation Fit", fontsize=14, y=0.96)

        params_list   = result.get("params_list", [])
        r2_list       = result.get("r2_list", [])
        fit_data_list = result.get("fit_data_list", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = fig.add_subplot(rows, cols, q_idx + 1)
            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])

            ax.plot(x_raw, y_raw, 'o', color='orange', markersize=5, label='Data', alpha=0.8)

            if q_idx < len(fit_data_list):
                y_fit = np.asarray(fit_data_list[q_idx])
                x_fit = x_raw if len(y_fit) == len(x_raw) else np.linspace(x_raw.min(), x_raw.max(), len(y_fit))
                ax.plot(x_fit, y_fit, '-', color='blue', linewidth=2.2, label='Fit')

            if q_idx < len(params_list):
                A, B, freq, phi, T2 = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                text = (f"A={A:.3f}\nB={B:.3f}\nf={freq/1e6:.3f}MHz\n"
                        f"φ={phi:.3f}\nT2={T2:.1f}µs\nR²={r2:.4f}")
                ax.text(0.04, 0.96, text, transform=ax.transAxes, va='top', fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9))

            ax.set_title(q_name, fontsize=11)
            ax.set_xlabel("Time (ns)")
            ax.set_ylabel("P(|1>)")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(fontsize=8)

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.close(fig)
        return fig