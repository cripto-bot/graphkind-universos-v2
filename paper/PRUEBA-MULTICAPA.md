# Prueba multicapa — T4 y la uniformidad entre canales

> Fabrica: GraphKind · 2026-09-13 · EXP-162 · D-010
> Estado: **(⇐) probada · (⇒) con gadget mínimo verificado y
> construcción general declarada abierta (∀L, S ⊂ {1..L})**.
> Evidencia empírica: complemento total 1298/1298 (L=2) y 1404/1404
> (L=3); complemento por capa 90/1298 (6.9%) y 104/1404 (7.4%) fallas
> (variante canónica). Testigos n=3 `(BO, BW)` y n=4 `(CC, C^)`.

---

## 0. Definiciones (fijadas en la spec, antes de correr)

- **Grafo multicapa** `𝓖 = (V, E_1, …, E_L)`: mismo `V`, capas
  etiquetadas, sin aristas cruzadas.
- **Refinamiento conjunto**, variante **canónica** (la primaria):
  `c_0(v) = H(multiset{deg_ℓ(v)})`;
  `c_{t+1}(v) = H(c_t(v) | multiset_ℓ{ multiset{c_t(w) : w ∈ N_ℓ(v)} })`.
  La variante **ordenada** usa tuplas en lugar de multisets.
- **Partición** `P(𝓖)`: la partición estable de `V` (versión fuerte).
- **T4(ι) vive** ⟺ `P(𝓖) = P(ι(𝓖))` como particiones del **mismo** `V`,
  para todo `𝓖` de la clase.
- **Operación uniforme sobre capas**: complementar **todas** las capas
  (eventualmente compuesta con una permutación de capas `π ∈ S_L` y un
  relabel `σ ∈ S_n`).
- **No uniforme**: complementar un subconjunto propio no vacío
  `S ⊂ {1..L}`, o mezclar capas de forma no uniforme.

## 1. (⇐) Probada: uniforme ⟹ T4

> **Teorema.** Si `ι` complementa todas las capas (y opcionalmente
> permuta capas y relabela vértices), entonces
> `P(𝓖) = P(ι(𝓖))`.

**Prueba** (inducción sobre rondas; se prueba la variante canónica; la
ordenada es idéntica coordenada a coordenada).

*Base (ronda 0).* El color inicial de `v` es el multiset de sus grados
por capa: `{deg_ℓ(v)}_{ℓ=1..L}`. En el complemento total,
`deg'_ℓ(v) = n − 1 − deg_ℓ(v)` para **cada** `ℓ`. La aplicación
`d ↦ n−1−d` es una biyección de `{0..n−1}`; aplicada **uniformemente a
todas las coordenadas**, transforma el multiset de grados en otro
multiset por una biyección. Por lo tanto la relación "mismo color
inicial" es la misma en `𝓖` y en `ι(𝓖)`: `P_0(𝓖) = P_0(ι(𝓖))`. ∎(base)

*Paso inductivo.* Supongamos `P_t(𝓖) = P_t(ι(𝓖)) =: P_t` (existe un
renombrado biyectivo `ψ_t` entre los colores de las dos coloraciones,
compatible con `P_t`). Fijemos `v ∈ V` y una capa `ℓ`. Sea

```
M_ℓ(v) := multiset de colores de ronda t de la vecindad cerrada N_ℓ[v] en 𝓖,
T     := multiset total de colores de P_t   (independiente de ℓ y de v).
```

En la capa complementada, la vecindad cerrada es
`N'_ℓ[v] = V ∖ N_ℓ(v)` (complemento de la vecindad abierta), y su
multiset de colores de ronda `t` es

```
M'_ℓ(v) = T − (M_ℓ(v) − [color_t(v)]) ,
```

donde `[color_t(v)]` es el multiset de un elemento con el color de `v`
(se resta `v` de su vecindad cerrada, se complementa respecto del total
`T`, y `v` vuelve a quedar incluido porque `v ∈ V ∖ N_ℓ(v)`).

Como `T` es **fijo** (depende solo de `P_t`), la aplicación
`M ↦ T − M` es **inyectiva** sobre multiséts de colores. Además es la
**misma** aplicación para toda capa `ℓ`. Entonces:

```
u, v tienen el mismo multiset (M_1(u), …, M_L(u)) en 𝓖
  ⇔ (aplicando la misma biyección inyectiva a cada coordenada)
u, v tienen el mismo multiset (M'_1(u), …, M'_L(u)) en ι(𝓖).
```

Como el color de ronda `t+1` es una función determinística de
`(color_t(v), (M_ℓ(v))_ℓ)` (y en la canónica, del multiset de las `M_ℓ`),
la relación "mismo color" se preserva ronda a ronda:
`P_{t+1}(𝓖) = P_{t+1}(ι(𝓖))`. ∎(paso)

