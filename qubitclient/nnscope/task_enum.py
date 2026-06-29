from enum import Enum, unique
@unique
class NNTaskName(Enum):
    # S21PEAK = "s21peak"
    # OPTPIPULSE = "optpipulse"
    # RABICOS = "rabicos"
    # S21VSFLUX = "s21vflux"
    # SINGLESHOT = "singleshot"
    # SPECTRUM = "spectrum"
    # T1FIT = "t1fit"
    # T2FIT = "t2fit"
    SPECTRUM2D = "spectrum2dnnscope"
    S21VSFLUX = "s21vfluxnnscope"
    POWERSHIFT = "powershiftnnscope"
    SPECTRUM = "spectrumnnscope"
    S21PEAK = "s21peaknnscope"
    S21PEAKMULTI = "s21peakmultinnscope"