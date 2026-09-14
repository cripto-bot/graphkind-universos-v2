# GraphKind: descubrimiento estructural autónomo y leyes emergentes en universos de observación

> **Borrador académico (v2)** · laboratorio GraphKind · 2026-09-13
> Repo: `cripto-bot/graphlang-natural` (privado) · todo reproducible.

**Autores**: [Juri] · con el motor GraphKind como instrumento.
**Código y datos**: repositorio completo (v2: T4 + arco de universos;
laboratorio: 169 EXP + SG-01/02/03, tags v0.1.0–v0.7.1).

---

## Abstract

Presentamos **GraphKind**, un motor de descubrimiento estructural que opera
por refinamiento iterativo de vecindades (1-WL / color refinement) sin
taxonomía previa, y un protocolo de laboratorio que permite **descubrir,
congelar, identificar y verificar** regularidades estructurales. El motor
iguala a los fingerprints de Morgan en moléculas reales (AUC 0.9608 vs
0.9541 sobre 40 000 compuestos) y descubre estructura en código humano real
(dos familias estables, ARI 0.615/0.802). Como resultado matemático,
T4 — la invariancia del perfil del color refinement bajo complemento —
fue **propuesto y verificado por el motor** (mecanismo de conjeturas
construido por el humano: el motor propuso, refutó, verificó, descubrió
la ley, generalizó y asimiló la capacidad), verificado en 2 131 019
grafos exhaustivos (n≤7) y 19 407 adversariales, con **prueba** escrita
(la inyectividad de la resta de multiséts de vecindades).
Más aún: parametrizando el *universo de observación* (la función que
comprime los conteos de vecinos y la involución que actúa), encontramos
una **ley emergente**: `T4 vive ⟺ la involución es trivial, o es dual
global y el conteo distingue 1 de 2`. La ley fue **elegida por la tabla,
no por el humano** (dos hipótesis humanas fueron refutadas por los datos)
y se verifica en 102/102 casos. Clasificamos las involuciones en tres
clases exhaustivas (trivial / dual global / local) y publicamos un
**atlas** de 15 universos. Un segundo ciclo refinó la ley hasta una
**caracterización**: `T4(ι,f) vive ⟺ ι ∈ Sₙ·K` (K = grupo de Klein de
las operaciones globales) y, cuando `ι` cambia el par, `f(1)≠f(2)`; la
disyunción humana "preserva el par ∨ distingue 1 de 2" fue **falsada en
ambas direcciones** (EXP-110) y la pieza que faltaba resultó ser la
**uniformidad**. La dirección (⇐) está **probada** (mecanismo de
conteos); la (⇒) está **verificada** exhaustiva en n≤4 (96 = 24·4
exactas, cero fuera) y dirigida en n=5, y una **búsqueda autónoma de
construcciones** halló el mejor testigo válido (`ciclo`, 99.63%) — un
**control negativo** cazó y retiró una "prueba" que medía la iota
extendida (otra operación). Todos los resultados son reproducibles con
38 workers; los límites (∀n de (⇒) abierto, n≤6–7, definiciones propias,
revisión externa pendiente) se declaran explícitamente. La **v2** agrega
el arco de universos (§12): la ley multicapa (coherencia de canales), el
grupo preservante, la escalera k\*, la matriz universo×observador, la
predicción en hipergrafos, el fallo del transplante por aridad y el dual
asimilado; y el **Santo Grial** (§13): la completitud en la clase, su
**precio** (6 168 pares del cociente por complemento), la individualización
y el retículo IR↔k-WL.

