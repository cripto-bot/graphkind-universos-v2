# Textos para comunidad (copiar y pegar)

> Regla: cada aparición **aporta contenido** (la cifra, el demo). Nada de
> "miren mi paper". Responder preguntas. No spamear.

---

## Show HN

**Título:**
`Show HN: GraphKind – an interactive map of the graph-isomorphism frontier`

**Texto (primer comentario):**

I built an interactive explainer for a graph-theory question that has been
open for ~50 years: does a *complete* isomorphism invariant exist?

We didn't answer it. We gave it coordinates. Measured results (all from
frozen runs, negative controls included):

- Complete up to n=10: 12,005,168 graphs swept exhaustively, zero
  collisions for {WL, 2-WL, 3-WL}. First known failure at n=16:
  Rook/Shrikhande, the classic cospectral pair.
- The observer lattice, measured side by side: WL = 2-WL for n≤9; IR₁ fails
  exactly where 3-WL fails; IR₂ behaves like 3-FWL ≡ 4-WL; Laplacian SNF
  separates the cospectral pair.
- Incompleteness is a property of the *(universe, observer)* pair, not of
  the object.
- The price of complement-invariance (theorem T4): exactly 6,168 fused
  pairs at n≤8 — and a complete invariant cannot be complement-invariant.

The demo runs the actual refinement in your browser: a T4 round-by-round
slider, and a "does it separate?" panel for C₆/2·C₃, Petersen/prism and
Rook/Shrikhande with WL / k=2 / k=3 (k-FWL ≡ (k+1)-WL).

Paper (PDF), code, data: https://doi.org/10.5281/zenodo.22747350 (CC-BY-4.0)

Happy to answer questions about the method (freeze-before-interpret,
mandatory negative controls, A/B/C/D attribution) or the math.

---

## Lobsters

**Título:** `GraphKind: an interactive map of the graph-isomorphism frontier`

**Texto:**

Same body as HN (shortened):

A lab notebook turned into an interactive explainer: where does color
refinement (and its higher-order variants) stop being complete? Measured:
complete up to n=10 by exhaustive sweep (12M graphs), first known failure
at n=16 (Rook/Shrikhande). The observer lattice measured side by side
(WL=2-WL n≤9; IR₁↔3-WL; IR₂↔3-FWL/4-WL; Laplacian SNF). Incompleteness is
relative to the (universe, observer) pair. Price of complement-invariance:
6,168 pairs.

Interactive demos + paper: https://huggingface.co/spaces/Jose-dev/graphlab-discoveries-demo
DOI: https://doi.org/10.5281/zenodo.22747350

---

## Reddit (r/math)

**Título:** `Where color refinement stops being complete: measured frontier and an observer lattice (interactive demo)`

**Texto:**

I run a small computational lab on structural invariants. We spent the last
months measuring — not conjecturing — where the known isomorphism
invariants stop working, and the result is a map rather than a theorem:

- **Frontier**: complete up to n=10 (12,005,168 graphs swept exhaustively,
  zero collisions for {WL, 2-WL, 3-WL}); first known failure at n=16
  (Rook/Shrikhande).
- **Observer lattice**: measured side by side on anchors — WL = 2-WL for
  n≤9; IR₁ fails exactly where 3-WL fails; IR₂ behaves like 3-FWL ≡ 4-WL;
  Laplacian SNF separates the cospectral pair.
- **Incompleteness is relative to the pair** (universe, observer): same
  graph, different universe, different answer.
- **The price of symmetry**: complement-invariance (T4) fuses exactly 6,168
  pairs at n≤8, and a complete invariant cannot be complement-invariant.

Everything is frozen before interpretation and has negative controls; the
limits (no complete invariant found, no impossibility proof, frontier
n=11..15 open) are declared in the paper.

Interactive demo (runs the refinement in your browser):
https://huggingface.co/spaces/Jose-dev/graphlab-discoveries-demo

Paper + data (CC-BY-4.0): https://doi.org/10.5281/zenodo.22747350

Feedback welcome — especially pointers to literature we should be comparing
against.

---

## Mastodon / Bluesky (hilo corto)

1/ ¿Dónde deja de ser completo el color refinement? Lo medimos: completo
hasta n=10 (12 005 168 grafos, 0 colisiones); primera falla conocida en
n=16 (Rook/Shrikhande). No resolvimos la pregunta de los 50 años: le
pusimos coordenadas. 🧭

2/ El demo corre el refinamiento en tu navegador: T4 ronda a ronda, y
¿lo separa? con C₆/2·C₃, Petersen/prisma y Rook/Shrikhande.
https://huggingface.co/spaces/Jose-dev/graphlab-discoveries-demo

3/ Paper + datos (CC-BY-4.0): https://doi.org/10.5281/zenodo.22747350
#math #graphtheory #GraphIsomorphism #WeisfeilerLeman #openscience
