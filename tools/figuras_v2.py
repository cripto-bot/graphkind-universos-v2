#!/usr/bin/env python3
"""Figuras v2 — arco de universos + Santo Grial (SVG, fieles a la teoría).

Genera assets/*.svg desde los números de los freezes. Estilo del repo:
Georgia (títulos), sans (texto), mono (ecuaciones); paleta del proyecto.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
BG = "#ffffff"; BORDE = "#e6e6e6"; TXT = "#0d0d0d"; MUT = "#6b6b6b"
VERDE = "#0b6b3a"; ROJO = "#a33"; AZUL = "#26557a"; ORO = "#9a7b1f"

def _head(w, h, titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">\n'
            f'  <rect width="{w}" height="{h}" rx="16" fill="{BG}"/>\n'
            f'  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="15.5" '
            f'fill="none" stroke="{BORDE}"/>\n'
            f'  <text x="36" y="46" font-family="Georgia,serif" font-size="22" '
            f'fill="{TXT}">{titulo}</text>\n')

def _mono(x, y, s, fill=VERDE, size=15, anchor="start"):
    return (f'  <text x="{x}" y="{y}" font-family="ui-monospace,monospace" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}">{s}</text>\n')

def _sans(x, y, s, fill=MUT, size=13, anchor="start"):
    return (f'  <text x="{x}" y="{y}" font-family="-apple-system,sans-serif" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}">{s}</text>\n')

def _fin(w, h):
    return "</svg>\n"

# 1. La ley multicapa
def fig_multicapa():
    s = _head(760, 460, "Multilayer T4 — the coherence law")
    s += _mono(36, 84, "c<tspan baseline-shift=\"sub\">t+1</tspan>(v) = H( c_t(v) | ⨆<tspan baseline-shift=\"sub\">ℓ</tspan> { c_t(w) : w ∈ N_ℓ(v) } )", TXT, 16)
    s += _sans(36, 108, "joint refinement — canonical: multiset over channels · ordered: tuple")
    # paneles
    x0, y0, w, h = 36, 140, 224, 150
    paneles = [
        ("TOTAL complement", f"E_ℓ → E_ℓ^c  ∀ℓ", "T4 lives", "1298/1298  (L=2)", "1404/1404  (L=3)", VERDE),
        ("PER-LAYER complement", "E_ℓ → E_ℓ^c  (one ℓ)", "T4 dies (canonical)", "90/1298  = 6.9%", "104/1404 = 7.4%", ROJO),
        ("CHANNEL permutation", "π ∈ S_L", "T4 lives", "partition blind", "to channel order", VERDE),
    ]
    for i, (tit, eq, ver, n1, n2, col) in enumerate(paneles):
        x = x0 + i * (w + 18)
        s += (f'  <rect x="{x}" y="{y0}" width="{w}" height="{h}" rx="12" '
              f'fill="none" stroke="{BORDE}"/>\n')
        s += _sans(x + 14, y0 + 26, tit, TXT, 14)
        s += _mono(x + 14, y0 + 50, eq, MUT, 12)
        s += _sans(x + 14, y0 + 82, ver, col, 16)
        s += _mono(x + 14, y0 + 108, n1, col, 13)
        s += _mono(x + 14, y0 + 128, n2, col, 13)
    # ley
    s += _mono(36, 342, "T4(ι) lives  ⟺  ι acts uniformly on the channels", VERDE, 17)
    s += _sans(36, 372, "canonical preserving group: exactly U = {∅, all} × S_L  →  4/4 (L=2), 12/12 (L=3), group closure ✓", MUT, 13)
    s += _sans(36, 396, "ordered variant: the whole group preserves (tuple equality is coordinate-wise) — the group is relative to the observation", MUT, 13)
    s += _mono(36, 428, "(⇐) proved: the same bijection M_ℓ ↦ T_ℓ − M_ℓ per layer · (⇒) open", MUT, 13)
    return s + _fin(760, 460)

# 2. Escalera k*
def fig_escalera():
    s = _head(760, 380, "The k*(L) ladder is flat")
    s += _mono(36, 84, "k*(L) = min{ k : #classes(F_k) = #classes(iso) }", TXT, 15)
    # ejes
    s += f'  <line x1="90" y1="290" x2="700" y2="290" stroke="{BORDE}"/>\n'
    s += f'  <line x1="90" y1="110" x2="90" y2="290" stroke="{BORDE}"/>\n'
    for i, L in enumerate((1, 2, 3, 4, 5)):
        x = 130 + i * 135
        s += _sans(x, 312, f"L = {L}", MUT, 14, "middle")
        s += f'  <circle cx="{x}" cy="270" r="8" fill="{VERDE}"/>\n'
        s += _mono(x, 250, "1", VERDE, 14, "middle")
    s += f'  <line x1="90" y1="230" x2="700" y2="230" stroke="{ROJO}" stroke-dasharray="6 6"/>\n'
    s += _mono(100, 224, "k* = 2", ROJO, 13)
    s += _sans(100, 132, "corpora: representatives n≤4 (123 / 1 349 / 14 751 / 161 621 classes)", MUT, 12)
    s += _sans(100, 150, "full labelings n≤3 (20 / 120 / 816 / 5 984) — both flat", MUT, 12)
    s += _mono(36, 352, "correction (EXP-164): EXP-162's k*=2 was the degenerate k=1 (initial colors, no refinement)", ROJO, 12)
    return s + _fin(760, 380)

# 3. Matriz universo x observador
def fig_matriz():
    s = _head(860, 420, "Universe × observer — where the frontier lives")
    filas = [("standard", "3900", "3900", "0", "0", "0", "0", "0"),
             ("typed (n≤6)", "12", "12", "0", "—", "—", "0", "—"),
             ("multilayer", "k*=1", "—", "—", "—", "—", "—", "—"),
             ("directed", "T4 ✓", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"),
             ("Z₃", "T4 ✗", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"),
             ("R1", "T4 ✗", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")]
    cols = ("WL", "KW2", "KW3", "KF2", "KF3", "IR1p", "IR2p")
    x0, y0, cw, ch = 190, 110, 88, 38
    for j, c in enumerate(cols):
        s += _mono(x0 + j * cw + cw // 2, y0 - 12, c, MUT, 12, "middle")
    for i, fila in enumerate(filas):
        y = y0 + i * ch
        s += _sans(36, y + 24, fila[0], TXT, 13)
        for j, v in enumerate(fila[1:]):
            col = ROJO if v in ("3900", "12") else (VERDE if v == "0" or v == "T4 ✓" else MUT)
            if v == "N/A":
                col = "#b9b9b9"
            s += f'  <rect x="{x0 + j*cw}" y="{y}" width="{cw-6}" height="{ch-8}" rx="6" fill="none" stroke="{BORDE}"/>\n'
            s += _mono(x0 + j * cw + (cw - 6) // 2, y + 24, v, col, 12, "middle")
    s += _sans(36, 372, "frontier (collisions / n_min): moves with the OBSERVER (WL/KW2 n_min=6; KW3/IR1p ≥7)", VERDE, 13)
    s += _sans(36, 394, "does NOT move with typing (typed row = standard row in n_min) · N/A = machinery not in the engine (declared)", MUT, 13)
    return s + _fin(860, 420)

# 4. Hipergrafos + aridades
def fig_hipergrafos():
    s = _head(820, 470, "Hypergraphs: the map predicts, and the arity transplant fails")
    s += _mono(36, 84, "E ⊆ C(V,k)   ·   E^c = C(V,k) ∖ E   ·   M'(v) = T_v − M(v)  (injective) ⟹ T4 lives", TXT, 14)
    s += _sans(36, 108, "prediction registered before measuring (3-uniform hypergraphs)")
    # prediccion
    s += f'  <rect x="36" y="130" width="360" height="120" rx="12" fill="none" stroke="{BORDE}"/>\n'
    s += _sans(52, 158, "PREDICTED", MUT, 13)
    s += _mono(52, 186, "T4 lives", VERDE, 20)
    s += _sans(52, 214, "MEASURED", MUT, 13)
    s += _mono(52, 240, "1831/1831  (n≤5 + sample n=6)", VERDE, 14)
    # escalera aridad
    s += f'  <rect x="420" y="130" width="364" height="120" rx="12" fill="none" stroke="{BORDE}"/>\n'
    s += _sans(436, 158, "ARITY LADDER — T4 lives", TXT, 13)
    for i, (k, v) in enumerate((("k=3", "34/34"), ("k=4", "156/156"), ("k=5", "7/7"))):
        x = 452 + i * 110
        s += _mono(x, 190, k, MUT, 13)
        s += _mono(x, 214, v, VERDE, 13)
        s += f'  <rect x="{x}" y="226" width="86" height="8" rx="4" fill="{VERDE}"/>\n'
    # transplante
    s += _sans(36, 292, "MIXED ARITIES {2,3}: the channel-law transplant FAILS", ROJO, 14)
    s += _mono(36, 320, "total complement: T4 lives 100%", VERDE, 14)
    s += _mono(36, 346, "per-arity complement: ALSO lives 1038/1038 (both variants)", ROJO, 14)
    s += _sans(36, 378, "mechanism: per-arity messages have different types (single colors vs pairs) —", MUT, 13)
    s += _sans(36, 398, "the refinement repairs the round-0 degree-multiset fusion (261 000 cases, 0 witnesses)", MUT, 13)
    s += _mono(36, 436, "the law is of CHANNELS, not of every decomposition", TXT, 14)
    return s + _fin(820, 470)

# 5. Dual por aridad
def fig_dual():
    s = _head(760, 380, "Per-arity dual: the law becomes capability")
    s += _mono(36, 84, "choose per arity:  E_a  or  E_a^c  (the smaller)   ⟹   partition preserved", TXT, 14)
    base = 140; esc = 460 / 1749801
    barras = [("original", 1749801, ROJO, "100%"),
              ("total dual", 1570281, ORO, "saving 10.26%"),
              ("per-arity dual", 1498382, VERDE, "saving 14.37%")]
    for i, (nom, v, col, lab) in enumerate(barras):
        y = base + i * 64
        w = v * esc
        s += f'  <rect x="200" y="{y}" width="{w:.0f}" height="26" rx="6" fill="{col}" opacity="0.85"/>\n'
        s += _sans(36, y + 19, nom, TXT, 14)
        s += _mono(210 + w, y + 19, f"{v:,}".replace(",", " "), col, 13)
        s += _sans(36, y + 42, lab, MUT, 12)
    s += _mono(36, 348, "validation: 60 000 cases · partition 100% · extra saving vs total: +4.11%", VERDE, 13)
    return s + _fin(760, 380)

# 6. Santo Grial
def fig_santo_grial():
    s = _head(820, 430, "The Holy Grail: completeness, its price, and i*")
    s += _mono(36, 84, "F3 = {1-WL, 2-WL, 3-WL}   ·   C_n(I) = collisions / pairs", TXT, 14)
    s += f'  <rect x="36" y="110" width="240" height="150" rx="12" fill="none" stroke="{BORDE}"/>\n'
    s += _sans(52, 138, "COMPLETENESS (n≤8)", MUT, 13)
    s += _mono(52, 168, "C_8 = 0", VERDE, 22)
    s += _mono(52, 194, "76 205 685 pairs", TXT, 13)
    s += _sans(52, 222, "leave-one-out: 3-WL", MUT, 12)
    s += _sans(52, 240, "does the work (350 without it)", MUT, 12)
    s += f'  <rect x="290" y="110" width="240" height="150" rx="12" fill="none" stroke="{BORDE}"/>\n'
    s += _sans(306, 138, "T4's PRICE", MUT, 13)
    s += _mono(306, 168, "6 168 pairs", ROJO, 22)
    s += _sans(306, 194, "the quotient G ~ Ḡ merges them", MUT, 12)
    s += _sans(306, 216, "10 self-complementary (n≤8)", MUT, 12)
    s += _sans(306, 238, "v2 n≤5 analogue: 24 pairs", MUT, 12)
    s += f'  <rect x="544" y="110" width="240" height="150" rx="12" fill="none" stroke="{BORDE}"/>\n'
    s += _sans(560, 138, "INDIVIDUALIZATION", MUT, 13)
    s += _mono(560, 168, "i* = 1", VERDE, 22)
    s += _sans(560, 194, "13 597 graphs (n≤8)", MUT, 12)
    s += _mono(560, 222, "i* = 2  at Rook/Shri", TXT, 13)
    s += _sans(560, 244, "IR_1 ✗   IR_2 ✓", MUT, 12)
    s += _sans(36, 300, "the complete invariant is NOT complement-invariant — that is exactly the information T4 describes", TXT, 14)
    s += _mono(36, 336, "i*(G) = min{ k : the pointed signature of G is unique in its class }", MUT, 13)
    s += _sans(36, 368, "lattice (n≤9): all complete invariants collapse (vacuous equivalence); WL = 2-WL;", MUT, 13)
    s += _sans(36, 388, "anchors: IR_1 fails where 3-WL fails, IR_2 separates where 3-FWL/4-WL separates (C not observed)", MUT, 13)
    return s + _fin(820, 430)

def main():
    OUT.mkdir(exist_ok=True)
    figs = {"multicapa-ley.svg": fig_multicapa(),
            "escalera-kstar.svg": fig_escalera(),
            "matriz-universo-observador.svg": fig_matriz(),
            "hipergrafos-aridades.svg": fig_hipergrafos(),
            "dual-aridad.svg": fig_dual(),
            "santo-grial.svg": fig_santo_grial()}
    import xml.dom.minidom as md
    for nombre, contenido in figs.items():
        md.parseString(contenido)
        (OUT / nombre).write_text(contenido)
        print(f"{nombre}: {len(contenido)} bytes OK")

if __name__ == "__main__":
    main()
