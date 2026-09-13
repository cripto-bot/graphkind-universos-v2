# Prueba de T4 (versión fuerte) — la dualidad de particiones del color refinement

> Fabrica: GraphKind · 2026-09-09 · EXP-086
> Estado: **prueba escrita** (verificada empíricamente en 2 131 019 grafos
> exhaustivos n≤7 + 19 407 adversariales + SRG dirigidos).
> Pendiente: revisión externa/bibliográfica y formalización asistida.

---

## Enunciado (versión fuerte)

Sea `G = (V, E)` un grafo finito simple y `Ḡ` su complemento. Sea
`CR_k(G)` la partición de `V` inducida por la ronda `k` del color
refinement (1-WL) con colores iniciales `f(tipo, grado)`.

> **Teorema.** Para todo `G` y todo `k ≥ 0`:
> `CR_k(G) = CR_k(Ḡ)` **como particiones del mismo conjunto `V`**
> (los nombres de los colores difieren; las clases son idénticas).
>
> **Corolario (T4).** Los multisets de tamaños de las clases finales de
> `CR(G)` y `CR(Ḡ)` coinciden; y también coinciden para cada ronda.

## Prueba

**Base (k = 0).** El color inicial de un vértice es una función
`f(tipo(v), deg(v))` (en el motor: `kind|value` + número de aristas
incidentes). En `Ḡ`: `deg_Ḡ(v) = n − 1 − deg_G(v)`. La clase de color de
un vértice en `G` está determinada por su grado, y en `Ḡ` también:
como `d ↦ n−1−d` es una biyección de los grados, la relación
"mismo color" sobre `V` es la misma en `G` y en `Ḡ` (sólo cambia el
nombre del color). Por lo tanto `CR_0(G) = CR_0(Ḡ)`. ∎(base)

**Paso inductivo.** Supongamos `CR_k(G) = CR_k(Ḡ) =: P_k` (como
particiones; existe un renombrado biyectivo `ψ_k` entre los colores de
`G` y los de `Ḡ` compatible con `P_k`).

Fijemos `v ∈ V`. Sea `N_G[v]` la clausura de vecindad en `G` y
`M_k(v)` el multiset de colores de ronda `k` de los vértices de
`N_G[v]`. En `Ḡ`, la clausura de vecindad es `N_Ḡ[v] = V \ N_G(v)`
(complemento de los vecinos, incluyendo a `v`), y su multiset de
colores de ronda `k` es

```
M'_k(v) = T_k − (M_k(v) − [color_k(v)]) ,   T_k := multiset total de colores de P_k
```

donde la resta es de multisets (válida porque `N_Ḡ[v] ⊆ V` y los
colores son los de `P_k`). Como `T_k` es **fijo** (depende sólo de
`P_k`), la aplicación `M_k(v) ↦ M'_k(v)` es **inyectiva**: dos vértices
`u, v` tienen el mismo multiset de vecinos (incluyéndose) en `G` si y
sólo si tienen el mismo en `Ḡ`.

El color de ronda `k+1` de `v` es, por definición del refinamiento,
una función determinística de `(color_k(v), M_k(v))` (el motor usa un
hash canónico de esa información). Por el renombrado `ψ_k` y la
inyectividad anterior:

```
color_{k+1}(u) = color_{k+1}(v) en G
  ⇔ ( color_k(u) = color_k(v)  y  M_k(u) = M_k(v) ) en G
  ⇔ ( ψ_k(color_k(u)) = ψ_k(color_k(v))  y  M'_k(u) = M'_k(v) ) en Ḡ
  ⇔ color_{k+1}(u) = color_{k+1}(v) en Ḡ .
```

Es decir: la relación "mismo color" en la ronda `k+1` es idéntica en
`G` y en `Ḡ`; por lo tanto `CR_{k+1}(G) = CR_{k+1}(Ḡ)`. ∎(paso)

**Conclusión.** Por inducción, `CR_k(G) = CR_k(Ḡ)` para todo `k`; en
particular la partición estable coincide y los multisets de tamaños
coinciden (T4). ∎

## Observaciones

1. **El punto fino** (el que el esbozo original no fijaba): la
   inducción **no** se hace sobre los *tamaños* de las clases, sino
   sobre las **particiones mismas** (mismo conjunto de vértices). La
   identidad de particiones se preserva porque el complemento de la
   vecindad es `V \ N_G(v)` y la resta de multisets con total fijo es
   inyectiva. Con sólo los tamaños el paso no cerraría (habría que
   inventar la biyección).
