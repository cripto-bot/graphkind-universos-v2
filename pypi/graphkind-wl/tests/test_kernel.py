"""Anchors and probes for the GraphKind WL kernel.

Expected values come from the frozen results of the GraphKind laboratory
(SG-02/SG-03/EXP-159): the union test criterion, exactly as the engine.
"""

from collections import Counter

import pytest

from graphkind_wl import (
    adj_from_edges,
    complement,
    kfwl_colors,
    particion,
    perfil,
    separa,
    t4,
    wl1_colors,
)


def ciclo(n):
    return [(i, (i + 1) % n) for i in range(n)]


def dos_c3():
    return [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]


def rook():
    """4x4 rook graph = K4 [] K4 (SRG(16,6,2,2))."""
    edges = []
    for a in range(4):
        for b in range(4):
            u = a * 4 + b
            for c in range(4):
                for d in range(4):
                    v = c * 4 + d
                    if u < v and (a == c or b == d):
                        edges.append((u, v))
    return edges


def shrikhande():
    """Shrikhande graph (SRG(16,6,2,2), Cayley on Z4 x Z4)."""
    edges = []
    for i in range(4):
        for j in range(4):
            u = i * 4 + j
            for di, dj in [(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)]:
                v = ((i + di) % 4) * 4 + ((j + dj) % 4)
                if u < v:
                    edges.append((u, v))
    return edges


def petersen():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    edges += [(5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
    edges += [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
    return edges


def prisma():
    """Pentagonal prism C5 x K2."""
    edges = ciclo(5)
    edges += [(i + 5, (i + 1) % 5 + 5) for i in range(5)]
    edges += [(i, i + 5) for i in range(5)]
    return edges


def test_ancla_c6_vs_2c3():
    a1 = adj_from_edges(6, ciclo(6))
    a2 = adj_from_edges(6, dos_c3())
    assert not separa(a1, a2, 1)      # 1-WL colisiona
    assert separa(a1, a2, 2)          # 2-FWL (3-WL) separa
    assert separa(a1, a2, 3)


def test_ancla_petersen_vs_prisma():
    a1 = adj_from_edges(10, petersen())
    a2 = adj_from_edges(10, prisma())
    assert not separa(a1, a2, 1)
    assert separa(a1, a2, 2)


def test_ancla_rook_vs_shrikhande():
    a1 = adj_from_edges(16, rook())
    a2 = adj_from_edges(16, shrikhande())
    assert not separa(a1, a2, 1)      # 1-WL colisiona
    assert not separa(a1, a2, 2)      # 3-WL estandar NO separa
    assert separa(a1, a2, 3)          # 3-FWL (4-WL) SI separa


def test_t4_particion_complemento():
    # arbol binario (2,3), n=15
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
             (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12),
             (6, 13), (6, 14)]
    adj = adj_from_edges(15, edges)
    assert t4(adj)
    assert t4(adj_from_edges(6, ciclo(6)))
    assert t4(adj_from_edges(16, rook()))


def test_particion_y_perfil():
    adj = adj_from_edges(6, ciclo(6))
    assert perfil(wl1_colors(6, adj)) == (6,)
    assert particion(wl1_colors(6, adj)) == [0] * 6
    adj2 = adj_from_edges(15, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
                               (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12),
                               (6, 13), (6, 14)])
    assert perfil(wl1_colors(15, adj2)) == (1, 2, 4, 8)


def test_rondas_fijas_y_determinismo():
    adj = adj_from_edges(15, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
                              (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12),
                              (6, 13), (6, 14)])
    assert wl1_colors(15, adj, rounds=0) == wl1_colors(15, adj, rounds=0)
    assert perfil(wl1_colors(15, adj, rounds=0)) == (1, 6, 8)
    col = kfwl_colors(6, adj_from_edges(6, ciclo(6)), 2)
    assert len(col) == 36
    assert len(set(col.values())) == 4          # diagonal, d=1, d=2, d=3
    assert sorted(Counter(col.values()).values()) == [6, 6, 12, 12]


def test_errores():
    with pytest.raises(ValueError):
        kfwl_colors(3, adj_from_edges(3, ciclo(3)), 1)
    with pytest.raises(ValueError):
        adj_from_edges(2, [(0, 0)])
