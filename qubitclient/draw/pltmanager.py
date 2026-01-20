from typing import Dict, List
from .powershiftnnscopepltplotter import PowershiftNNScopeDataPltPlotter
from .pltplotter import QuantumDataPltPlotter
from .spectrum2dnnscopepltplotter import Spectrum2DNNScopeDataPltPlotter
from .s21vfluxscopepltplotter import S21VfluxScopeDataPltPlotter
from .s21vfluxnnscopepltplotter import S21VfluxNNScopeDataPltPlotter
from .singleshotpltplotter import SingleShotDataPltPlotter
from .spectrum2dscopepltplotter import Spectrum2DScopeDataPltPlotter
from .spectrumpltplotter import SpectrumDataPltPlotter
from .s21peakpltplotter import S21PeakDataPltPlotter

from .optpipulsepltplotter import OptPiPulseDataPltPlotter
from .ramseypltplotter import RamseyDataPltPlotter
from .t1fitpltplotter import T1FitDataPltPlotter
from .t2fitpltplotter import T2FitDataPltPlotter
from .rabicospltplotter import RabiCosDataPltPlotter
from .powershiftpltplotter import PowerShiftDataPltPlotter

class QuantumPlotPltManager:
    def __init__(self):
        self.plotters: Dict[str, QuantumDataPltPlotter] = {}
        self.register_plotters()

    def register_plotters(self):
        self.plotters["spectrum2dnnscope"] = Spectrum2DNNScopeDataPltPlotter()
        self.plotters["s21vfluxnnscope"] = S21VfluxNNScopeDataPltPlotter()
        self.plotters["powershiftnnscope"] = PowershiftNNScopeDataPltPlotter()
        self.plotters["s21vfluxscope"] = S21VfluxScopeDataPltPlotter()
        self.plotters["singleshot"] = SingleShotDataPltPlotter()
        self.plotters["spectrum2dscope"] = Spectrum2DScopeDataPltPlotter()
        self.plotters["spectrum"] = SpectrumDataPltPlotter()
        self.plotters["optpipulse"] = OptPiPulseDataPltPlotter()
        self.plotters["rabicos"] = RabiCosDataPltPlotter()
        self.plotters["t1fit"] = T1FitDataPltPlotter()
        self.plotters["t2fit"] = T2FitDataPltPlotter()
        self.plotters["ramsey"] = RamseyDataPltPlotter()
        self.plotters["s21peak"] = S21PeakDataPltPlotter()
        self.plotters["powershift"] = PowerShiftDataPltPlotter()

    def get_plotter(self, task_type: str) -> QuantumDataPltPlotter:
        if task_type not in self.plotters:
            raise ValueError(f"未找到任务 '{task_type}' 的绘图器")
        return self.plotters[task_type]

    def list_available_tasks(self) -> List[str]:
        return list(self.plotters.keys())

    def plot_quantum_data(self, data_type: str, task_type: str, save_path, **kwargs):
        plotter = self.get_plotter(task_type)
        if data_type=='npy':
            fig = plotter.plot_result_npy(**kwargs)
        if data_type=='npz':
            fig = plotter.plot_result_npz(**kwargs)
        plotter.save_plot(fig,save_path)
        return fig
