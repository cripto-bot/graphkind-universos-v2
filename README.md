<p align="center">
  <img src="assets/banner.svg" width="100%" alt="GraphKind — Universes of color refinement">
</p>

<p align="center">
  <a href="https://github.com/cripto-bot/graphkind-universos/actions"><img src="https://github.com/cripto-bot/graphkind-universos/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/status-private%20preprint-0b6b3a" alt="private preprint">
  <img src="https://img.shields.io/badge/verification-V1%E2%80%93V12%20asserts-26557a" alt="verifications">
  <img src="https://img.shields.io/badge/proof-(%E2%87%90)%20proved%20%C2%B7%20(%E2%87%92)%20verified-9a7b1f" alt="proof status">
</p>

<p align="center">
  <a href="README.es.md">Español</a> · <a href="index.html">Page (ES)</a> · <a href="index.en.html">Page (EN)</a> · <a href="paper/PAPER.md">Paper</a> · <a href="paper/PRUEBA-CARACTERIZACION.md">Proof</a> · <a href="reproduce.sh">Reproduce</a>
</p>

---

## Abstract

We classify the operators under which the **color refinement** (1-WL)
profile of a graph is invariant, inside a parametric family of
**observation universes** `(f, ι)` — `f` compresses neighborhood counts
and `ι` is an involution. The engine **proposed and verified** that the
color refinement partition is complement-invariant (call it **T4**; the
conjecture mechanism was human-built), verified it on **2,131,019
exhaustive graphs** (n≤7, 100.0000%) plus
19,407 adversarial ones, and a **written proof** was produced
(injectivity of the neighborhood-multiset subtraction). Parameterizing
the universe, the data — not the authors — selected the **count law**
`T4 ⟺ f(1) ≠ f(2)` (34/34 and 102/102), and further probing produced a
**characterization**:

$$
T4(\iota, f)\ \text{holds} \iff \iota \in S_n \cdot K
\quad\text{and}\quad
\bigl(\iota\ \text{changes the pair} \implies f(1) \neq f(2)\bigr),
\qquad
K = \{\mathrm{id},\ \mathrm{comp\_dir},\ \mathrm{transp},\ \mathrm{comp\_transp}\} \cong \mathbb{Z}_2 \times \mathbb{Z}_2 .
$$

The **forward direction is proved** (count mechanism); the **converse is
verified** exhaustively in n=4 (96 exact survivors, zero outside),
targeted in n=5 (6,424 witnesses), and on real data (molecules 100/100,
CST 94/94). Changing the **type** of the invariant — partition → orbit →
distribution → observer — T4 dies in a deterministic Z₃ universe, dies
under process randomness, survives under object randomness, and is
**inherited by the whole k-FWL hierarchy** (≡ (k+1)-WL; 51/51). Every claim is
reproducible with one command, each verification carrying an `assert`
with the exact number. Limits are declared; five of our own bugs were
caught by controls and are documented, not deleted.

---

## Contributions

1. **T4, proposed and verified by the engine**: `CR_k(G) = CR_k(Ḡ)` as partitions
   (not merely equal multisets of class sizes) — with a written proof.
2. **The count law** `f(1) ≠ f(2)`, **selected by the data** after two
   human hypotheses were refuted by the table.
3. **The characterization** `Sₙ·K` with (⇐) proved and (⇒) verified;
   the missing piece — **uniformity** — identified by falsification.
4. **The type change**: T4 across deterministic, dynamic, probabilistic
   and observer universes.
5. **Method**: freeze-before-interpret, negative controls, and five own
   bugs caught and recorded.

---

## 1. The theorem (T4)

Let `G = (V, E)` be a finite simple graph, `Ḡ` its complement, and
`CR_k(G)` the partition of `V` induced by round `k` of color refinement
with initial colors `f(type, degree)`.

> **Theorem (EXP-086).** For every `G` and every `k ≥ 0`:
> $$CR_k(G) = CR_k(\bar G)$$
> as partitions of the **same** vertex set `V` (color names differ; the
> classes are identical).
>
> **Corollary (T4).** The multisets of class sizes of the stable
> partitions of `CR(G)` and `CR(Ḡ)` coincide, and they coincide at every
> round.

