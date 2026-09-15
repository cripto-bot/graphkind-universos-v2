"""Color refinement (WL) y utilidades — autocontenido.

- wl_sym: WL simétrico (in/out por color, grados crudos) — el del teorema.
- wl_k_colors: k-FWL (folklore, correlacionada; ≡ (k+1)-WL) — la jerarquía
  de observadores. El nombre "k-WL" a secas designa la variante estándar
  (multiséts separados por posición), que es estrictamente más débil.
- helpers de grafos (bitmasks), complemento, digrafos.
"""

import hashlib
from collections import Counter
from itertools import product


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def wl_sym(n, adj, f, h_fn=None, info=False, rondas_fijas=None):
    """Perfil del WL simétrico: multiset de tamaños de clase.

    Por defecto corre hasta que la partición se estabiliza (tope n+2).
    `h_fn` permite cambiar la función de hash (certificado de colisión);
    `rondas_fijas` fuerza un número exacto de rondas (certificado de
    convergencia); `info=True` devuelve (perfil, rondas_usadas).
    """
    hh = h_fn or h
    in_adj = transp(n, adj)
    colors = [hh(f"g|{adj[v].bit_count()}|{in_adj[v].bit_count()}")
              for v in range(n)]
    prev = None
    usadas = 0
    tope = rondas_fijas if rondas_fijas is not None else (n + 2)
    for r in range(tope):
        new = []
        for v in range(n):
            cnt = Counter()
            m = adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                cnt[colors[u]] += 1
            ci = Counter()
            m = in_adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                ci[colors[u]] += 1
            keys = set(cnt) | set(ci)
            prof = tuple(sorted((c, f(ci.get(c, 0)), f(cnt.get(c, 0)))
                                for c in keys))
            new.append(hh(f"{colors[v]}|{prof}"))
        colors = new
        usadas = r + 1
        if rondas_fijas is None:
            part = tuple(sorted(Counter(colors).values()))
            if part == prev:
                break
            prev = part
    perfil = tuple(sorted(Counter(colors).values()))
    return (perfil, usadas) if info else perfil


def transp(n, adj):
    out = [0] * n
    for v in range(n):
        m = adj[v]
        while m:
            u = (m & -m).bit_length() - 1
            m &= m - 1
            out[u] |= 1 << v
    return out


def wl_k_colors(n, adj, k, rounds=None, info=False):
    """k-FWL (folklore, correlacionada; ≡ (k+1)-WL): colores de k-tuplas.

    La actualización usa pares de posiciones (i,j) con el MISMO w; por la
    equivalencia conocida es tan fuerte como (k+1)-WL. La variante estándar
    ("k-WL", multiséts separados) es más débil y NO separa Rook de
    Shrikhande en k=3 (ver EXP-159 del laboratorio)."""
    if rounds is None:
        rounds = n + 2
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
    usadas = 0
    tope = rounds if rounds is not None else (n + 2)
    for r in range(tope):
        usadas = r + 1
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
        firma = tuple(sorted(colors.values()))
        if firma == prev:
            break
        prev = firma
    return (colors, usadas) if info else colors


def wl_k_union(adj1, adj2, k):
    n1, n2 = len(adj1), len(adj2)
    n = n1 + n2
    adj_u = [0] * n
    for v in range(n1):
        adj_u[v] = adj1[v]
    for v in range(n2):
        adj_u[n1 + v] = adj2[v] << n1
    return wl_k_colors(n, adj_u, k, rounds=n + 2)


def separados(adj1, adj2, k):
    """¿k-FWL separa los dos grafos? (colores compartidos en la unión)."""
    n1 = len(adj1)
    colors = wl_k_union(adj1, adj2, k)
    c1 = Counter(colors[t] for t in product(range(n1), repeat=k))
    c2 = Counter(colors[t] for t in product(range(n1, n1 + len(adj2)),
                                            repeat=k))
    return set(c1) != set(c2) or sorted(c1.values()) != sorted(c2.values())


