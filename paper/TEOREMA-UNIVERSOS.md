# El teorema de universos — documento maestro

> Ciclo **EXP-099 → EXP-113** · laboratorio GraphKind · 2026-09-10
> Repo `cripto-bot/graphlang-natural` (privado) · todo reproducible.
>
> Este documento integra **todo** el ciclo: la historia, la matemática,
> las pruebas, las verificaciones, los errores cazados, el método y el
> estado exacto. Los detalles viven en `EXPERIMENTS/EXP-1xx/README.md` y
> en los `results_frozen.json` de cada experimento.

---

## 0. Resumen ejecutivo

**El resultado.** Con el perfil del color refinement (1-WL), para
involuciones del espacio de digrafos y compresiones de conteo `f`:

```
T4(ι, f) vive ⟺ ι ∈ Sₙ·K   y   (ι cambia el par ⟹ f(1) ≠ f(2))
K = {id, comp_dir, transp, comp_transp} ≅ Z₂×Z₂
```

- **(⇐) probada**: σ (relabel) y s (swap in/out) viven con toda `f`;
  c (complemento uniforme) vive ⟺ `f(1)≠f(2)` (mecanismo de conteos).
- **(⇒) verificada**: n≤4 exhaustivo (**96 = 24·4 exactas, cero fuera**),
  n=5 dirigido (6424/6424 con testigo válido), datos reales (moléculas
  100/100; CST 94/94).
- **Búsqueda autónoma** (113): la mejor construcción válida hallada por
  el motor es `ciclo` (**99.63%**, complejidad 1), mejor que la humana
  (C1 = 97.8%); **no hay receta universal 100%** en la familia probada.
- **∀n de (⇒): abierto.** Declarado, con el esqueleto verificado.

**La ley previa (102/105)**, que este ciclo refina:

```
T4 vive ⟺ f(1) ≠ f(2)          (universo estándar, involución dual global)
```

**La relatividad al WL** (109/110): "dual global" es propiedad del par
**(involución, WL)**, no de la involución: 76/1504 iotas cambian de
veredicto entre WL simétrico (in,out) y out-only.

---

## 1. Cronología (qué pasó, en orden)

| exp | qué se hizo | resultado |
|---|---|---|
| **099** | mapa de universos: estándar, F2, booleano, dirigido, tropical | T4 vive en 5/6 (muere en booleano) |
| **100** | mapa completo: + vértices/aristas tipados | T4 vive en 5/6 regiones |
| **101** | 24 universos generados automáticamente | hipótesis humana refutada |
| **102** | barrido del eje del conteo (17 `f` × 2 involuciones) | **ley: `f(1)≠f(2)` — 34/34** |
| **103** | explorador (DSL × banco de conjeturas) | regiones: Tperm/Tunion2 universales; T4 específica; frontera `k_c=2` |
| **104** | eje de involuciones (6 ops × 17 `f`) | **3 clases**: trivial / dual global / local |
| **105** | blindaje con definición formal + atlas | **ley 102/102**; 15 JSONs |
| **106** | bestiario de universos (6 criaturas) | ESPEJO/ECO/DESTELLO viven; SOMBRA/LEJANÍA/RELEVO mueren |
| **107** | la ley **en el motor** (`naturalkinds/universos.py`) | oráculo: predice T4 sin enumerar; **87/87** |
| **108** | grafos reales (moléculas + CST) | moléculas: dual+T4+oráculo; CST: son digrafos |
| **109** | digrafos con WL simétrico | `comp_dir`/`transp`/`comp_transp` 94/94 (f=id); **`transp` es dual universal** (vive con const1) |
| **110** | **la disyunción puesta a prueba** | M1 y M2 **no suficientes**; falsaciones en ambas direcciones; relatividad al WL 76/1504 |
| **111** | caracterización Sₙ·K: prueba + verificación | n=4: **96 exactas, 0 fuera**; n=5 dirigido: 7680 testigos |
| **112** | el testigo: minería de la construcción | 6424/6424 con testigo; formas variadas |
| **113** | **búsqueda autónoma** + corrección | mejor válida: `ciclo` 99.63%; control cazó un artefacto |

---

## 2. La matemática

### 2.1 Definiciones

- **Digrafo** `G=(V,E)`: `adj[v]` = bitmask de vecinos salientes; `n=|V|`.
- **WL simétrico** (el del teorema): coloración inicial por grados
  **crudos** `(out, in)`; actualización
  `color'(v) = H(color(v) | {(color(u), f(in_c), f(out_c))})` por clase
  `c`; se itera `n+2` rondas. **Perfil** `I(G)` = multiset de tamaños de
  clase.
