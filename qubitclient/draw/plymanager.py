
from typing import Dict, List

from qubitclient.draw.nnscope.powershiftnnscopeplyplotter import PowershiftNNScopeDataPlyPlotter
from qubitclient.draw.nnscope.spectrumnnscopeplyplotter import SpectrumNNScopeDataPlyPlotter
from .plyplotter import QuantumDataPlyPlotter
from qubitclient.draw.nnscope.spectrum2dnnscopeplyplotter import Spectrum2DNNScopeDataPlyPlotter
from qubitclient.draw.scope.s21vfluxscopeplyplotter import S21VfluxScopeDataPlyPlotter
from qubitclient.draw.nnscope.s21vfluxnnscopeplyplotter import S21VfluxNNScopeDataPlyPlotter

from qubitclient.draw.scope.singleshotplyplotter import SingleShotDataPlyPlotter
from qubitclient.draw.scope.spectrum2dscopeplyplotter import Spectrum2DScopeDataPlyPlotter
from qubitclient.draw.scope.spectrumplyplotter import SpectrumDataPlyPlotter

from qubitclient.draw.scope.optpipulseplyplotter import OptPiPulseDataPlyPlotter
from qubitclient.draw.scope.ramseyplyplotter import RamseyDataPlyPlotter
from qubitclient.draw.scope.t1fitplyplotter import T1FitDataPlyPlotter
from qubitclient.draw.scope.t2fitplyplotter import T2FitDataPlyPlotter
from qubitclient.draw.scope.rabicosplyplotter import RabiCosDataPlyPlotter
from qubitclient.draw.scope.s21peakplyplotter import S21PeakDataPlyPlotter
from qubitclient.draw.scope.powershiftplyplotter import PowerShiftDataPlyPlotter
from qubitclient.draw.scope.dragplyplotter import DragDataPlyPlotter

class QuantumPlotPlyManager:


    def __init__(self):
        self.plotters: Dict[str, QuantumDataPlyPlotter] = {}
        self.register_plotters()

    def register_plotters(self):

        self.plotters["spectrum2dnnscope"] = Spectrum2DNNScopeDataPlyPlotter()
        self.plotters["s21vfluxnnscope"] = S21VfluxNNScopeDataPlyPlotter()
        self.plotters["s21vfluxscope"] = S21VfluxScopeDataPlyPlotter()
        self.plotters["powershiftnnscope"] = PowershiftNNScopeDataPlyPlotter()
        self.plotters["spectrumnnscope"] = SpectrumNNScopeDataPlyPlotter()

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
        self.plotters["drag"] = DragDataPlyPlotter()

    def get_plotter(self, task_type: str) -> QuantumDataPlyPlotter:

        if task_type not in self.plotters:
            raise ValueError(f"未找到任务 '{task_type}' 的绘图器")
        return self.plotters[task_type]

    def list_available_tasks(self) -> List[str]:

        return list(self.plotters.keys())

    def plot_quantum_data(self, task_type: str,save_path: str=None, data_type: str=None,**kwargs):
        plotter = self.get_plotter(task_type)

        if data_type=='npz':
            fig = plotter.plot_result_npz(**kwargs)
        else: #  data_type=='npy':
            fig = plotter.plot_result_npy(**kwargs)

        if save_path:
            plotter.save_plot(fig,save_path)
        return fig