2. **La biyección es explícita**: `ψ_k` asigna al color de `v` en `G`
   el color de `v` en `Ḡ` (la identidad sobre `V`).
3. **Verificación empírica** (el motor, EXP-086): la versión fuerte
   (particiones idénticas) se cumple en **2 131 019/2 131 019** grafos
   exhaustivos de n≤7, en los SRG dirigidos (rook 4×4, Shrikhande,
   Paley 13/17, Petersen) y en 192 cúbicos aleatorios asimétricos; el
   lema por ronda (multisets) ya se había verificado en el EXP-084.
4. **Alcance**: grafos finitos simples, sin lazos, con colores
   iniciales dependientes del grado (cualquier refinamiento "natural"
   por vecindad). Digrafos o colores iniciales arbitrarios: fuera del
   enunciado (anotado).
5. **Estatus**: prueba escrita (una página); la validación externa
   (revisión humana, bibliografía, Lean) sigue pendiente — si algún
   paso fallara en revisión, el contraejemplo estaría en la clase
   "particiones iguales pero paso roto", que el exhaustivo n≤7 no
   contiene.

## Por qué importa

- Convierte T4 de "invariante empírica" en **teorema con prueba**
  (sujeto a revisión), y explica *por qué* el sistema nunca encontró
  contraejemplo: la partición del color refinement es un invariante
  exacto de la dualidad G/Ḡ.
- Habilita las capacidades (085) con base firme: el fingerprint (y la
  partición) son los mismos para G y Ḡ **demostrado**, no sólo medido.


---

# Sección añadida (EXP-089): Rigidez del complemento bajo 1-WL (C1'')

## La conjetura afilada (y su corrección)

La versión estrecha propuesta — "f preserva para todo G ⇔ f = σ∘(·)ᵋ"
(identidad o complemento) — es **falsa por mezclas** (EXP-089):
`f(G) = G si G es bipartito, si no Ḡ` preserva la partición para todo
G (ambos lados la preservan), es isomorfismo-natural, y **no** es
identidad ni complemento. Lo mismo `f(G) = G si G es conexo, si no Ḡ`.
Ambas dieron **300/300 = 100%**.

## La formulación correcta (C1'')

> Sea `f` una operación sobre grafos simples con `V` fijo, **isomorfismo-
> natural** (equivariante: `f(σ(G)) = σ(f(G))` para todo isomorfismo σ).
> Si `f` preserva la partición del color refinement para todo `G`,
> entonces para cada `G`: **`f(G)` es isomorfo a `G` o a `Ḡ`** (vía el
> renombrado natural), pudiendo la elección depender de la clase de
> isomorfismo de `G` según invariantes.
>
> La parte sustantiva: **la única operación natural que cambia aristas
> de manera distinta al complemento es inexistente**: toda operación
> que cambie aristas "de verdad" rompe la preservación universal.

## Evidencia adversarial (EXP-089, 300 grafos aleatorios n 8-18)

| operación | preservación | |
|---|---|---|
| identidad | 300/300 = 100% | trivial |
| complemento | 300/300 = 100% | T4 (086) |
| mezcla(bipartito) | 300/300 = 100% | contraejemplo de la versión estrecha |
| mezcla(conexo) | 300/300 = 100% | idem |
| relabel canónico WL | 300/300 (perfiles) | trivial (renombrado) |
| **switch canónico** | **298/300 = 99.3%** | **el más cercano: falla (2 testigos)** |
| add-edge canónico | 270/300 = 90.0% | falla |
| remove-edge canónico | 241/300 = 80.3% | falla |
| potencia G² | 28/300 = 9.3% | falla (no inyectiva) |

## Estado

- **Suficiencia** de C1'': trivial (identidad, complemento y sus mezclas
  por invariantes preservan: T4).
- **Necesidad**: la evidencia adversarial (ninguna operación que cambie
  aristas preserva universalmente; el switch canónico — el candidato
  más fuerte — falla en 2/300) **apoya** la rigidez; la prueba general
  es trabajo matemático externo.
- El **line graph** (087) queda como confirmación: cambia `V` y no es
  de la forma σ(·)ᵋ: falla.
