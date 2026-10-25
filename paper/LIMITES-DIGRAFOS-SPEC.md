# Puesta a prueba de la conjetura Sₙ·K + f(1)≠f(2) (pre-registro)

> Escrito ANTES de correr. Fecha: 2026-10-25. **No** se declara novedad:
> la novedad se verifica leyendo la literatura; esto solo testea las
> predicciones computacionales de la conjetura y busca contraejemplos.

## Conjetura

Para WL simétrico (in/out por color) con compresión de conteos `f` e
involución `ι`:

    T4(ι, f)  ⟺  ι ∈ Sₙ·K  y  (c=1 ⟹ f(1) ≠ f(2))

con `K = {id, comp_dir, transp, comp_transp} ≅ Z₂×Z₂` y `ι = σ∘s∘c`
(σ relabel, s swap global in/out, c complemento uniforme). `T4` significa
`CR₁(G) = CR₁(ι(G))` como **particiones** de V, para todo G.

## Diseño

- Motor: `codigo/wl.py` (`wl_partition` de `verificaciones_particiones.py`,
  WL simétrico con f, particiones, no perfiles), `codigo/universos.py`
  (`t4_garantizado`).
- f: **tablas aleatorias** `f: {0..6}→{0,1,2,3}` (no solo el catálogo de
  17), 64 con `f(1)≠f(2)` y 64 con `f(1)=f(2)`, más el catálogo de 17.
  Las colisiones en 0,3,4,5,6 son libres: la conjetura dice que no importan.
- A (no dirigidos): `comp` (dual), todos los grafos n=2..6 (33.866);
  comparación de particiones.
- B (digrafos): n=4 (4.096), las 4 involuciones de K, 32 f aleatorias con
  `f(1)≠f(2)`, 32 con `f(1)=f(2)`, más catálogo. Predicción: `id` y
  `transp` viven con toda f; `comp_dir` y `comp_transp` viven ⟺ f(1)≠f(2).
- C (controles no uniformes): `comp_parcial` (S=range(n//2)), `flip_inc0`
  (toggle de aristas incidentes a 0), y 30 subconjuntos propios de vértices
  para n=5 (complemento dentro de S); buscar testigo n≤6. Predicción:
  todos fallan en algún grafo (la uniformidad es necesaria).
- 5 seeds para las f aleatorias; doble corrida con hash del JSON.

## Hipótesis y falsación

- **H1 (ley, A).** Para `comp`: f(1)≠f(2) → 0 fallas en n≤6; f(1)=f(2) →
  ≥1 falla (testigo, esperado n=6). **Falsación**: una f con f(1)≠f(2) que
  falle (contraejemplo a la conjetura) o una f con f(1)=f(2) que no falle
  (contraejemplo a la ley).
- **H2 (K, B).** `id`/`transp`: 0 fallas con toda f; `comp_dir`/
  `comp_transp`: 0 fallas ⟺ f(1)≠f(2). **Falsación**: cualquier mismatch
  entre la predicción del oráculo y la partición real.
- **H3 (necesidad de uniformidad, C).** Cada control no uniforme tiene un
  testigo en n≤6. Un “superviviente” n≤6 no es contraejemplo a ∀n, pero se
  reporta: debilita la necesidad de uniformidad y pide testigos mayores.
- **H4 (oráculo).** `t4_garantizado(f1,f2,clase)` coincide con la partición
  real en todos los casos A/B. **Falsación**: cualquier mismatch.
- **Sanity**: f=id, comp → T4 vive; f=const1, comp → falla en n=6;
  `wl_partition` (perfil) == `wl_sym` para grafos aleatorios con f=id.

## Alcance

Esto es evidencia computacional sobre espacios finitos (n≤6 y n=4
digrafos). No prueba (⇒) ∀n ni la suficiencia de f(1)≠f(2) para f
arbitraria; esos siguen abiertos. La novedad de la caracterización es una
cuestión de lectura (Kiefer–de Mel Lemma 4.5; flip lemma de
Kiefer–Schweitzer–Selman), no de este experimento. Si no hay contraejemplos,
la conjetura queda **soportada**, no demostrada.
