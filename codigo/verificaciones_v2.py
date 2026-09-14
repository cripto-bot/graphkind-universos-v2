#!/usr/bin/env python3
"""Verificaciones v2 — el arco de universos (multicapa, hipergrafos, dual).

    python codigo/verificaciones_v2.py

V13 multicapa: total vive; POR CAPA muere en la canónica (coherencia).
V14 hipergrafos 3-uniformes: T4 vive (n<=5 exhaustivo + muestra n=6).
V15 dual por aridad: partición garantizada + ahorro (n=4 exhaustivo).
V16 aridades mezcladas: por aridad VIVE (el refinamiento repara).
"""

import random
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from multicapa import (refinar_conjunto, complemento_total,  # noqa: E402
                       complemento_capa, complemento_canales, t4)
from hipergrafo import (t4_k_uniforme, t4_mezclado,  # noqa: E402
                        refine_dual_mezclado, refinar_mezclado,
                        complemento_k_uniforme)
from individualizacion import IR_k  # noqa: E402
from wl import separados, build_adj  # noqa: E402


def _grafos(n):
    """Todos los grafos etiquetados de n vértices (lista de aristas)."""
    pares = list(combinations(range(n), 2))
    out = []
    for mask in range(1 << len(pares)):
        out.append([pares[i] for i in range(len(pares)) if (mask >> i) & 1])
    return out


def V13_multicapa():
    """Ley de canales: total vive; por-capa muere (canónica); ordenada vive."""
    total = per_capa_falla = ord_vive = canales_vive = objetos = 0
    for n in (3, 4):
        gs = _grafos(n)
        for E1 in gs:
            for E2 in gs:
                capas = [E1, E2]
                objetos += 1
                if t4(n, capas, complemento_total(n, capas),
                      "canonica")["particion_igual"]:
                    total += 1
                for ell in (0, 1):
                    if not t4(n, capas, complemento_capa(n, capas, ell),
                              "canonica")["particion_igual"]:
                        per_capa_falla += 1
                    if t4(n, capas, complemento_capa(n, capas, ell),
                          "ordenada")["particion_igual"]:
                        ord_vive += 1
                if t4(n, capas, complemento_canales(capas, [1, 0]),
                      "canonica")["particion_igual"]:
                    canales_vive += 1
    assert total == objetos, (total, objetos)
    assert per_capa_falla > 0, "la ley de canales no se reproduce"
    assert ord_vive == 2 * objetos, ord_vive
    assert canales_vive == objetos, canales_vive
    print(f"V13 multicapa: total {total}/{objetos} vive | por-capa "
          f"canónica falla {per_capa_falla} | por-capa ordenada "
          f"{ord_vive}/{2*objetos} | canales {canales_vive}/{objetos}: OK")


def V14_hipergrafos():
    """3-uniformes: T4 vive (exhaustivo n<=5 + muestra n=6)."""
    vivos = objetos = 0
    for n in (3, 4, 5):
        for mask in range(1 << len(list(combinations(range(n), 3)))):
            trios = [t for i, t in enumerate(combinations(range(n), 3))
                     if (mask >> i) & 1]
            objetos += 1
            vivos += int(t4_k_uniforme(n, 3, trios))
    rng = random.Random(7)
    tri6 = list(combinations(range(6), 3))
    muestra = 0
    for _ in range(5000):
        H = [t for t in tri6 if rng.random() < 0.5]
        muestra += 1
        vivos += int(t4_k_uniforme(6, 3, H))
    assert vivos == objetos + muestra, (vivos, objetos + muestra)
    print(f"V14 hipergrafos 3-uniformes: {vivos}/{objetos+muestra} "
          f"(n<=5 exhaustivo + muestra n=6): OK")


def V15_dual_aridad():
    """Dual por aridad: partición garantizada + ahorro (n=4 exhaustivo)."""
    todos2 = list(combinations(range(4), 2))
    todos3 = list(combinations(range(4), 3))
    ok = objetos = a_orig = a_dual = 0
    for m2 in range(1 << len(todos2)):
        e2 = [todos2[i] for i in range(len(todos2)) if (m2 >> i) & 1]
        for m3 in range(1 << len(todos3)):
            e3 = [todos3[i] for i in range(len(todos3)) if (m3 >> i) & 1]
            objetos += 1
            p_orig, _ = refinar_mezclado(4, e2, e3, "canonica")
            p_dual, lados = refine_dual_mezclado(4, e2, e3, "canonica")
            ok += int(p_orig == p_dual)
            c2 = complemento_k_uniforme(4, 2, e2)
            c3 = complemento_k_uniforme(4, 3, e3)
            a_orig += len(e2) + len(e3)
            a_dual += ((len(c2) if lados[0] == "e2bar" else len(e2))
                       + (len(c3) if lados[1] == "e3bar" else len(e3)))
    assert ok == objetos, (ok, objetos)
    assert a_dual <= a_orig, (a_dual, a_orig)
    print(f"V15 dual por aridad: partición {ok}/{objetos} | aristas "
          f"{a_orig} -> {a_dual} (ahorro {100*(1-a_dual/a_orig):.1f}%): OK")