<p align="center">
  <img src="assets/g-vs-gbar.svg" width="720" alt="G and its complement share the same partition">
</p>

<p align="center">
  <img src="assets/t4-particion.svg" width="820" alt="Real data: Q3 and its complement, colored by WL class — the same partition">
  <br><em>Real data: Q₃ and its complement, vertices colored by WL class — the partition is identical (T4).</em>
</p>
<p align="center">
  <img src="assets/t4-evolucion.svg" width="100%" alt="T4 round by round: G and its complement, colored by WL class at k=0..3">
  <br><em>Real data: the WL refinement round by round (k=0…3) — G and its complement keep the same classes at every level.</em>
</p>

**Proof (sketch).** *Base.* In `Ḡ`, `deg_Ḡ(v) = n−1−deg_G(v)`; since
`d ↦ n−1−d` is a bijection of degrees, the relation "same color" is the
same in `G` and `Ḡ`. *Step.* Assume `CR_k(G) = CR_k(Ḡ) =: P_k`. For
`v ∈ V`, the closed neighborhood in `Ḡ` is `N_Ḡ[v] = V ∖ N_G(v)`, and
its round-`k` color multiset is

$$M'_k(v) = T_k - \bigl(M_k(v) - [\mathrm{color}_k(v)]\bigr), \qquad T_k := \text{total color multiset of } P_k .$$

Since `T_k` is **fixed**, the map `M_k(v) ↦ M'_k(v)` is **injective**:
`u, v` have the same closed-neighborhood multiset in `G` iff they do in
`Ḡ`. Because `color_{k+1}(v)` is a deterministic function of
`(color_k(v), M_k(v))`, the relation "same color" is preserved, hence
`CR_{k+1}(G) = CR_{k+1}(Ḡ)`. ∎

*Status*: written proof (one page), verified on 2,131,019 exhaustive
graphs (n≤7), 19,407 adversarial, and 688/688 compatibility pairs;
**external review pending**. Full text:
[`paper/PRUEBA-T4.md`](paper/PRUEBA-T4.md) · cycle:
[`paper/TEOREMA-UNIVERSOS.md`](paper/TEOREMA-UNIVERSOS.md).

---

## 2. The count law

In the standard universe with an involution that changes the connected
pair:

$$
T4\ \text{holds} \iff f(1) \neq f(2).
$$

**Mechanism.** In the complement, a vertex with **1** neighbor in a class
gets `|c|−1` (which may be **2**): if `f` collapses 1 and 2, the duality
dies. What `f` does with 3, 4, 5… is irrelevant. Verified **34/34**
(17 functions × 2 involutions, n≤6) and shielded **102/102** (formal
definition of dual-global, 6 involutions × 17 functions).

<p align="center">
  <img src="assets/universos-mapa.svg" width="700" alt="The 34 universes of EXP-102: T4 holds iff f(1) != f(2)">
  <br><em>Real data: the 34 universes (17 functions × 2 involutions) — T4 holds exactly when f(1) ≠ f(2).</em>
</p>

---

## 3. The characterization

<p align="center">
  <img src="assets/klein.svg" width="720" alt="The Klein group: two halves, two conditions">
</p>

**Forward direction (proved).** For `ι = σ∘s∘c`:

| case | mechanism | condition |
|---|---|---|
| **σ** (relabel) | WL is isomorphism-invariant; the coloring transports bijectively | holds for **every** `f` |
| **s** (global in/out swap) | counts swap: `(in_D,out_D) → (out_D,in_D)`; the profile maps by `(f(a),f(b)) → (f(b),f(a))` | holds for **every** `f` |
| **c** (uniform complement) | counts map `m → |D|−m` (or `|D|−1−m`), a bijection | holds **iff** `f(1) ≠ f(2)` (counterexample at n=6 otherwise) |

The non-obvious piece is **uniformity**: preserving the pair is *not*
enough if the action is not uniform (`flip_inc0` preserves the pair and
dies 0/24). Outside `Sₙ·K`, everything dies.

**Converse (verified).**

