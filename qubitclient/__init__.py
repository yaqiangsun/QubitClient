from importlib.metadata import version
try:
    __version__ = version("qubitclient")
except Exception:
    __version__ = "unknown"

from .nnscope.nnscope_api.curve.curve_type import CurveType  # noqa: F401
from .scope.scope import QubitScopeClient
from .nnscope.nnscope import QubitNNScopeClient
from .scope.task import TaskName
from .nnscope.task import NNTaskName
from .wrapper_handler import handle_exceptions, control_api_execution

__all__ = [
    "__version__",
    "QubitScopeClient",
    "QubitNNScopeClient",
    "TaskName",
    "NNTaskName",
    "CurveType",
    "handle_exceptions",
    "control_api_execution",
]