def V16_mezclado():
    """Aridades mezcladas: por aridad VIVE (el refinamiento repara)."""
    todos2 = list(combinations(range(4), 2))
    todos3 = list(combinations(range(4), 3))
    total = aridad = objetos = 0
    for m2 in range(1 << len(todos2)):
        e2 = [todos2[i] for i in range(len(todos2)) if (m2 >> i) & 1]
        for m3 in range(1 << len(todos3)):
            e3 = [todos3[i] for i in range(len(todos3)) if (m3 >> i) & 1]
            objetos += 1
            total += int(t4_mezclado(4, e2, e3, "total", "canonica"))
            aridad += int(t4_mezclado(4, e2, e3, "aridad2", "canonica"))
    assert total == objetos and aridad == objetos, (total, aridad, objetos)
    print(f"V16 aridades mezcladas (n=4 exhaustivo): total {total}/{objetos} "
          f"| por aridad {aridad}/{objetos} VIVE (reparo): OK")


def _grafos_unicos(n):
    """Grafos no isomorfos de n vértices (canónica por fuerza bruta)."""
    from itertools import permutations
    pares = list(combinations(range(n), 2))
    vistos = {}
    for mask in range(1 << len(pares)):
        E = [pares[i] for i in range(len(pares)) if (mask >> i) & 1]
        es = tuple(sorted(tuple(sorted(e)) for e in E))
        mejor = None
        for p in permutations(range(n)):
            k = tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in es))
            if mejor is None or k < mejor:
                mejor = k
        if mejor not in vistos:
            vistos[mejor] = E
    return list(vistos.values())


def V17_cociente_complemento():
    """T4 tiene precio: el invariante completo identifica G con su
    complemento; el cociente fusiona (N - autocomplementarios)/2 pares.

    (SG-01: en n<=8 son 6 168 pares; acá se ejecuta el análogo n<=5.)"""
    import networkx as nx
    from wl import wl_sym
    N = identificados = autocomp = 0
    for n in (1, 2, 3, 4, 5):
        for E in _grafos_unicos(n):
            N += 1
            adj = build_adj(n, sum(1 << i for i, e in enumerate(
                combinations(range(n), 2)) if list(e) in
                [sorted(x) for x in E]))
            g = nx.Graph()
            g.add_nodes_from(range(n))
            g.add_edges_from(E)
            gc = nx.complement(g)
            # clave = perfil WL (complemento-invariante por T4)
            if wl_sym(n, adj, lambda k: k) == wl_sym(
                    n, build_adj(n, sum(1 << i for i, e in enumerate(
                        combinations(range(n), 2))
                        if list(e) in [sorted(x) for x in gc.edges])),
                    lambda k: k):
                identificados += 1
            if nx.is_isomorphic(g, gc):
                autocomp += 1
    assert identificados == N, (identificados, N)
    assert (N - autocomp) % 2 == 0
    print(f"V17 cociente por complemento (n<=5): {N} grafos | "
          f"identificados {identificados} | autocomplementarios {autocomp} "
          f"| pares fusionados {(N-autocomp)//2} (SG-01 n<=8: 6 168): OK")


def V18_ir_anclas():
    """IR_1 NO separa Rook/Shrikhande; IR_2 SÍ (SG-02/03)."""
    import networkx as nx
    rook = nx.cartesian_product(nx.complete_graph(4), nx.complete_graph(4))
    shri = nx.Graph()
    for i in range(4):
        for j in range(4):
            for di, dj in [(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)]:
                shri.add_edge((i, j), ((i + di) % 4, (j + dj) % 4))
    def datos(g):
        g = nx.convert_node_labels_to_integers(g)
        return g.number_of_nodes(), sorted(tuple(sorted(e)) for e in g.edges)
    n1, E1 = datos(rook)
    n2, E2 = datos(shri)
    assert IR_k(n1, E1, 1, "peor") == IR_k(n2, E2, 1, "peor")
    assert IR_k(n1, E1, 2, "peor") != IR_k(n2, E2, 2, "peor")
    print("V18 IR: IR_1 no separa Rook/Shrikhande; IR_2 SÍ "
          "(i*=2): OK")


def main():
    print("== VERIFICACIONES v2 (arco de universos) ==")
    V13_multicapa()
    V14_hipergrafos()
    V15_dual_aridad()
    V16_mezclado()
    V17_cociente_complemento()
    V18_ir_anclas()
    print("\nTODAS LAS VERIFICACIONES v2 OK")


if __name__ == "__main__":
    main()