**Abstract (English)**. We present GraphKind, a structural discovery engine
based on iterated neighborhood refinement (1-WL) with no prior taxonomy,
plus a laboratory protocol to discover, freeze, identify and verify
structural regularities. The engine matches Morgan fingerprints on real
molecules (AUC 0.9608 vs 0.9541, 40k compounds), discovers stable
structure in real code, **proposed and verified theorem-candidate T4**
(complement-invariance of the color-refinement profile; the conjecture
mechanism was human-built: the engine proposed, refuted, verified,
discovered the law, generalized it and assimilated the capability;
verified on 2 131 019 exhaustive graphs plus 19 407 adversarial ones,
with a written
proof), and yields an **emergent law** over observation universes:
`T4 holds ⟺ the involution is trivial, or dual-global with a count that
distinguishes 1 from 2` (102/102 verified; the law was selected by the
data, not by us). A second cycle refined this into a **characterization**
`T4(ι,f) holds ⟺ ι ∈ Sₙ·K and (ι changes the pair ⟹ f(1)≠f(2))`: the
human disjunction "preserves the pair ∨ distinguishes 1 from 2" was
**falsified in both directions**, uniformity being the missing piece;
(⇐) is **proved**, (⇒) **verified** exhaustively in n≤4 and targeted in
n=5, and an **autonomous construction search** found the best valid
witness (`cycle`, 99.63%) while a **negative control** caught and
retracted a "proof" that measured the extended involution. All results
are reproducible; limits are declared.

---

## 1. Introducción

Los sistemas de descubrimiento automático suelen atacar problemas con una
métrica y un objetivo fijos. Nuestra pregunta es distinta:

> ¿Puede un sistema **descubrir regularidades estructurales** antes de
> disponer de una semántica humana para nombrarlas — y puede hacerlo
> también **sobre sus propias reglas de observación**?

La tesis del laboratorio se resume en: **la sintaxis se declara; la
semántica emerge**. El sistema recibe objetos (grafos, moléculas, código,
secuencias) y reglas de observación; el resto — familias, invariantes,
anomalías, leyes — se busca y se verifica, con **controles negativos** que
distinguen estructura real de fabricación.

**Contribuciones**:

1. Un motor de kinds emergentes (WL) con paridad frente al estándar
   industrial (Morgan/ECFP) y con descubrimiento estructural en código
   real (§4).
2. Un protocolo de laboratorio: selector de representaciones, controles
   multi-réplica, re-auditoría e identificación post-freeze (§4).
3. **T4**: descubierto autónomamente, verificado masivamente, con prueba
   escrita y capacidad medida (§5).
4. **La ley de universos**: una condición puntual (`f(1)≠f(2)`) que la
   tabla eligió; clasificación trivial/dual/local; atlas (§6).

---

## 2. Trabajo relacionado (y qué no somos)

- **Color refinement / 1-WL** [Weisfeiler–Leman 1968; Morgan/ECFP]:
  nuestro kernel. Sabido: 1-WL no distingue grafos regulares del mismo
  grado (C6 vs 2·C3). No aspiramos a resolver isomorfismo [Babai 2016].
- **Expresividad de GNNs** [Xu et al. 2019; Morris et al.]: los mensajes
  de paso están acotados por 1-WL. Nuestro motor no es una GNN: no
  aprende, **deriva**.
- **Generación de conjeturas** [Graffiti; AutoGraphiX; Ramanujan Machine;
  AlphaTensor/AlphaGeometry]: comparten el espíritu de "buscar
  regularidades". La diferencia aquí: (a) el sistema descubre conjeturas
  **sobre su propio invariante**; (b) la ley final fue **refutando
  hipótesis humanas**, no confirmándolas.
- **Homomorfismos y WL** [Dvořák 2010; Dell–Arvind–Larsson 2018]: base
  para la conexión con conteos; nuestro EXP-092-093 falsificó la
  triangularidad lineal sobre árboles y conexos (aparecen productos).
- **Teoría de grafos hamiltonianos** [Tait 1884; Petersen; Zamfirescu
  1980]: usada como coto de prueba de nuestro pipeline de refutación.

**Lo que no somos**: no probamos teoremas generales (T4 tiene prueba
escrita, pendiente de revisión externa); no resolvemos P vs NP,
Hadwiger, CDC, Lovász ni Erdős–Hajnal; no violamos límites de la
computación — buscamos **universos donde el viaje es más corto** (§6).

---

## 3. El motor y el laboratorio

