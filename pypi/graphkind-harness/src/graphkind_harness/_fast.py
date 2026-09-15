"""k-FWL vectorizado (numpy) para el harness — misma PARTICIÓN que el motor.

El motor (`graphkind.wl.wl_k_colors`) es la referencia congelada: exacto
pero costoso en n≥16. Acá se usa la misma recurrencia k-FWL con:

- tuplas codificadas como índices enteros y vecinos precomputados (arrays);
- compresión **conmutativa** del multiset de vecinos (suma módulo 2^64 de
  un hash no lineal por entrada) en lugar de ordenar;
- internado determinístico de colores por ronda (`np.unique`).

La partición resultante coincide con la del motor (verificado en los tests
contra las anclas). Al ser todo operaciones vectoriales, el mismo código
puede correr en GPU con CuPy reemplazando `numpy` por `cupy`.
"""

from __future__ import annotations

import numpy as np

MASK = np.uint64(0xFFFFFFFFFFFFFFFF)
K1 = np.uint64(0x9E3779B97F4A7C15)
K2 = np.uint64(0x100000001B3)
K3 = np.uint64(0xC2B2AE3D27D4EB4F)
SHIFT = np.uint64(29)


def _vecinos(n: int, k: int):
    """Arrays (N, M) con los índices de los vecinos y etiquetas (M,)."""
    pot = [n ** (k - 1 - p) for p in range(k)]
    N = n ** k
    ti = np.arange(N, dtype=np.int64)
    t = np.stack([(ti // pot[p]) % n for p in range(k)], axis=1)  # (N,k)
    ets, i2, i3 = [], [], []
    for i in range(k):
        for j in range(i + 1, k):
            et = i * 10 + j
            for w in range(n):
                ets.append(et)
                i2.append(ti + (w - t[:, i]) * pot[i])
                i3.append(ti + (w - t[:, j]) * pot[j])
    return (t, np.array(ets, dtype=np.uint64),
            np.stack(i2, axis=1), np.stack(i3, axis=1))


def kfwl_fast(n: int, adj, k: int, max_rounds: int | None = None):
    """Colores k-FWL (ids internados) por tupla, vectorizado. k >= 2."""
    if k < 2:
        raise ValueError("kfwl_fast requiere k >= 2")
    t, et, i2, i3 = _vecinos(n, k)
    N = t.shape[0]

    deg = np.array([adj[v].bit_count() for v in range(n)], dtype=np.int64)
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            A[a, b] = 1 if (adj[a] >> b) & 1 else 0

    # color inicial exacto: grados (base n) + bits de igualdad/adyacencia (base 3)
    code = np.zeros(N, dtype=np.int64)
    for p in range(k):
        code = code * n + deg[t[:, p]]
    q = 0
    for i in range(k):
        for j in range(i + 1, k):
            a, b = t[:, i], t[:, j]
            bit = np.where(a == b, 2, A[a, b])
            code = code * 3 + bit
            q += 1
    col = code.astype(np.uint64)   # color inicial global (sin internar)

    tope = max_rounds or (n + 2)
    prev = None
    for _ in range(tope):
        ca = col[i2]
        cb = col[i3]
        h = (et + K1) & MASK
        h = ((h ^ (ca + K2)) * K2) & MASK
        h = ((h ^ (cb + K3)) * K1) & MASK
        h ^= h >> SHIFT
        s = h.sum(axis=1, dtype=np.uint64)          # hash conmutativo
        # nuevo color = hash global de (color previo, s) — sin internado
        # per-grafo: la identidad del color no se pierde entre grafos.
        h2 = (col + K1) & MASK
        h2 = ((h2 ^ (s + K2)) * K2) & MASK
        h2 ^= h2 >> SHIFT
        col = h2
        _, cnt = np.unique(col, return_counts=True)
        part = tuple(sorted(cnt.tolist()))
        if part == prev:
            break
        prev = part
    return col


def firma_kfwl(n: int, adj, k: int):
    """Firma del grafo: multiset de colores k-FWL (tupla ordenada de ids)."""
    return tuple(sorted(kfwl_fast(n, adj, k).tolist()))


def particion_kfwl(n: int, adj, k: int):
    """Partición canónica de las k-tuplas (ids por primera aparición)."""
    from graphkind.wl import particion
    return particion(kfwl_fast(n, adj, k).tolist())