| camera | result |
|---|---|
| n=4, induced space, exhaustive (528 iotas × 4096 digraphs) | **96 exact survivors** (= 24·4), **zero** outside |
| n=5, targeted (8,160 iotas) | 7,680 with valid witness; the 480 without are uniform |
| outside the space (10,000 random affine) | **10,000/10,000** with witness |
| witness existence (6,424 non-uniform) | **6,424/6,424** valid witnesses |
| real data | molecules **100/100** · CST **94/94** |

<p align="center">
  <img src="assets/caracterizacion.svg" width="620" alt="Real data: of the 528 induced iotas at n=4, exactly the 96 uniform ones survive">
  <br><em>Real data: of the 528 induced iotas at n=4, exactly the 96 uniform ones survive (= 24·4).</em>
</p>

**Autonomous search.** Given a language of 11 primitives + 3 combinators
(~400 recipes) and a rate/MDL criterion, the engine found that the best
**valid** witness is the `cycle` (**99.63%**, complexity 1) — better than
the human construction (97.8%). No valid recipe reaches 100%.

---

## 4. From conjecture to theorem candidate

<p align="center">
  <img src="assets/pipeline.svg" width="100%" alt="From autonomous conjecture to theorem candidate">
</p>

---

## 5. The type change

<p align="center">
  <img src="assets/universos.svg" width="100%" alt="The invariant changes type">
</p>

<p align="center">
  <img src="assets/cascada.svg" width="720" alt="Observer cascade: 26 to 0">
</p>

| universe | invariant | T4 | evidence |
|---|---|---|---|
| standard | partition | ✅ holds (proved) | 2,131,019/2,131,019 |
| deterministic Z₃ | **orbit** (periods) | ❌ dies | max 52.4% (`maj`); 6 rules |
| random R1 (async WL) | **distribution** | ❌ dies | 204/1096 = 18.6% |
| random R2 (`G(n,p)` vs `G(n,1−p)`) | distribution | ✅ holds | exactly (complement bijects ensembles) |
| random R3 (random involutions) | **measure** | threshold = measure | 0/5000 uniform vs 96/528 induced |
| k-FWL hierarchy (≡ (k+1)-WL) | partition of k-tuples | ✅ inherited | 51/51 in k=1,2,3 |
| observer cascade (n≤7) | — | — | 26 → 0 (k=1 → k=2) |
| Rook vs Shrikhande | — | — | k=1 no, k=2 no, **k=3 yes** |

---

## 6. Method

- **Freeze before interpreting**: every experiment freezes
  `results_frozen.json` first.
- **Negative controls**: the check that caught the false "proof" (52/104
  uniform failures) and the wrongly built Shrikhande
  (`is_isomorphic = True`).
- **Five own bugs caught and recorded** (not deleted):

| # | bug | fix |
|---|---|---|
| 1 | multiset of sizes (weak: C6 and 2·C3 share it) | colors |
| 2 | comparing colors across graphs | compare partitions |
| 3 | indices in the initial coloring | degrees + adjacencies |
| 4 | separated multisets (weak k-WL) | correlated pairs (= k-FWL) |
| 5 | wrongly built Shrikhande (it was the Rook twice) | `is_isomorphic` |

**The method is part of the result.**

---

## 7. Reproduce

```bash
git clone https://github.com/cripto-bot/graphkind-universos
cd graphkind-universos
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
bash reproduce.sh            # V1–V12 (~10-15 min)
bash reproduce.sh --rapido   # V1, V3, V5, V8, V10, V11 (~3 min)
```

Every verification carries an **assert** with the exact number from the
paper: if anything does not match, it fails. CI runs the fast subset on
every push and the full suite on demand.

| # | verification | assert |
|---|---|---|
| V1 | the law `f(1)≠f(2)` (17 f × 2 involutions, n≤6) | 34/34 |
| V2 | characterization n=4 exhaustive | 96 and 48 |
| V3 | T4_k complement-invariance (k-FWL) | 51/51 |
| V4 | observer cascade n≤7 | 26 → 0 |
| V5 | Rook vs Shrikhande (k-FWL; 3-WL std does NOT) | k*=3 |
| V6 | deterministic Z₃ | does not hold |
| V7 | random R1 | 204/1096 |
| V8 | R3 measure dependence | 96/528 |
| V9 | autonomous search | cycle 99.63% |
| V10 | hash certificate (12-hex == 64-hex) | no collisions |
| V11 | convergence certificate (stable == n+2) | OK |
| V12 | classification constant across graphs (n=4) | OK |