### 3.1 Definiciones

- **Grafo** `G=(V,E)`: nodos con `(tipo, valor)` y aristas etiquetadas
  dirigidas (el laboratorio usa aristas en ambos sentidos para grafos
  simples).
- **Color refinement** (1-WL): `color_0(v)=H(tipo|valor|grado)`;
  `color_{r+1}(v)=H(color_r(v) | multiset ordenado{(color_r(u),label,dir)})`;
  se itera hasta partición estable (o 64 rondas, con warning).
- **Kinds emergentes**: las clases de color estables (sin taxonomía
  previa). **Perfil** `I(G)`: multiset ordenado de tamaños de clase.
- **Complemento**: `Ḡ = (V, J−I−A)`.

### 3.2 Protocolo del laboratorio

1. **Representación**: el sistema **elige** la mirada (p.ej. entre
   R1–R6, o 16 miradas generadas) por criterio pre-registrado.
2. **Controles**: negativo (shuffle de marginales; **mediana de N=5
   réplicas** — una sola pasada es inestable), estabilidad (mitades),
   predicción (GMM sobre holdout).
3. **Congelar antes de interpretar** (`results_frozen.json`).
4. **Identificación post-freeze**: comparar con propiedades
   independientes (ARI contra referencias) — y **corregir la
   interpretación** si no se sostiene.
5. **Reproducibilidad**: `SEED=7`, Pool(22) (22 núcleos/44 hilos) con
   verificación de CPU (1200–2200%), tests del motor 104/104 al cierre
   de la v2, CI.

### 3.3 La regla de oro

Los hallazgos son **del motor** (autónomos, sin leer literatura). El
estatus "descubrimiento vs redescubrimiento" se decide **contra la
literatura, con verificación** — nunca por suposición. Esta regla nos
obligó a reetiquetar hallazgos propios (p.ej. C6b) y a re-auditar señales
previas (§4.3).

---

## 4. Resultados I: descubrimiento estructural

### 4.1 Moléculas: paridad con el estándar

| métrica | GraphKind (WL r1+sym) | Morgan ECFP |
|---|---|---|
| AUC TEST (40 000 ChEMBL) | **0.9608** | 0.9541 |
| AUC CV-5 | 0.9617 ± 0.0015 | 0.9511 ± 0.0012 |

La ventaja **crece con el dato** (+0.0013 a 4k → +0.0067 a 40k): la
equivalencia estructural no es un artefacto de muestra.

### 4.2 Código real: estructura estable

Sobre 600 funciones Python reales (CodeSearchNet), el sistema eligió su
mirada y encontró dos familias estables (ARI mitades 0.615/0.802 ≥ 0.5
pre-registrado). La identificación post-freeze mostró que la separación
es de **tamaño/complejidad** (116 vs 413 nodos; la fracción
"llamadas vs atributos" idéntica): una interpretación semántica previa
fue **corregida por el protocolo**.

### 4.3 El valor del control negativo

En 6/6 campañas de ontología sobre proteínas (051–056), el control
rechazó todas las candidatas — incluidas las siluetas más altas del
laboratorio (0.962, 0.966). La re-auditoría multi-réplica (077) tumbó
señales previas (052: −0.006) y confirmó la estructura del 050. **El
sistema no fabrica categorías.**

---

## 5. Resultados II: T4, de conjetura a teorema candidato

### 5.1 Descubrimiento autónomo

El sistema, en un corpus ciego de 10 familias, propuso conjeturas sobre
transformaciones y halló: `I(Ḡ)=I(G)` en 68/68. Cámaras posteriores:
**3 045** grafos aleatorios + **19 407** adversariales + **2 131 019**
exhaustivos (todos los grafos n≤7, **100.0000%**) + lema por ronda
(multisets iguales en cada iteración) + compatibilidad
(`I(G)=I(H) ⇒ I(Ḡ)=I(H̄)`, 688/688).

### 5.2 La prueba (versión fuerte)

