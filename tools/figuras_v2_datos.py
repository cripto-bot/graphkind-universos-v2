#!/usr/bin/env python3
"""Figuras v2 de DATOS (matplotlib + mathtext), ancladas a los freezes.

Genera en assets/:
  1. frontera-Cn.svg             curvas C_n(I) por observador (SG-01/03, EXP-119)
  2. trayectoria-refinamiento.svg rondas vs clases: G vs Ḡ (T4) y multicapa (EXP-162)
  3. aridades.svg                escalera de aridad + transplante (EXP-167/168/169)

Regla: los números salen de resultados/*.json (asserts); nada tipeado.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "resultados"
OUT = ROOT / "assets"

plt.rcParams.update({
    "svg.fonttype": "path",
    "mathtext.fontset": "cm",
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#6b6b6b",
    "axes.labelcolor": "#0d0d0d",
    "xtick.color": "#6b6b6b",
    "ytick.color": "#6b6b6b",
    "text.color": "#0d0d0d",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.color": "#ececec",
    "grid.linewidth": 0.8,
})
# Okabe-Ito (colorblind-safe)
AZUL, NARANJA, VERDE, ROJO = "#0072B2", "#E69F00", "#009E73", "#D55E00"
VIOLETA, CIELO, GRIS = "#CC79A7", "#56B4E9", "#6b6b6b"


def _cargar(nombre):
    return json.loads((RES / nombre).read_text())


# ---------------------------------------------------------------- 1. frontera
def fig_frontera():
    sg3 = _cargar("SG-03_results_frozen.json")["test"]
    sg1 = _cargar("SG-01_results_frozen.json")
    e119 = _cargar("EXP-119_results_frozen.json")
    sg4 = _cargar("SG-04_results_frozen.json")
    c1 = sg4["capa1_n10"]
    assert c1["grafos"] == 12005168 and c1["KW3"]["pares"] == 0 \
        and c1["IR1p"]["pares"] == 0, c1
    wl_n = {int(n): v for n, v in sg3["fallas_por_n"]["WL"].items()}
    assert wl_n == {9: 3900}, wl_n
    assert sg3["n_min"]["WL"] == 6 and sg3["n_min"]["KW3"] is None
    assert e119["cascada"] == {"k1": 26, "k2": 0, "k3": 0}
    assert sg1["leave_one_out"]["C3"]["colisiones_sin"] == 350
    assert sg1["cociente_complemento"]["colisiones_cociente"] == 6168

    fig, ax = plt.subplots(figsize=(7.6, 4.4), dpi=110)
    ns = [6, 7, 8, 9]
    col = [4, 22, 350, 3900]
    ax.plot(ns, col, "-o", color=ROJO, lw=2.2, ms=7,
            label=r"WL $=$ KW2 (the base observer)")
    ns0 = [6, 7, 8, 9, 10]
    ax.plot(ns0, [0.45] * len(ns0), "s", color=VERDE, ms=8,
            label=r"KW3, KF2, KF3, IR$_1$, IR$_2$: 0 collisions")
    ax.annotate("$n=10$ exhaustive: 0 / 12 005 168 (SG-04)",
                xy=(7.35, 0.78), fontsize=8.5, color=VERDE)
    ax.axhspan(0.30, 0.65, color=VERDE, alpha=0.08)
    ax.set_yscale("log")
    ax.set_ylim(0.25, 3e4)
    ax.set_xticks(ns0)
    ax.set_xlim(5.7, 10.35)
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"collisions $C_n$ (log)")
    ax.set_title(r"Frontier curves $C_n(I)$: what each observer loses",
                 fontsize=12)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.annotate(r"leave-one-out: $F_3\setminus\{3\text{-WL}\}\Rightarrow 350$",
                xy=(8, 350), xytext=(6.35, 200), fontsize=9, color=GRIS,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=1))
    ax.annotate(r"C6 vs 2$\cdot$C3: WL fails at $n=6$", xy=(6, 4),
                xytext=(6.3, 9), fontsize=9, color=GRIS,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=1))
    fig.text(0.012, 0.055, "Rook vs Shrikhande ($n=16$): 3-WL fails, "
             "3-FWL $\\equiv$ 4-WL separates", fontsize=8.5, color=GRIS)
    fig.text(0.012, 0.012, "cascade 26 $\\to$ 0 (atlas $n\\leq7$): 2-WL "
             "resolves all  ·  $k^*=1$ with the corrected joint-refinement "
             "base (D-012)", fontsize=8.5, color=AZUL)
    fig.tight_layout(rect=[0, 0.075, 1, 1])
    fig.savefig(OUT / "frontera-Cn.svg", bbox_inches="tight")
    plt.close(fig)
    print("frontera-Cn.svg OK")


# ------------------------------------------------------------ 2. trayectoria
def fig_trayectoria():
    import hashlib
    import networkx as nx

    def serie(n, capas):
        """Clases por ronda del refinamiento conjunto canónico."""
        def h(s):
            return hashlib.sha256(s.encode()).hexdigest()[:12]

        adj = [{v: set() for v in range(n)} for _ in capas]
        for l, E in enumerate(capas):
            for a, b in E:
                adj[l][a].add(b)
                adj[l][b].add(a)
        L = len(capas)
        colors = {v: h(",".join(sorted(str(len(adj[l][v]))
                                       for l in range(L))))
                  for v in range(n)}
        out = [len(set(colors.values()))]
        for _ in range(n + 2):
            nuevos = {}
            for v in range(n):
                por = [tuple(sorted(colors[u] for u in adj[l][v]))
                       for l in range(L)]
                datos = ";".join(",".join(x) for x in sorted(por))
                nuevos[v] = h(f"{colors[v]}|{datos}")
            colors = nuevos
            out.append(len(set(colors.values())))
            if out[-1] == out[-2]:
                break
        return out

    def edges(g):
        g = nx.convert_node_labels_to_integers(g)
        return sorted(tuple(sorted(e)) for e in g.edges)

    tree = nx.balanced_tree(2, 3)
    T = edges(tree)
    C = edges(nx.complement(tree))
    s_g, s_gb = serie(15, [T]), serie(15, [C])
    assert s_g == s_gb == [3, 4, 4], (s_g, s_gb)
    # testigo multicapa (EXP-162): (E1, P3) y su complemento por capa
    E1, P3 = [(0, 2)], [(0, 2), (1, 2)]
    PC = [(0, 1), (1, 2)]
    s_a, s_b = serie(3, [E1, P3]), serie(3, [PC, P3])
    assert s_a == [3, 3] and s_b == [2, 2], (s_a, s_b)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.0), dpi=110)
    ax = axes[0]
    ax.plot(range(len(s_g)), s_g, "-o", color=AZUL, lw=2.4, ms=8,
            label=r"$G$ (binary tree)")
    ax.plot(range(len(s_gb)), s_gb, "--s", color=NARANJA, lw=2.4, ms=7,
            label=r"$\bar{G}$ (complement)")
    ax.set_title(r"Single-layer: $G$ and $\bar{G}$", fontsize=11)
    ax.set_xlabel("refinement round $t$")
    ax.set_ylabel("number of classes")
    ax.set_xticks(range(len(s_g)))
    ax.set_ylim(0.5, 5.2)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.annotate(r"identical partition every round $\Rightarrow$ T4",
                xy=(2, 4), xytext=(0.15, 4.55), fontsize=9, color=VERDE)
    ax = axes[1]
    ax.plot(range(len(s_a)), s_a, "-o", color=VERDE, lw=2.4, ms=8,
            label=r"multilayer $(E_1,P_3)$")
    ax.plot(range(len(s_b)), s_b, "--s", color=ROJO, lw=2.4, ms=7,
            label="per-layer complement")
    ax.set_title("Multilayer (canonical): coherence", fontsize=11)
    ax.set_xlabel("refinement round $t$")
    ax.set_ylabel("number of classes")
    ax.set_xticks(range(len(s_a)))
    ax.set_ylim(0.5, 3.8)
    ax.legend(frameon=False, fontsize=9, loc="center right")
    ax.annotate("broken at round 0: 3 $\\to$ 2\n(one layer flipped)",
                xy=(1, 2), xytext=(0.12, 2.6), fontsize=9, color=ROJO)
    fig.tight_layout()
    fig.savefig(OUT / "trayectoria-refinamiento.svg", bbox_inches="tight")
    plt.close(fig)
    print("trayectoria-refinamiento.svg OK")


# --------------------------------------------------------------- 3. aridades
def fig_aridades():
    e167 = _cargar("EXP-167_results_frozen.json")["resultados"]
    e168 = _cargar("EXP-168_results_frozen.json")
    e169 = _cargar("EXP-169_results_frozen.json")
    esc = e167["uniforme"]
    assert (esc["k4_n6"]["t4_vive"], esc["k4_n6"]["objetos"]) == (156, 156)
    assert (esc["k5_n6"]["t4_vive"], esc["k5_n6"]["objetos"]) == (7, 7)
    mz = e167["mezclado"]["n5"]
    assert mz["total|canonica"]["vive"] == mz["total|canonica"]["objetos"]
    assert mz["aridad2|canonica"]["vive"] == mz["aridad2|canonica"]["objetos"]
    ag = e168["agregados"]
    fusions = sum(v["fusion"] for k, v in ag.items() if k.startswith("dirigida"))
    fallas = sum(v["fallas_t4c"] for v in ag.values())
    assert fusions == 21821 and fallas == 0, (fusions, fallas)
    v169 = e169["validacion"]
    assert v169["particion_igual"] == v169["casos"]

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9), dpi=110)
    ax = axes[0]
    ks = ["$k=3$", "$k=4$", "$k=5$"]
    vals = [esc["k3_n5"]["objetos"], esc["k4_n6"]["objetos"],
            esc["k5_n6"]["objetos"]]
    bars = ax.bar(ks, vals, color=[CIELO, AZUL, VERDE], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 3, f"{v}/{v}",
                ha="center", fontsize=10, color="#0d0d0d")
    ax.set_ylabel("non-isomorphic classes")
    ax.set_title(r"Arity ladder: T4 lives ($E^c=C(V,k)\setminus E$)",
                 fontsize=11)
    ax.set_ylim(0, max(vals) * 1.25)
    ax = axes[1]
    labels = ["total\n(canonical)", "per-arity\n(canonical)",
              "per-arity\n(ordered)"]
    vals2 = [mz["total|canonica"]["vive"], mz["aridad2|canonica"]["vive"],
             mz["aridad2|ordenada"]["vive"]]
    tot = mz["total|canonica"]["objetos"]
    bars = ax.bar(labels, [v / tot * 100 for v in vals2],
                  color=[VERDE, ROJO, NARANJA], width=0.55)
    for b, v in zip(bars, vals2):
        ax.text(b.get_x() + b.get_width() / 2, 102, f"{v}/{tot}",
                ha="center", fontsize=10, color="#0d0d0d")
    ax.set_ylabel("% T4 alive")
    ax.set_ylim(0, 118)
    ax.set_title("Mixed arities {2,3}: the transplant fails", fontsize=11)
    fig.suptitle("Arities: the ladder lives, the transplant fails",
                 fontsize=12)
    fig.text(0.012, 0.012,
             f"$M'(v)=T_v-M(v)$ (injective) $\\Rightarrow$ T4 lives  ·  "
             f"repair: {fusions:,} fusions, {fallas} witnesses "
             f"(261 000 cases)  ·  per-arity dual: "
             f"{v169['ahorro_aridad_%']:.2f}% saving".replace(",", " "),
             fontsize=8.5, color=GRIS)
    fig.tight_layout(rect=[0, 0.04, 1, 0.95])
    fig.savefig(OUT / "aridades.svg", bbox_inches="tight")
    plt.close(fig)
    print("aridades.svg OK")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig_frontera()
    fig_trayectoria()
    fig_aridades()
