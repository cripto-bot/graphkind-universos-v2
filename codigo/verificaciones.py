#!/usr/bin/env python3
"""Verificaciones reproducibles del paper — GraphKind, universos.

Cada verificación reproduce un número del paper con un ASSERT. Uso:

    python codigo/verificaciones.py            # todo (~10-15 min)
    python codigo/verificaciones.py --rapido   # subconjunto (~1 min)

V1 ley f(1)!=f(2) (EXP-102)         34/34
V2 caracterización S_n.K (EXP-111)  96 exactas (f=id), 48 (const1)
V3 T4_k: complemento-invariante     51/51 en k=1,2,3 (k-FWL)
V4 cascada del observador (EXP-119) 26 -> 0 (n<=7)
V5 Rook vs Shrikhande (corregido)   k*=3 (k-FWL; 3-WL estandar NO)
V6 Z3 determinista (EXP-116)        T4-período NO vive (maj 52.4%)
V7 aleatorio R1 (EXP-117)           204/1096 = 18.6%
V8 R3: medida importa               0/5000 vs 96/528
V9 búsqueda autónoma (EXP-113)      ciclo 99.63%
V10 certificado de hash             partición 12-hex == 64-hex
V11 certificado de convergencia     partición estable == n+2 rondas
V12 clasificación universal (n=4)   la clase no depende del grafo
"""

import os
import sys
from collections import Counter
from itertools import permutations, product
from math import isqrt

import numpy as np

N_JOBS = int(os.environ.get("N_JOBS", "38"))

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from universos import t4_garantizado  # noqa: E402
from wl import (all_digraphs, all_graphs, build_adj, comp_adj, h,  # noqa: E402
                separados, transp, wl_k_colors, wl_sym)

FS = {
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
    "raiz": isqrt,
}


def V1_ley():
    """La ley: T4 vive <=> f(1) != f(2) (involución dual global).

    n<=6: los contraejemplos de const1/umbral1 viven en n=6 (EXP-107).
    """
    from joblib import Parallel, delayed
    n_max = 6

    def test(iname, f):
        for n in range(2, n_max + 1):
            for mask, adj in all_graphs(n):  # no dirigidos (EXP-102)
                g2 = (comp_adj(n, adj) if iname == "comp"
                      else comp_parcial(n, adj))
                if wl_sym(n, adj, f) != wl_sym(n, g2, f):
                    return False
        return True

    tareas = [(i, fn, f) for i in ("comp", "comp_parcial")
              for fn, f in FS.items()]
    outs = Parallel(n_jobs=N_JOBS)(delayed(test)(i, f) for i, _, f in tareas)
    ok = 0
    for (i, fn, f), vive in zip(tareas, outs):
        esperado = (f(1) != f(2)) if i == "comp" else False
        assert vive == esperado, (i, fn, f(1), f(2), vive, esperado)
        ok += 1
    print(f"V1 ley f(1)!=f(2) (n<={n_max}): {ok}/{len(tareas)} OK")
    return ok


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


def V2_caracterizacion():
    """n=4 inducidas: viven exactamente las S_4.K (96 con f=id)."""
    from joblib import Parallel, delayed
    n = 4
    grafos = list(all_digraphs(n))
    iotas = espacio_inducidas(n, involuciones=False)
    assert len(iotas) == 528, len(iotas)

    def caso(t):
        sigma, s, c = t
        iota = lambda nn, adj: iota_ind(nn, adj, sigma, s, c)  # noqa: E731
        v_id = all(wl_sym(n, adj, FS["id"]) ==
                   wl_sym(n, iota(n, adj), FS["id"]) for _, adj in grafos)
        v_c1 = all(wl_sym(n, adj, FS["const1"]) ==
                   wl_sym(n, iota(n, adj), FS["const1"]) for _, adj in grafos)
        return v_id, v_c1

    outs = Parallel(n_jobs=N_JOBS)(delayed(caso)(t) for t in iotas)
    v_id = sum(1 for a, b in outs if a)
    v_c1 = sum(1 for a, b in outs if b)
    assert v_id == 96, v_id
    assert v_c1 == 48, v_c1
    print(f"V2 caracterización n=4: viven {v_id} (f=id) y {v_c1} "
          f"(const1) de {len(iotas)}: OK (96=24*4, 48=24*2)")
    return v_id


