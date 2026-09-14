#!/usr/bin/env python3
"""Figuras v1 de datos (t4-particion, t4-evolucion) — wording preciso (v2).

Regla: lo que T4 preserva es la PARTICIÓN de clases; las etiquetas de
color son hashes arbitrarios y PUEDEN diferir entre G y Ḡ. Genera:
  assets/t4-particion.svg
  assets/t4-evolucion.svg
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "assets"
PALETA = ["#9a7b1f", "#26557a", "#a33", "#0b6b3a", "#6b3fa0", "#b06a1f"]


def to_adj(g):
    g = nx.convert_node_labels_to_integers(g)
    n = g.number_of_nodes()
    adj = [0] * n
    for u, v in g.edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def comp_adj(n, adj):
    out = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if not (adj[i] >> j) & 1:
                out[i] |= 1 << j
                out[j] |= 1 << i
    return out


def _h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def clases_wl(n, adj):
    colors = [_h(f"g|{adj[v].bit_count()}") for v in range(n)]
    for _ in range(n + 2):
        new = []
        for v in range(n):
            cnt = Counter()
            m = adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                cnt[colors[u]] += 1
            new.append(_h(f"{colors[v]}|{tuple(sorted(cnt.items()))}"))
        colors = new
    idx = {c: i for i, c in enumerate(sorted(set(colors)))}
    return [idx[c] for c in colors]


def clases_wl_ronda(n, adj, k):
    colors = [_h(f"g|{adj[v].bit_count()}") for v in range(n)]
    for _ in range(k):
        new = []
        for v in range(n):
            cnt = Counter()
            m = adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                cnt[colors[u]] += 1
            new.append(_h(f"{colors[v]}|{tuple(sorted(cnt.items()))}"))
        colors = new
    rep = {}
    for v in range(n):
        rep.setdefault(colors[v], v)
    idx = {rep[c]: i for i, c in enumerate(sorted(rep))}
    return [idx[rep[colors[v]]] for v in range(n)]


def _dibujar(n, adj, cl, pos, ax, titulo):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for u in range(n):
        for v in range(u + 1, n):
            if (adj[u] >> v) & 1:
                G.add_edge(u, v)
    colores = [PALETA[c % len(PALETA)] for c in cl]
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc", width=1.6)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colores,
                           node_size=430, edgecolors="white", linewidths=1.5)
    ax.set_title(titulo, fontsize=13, color="#0d0d0d")
    ax.axis("off")


def fig_t4(destino):
    n = 8
    adj = to_adj(nx.hypercube_graph(3))
    adjc = comp_adj(n, adj)
    cg = clases_wl(n, adj)
    cc = clases_wl(n, adjc)
    G0 = nx.convert_node_labels_to_integers(nx.hypercube_graph(3))
    pos = nx.spring_layout(G0, seed=7)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.6))
    _dibujar(n, adj, cg, pos, axes[0], "G = Q₃")
    _dibujar(n, adjc, cc, pos, axes[1], "Ḡ (complemento)")
    fig.suptitle("T4: la misma PARTICIÓN en G y Ḡ "
                 "(las etiquetas de color son arbitrarias)",
                 fontsize=12, color="#0d0d0d")
    fig.tight_layout()
    fig.savefig(destino, format="svg", facecolor="white")
    plt.close(fig)


def fig_t4_evolucion(destino):
    n = 15
    G = nx.convert_node_labels_to_integers(nx.balanced_tree(2, 3))
    adj = to_adj(G)
    adjc = comp_adj(n, adj)
    pos = {0: (0.0, 3.0)}
    nivel = {1: [(-2.0, 2.0), (2.0, 2.0)],
             2: [(-3.0, 1.0), (-1.0, 1.0), (1.0, 1.0), (3.0, 1.0)],
             3: [(-3.5, 0.0), (-2.5, 0.0), (-1.5, 0.0), (-0.5, 0.0),
                 (0.5, 0.0), (1.5, 0.0), (2.5, 0.0), (3.5, 0.0)]}
    nodos = sorted(G.nodes)
    for li, xs in nivel.items():
        hijos = [v for v in nodos
                 if len(nx.shortest_path(G, 0, v)) - 1 == li]
        for v, xy in zip(sorted(hijos), xs):
            pos[v] = xy
    trayectorias = {}
    for clave, a in (("G", adj), ("Gbar", adjc)):
        trayectorias[clave] = [len(set(clases_wl_ronda(n, a, k)))
                               for k in range(4)]
    assert trayectorias["G"] == [3, 4, 4, 4], trayectorias
    assert trayectorias["Gbar"] == [3, 4, 4, 4], trayectorias
    freeze = OUT.parent / "resultados" / "t4-arbol-trayectoria.json"
    freeze.parent.mkdir(exist_ok=True)
    freeze.write_text(json.dumps({
        "figura": "assets/t4-evolucion.svg",
        "grafo": "árbol binario balanceado (2,3), n=15",
        "rondas": [0, 1, 2, 3],
        "G": trayectorias["G"],
        "Gbar": trayectorias["Gbar"],
        "assert": "G y Ḡ coinciden por ronda (T4)",
    }, ensure_ascii=False, indent=2) + "\n")
    fig = plt.figure(figsize=(13.6, 6.2))
    gs = fig.add_gridspec(2, 5, width_ratios=[1, 1, 1, 1, 0.62])
    axes = [[fig.add_subplot(gs[fila, k]) for k in range(4)]
            for fila in range(2)]
    paneles = [fig.add_subplot(gs[fila, 4]) for fila in range(2)]
    for fila, (a, nombre, clave) in enumerate(
            ((adj, "G (árbol binario)", "G"),
             (adjc, "Ḡ (complemento)", "Gbar"))):
        Ga = nx.Graph()
        Ga.add_nodes_from(range(n))
        for u in range(n):
            for v in range(u + 1, n):
                if (a[u] >> v) & 1:
                    Ga.add_edge(u, v)
        for k in range(4):
            ax = axes[fila][k]
            cl = clases_wl_ronda(n, a, k)
            colores = [PALETA[c % len(PALETA)] for c in cl]
            nx.draw_networkx_edges(Ga, pos, ax=ax, edge_color="#dddddd",
                                   width=1.2)
            nx.draw_networkx_nodes(Ga, pos, ax=ax, node_color=colores,
                                   node_size=150, edgecolors="white",
                                   linewidths=1.0)
            ax.set_title(f"k = {k} · {len(set(cl))} clase(s)", fontsize=11)
            ax.axis("off")
            if k == 0:
                ax.text(-4.2, 1.5, nombre, rotation=90, va="center",
                        ha="center", fontsize=11.5, color="#0d0d0d")
        axp = paneles[fila]
        tabla = ("ronda   0  1  2  3\nclases  "
                 + "  ".join(str(x) for x in trayectorias[clave]))
        axp.text(0.5, 0.5, tabla, transform=axp.transAxes, ha="center",
                 va="center", family="monospace", fontsize=10.5,
                 linespacing=1.7,
                 bbox=dict(boxstyle="round,pad=0.55", facecolor="#f7f7f7",
                           edgecolor="#cccccc"))
        axp.set_title("trayectoria (motor)", fontsize=10.5)
        axp.axis("off")
    fig.suptitle("T4 ronda a ronda: la PARTICIÓN de clases coincide en G y "
                 "Ḡ en cada nivel (las etiquetas de color pueden diferir)",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(destino, format="svg", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig_t4(OUT / "t4-particion.svg")
    fig_t4_evolucion(OUT / "t4-evolucion.svg")
    print("t4-particion.svg y t4-evolucion.svg regenerados")
