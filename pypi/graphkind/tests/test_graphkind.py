"""Tests del motor GraphKind (anclas y leyes, contra los freezes del lab).

Rápidos (~10 s). Las suites completas V1–V19 se corren con
`pytest -m slow` (requieren numpy).
"""

from collections import Counter

import pytest

from graphkind import hipergrafo, individualizacion, multicapa, universos, wl
from graphkind.wl import adj_from_edges, complement, separa, t4


def ciclo(n):
    return [(i, (i + 1) % n) for i in range(n)]


def dos_c3():
    return [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]


def arbol_binario():
    return [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
            (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12),
            (6, 13), (6, 14)]


def rook():
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
    return [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
            (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
            (0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]


def prisma():
    return ciclo(5) + [(i + 5, (i + 1) % 5 + 5) for i in range(5)] + \
        [(i, i + 5) for i in range(5)]


def test_anclas_wl():
    a1, a2 = adj_from_edges(6, ciclo(6)), adj_from_edges(6, dos_c3())
    assert not separa(a1, a2, 1) and separa(a1, a2, 2) and separa(a1, a2, 3)
    b1, b2 = adj_from_edges(10, petersen()), adj_from_edges(10, prisma())
    assert not separa(b1, b2, 1) and separa(b1, b2, 2)
    c1, c2 = adj_from_edges(16, rook()), adj_from_edges(16, shrikhande())
    assert not separa(c1, c2, 1)
    assert not separa(c1, c2, 2)          # 3-WL estandar NO separa
    assert separa(c1, c2, 3)              # 3-FWL (4-WL) SI separa


def test_t4_particion():
    adj = adj_from_edges(15, arbol_binario())
    assert t4(adj)
    assert wl.perfil(wl.wl1_colors(15, adj)) == (1, 2, 4, 8)


def test_ley_universos():
    assert universos.t4_garantizado(1, 2, "dual") is True
    assert universos.t4_garantizado(1, 1, "dual") is False
    assert universos.t4_garantizado(1, 1, "trivial") is True
    assert universos.t4_garantizado(0, 1, "local") is False


def test_oraculo_complemento():
    n = 6
    adj = adj_from_edges(n, ciclo(6))          # C6 no es autocomplementario
    r = universos.oraculo(n, adj, lambda n, a: complement(n, a),
                          f=lambda k: k, f1=1, f2=2)
    assert r["clase"] == "dual"
    assert r["t4_predicho"] is True
    r2 = universos.oraculo(n, adj, lambda n, a: complement(n, a),
                           f=lambda k: 1, f1=1, f2=1)
    assert r2["t4_predicho"] is False   # f colapsa 1 y 2
    # C5 es autocomplementario: la clase es "trivial"
    n5 = 5
    r3 = universos.oraculo(n5, adj_from_edges(n5, ciclo(5)),
                           lambda n, a: complement(n, a),
                           f=lambda k: k, f1=1, f2=2)
    assert r3["clase"] == "trivial"


def test_multicapa_dualidad_total_y_canales():
    n = 5
    E1 = ciclo(5)
    E2 = [(0, 2), (2, 4)]
    capas = [E1, E2]
    r = multicapa.t4(n, capas, multicapa.complemento_total(n, capas))
    assert r["perfil_igual"] and r["particion_igual"]
    r2 = multicapa.t4(n, capas, multicapa.complemento_canales(capas, [1, 0]))
    assert r2["particion_igual"]          # el orden de canales no cambia la particion


def test_hipergrafo_k_uniforme():
    n = 5
    aristas = [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
    assert hipergrafo.t4_k_uniforme(n, 3, aristas) is True


def test_individualizacion_rook_shrikhande():
    R, S = rook(), shrikhande()
    assert (individualizacion.IR_k(16, R, 1, "peor") ==
            individualizacion.IR_k(16, S, 1, "peor"))       # IR_1 no separa
    assert (individualizacion.IR_k(16, R, 2, "peor") !=
            individualizacion.IR_k(16, S, 2, "peor"))       # IR_2 si (i*=2)


def test_suites_importables():
    from graphkind import verificaciones, verificaciones_v2  # noqa: F401
    assert callable(verificaciones.main)
    assert callable(verificaciones_v2.main)


@pytest.mark.slow
def test_suites_completas():
    """V1–V19 completas (requieren numpy y los datos del repo; no en el paquete).

    En el repo: `cd pypi/graphkind && pytest -m slow` con GRAPHKIND_REPO=1.
    """
    import os
    if not os.environ.get("GRAPHKIND_REPO"):
        pytest.skip("las suites V1-V19 necesitan los datos del repositorio")
    from graphkind import verificaciones, verificaciones_v2
    verificaciones.main()
    verificaciones_v2.main()
