from enum import Enum, unique
# @unique
class TaskName(Enum):
    S21PEAK = "s21peak"
    S21PEAKMULTI = "s21peakmulti"
    OPTPIPULSE = "optpipulse"
    RAMSEY = "ramsey"
    RABICOS = "rabicos"
    S21VSFLUX = "s21vsfluxscope"
    SINGLESHOT = "singleshot"
    SPECTRUM = "spectrum"
    T1FIT = "t1fit"
    T2FIT = "t2fit"
    SPECTRUM2D = "spectrum2dscope"
    POWERSHIFT = "powershift"
    DRAG = "drag"
    RB = "rb"
    DELTA = "delta"
    XEB = "xeb"
    T12DFIT = "t12dfit"
    ############################
    # additonal tasks
    SPINECHO = "spinecho"
    TIMINGXYZ = "xyz_timing"
    OPTREADFREQ = "optreadfreq"
    # reflection
    RAMSEY_T2 = "t2fit"
    SPINECHO_T2 = "spinecho"
    SETPIALPHA = "optpipulse"