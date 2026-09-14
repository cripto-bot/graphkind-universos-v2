"""Individualización (v2): IR_k en dos modos — autocontenido.

- `individualizar_refinar(n, E, S)`: marcador canónico `IND` (sin id de
  vértice) + refinamiento a convergencia → firma (multiset de colores).
- `IR_k(n, E, k, modo)`: invariante con cada k-subconjunto individualizado;
  `"peor"` = soporte (sin multiplicidades, primario), `"multiset"` = con
  multiplicidades.

Hallazgo SG-02/SG-03: IR_1 NO separa Rook de Shrikhande (y falla donde
falla 3-WL); IR_2 SÍ (se comporta como 3-FWL ≡ 4-WL).
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


def individualizar_refinar(n, E, S):
    adj = _adj(n, E)
    colors = {v: _h("IND" if v in S else f"g|{len(adj[v])}")
              for v in range(n)}
    prev = None
    for _ in range(n + 2):
        nuevos = {}
        for v in range(n):
            msg = ",".join(sorted(colors[u] for u in adj[v]))
            nuevos[v] = _h(f"{colors[v]}|{msg}")
        colors = nuevos
        p = tuple(sorted(Counter(colors.values()).values()))
        if p == prev:
            break
        prev = p
    return tuple(sorted(colors.values()))


def IR_k(n, E, k=1, modo="peor"):
    if modo not in ("peor", "multiset"):
        raise ValueError("modo ∈ {'peor','multiset'}")
    if k == 1:
        casos = [individualizar_refinar(n, E, {v}) for v in range(n)]
    elif k == 2:
        casos = [individualizar_refinar(n, E, set(p))
                 for p in combinations(range(n), 2)]
    else:
        raise ValueError("k ∈ {1,2}")
    if modo == "peor":
        return frozenset(casos)
    return tuple(sorted(casos))