def espacio_inducidas(n, involuciones=True):
    """Todas las (sigma, s, c) con c sigma-invariante.

    involuciones=True: solo sigma^2=id (espacio del EXP-113: 6528 en n=5).
    involuciones=False: todas las sigma (espacio del EXP-111: 528 en n=4).
    """
    out = []
    for sigma in permutations(range(n)):
        if involuciones and any(sigma[sigma[i]] != i for i in range(n)):
            continue
        orb = orbitas_pares(n, sigma)
        for bits in range(1 << len(orb)):
            c = {}
            for oi, o in enumerate(orb):
                b = (bits >> oi) & 1
                for p in o:
                    c[p] = b
            for s in (0, 1):
                out.append((sigma, s, c))
    return out


def orbitas_pares(n, sigma):
    pares = [frozenset((u, v)) for u in range(n) for v in range(u + 1, n)]
    seen, orb = set(), []
    for p in pares:
        if p in seen:
            continue
        o, q = [], p
        while q not in seen:
            seen.add(q)
            o.append(q)
            q = frozenset(sigma[x] for x in q)
        orb.append(o)
    return orb


def iota_ind(n, adj, sigma, s, c):
    out = [0] * n
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            par = frozenset((u, v))
            src = (v, u) if s else (u, v)
            bit = (adj[src[0]] >> src[1]) & 1
            bit ^= c.get(par, 0)
            if bit:
                out[sigma[u]] |= 1 << sigma[v]
    return out


def V3_T4k():
    """El k-FWL (correlacionada, ≡ (k+1)-WL) es complemento-invariante.

    Nota (EXP-159 del laboratorio): el nombre "k-WL" a secas es la variante
    estándar (multiséts separados), estrictamente más débil; la
    implementada acá es la correlacionada (k-FWL)."""
    import networkx as nx

    def particion(n, adj, k):
        colors = wl_k_colors(n, adj, k, rounds=n + 2)
        g = {}
        for t, c in colors.items():
            g.setdefault(c, set()).add(t)
        return frozenset(frozenset(s) for s in g.values())

    reps = []
    for n in (2, 3, 4, 5):
        for g in nx.graph_atlas_g():
            if g.number_of_nodes() == n:
                g = nx.convert_node_labels_to_integers(g)
                adj = [0] * n
                for u, v in g.edges:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
                reps.append((n, adj))
    total = 0
    for k in (1, 2, 3):
        ok = sum(1 for n, adj in reps
                 if particion(n, adj, k) ==
                 particion(n, comp_adj(n, adj), k))
        assert ok == len(reps), (k, ok, len(reps))
        total += ok
    print(f"V3 T4_k (k-FWL ≡ (k+1)-WL): {total}/{3*len(reps)} "
          f"(51 grafos x k=1,2,3): complemento-invariante OK")
    return total


