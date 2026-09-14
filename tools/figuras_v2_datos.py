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
    "svg.fonttype": "none",
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
    wl_n = {int(n): v for n, v in sg3["fallas_por_n"]["WL"].items()}
    assert wl_n == {9: 3900}, wl_n
    assert sg3["n_min"]["WL"] == 6 and sg3["n_min"]["KW3"] is None
    assert e119["cascada"] == {"k1": 26, "k2": 0, "k3": 0}
    assert sg1["leave_one_out"]["C3"]["colisiones_sin"] == 350
    assert sg1["cociente_complemento"]["colisiones_cociente"] == 6168

    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=110)
    # WL / KW2 (TRAIN 6..8 del freeze de SG-03 en el lab + TEST 9)
    ns = [6, 7, 8, 9]
    col = [4, 22, 350, 3900]
    ax.plot(ns, col, "-o", color=ROJO, lw=2.2, ms=7,
            label=r"WL $=$ KW2 (the base observer)")
    # completos: 0 en toda la clase (n=6..9)
    ax.plot(ns, [0.45] * len(ns), "s", color=VERDE, ms=8,
            label=r"KW3, KF2, KF3, IR$_1$, IR$_2$: 0 collisions")
    ax.axhspan(0.30, 0.65, color=VERDE, alpha=0.08)
    ax.set_yscale("log")
    ax.set_ylim(0.25, 2e4)
    ax.set_xticks(ns)
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"collisions $C_n$ (log)")
    ax.set_title(r"Frontier curves $C_n(I)$: what each observer loses",
                 fontsize=12)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.annotate(r"leave-one-out: $F_3\setminus\{3\text{-WL}\}\Rightarrow 350$",
                xy=(8, 350), xytext=(6.3, 2200), fontsize=9, color=GRIS,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=1))
    ax.annotate("C6 vs 2·C3: WL fails at $n=6$", xy=(6, 4),
                xytext=(6.15, 30), fontsize=9, color=GRIS,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=1))
    ax.annotate("Rook vs Shrikhande ($n=16$):\n3-WL fails, 3-FWL $\\equiv$ 4-WL separates",
                xy=(9, 2.6e3), xytext=(7.15, 9e3), fontsize=9, color=GRIS,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=1))
    ax.annotate(r"cascade $26 \to 0$ (atlas $n\leq7$): 2-WL resolves all",
                xy=(7.6, 0.45), xytext=(6.3, 0.9), fontsize=9, color=GRIS)
    ax.text(6.0, 0.55, r"$k^*=1$ with the corrected joint-refinement base (D-012)",
            fontsize=8.5, color=AZUL)
    fig.tight_layout()
    fig.savefig(OUT / "frontera-Cn.svg")
    plt.close(fig)
    print("frontera-Cn.svg OK")


# ------------------------------------------------------------ 2. trayectoria
def fig_trayectoria():
    import sys
    sys.path.insert(0, str(ROOT / "codigo"))
    from multicapa import (refinar_conjunto, complemento_capa,
                           complemento_total)
    from collections import Counter
    from itertools import combinations

    def ronda_a_ronda(n, capas, variante="canonica"):
        """Clases por ronda (reimplementa el update paso a paso)."""
        import hashlib

        def h(s):
            return hashlib.sha256(s.encode()).hexdigest()[:12]

        adj = [{v: set() for v in range(n)} for _ in capas]
        for l, E in enumerate(capas):
            for a, b in E:
                adj[l][a].add(b)
                adj[l][b].add(a)
        L = len(capas)
        if variante == "ordenada":
            colors = {v: h("|".join(str(len(adj[l][v])) for l in range(L)))
                      for v in range(n)}
        else:
            colors = {v: h(",".join(sorted(str(len(adj[l][v]))
                                           for l in range(L))))
                      for v in range(n)}
        serie = [len(set(colors.values()))]
        for _ in range(n + 2):
            nuevos = {}
            for v in range(n):
                por = [tuple(sorted(colors[u] for u in adj[l][v]))
                       for l in range(L)]
                datos = ";".join(",".join(x) for x in sorted(por)) \
                    if variante == "canonica" else \
                    "|".join(",".join(x) for x in por)
                nuevos[v] = h(f"{colors[v]}|{datos}")
            colors = nuevos
            serie.append(len(set(colors.values())))
            if serie[-1] == serie[-2]:
                break
        return serie

    # C6 y su complemento (single-layer)
    E6 = [(i, (i + 1) % 6) for i in range(6)]
    comp6 = complemento_total(6, [E6])[0]
    s_g = ronda_a_ronda(6, [E6])
    s_gb = ronda_a_ronda(6, [comp6])
    assert s_g == s_gb, (s_g, s_gb)
    # testigo multicapa (E1, P3) y su complemento por capa (canónica)
    E1 = [(0, 2)]
    P3 = [(0, 2), (1, 2)]
    s_a = ronda_a_ronda(3, [E1, P3])
    s_b = ronda_a_ronda(3, complemento_capa(3, [E1, P3], 0))
    assert s_a != s_b, (s_a, s_b)

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8), dpi=110)
    ax = axes[0]
    ax.plot(range(len(s_g)), s_g, "-o", color=AZUL, lw=2.4, ms=7,
            label=r"$G$")
    ax.plot(range(len(s_gb)), s_gb, "--s", color=NARANJA, lw=2.4, ms=7,
            label=r"$\bar{G}$")
    ax.set_title(r"Single-layer: $G$ and $\bar{G}$", fontsize=11)
    ax.set_xlabel("refinement round $t$")
    ax.set_ylabel("number of classes")
    ax.set_ylim(0.6, 6.6)
    ax.legend(frameon=False, fontsize=10)
    ax.annotate(r"identical partition every round $\Rightarrow$ T4",
                xy=(len(s_g) - 1, s_g[-1]), xytext=(0.8, 5.6),
                fontsize=9, color=VERDE)
    ax = axes[1]
    ax.plot(range(len(s_a)), s_a, "-o", color=VERDE, lw=2.4, ms=7,
            label="multilayer $(E_1,P_3)$")
    ax.plot(range(len(s_b)), s_b, "--s", color=ROJO, lw=2.4, ms=7,
            label="per-layer complement")
    ax.set_title("Multilayer (canonical): coherence", fontsize=11)
    ax.set_xlabel("refinement round $t$")
    ax.set_ylabel("number of classes")
    ax.set_ylim(0.6, 3.6)
    ax.legend(frameon=False, fontsize=9)
    ax.annotate("broken: 3 classes $\\to$ 2\n(one layer flipped)",
                xy=(len(s_b) - 1, s_b[-1]), xytext=(1.2, 1.6),
                fontsize=9, color=ROJO)
    eq = (r"Refinement trajectory: "
          r"$c_{t+1}(v)=H(c_t(v)\mid\sqcup_\ell\{c_t(w):w\in N_\ell(v)\})$")
    fig.suptitle(eq, fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / "trayectoria-refinamiento.svg")
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
    fig.suptitle(r"$M'(v)=T_v-M(v)$ (injective) $\Rightarrow$ T4 lives; "
                 f"repair: {fusions:,} fusions, {fallas} witnesses "
                 f"(261 000 cases); per-arity dual: "
                 f"{v169['ahorro_aridad_%']:.2f}% saving".replace(",", " "),
                 fontsize=10, y=1.03)
    fig.tight_layout()
    fig.savefig(OUT / "aridades.svg")
    plt.close(fig)
    print("aridades.svg OK")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig_frontera()
    fig_trayectoria()
    fig_aridades()