- **T4(ι, f)**: `I(G) = I(ι(G))` para todo digrafo `G` (n fijo).
- **Involución**: `ι² = id` (el complemento es el caso canónico).
- **Par**: el conjunto no dirigido `{u,v}`; "cambiar el par" = existe un
  par cuya presencia (`A_uv ∨ A_vu`) cambia.
- **Uniformidad**: `ι` actúa igual sobre todos los pares (la pieza que
  une las dos mitades).
- **K (Klein)**: `{id, comp_dir, transp, comp_transp}` ≅ Z₂×Z₂, donde
  `comp_dir` = complemento dirigido, `transp` = `Aᵀ`.

### 2.2 La ley del conteo (EXP-102, blindada en 105)

> En el universo estándar con involución que cambia el par:
> **T4 vive ⟺ f(1) ≠ f(2).**

**Mecanismo**: en el complemento, un vértice con **1** vecino de una
clase pasa a tener `|c|−1` (que puede ser **2**): si `f` colapsa 1 y 2,
la dualidad muere. Lo que `f` haga con 3, 4, 5… es irrelevante: solo
importa la distinción mínima. Verificado 34/34 (barrido) y 102/102
(blindaje con definición formal); contraejemplo mínimo en n=6.

### 2.3 La disyunción y su refutación (EXP-110)

Hipótesis humana puesta a prueba:

```
T4 vive ⟺ M1 ∨ M2
M1: preserva el par;  M2: cambia el par ∧ f(1)≠f(2)
```

Los datos la **falsaron en ambas direcciones**:

1. **M1 no es suficiente**: `flip_inc0` (invertir solo los arcos
   incidentes al vértice 0) preserva el par y **muere 0/24** con toda
   `f`: hay que preservarlo **uniformemente**.
2. **M2 no es suficiente**: con `f=id` (f(1)≠f(2)) mueren **1364/1504**
   iotas afines que cambian el par de forma **no uniforme**.
3. Los `TERCER_CAMINO` aparentes (n=3) eran **rango**: en los CST reales
   `comp_dir+const1` muere **0/94**.

La pieza que faltaba es la **uniformidad (coherencia global)**.

### 2.4 La caracterización Sₙ·K (EXP-111)

En el espacio de iotas inducidas (σ∈Sₙ, swap s, complementación c por
par, c σ-invariante) y con WL simétrico:

| cámara | resultado |
|---|---|
| n=4 exhaustivo (528 iotas × 4096 grafos) | viven **96** (f=id) y **48** (const1), **todas uniformes, 0 fuera** |
| n=5 dirigido (8160 iotas) | **7680 con testigo**; 480 sin testigo = uniformes (104 involuciones válidas + 376 relabels no involutivos) |
| fuera del espacio (afín aleatoria n=4) | **10000/10000 con testigo** |

### 2.5 La prueba de (⇐)

Sea `ι = σ∘s∘c`:

1. **σ (relabel)**: el WL es invariante por isomorfismo: la partición se
   transporta biyectivamente. Vale con toda `f`.
2. **s (swap in/out)**: `(in_D,out_D) → (out_D,in_D)` y el perfil por el
   swap `(f(a),f(b))→(f(b),f(a))`: biyección de perfiles. Vale con toda `f`.
3. **c (complemento uniforme)**: los conteos van `m → |D|−m` (o
   `|D|−1−m`): biyección de conteos; la partición se preserva **siempre
   que `f` distinga 1 de 2** (contraejemplo con `f(1)=f(2)`: n=6,
   EXP-102). ∎ *(la suficiencia de `f(1)≠f(2)` para `f` arbitraria está
   verificada en 102/102 + 87/87 + 94/94 + 528/528; la prueba general
   para `f` arbitraria queda como trabajo externo).*

### 2.6 La verificación de (⇒)

- **n≤4 exhaustivo** (111-B): viven exactamente 96 (f=id) y 48
  (const1); **cero** no uniformes.
- **n=5 dirigido** (111-C): 7680/8160 con testigo; las 480 sin testigo
  son uniformes.
- **Real** (108/109): moléculas 100/100 (dual + T4); CST 94/94
  (`comp_dir` dual + T4 dirigido).
- **Existencia de testigo por iota** (112): 6424/6424 no-uniformes con
  testigo válido en n≤5.

### 2.7 El testigo y la búsqueda autónoma (EXP-112/113)

- El motor minó testigos mínimos (6424/6424) y midió construcciones
  candidatas.
- **EXP-113** (búsqueda autónoma): lenguaje de 11 primitivos + 3
  combinadores (~400 recetas), criterio **tasa / MDL** (tasa − 0.005·comp).
- **Mejor testigo válido**: `ciclo` (ciclo dirigido `0→1→…→n−1→0`),
  **99.63%**, complejidad 1 — mejor que la construcción humana C1
  (97.8%). **Ninguna construcción válida llega al 100%.**
