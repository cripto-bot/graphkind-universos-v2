"""Corpus del harness: geng (no isomorfos), pares canónicos, random y archivo.

Un corpus es una lista de ``(n, E)`` con ``E`` = lista de aristas
``(u, v)`` 0-indexadas. El harness solo mide sobre corpus **no isomorfos**
(las colisiones entre copias isomorfas no significan nada): `geng` es la
fuente por defecto; `all` (etiquetados) queda solo para pruebas chicas.
"""

from __future__ import annotations

import random
import shutil
import subprocess
from pathlib import Path

from graphkind.graph6 import from_graph6, to_graph6  # noqa: F401 (reexport)
from graphkind.wl import edges_from_adj

GENG_CANDIDATES = ("geng", "nauty-geng", "/usr/bin/nauty-geng",
                   "/usr/bin/geng")


def geng_bin() -> str | None:
    for c in GENG_CANDIDATES:
        p = shutil.which(c) if not c.startswith("/") else (
            c if Path(c).exists() else None)
        if p:
            return p
    return None


def corpus_geng(n_max: int, n_min: int = 1) -> list[tuple[int, list]]:
    """Todos los grafos no isomorfos hasta n_max (requiere nauty-geng)."""
    exe = geng_bin()
    if not exe:
        raise RuntimeError(
            "no se encontró geng (nauty). Instalar nauty o usar otro corpus")
    out = []
    for n in range(n_min, n_max + 1):
        res = subprocess.run([exe, "-q", str(n)], capture_output=True,
                             text=True, timeout=600)
        for line in res.stdout.splitlines():
            if line.strip():
                n2, E = from_graph6(line)
                out.append((n2, E))
    return out


def corpus_all_labeled(n_max: int) -> list[tuple[int, list]]:
    """Todos los grafos ETIQUETADOS (2^C(n,2)); solo para pruebas chicas."""
    from graphkind import wl
    out = []
    for n in range(1, n_max + 1):
        for mask, adj in wl.all_graphs(n):
            out.append((n, edges_from_adj(adj)))
    return out


def n_de(E) -> int:
    """Cantidad de vértices de una lista de aristas (max + 1)."""
    return (max(max(u, v) for u, v in E) + 1) if E else 0


def corpus_pairs() -> list[tuple[int, list]]:
    """Pares canónicos como corpus (cada grafo por separado)."""
    pares = pares_canonicos()
    out = []
    for _, _, g1, g2 in pares:
        out.append((n_de(g1), g1))
        out.append((n_de(g2), g2))
    return out


def pares_canonicos():
    """(nombre, descripción, E1, E2) de los pares ancla."""
    c6 = [(i, (i + 1) % 6) for i in range(6)]
    dos_c3 = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
    petersen = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
                (0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
    prisma = ([(i, (i + 1) % 5) for i in range(5)]
              + [(i + 5, (i + 1) % 5 + 5) for i in range(5)]
              + [(i, i + 5) for i in range(5)])
    rook, shri = [], []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    u, v = a * 4 + b, c * 4 + d
                    if u < v and (a == c or b == d):
                        rook.append((u, v))
    for i in range(4):
        for j in range(4):
            u = i * 4 + j
            for di, dj in [(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)]:
                v = ((i + di) % 4) * 4 + ((j + dj) % 4)
                if u < v:
                    shri.append((u, v))
    return [
        ("C6 vs 2·C3", "1-WL no lo distingue", c6, dos_c3),
        ("Petersen vs prisma", "dos 3-regulares de 10 vértices", petersen, prisma),
        ("Rook vs Shrikhande", "SRG(16,6,2,2) cospectrales", rook, shri),
    ]


def corpus_random(n: int, m: int, p: float, seed: int = 7):
    """m grafos G(n,p) con semilla (no isomorfos casi seguro)."""
    rng = random.Random(seed)
    out = []
    for _ in range(m):
        E = [(u, v) for u in range(n) for v in range(u + 1, n)
             if rng.random() < p]
        out.append((n, E))
    return out


def corpus_file(path: str):
    """Archivo con una línea por grafo: graph6 o lista `n u v u v ...`."""
    out = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line[0].isalpha() and not line[0].isdigit():
            out.append(from_graph6(line))
        else:
            nums = [int(x) for x in line.split()]
            n, vals = nums[0], nums[1:]
            out.append((n, [(vals[i], vals[i + 1])
                            for i in range(0, len(vals), 2)]))
    return out


def load(corpus: str, n_max: int = 7, n_min: int = 1, seed: int = 7,
         path: str | None = None):
    """Despacha el corpus por nombre."""
    if corpus == "geng":
        return corpus_geng(n_max, n_min)
    if corpus == "all":
        return corpus_all_labeled(n_max)
    if corpus == "pairs":
        return corpus_pairs()
    if corpus == "random":
        return corpus_random(n_max, m=40, p=0.5, seed=seed)
    if corpus == "file":
        if not path:
            raise ValueError("corpus 'file' requiere --path")
        return corpus_file(path)
    raise ValueError(f"corpus desconocido: {corpus}")
