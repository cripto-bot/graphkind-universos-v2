"""Hipergrafos (v2): k-uniforme, aridades mezcladas y dual — autocontenido.

- `refinar_k_uniforme`, `complemento_k_uniforme`, `t4_k_uniforme`.
- `refinar_mezclado` (canónica/ordenada), `complemento_total_mezclado`,
  `complemento_aridad`, `t4_mezclado`.
- `refine_dual_mezclado`: elige el lado ralo POR ARIDAD (EXP-168/169:
  el refinamiento repara la incoherencia; partición garantizada en la
  clase medida).
"""

import hashlib
from collections import Counter
from itertools import combinations


def _h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def _norm(n, aristas, k):
    out = set()
    for e in aristas:
        e = tuple(sorted(e))
        if len(e) != k or len(set(e)) != k:
            raise ValueError(f"aristas de {k} distintos")
        if any(not (0 <= v < n) for v in e):
            raise ValueError("fuera de rango")
        out.add(e)
    return sorted(out)


def _links(n, aristas, k):
    link = {v: [] for v in range(n)}
    for e in aristas:
        for v in e:
            link[v].append(tuple(x for x in e if x != v))
    return link


def _part(colors):
    cl = {}
    for v, c in colors.items():
        cl.setdefault(c, set()).add(v)
    return (frozenset(frozenset(s) for s in cl.values()),
            tuple(sorted(colors.values())))


def refinar_k_uniforme(n, aristas, k):
    aristas = _norm(n, aristas, k)
    link = _links(n, aristas, k)
    colors = {v: _h(f"g|{len(link[v])}") for v in range(n)}
    prev = None
    for _ in range(n + 2):
        nuevos = {}
        for v in range(n):
            msgs = sorted(tuple(sorted(colors[u] for u in S))
                          for S in link[v])
            nuevos[v] = _h(f"{colors[v]}|" + ",".join("+".join(m)
                                                      for m in msgs))
        colors = nuevos
        p = tuple(sorted(Counter(colors.values()).values()))
        if p == prev:
            break
        prev = p
    return _part(colors)


def complemento_k_uniforme(n, k, aristas):
    todos = {tuple(sorted(t)) for t in combinations(range(n), k)}
    return sorted(todos - {tuple(sorted(e)) for e in aristas})


def t4_k_uniforme(n, k, aristas):
    p1, _ = refinar_k_uniforme(n, aristas, k)
    p2, _ = refinar_k_uniforme(n, complemento_k_uniforme(n, k, aristas), k)
    return p1 == p2


def _msg(colors, link_v):
    return tuple(sorted(tuple(sorted(colors[u] for u in S))
                        for S in link_v))


def refinar_mezclado(n, e2, e3, variante="canonica"):
    if variante not in ("canonica", "ordenada"):
        raise ValueError("variante ∈ {'canonica','ordenada'}")
    e2 = _norm(n, e2, 2)
    e3 = _norm(n, e3, 3)
    l2 = _links(n, e2, 2)
    l3 = _links(n, e3, 3)
    if variante == "ordenada":
        colors = {v: _h(f"g|{len(l2[v])}|{len(l3[v])}") for v in range(n)}
    else:
        colors = {v: _h(",".join(sorted([str(len(l2[v])),
                                         str(len(l3[v]))])))
                  for v in range(n)}
    prev = None
    for _ in range(n + 2):
        nuevos = {}
        for v in range(n):
            m2 = _msg(colors, l2[v])
            m3 = _msg(colors, l3[v])
            msg = f"{m2}|{m3}" if variante == "ordenada" else \
                ",".join(str(x) for x in sorted([m2, m3]))
            nuevos[v] = _h(f"{colors[v]}|{msg}")
        colors = nuevos
        p = tuple(sorted(Counter(colors.values()).values()))
        if p == prev:
            break
        prev = p
    return _part(colors)


def complemento_total_mezclado(n, e2, e3):
    return (complemento_k_uniforme(n, 2, e2),
            complemento_k_uniforme(n, 3, e3))


def complemento_aridad(n, e2, e3, aridad):
    if aridad == 2:
        return complemento_k_uniforme(n, 2, e2), e3
    if aridad == 3:
        return e2, complemento_k_uniforme(n, 3, e3)
    raise ValueError("aridad ∈ {2,3}")


def t4_mezclado(n, e2, e3, dualidad="total", variante="canonica"):
    if dualidad == "total":
        e2p, e3p = complemento_total_mezclado(n, e2, e3)
    elif dualidad == "aridad2":
        e2p, e3p = complemento_aridad(n, e2, e3, 2)
    elif dualidad == "aridad3":
        e2p, e3p = complemento_aridad(n, e2, e3, 3)
    else:
        raise ValueError("dualidad ∈ {total, aridad2, aridad3}")
    p1, _ = refinar_mezclado(n, e2, e3, variante)
    p2, _ = refinar_mezclado(n, e2p, e3p, variante)
    return p1 == p2


def _cuenta(e):
    return len({tuple(sorted(x)) for x in e})


def refine_dual_mezclado(n, e2, e3, variante="canonica"):
    """Elige el lado ralo POR ARIDAD; devuelve (particion, lados)."""
    c2 = complemento_k_uniforme(n, 2, e2)
    c3 = complemento_k_uniforme(n, 3, e3)
    if _cuenta(e2) <= _cuenta(c2):
        e2e, l2 = e2, "e2"
    else:
        e2e, l2 = c2, "e2bar"
    if _cuenta(e3) <= _cuenta(c3):
        e3e, l3 = e3, "e3"
    else:
        e3e, l3 = c3, "e3bar"
    p, _ = refinar_mezclado(n, e2e, e3e, variante)
    return p, (l2, l3)
