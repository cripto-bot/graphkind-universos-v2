# graphkind-harness

**Benchmark de invariantes estructurales** sobre universos (motor
[GraphKind](https://pypi.org/project/graphkind/)). Mide, sobre corpus **no
isomorfos**, lo que el paper mide:

- **Colisiones y frontera** por observador y por n (las curvas `C_n`).
- **Anclas**: la tabla de separación de los pares canónicos.
- **T4 por universo**: estándar (1-WL y k-FWL), multicapa (total vs por
  capa) e hipergrafo k-uniforme.
- **Controles**: invarianza bajo relabeling + control negativo (un
  observador débil *debe* colisionar).

Todo sale de un **JSON congelable** (versión del motor, corpus, semilla,
wall time) y es determinista.

## Instalar

```bash
pip install graphkind-harness
# para el corpus exhaustivo (no isomorfos):
sudo apt install nauty        # provee `geng`
```

## Uso (CLI)

```bash
# frontera completa hasta n=7 sobre todos los grafos no isomorfos
graphkind-harness run --corpus geng --n-max 7 --out freeze.json

# solo las anclas (no necesita geng)
graphkind-harness anclas

# reporte de texto de un freeze
graphkind-harness reporte freeze.json
```

Salida de `anclas`:

```
par         n     grado   wl      kw2     kw3     ir1     ir2
C6 vs 2·C3  6     separa  colisiona separa  separa  separa  separa
Petersen vs prisma 10 ...
Rook vs Shrikhande 16 ...
```

## Uso (librería)

```python
from graphkind_harness import bench

res = bench.run(corpus="geng", n_max=7, observadores="wl,kw2,kw3")
print(bench.reporte(res))
print(res["frontera"]["kw3"])      # colisiones por n
```

## Corpus

| nombre | qué es |
|---|---|
| `geng` | **todos** los grafos no isomorfos hasta `--n-max` (nauty) |
| `pairs` | los pares canónicos (C₆/2·C₃, Petersen/prisma, Rook/Shrikhande) |
| `random` | m grafos G(n,p) con semilla |
| `file` | un archivo: graph6 o `n u v u v …` por línea |
| `all` | todos los grafos **etiquetados** (solo pruebas chicas) |

## Observadores

`grado` (control negativo), `wl`, `kw2`, `kw3`, `ir1`, `ir2`.
El motor no incluye el observador SNF del Laplaciano (línea del
laboratorio, EXP-161); se puede sumar registrando una función en
`observers.OBSERVADORES`.

## Qué NO es

- No es el motor: la matemática vive en `graphkind` (o `graphkind-wl`).
- No mide tiempo de cómputo por observador (solo colisiones y leyes).
- No promete completitud universal: mide **en la clase** del corpus.

## Cita y licencia

Argaña Silguero, J. (2026). *GraphKind — Universes v2*. Zenodo.
<https://doi.org/10.5281/zenodo.22747350> · CC-BY-4.0.
