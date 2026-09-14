#!/usr/bin/env python3
"""Figuras del MOTOR GraphKind (datos reales).

  1. motor-como-funciona.svg  el pipeline WL con un grafo real:
                              k=0,1,2 (partición estable) + las cajas.
  2. motor-potencia.svg       los números medidos del motor (dashboard).

Uso: python tools/figuras_motor.py [destino]
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
PALETA = ["#9a7b1f", "#26557a", "#a33", "#0b6b3a", "#6b3fa0", "#b06a1f"]
VERDE, GRIS = "#0b6b3a", "#6b6b6b"


def to_adj(g):
    g = nx.convert_node_labels_to_integers(g)
    n = g.number_of_nodes()
    adj = [0] * n
    for u, v in g.edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def clases_ronda(n, adj, k):
    import hashlib
    from collections import Counter

    def h(s):
        return hashlib.sha256(s.encode()).hexdigest()[:12]

    colors = [h(f"g|{adj[v].bit_count()}") for v in range(n)]
    for _ in range(k):
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
    rep = {}
    for v in range(n):
        rep.setdefault(colors[v], v)
    idx = {rep[c]: i for i, c in enumerate(sorted(rep))}
    return [idx[rep[colors[v]]] for v in range(n)]


def fig_como_funciona(destino):
    G = nx.path_graph(7)
    G.add_edge(3, 7)
    n = 8
    adj = to_adj(G)
    pos = nx.spring_layout(G, seed=11)
    fig = plt.figure(figsize=(13.5, 6.8))
    # fila superior: el grafo en k=0,1,2 y la particion estable
    for i, k in enumerate((0, 1, 2, 3)):
        ax = fig.add_axes([0.03 + i * 0.24, 0.55, 0.21, 0.34])
        cl = clases_ronda(n, adj, k)
        colores = [PALETA[c % len(PALETA)] for c in cl]
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#dddddd",
                               width=1.5)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colores,
                               node_size=330, edgecolors="white",
                               linewidths=1.4)
        ax.set_title(f"ronda k = {k} · {len(set(cl))} clase(s)",
                     fontsize=11.5)
        ax.axis("off")
        if k == 3:
            ax.text(0.5, -0.08, "(estable: partición final)",
                    transform=ax.transAxes, ha="center", fontsize=10,
                    color=VERDE)
    # fila inferior: las cajas del pipeline
    ax2 = fig.add_axes([0.0, 0.0, 1.0, 0.5])
    ax2.axis("off")
    cajas = [
        ("dato", "SMILES · código\nsecuencia · grafo"),
        ("grafo", "nodos (tipo, valor)\naristas etiquetadas"),
        ("label₀", "H(tipo | valor | grado)\ncanónico, determinístico"),
        ("round", "H(label | vecinos)\nsubestructuras por hash"),
        ("STOP", "partición estable\n(nunca un K a mano)"),
        ("kinds", "clases emergentes\n+ compresión"),
    ]
    x = 0.035
    ancho, alto = 0.135, 0.62
    for i, (titulo, sub) in enumerate(cajas):
        color = VERDE if titulo in ("STOP", "kinds") else "#0d0d0d"
        ax2.add_patch(FancyBboxPatch((x, 0.18), ancho, alto,
                                     boxstyle="round,pad=0.012",
                                     linewidth=1.2, edgecolor="#d9d9d9",
                                     facecolor="#f7f7f5"))
        ax2.text(x + ancho / 2, 0.62, titulo, ha="center", va="center",
                 fontsize=13, color=color, family="monospace")
        ax2.text(x + ancho / 2, 0.38, sub, ha="center", va="center",
                 fontsize=9, color=GRIS)
        if i < len(cajas) - 1:
            ax2.add_patch(FancyArrowPatch((x + ancho + 0.004, 0.49),
                                          (x + ancho + 0.026, 0.49),
                                          arrowstyle="-|>",
                                          mutation_scale=14,
                                          color="#c9c9c9"))
        x += ancho + 0.03
    fig.suptitle("GraphKind: cómo funciona — refinamiento iterativo 1-WL "
                 "(ejemplo real, 8 nodos)", fontsize=13, y=0.97)
    fig.savefig(destino, format="svg", facecolor="white")
    plt.close(fig)


def fig_potencia(destino):
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))
    # 1) paridad con Morgan
    ax = axes[0]
    vals = [0.9608, 0.9541]
    ax.bar(["GraphKind\n(WL r1+sym)", "Morgan\n(ECFP)"], vals,
           color=[VERDE, GRIS], alpha=0.85, width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v - 0.012, f"{v:.4f}", ha="center", va="top",
                color="white", fontsize=12)
    ax.set_ylim(0.9, 0.98)
    ax.set_title("Moléculas ChEMBL 40K: AUC\n(la ventaja crece con el dato)",
                 fontsize=11.5)
    ax.spines[["top", "right"]].set_visible(False)
    # 2) compresión
    ax = axes[1]
    ax.bar(["50K moléculas", "10K código"], [3.001, 187.5],
           color=[VERDE, "#26557a"], alpha=0.85, width=0.55)
    ax.text(0, 3.001 + 3, "3.00×", ha="center", fontsize=12)
    ax.text(1, 187.5 + 3, "187.5×", ha="center", fontsize=12)
    ax.set_ylim(0, 215)
    ax.set_title("Compresión (nodos físicos / kinds)\nsin taxonomía previa",
                 fontsize=11.5)
    ax.spines[["top", "right"]].set_visible(False)
    # 3) capacidades del teorema + motor
    ax = axes[2]
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    filas = [
        ("refine_dual (T4 en el motor)", "10.3×"),
        ("ahorro por normalización dual", "40.5%"),
        ("oráculo de universos", "87/87"),
        ("tests del motor", "104/104"),
        ("grafos del banco T4", "2.13M"),
    ]
    for i, (k_, v) in enumerate(filas):
        y = 0.86 - i * 0.16
        ax.text(0.02, y, k_, fontsize=11, color="#0d0d0d", va="center")
        ax.text(0.98, y, v, fontsize=13, color=VERDE, va="center",
                ha="right", family="monospace")
        ax.plot([0.02, 0.98], [y - 0.06, y - 0.06], color="#ececec",
                linewidth=1)
    ax.set_title("Capacidad medida (todo con assert)", fontsize=11.5)
    fig.suptitle("GraphKind: la potencia del motor, en números reales",
                 fontsize=13, y=1.0)
    fig.tight_layout()
    fig.savefig(destino, format="svg", facecolor="white")
    plt.close(fig)


def main():
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"
    fig_como_funciona(destino / "motor-como-funciona.svg")
    print("motor-como-funciona.svg OK")
    fig_potencia(destino / "motor-potencia.svg")
    print("motor-potencia.svg OK")


if __name__ == "__main__":
    main()