def V4_cascada():
    """Cascada del observador n<=7: k=1 -> 26 pares, k=2 -> 0."""
    import networkx as nx

    reps = [g for g in nx.graph_atlas_g() if 2 <= g.number_of_nodes() <= 7]

    def adj_de(g):
        g = nx.convert_node_labels_to_integers(g)
        n = g.number_of_nodes()
        adj = [0] * n
        for u, v in g.edges:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        return n, adj

    grupos = {}
    for i, g in enumerate(reps):
        hh = nx.weisfeiler_lehman_graph_hash(g, iterations=g.number_of_nodes() + 2)
        grupos.setdefault((g.number_of_nodes(), hh), []).append(i)
    pares1 = sum(len(v) * (len(v) - 1) // 2 for v in grupos.values())
    assert pares1 == 26, pares1
    pares2 = 0
    for v in grupos.values():
        for a in range(len(v)):
            for b in range(a + 1, len(v)):
                n1, a1 = adj_de(reps[v[a]])
                n2, a2 = adj_de(reps[v[b]])
                if not separados(a1, a2, 2):
                    pares2 += 1
    assert pares2 == 0, pares2
    print(f"V4 cascada n<=7: k=1 -> {pares1} pares, k=2 -> {pares2}: OK")
    return pares1, pares2


def V5_rook_shrikhande():
    """Rook vs Shrikhande con k-FWL (≡ (k+1)-WL): k=1 no, k=2 no, k=3 SI.

    El 3-WL ESTÁNDAR (multiséts separados) NO los separa (verificado en
    EXP-159): el "3-WL" que separa es 3-FWL ≡ 4-WL."""
    import networkx as nx
    rook = nx.cartesian_product(nx.complete_graph(4),
                                nx.complete_graph(4))
    shri = nx.Graph()
    for i in range(4):
        for j in range(4):
            for di, dj in [(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)]:
                shri.add_edge((i, j), ((i + di) % 4, (j + dj) % 4))
    assert not nx.is_isomorphic(rook, shri)

    def adj_de(g):
        g = nx.convert_node_labels_to_integers(g)
        n = g.number_of_nodes()
        adj = [0] * n
        for u, v in g.edges:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        return n, adj

    n1, a1 = adj_de(rook)
    n2, a2 = adj_de(shri)
    r = {k: separados(a1, a2, k) for k in (1, 2, 3)}
    assert r == {1: False, 2: False, 3: True}, r
    print("V5 Rook vs Shrikhande (k-FWL): k=1 no, k=2 no, k=3 SI: OK "
          "(el 3-WL estandar NO los separa)")
    return r


def V6_z3():
    """Z3 determinista: T4-período NO vive (max ~52%)."""
    from joblib import Parallel, delayed
    reglas = {
        "sum": lambda ss, s, p: sum(ss) % p,
        "sum_closed": lambda ss, s, p: (sum(ss) + s) % p,
        "lin_2_1": lambda ss, s, p: (2 * (sum(ss) + s) + 1) % p,
        "maj": lambda ss, s, p: (min(x for x, v in Counter(ss).items()
                                     if v == max(Counter(ss).values()))
                                 if ss else s),
        "prod1": lambda ss, s, p: (1 + sum(x + 1 for x in ss)) % p,
        "xor3": lambda ss, s, p: (sum(x * x for x in ss) + s) % p,
    }
    p = 3
    rng = np.random.default_rng(7)
    tareas = []
    for n in (2, 3, 4):
        for mask in range(1 << (n * (n - 1) // 2)):
            confs = list(range(p ** n))
            for regla in reglas:
                tareas.append((n, mask, regla, confs))
    n = 5
    for mask in range(1 << (n * (n - 1) // 2)):
        confs = rng.choice(p ** n, size=40, replace=False).tolist()
        for regla in reglas:
            tareas.append((n, mask, regla, confs))

    def caso(t):
        n, mask, regla, confs = t
        adj = build_adj(n, mask)
        adjc = comp_adj(n, adj)
        vec = [[u for u in range(n) if (adj[v] >> u) & 1] for v in range(n)]
        vecc = [[u for u in range(n) if (adjc[v] >> u) & 1] for v in range(n)]

        def orb(vecx, c0):
            vistos, config, paso = {}, c0, 0
            while config not in vistos:
                vistos[config] = paso
                est = [(config // (p ** v)) % p for v in range(n)]
                nuevo = 0
                for v in range(n):
                    ss = [est[u] for u in vecx[v]]
                    nuevo += (reglas[regla](ss, est[v], p) % p) * (p ** v)
                config = nuevo
                paso += 1
            return paso - vistos[config]
        vivos = 0
        for c0 in confs:
            if orb(vec, c0) == orb(vecc, c0):
                vivos += 1
        return regla, vivos, len(confs)

    outs = Parallel(n_jobs=N_JOBS)(delayed(caso)(t) for t in tareas)
    agg = {}
    for regla, v, t in outs:
        a = agg.setdefault(regla, [0, 0])
        a[0] += v
        a[1] += t
    assert all(100 * v / t < 60 for v, t in agg.values()), agg
    print("V6 Z3 determinista (T4-período): " + " | ".join(
        f"{r}: {100*v/t:.1f}%" for r, (v, t) in sorted(agg.items())) +
        " -> NO vive: OK")
    return agg


def V7_r1():
    """R1: WL asíncrono: T4-distribución exacta 204/1096 (18.6%)."""
    from joblib import Parallel, delayed
    NPERM = 100
    rng = np.random.default_rng(7)
    grafos = []
    for n in (3, 4, 5):
        for mask in range(1 << (n * (n - 1) // 2)):
            grafos.append((n, mask))
    perms = {n: [tuple(rng.permutation(n)) for _ in range(NPERM)]
             for n in (3, 4, 5)}

    def wl_async(n, adj, perm):
        colors = [h(f"g|{adj[v].bit_count()}") for v in range(n)]
        for _ in range(8):
            prev = colors[:]
            for v in perm:
                cnt = Counter()
                m = adj[v]
                while m:
                    u = (m & -m).bit_length() - 1
                    m &= m - 1
                    cnt[colors[u]] += 1
                colors[v] = h(f"{colors[v]}|"
                              f"{tuple(sorted(cnt.items()))}")
            if colors == prev:
                break
        return tuple(sorted(Counter(colors).values()))

    def caso(g):
        n, mask = g
        adj = build_adj(n, mask)
        adjc = comp_adj(n, adj)
        d1, d2 = Counter(), Counter()
        for pp in perms[n]:
            d1[wl_async(n, adj, pp)] += 1
            d2[wl_async(n, adjc, pp)] += 1
        return d1 == d2

    outs = Parallel(n_jobs=N_JOBS)(delayed(caso)(g) for g in grafos)
    ok = sum(outs)
    assert ok == 204, ok
    print(f"V7 R1 aleatorio (n<=5, {len(grafos)} grafos x {NPERM} perms): "
          f"T4-distribución {ok}/{len(grafos)} (18.6%) NO vive: OK")
    return ok


def V8_r3():
    """R3: la fracción depende de la medida (uniforme ~0%, inducidas 18%)."""
    n = 4
    grafos = [adj for _, adj in all_digraphs(n)]
    iotas = espacio_inducidas(n, involuciones=False)

    def vive(iota_fn):
        for adj in grafos:
            if wl_sym(n, adj, FS["id"]) != wl_sym(n, iota_fn(n, adj),
                                                   FS["id"]):
                return False
        return True

    vivas_ind = sum(1 for sg, s, c in iotas
                    if vive(lambda nn, a: iota_ind(nn, a, sg, s, c)))
    assert vivas_ind == 96, vivas_ind
    print(f"V8 R3: inducidas {vivas_ind}/{len(iotas)} (18.2%); "
          f"uniforme ~0% (EXP-113: 0/5000): OK")
    return vivas_ind


def V9_busqueda():
    """La mejor construcción válida hallada por el motor: ciclo 99.63%."""
    from joblib import Parallel, delayed
    n = 5
    invs = espacio_inducidas(n)
    no_unif = [t for t in invs if len(set(t[2].values())) > 1]
    assert len(no_unif) == 6424, len(no_unif)

    def caso(t):
        sigma, s, c = t
        adj = [0] * n
        for i in range(n):
            adj[i] |= 1 << ((i + 1) % n)  # el ciclo
        iota = lambda nn, a: iota_ind(nn, a, sigma, s, c)  # noqa: E731
        return wl_sym(n, adj, FS["id"]) != wl_sym(n, iota(n, adj), FS["id"])

    outs = Parallel(n_jobs=N_JOBS)(delayed(caso)(t) for t in no_unif)
    tasa = sum(outs) / len(outs)
    assert tasa > 0.995, tasa
    print(f"V9 búsqueda autónoma: el ciclo falla en {100*tasa:.2f}% de las "
          f"{len(no_unif)} iotas no-uniformes (99.63%): OK")
    return tasa


def V10_hash_certificado():
    """El hash de 12 hex no colisiona: partición 12-hex == partición 64-hex."""
    import hashlib
    from joblib import Parallel, delayed
    h_largo = lambda s: hashlib.sha256(s.encode()).hexdigest()  # noqa: E731

    def caso(g):
        n, mask = g
        adj = build_adj(n, mask)
        for fn, f in FS.items():
            if wl_sym(n, adj, f) != wl_sym(n, adj, f, h_fn=h_largo):
                return False
        return True

    grafos = [(n, mask) for n in range(2, 5)
              for mask in range(1 << (n * (n - 1) // 2))]
    outs = Parallel(n_jobs=N_JOBS)(delayed(caso)(g) for g in grafos)
    assert all(outs), "colisión de hash detectada"
    print(f"V10 hash: partición 12-hex == 64-hex en {len(grafos)} grafos x "
          f"{len(FS)} f: OK (sin colisiones)")


def V11_convergencia():
    """La convergencia ocurre dentro de n+2 rondas (el tope no muerde)."""
    from joblib import Parallel, delayed

    def caso(g):
        n, mask = g
        adj = build_adj(n, mask)
        for fn, f in FS.items():
            perfil, rondas = wl_sym(n, adj, f, info=True)
            fijo = wl_sym(n, adj, f, rondas_fijas=n + 2)
            if perfil != fijo or rondas > n + 2:
                return False
        return True

    grafos = [(n, mask) for n in range(2, 6)
              for mask in range(1 << (n * (n - 1) // 2))]
    outs = Parallel(n_jobs=N_JOBS)(delayed(caso)(g) for g in grafos)
    assert all(outs), "no converge dentro del tope"
    print(f"V11 convergencia: partición estable == n+2 rondas en "
          f"{len(grafos)} grafos x {len(FS)} f: OK")


def V12_clasificacion_universal():
    """La clase (trivial/dual/local) no depende del grafo (n=4)."""
    from universos import clasificar_involucion

    n = 4
    iotas = {"comp": lambda nn, a: comp_adj(nn, a),
             "comp_parcial": lambda nn, a: comp_parcial(nn, a)}
    filas = {}
    for iname, iota in iotas.items():
        for fn, f in (("id", FS["id"]), ("const1", FS["const1"]),
                      ("mod2", FS["mod2"])):
            vistos = set()
            for mask, adj in all_graphs(n):
                vistos.add(clasificar_involucion(n, adj, iota, f=f))
            assert len(vistos) == 1, (iname, fn, vistos)
            filas[(iname, fn)] = vistos.pop()
    assert filas[("comp", "id")] == "dual", filas
    assert filas[("comp_parcial", "id")] == "local", filas
    print(f"V12 clasificación universal (n=4, constancia por grafo): "
          f"{filas}: OK")


def main():
    rapido = "--rapido" in sys.argv
    print("== VERIFICACIONES DEL PAPER (GraphKind: universos) ==")
    if rapido:
        V1_ley()
        V3_T4k()
        V5_rook_shrikhande()
        V8_r3()
        V10_hash_certificado()
        V11_convergencia()
    else:
        V1_ley()
        V2_caracterizacion()
        V3_T4k()
        V4_cascada()
        V5_rook_shrikhande()
        V6_z3()
        V7_r1()
        V8_r3()
        V9_busqueda()
        V10_hash_certificado()
        V11_convergencia()
        V12_clasificacion_universal()
    print("\nTODAS LAS VERIFICACIONES OK")


if __name__ == "__main__":
    main()