def build_adj(n, mask):
    adj = [0] * n
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (mask >> bit) & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            bit += 1
    return adj


def comp_adj(n, adj):
    out = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if not (adj[i] >> j) & 1:
                out[i] |= 1 << j
                out[j] |= 1 << i
    return out


def all_digraphs(n):
    pos = [(u, v) for u in range(n) for v in range(n) if u != v]
    for mask in range(1 << len(pos)):
        adj = [0] * n
        for k, (u, v) in enumerate(pos):
            if (mask >> k) & 1:
                adj[u] |= 1 << v
        yield mask, adj


def all_graphs(n):
    for mask in range(1 << (n * (n - 1) // 2)):
        yield mask, build_adj(n, mask)


# ---------------------------------------------------------------------------
# API amigable (añadida en el paquete `graphkind`; no altera lo de arriba)
# ---------------------------------------------------------------------------

def adj_from_edges(n, edges):
    """Bitmasks de adyacencia desde una lista de aristas (0-index, simple)."""
    adj = [0] * n
    for u, v in edges:
        if u == v:
            raise ValueError("sin lazos")
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def edges_from_adj(adj):
    """Lista de aristas desde bitmasks."""
    return [(u, v) for u in range(len(adj)) for v in range(u + 1, len(adj))
            if (adj[u] >> v) & 1]


def complement(n, adj):
    """Complemento simple (nombre amigable de comp_adj)."""
    return comp_adj(n, adj)


def _wl1_raw(n, adj, rounds):
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


def wl1_colors(n, adj, rounds=None, info=False):
    """1-WL (color refinement) por vértice; converge (tope n+2) o `rounds`.

    Con `info=True` devuelve `(colors, rondas_usadas)` (aditivo).
    """
    if rounds is not None:
        col = _wl1_raw(n, adj, rounds)
        return (col, rounds) if info else col
    colors = [h(f"g|{adj[v].bit_count()}") for v in range(n)]
    prev = None
    usadas = 0
    for r in range(n + 2):
        usadas = r + 1
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
    return (colors, usadas) if info else colors


def kfwl_colors(n, adj, k, rounds=None, info=False):
    """k-FWL (correlacionada; ≡ (k+1)-WL). Requiere k >= 2.

    Con `info=True` devuelve `(colors, rondas_usadas)` (aditivo).
    """
    if k < 2:
        raise ValueError("kfwl requiere k >= 2 (usa wl1_colors para k = 1)")
    return wl_k_colors(n, adj, k, rounds=rounds, info=info)


def firma(colors):
    """Multiset de colores ordenado (firma de un grafo para un observador)."""
    if isinstance(colors, dict):
        colors = colors.values()
    return tuple(sorted(colors))


def separa(adj1, adj2, k):
    """¿El observador (1-WL si k=1; k-FWL si k>=2) separa el par?

    Firma por grafo; equivalente al test de la unión (sin aristas cruzadas).
    """
    def f(n, adj):
        return (firma(wl1_colors(n, adj)) if k == 1
                else firma(kfwl_colors(n, adj, k)))
    return f(len(adj1), adj1) != f(len(adj2), adj2)


def particion(colors):
    """Partición canónica (índice de clase por primera aparición)."""
    if isinstance(colors, dict):
        colors = [colors[t] for t in sorted(colors)]
    seen = {}
    out = []
    for c in colors:
        if c not in seen:
            seen[c] = len(seen)
        out.append(seen[c])
    return out


def perfil(colors):
    """Multiset de tamaños de clase (el perfil WL)."""
    if isinstance(colors, dict):
        colors = colors.values()
    return tuple(sorted(Counter(colors).values()))


def t4(adj):
    """¿La partición 1-WL es complemento-invariante? (teorema T4)."""
    n = len(adj)
    return (particion(wl1_colors(n, adj)) ==
            particion(wl1_colors(n, comp_adj(n, adj))))
