# DECISION_LOG — decisiones técnicas del laboratorio

> Formato: D-NNN · fecha · decisión · por qué · evidencia · alcance.

## D-001 · 2026-09-12 · Fix del parser SMILES (`naturalkinds/ingest.py`)

- **Decisión**: `if ch in "ClBr"` → `if (ch + smiles[i]) in ("Cl", "Br")`.
- **Por qué**: la condición era True para `'C'` y `'B'` solos, así que
  `Cc1ccccc1` (tolueno) se parseaba como el elemento inexistente `"Cc"` y
  se perdía un átomo del anillo; lo mismo con `Cn`, `Co`, `Cs`... de forma
  **silenciosa** (no lanzaba error).
- **Evidencia**: 5000 moléculas únicas del SDF GEOM 5confs contra RDKit:
  parser viejo mal **1089 (21.8%)**; parser nuevo **0 (0.0%)**. Tests de
  regresión: `Cc1ccccc1`=7 nodos, `CCc1ccccc1`=8, `N1CCN(Cc2ccccc2)CC1`=13,
  `ClC`/`BrC` siguen de dos letras. Suite 34/34 OK.
- **Alcance**: motor raíz y experimentos futuros. Los resultados congelados
  141-152 usaron el subconjunto que parseaba consistente (p. ej. 759/1000
  en el test ciego); siguen válidos como históricos con **sesgo declarado**
  (se descartaban las moléculas con el patrón). Re-correr el arco con el
  parser corregido queda como opción, no como obligación.
- **Detección**: VERIFY GATE de EXP-154 (Fase 7.2): el run devolvió 0
  grafos y el chequeo de conteo de átomos reveló el bug.

## D-002 · 2026-09-12 · Cierre de la línea interventional (EXP-155/156)

- **Decisión**: cerrar la línea "acoplamiento interventional" como
  **resultado parcial**: mecanismo descubierto (32-33 relaciones X→Y en
  TRAIN, snr 5-27) pero **transferencia OOD no lograda**.
- **Evidencia**: EXP-155 (cobertura 0.5%, ganancia +0.035°); EXP-156 causal
  de 4 brazos: hash vs estructura B−A +0.000, granularidad C−A +0.001,
  ambos D−A +0.001; ninguna condición supera el criterio operativo
  (cobertura >5%, ganancia >20%).
- **Hallazgo lateral**: el gate de representación mostró 33 colapsos del
  hash (pérdida de `initial_labels`, que descarta la composición de aristas
  en la etiqueta base), pero su efecto en transferencia es nulo.
- **Causa**: los contextos de kinds no reaparecen en scaffolds OOD ni en la
  granularidad más gruesa elegida por el motor.
- **Alcance**: no se sigue ajustando la representación; el próximo eje es
  restricciones geométricas / proteína-PDB (o volver a papers), según el
  roadmap de la spec.

## D-003 · 2026-09-12 · Umbrales emergentes (EXP-157) y cierre de iteraciones

- **Decisión**: los umbrales `MIN_N` y `BINS` se mueven al mecanismo de
  emergencia (CV+1-SE en TRAIN, como r*), no a barridos. Tras EXP-157 **no
  hay más iteraciones de ajuste**: sigue escribir papers.
- **Evidencia**: interventional eligió MIN_N=10 (CV +0.0539 vs +0.0288 en
  30) y mejoró OOD marginalmente (0.98%/+0.79% vs 0.53%/+0.50%);
  conformacional eligió (10, 20°) y mejoró OOD (1.060 Å/21.8% vs
  1.136 Å/19.9% del heredado 30/10°).
- **Conclusión**: `MIN_N=30`/`BINS=10°` eran convención, no óptimos. La
  línea interventional cierra con tres explicaciones eliminadas
  (granularidad, hash, umbrales).
- **Alcance**: los grids de candidatos son humanos (declarado); la elección
  es del motor. `Z`, `n_boot`, `semilla` quedan como prioris estadísticas
  (no se calibran por emergencia).

## D-004 · 2026-09-12 · Calibración emergente probada (3 controles)

- **Decisión**: la calibración emergente de EXP-157 queda **probada** y va
  al paper con evidencia completa.
