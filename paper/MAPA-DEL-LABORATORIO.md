# El mapa del laboratorio — 120 experimentos, verificables

> GraphKind · 2026-09-10 · documento de síntesis
> Verificación: **EXP-120** (`26/26` hitos contra los freezes) ·
> índice completo: `EXPERIMENTOS-INDICE.md` · paper: `PAPER.md` ·
> ciclo de universos: `TEOREMA-UNIVERSOS.md` · motor: `MOTOR-GRAPHKIND.md`.

---

## 0. Los números del corpus

| métrica | valor |
|---|---|
| experimentos | **120** (EXP-000 → EXP-120) |
| con `run.py` | 113 |
| con resultados congelados | 112 |
| con README | **120** |
| líneas de `run.py` | **26 384** |
| resultados congelados | **321 KB** |
| hitos verificados por EXP-120 | **26/26** |

Todo el laboratorio se reproduce con `reproduce.sh` y cada número de
este documento está anclado a un artefacto congelado que EXP-120
comprueba automáticamente.

---

## 1. Fundacional (EXP-000 → 010)

**Pregunta**: ¿se puede describir estructura sin taxonomía previa, y a
qué granularidad?

| hito | número |
|---|---|
| Baseline código real (FROZEN-12) | 87.1% de nodos; 11 kinds para el 95% |
| Auditoría de la taxonomía | **colapso 0.5876** (58.8% de información descartada), B=0 ruido |
| Moléculas ChEMBL (5K→50K) | compresión 2.485× → **3.001×**; 474 840 kinds |
| Paridad con Morgan (750 pares) | **1.0000 vs 0.9973** |
| Granularidad natural | k\* = 21 → 24; meseta 13–27; techo en 28 |
| Superficie G(r,k) | máximo acuerdo con la taxonomía humana **ARI 0.736** |

**Lección**: la taxonomía manual no es la verdad — es una compresión
que descarta estructura medible. La granularidad emerge del dato.

---

## 2. Riemann (EXP-011 → 019)

**Pregunta**: con el objeto matemático crudo (primos, ceros), ¿qué
estructura emerge sola, con controles?

| hito | número |
|---|---|
| 2 001 052 ceros (Odlyzko) | **JS 0.1350 vs remap 0.0161** (8.4×) |
| Transferencia OOS | JS 0.0191; Montgomery **0.670** |
| Puente de Euler | **a = 0.16110** ⊃ **1/2π = 0.159154** (dentro del CI) |
| Línea crítica | **σ\* = 0.50000** (12/12 ceros, derivado del dato) |
| 18 L(s,χ) | OOS 0.0337 vs remap 0.2380 (7.1×) |
| Subdivisión de L | **negativo limpio**: OOS ARI −0.054 / −0.083 |

**Lección**: la disciplina anti-sesgo (freeze, permutado, blind, OOS)
también funciona en matemática — y los negativos son resultados.

---

## 3. Aritmética, álgebra y física (EXP-020 → 046)

**Pregunta**: ¿puede el sistema representar y verificar matemática sin
reglas programadas?

| hito | número |
|---|---|
| r\* emergente (validación interna → B) | **r=1, AUC 0.8934** |
| WL discreto vs Morgan | **0.8877 vs 0.8864** (la vecindad como subestructura) |
| Cálculo estructural (sin aritmética) | neutro 10/10 · conmutativa 49/49 · asociativa 125/125 · puente 64/64 |
| Inversión | **100/100** verificados + "no hay solución" detectado |
| Derivación ciega | **16/16** con verificación independiente 16/16 |
| NS-3D | vórtice verificado; LAP=6; continuidad 3≠0 (control) |
| Integración | y'=2x → x²; y'=3 → 3x (búsqueda + verificación) |

**Lección**: las leyes se recuperan como equivalencias estructurales; el
lenguaje se declara, la semántica emerge.

---

## 4. Descubrimiento y ontología (EXP-047 → 079)

**Pregunta**: ¿qué descubre el sistema en código real y proteínas reales
— y qué rechaza?

| hito | número |
|---|---|
| Descubrimiento en código | 129 cadenas + 119 anillos + 152 estrellas (ARI 0.7034) |
| Código real (600 funciones) | 2 familias estables **0.615/0.802** (luego: eran tamaño) |
| Proteínas: 6 vías | **6/6 rechazadas por el control** (siluetas 0.96 incluidas) |
| Matemática emergente | x²/2, e^x/ln, TG-2D (λ=2ν), **λ=νn²**, ABC 6/6, cascada **√5**, límite Euler **~1.2** |
| WL vs Morgan a 40K | **0.9608 vs 0.9541** (la ventaja crece con el dato) |
| Transferencia bio→código | 0.461 vs 0.134 (3.4×) |
| Tribunal (077) | 050 sobrevive (0.615/0.802); 052 cae (−0.006); 070 era ruido |
| Identificaciones | 078: rareza [3998,2]; 079: 050 era **tamaño** (116 vs 413 nodos) |

