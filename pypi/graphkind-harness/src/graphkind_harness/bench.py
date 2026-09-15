"""Mediciones del harness: colisiones/frontera, anclas, T4 por universo y controles.

Todo es determinista y sale de un JSON congelable (``run``). La métrica de
colisiones solo tiene sentido sobre corpus **no isomorfos** (geng): cuenta
pares de grafos no isomorfos con la misma firma.
"""

from __future__ import annotations

import random
import time
from collections import Counter, defaultdict

from graphkind import hipergrafo, multicapa, universos, wl

from . import corpus as _corpus
from .observers import OBSERVADORES, observadores as _obs


def colisiones(grafos, obs):
    """Colisiones de un observador sobre un corpus no isomorfo.

    Devuelve total, por n, y hasta 3 testigos (índices dentro del corpus).
    """
    grupos = defaultdict(list)
    for i, (n, E) in enumerate(grafos):
        grupos[(n, obs(n, E))].append(i)
    total, por_n = 0, defaultdict(int)
    # pares evaluados: TODOS los pares del corpus a igual n
    tam = Counter(n for n, _ in grafos)
    pares_n = {n: k * (k - 1) // 2 for n, k in tam.items()}
    testigos = []
    for (n, _), idxs in grupos.items():
        k = len(idxs)
        if k > 1:
            pares = k * (k - 1) // 2
            total += pares
            por_n[n] += pares
            if len(testigos) < 3:
                testigos.append({"n": n, "i": idxs[0], "j": idxs[1]})
    return {"total": total, "por_n": dict(sorted(por_n.items())),
            "pares_por_n": dict(sorted(pares_n.items())),
            "pares_total": sum(pares_n.values()),
            "testigos": testigos, "grupos": len(grupos)}


def frontera(grafos, obs_dict):
    """Colisiones por observador y por n (las curvas C_n)."""
    out = {}
    for nombre, obs in obs_dict.items():
        r = colisiones(grafos, obs)
        out[nombre] = {"total": r["total"], "por_n": r["por_n"],
                       "pares_por_n": r["pares_por_n"],
                       "pares_total": r["pares_total"],
                       "testigos": r["testigos"]}
    return out


def anclas(obs_dict):
    """Tabla de separación de los pares canónicos por observador."""
    out = []
    for nombre, desc, E1, E2 in _corpus.pares_canonicos():
        n = _corpus.n_de(E1)
        fila = {"par": nombre, "desc": desc, "n": n}
        for on, obs in obs_dict.items():
            fila[on] = "separa" if obs(n, E1) != obs(n, E2) else "colisiona"
        out.append(fila)
    return out


def t4_estandar(grafos, k=None):
    """T4 sobre el universo estándar (1-WL, o k-FWL si k>=2): tasa de éxito.

    T4 (1-WL): la partición de G y Ḡ coincide. T4_k (k-FWL): la partición
    de k-tuplas coincide. Devuelve {"casos", "viven", "tasa"}.
    """
    viven = 0
    for n, E in grafos:
        adj = wl.adj_from_edges(n, E)
        adjc = wl.comp_adj(n, adj)
        if k is None:
            ok = wl.t4(adj)
        else:
            from ._fast import particion_kfwl
            ok = particion_kfwl(n, adj, k) == particion_kfwl(n, adjc, k)
        viven += 1 if ok else 0
    return {"casos": len(grafos), "viven": viven,
            "tasa": viven / len(grafos) if grafos else None}


def t4_multicapa(grafos, dualidad="total", variante="canonica"):
    """T4 en objetos multicapa (capas = [E, complemento(E)]).

    dualidad: "total" (uniforme) o "capa0" (por capa). Devuelve la tasa.
    """
    viven = 0
    for n, E in grafos:
        es = {tuple(sorted(e)) for e in E}
        comp = [(u, v) for u in range(n) for v in range(u + 1, n)
                if (u, v) not in es]
        capas = [E, comp]
        if dualidad == "total":
            capas2 = multicapa.complemento_total(n, capas)
        elif dualidad == "capa0":
            capas2 = multicapa.complemento_capa(n, capas, 0)
        else:
            raise ValueError("dualidad ∈ {total, capa0}")
        r = multicapa.t4(n, capas, capas2, variante)
        viven += 1 if r["particion_igual"] else 0
    return {"casos": len(grafos), "viven": viven,
            "tasa": viven / len(grafos) if grafos else None}


def t4_hipergrafo(n, m, k=3, seed=7):
    """T4_k en hipergrafos k-uniformes aleatorios (semilla fija)."""
    rng = random.Random(seed)
    viven = 0
    from itertools import combinations
    todos = list(combinations(range(n), k))
    for _ in range(m):
        aristas = [e for e in todos if rng.random() < 0.4]
        viven += 1 if hipergrafo.t4_k_uniforme(n, k, aristas) else 0
    return {"casos": m, "viven": viven, "tasa": viven / m if m else None,
            "n": n, "k": k, "seed": seed}


def control_relabeling(grafos, obs_dict, seed=7):
    """Control: la firma no debe cambiar al relabelar los vértices."""
    rng = random.Random(seed)
    fallas = []
    for nombre, obs in obs_dict.items():
        ok = True
        for n, E in grafos:
            pi = list(range(n))
            rng.shuffle(pi)
            E2 = [(pi[u], pi[v]) for u, v in E]
            if obs(n, E) != obs(n, E2):
                ok = False
                break
        fallas.append({"observador": nombre, "invarianza": ok})
    return fallas


def run(corpus="geng", n_max=7, n_min=1, observadores=None, seed=7,
        path=None, hipergrafo_n=5, hipergrafo_m=40):
    """Corrida completa: corpus -> frontera + anclas + T4 + controles."""
    import graphkind
    from . import __version__
    t0 = time.time()
    grafos = _corpus.load(corpus, n_max=n_max, n_min=n_min, seed=seed,
                          path=path)
    obs = _obs(observadores)
    res = {
        "programa": "graphkind-harness",
        "version": __version__,
        "motor": graphkind.__version__,
        "motor_doi": graphkind.DOI,
        "corpus": {"nombre": corpus, "n_min": n_min, "n_max": n_max,
                   "grafos": len(grafos), "seed": seed,
                   "geng": _corpus.geng_bin() or "no disponible"},
        "observadores": list(obs),
        "frontera": frontera(grafos, obs),
        "anclas": anclas(obs),
        "t4": {
            "estandar_wl": t4_estandar(grafos),
            "estandar_kw2": t4_estandar(grafos, k=2),
            "multicapa_total": t4_multicapa(grafos, "total"),
            "multicapa_capa0": t4_multicapa(grafos, "capa0"),
            "hipergrafo_k3": t4_hipergrafo(hipergrafo_n, hipergrafo_m, 3, seed),
        },
        "controles": {"relabeling": control_relabeling(grafos, obs, seed)},
        "wall_s": round(time.time() - t0, 3),
    }
    return res


def reporte(res):
    """Reporte de texto legible de una corrida."""
    L = []
    L.append(f"GraphKind harness {res['version']} (motor {res['motor']})")
    c = res["corpus"]
    L.append(f"corpus: {c['nombre']} n∈[{c['n_min']},{c['n_max']}] "
             f"grafos={c['grafos']} geng={c['geng']}")
    L.append("")
    L.append("Colisiones (0 = completo en la clase):")
    ns = sorted({n for o in res["frontera"].values() for n in o["por_n"]}
                | set())
    cab = "observador".ljust(10) + "".join(f"n={n}".rjust(9) for n in ns)
    L.append("  " + cab + "   total")
    for nombre, o in res["frontera"].items():
        fila = nombre.ljust(10) + "".join(
            str(o["por_n"].get(n, 0)).rjust(9) for n in ns)
        L.append("  " + fila + f"   {o['total']}")
    L.append("")
    L.append("Anclas:")
    for fila in res["anclas"]:
        vals = " ".join(f"{k}={v}" for k, v in fila.items()
                        if k not in ("par", "desc", "n"))
        L.append(f"  {fila['par']:22s} n={fila['n']:2d}  {vals}")
    L.append("")
    t = res["t4"]
    L.append("T4 por universo (tasa de supervivencia):")
    for k, v in t.items():
        L.append(f"  {k:18s} {v['viven']}/{v['casos']} "
                 f"({v['tasa']:.3f})" if v["tasa"] is not None else k)
    L.append("")
    L.append("Controles:")
    for f in res["controles"]["relabeling"]:
        L.append(f"  relabeling {f['observador']:10s} "
                 f"{'OK' if f['invarianza'] else 'FALLA'}")
    L.append("")
    L.append(f"wall: {res['wall_s']} s")
    return "\n".join(L)