- **Evidencia**: (1) bootstrap pareado ΔRMSD IC95 [−0.130, −0.019] no cruza
  cero; (2) el motor elige (10, 20°) en **4/4 splits** y mejora en 4/4;
  (3) (10,20°) es el mejor OOD del grid medido (control, no selección).
- **Alcance**: `MIN_N=30`/`BINS=10°` quedan documentados como convención
  subóptima; los valores emergentes (10, 20°) son los reportados.


## D-005 · 2026-09-12 · Naming k-WL/k-FWL corregido (EXP-159)

- **Decisión**: la variante de EXP-118/119 es k-FWL (correlacionada, ≡
  (k+1)-WL); el "3-WL separa Rook/Shrikhande" de 119 §8 es 3-FWL ≡ 4-WL.
  Corregido en el README de EXP-119.
- **Evidencia**: `naturalkinds/kwl.py` implementado desde cero + verificado
  contra 118/119: `kwl(3)` NO separa Rook/Shrikhande; `kfwl(3)` SÍ.
  T4_k universal (207/207) en las 5 variantes; `kwl(1)=kwl(2)` en el atlas.
- **Alcance**: la jerarquía conocida se reporta como **redescubrimiento**;
  EXP-159 cierra y se pasa a papers (no más iteraciones).


## D-006 · 2026-09-12 · Ruptura empírica en tw=3 (EXP-160)

- **Decisión**: se reporta como **hallazgo experimental** (no teorema) que
  en el espacio declarado (bases lineales por tw + productos de a dos) las
  relaciones para `hom(H,Ḡ)` transfieren OOD para **tw≤2** y **no existen**
  para **tw≥3** (6/6 refutados, K5 incluido).
- **Evidencia**: `EXPERIMENTS/EXP-160-.../results_frozen.json`; sin
  fórmula programada; R² TEST 0.2–0.7 (leyes parciales); consistente con
  EXP-092/093 (no hay base triangular simple).
- **Alcance**: H≤5, corpus n≤8; la conexión hom/treewidth/k-WL es teoría
  conocida (post-freeze, redescubrimiento parcial); el punto de ruptura
  empírico es el aporte.


## D-007 · 2026-09-13 · SNF del Laplaciano separa Rook/Shrikhande (EXP-161)

- **Decisión**: se registra como hallazgo del barrido algebraico que el
  **SNF del Laplaciano/signless** distingue el par SRG **cospectral**
  Rook 4×4 vs Shrikhande, donde espectros de A/L/Q, Seidel, SNF(A),
  SNF(A+I), det/rango y |Aut| fallan. Ningún invariante algebraico del
  barrido es complemento-invariante exacto.
- **Evidencia**: `EXPERIMENTS/EXP-161-.../results_frozen.json` (pares
  conocidos); sanity espectral 25/25 en regulares (EXP-090).
- **Alcance**: n≤8; comparación bibliográfica pendiente (redescubrimiento
  si aplica). Anticipo directo del programa SG-01 (invariantes completos).

## D-008 · 2026-09-13 · IR canónico: marcador sin id + firma completa (SG-02)

- **Decisión**: `IR_k` usa (a) marcador canónico `IND` —sin el id del
  vértice— y (b) la **firma completa** del refinamiento (multiset de
  colores), no el perfil de tamaños de clase. Ambas fugas fueron cazadas
  por los tests antes del freeze.
- **Evidencia**: con el marcador `ind:{nid}` el control de relabeling
  falla (fuga de etiquetado); con el perfil, i* daba "+" para 13 595/13 597
  y el complemento "identificaba" 12 346/12 346 (imposible). Con la
  corrección: i* = 1 en n≤8 (13 597), frontera Rook/Shrikhande i* = 2
  (IR_1 no, IR_2 sí), complemento 10/12 346 → cociente 6 168 (igual que
  SG-01).
- **Alcance**: los tests usaban un multigrafo (aristas duplicadas en la
  construcción manual): se corrigió a grafos simples. La corrección
  cambió el resultado (i* de artefacto a 1/2) — se registra, no se borra.

## D-009 · 2026-09-13 · SG-03: IR1p sigue a 3-WL y IR2p a 3-FWL/4-WL; n=10 no alcanzado

