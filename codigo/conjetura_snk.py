#!/usr/bin/env python3
"""Puesta a prueba computacional de la conjetura Sₙ·K + f(1)≠f(2).

No declara novedad: testea predicciones y busca contraejemplos.
Motor: codigo/wl.py + codigo/universos.py + wl_partition (particiones).
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import hashlib
import json
import math
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wl import (all_digraphs, all_graphs, build_adj, comp_adj,  # noqa: E402
                transp, wl_sym)
from universos import clasificar_involucion, t4_garantizado  # noqa: E402
from verificaciones_particiones import wl_partition  # noqa: E402

NMAX = 6
SEEDS = range(5)


def f_from_tab(tab):
    return lambda k: tab[k] if 0 <= k < len(tab) else tab[-1]


def catalog_tabs():
    fs = {
        "id": lambda k: k,
        "const1": lambda k: 1,
        "umbral1": lambda k: int(k >= 1),
        "umbral2": lambda k: int(k >= 2),
        "umbral3": lambda k: int(k >= 3),
        "umbral4": lambda k: int(k >= 4),
        "mod2": lambda k: k % 2,
        "mod3": lambda k: k % 3,
        "mod4": lambda k: k % 4,
        "mod5": lambda k: k % 5,
        "trunc1": lambda k: min(k, 1),
        "trunc2": lambda k: min(k, 2),
        "trunc3": lambda k: min(k, 3),
        "log2": lambda k: k.bit_length(),
        "cuadrado": lambda k: k * k,
        "cubo": lambda k: k ** 3,
        "raiz": lambda k: math.isqrt(k),
    }
    return [(name, tuple(f(k) for k in range(NMAX + 1)))
            for name, f in fs.items()]


def random_tabs(seed, n, equal):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        tab = rng.integers(0, 4, size=NMAX + 1).astype(int)
        if equal:
            tab[2] = tab[1]
        else:
            tab[2] = (tab[1] + rng.integers(1, 4)) % 4
        out.append(tuple(int(x) for x in tab))
    return out


def comp_dir(n, adj):
    out = [0] * n
    for u in range(n):
        for v in range(n):
            if u != v and not ((adj[u] >> v) & 1):
                out[u] |= 1 << v
    return out


def apply_iota(name, n, adj):
    if name == "id":
        return adj
    if name == "comp_dir":
        return comp_dir(n, adj)
    if name == "transp":
        return transp(n, adj)
    if name == "comp_transp":
        return comp_dir(n, transp(n, adj))
    raise ValueError(name)


def comp_parcial(n, adj):
    S = set(range(n // 2))
    out = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            has = (adj[i] >> j) & 1
            if i in S and j in S:
                has = not has
            if has:
                out[i] |= 1 << j
                out[j] |= 1 << i
    return out


def flip_inc0(n, adj):
    out = adj[:]
    for v in range(1, n):
        out[0] ^= 1 << v
        out[v] ^= 1 << 0
    return out


def toggle_subset(n, adj, smask):
    S = {v for v in range(n) if (smask >> v) & 1}
    out = adj[:]
    for i in range(n):
        for j in range(i + 1, n):
            if i in S and j in S:
                out[i] ^= 1 << j
                out[j] ^= 1 << i
    return out


def _profile(part):
    return tuple(sorted(len(s) for s in part))


def worker_A(args):
    label, tab = args
    f = f_from_tab(tab)
    fails = 0
    first = None
    for n in range(2, NMAX + 1):
        for mask, adj in all_graphs(n):
            if wl_partition(n, adj, f) != wl_partition(n, comp_adj(n, adj), f):
                fails += 1
                if first is None:
                    first = [n, mask]
    pred = tab[1] != tab[2]
    return ("A", label, tab, pred, fails, first)


def worker_B(args):
    label, tab, iname = args
    f = f_from_tab(tab)
    fails = 0
    first = None
    for mask, adj in all_digraphs(4):
        if wl_partition(4, adj, f) != wl_partition(4, apply_iota(iname, 4, adj), f):
            fails += 1
            if first is None:
                first = [mask]
    clase = "trivial" if iname in ("id", "transp") else "dual"
    pred = t4_garantizado(tab[1], tab[2], clase)
    return ("B", label, tab, iname, pred, fails, first)


def worker_C(args):
    kind, smask = args
    f = f_from_tab(tuple(range(NMAX + 1)))
    fails = 0
    first = None
    if kind in ("comp_parcial", "flip_inc0"):
        rng_n = range(2, NMAX + 1)
    else:
        rng_n = (5, 6)
    for n in rng_n:
        for mask, adj in all_graphs(n):
            if kind == "comp_parcial":
                adj2 = comp_parcial(n, adj)
            elif kind == "flip_inc0":
                adj2 = flip_inc0(n, adj)
            else:
                adj2 = toggle_subset(n, adj, smask)
            if wl_partition(n, adj, f) != wl_partition(n, adj2, f):
                fails += 1
                if first is None:
                    first = [n, mask]
                break
        if fails:
            break
    return ("C", kind, smask, fails, first)


def sanity():
    # wl_partition (perfil) == wl_sym con f=id
    f = f_from_tab(tuple(range(NMAX + 1)))
    for n in range(2, 6):
        for mask, adj in all_graphs(n):
            p = _profile(wl_partition(n, adj, f))
            assert p == wl_sym(n, adj, f), (n, mask, p)
    # const1: la ley predice falla en n=6
    tab = tuple(1 for _ in range(NMAX + 1))
    f1 = f_from_tab(tab)
    found = False
    for mask, adj in all_graphs(6):
        if wl_partition(6, adj, f1) != wl_partition(6, comp_adj(6, adj), f1):
            found = True
            break
    assert found, "const1 debería fallar en n=6"
    # Gap de API: clasificar_involucion es out-only; el teorema es simétrico.
    # En un digrafo asimétrico, transp debería ser 'trivial' (swap in/out),
    # pero el clasificador out-only probablemente diga 'local'.
    adj_path = [1 << 1, 1 << 2, 1 << 3, 0]  # 0->1->2->3
    api_transp = clasificar_involucion(4, adj_path, transp,
                                       f=lambda k: k)
    return {"status": "ok", "api_transp": api_transp,
            "esperado_simetrico": "trivial"}


def main():
    t0 = time.time()
    here = os.path.dirname(os.path.abspath(__file__))
    spec_path = os.path.join(os.path.dirname(here), "paper",
                             "LIMITES-DIGRAFOS-SPEC.md")
    spec = open(spec_path, "rb").read()
    spec_sha = hashlib.sha256(spec).hexdigest()
    san = sanity()

    cat = catalog_tabs()
    r_eq, r_neq = [], []
    for s in SEEDS:
        r_eq += random_tabs(1000 + s, 13, True)
        r_neq += random_tabs(2000 + s, 13, False)
    r_eq = r_eq[:64]
    r_neq = r_neq[:64]

    tA = [(lab, tab) for lab, tab in cat]
    tA += [(f"rand_eq_{i}", tab) for i, tab in enumerate(r_eq)]
    tA += [(f"rand_neq_{i}", tab) for i, tab in enumerate(r_neq)]

    tB = []
    for lab, tab in cat + [(f"rand_eq_{i}", t) for i, t in enumerate(r_eq)] + \
            [(f"rand_neq_{i}", t) for i, t in enumerate(r_neq)]:
        for iname in ("id", "comp_dir", "transp", "comp_transp"):
            tB.append((lab, tab, iname))

    subs = [m for m in range(1, 31)]
    tC = [("comp_parcial", None), ("flip_inc0", None)]
    tC += [("subset", m) for m in subs]

    with Pool(22) as pool:
        outA = pool.map(worker_A, tA, chunksize=1)
        outB = pool.map(worker_B, tB, chunksize=1)
        outC = pool.map(worker_C, tC, chunksize=1)

    A = []
    for _, label, tab, pred, fails, first in outA:
        A.append({"label": label, "f1": tab[1], "f2": tab[2],
                  "pred": bool(pred), "fails": fails, "first": first,
                  "ok": bool(pred) == (fails == 0)})
    B = []
    for _, label, tab, iname, pred, fails, first in outB:
        B.append({"label": label, "iota": iname, "f1": tab[1], "f2": tab[2],
                  "pred": bool(pred), "fails": fails, "first": first,
                  "ok": bool(pred) == (fails == 0)})
    C = []
    for _, kind, smask, fails, first in outC:
        C.append({"kind": kind, "smask": smask, "fails": fails,
                  "first": first, "ok": fails > 0})

    canon = json.dumps({"A": A, "B": B, "C": C}, sort_keys=True,
                       separators=(",", ":"))
    res = {
        "spec_sha256": spec_sha,
        "sanity": san,
        "nA": len(A), "nB": len(B), "nC": len(C),
        "A_mismatch": [a for a in A if not a["ok"]],
        "B_mismatch": [b for b in B if not b["ok"]],
        "C_survivors": [c for c in C if not c["ok"]],
        "A_fails_summary": {
            "neq_ok": sum(1 for a in A if a["f1"] != a["f2"]
                          and a["fails"] == 0),
            "neq_total": sum(1 for a in A if a["f1"] != a["f2"]),
            "eq_witness": sum(1 for a in A if a["f1"] == a["f2"]
                              and a["fails"] > 0),
            "eq_total": sum(1 for a in A if a["f1"] == a["f2"]),
        },
        "B_fails_summary": {
            "id_transp_ok": sum(1 for b in B if b["iota"] in ("id", "transp")
                                and b["fails"] == 0),
            "id_transp_total": sum(1 for b in B if b["iota"] in ("id", "transp")),
            "comp_ok": sum(1 for b in B if b["iota"] in ("comp_dir", "comp_transp")
                           and b["ok"]),
            "comp_total": sum(1 for b in B if b["iota"] in ("comp_dir", "comp_transp")),
        },
        "C_summary": {"witness": sum(1 for c in C if c["ok"]),
                      "total": len(C)},
        "hash": hashlib.sha256(canon.encode()).hexdigest(),
        "wall_s": round(time.time() - t0, 3),
    }
    out_path = os.path.join(os.path.dirname(here), "resultados",
                            "CONJETURA-SNK_results_frozen.json")
    with open(out_path, "w") as fh:
        json.dump({**res, "A": A, "B": B, "C": C}, fh, indent=2,
                  sort_keys=True)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("A", "B", "C")}, indent=2, sort_keys=True))
    print("A[0:3]", A[:3])
    print("B[0:3]", B[:3])
    print("C", C)


if __name__ == "__main__":
    main()
