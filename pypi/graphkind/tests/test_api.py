"""Tests de la API de instrumento (`GraphKind` + `GraphKindResult`)."""

import json

import pytest

from graphkind import GraphKind, GraphKindResult, graph6, wl


def ciclo(n):
    return [(i, (i + 1) % n) for i in range(n)]


def dos_c3():
    return [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]


def arbol_binario():
    return [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
            (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12),
            (6, 13), (6, 14)]


def rook():
    E = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    u, v = a * 4 + b, c * 4 + d
                    if u < v and (a == c or b == d):
                        E.append((u, v))
    return E


def shrikhande():
    E = []
    for i in range(4):
        for j in range(4):
            u = i * 4 + j
            for di, dj in [(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)]:
                v = ((i + di) % 4) * 4 + ((j + dj) % 4)
                if u < v:
                    E.append((u, v))
    return E


def test_resultado_estructural():
    r = GraphKind("wl").transform((15, arbol_binario()))
    assert isinstance(r, GraphKindResult)
    assert r.observer == "wl" and r.n == 15
    assert r.profile == (1, 2, 4, 8)
    assert len(r.kinds) == 15 and len(r.partition) == 15
    assert r.rounds and r.rounds >= 1
    d = json.loads(json.dumps(r.as_dict()))       # serializable
    assert d["observer"] == "wl" and d["n"] == 15


def test_observador_invalido():
    with pytest.raises(ValueError):
        GraphKind("nope")
    with pytest.raises(ValueError):
        GraphKind("").transform((1, []))


def test_anclas_por_api():
    c6, dos = (6, ciclo(6)), (6, dos_c3())
    assert not GraphKind("wl").separa(c6, dos)
    assert GraphKind("kw2").separa(c6, dos)
    R, S = (16, rook()), (16, shrikhande())
    assert not GraphKind("wl").separa(R, S)
    assert not GraphKind("kw2").separa(R, S)
    assert GraphKind("kw3").separa(R, S)
    assert not GraphKind("ir1").separa(R, S)
    assert GraphKind("ir2").separa(R, S)


def test_adaptadores_misma_firma():
    n, E = 6, ciclo(6)
    sig = GraphKind("wl").signature((n, E))
    assert GraphKind("wl").signature(E) == sig              # lista de aristas
    assert GraphKind("wl").signature(graph6.to_graph6(n, E)) == sig
    assert GraphKind("wl").signature(wl.adj_from_edges(n, E)) == sig
    nx = pytest.importorskip("networkx")
    g = nx.Graph(E)
    assert GraphKind("wl").signature(g) == sig


def test_firma_igual_al_motor():
    for nombre in ("wl", "kw2", "kw3", "ir1", "ir2"):
        gk = GraphKind(nombre)
        E = arbol_binario()
        adj = wl.adj_from_edges(15, E)
        if nombre == "wl":
            ref = wl.firma(wl.wl1_colors(15, adj))
        elif nombre in ("kw2", "kw3"):
            ref = wl.firma(wl.kfwl_colors(15, adj, int(nombre[-1])))
        else:
            from graphkind import individualizacion
            ref = individualizacion.IR_k(15, E, int(nombre[-1]), "peor")
        assert gk.signature((15, E)) == ref, nombre


def test_determinismo_y_relabeling():
    import random
    rng = random.Random(7)
    E = arbol_binario()
    for nombre in ("wl", "kw2", "kw3", "ir1"):
        gk = GraphKind(nombre)
        s1 = gk.signature((15, E))
        assert gk.signature((15, E)) == s1                    # determinismo
        pi = list(range(15))
        rng.shuffle(pi)
        E2 = [(pi[u], pi[v]) for u, v in E]
        assert gk.signature((15, E2)) == s1, nombre           # relabeling


def test_universos():
    gk = GraphKind()
    assert gk.t4((15, arbol_binario())) is True
    from graphkind import universos, wl as _wl
    adj = _wl.adj_from_edges(6, ciclo(6))
    r = gk.oraculo(6, adj, lambda n, a: _wl.comp_adj(n, a),
                   f=lambda k: k, f1=1, f2=2)
    assert r["clase"] == "dual" and r["t4_predicho"] is True
    capas = [ciclo(5), [(0, 2), (2, 4)]]
    from graphkind import multicapa
    r2 = gk.t4_multicapa(5, capas, multicapa.complemento_total(5, capas))
    assert r2["particion_igual"] is True
    assert gk.t4_hipergrafo(5, 3, [(0, 1, 2), (1, 2, 3), (2, 3, 4)]) is True


def test_graph6_roundtrip():
    for n, E in [(6, ciclo(6)), (15, arbol_binario()), (4, [])]:
        s = graph6.to_graph6(n, E)
        n2, E2 = graph6.from_graph6(s)
        assert (n2, sorted(map(tuple, map(sorted, E2)))) == \
               (n, sorted(map(tuple, map(sorted, E))))
    with pytest.raises(ValueError):
        graph6.from_graph6("")


def test_fast_misma_particion_que_motor():
    """El camino rápido (numpy) induce la misma partición que el motor."""
    from graphkind import fast
    for k in (2, 3):
        E = ciclo(6)
        adj = wl.adj_from_edges(6, E)
        ref = wl.particion(wl.kfwl_colors(6, adj, k))
        rap = wl.particion(fast.kfwl_fast(6, adj, k).tolist())
        from collections import Counter
        assert (sorted(Counter(ref).values()) ==
                sorted(Counter(rap).values()))
