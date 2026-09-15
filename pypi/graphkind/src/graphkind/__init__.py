"""GraphKind — motor de descubrimiento estructural (universos de observación).

API de instrumento: `GraphKind` (clase) + `GraphKindResult`.

Módulos (todos stdlib, salvo `verificaciones*` que usan numpy):

- `wl`: color refinement (1-WL), k-FWL (≡ (k+1)-WL), separación, T4.
- `universos`: la ley de T4 (clasificación trivial/dual/local + oráculo).
- `multicapa`: refinamiento conjunto y las tres dualidades (ley de canales).
- `hipergrafo`: k-uniforme y aridades mezcladas; el dual por aridad.
- `individualizacion`: IR_k (peor/multiset).

Paper / datos: DOI 10.5281/zenodo.22747350 (CC-BY-4.0).
"""

from . import (  # noqa: F401
    graph6,
    hipergrafo,
    individualizacion,
    multicapa,
    universos,
    wl,
)
from .api import OBSERVADORES, GraphKind, GraphKindResult  # noqa: F401
from .wl import (  # noqa: F401
    adj_from_edges,
    complement,
    edges_from_adj,
    firma,
    h,
    kfwl_colors,
    particion,
    perfil,
    separa,
    t4,
    wl1_colors,
)
from .universos import t4_garantizado  # noqa: F401

__version__ = "0.2.2"
DOI = "10.5281/zenodo.22747350"

def __getattr__(name):
    """`graphkind.fast` es lazy: requiere numpy (extra `fast`)."""
    if name == "fast":
        import importlib
        try:
            return importlib.import_module("graphkind.fast")
        except ImportError as exc:  # pragma: no cover
            raise AttributeError(
                "graphkind.fast requiere numpy (pip install graphkind[fast])"
            ) from exc
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "DOI",
    "OBSERVADORES",
    "GraphKind",
    "GraphKindResult",
    "__version__",
    "adj_from_edges",
    "complement",
    "edges_from_adj",
    "firma",
    "graph6",
    "h",
    "hipergrafo",
    "individualizacion",
    "kfwl_colors",
    "multicapa",
    "particion",
    "perfil",
    "separa",
    "t4",
    "t4_garantizado",
    "universos",
    "wl",
    "wl1_colors",
]