> Para todo grafo finito simple `G`: las particiones del color refinement
> de `G` y `Ḡ` son **idénticas** sobre `V` (y por tanto los perfiles).

**Prueba**: inducción sobre rondas. Base: los grados se complementan
(`d ↦ n−1−d`). Paso: la vecindad cerrada se invierte
(`N_Ḡ[v]=V∖N_G(v)`), y la aplicación `M ↦ T−M` (T fijo) es **inyectiva**
sobre multiséts de colores ⇒ la relación "mismo color" se preserva ronda
a ronda. ∎ *(escrita en `PRUEBA-T4.md`; pendiente de revisión externa.)*

### 5.3 Capacidad (el teorema como herramienta)

- **Sanity interno**: `I(G)=I(Ḡ)` como test de consistencia del motor
  (0 fallos en 2 000 grafos).
- **Normalización dual**: almacenar el lado más ralo de {G, Ḡ} sin perder
  el perfil: **40.5% de ahorro** de aristas.
- **`refine_dual` en el motor** (validado por experimento): refinar el
  lado ralo acelera hasta **10.3×** en grafos densos (2.38× global), con
  identidad de partición garantizada.

---

## 6. Resultados III: universos y la ley emergente

### 6.1 El mapa

Parametrizando el **universo de observación** `(f, ι)` — `f` comprime los
conteos de vecinos; `ι` es la involución (complemento, relabels, locales)
— medimos dónde vive T4:

| universo | T4 |
|---|---|
| conteo exacto, F2 (paridad), dirigido, vértices/aristas tipados | ✅ vive |
| umbral booleano (≥1) | ❌ muere (testigo mínimo n=4) |
| tropical | no aplica (sin involución natural) |

### 6.2 La ley (elegida por la tabla)

Barriendo 17 funciones `f` (identidad, mod p, umbral k, truncado, log,
polinomios…) × 2 involuciones:

> ### **T4 VIVE ⟺ f(1) ≠ f(2)**
> (34/34 en el barrido del eje del conteo; 102/102 en el blindaje.)

**Mecanismo**: en el complemento, un vértice con 1 vecino de color c pasa
a `|c|−1` (que puede ser 2): si `f` colapsa 1 y 2, la dualidad muere.
**No importa** qué hace `f` con 3, 4, 5…: solo la distinción mínima.

Dos hipótesis humanas fueron **refutadas por los datos**:
"involución inyectiva" (101) y "cada involución tiene su par" (104).

### 6.3 La clasificación y la ley unificadora

Con la definición formal — `ι` es **dual global** si existen `σ:V→V` y
`g:N→N` con `|N_{ι(G)}(v)∩σ(c)| = g(|N_G(σ(v))∩c|, |c|, n, 1[σ(v)∈c])`,
`g` inyectiva — las involuciones se parten en **tres clases**:

| clase | ejemplos | T4 |
|---|---|---|
| **trivial** (g=id) | swap, reverse | vive siempre |
| **dual global** | complemento, complemento∘reverse | ⟺ `f(1)≠f(2)` |
| **local** | complemento parcial, flip de vértice | **imposible** (ninguna f) |

> **Ley de las leyes**: una involución admite T4 ⟺ induce una
> transformación **global** de la vecindad; y cuando lo hace, la
> condición es **siempre** `f(1)≠f(2)`. Verificada **102/102**.

### 6.4 El explorador y el atlas

Con el **mismo banco** de conjeturas en 15 universos: Tperm y Tunion2 son
**universales**; T4 es **específica** de la región `f(1)≠f(2)`; Tsub,
Tdup, Tleaf son **imposibles**; la frontera paramétrica es `k_c=2`
(TRUNC) y no monótona (THRESH). El **atlas** (15 JSONs, en `resultados/atlas/`) fija el formato
estable: cada universo con su conteo (`f1/f2`), sus involuciones (clase +
veredicto), la ley y la evidencia.

### 6.5 La caracterización Sₙ·K (EXP-110 → 113)

La ley del 102 es el caso particular (involución que cambia el par) de
una caracterización más fina. La disyunción humana

