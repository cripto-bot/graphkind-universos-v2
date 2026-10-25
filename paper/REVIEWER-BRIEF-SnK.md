# Reviewer brief — the Sₙ·K characterization (GraphKind / universes)

## 0. What we ask you to review

Not the complement invariance of color refinement (that is known), but **the
characterization of which uniform involutions preserve the 1-WL partition and
for which count compressions**, together with the count law `f(1) ≠ f(2)`.

## 1. Exact definitions

- Finite graph/digraph `G=(V,E)`, `|V|=n`, no loops.
- Symmetric WL: initial color `c_0(v)=f(type(v), deg(v))`; in each round, for
  each class `D` of the current partition, count
  `m_D^in(v)=|{u∈D:(u,v)∈E}|` and `m_D^out(v)=|{u∈D:(v,u)∈E}|`, and update
  `c_{k+1}(v)=H(c_k(v), {(c, f(m_D^in), f(m_D^out))})`.
- `CR_k(G)` = partition of `V` induced by `c_k`.
- Universe: a pair `(ι,f)`, with `f:N→N` and `ι` an involution on graphs.
- `T4(ι,f) :⇔ ∀G ∀k, CR_k(G)=CR_k(ι(G))` as partitions of `V`.

## 2. Claims

- **C1 (complement).** `CR_k(G)=CR_k(Ḡ)` for every `k`.
  Written proof (multisets: `M'_k(v)=T_k−(M_k(v)−[c_k(v)])`, injective).
  This is a special case of the complement closure already used by Kiefer &
  de Mel (Lemma 4.5, SODA 2026) and close to the flip lemma of
  Kiefer–Schweitzer–Selman.
- **C2 (count law).** For a dual-global `ι`:
  `T4(ι,f) ⇔ f(1)≠f(2)`.
  Verified 34/34 (17 f × 2 involutions, n≤6) and 102/102.
- **C3 (characterization).**
  `T4(ι,f) ⇔ ι∈S_n·K ∧ (c=1 ⇒ f(1)≠f(2))`,
  `K={id, comp_dir, transp, comp_transp}≅Z_2×Z_2`,
  with `ι=σ∘s∘c`, `σ∈S_n`, `s` a global in/out swap, `c` a uniform
  complementation (constant on the σ-orbits of pairs). Uniformity is the
  non-obvious clause: preserving the pair is not enough (`flip_inc0` dies
  0/24).

## 3. Status

| piece | status |
|---|---|
| C1 | written proof; external review pending |
| C2 | verified on catalogs; general proof for arbitrary f **open** |
| C3 (⇐) | proved: σ and s for every f; c ⇔ f(1)≠f(2) |
| C3 (⇒) | verified n=4 exhaustive (96=24·4), n=5 targeted (6,424 witnesses), real data; **open ∀n** |
| 2,131,019 | **reproduced with partitions** (not profiles): 2,131,019/2,131,019, 0 mismatches, double run identical, sha256 `cdb16f5c…`; script `codigo/verificaciones_particiones.py` |
| V3 k=1 | **fixed**: `wl_k_colors(...,k=1)` did not refine (empty pair loop); V3 k=1 was the degree partition, not 1-WL |

## 4. Closest prior art (positioning, not copying)

1. **Kiefer & de Mel**, *A Classification of Long-Refinement Graphs for
   Colour Refinement*, SODA 2026 (DOI 10.1137/1.9781611978971.18), Lemma 4.5:
   complement closure of the color-refinement partition; used to transfer the
   low-degree classification to high degrees. **This is C1, not C3.**
2. **Kiefer, Schweitzer & Selman**, *Graphs Identified by Logics with
   Counting*, ICALP 2015 (arXiv 1503.08792), Definition 11 + Lemma 12
   ("flip"): for each pair of C² classes `(P,Q)`, if there are more edges than
   non-edges, complement `[P,Q]`. This is a **local per-class-pair
   normalization**, coloring-dependent; it is **not** a global uniform
   involution. **It does not imply Sₙ·K**, but a reviewer will ask about the
   relation.
3. **Grohe, Kersting, Mladenov & Selman**, *Graph Isomorphism, Color
   Refinement, and Compactness* (Computational Complexity, 2017; arXiv
   1502.01255). No characterization.
4. **Bianchi, Grattarola & Alippi**, *Rethinking pooling in GNNs* (NeurIPS
   2020): clustering on the complement graph; empirical, not theoretical.

## 5. Questions for the reviewer

1. Is the `S_n·K` characterization already implied by the flip lemma or by a
   theory of "uniform switching" / "Seidel switching" we did not find?
2. Is the law `f(1)≠f(2)` for arbitrary `f` a known quantization/compression
   result in WL/C², or new?
3. Can the (⇒) direction for all `n` be proved with equitable partitions /
   the flip lemma, or does it require a witness search?
4. Is the relativity to the WL variant (symmetric vs out-only; `transp`
   changes from dual to local) formalized correctly?
5. Is the C1 proof correct in the inductive step with partitions (not only
   class sizes)?

## 6. What not to claim

- Do not claim the complement invariance as new.
- Do not claim the flip lemma as ours.
- Do not say "2,131,019 exhaustive" without clarifying that the new
  certificate compares partitions and that the original V1 compared profiles.
- Do not sell this as a CASMI/Kaggle tool: molecular graphs are sparse and the
  complement has no chemical meaning.
