"""Tests del harness: corpus, observadores, mediciones y controles."""

import json
import shutil

import pytest

from graphkind_harness import bench, corpus
from graphkind_harness.observers import OBSERVADORES, observadores

# los 11 grafos no isomorfos de 4 vértices (para tests sin geng)
N4 = [
    [],
    [(0, 1)],
    [(0, 1), (0, 2)],
    [(0, 1), (2, 3)],
    [(0, 1), (0, 2), (0, 3)],
    [(0, 1), (1, 2), (2, 3)],
    [(0, 1), (1, 2), (2, 0)],
    [(0, 1), (1, 2), (2, 3), (3, 0)],
    [(0, 1), (1, 2), (2, 0), (0, 3)],
    [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3)],
    [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)],
]


def test_graph6_roundtrip():
    def enc(n, E):
        E = set(map(lambda e: tuple(sorted(e)), E))
        bits = []
        for j in range(1, n):
            for i in range(j):
                bits.append(1 if (i, j) in E else 0)
        s = chr(63 + n)
        for k in range(0, len(bits), 6):
            grupo = bits[k:k + 6] + [0] * (6 - len(bits[k:k + 6]))
            v = 0
            for b in grupo:
                v = (v << 1) | b
            s += chr(63 + v)
        return s

    for E in N4:
        n2, E2 = corpus.from_graph6(enc(4, E))
        assert n2 == 4
        assert sorted(E2) == sorted(tuple(sorted(e)) for e in E)


def test_control_negativo_y_kw3():
    grafos = corpus.corpus_pairs()
    grado = bench.colisiones(grafos, OBSERVADORES["grado"])
    kw3 = bench.colisiones(grafos, OBSERVADORES["kw3"])
    assert grado["total"] > 0        # el control negativo colisiona
    assert kw3["total"] == 0         # 3-FWL separa los pares ancla


def test_anclas():
    filas = {f["par"]: f for f in bench.anclas(observadores())}
    c6 = filas["C6 vs 2·C3"]
    assert c6["wl"] == "colisiona" and c6["kw2"] == "separa"
    rs = filas["Rook vs Shrikhande"]
    assert rs["wl"] == "colisiona" and rs["kw2"] == "colisiona"
    assert rs["kw3"] == "separa" and rs["ir2"] == "separa"
    assert rs["ir1"] == "colisiona"


def test_t4_estandar_y_multicapa():
    grafos = [(4, E) for E in N4]
    r = bench.t4_estandar(grafos)
    assert r["casos"] == 11 and r["tasa"] == 1.0
    r2 = bench.t4_multicapa(grafos, "total")
    assert r2["tasa"] == 1.0
    r3 = bench.t4_multicapa(grafos, "capa0")
    assert 0.0 <= r3["tasa"] <= 1.0


def test_control_relabeling():
    grafos = [(4, E) for E in N4]
    for f in bench.control_relabeling(grafos, observadores()):
        assert f["invarianza"] is True, f


def test_run_pairs_json():
    res = bench.run(corpus="pairs", observadores="wl,kw2,kw3")
    assert res["programa"] == "graphkind-harness"
    assert res["corpus"]["grafos"] == 6
    assert set(res["frontera"]) == {"wl", "kw2", "kw3"}
    txt = json.dumps(res)          # congelable
    assert "anclas" in json.loads(txt)
    rep = bench.reporte(res)
    assert "Colisiones" in rep and "T4 por universo" in rep


@pytest.mark.geng
def test_corpus_geng_n4():
    if not shutil.which("geng") and not corpus.geng_bin():
        pytest.skip("geng no disponible")
    grafos = corpus.corpus_geng(4, n_min=4)
    assert len(grafos) == 11       # el número conocido de grafos de n=4
    r = bench.colisiones(grafos, OBSERVADORES["wl"])
    assert r["total"] == 0         # 1-WL es completa en n<=4


def test_kfwl_fast_coincide_con_motor_pares_chicos():
    """La partición del k-FWL rápido coincide con la del motor (pares chicos)."""
    from graphkind import wl
    from graphkind.fast import firma_kfwl

    for nombre, _, E1, E2 in corpus.pares_canonicos():
        n = len(E1)
        if n > 10:
            continue
        a1, a2 = wl.adj_from_edges(n, E1), wl.adj_from_edges(n, E2)
        for k in (2, 3):
            ref = wl.separa(a1, a2, k)
            fast = firma_kfwl(n, a1, k) != firma_kfwl(n, a2, k)
            assert ref == fast, (nombre, k)


@pytest.mark.slow
def test_kfwl_fast_coincide_con_motor_n16():
    """Caso n=16 (lento con el motor de referencia)."""
    from graphkind import wl
    from graphkind.fast import firma_kfwl

    for nombre, _, E1, E2 in corpus.pares_canonicos():
        if len(E1) != 16:
            continue
        a1, a2 = wl.adj_from_edges(16, E1), wl.adj_from_edges(16, E2)
        for k in (2, 3):
            ref = wl.separa(a1, a2, k)
            fast = firma_kfwl(16, a1, k) != firma_kfwl(16, a2, k)
            assert ref == fast, (nombre, k)
