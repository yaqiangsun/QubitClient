from typing import Dict, List
from .pltplotter import QuantumDataPltPlotter

from qubitclient.draw.nnscope.powershiftnnscopepltplotter import PowershiftNNScopeDataPltPlotter
from qubitclient.draw.nnscope.spectrumnnscopepltplotter import SpectrumNNscopeDataPltPlotter
from qubitclient.draw.nnscope.spectrum2dnnscopepltplotter import Spectrum2DNNScopeDataPltPlotter
from qubitclient.draw.scope.s21vfluxscopepltplotter import S21VfluxScopeDataPltPlotter
from qubitclient.draw.nnscope.s21vfluxnnscopepltplotter import S21VfluxNNScopeDataPltPlotter
from qubitclient.draw.scope.singleshotpltplotter import SingleShotDataPltPlotter
from qubitclient.draw.scope.spectrum2dscopepltplotter import Spectrum2DScopeDataPltPlotter
from qubitclient.draw.scope.spectrumpltplotter import SpectrumDataPltPlotter
from qubitclient.draw.scope.s21peakpltplotter import S21PeakDataPltPlotter

from qubitclient.draw.scope.optpipulsepltplotter import OptPiPulseDataPltPlotter
from qubitclient.draw.scope.ramseypltplotter import RamseyDataPltPlotter
from qubitclient.draw.scope.t1fitpltplotter import T1FitDataPltPlotter
from qubitclient.draw.scope.t2fitpltplotter import T2FitDataPltPlotter
from qubitclient.draw.scope.rabicospltplotter import RabiCosDataPltPlotter
from qubitclient.draw.scope.powershiftpltplotter import PowerShiftDataPltPlotter
from qubitclient.draw.scope.dragpltplotter import DragDataPltPlotter


class QuantumPlotPltManager:
    def __init__(self):
        self.plotters: Dict[str, QuantumDataPltPlotter] = {}
        self.register_plotters()

    def register_plotters(self):
        self.plotters["spectrum2dnnscope"] = Spectrum2DNNScopeDataPltPlotter()
        self.plotters["s21vfluxnnscope"] = S21VfluxNNScopeDataPltPlotter()
        self.plotters["powershiftnnscope"] = PowershiftNNScopeDataPltPlotter()
        self.plotters["spectrumnnscope"] = SpectrumNNscopeDataPltPlotter()
        
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
        self.plotters["drag"] = DragDataPltPlotter()

    def get_plotter(self, task_type: str) -> QuantumDataPltPlotter:
        if task_type not in self.plotters:
            raise ValueError(f"未找到任务 '{task_type}' 的绘图器")
        return self.plotters[task_type]

    def list_available_tasks(self) -> List[str]:
        return list(self.plotters.keys())

    def plot_quantum_data(self, task_type: str, save_path:str=None, data_type: str=None, **kwargs):
        plotter = self.get_plotter(task_type)
        if data_type=='npz':
            fig = plotter.plot_result_npz(**kwargs)
        else: # data_type=='npy':
            fig = plotter.plot_result_npy(**kwargs)

        if save_path:
            plotter.save_plot(fig,save_path)
        return fig
