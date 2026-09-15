# Metadata para espejos académicos (HAL / OSF Preprints / Preprints.org)

> El mismo PDF (`paper/graphkind-v2.pdf`) se sube a cada espejo. El DOI de
> Zenodo ya existe: declararlo como **versión relacionada** para que los
> cosechadores unan los registros.

---

## Campos comunes

**Título (ES)**
GraphKind: descubrimiento estructural autónomo y leyes emergentes en universos de observación

**Título (EN)**
GraphKind: autonomous structural discovery and emergent laws in observation universes

**Autor**
Argaña Silguero, Josué · ORCID `0009-0009-1983-4711`

**Fecha**: 2026-09-14

**Tipo**: Preprint / Working paper

**Licencia**: CC-BY-4.0

**Idioma**: Español (abstract bilingüe)

**Páginas**: 15

**DOI relacionado (versión de registro)**: `10.5281/zenodo.22747350`
(URL: https://doi.org/10.5281/zenodo.22747350)

**Repositorio de código**: https://github.com/cripto-bot/graphkind-universos-v2

**Demo**: https://huggingface.co/spaces/Jose-dev/graphlab-discoveries-demo

**Dataset**: https://huggingface.co/datasets/Jose-dev/graphkind-universos

**Keywords (ES)**: color refinement; Weisfeiler–Leman; isomorfismo de
grafos; invariantes estructurales; T4; k-FWL; individualización; hipergrafos;
multicapa; matemática discreta.

**Keywords (EN)**: color refinement; Weisfeiler–Leman; graph isomorphism;
structural invariants; T4; k-FWL; individualization; hypergraphs;
multilayer; discrete mathematics.

---

## Abstract (ES)

Presentamos GraphKind, un motor de descubrimiento estructural que opera por
refinamiento iterativo de vecindades (1-WL / color refinement) sin
taxonomía previa, y un protocolo de laboratorio para descubrir, congelar,
identificar y verificar regularidades estructurales. El resultado central
es **T4**: la partición del refinamiento es invariante bajo complemento
(propuesto y verificado por el motor; prueba escrita), con un **precio**
medido — 6 168 pares fusionados en n≤8 — y una tensión estructural: un
invariante completo no puede ser complemento-invariante. Parametrizando el
universo de observación, la ley emergente `T4(ι,f) ⟺ ι ∈ Sₙ·K` y, cuando
`ι` cambia el par, `f(1) ≠ f(2)`, con la uniformidad como pieza faltante
(la disyunción humana fue falsada en ambas direcciones). El arco v2 mide la
**frontera de la completitud** (0 colisiones en 12 005 168 grafos n=10; la
primera falla conocida en n=16, Rook/Shrikhande), caracteriza el **retículo
de observadores** (WL = 2-WL en n≤9; IR₁ ↔ 3-WL; IR₂ ↔ 3-FWL/4-WL; SNF del
Laplaciano), demuestra que la incompletitud es del **par** (universo,
observador), y encuentra una **ley de composición** multicapa (`ℤ₂^L ⋊ S_L`)
y un **reparo** de hipergrafos por dualidad de aridad. Todos los números
salen de ejecuciones congeladas con controles negativos; los límites se
declaran.

## Abstract (EN)

We present GraphKind, a structural discovery engine based on iterated
neighborhood refinement (1-WL / color refinement) with no prior taxonomy,
plus a laboratory protocol to discover, freeze, identify and verify
structural regularities. The central result is **T4**: the refinement
partition is invariant under complement (proposed and verified by the
engine; written proof), with a measured **price** — 6,168 fused pairs at
n≤8 — and a structural tension: a complete invariant cannot be
complement-invariant. Parameterizing the observation universe yields the
emergent law `T4(ι,f) ⟺ ι ∈ Sₙ·K` and, when `ι` changes the pair,
`f(1) ≠ f(2)`, with uniformity as the missing piece. The v2 arc measures
the **completeness frontier** (0 collisions over 12,005,168 graphs at n=10;
first known failure at n=16, Rook/Shrikhande), characterizes the **observer
lattice** (WL = 2-WL for n≤9; IR₁ ↔ 3-WL; IR₂ ↔ 3-FWL/4-WL; Laplacian SNF),
shows that incompleteness belongs to the *(universe, observer)* pair, and
finds a **multilayer composition law** (`ℤ₂^L ⋊ S_L`) and a **hypergraph
repair** by arity duality. Every number comes from frozen runs with
negative controls; limits are declared.

---

## Pasos por servidor

### HAL (hal.science)
1. Cuenta + login.
2. *Déposer* → tipo **Preprint** (o *Working paper*).
3. Subir el PDF; completar los campos de arriba; en *Relaciones*:
   `is a version of` → `10.5281/zenodo.22747350`.
4. Colección sugerida: *Computer Science* / *Mathematics*.

### OSF Preprints (osf.io/preprints)
1. Cuenta + *Add a preprint*.
2. Servidor: `OSF Preprints` (genérico) o `arXiv` no aplica.
3. Subir el PDF; título/abstract/keywords; licencia CC-BY-4.0.
4. DOI: OSF emite el suyo; agregar el de Zenodo como *related work*.

### Preprints.org (MDPI)
1. Cuenta + *Submit preprint*.
2. Área: *Computer Science and Mathematics* → *Discrete Mathematics*.
3. Subir el PDF; completar; declarar el preprint de Zenodo como versión
   relacionada.

---

## Después de subir

- Anotar en `paper/ESTRATEGIA-VISIBILIDAD.md` (o en el DECISION_LOG) los
  DOI/URLs nuevos.
- Verificar en 2–4 semanas: Google Scholar, Semantic Scholar, OpenAlex.