```
T4 vive ⟺ M1 (preserva el par) ∨ M2 (cambia el par ∧ f(1)≠f(2))
```

fue **falsada en ambas direcciones** (EXP-110): `flip_inc0` preserva el
par y **muere 0/24** (M1 no basta: falta **uniformidad**); y con `f=id`
mueren **1364/1504** iotas que cambian el par de forma no uniforme (M2
no basta). Los "tercer camino" aparentes eran rango (resueltos en real:
`comp_dir+const1` muere 0/94). Lo que emerge:

```
T4(ι, f) vive ⟺ ι ∈ Sₙ·K   y   (ι cambia el par ⟹ f(1) ≠ f(2))
K = {id, comp_dir, transp, comp_transp} ≅ Z₂×Z₂
```

- **(⇐) probada**: σ (relabel) y s (swap in/out) viven con toda `f`;
  c (complemento uniforme) vive ⟺ `f(1)≠f(2)` (mecanismo de conteos,
  contraejemplo n=6).
- **(⇒) verificada**: n=4 exhaustivo (**96 = 24·4 exactas, cero
  fuera**); n=5 dirigido (7680/8160 con testigo; las 480 sin testigo
  son uniformes); afín aleatoria n=4 (10000/10000 con testigo); real
  (moléculas 100/100, CST 94/94).
- **Búsqueda autónoma** (113): con un lenguaje de 11 primitivos + 3
  combinadores (~400 recetas) y criterio tasa/MDL, el motor halló que
  el mejor testigo **válido** es `ciclo` (**99.63%**, complejidad 1),
  mejor que la construcción humana C1 (97.8%); **ninguna válida llega
  al 100%**.
- **Corrección (control negativo)**: las recetas con aislado daban 100%
  pero usaban la **iota extendida** a n+k — otra operación. El control
  de uniformes falló 52/104 (deben ser 0 por (⇐)) y delató el
  artefacto; la "prueba" quedó **retirada** (documentada, no borrada).
- **Relatividad al WL**: `transp` es dual con WL simétrico y local con
  out-only; 76/1504 iotas cambian de veredicto. El esquema correcto es
  **(universo, WL, involución, f) → resultado**.

---

## 7. Discusión

1. **El resultado central no es T4: es el método.** La ley de universos
   fue *seleccionada por los datos* — el humano puso hipótesis y la tabla
   las refutó dos veces. Eso es lo que distingue un laboratorio de un
   buscador de confirmaciones.
2. **Universal ≠ interesante.** La ley muestra que las conjeturas viven
   en regiones: saber *dónde nace* una propiedad es un fenómeno de
   segundo orden, y el explorador lo mide con métricas objetivas.
3. **Los controles negativos son el activo.** La historia del laboratorio
   incluye señales propias tumbadas (052, 070) e interpretaciones
   corregidas (050): la credibilidad viene de ahí.
4. **Relación con los LLMs.** Un LLM describe universos; este sistema
   **corre en ellos**. La diferencia operativa: el barrido paramétrico +
   la verificación + el congelado, no el conocimiento.

---

## 8. Límites (declarados)

- **T4**: prueba escrita, **pendiente de revisión externa/bibliográfica**
  y de formalización asistida (Lean no disponible en el entorno).
- **La ley de universos**: verificada 102/102 en n≤6; candidata a
  teorema (el mecanismo está esbozado; la prueba general es trabajo
  externo).
- **La caracterización Sₙ·K**: (⇐) probada; (⇒) verificada en n≤4
  exhaustivo, n=5 dirigido y real; **∀n abierto**; receta universal
  100% **no hallada** (mejor válida: `ciclo` 99.63%); la "prueba" por
  extensión fue retirada por control negativo (EXP-113).
- **C6/C6b**: el mínimo `n=8` (3-conexo no trazable) hallado
  autónomamente; su estatus frente a la literatura requiere verificación
  (no se etiqueta por suposición).
- **Universos**: definiciones propias y declaradas; el espacio es
  abierto (más ejes: estructura base, CR no estándar).
