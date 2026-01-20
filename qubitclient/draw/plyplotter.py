
from abc import ABC, abstractmethod
import json
import os

class QuantumDataPlyPlotter(ABC):


    def __init__(self, task_type: str):
        self.task_type = task_type
    @abstractmethod
    def plot_result_npy(self, **kwargs):
        pass
    def plot_result_npz(self, **kwargs):
        pass

    def save_plot(self, fig,  save_path: str):
        directory = os.path.dirname(save_path)
        if os.path.exists(directory):
            fig.write_html(save_path)   # save_path  最中存储路径 “./tmp/client/result_s21peak_tmp***.html”
        return fig