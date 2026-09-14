# El mapa y no la respuesta

### Invariantes de isomorfismo, observadores y una frontera medida

**Revisión y posición · laboratorio GraphKind · 2026-09-14**

**Autor**: [Juri] · con el motor GraphKind como instrumento.
**DOI (datos y código)**: [10.5281/zenodo.22747350](https://doi.org/10.5281/zenodo.22747350) · **Repo**: `cripto-bot/graphkind-universos-v2`.

---

## Resumen

El problema del isomorfismo de grafos —decidir si dos grafos son el mismo
objeto con otro nombre— es uno de los problemas abiertos clásicos de la
matemática. Su versión estructural pregunta si existe una **huella
completa**: un invariante que distinga todo par de grafos no isomorfos y
que se calcule en tiempo polinómico. No se conoce ninguna; la conjetura
corriente es que no existe una práctica. Este documento revisa el estado
del arte (color refinement, jerarquía k-WL, individualización y
refinamiento, invariantes algebraicos, conteos de homomorfismos) y sitúa
el aporte del laboratorio con una tesis modesta y precisa: **no
resolvimos la pregunta de los cincuenta años; le pusimos coordenadas.**
Medimos la frontera de la completitud en la clase de grafos pequeños
(completa hasta n=10 por barrido exhaustivo, primera falla conocida en
n=16), caracterizamos el orden de los observadores entre sí (WL = 2-WL en
n≤9; IR₁ ↔ 3-WL; IR₂ ↔ 3-FWL/4-WL), demostramos que la incompletitud es
una propiedad del **par** (universo, observador) y no del objeto,
cuantificamos el **precio de la simetría** bajo complemento (6 168 pares
fusionados en n≤8), encontramos una **ley de composición multicapa** y
medimos el **reparo de hipergrafos** por dualidad de aridad. Un mapa, en
matemática, no responde: redirige la pregunta. Eso es lo que ofrecemos.

**Abstract (English)**. Graph isomorphism —deciding whether two graphs are
the same object under renaming— is a classical open problem. Its
structural version asks for a *complete invariant*: a fingerprint
separating every non-isomorphic pair in polynomial time. None is known.
This document reviews the state of the art (color refinement, the k-WL
hierarchy, individualization-refinement, algebraic invariants,
homomorphism counts) and situates the laboratory's contribution with a
modest claim: **we did not solve the fifty-year question; we gave it
coordinates.** We measured the completeness frontier on small graphs
(complete up to n=10 by exhaustive sweep; first known failure at n=16),
characterized the order among observers, showed that incompleteness is a
property of the *(universe, observer)* pair rather than of the object,
quantified the **price of symmetry** under complement (6,168 fused pairs
for n≤8), found a **multilayer composition law**, and measured the
**hypergraph repair** by arity duality. A map does not answer; it
redirects. That is the offering.

---

## 1. La pregunta

Dos grafos son isomorfos si existe una biyección entre sus vértices que
preserva las aristas. Decidirlo es el **problema del isomorfismo de
grafos** (GI). No es un problema cualquiera: es el ejemplo canónico de
problema en NP que no se sabe si es P ni si es NP-completo, y su
resolución práctica mueve química computacional, verificación de
circuitos, bases de datos y criptografía.

Tres hechos delimitan el terreno:

1. **Hay algoritmos excelentes en la práctica.** `nauty`/`Traces`
   [McKay 1981; McKay & Piperno 2014] resuelven instancias enormes con
   individualización y refinamiento, aunque su peor caso es exponencial.
2. **Hay un algoritmo cuasi-polinomial.** Babai [2016] probó que GI se
   decide en tiempo `exp(O(log² n))`. Sigue abierto si existe uno
   polinómico.
3. **Los invariantes conocidos son incompletos.** Color refinement (1-WL)
   no distingue `C₆` de `2·C₃`; la jerarquía k-WL es estrictamente
   creciente [Cai, Fürer & Immerman 1992], y para cada k hay pares que
   solo `(k+1)`-WL separa.

La pregunta estructural es, entonces:

> ¿Existe un invariante **completo** —una huella que distinga todo par de
> grafos no isomorfos— que se calcule en tiempo polinómico?

Nadie lo encontró. Nadie probó que no exista. La conjetura general es que
no hay uno práctico.

---

## 2. Los observadores

Un **observador** es una función que asigna a cada grafo una firma, con
la propiedad de ser invariante bajo relabeling. La literatura ofrece una
familia:

- **Color refinement (1-WL)** [Weisfeiler & Leman 1968; Morgan 1965;
  Rogers & Hahn 2010]. Refina colores mirando el multiset de colores de
  los vecinos. Es el kernel de ECFP/Morgan en química y el techo
  expresivo de las GNN de paso de mensajes [Xu et al. 2019].
- **Jerarquía k-WL / k-FWL** [Weisfeiler & Leman 1968; Cai, Fürer &
  Immerman 1992; Grohe 2017]. Refina k-tuplas de vértices; la variante
  correlacionada (k-FWL) equivale a `(k+1)`-WL estándar. Para cada k hay
  pares que exigen k+1.
- **Individualización y refinamiento (IR)** [Babai & Kučera 1979; Arvind
  et al. 2015]. Fija vértices ("individualiza") y refina; `IR_k`
  individualiza hasta k vértices. Es la familia que usan los solvers
  prácticos.
- **Invariantes algebraicos.** Espectro del grafo y del Laplaciano
  [Godsil & Royle 2001]; hay pares cospectrales no isomorfos (el más
  famoso: el grafo torre y el de Shrikhande, SRG(16,6,2,2), [Shrikhande
  1959]). La forma normal de Smith (SNF) del Laplaciano es un invariante
  más fino que el espectro, y el laboratorio lo midió (EXP-161).
- **Conteos de homomorfismos** [Lovász 1967; Dvořák 2010; Dell, Arvind &
  Larsson 2018]. El vector de conteos `hom(F, ·)` sobre todas las clases
  F determina el grafo; los conteos acotados caracterizan el poder de WL.

Existen, además, generadores automáticos de conjeturas estructurales
(Graffiti, AutoGraphiX, la Máquina de Ramanujan, AlphaGeometry) que
comparten el espíritu de buscar regularidades. Nuestro motor pertenece a
esa familia, con dos diferencias: propone conjeturas **sobre su propio
invariante**, y su ley final fue **elegida refutando hipótesis humanas**,
no confirmándolas.

Lo que la literatura **no** ofrece es el orden entre observadores como un
objeto: se conocen las inclusiones teóricas, pero no un retículo medido,
par a par, en una clase de grafos. Eso es parte de lo que aportamos.

---

## 3. Lo que medimos

### 3.1 La frontera de la completitud

Sobre **todos** los grafos no isomorfos hasta n=8 (12 346 grafos; **76 205
685 pares**), la familia mínima que alcanza la completitud en la clase es
`F3 = {WL, 2-WL, 3-WL}`, con **cero colisiones**. El *leave-one-out*
muestra que **3-WL hace el trabajo**: sin él quedan 350 colisiones. El
control de relabeling (50/50) descarta fugas de etiquetas.

En **n=9** (274 668 grafos), todos los invariantes completos colapsan a la
misma partición discreta (equivalencia vacua) y `WL = 2-WL`: la evidencia
discriminante son las **anclas** (`C₆` vs `2·C₃`; Rook/Shrikhande).

En **n=10** el barrido exhaustivo (**12 005 168 grafos**, 11.1 h con 22
procesos) da **cero colisiones** para `KW3` e `IR₁p`: la primera
incompletitud **no está en n=10**. El corpus dirigido (9 combinaciones
regulares n=11–15 con tope 5 000, más 10 pares Cayley/Paley/Q₄) tampoco
falla.

La primera falla conocida sigue en **n=16**: el par **Rook/Shrikhande**,
cuyos espectros coinciden. Allí `F1–F6` colisionan y solo la familia
total lo separa; la huella muestra que lo separan descriptores
elementales (SNF del Laplaciano, automorfismos, ciclos, vecindad local,
conteos de homomorfismos) además de `KF3` e `IR₂p`. La frontera exacta
entre n=11 y n=15 queda abierta: el barrido es inabordable
(1019 millones de grafos en n=11).

**Resultado**: la frontera entre "completa" e "incompleta" quedó **medida,
no intuida**, para esta clase.

### 3.2 El retículo de observadores

En las anclas, el orden medido es:

| observador | comportamiento medido |
|---|---|
| WL | = 2-WL en n≤9; falla en `C₆`/`2·C₃` |
| 3-WL (estándar) | completa en n≤8; **no** separa Rook/Shrikhande |
| IR₁ | falla exactamente donde falla 3-WL |
| IR₂ | se comporta como 3-FWL ≡ 4-WL; **sí** separa Rook/Shrikhande |
| SNF del Laplaciano | separa Rook/Shrikhande |
| homomorfismos | separan donde WL acotado no alcanza |

Ese orden —un retículo medido, con anclas— no está tabulado así en la
literatura: existen los observadores; la comparación lado a lado, no.

### 3.3 La individualización mínima

Para los 13 597 grafos de n≤8, la individualización mínima es `i* = 1`:
ninguno necesita 0 (WL nunca es único en la clase) y ninguno necesita 2.
En la frontera, Rook/Shrikhande exige `i* = 2`. La individualización es,
así, una **escala**: mide cuántos vértices hay que fijar antes de que el
refinamiento sea completo.

---

## 4. La incompletitud es del par

La pregunta "¿existe un invariante completo?" está mal planteada, porque
su respuesta depende de tres elecciones:

1. **El universo**: grafos estándar, dinámicas sobre ℤ₃, ensembles
   aleatorios R1/R2/R3, objetos multicapa, hipergrafos.
2. **El observador**: WL, k-WL, k-FWL, IR, algebraico, homomorfismos.
3. **La operación**: complemento total, por capa, por aridad.

La incompletitud no es una propiedad del objeto. Es una propiedad del
**par**. Dos ejemplos medidos:

- En el universo **estándar**, el complemento total preserva la partición
  (T4). En **ℤ₃ determinista**, la dualidad del conteo no tiene análogo
  dinámico y T4 **muere** (máximo 52.4%). En el ensemble **R2** (azar en
  el objeto con la simetría correcta) T4 **vive** casi seguro; en **R1**
  (azar en el proceso) muere (18.6%).
- En **multicapa**, T4 vive si y solo si el complemento actúa
  uniformemente sobre las capas (ley de canales; §6). En **hipergrafos**
  de aridad mezclada, el transplante directo **falla** y hace falta el
  dual por aridad (§7).

**Reformulación**: la pregunta correcta no es "¿existe el invariante
completo?" sino **"¿qué ve cada observador en cada universo, y dónde se
mueve la frontera?"**. Esa es la pregunta que el mapa responde.

---

## 5. El precio de la simetría

T4 dice que la partición del color refinement es invariante bajo
complemento. Eso tiene un costo exacto: si imponemos
complemento-invarianza, el cociente `G ~ Ḡ` **fusiona 6 168 pares** en
n≤8 (con 10 grafos autocomplementarios). Esa es la información que T4
describe, cuantificada: la simetría se paga con pares indistinguibles.

Y hay una **tensión estructural**: un invariante completo **no puede** ser
complemento-invariante. Las dos propiedades son incompatibles por
construcción: si `I` es completo y `I(G) = I(Ḡ)` para todo `G`, entonces
`I` identifica pares no isomorfos siempre que `G` no sea
autocomplementario — y la mayoría de los grafos no lo son. Esto conecta
T4 con el problema del isomorfismo de forma directa: **la simetría que
hace elegante al invariante es la que lo vuelve incompleto**.

---

## 6. La ley multicapa

Cuando el universo tiene L capas acopladas, T4 deja de ser una propiedad
de un grafo y pasa a ser una propiedad de la **composición**:

> T4 vive en objetos acoplados **si y solo si** el complemento actúa
> **uniformemente** sobre las capas.

La estructura del grupo que preserva el perfil quedó caracterizada como
`ℤ₂^L ⋊ S_L` (complementos por capa, permutaciones de capas). La
coherencia se midió en 1 298/1 298 casos (L=2) y 1 404/1 404 (L=3); el
grupo preservante exacto es `U` en la versión canónica (4/4 y 12/12), y
la escalera `k*(L)` es plana (`k* = 1`). El **transplante** de la ley de
canales a universos de aridad mezclada **falla**: la ley es de la
composición, no del objeto.

---

## 7. El reparo de hipergrafos

En hipergrafos de aridad mezclada, la operación "complemento" puede
romper la invariancia. La pregunta es qué operaciones la **reparan**. La
respuesta medida: el **dual por aridad** es seguro — 261 000 casos,
21 821 fusiones dirigidas, **cero testigos** de fallo. La frontera entre
"rompe" y "repara" es el **tipo de mensaje** que la operación induce: no
es una cuestión de tamaño ni de densidad, es estructural. Distinción
medida, no supuesta. El dual por aridad entró al motor con partición
correcta en 60 000 casos y un ahorro del 14.37% frente al 10.26% de la
línea base.

---

## 8. Lo que NO resolvimos

Debe decirse sin ambigüedad:

- **No encontramos el invariante completo universal.** No existe, o no se
  sabe si existe.
- **No probamos que sea imposible.** Solo mostramos que ninguno de los
  observadores probados lo es en la clase medida.
- **No resolvimos P vs NP.** El isomorfismo sigue cuasi-polinomial
  [Babai 2016].
- **No medimos la frontera exacta entre n=11 y n=15.** Es inabordable por
  barrido (1019 millones de grafos en n=11); la primera falla conocida es
  n=16.
- **La dirección (⇒) de la caracterización multicapa** está verificada
  exhaustiva en n≤4 y dirigida en n=5; el `∀n` sigue abierto.

---

## 9. Cierre: el mapa

Convertimos una pregunta abierta en un objeto medible. No la resolvimos:
la **acotamos**.

- La completitud vive en **n≤10** (exhaustivo).
- La primera falla es **n=16** (Rook/Shrikhande).
- La frontera exacta está **entre esos dos**.
- La incompletitud es **relativa al par** (universo, observador).
- El costo de la simetría es **6 168 pares**.
- Hay una **ley de composición** multicapa.
- Hay un **reparo** de hipergrafos por dualidad de aridad.

Eso es un mapa, no una respuesta. Y los mapas, en matemática, son más
duraderos que las respuestas: redirigen la pregunta.

---

## Tabla de trazabilidad

| cifra | fuente (freeze/EXP) |
|---|---|
| 76 205 685 pares, `C₈=0`, 350 sin 3-WL | SG-01 |
| 6 168 pares fusionados, 10 autocomplementarios | SG-01 |
| `i*=1` (13 597 grafos); Rook/Shri `i*=2`; IR₁↔3-WL; IR₂↔3-FWL/4-WL | SG-02 / SG-03 |
| 274 668 grafos n=9; `WL=2-WL`; colapso de completos | SG-03 |
| 12 005 168 grafos n=10, 0 colisiones (KW3/IR1p) | SG-04 |
| capa dirigida n=11–15 + Cayley/Paley/Q₄: 0 fallas | SG-04 (capa 2) |
| 1 298/1 298 y 1 404/1 404 (coherencia multicapa) | EXP-162 / EXP-163 |
| grupo preservante `U` (4/4, 12/12); `k*` plana | EXP-163 / EXP-164 |
| matriz tipada n≤6 (5 342 clases); WL/KW2 n_min=6 | EXP-165 |
| hipergrafos 3-uniformes: 1 831/1 831; n_min=6 | EXP-166 |
| transplante por aridad falla; por aridad vive (1 038/1 038) | EXP-167 |
| 261 000 casos, 21 821 fusiones, 0 testigos | EXP-168 |
| dual por aridad: partición 100%; 14.37% vs 10.26% | EXP-169 |
| T4: 2 131 019 grafos exhaustivos + 19 407 adversariales; (⇐) probada | EXP-084 / T4 |

---

## Referencias (selección verificable)

- Weisfeiler, B., Leman, A. (1968). *A reduction of a graph to a canonical form and an algebra arising during this reduction.*
- Morgan, H. L. (1965). *The generation of a unique machine description for chemical structures.*
- Rogers, D., Hahn, M. (2010). *Extended-connectivity fingerprints.* J. Chem. Inf. Model.
- Cai, J., Fürer, M., Immerman, N. (1992). *An optimal lower bound on the number of variables for graph identification.* Combinatorica.
- Babai, L. (2016). *Graph isomorphism in quasipolynomial time.* STOC.
- Babai, L., Kučera, L. (1979). *Canonical labelling of graphs in linear average time.* FOCS.
- McKay, B. (1981). *Practical graph isomorphism.* Congressus Numerantium.
- McKay, B., Piperno, A. (2014). *Practical graph isomorphism, II.* J. Symbolic Computation.
- Lovász, L. (1967). *Operations with structures.* Acta Math. Acad. Sci. Hungar.
- Dvořák, Z. (2010). *On recognizing graphs by numbers of homomorphisms.* J. Graph Theory.
- Dell, H., Arvind, V., Larsson, J.-E. (2018). *Locality and the complexity of the Weisfeiler–Leman algorithm.*
- Grohe, M. (2017). *Descriptive Complexity, Canonisation, and Definable Graph Structure Theory.* Cambridge.
- Xu, K., Hu, W., Leskovec, J., Jegelka, S. (2019). *How powerful are graph neural networks?* ICLR.
- Morris, C. et al. (2019). *Weisfeiler and Leman go neural: higher-order graph neural networks.* AAAI.
- Godsil, C., Royle, G. (2001). *Algebraic Graph Theory.* Springer.
- Shrikhande, S. S. (1959). *The uniqueness of the L₂ association scheme.* Ann. Math. Statist.
- Arvind, V., Köbler, J., Rattan, G., Verbitsky, O. (2015). *On the power of color refinement.*
- Fajtlowicz, S. (1988). *On conjectures of Graffiti.*
- Caporaso, J. et al. (2021). *The Ramanujan Machine.* Nature.

---

*"El universo habla una gramática; el isomorfismo pregunta si dos frases
dicen lo mismo. Nosotros no respondimos la pregunta: dibujamos el mapa de
dónde se puede responder." — laboratorio GraphKind, 2026.*