---

## 7b. Corrections (2026-09-13)

Independent verification (EXP-159 of the lab) found a **naming error** and
two certificates were added:

1. **k-FWL, not "k-WL"** (D-005). The kernel implemented in `codigo/wl.py`
   is the **correlated** one (*folklore*, k-FWL), equivalent to
   **(k+1)-WL**. The plain name "k-WL" is the standard variant (position-
   separated multisets), which is strictly weaker: **standard 3-WL does
   NOT separate Rook from Shrikhande**; 3-FWL (≡ 4-WL) does. The code,
   docstrings and prints now say `k-FWL (≡ (k+1)-WL)`. V3/V5 are unchanged
   numerically.
2. **V10 — hash certificate**: the 12-hex hash does not alter any
   partition (12-hex partition == 64-hex partition over 74 graphs × 17 f).
3. **V11 — convergence certificate**: the refinement reaches its stable
   partition within the n+2 cap (stable == fixed n+2 rounds over 1098
   graphs × 17 f); `wl_sym`/`wl_k_colors` now stop at convergence.
4. **V12 — classification scope**: `clasificar_involucion` classifies on
   **one graph**; V12 verifies that the class is constant across all
   graphs n=4 for the tested (ι, f). The universal statement remains the
   open direction of the paper.

The numerical results of the paper are **unchanged**; the naming and the
certificates are the corrections.

---

## 7c. The universe arc (v2, EXP-162 → 169)

The v2 adds the **universe arc** (multilayer, matrix, hypergraphs,
arities, dual), with its freezes in `resultados/` and **V13–V16** in
`codigo/verificaciones_v2.py`:

