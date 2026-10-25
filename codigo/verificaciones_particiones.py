#!/usr/bin/env python3
"""EXP-086p — certificado de T4 fuerte: PARTICIONES, no perfiles.

El claim del paper ("2 131 019/2 131 019 grafos exhaustivos n≤7") se
verificaba con V1, que compara el *perfil* (multiset de tamaños de clase),
una versión más débil que la igualdad de particiones. Este script repite
la enumeración exhaustiva n≤7 comparando CR_1(G) == CR_1(Ḡ) como
particiones del mismo V, con un 1-WL simétrico propio.

Uso:
    python3 codigo/verificaciones_particiones.py                 # n≤7
    python3 codigo/verificaciones_particiones.py --doble         # doble corrida
    python3 codigo/verificaciones_particiones.py --nmax 6        # sanity rápida

Salida: resultados/EXP-086_particiones_frozen.json (o --out).
"""

import argparse
import hashlib
import json
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wl import build_adj, transp, wl_k_colors, wl_sym  # noqa: E402

NMAX = 7
CHUNK = 500


def _particion(n, colors):
    by = {}
    for v, c in enumerate(colors):
        by.setdefault(c, []).append(v)
    return frozenset(frozenset(vs) for vs in by.values())


def wl_partition(n, adj, f=None, max_rounds=None):
    """1-WL simétrico (in/out por color): devuelve la partición de V.

    Replica `wl_sym` (el del teorema) pero devolviendo la partición, no
    solo el multiset de tamaños. `f` comprime los conteos por color.
    """
    if f is None:
        f = lambda x: x  # noqa: E731
    if max_rounds is None:
        max_rounds = n + 2

    in_adj = transp(n, adj)
    raw = [("d", adj[v].bit_count(), in_adj[v].bit_count())
           for v in range(n)]
    tabla = {}
    colors = [tabla.setdefault(c, len(tabla)) for c in raw]
    prev = None

    for _ in range(max_rounds):
        nuevas = []
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
            nuevas.append((colors[v], prof))
        tabla = {}
        colors = [tabla.setdefault(c, len(tabla)) for c in nuevas]
        firma = tuple(sorted(Counter(colors).values()))
        if firma == prev:
            break
        prev = firma

    return _particion(n, colors)


def _rango(args):
    n, lo, hi = args
    total = 0
    bad = 0
    primer_bad = -1
    full = (1 << (n * (n - 1) // 2)) - 1
    for mask in range(lo, hi):
        adj = build_adj(n, mask)
        adj_c = build_adj(n, full ^ mask)
        total += 1
        if wl_partition(n, adj) != wl_partition(n, adj_c):
            bad += 1
            if primer_bad < 0:
                primer_bad = mask
    return n, total, bad, primer_bad


def _chunks(n):
    full = 1 << (n * (n - 1) // 2)
    for lo in range(0, full, CHUNK):
        yield (n, lo, min(lo + CHUNK, full))


def _corrida(nmax, nproc):
    res = {}
    for n in range(1, min(nmax, 6) + 1):
        _, total, bad, pb = _rango((n, 0, 1 << (n * (n - 1) // 2)))
        res[n] = {"total": total, "bad": bad, "primer_bad": pb}

    if nmax >= 7:
        with Pool(nproc) as pool:
            for n_, total, bad, pb in pool.imap_unordered(_rango,
                                                          _chunks(7),
                                                          chunksize=1):
                r = res.setdefault(n_, {"total": 0, "bad": 0,
                                        "primer_bad": -1})
                r["total"] += total
                r["bad"] += bad
                if pb >= 0 and r["primer_bad"] < 0:
                    r["primer_bad"] = pb

    total = sum(r["total"] for r in res.values())
    bad = sum(r["bad"] for r in res.values())
    return {str(k): res[k] for k in sorted(res)}, total, bad


def _hash(por_n):
    canon = json.dumps(por_n, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode()).hexdigest()


def _sanity():
    """Regresión: 1-WL propio == wl_sym (perfil) y k=1 ya no es grado."""
    for n in range(1, 6):
        for mask in range(1 << (n * (n - 1) // 2)):
            adj = build_adj(n, mask)
            p = wl_partition(n, adj)
            perfil = tuple(sorted(len(s) for s in p))
            assert perfil == wl_sym(n, adj, lambda k: k), (n, mask)

    # n=5, mask 28: grado [4,1]; 1-WL refina a [1,2,2].
    adj = build_adj(5, 28)
    p1 = wl_partition(5, adj)
    pk = wl_k_colors(5, adj, 1, rounds=5 + 2)
    by = {}
    for (v,), c in pk.items():
        by.setdefault(c, set()).add(v)
    pk_part = frozenset(frozenset(vs) for vs in by.values())
    deg = {}
    for v in range(5):
        deg.setdefault(adj[v].bit_count(), set()).add(v)
    deg_part = frozenset(frozenset(vs) for vs in deg.values())
    assert pk_part == p1, "wl_k_colors(k=1) no reproduce 1-WL"
    assert p1 != deg_part, "el sanity del ejemplo no refina"
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=NMAX,
                    help="máximo n (≤7; default 7)")
    ap.add_argument("--nproc", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "resultados", "EXP-086_particiones_frozen.json"))
    ap.add_argument("--doble", action="store_true",
                    help="correr dos veces y exigir el mismo hash")
    args = ap.parse_args()

    if args.nmax > NMAX:
        raise SystemExit("nmax > 7 es inviable (n=8 son 2^28 grafos)")

    sanity = _sanity()
    esperado = sum(1 << (n * (n - 1) // 2)
                   for n in range(1, args.nmax + 1))

    t0 = time.time()
    por_n, total, bad = _corrida(args.nmax, args.nproc)
    wall = round(time.time() - t0, 3)
    h1 = _hash(por_n)

    out = {
        "exp": "EXP-086p",
        "definicion": ("CR_1(G)==CR_1(complemento(G)) como particiones "
                       "de V; 1-WL simétrico propio, f=id; exhaustivo"),
        "nmax": args.nmax,
        "nproc": args.nproc,
        "por_n": por_n,
        "total": total,
        "esperado": esperado,
        "bad": bad,
        "sha256": h1,
        "wall_s": wall,
        "sanity": sanity,
    }

    if args.doble:
        t1 = time.time()
        por_n2, total2, bad2 = _corrida(args.nmax, args.nproc)
        wall2 = round(time.time() - t1, 3)
        h2 = _hash(por_n2)
        assert (total, bad, h1) == (total2, bad2, h2), "doble corrida difiere"
        out["sha256_segunda"] = h2
        out["wall_s_segunda"] = wall2

    assert total == esperado, (total, esperado)
    assert bad == 0, bad

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
