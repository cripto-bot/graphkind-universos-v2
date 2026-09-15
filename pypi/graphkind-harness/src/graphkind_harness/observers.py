"""Observadores del harness: firma de un grafo para cada invariante.

Un observador es una función ``(n, E) -> firma`` (hashable). El registro
incluye un control negativo ("grado") que debe colisionar: sirve para
verificar que la métrica de colisiones detecta observadores débiles.
"""

from __future__ import annotations

from graphkind import individualizacion, wl

from ._fast import firma_kfwl


def _adj(n, E):
    return wl.adj_from_edges(n, E)


def obs_wl(n, E):
    """1-WL (color refinement)."""
    return wl.firma(wl.wl1_colors(n, _adj(n, E)))


def obs_kw2(n, E):
    """2-FWL (correlacionada; ≡ 3-WL). Implementación rápida del harness."""
    return firma_kfwl(n, _adj(n, E), 2)


def obs_kw3(n, E):
    """3-FWL (correlacionada; ≡ 4-WL). Implementación rápida del harness."""
    return firma_kfwl(n, _adj(n, E), 3)


def obs_ir1(n, E):
    """IR₁ (peor caso sobre la individualización de 1 vértice)."""
    return individualizacion.IR_k(n, E, 1, "peor")


def obs_ir2(n, E):
    """IR₂ (peor caso sobre pares)."""
    return individualizacion.IR_k(n, E, 2, "peor")


def obs_grado(n, E):
    """Control negativo: solo la lista de grados (debe colisionar)."""
    adj = _adj(n, E)
    return tuple(sorted(adj[v].bit_count() for v in range(n)))


OBSERVADORES = {
    "grado": obs_grado,      # control negativo
    "wl": obs_wl,
    "kw2": obs_kw2,
    "kw3": obs_kw3,
    "ir1": obs_ir1,
    "ir2": obs_ir2,
}

#: observadores "serios" (sin el control negativo)
REALES = ("wl", "kw2", "kw3", "ir1", "ir2")


def observador(nombre):
    if nombre not in OBSERVADORES:
        raise ValueError(f"observador desconocido: {nombre} "
                         f"(hay: {', '.join(OBSERVADORES)})")
    return OBSERVADORES[nombre]


def observadores(nombres=None):
    nombres = nombres or list(OBSERVADORES)
    if isinstance(nombres, str):
        nombres = [x.strip() for x in nombres.split(",") if x.strip()]
    return {n: observador(n) for n in nombres}
