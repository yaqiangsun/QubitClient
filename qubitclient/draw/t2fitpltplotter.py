# src/draw/t2fitpltplotter.py
from .pltplotter import QuantumDataPltPlotter
import matplotlib.pyplot as plt
import numpy as np


class T2FitDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("t2fit")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')   # 统一使用 dict_param

        if not result or not dict_param:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data", ha='center', transform=ax.transAxes)
            return fig

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        n_qubits = len(qubit_names)
        cols = min(3, n_qubits)
        rows = (n_qubits + cols - 1) // cols

        fig = plt.figure(figsize=(5.8 * cols, 4.8 * rows))
        fig.suptitle("T2 Ramsey / Echo Fit", fontsize=14, y=0.96)

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
                if len(y_fit) != len(x_raw):
                    x_fit = np.linspace(x_raw.min(), x_raw.max(), len(y_fit))
                else:
                    x_fit = x_raw
                ax.plot(x_fit, y_fit, '-', color='blue', linewidth=2.2, label='Fit')

            if q_idx < len(params_list):
                A, B, T1, T2, w, phi = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                text = (f"A={A:.3f}\nB={B:.3f}\nT1={T1:.1f}µs\n"
                        f"T2={T2:.1f}µs\nω={w/1e6:.2f}MHz\nφ={phi:.3f}\nR²={r2:.4f}")
                ax.text(0.04, 0.96, text, transform=ax.transAxes,
                        verticalalignment='top', fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9))

            ax.set_title(q_name, fontsize=11, pad=10)
            ax.set_xlabel("Time")
            ax.set_ylabel("Amp")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(fontsize=8, loc='upper right')

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.close(fig)
        return fig