# Auditoría de reproducibilidad — 2026-10-25

> Tres puntos planteados por una revisión externa: (1) el claim de
> 2.131.019 no era reproducible con particiones; (2) `f` y el `False` de
> `t4_garantizado` no estaban claros; (3) la caracterización `Sₙ·K` es lo
> único potencialmente nuevo y necesita revisión externa. Este documento
> registra qué se hizo, qué se midió y qué queda abierto.

## 1. Certificado de particiones (EXP-086p)

El claim del paper se verificaba con V1, que compara el **perfil** (multiset
de tamaños de clase), una versión más débil que la igualdad de particiones.
Se agregó `codigo/verificaciones_particiones.py`: 1-WL simétrico propio,
exhaustivo n=1..7, comparando `CR_1(G) == CR_1(Ḡ)` como **particiones** del
mismo `V`.

Resultado (doble corrida, `--doble`):

- `2.131.019/2.131.019`, **0 mismatches**.
- Por n: 1, 2, 8, 64, 1.024, 32.768, 2.097.152.
- sha256 del certificado: `cdb16f5c0b52c405056101ed48ff9c82d799b457f10b988c532921dc87e1844a`.
- Wall 35,7 s / 36,1 s por corrida con `--nproc 22` · CPU 1.830% · RSS 19 MB;
  doble corrida 72 s.
- Freeze: `resultados/EXP-086_particiones_frozen.json`.

**Bug encontrado en el camino.** `wl_k_colors(..., k=1)` no refinaba: el loop
`for i in range(k): for j in range(i+1,k)` queda vacío para k=1, así que V3
k=1 medía la partición por grado, no 1-WL. Ejemplo: n=5, mask 28 → grado
`[4,1]`, 1-WL `[1,2,2]`. Se corrigió `wl.py` con `_wl1_colors` (1-WL
simétrico) y se agregó un sanity en V3. El teorema no cambia; el 2.13M con
particiones lo confirma.

## 2. `f` y el `False` de `t4_garantizado`

- `f: N→N` comprime los **conteos de vecinos por color** en la ronda de WL.
  No comprime grados ni colores iniciales: el color inicial usa el grado
  crudo; en la actualización, cada conteo `k` se reemplaza por `f(k)`. La ley
  solo mira `f(1)` y `f(2)`; lo que `f` haga con 3,4,5… es irrelevante.
- `t4_garantizado(f1, f2, clase)` recibe `f1=f(1)`, `f2=f(2)` y la clase de
  `clasificar_involucion` (`trivial`/`dual`/`local`). Devuelve una
  **predicción** de T4, no un estado de error:
  - `trivial` → `True` con toda `f`;
  - `dual` → `True` si `f1 != f2`, `False` si `f1 == f2`;
  - `local` → `False` siempre (ninguna `f` la salva).
- Se cambió el fallback silencioso por `ValueError` para una clase
  desconocida, y se agregó `t4_garantizado_f(f, clase)`. Doctests OK.
- **Variante de WL**: `clasificar_involucion` usa WL out-only; el teorema usa
  WL simétrico (in/out). `transp` es dual con WL simétrico y local con
  out-only; la ley es relativa a `(universo, variante de WL, ι, f)`.

## 3. Revisión externa de `Sₙ·K`

No se puede conseguir un reviewer humano desde el repo; se preparó el brief
`paper/REVIEWER-BRIEF-SnK.md` con definiciones exactas, claims, estatus,
prior art y preguntas. Lo que sí se verificó:

- **C1 (complemento)** ya está en Kiefer & de Mel (SODA 2026, Lemma 4.5) y
  cerca del flip lemma de Kiefer–Schweitzer–Selman (ICALP 2015).
- **El flip lemma no es C3**: es una normalización local por par de clases
  C², dependiente del coloreo, no una involución uniforme global.
- No se encontró en la literatura la caracterización `Sₙ·K` con la cláusula de
  uniformidad y la ley `f(1)≠f(2)`; **no se puede confirmar novedad** sin
  revisión externa.
- **Abierto**: C2 para `f` arbitraria; C3 (⇒) para todo `n`.

## 4. Archivos y comandos

Archivos nuevos/cambiados:

- `codigo/verificaciones_particiones.py` — certificado EXP-086p.
- `codigo/wl.py` — `wl_k_colors(k=1)` ahora es 1-WL simétrico.
- `codigo/universos.py` — docstring de `f`, `ValueError`, `t4_garantizado_f`.
- `codigo/verificaciones.py` — sanity de V3 (k=1 refina).
- `resultados/EXP-086_particiones_frozen.json` — freeze del certificado.
- `paper/REVIEWER-BRIEF-SnK.md` — brief para revisión externa.
- `README.md` / `README.es.md` — sección 7f y fila V1b.

Comandos:

```bash
python3 codigo/verificaciones_particiones.py --nmax 7 --doble --nproc 22
python3 codigo/verificaciones.py --rapido
python3 codigo/verificaciones_v2.py
python3 -m doctest codigo/universos.py
```