- **Resultado**: con las definiciones fijadas antes de correr (IR_k-peor
  primario: soporte de tipos puntados sin multiplicidades; simultánea),
  en la clase n≤9 (274 668) todos los primitivos completos inducen la
  misma partición (discreta): la equivalencia en la clase es **vacua**.
  WL = KW2 (3 900 pares fusionados, 271 941 clases: KW2 no agrega poder).
  La evidencia discriminante son las anclas: IR1p falla donde 3-WL falla
  (Rook/Shrikhande) y separa donde 3-WL separa (C6/2C3); IR2p separa
  Rook/Shri como 3-FWL ≡ 4-WL (KF3), y **KF2 no** (a n=16 kfwl(2) y
  kfwl(3) difieren: el atlas los igualaba).
- **Evidencia**: `EXPERIMENTS/SG-03-01-ir-vs-kwl/results_frozen.json`
  (retículo, anclas, n_min, piloto); relabeling 30/30.
- **Alcance**: n≤9 + anclas; n=10 no alcanzado (piloto 36.9 h > 12 h
  declaradas); C (incomparables) no observado; peor vs multiset sin
  divergencia observada. La frontera exacta queda abierta.

## D-010 · 2026-09-13 · Multicapa: la coherencia de canales (EXP-162)

- **Resultado**: en el universo multicapa (refinamiento conjunto), T4
  vive con el complemento **total** y muere con el **por capa** (6.9%
  L=2, 7.4% L=3) — **solo en la variante canónica** (canales como
  conjunto); la ordenada es el control. La ley: el complemento debe
  actuar uniformemente sobre las capas. Las permutaciones de canales
  preservan en ambas variantes (la partición es ciega al orden: H3
  corregida). El acoplamiento sube k* de 1 (single) a 2 (multicapa).
- **Evidencia**: `EXPERIMENTS/EXP-162-.../results_frozen.json` (1 298 y
  1 404 objetos; cascada 674 976 pares; testigos n=3/n=4).
- **Alcance**: L≤3, n≤5/4; capas etiquetadas; definiciones propias;
  empírico en la clase.

## D-011 · 2026-09-13 · El grupo preservante es relativo a la observación (EXP-163)

- **Resultado**: en el espacio `Z₂^L ⋊ S_L`, el conjunto que preserva T4
  es **exactamente el subgrupo uniforme U** (`∅` o todas las capas +
  `S_L`) en la variante canónica (L=2: 4/4; L=3: 12/12; cierre
  verificado); en la **ordenada** preserva **todo el grupo** (8/8 y
  48/48). El grupo es **relativo a la observación** (análogo multicapa
  de la relatividad al WL, EXP-109/110).
- **Evidencia**: `EXPERIMENTS/EXP-163-.../results_frozen.json`.
- **Alcance**: L≤3, n≤5/4; la (⇒) ∀L sigue abierta
  (`PRUEBA-MULTICAPA.md`); empírico en la clase.

## D-012 · 2026-09-13 · La escalera k\*(L) es plana; corrección del k\*=2 de EXP-162 (EXP-164)

- **Resultado**: con `k=1` = refinamiento conjunto (corregido) y `k≥2` =
  k-FWL conjunta, `k*=1` para L=2..5 en dos corpus (representantes n≤4:
  123/1 349/14 751/161 621 clases; etiquetas completas n≤3: 20/120/816/
  5 984). Escalera **plana**: si hay umbral, `k₀ ≥ 5`.
- **Corrección**: EXP-162 reportó `k*=2` con `kwl_conjunto(k=1)`
  degenerado (solo colores iniciales, sin actualización). Con el k=1
  corregido —el mismo criterio que el motor single-layer— el
  acoplamiento no sube k\*. Se registra (patrón D-008).
- **Evidencia**: `EXPERIMENTS/EXP-164-.../results_frozen.json` +
  `verificacion_corpus.py`.
- **Alcance**: n≤4/3, L≤5, techo `k* ≤ n`; la (⇒) ∀L de
  `PRUEBA-MULTICAPA.md` sigue abierta.

## D-013 · 2026-09-13 · La frontera es de la pareja; pesa el observador (EXP-165)

- **Resultado**: en la matriz universo × observador (dos métricas: T4 y
  frontera), la frontera **se mueve con el observador** (WL/KW2 fallan en
  n=6; KW3/IR1p completos en n≤6) y **no se mueve con el tipado** (fila
  tipado = fila estándar en `n_min`). T4 vive en tipado 4 784/4 784.