*Conclusión.* Por inducción, `P_t(𝓖) = P_t(ι(𝓖))` para todo `t`; en
particular la partición estable coincide. ∎

**Corolarios** (partes de la operación uniforme):

1. **Permutación de capas** `π ∈ S_L`: el multiset por capa es
   `S_L`-invariante (canónica), y en la ordenada la permutación de
   coordenadas preserva la igualdad de tuplas; la partición se preserva
   en ambas variantes.
2. **Relabel** `σ ∈ S_n`: el refinamiento es isomorfismo-natural; la
   coloración se transporta biyectivamente.
3. **Composición** `σ ∘ π ∘ (complemento total)`: composición de
   preservaciones. ∎

*Observación fina.* El punto que hace funcionar la inducción es la
**uniformidad**: la misma biyección `M ↦ T − M` se aplica a **todas** las
capas. Si el complemento actuara sobre un subconjunto propio de capas,
la transformación del vector `(M_1..M_L)` dejaría de ser "la misma
biyección en cada coordenada" y la igualdad de multisets podría no
preservarse — que es exactamente lo que muestra la dirección (⇒).

## 2. (⇒) Abierta: no uniforme ⟹ existe testigo

> **Conjetura (contrapositiva).** Si `ι` complementa un subconjunto
> propio no vacío `S ⊂ {1..L}` (o mezcla capas de forma no uniforme),
> existe `𝓖` con `P(𝓖) ≠ P(ι(𝓖))`.

**Gadget mínimo (n=3, L=2, S={1}).** Capas `(E1, P3)` sobre `V={0,1,2}`:

- `E_1 = {(0,2)}` (una arista), `E_2 = {(0,2),(1,2)}` (P3).
- Grados por capa: `v0=(1,1)`, `v1=(0,1)`, `v2=(1,2)` → multisets
  `{1,1}`, `{0,1}`, `{1,2}` → **tres clases** en la ronda 0.
- Complemento de la capa 0 (no uniforme): `v1=(2,1) → {1,2}`,
  `v2=(1,2) → {1,2}` → **v1 y v2 se fusionan** → dos clases.
- Particiones distintas: `[['0'],['1'],['2']]` vs `[['0'],['1','2']]`.
  **Verificado en el motor.**

**Mecanismo.** El complemento no uniforme **cambia la coherencia entre
capas** de cada vértice: `v1` y `v2` tenían patrones de grado por capa
distintos, y el flip de una sola capa los volvió coherentes. La
observación canónica ve el **multiset** por capa, así que pierde la
distinción.

**Generalización conjeturada.** Para `S ⊂ {1..L}` propio no vacío,
elegir dos vértices `u, v` cuyos vectores de grados por capa `d_u, d_v`
tengan multiséts **distintos** pero **iguales tras el flip de `S`**
(`d_ℓ ↦ n−1−d_ℓ` si `ℓ ∈ S`), y realizar esos grados con las
adyacencias correctas en un grafo simple (gadget). El caso n=3 es el
testigo mínimo del mecanismo.

**Lo que falta para cerrar la (⇒)** (declarado, como la revisión externa
de T4):

1. Construcción explícita del gadget para **todo** `S` y **todo** `L`.
2. Mostrar que la fusión (o separación) inducida en la ronda 0
   **sobrevive al refinamiento** (no se repara en rondas posteriores).
3. El caso mixto (operaciones que no son ni complemento ni permutación
   de capas).

## 3. Estado y alcance

| pieza | estado |
|---|---|
| (⇐) uniforme ⟹ T4 | **probada** (esta página) |
| (⇒) no uniforme ⟹ testigo | gadget mínimo n=3 verificado; construcción general **abierta** |
| Evidencia empírica | total 1298/1298 + 1404/1404; por capa 6.9% + 7.4% (canónica) |
| Guardrail del motor | `refine_dual_multilayer` ofrece solo el dual **total** |

**Alcance**: grafos finitos simples multicapa, capas etiquetadas, sin
aristas cruzadas; refinamiento conjunto en las dos variantes declaradas;
`L ≤ 3`, `n ≤ 5` en la evidencia. La (⇒) ∀L y el caso mixto quedan
abiertos.

## 4. Por qué importa

1. Convierte la ley multicapa de **resultado de experimento** (§9.11) en
   **teorema parcial** con el patrón T4: una dirección probada, la otra
   con gadget y declarada abierta.
2. Hace la ley **prescriptiva con respaldo**: el motor no ofrece el dual
   por capa porque la (⇐) garantiza el total y el gadget + la evidencia
   muestran que el no uniforme rompe el invariante.
3. Deja la pregunta exacta para EXP-163: **¿cuál es el grupo de
   operaciones que preservan?** La respuesta conjeturada es "las
   uniformes" (`S_L` + complemento total + relabels); cerrarla exige la
   (⇒).
