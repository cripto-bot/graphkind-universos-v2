"""GraphKind WL — color refinement (1-WL) and k-FWL over bitmask adjacency.

Self-contained kernel of the GraphKind laboratory:

- ``wl1_colors``: classic color refinement (1-WL) — the engine's kernel.
- ``kfwl_colors``: correlated k-FWL (folklore), equivalent to (k+1)-WL.
  The plain "k-WL" variant (position-separated multisets) is strictly
  weaker; it is not implemented here (see the paper).
- ``separa``: does an observer separate two graphs? (union test).
- ``t4``: is the 1-WL partition complement-invariant? (theorem T4).

Graphs are adjacency bitmasks: ``adj[v]`` is an int whose bit ``u`` is 1
iff ``u`` is a neighbor of ``v`` (no self-loops).

Reference: GraphKind — Universes v2, DOI 10.5281/zenodo.22747350
(CC-BY-4.0). Repository: github.com/cripto-bot/graphkind-universos-v2.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from itertools import product

__all__ = [
    "h",
    "adj_from_edges",
    "edges_from_adj",
    "complement",
    "wl1_colors",
    "kfwl_colors",
    "firma",
    "separa",
    "particion",
    "perfil",
    "t4",
]

__version__ = "0.1.1"
DOI = "10.5281/zenodo.22747350"


def h(s: str) -> str:
    """Deterministic color hash (sha256, first 12 hex chars)."""
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def adj_from_edges(n: int, edges) -> list[int]:
    """Adjacency bitmasks from an edge list (0-indexed, undirected)."""
    adj = [0] * n
    for u, v in edges:
        if u == v:
            raise ValueError("self-loops are not supported")
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def edges_from_adj(adj) -> list[tuple[int, int]]:
    """Edge list from adjacency bitmasks."""
    return [(u, v) for u in range(len(adj)) for v in range(u + 1, len(adj))
            if (adj[u] >> v) & 1]


def complement(n: int, adj) -> list[int]:
    """Simple complement (same vertices, no loops)."""
    out = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if not (adj[i] >> j) & 1:
                out[i] |= 1 << j
                out[j] |= 1 << i
    return out


def _wl1_raw(n: int, adj, rounds: int) -> list[str]:
    colors = [h(f"g|{adj[v].bit_count()}") for v in range(n)]
    for _ in range(rounds):
        new = []
        for v in range(n):
            cnt = Counter()
            m = adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                cnt[colors[u]] += 1
            new.append(h(f"{colors[v]}|{tuple(sorted(cnt.items()))}"))
        colors = new
    return colors


def wl1_colors(n: int, adj, rounds: int | None = None) -> list[str]:
    """1-WL (color refinement) colors, one per vertex.

    Refines until the partition stabilizes (cap ``n + 2``), or exactly
    ``rounds`` rounds when given. Deterministic.
    """
    if rounds is not None:
        return _wl1_raw(n, adj, rounds)
    colors = [h(f"g|{adj[v].bit_count()}") for v in range(n)]
    prev = None
    for _ in range(n + 2):
        new = []
        for v in range(n):
            cnt = Counter()
            m = adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                cnt[colors[u]] += 1
            new.append(h(f"{colors[v]}|{tuple(sorted(cnt.items()))}"))
        colors = new
        part = tuple(sorted(Counter(colors).values()))
        if part == prev:
            break
        prev = part
    return colors


def kfwl_colors(n: int, adj, k: int, rounds: int | None = None) -> dict:
    """Correlated k-FWL colors of the k-tuples (equivalent to (k+1)-WL).

    ``k >= 2``. Returns a dict ``{(v1, ..., vk): color}``. Refines until
    the color multiset stabilizes (cap ``n + 2``) or ``rounds`` rounds.
    """
    if k < 2:
        raise ValueError("kfwl requires k >= 2 (use wl1_colors for k = 1)")
    tuplas = list(product(range(n), repeat=k))

    def init(t):
        grados = [str(adj[a].bit_count()) for a in t]
        est = []
        for i in range(k):
            for j in range(i + 1, k):
                a, b = t[i], t[j]
                est.append("=" if a == b else
                           ("1" if (adj[a] >> b) & 1 else "0"))
        return h("|".join(grados) + ":" + "".join(est))

    colors = {t: init(t) for t in tuplas}
    prev = None
    tope = rounds if rounds is not None else (n + 2)
    for _ in range(tope):
        new = {}
        for t in tuplas:
            vecinos = []
            for i in range(k):
                for j in range(i + 1, k):
                    for w in range(n):
                        t2 = t[:i] + (w,) + t[i + 1:]
                        t3 = t[:j] + (w,) + t[j + 1:]
                        vecinos.append((i, j, colors[t2], colors[t3]))
            vecinos.sort()
            new[t] = h(colors[t] + "|" + ",".join(
                f"{i}{j}:{a}:{b}" for i, j, a, b in vecinos))
        colors = new
        firma_ = tuple(sorted(colors.values()))
        if rounds is None and firma_ == prev:
            break
        prev = firma_
    return colors


def firma(colors) -> tuple:
    """Sorted color multiset (a graph signature for a fixed observer)."""
    if isinstance(colors, dict):
        colors = colors.values()
    return tuple(sorted(colors))


def separa(adj1, adj2, k: int) -> bool:
    """Does the observer (1-WL for k=1, k-FWL for k>=2) separate the pair?

    Computes each graph's signature (sorted color multiset) separately and
    compares them. Equivalent to the union test used by the engine: the
    colors are deterministic functions of the local structure and the
    union has no cross edges, so the shared color space does not merge
    anything.
    """
    def firma_de(n, adj):
        if k == 1:
            return firma(wl1_colors(n, adj))
        return firma(kfwl_colors(n, adj, k))

    return firma_de(len(adj1), adj1) != firma_de(len(adj2), adj2)


def particion(colors) -> list[int]:
    """Partition of the vertices induced by the colors (canonical: class
    index by first appearance, so two graphs with the same partition get
    the same list even when the color labels differ)."""
    if isinstance(colors, dict):
        colors = [colors[t] for t in sorted(colors)]
    seen: dict = {}
    out = []
    for c in colors:
        if c not in seen:
            seen[c] = len(seen)
        out.append(seen[c])
    return out


def perfil(colors) -> tuple:
    """Multiset of class sizes (the WL profile)."""
    if isinstance(colors, dict):
        colors = colors.values()
    return tuple(sorted(Counter(colors).values()))


def t4(adj) -> bool:
    """Is the 1-WL partition complement-invariant? (theorem T4).

    True for every graph in the standard universe (the theorem); the
    laboratory measures where it dies in other universes (Z3 dynamics,
    multilayer, mixed arities). Included as the theorem's probe.
    """
    n = len(adj)
    return particion(wl1_colors(n, adj)) == particion(wl1_colors(n, complement(n, adj)))
