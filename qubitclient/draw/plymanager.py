
from typing import Dict, List
from .powershiftnnscopeplyplotter import PowershiftNNScopeDataPlyPlotter
from .plyplotter import QuantumDataPlyPlotter
from .spectrum2dnnscopeplyplotter import Spectrum2DNNScopeDataPlyPlotter
from .s21vfluxscopeplyplotter import S21VfluxScopeDataPlyPlotter
from .s21vfluxnnscopeplyplotter import S21VfluxNNScopeDataPlyPlotter

from .singleshotplyplotter import SingleShotDataPlyPlotter
from .spectrum2dscopeplyplotter import Spectrum2DScopeDataPlyPlotter
from .spectrumplyplotter import SpectrumDataPlyPlotter

from .optpipulseplyplotter import OptPiPulseDataPlyPlotter
from .ramseyplyplotter import RamseyDataPlyPlotter
from .t1fitplyplotter import T1FitDataPlyPlotter
from .t2fitplyplotter import T2FitDataPlyPlotter
from .rabicosplyplotter import RabiCosDataPlyPlotter
from .s21peakplyplotter import S21PeakDataPlyPlotter
from .powershiftplyplotter import PowerShiftDataPlyPlotter

class QuantumPlotPlyManager:


    def __init__(self):
        self.plotters: Dict[str, QuantumDataPlyPlotter] = {}
        self.register_plotters()

    def register_plotters(self):

        self.plotters["spectrum2dnnscope"] = Spectrum2DNNScopeDataPlyPlotter()
        self.plotters["s21vfluxnnscope"] = S21VfluxNNScopeDataPlyPlotter()
        self.plotters["s21vfluxscope"] = S21VfluxScopeDataPlyPlotter()
        self.plotters["powershiftnnscope"] = PowershiftNNScopeDataPlyPlotter()

        self.plotters["singleshot"] = SingleShotDataPlyPlotter()
        self.plotters["spectrum2dscope"] = Spectrum2DScopeDataPlyPlotter()
        self.plotters["spectrum"] = SpectrumDataPlyPlotter()
        self.plotters["optpipulse"] = OptPiPulseDataPlyPlotter()
        self.plotters["rabicos"] = RabiCosDataPlyPlotter()
        self.plotters["t1fit"] = T1FitDataPlyPlotter()
        self.plotters["t2fit"] = T2FitDataPlyPlotter()
        self.plotters["ramsey"] = RamseyDataPlyPlotter()
        self.plotters["s21peak"] = S21PeakDataPlyPlotter()
        self.plotters["powershift"] = PowerShiftDataPlyPlotter()

    def get_plotter(self, task_type: str) -> QuantumDataPlyPlotter:

        if task_type not in self.plotters:
            raise ValueError(f"未找到任务 '{task_type}' 的绘图器")
        return self.plotters[task_type]

    def list_available_tasks(self) -> List[str]:

        return list(self.plotters.keys())

    def plot_quantum_data(self, data_type: str, task_type: str,save_path: str,**kwargs):
        plotter = self.get_plotter(task_type)
        if data_type=='npy':
            fig = plotter.plot_result_npy(**kwargs)
        if data_type=='npz':
            fig = plotter.plot_result_npz(**kwargs)

        plotter.save_plot(fig,save_path)
        return fig