**Lección**: el control negativo es el activo — el sistema **no fabrica
categorías**, y cuando una interpretación cae, se corrige y se registra.

---

## 5. T4 (EXP-080 → 098)

**Pregunta**: ¿puede el motor descubrir, verificar y probar un teorema
sobre su propio invariante?

| hito | número |
|---|---|
| Descubrimiento autónomo (corpus ciego) | **68/68** |
| Cámara de contraejemplos | **3 045/3 045** |
| Adversario masivo (8 generadores) | **19 407/19 407** |
| Exhaustivo n≤7 | **2 131 019/2 131 019 = 100.0000%** |
| Compatibilidad | 688/688 |
| Prueba escrita | `PRUEBA-T4.md` (inyectividad `M ↦ T−M`) |
| Capacidad | ahorro **40.5%**; `refine_dual` hasta **10.3×** |
| Banco de conjeturas | 21 × 2.1M; C6 refutada en n=8; C6b 858 violaciones; C6c resiste 5 114 079 |

**Lección**: de conjetura a teorema candidato con prueba escrita — y el
teorema entra al motor (`refine_dual`), validado por experimento.

---

## 6. Universos (EXP-099 → 120)

**Pregunta**: ¿en qué universos de observación `(f, ι)` vive T4 — y qué
tipo de teorema es en cada uno?

| hito | número |
|---|---|
| Ley del conteo | **T4 ⟺ f(1) ≠ f(2)** · 34/34 · blindaje 102/102 |
| Caracterización Sₙ·K | (⇐) **probada**; (⇒) n=4: **96 exactas**, cero fuera |
| Testigos | **6 424/6 424**; búsqueda autónoma: `ciclo` **99.63%** |
| Grafos reales | moléculas **100/100**; CST 94/94; consistencia 194/194 |
| Relatividad al WL | 76/1504 iotas cambian de veredicto |
| Z₃ determinista | T4-período **muere** (máx 52.4%) |
| Aleatorio | R1 muere (18.6%) · R2 vive · R3 umbral = medida |
| Jerarquía k-FWL (≡ (k+1)-WL) | T4_k **51/51** · cascada **26 → 0** · Rook k\*=3 |
| Auditoría externa (HF) | 29/30 en rango, pero **10/15 reproducen** su N; ruido dentro/fuera según método |
| Ley de N (búsqueda ciega) | los rangos **no convergen**: N es del método, no del sistema |

**Lección**: T4 no es absoluto — es **relativo al par (universo, WL)**;
el invariante cambia de tipo (partición → órbita → distribución →
observador) y con él cambia la categoría del teorema.

---

## 7. Los patrones transversales

1. **El método es constante**: congelar antes de interpretar, control
   negativo (multi-réplica desde 076), negativos honestos, y
   **correcciones registradas, no borradas**:
   050→tamaño · 052→cae · 070→ruido · 112/113→artefacto de extensión ·
   118/119→kernel k-FWL mal nombrado (D-005, corregido en 159) y **Shrikhande mal construido** (`is_isomorphic`).
2. **Cuatro tipos de resultado**: kinds → leyes matemáticas → teoremas
   → universos. Cada salto sube un nivel de abstracción.
3. **El motor evolucionó**: describir (kinds) → elegir (miradas) →
   probar (T4) → caracterizar (Sₙ·K) → buscar construcciones (ciclo) →
   **publicar con asserts**.
4. **La regla de oro**: el motor descubre; el estatus
   descubrimiento/redescubrimiento se decide contra la literatura con
   verificación, nunca por suposición.

---

## 8. Estado actual y publicación

- **T4**: prueba escrita, revisión externa pendiente.
- **Caracterización Sₙ·K**: (⇐) probada; (⇒) verificada; ∀n abierto.
- **Artefacto de publicación**: repo privado
  `cripto-bot/graphkind-universos` (paper + V1–V9 con asserts + CI +
  página ES/EN) — listo para arXiv cuando se decida.
- **Verificación de este mapa**: `EXP-120` (26/26 hitos) — correr
  `python run.py` en su carpeta.

---

*Este documento no reclama prioridad sobre problemas abiertos: reporta
lo que el laboratorio construyó, con cada número anclado a un artefacto
congelado y comprobable.*
