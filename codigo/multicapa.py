"""Multicapa (v2): refinamiento conjunto y tres dualidades — autocontenido.

- `refinar_conjunto(n, capas, variante)`: 1-WL conjunto de (V, E_1..E_L)
  en variantes "ordenada" (capas etiquetadas) y "canonica" (S_L-invariante).
- `complemento_total`, `complemento_capa`, `complemento_canales`.
- `t4`: perfil + partición fuerte.

Ley (EXP-162/163): T4 vive con el complemento TOTAL (uniforme); con el
complemento POR CAPA muere en la variante canónica (coherencia
multicanal); las permutaciones de canales preservan (la partición es
ciega al orden).
"""

import hashlib
from collections import Counter
from itertools import combinations


def _h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def _adj(n, E):
    d = {v: set() for v in range(n)}
    for a, b in E:
        d[a].add(b)
        d[b].add(a)
    return d


def refinar_conjunto(n, capas, variante="canonica"):
    if variante not in ("ordenada", "canonica"):
        raise ValueError("variante ∈ {'ordenada','canonica'}")
    adj = [_adj(n, E) for E in capas]
    L = len(capas)
    if variante == "ordenada":
        colors = {v: _h("|".join(str(len(adj[l][v]))
                                 for l in range(L))) for v in range(n)}
    else:
        colors = {v: _h(",".join(sorted(str(len(adj[l][v]))
                                         for l in range(L))))
                  for v in range(n)}
    prev = None
    for _ in range(n + 2):
        nuevos = {}
        for v in range(n):
            if variante == "ordenada":
                datos = "|".join(
                    ",".join(sorted(colors[u] for u in adj[l][v]))
                    for l in range(L))
            else:
                por = [tuple(sorted(colors[u] for u in adj[l][v]))
                       for l in range(L)]
                datos = ";".join(",".join(x) for x in sorted(por))
            nuevos[v] = _h(f"{colors[v]}|{datos}")
        colors = nuevos
        part = tuple(sorted(Counter(colors.values()).values()))
        if part == prev:
            break
        prev = part
    clases = {}
    for v, c in colors.items():
        clases.setdefault(c, set()).add(v)
    particion = frozenset(frozenset(s) for s in clases.values())
    firma = tuple(sorted(colors.values()))
    return firma, colors, particion


def complemento_total(n, capas):
    todas = {tuple(sorted(p)) for p in combinations(range(n), 2)}
    return [sorted(todas - {tuple(sorted(e)) for e in E}) for E in capas]


def complemento_capa(n, capas, ell):
    c = complemento_total(n, capas)
    return [c[i] if i == ell else capas[i] for i in range(len(capas))]


def complemento_canales(capas, pi):
    if sorted(pi) != list(range(len(capas))):
        raise ValueError("pi debe ser permutación")
    return [capas[i] for i in pi]


def t4(n, capas, capas_iota, variante="canonica"):
    _, c1, p1 = refinar_conjunto(n, capas, variante)
    _, c2, p2 = refinar_conjunto(n, capas_iota, variante)
    perfil = lambda c: tuple(sorted(Counter(c.values()).values()))  # noqa: E731
    return {"perfil_igual": perfil(c1) == perfil(c2),
            "particion_igual": p1 == p2}