- **Datos**: ChEMBL (CC-BY 4.0), CodeSearchNet, UniProt, Pfam —
  citados; muestras fijas por seed.

---

## 9. Reproducibilidad

- **Tags**: v0.1.0 … v0.7.1 (11 releases privados).
- **Tests del motor**: 104/104 (v2) · **CI** verde · `reproduce.sh` OK.
- **Comandos clave**:
  ```bash
  bash reproduce.sh
  cd EXPERIMENTS/EXP-084... && python run.py   # T4 exhaustivo n≤7
  cd EXPERIMENTS/EXP-102... && python run.py   # la ley f(1)≠f(2)
  cd EXPERIMENTS/EXP-105... && python run.py   # blindaje 102/102 + atlas
  ```
- **Regla de hardware**: Pool(22), CPU verificada 1200–2200%.

---

## 10. Conclusión

Un motor estructural, sin aprendizaje ni taxonomía, **descubre**:
kinds en moléculas y código, un teorema candidato (T4) con prueba y
capacidad, y una **ley sobre sus propias reglas de observación** que la
tabla eligió. El laboratorio entrega además el método completo —
parametrizar, generar, correr, congelar, identificar, verificar — con los
límites a la vista y todo reproducible. La pregunta abierta que deja:
¿qué propiedades matemáticas **aparecen solo cuando cambia la regla de
observación**? El atlas es el mapa; los próximos ejes, el territorio.

---

## 12. El arco de universos (v2, EXP-162 → 169)

La v2 agrega el **arco de universos** del laboratorio, con el mismo
protocolo (predicción/freeze antes de medir, controles, correcciones
registradas). Cada resultado tiene su freeze en `resultados/` y su
verificación ejecutable en `codigo/verificaciones_v2.py` (V13–V16).

**12.1 Multicapa: la ley de coherencia (EXP-162/163/164).** En un grafo
multicapa `(V, E_1..E_L)` con refinamiento conjunto (variantes
**canónica** = canales como conjunto, y **ordenada**): T4 vive con el
complemento **total** (1298/1298 en L=2; 1404/1404 en L=3) y **muere con
el complemento por capa** (6.9% y 7.4% de fallas) — **solo en la
canónica**; la ordenada es el control (todo vive). Ley: *el complemento
tiene que actuar uniformemente sobre las capas*. El **grupo preservante**
es exactamente el subgrupo uniforme `U = {∅, todas} × S_L` en la canónica
(L=2: 4/4; L=3: 12/12, cierre de grupo ✓) y **todo el grupo** en la
ordenada. La **escalera k\*(L)** es plana (`k*=1` para L=2..5, dos
corpus), lo que **corrige** el `k*=2` de EXP-162 (era el `k=1`
degenerado). La (⇐) de la ley está **probada** (misma biyección
`M ↦ T−M` por capa); la (⇒) queda abierta.

**12.2 Matriz universo × observador (EXP-165).** Con dos métricas por
celda (T4 y frontera de completitud), reusando los freezes: la frontera
**se mueve con el observador** (WL/KW2 fallan en n=6; KW3/IR1p no) y **no
se mueve con el tipado** (fila nueva n≤6, 5 342 clases, mismo `n_min`).
De la pareja (universo, observador), la mitad que pesa es el observador.

**12.3 Hipergrafos 3-uniformes (EXP-166): el mapa es predictivo.** Se
declaró un universo nunca visitado, se **predijo** T4 con la ley (el
complemento es dual global: resta de multiséts con total fijo) y se midió:
**1831/1831** (n≤5 exhaustivo + muestra n=6). La frontera medida coincide
con la de grafos (`n_min=6`).

**12.4 Aridad k y aridades mezcladas (EXP-167).** La **escalera de
aridad** vive (k=4: 156/156; k=5: 7/7). Pero el **transplante de la ley
de canales falla**: en aridades mezcladas {2,3}, el complemento **total**
vive (100%) y el **por aridad también** (1038/1038, ambas variantes) —
la diferencia es la **estructura del mensaje** (en multicapa las capas
comparten tipo; en mezclado los mensajes por aridad difieren y el
refinamiento repara). La ley es **de canales**, no de toda descomposición.