- **Celdas N/A declaradas**: completitud de dirigido/Z₃/R1 (maquinaria
  del observador dinámico fuera del motor) — no se inventan.
- **Evidencia**: `EXPERIMENTS/EXP-165-.../results_frozen.json` + freezes
  citados (SG-03, EXP-109/116/117/162/164).
- **Alcance**: tipado n≤6, 2 kinds; `n_min` acotado por corpus.

## D-014 · 2026-09-13 · El mapa es predictivo en universos no visitados (EXP-166)

- **Predicción registrada antes de medir**: T4 vive en hipergrafos
  3-uniformes (complemento dual global: resta de multiséts con total
  fijo `T_v` sobre el link, inyectiva por clase).
- **Medición**: T4 viva **1831/1831** (n=3: 2/2; n=4: 5/5; n=5: 34/34;
  n=6 muestra: 1790/1790). **A: la predicción acierta.**
- **Frontera**: 1-WL de hipergrafos, `n_min = 6` (60 colisiones en la
  muestra n=6) — coincide con la de grafos (EXP-165).
- **Evidencia**: `EXPERIMENTS/EXP-166-.../results_frozen.json`.
- **Alcance**: n≤6 (n=6 por muestra), 3-uniformes; k≥2/IR de hipergrafos
  N/A; (⇒) multicapa abierta.

## D-015 · 2026-09-13 · El transplante de la ley de canales falla (EXP-167)

- **Escalera de aridad**: T4 vive en k=4 (156/156) y k=5 (7/7); frontera
  1-WL n=6 (4 colisiones en k=4) — "lo vasto se siente estándar".
- **Mezclado (2+3)**: total vive 100%; **por aridad también vive
  1038/1038** en ambas variantes — la predicción de canales (por aridad
  muere en la canónica) **falla**.
- **Hipótesis mecanística**: la diferencia es la estructura del mensaje
  (en multicapa todas las capas comparten tipo; en mezclado los mensajes
  por aridad tienen tipos distintos y el refinamiento repara la colisión
  inicial de grados). Testigo dirigido en n≥6 pendiente.
- **Ley afinada**: "uniformidad" es **suficiente**; como necesaria
  depende del tipo de mensaje — la ley es **de canales**, no de toda
  descomposición.
- **Evidencia**: `EXPERIMENTS/EXP-167-.../results_frozen.json`.
- **Alcance**: k≤5, aridades {2,3}, n≤6; empírico.

## D-016 · 2026-09-13 · Reparo robusto en aridades mezcladas (EXP-168)

- **Resultado (B)**: búsqueda dirigida (construcción canónica) +
  muestras amplias en n=6,7,8: **261 000 casos, 21 821 fusiones
  dirigidas en ronda 0, todas reparadas, 0 testigos** (T4 nunca falló).
  Controles negativo (sin fusión: 0 fallas) y total (uniforme: 100%
  vive) limpios.
- **Consecuencia**: la conjetura D-015 se fortalece; el **guardrail**
  para hipergrafos mezclados puede **permitir** el dual por aridad
  (ahorro de hiperaristas) — la asimilación como capacidad queda como
  decisión pendiente declarada. En multicapa el por-capa sigue
  prohibido.
- **Evidencia**: `EXPERIMENTS/EXP-168-.../results_frozen.json`.
- **Alcance**: n≤8, aridades {2,3}, muestras (no exhaustivo); empírico;
  la (⇒) multicapa sigue abierta.

## D-017 · 2026-09-13 · El dual por aridad entra al motor (EXP-169)

- **Capacidad asimilada**: `refine_dual_mezclado` (hipergrafos
  mezclados) elige el lado ralo **por aridad** y devuelve la partición
  con garantía empírica (EXP-168). Validación: 60 000 casos, **partición
  100%**, ahorro **14.37%** vs 10.26% del dual total (**+4.11% extra**).
- **Guardrail**: el dual por aridad **se ofrece** en mezclados; el dual
  por capa de multicapa sigue **prohibido** (rompe). La diferencia es el
  tipo de mensaje (EXP-167/168).
- **Evidencia**: `EXPERIMENTS/EXP-169-.../results_frozen.json` + tests
  104/104.
- **Alcance**: n≤8, aridades {2,3}, garantía empírica (no ∀n).