| # | verification | assert |
|---|---|---|
| V13 | multilayer: total holds, **per-layer dies** in the canonical variant, channels hold | 4160/4160 · failures > 0 · 8320/8320 |
| V14 | 3-uniform hypergraphs: T4 holds | 6042/6042 (n≤5 + n=6 sample) |
| V15 | per-arity dual: partition + saving | 1024/1024 · 5120→3392 edges |
| V16 | mixed arities: per-arity **holds** (repair) | 1024/1024 |
| V17 | complement quotient (T4's price) | 52 graphs · 24 pairs (SG-01 n≤8: 6,168) |
| V18 | IR: IR_1 does not separate Rook/Shri, IR_2 does | i\*=2 |
| V19 | SG-04 certificate: n=10 exhaustive, no failures | 12,005,168 · 0 collisions |


<p align="center">
  <img src="assets/multicapa-ley.svg" width="760" alt="Multilayer law">
  <br><em>The multilayer coherence law (EXP-162/163): total holds, per-layer dies in the canonical variant.</em>
</p>


<p align="center">
  <img src="assets/escalera-kstar.svg" width="760" alt="k* ladder">
  <br><em>The k\*(L) ladder is flat and corrects EXP-162's k\*=2.</em>
</p>

**Results**: (1) **multilayer** — the coherence law: total holds
(1298/1298, 1404/1404), per-layer dies only in the canonical variant
(6.9%/7.4%); the preserving group is exactly the uniform one; the `k*`
ladder is flat (corrects EXP-162's `k*=2`); (⇐) proved, (⇒) open.
(2) **matrix** — the frontier moves with the observer, not with typing.
(3) **hypergraphs** — prediction registered and correct (1831/1831).
(4) **arities** — the ladder holds; the per-arity transplant **fails**
(the law is of channels). (5) **per-arity dual** — assimilated: partition
100%, saving 14.37% vs 10.26%.


<p align="center">
  <img src="assets/matriz-universo-observador.svg" width="860" alt="Matrix">
  <br><em>The frontier moves with the observer, not with typing.</em>
</p>


<p align="center">
  <img src="assets/hipergrafos-aridades.svg" width="820" alt="Hypergraphs">
  <br><em>Prediction correct (1831/1831) and the arity transplant that fails.</em>
</p>


<p align="center">
  <img src="assets/dual-aridad.svg" width="760" alt="Dual">
  <br><em>Per-arity dual: 14.37% saving with guaranteed partition.</em>
</p>


<p align="center">
  <img src="assets/trayectoria-refinamiento.svg" width="840" alt="Trajectory">
  <br><em>The refinement trajectory: T4 and the multilayer divergence.</em>
</p>


<p align="center">
  <img src="assets/aridades.svg" width="840" alt="Arities">
  <br><em>The arity ladder and the failing transplant.</em>
</p>

## 7d. The Holy Grail (SG-01→03)

- **Completeness in the class**: the minimal family is **{WL, 2-WL,
  3-WL}** with **C_8 = 0** over **76,205,685 pairs** (n≤8); leave-one-out:
  k-WL 3 does the work; the n=16 frontier (Rook/Shri) is separated only by
  the full family. Freeze: `resultados/SG-01_results_frozen.json`.

<p align="center">
  <img src="assets/frontera-Cn.svg" width="760" alt="Frontier C_n">
  <br><em>The frontier curves per observer (SG-01/03, EXP-119).</em>
</p>

- **The price of T4**: the complete invariant is **not**
  complement-invariant; the quotient `G~Ḡ` merges **6,168 pairs**.
- **Individualization**: **i\*=1** at n≤8 (13,597 graphs); **i\*=2** at
  Rook/Shrikhande (IR_1 no, IR_2 yes). The IR↔k-WL lattice: at n≤9 the
  complete ones collapse (vacuous equivalence); anchors A/B, C not
  observed. Freezes: `SG-02`, `SG-03`.

<p align="center">
  <img src="assets/santo-grial.svg" width="820" alt="Holy Grail">
  <br><em>Completeness, T4's price and i\*.</em>
</p>

- **The multilayer proof** ships in `paper/PRUEBA-MULTICAPA.md` ((⇐)
  proved, (⇒) open) and the **transversal patterns** + `DECISION_LOG`
  (D-001→D-017) in `paper/DECISION_LOG.md`.

## 7e. SG-04: the door (n=10 exhaustive)

- **0 collisions** over **12,005,168** exhaustive n=10 graphs (KW3/IR1p,
  11.1 h) → the first incompleteness is **not at n=10**.
- Directed: 9 regular combos n=11–15 (cap 5,000) + 10 Cayley/Paley/Q4
  pairs → **0 failures**.
- The first known failure remains at **n=16** (Rook/Shri): separated by
  **elementary descriptors** (SNFL, AUT, CICLOS, LOCAL, HOM2) + KF3/IR2p.
  Freeze: `resultados/SG-04_results_frozen.json` (certificate V19).
- Registered correction: `geng -d 3` (separated) fails; it is `-d3`.

## 8. Repository structure

```
paper/PAPER.md                   the paper (bilingual abstract, method, results, §12 v2 arc)
paper/TEOREMA-UNIVERSOS.md       the full cycle EXP-099→119
paper/PRUEBA-CARACTERIZACION.md  the (⇐) proof and the status of (⇒)
codigo/universos.py              the law inside the engine (t4_garantizado, oracle)
codigo/wl.py                     symmetric WL + correlated k-FWL (≡ (k+1)-WL)
codigo/verificaciones.py         V1–V12 with asserts of the exact numbers
paper/PRUEBA-MULTICAPA.md        (⇐) proved, (⇒) open (EXP-162)
paper/DECISION_LOG.md            laboratory decisions D-001→D-017
resultados/*.json                original freezes (EXP-102..169 + SG-01..04)
resultados/atlas/*.json          the atlas: 15 universes (EXP-105)
assets/*.svg                     figures
index.html · index.en.html       presentation pages (ES/EN)
```

---

## 9. Limits and open problems

- **(⇒) for all n: open.** Verified in n≤4 exhaustive, n=5 targeted,
  and real data; the ∀n argument is the remaining step.
- **Sufficiency of `f(1)≠f(2)` for arbitrary `f`**: verified in the
  catalogs; general proof open.
- **The full affine space n≥5** is intractable (involutions of S₂₀); the
  tested space is the induced one plus random affine.
- **T4**: written proof, **external review pending**; Lean formalization
  not available in the environment.
- **Universes**: our own definitions, declared; the space is open.
- **Data**: ChEMBL (CC-BY 4.0), CodeSearchNet, UniProt, Pfam — cited;
  fixed samples by seed.

---

## 10. References (selection)

- Weisfeiler, Leman (1968). *A reduction of a graph to a canonical form…*
- Morgan (1965); Rogers, Hahn (2010). *Extended-connectivity fingerprints.*
- Dvořák (2010); Dell, Arvind, Larsson (2018). *Homomorphisms and 1-WL.*
- Babai (2016). *Graph isomorphism in quasipolynomial time.*
- Xu et al. (2019). *How powerful are graph neural networks?*
- Morris et al. (2019). *Weisfeiler and Leman go neural.*
- Zamfirescu (1980). *Non-traceable 3-connected planar cubic graphs.*
- Lovász (1970). *Problem on vertex-transitive graphs.*

---


---

## 11. The laboratory behind this result

This paper is one thread of a **120-experiment laboratory**
(EXP-000 → EXP-120; **26,384** lines of `run.py`; **321 KB** of frozen
results) spanning six arcs. Every number here is anchored to a frozen
artifact, and a meta-experiment (**EXP-120**) verifies the laboratory's
key claims: **26/26 hits**.

| arc | range | what it built |
|---|---|---|
| Foundational | 000–010 | taxonomy collapse **0.5876**; molecules 3.00×; parity with Morgan **1.0000 vs 0.9973**; granularity k\*=21→24 |
| Riemann | 011–019 | 2,001,052 zeros; JS **0.1350 vs 0.0161**; Euler bridge **0.16110 ⊃ 1/2π**; critical line **σ\*=0.50000**; clean negatives |
| Arithmetic/Algebra/Physics | 020–046 | r\* emerged (**0.8934**); discrete WL = Morgan (**0.8877 vs 0.8864**); structural calculus with no rules; NS-3D verified |
| Discovery/Ontology | 047–079 | real code (129 chains / 119 rings / 152 stars); **6/6 protein hypotheses rejected by controls**; emergent math (λ=νn², ABC 6/6, cascade √5, Euler limit ~1.2); the tribunal |
| **T4** | 080–098 | 68/68 → 19,407 → **2,131,019/2,131,019**; written proof; `refine_dual` 10.3× / 40.5%; conjecture bank |
| **Universes** | 099–120 | this paper: law, characterization, witnesses, autonomous search, Z₃, random, k-FWL |
| **Universes v2** | 162–169 | multilayer (uniform law, group, k\* ladder), universe×observer matrix, hypergraphs (prediction), arities, arity dual |

**Transversal patterns**: freeze before interpreting · negative controls
(single-pass shuffle is not evidence: it varies 0.05–0.84) · five of our
own bugs caught and **recorded, not deleted** · four types of result:
kinds → laws → theorems → universes.

Full map: [`paper/MAPA-DEL-LABORATORIO.md`](paper/MAPA-DEL-LABORATORIO.md).


## 12. The engine: how it works and its measured power

<p align="center">
  <img src="assets/motor-como-funciona.svg" width="100%" alt="How it works: iterative 1-WL refinement on a real 8-node example">
  <br><em>The engine pipeline: data → graph → label₀ → round → STOP → kinds; the example shows rounds 3 → 5 → 5 → 5 up to the stable partition.</em>
</p>

<p align="center">
  <img src="assets/motor-potencia.svg" width="100%" alt="The engine's power, in real numbers">
  <br><em>Measured power: parity with Morgan (AUC 0.9608 vs 0.9541), compression 3.00× (molecules) and 187.5× (code), <code>refine_dual</code> 10.3×, dual-normalization saving 40.5%, universe oracle 87/87, engine tests 104/104, T4 bank 2.13M.</em>
</p>

<p align="center">
  <sub>© 2026 Juri (cripto-bot) · preprint · <a href="LICENSE">CC-BY-4.0</a> license (attribution required).<br>
  This document claims no priority over open problems: it reports a verified characterization in a bounded domain.<br>
  Cite as: see <a href="CITATION.cff">CITATION.cff</a>.</sub>
</p>