**12.5 El reparo y su asimilación (EXP-168/169).** Búsqueda **dirigida**
(construcción canónica, n=6,7,8, controles negativo y total): **261 000
casos, 21 821 fusiones dirigidas, todas reparadas, 0 testigos** → reparo
robusto (B). Consecuencia: el dual **por aridad** entra al motor
(`refine_dual_mezclado`): validación 60 000 casos, **partición 100%**,
ahorro **14.37%** (vs 10.26% del dual total). Ciclo completo: anomalía →
conjetura → testigo → capacidad.

**12.6 Verificaciones v2.** V13 (multicapa: total vive, por-capa muere en
la canónica, canales viven), V14 (hipergrafos: T4 vive), V15 (dual:
partición + ahorro), V16 (aridades mezcladas: por aridad vive). Todas
ejecutables con `python codigo/verificaciones_v2.py`.

## 13. El Santo Grial: completitud, su precio y los patrones (SG-01→03)

**13.1 La familia mínima completa en la clase (SG-01).** Sobre **todos**
los grafos no isomorfos n≤7 (geng) → freeze → n=8 (12 346 grafos;
**76 205 685 pares**), la familia mínima que alcanza la completitud es
**F3 = {WL, 2-WL, 3-WL}** con **C_8 = 0** (desenlace **A**). El
leave-one-out muestra que **k-WL 3 hace el trabajo** (quitarlo deja 350
colisiones); el control de relabeling (50/50) descarta fuga. No es un
invariante completo universal: a **n=16 Rook/Shrikhande** colisiona
F1–F6 y solo la familia total lo separa — la completitud es **de la
clase**, con la frontera medida.

**13.2 El precio de T4 (SG-01).** El invariante completo **no es
complemento-invariante**: el cociente `G ~ Ḡ` fusiona exactamente
**6 168 pares** (con 10 autocomplementarios en n≤8). Esa es la
información que T4 describe, **cuantificada**: la complemento-invarianza
cuesta esos pares. La verificación v2 (V17) ejecuta el análogo n≤5: 52
grafos, 4 autocomplementarios, **24 pares fusionados**.

**13.3 Individualización y el retículo IR↔k-WL (SG-02/03).** La
individualización mínima es **i\*=1** para los 13 597 grafos de n≤8
(ninguno necesita 0: WL nunca es único en la clase; ninguno necesita 2).
En la frontera, Rook/Shrikhande exige **i\*=2**: `IR_1` **no** los separa
(y falla donde falla 3-WL), `IR_2` **sí** (se comporta como 3-FWL ≡
4-WL). El retículo sobre n≤9 (274 668 grafos) muestra que **todos los
invariantes completos colapsan** (partición discreta idéntica:
equivalencia vacua) y que `WL = 2-WL`; la evidencia discriminante son
las anclas (C6/2C3, Rook/Shrikhande, Petersen/C5). Cierre: **A** en
anclas, **B** (IR_2 > 3-WL) y **C no observado**. La verificación v2
(V18) ejecuta las anclas.

**13.4 El método: los patrones transversales.** Ocho patrones sostienen
todo el laboratorio: (1) **el dato decide** (k\*, r\*, umbrales por
validación interna); (2) **congelar antes de interpretar**; (3) **control
negativo obligatorio** (sin control, un número no se reporta); (4)
**atribución A/B/C/D** (A laboratorio, B motor, C en `naturalkinds/`, D
validado a ciegas); (5) **emerger ≠ barrer** (CV, no sweeps); (6) **las
correcciones se registran, no se borran** (D-001→D-017); (7) **el
negativo vale** (refutaciones documentadas); (8) **versionado exacto del
motor** (`MOTOR.json`). El `DECISION_LOG.md` completo viaja en
`paper/DECISION_LOG.md`.

