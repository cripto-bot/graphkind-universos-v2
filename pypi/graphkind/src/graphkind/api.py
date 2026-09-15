"""API de instrumento: `GraphKind` + `GraphKindResult`.

Fachada chica y estable sobre el motor existente (módulos `wl`,
`universos`, `multicapa`, `hipergrafo`, `individualizacion`). La idea es
consumir el descubridor como una primitiva, no como un framework:

    from graphkind import GraphKind

    gk = GraphKind(observer="wl")
    fp = gk.transform(graph)        # fingerprint estructural
    fp.signature                    # comparable / hasheable
    fp.kinds, fp.partition, fp.profile, fp.rounds, fp.observer

La firma coincide exactamente con la de `graphkind-harness` (una sola
fuente de verdad). Nada de esto cambia los resultados del motor.
"""

from __future__ import annotations

from dataclasses import dataclass, fields

from . import hipergrafo, individualizacion, multicapa, universos, wl
from .graph6 import from_graph6

#: observadores registrados (mismos nombres que el harness y los freezes)
OBSERVADORES = ("wl", "kw2", "kw3", "ir1", "ir2")

__all__ = ["GraphKind", "GraphKindResult", "OBSERVADORES"]


@dataclass(frozen=True)
class GraphKindResult:
    """Resultado estructural de un observador sobre un grafo.

    - `signature`: la firma comparable (tupla para WL/k-FWL; frozenset
      para IR). Igual que la del harness.
    - `kinds`: id de clase por vértice (WL) o por k-tupla (k-FWL).
    - `partition`: partición canónica (id por primera aparición).
    - `profile`: multiset de tamaños de clase.
    - `rounds`: rondas de refinamiento usadas (None si no aplica, p. ej. IR).
    """

    observer: str
    signature: object
    kinds: tuple = ()
    partition: tuple = ()
    profile: tuple = ()
    rounds: int | None = None
    n: int = 0

    def as_dict(self) -> dict:
        """Versión serializable (JSON-friendly)."""
        sig = self.signature
        if isinstance(sig, frozenset):
            sig = sorted(sorted(x) if isinstance(x, tuple) else x for x in sig)
        return {
            "observer": self.observer,
            "n": self.n,
            "rounds": self.rounds,
            "signature": sig,
            "kinds": list(self.kinds),
            "partition": list(self.partition),
            "profile": list(self.profile),
        }

    def __repr__(self) -> str:  # corto y legible
        return (f"GraphKindResult(observer={self.observer!r}, n={self.n}, "
                f"rounds={self.rounds}, clases={len(self.profile)})")


def _normalizar(g):
    """Entrada -> (n, edges). Acepta la forma canónica, aristas, graph6,
    networkx (opcional) y bitmasks de adyacencia."""
    if isinstance(g, (tuple, list)) and len(g) == 2 and isinstance(g[0], int):
        n, E = g
        return int(n), [tuple(sorted(e)) for e in E]
    if isinstance(g, str):
        return from_graph6(g)
    if hasattr(g, "number_of_nodes") and hasattr(g, "edges"):
        return g.number_of_nodes(), [tuple(sorted(e)) for e in g.edges()]
    if isinstance(g, (tuple, list)) and g and all(isinstance(x, int) for x in g):
        return len(g), wl.edges_from_adj(list(g))
    if isinstance(g, (tuple, list)):
        E = [tuple(sorted(e)) for e in g]
        n = (max(max(e) for e in E) + 1) if E else 0
        return n, E
    raise TypeError("grafo no reconocido: usá (n, edges), aristas, graph6, "
                    "networkx o bitmasks de adyacencia")


class GraphKind:
    """Instrumento: convierte un grafo en su representación estructural.

    >>> from graphkind import GraphKind
    >>> gk = GraphKind("wl")
    >>> gk.transform((6, [(i, (i + 1) % 6) for i in range(6)])).observer
    'wl'
    """

    OBSERVADORES = OBSERVADORES

    def __init__(self, observer: str = "wl"):
        if observer not in OBSERVADORES:
            raise ValueError(f"observador desconocido: {observer!r} "
                             f"(válidos: {', '.join(OBSERVADORES)})")
        self.observer = observer

    def transform(self, grafo) -> GraphKindResult:
        """Firma estructural del grafo con el observador elegido."""
        n, E = _normalizar(grafo)
        adj = wl.adj_from_edges(n, E)
        if self.observer == "wl":
            colors, rounds = wl.wl1_colors(n, adj, info=True)
            part = tuple(wl.particion(colors))
            return GraphKindResult("wl", wl.firma(colors), part, part,
                                   tuple(wl.perfil(colors)), rounds, n)
        if self.observer in ("kw2", "kw3"):
            k = int(self.observer[-1])
            colors, rounds = wl.kfwl_colors(n, adj, k, info=True)
            part = tuple(wl.particion(colors))
            return GraphKindResult(self.observer, wl.firma(colors), (),
                                   part, tuple(wl.perfil(colors)), rounds, n)
        k = int(self.observer[-1])          # ir1 / ir2
        sig = individualizacion.IR_k(n, E, k, "peor")
        return GraphKindResult(self.observer, sig, (), (), (), None, n)

    def signature(self, grafo):
        """Atajo: `transform(grafo).signature`."""
        return self.transform(grafo).signature

    def separa(self, g1, g2) -> bool:
        """¿El observador distingue los dos grafos?"""
        return self.signature(g1) != self.signature(g2)

    # ----- universos (ley de T4 y dualidades) -----

    def t4(self, grafo) -> bool:
        """¿La partición WL del grafo es complemento-invariante? (T4)."""
        n, E = _normalizar(grafo)
        return wl.t4(wl.adj_from_edges(n, E))

    def oraculo(self, n, adj, iota, f, f1, f2, sigma=None) -> dict:
        """Predice T4 para un universo (f, ι) sin enumerar grafos."""
        return universos.oraculo(n, adj, iota, f, f1, f2, sigma=sigma)

    def t4_multicapa(self, n, capas, capas_iota, variante="canonica") -> dict:
        """T4 en objetos multicapa (perfil y partición)."""
        return multicapa.t4(n, capas, capas_iota, variante)

    def t4_hipergrafo(self, n, k, aristas) -> bool:
        """T4_k en hipergrafos k-uniformes."""
        return hipergrafo.t4_k_uniforme(n, k, aristas)

    def __repr__(self) -> str:
        return f"GraphKind(observer={self.observer!r})"