- **Corrección por control negativo**: las recetas con aislado
  (`vacio+aisl1`, `c1+aisl1`) daban 100% pero usaban la **iota extendida**
  a n+k (otra operación): el control de uniformes falló 52/104 (deben
  ser 0 por (⇐)) y delató el artefacto. Retirado como "prueba"; queda
  como testigo de la extensión (otra iota, otro teorema).

### 2.8 Relatividad al WL (EXP-109/110)

- `transp`: **dual con WL simétrico** (vive con toda `f`), **local con
  WL out-only** (el del módulo): **76/1504** iotas cambian de veredicto.
- El esquema correcto es **(universo, WL, involución, f) → resultado**,
  no (universo, involución) → resultado.

---

## 3. El método (por qué esto es creíble)

### 3.1 Principio de descubrimiento

La **sintaxis se declara; la semántica emerge**. El motor descubre
estructura que está ahí, independiente de la literatura; el estatus
"descubrimiento vs redescubrimiento" se decide **contra la literatura,
con verificación**, nunca por suposición.

### 3.2 Controles negativos (los que cazaron errores reales)

| error | cómo se cazó |
|---|---|
| firma del WL sin color | control de isomorfismo (C6 vs 2·C3) |
| rondas variables en el WL | lema por ronda |
| matching greedy en el complemento | identidad 12/12 con σ-inducido |
| `m` sin `σ(v)` | re-verificación |
| grado doble `_out+_in` | test dirigido |
| orden lexicográfico `n2` vs `n10` | atlas |
| `wl_dir` aplicaba `f` al grado inicial | control de no-trivialidad |
| **ciclo k=1 = self-loop en el testigo** | la identidad "fallaba" |
| **recetas con aislado = iota extendida** | **control de uniformes 52/104** |

Sin el último control, el paper habría reportado una prueba falsa.

### 3.3 Atribución precisa (sin hype)

- **Del motor**: la ley (102), la falsación de las hipótesis humanas
  (101/104/110), la clasificación (111), los testigos (112), la mejor
  receta de la familia (113: `ciclo`).
- **Humano**: la redacción de la prueba (⇐), la definición del lenguaje
  de primitivos, la interpretación, y la **corrección** del artefacto de
  extensión.
- **Nombre preciso del avance**: *búsqueda autónoma de construcciones en
  un lenguaje dado* (el motor optimiza recetas y superó la humana). **No**
  es "el motor prueba teoremas".

### 3.4 Freeze y re-auditoría

Cada experimento congela `results_frozen.json` antes de interpretar;
las re-auditorías (077) tumbaron señales previas (052). Los errores se
documentan en los READMEs, no se borran.

---

## 4. Estado y trabajo abierto (declarado)

1. **(⇒) ∀n**: abierto. Verificado n≤4 exhaustivo + n=5 dirigido +
   real; receta universal 100% **no hallada** (mejor: `ciclo` 99.63%).
2. **(⇐) para `f` arbitraria con `f(1)≠f(2)`**: verificado en los
   catálogos; prueba general abierta.
3. **Espacio afín completo n≥5**: inabordable (involuciones de S₂₀);
   el espacio probado es el inducido + afín aleatorio (10k, todos con
   testigo).
4. **Formalización asistida** (Lean): no disponible en el entorno.
5. **Revisión externa**: pendiente (T4 y la caracterización).

---

## 5. Archivos y reproducción

| experimento | qué contiene | comando |
|---|---|---|
| `EXP-099/100` | mapas de universos | `python run.py` |
| `EXP-102` | la ley `f(1)≠f(2)` (34/34) | `python run.py` |
| `EXP-105` | blindaje 102/102 + `atlas/*.json` | `python run.py` |
| `EXP-107` | `naturalkinds/universos.py` + oráculo 87/87 | `python run.py` |
| `EXP-108/109` | real: moléculas + CST | `python run.py` |
| `EXP-110` | disyunción (falsaciones) | `python run.py` |
| `EXP-111` | caracterización + `PRUEBA-CARACTERIZACION.md` | `python run.py` |
| `EXP-112` | testigos mínimos + `fase2_construcciones.py` | `python run.py` |
| `EXP-113` | búsqueda autónoma + **corrección** (`fase3_validas.py`) | `python run.py` |

**Documentos relacionados**: `PAPER.md` (paper académico),
`PRUEBA-CARACTERIZACION.md` (EXP-111), `ALGORITMO-UNIVERSOS.md`
(el algoritmo), `DOCUMENTAL-UNIVERSOS.md` (la narración),
`naturalkinds/universos.py` (la ley en el motor).

**Regla de hardware**: Pool(22), CPU verificada 1200–2200%; `SEED=7`.