**Pendiente declarado**: la (⇒) ∀L de `PRUEBA-MULTICAPA.md` y la
frontera exacta n=10→16 del universo estándar (SG-04, en curso).

## Referencias (selección)

- Weisfeiler, Leman (1968). *A reduction of a graph to a canonical form…*
- Morgan (1965); Rogers, Hahn (2010). *Extended-connectivity fingerprints.*
- Dvořák (2010); Dell, Arvind, Larsson (2018). *Homomorphisms and 1-WL.*
- Babai (2016). *Graph isomorphism in quasipolynomial time.*
- Xu et al. (2019). *How powerful are graph neural networks?*
- Zamfirescu (1980); Abrishami, Rahbarnia (2026). *Non-traceable 3-connected planar cubic graphs.*
- Erdős, Fajtlowicz, Staton (1987). *Arboricity conjecture.*
- Petersen (1891); Tait (1884). *Hamiltonian graphs.*
- Lovász (1970). *Problem on vertex-transitive graphs.*

---

## 11. Addendum — universos dinámicos, probabilísticos y observadores

Después de la ley (§6), el laboratorio cambió el **tipo del invariante**
en tres direcciones. En cada una, T4 cambia de categoría:

| universo | invariante | T4 es… | resultado |
|---|---|---|---|
| estándar | partición | igualdad | **vive** (T4, probado) |
| **Z₃ determinista** (EXP-116) | **órbita** | igualdad de períodos | **muere** (máx. 52.4%, `maj`) |
| aleatorio **R1** (EXP-117) | distribución | igualdad de distribuciones | **muere** (18.6%) |
| aleatorio **R2** (EXP-117) | distribución | igualdad en distribución | **vive** (casi seguro) |
| aleatorio **R3** (EXP-117) | medida | fracción | **umbral = medida** |
| jerarquía **k-FWL** (≡ (k+1)-WL; EXP-118/119) | partición de k-tuplas | complemento-invarianza | **T4_k: 51/51** en k=1,2,3 |
| cascada (EXP-119) | — | — | **26 → 0** pares no separados (n≤7) |
| Rook vs Shrikhande | — | — | **k\*=3** (k-FWL: 3-FWL sí; el 3-WL estándar NO — D-005) |

**Hallazgos centrales del addendum**:

1. **Z₃ determinista**: el invariante es una **órbita** (período +
   transitorio + distribución); la dualidad del conteo no tiene análogo
   dinámico y T4 **muere** (6 reglas medidas; `maj` es la más robusta).
   Aparecen períodos nuevos (3, 5, 7, 13, 19, 26, 39, 78, 104) — y, con
   F arbitraria, también en Z₂ (la intuición "solo potencias de 2" vale
   para dinámicas lineales).
2. **Aleatorio**: el azar en el **proceso** (R1: WL asíncrono) **rompe**
   T4 (18.6%); el azar en el **objeto** con la simetría correcta (R2:
   G(n,p) vs G(n,1−p)) lo **preserva** (el complemento biyecta los
   ensembles); el azar en la **operación** (R3) convierte T4 en un
   **umbral**: la fracción de involuciones que lo admiten es una función
   de la medida del ensemble.
3. **Observadores**: la jerarquía k-FWL (≡ (k+1)-WL) **preserva** la
   complemento-invarianza (T4_k 51/51) y la aleatoriedad aparente
   **decrece** con el poder del observador: en el atlas completo n≤7
   (781 875 pares), 1-WL deja 26 pares sin separar y **2-WL los resuelve
   todos** (k\*=2); el par canónico Rook/Shrikhande requiere k=3.

**Correcciones registradas** (parte del método): 5 bugs propios cazados
por controles (multiset de tamaños → colores → índices → posición →
construcción del Shrikhande). El error del Shrikhande (se construyó el
Rook dos veces) fue cazado por el análisis de invariantes
(`is_isomorphic = True`): la k-FWL implementada era correcta (el 3-WL estándar NO separa Rook/Shrikhande: D-005); el grafo de
prueba, no.
