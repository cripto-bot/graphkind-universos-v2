# Resultados: puesta a prueba de Sₙ·K + f(1)≠f(2) (2026-10-25)

Protocolo `paper/LIMITES-DIGRAFOS-SPEC.md` (sha256 `54ad76d6…`). Motor: `codigo/wl.py` +
`codigo/universos.py` + `wl_partition` (particiones, no perfiles).
145 f (catálogo de 17 + 64 aleatorias con f(1)≠f(2) + 64 con f(1)=f(2)).
Wall **73,7 s** · CPU **1.947%** · `Pool(22)`.

## A. No dirigidos: la ley del complemento se sostiene

Todos los grafos n=2..6 (33.866), involución `comp`.

| caso | resultado |
|---|---|
| f(1)≠f(2) | **75/75 con 0 fallas** |
| f(1)=f(2) | **70/70 con testigo** (el primero: n=6, mask 657) |

La ley `T4(comp,f) ⇔ f(1)≠f(2)` queda **soportada** en este espacio, con f
aleatorias y colisiones libres en 0,3,4,5,6.

## B. Digrafos: contraejemplo a la cláusula f(1)≠f(2)

n=4 (4.096 digrafos), K={id, comp_dir, transp, comp_transp}.

| iota | resultado |
|---|---|
| id | 145/145 con 0 fallas |
| transp | 145/145 con 0 fallas |
| comp_dir / comp_transp, f(1)=f(2) | 30/140 con testigo en n=4; 110 sin testigo en n=4 (no es contraejemplo: puede necesitar n≥5) |
| comp_dir / comp_transp, f(1)≠f(2) | **46/150 con fallas** |

**Contraejemplo concreto** (`umbral2`, f=(0,0,1,1,1,1,1), f(1)=0≠f(2)=1,
`comp_dir`, n=4, mask 21):

```
adj:      0->{1,3}, 1->{2}, 2->{}, 3->{}
comp_dir: 0->{2},   1->{0,3}, 2->{0,1,3}, 3->{0,1,2}

partición G    = [[0],[1],[2],[3]]        perfil (1,1,1,1)
partición comp = [[0],[1],[2,3]]          perfil (1,1,2)
```

El motor confirma la diferencia; no es un artefacto de perfiles.
**Causa**: en digrafos el conteo es un par (in,out); `umbral2` colapsa
`f(0)=f(1)=0`, y esa colisión (no la de 1 vs 2) rompe la dualidad. La
condición `f(1)≠f(2)` es **necesaria pero no suficiente** para digrafos.
El paper solo testeó la ley con las 17 f en **no dirigidos** (V1) y en
digrafos usó f=id/const1 (V2); el hueco es real.

## C. Controles no uniformes

| control | testigo |
|---|---|
| comp_parcial | n=4, mask 0 |
| flip_inc0 | n=3, mask 0 |
| subconjuntos propios S (30) | 27/32 con testigo (n=5/6) |

Los 5 “supervivientes” son los **singletons** (S={v}): no hay aristas dentro
de S, así que la iota es la **identidad** (trivial, en Sₙ·K); sobreviven por
derecho. No son contraejemplos. Todo control no trivial falla.

## D. Gap de API

`clasificar_involucion` es **out-only**; en el digrafo 0->1->2->3 con
`transp` devuelve `"local"`, cuando el teorema (WL simétrico) dice
`"trivial"`. El test B usa la clase del teorema, no la del clasificador.
El oráculo `oraculo(...)` heredaría ese error en digrafos; hay que darle
una variante simétrica (o arreglar `wl_labels` para usar in/out).

## Lectura

- **No** se confirma la conjetura en su forma actual: la cláusula
  `f(1)≠f(2)` **falla para digrafos** con f arbitraria. El contraejemplo es
  `umbral2` (f(0)=f(1), f(1)≠f(2)).
- **Sí** se sostiene la ley del **complemento no dirigido** (75/75 y
  70/70) y la parte de grupo (`id`/`transp` 290/290).
- La caracterización necesita una **cláusula de digrafos**: la compresión
  f debe ser inyectiva en los pares de conteos relevantes (al menos
  f(0)≠f(1) y f(1)≠f(2); posiblemente más). Eso es una conjetura nueva,
  no un teorema; hay que buscarla y probarla.
- La novedad de Sₙ·K sigue siendo una cuestión de **lectura**
  (Kiefer–de Mel; flip lemma KSS), no de este test. Este test solo dice
  qué predicciones fallan.

## Instancia en datos reales (openai/math)

El grafo de **composición de kinds** de la gramática Lean de OpenAI
(top60 de `lean_ir_merge.json`) realiza el contraejemplo: con `umbral2`
(`f(0)=f(1)=0`, `f(2)=1`), `comp_dir`/`comp_transp` **fallan**; en
Mathlib viven. Además, los roles WL de kinds difieren (OpenAI 11 vs
Mathlib 10; ARI sobre los 13 kinds comunes **−0,04**). `transp` vive con
toda f en ambas gramáticas: la dirección de composición es invisible a
la partición WL. Ver
`graphkind-harness/showcases/openai-math-radar/universos-openai/{gramatica_universos.py,GRAMATICA-UNIVERSOS.md,gramatica_universos.json}`.
Es una **instancia** del límite de digrafos, no un teorema sobre todo el
corpus (top60, 13 kinds).

## Límites

- A: n≤6 no dirigidos; B: n=4 digrafos (los 110 sin testigo no son
  contraejemplos; la búsqueda n≥5 queda pendiente); C: subconjuntos n≤6.
- No prueba (⇒) ∀n ni la suficiencia para f arbitraria; encuentra
  contraejemplos y soporte finito.
- La generalización cross-domain no se toca acá.

## Próximo

1. Extender B a n=5 (muestra o all) para los 110 sin testigo y para
   `mod2`/`mod3` (colisiones 0/2, 0/3) y ver si la condición es
   f inyectiva en 0/1/2 o en todos los conteos.
2. Arreglar `clasificar_involucion` a WL simétrico (in/out).
3. Si aparece una condición de digrafos estable, pre-registrarla y
   testearla; si no, reportar la ley solo para no dirigidos.


## Reproducción

```bash
python3 codigo/conjetura_snk.py
```

El script lee `paper/LIMITES-DIGRAFOS-SPEC.md`, usa `codigo/` (WL, universos,
`wl_partition`) y escribe `resultados/CONJETURA-SNK_results_frozen.json`.
