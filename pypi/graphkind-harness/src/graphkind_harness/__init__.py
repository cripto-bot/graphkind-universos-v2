"""GraphKind harness — benchmark de invariantes sobre universos.

Mide colisiones y fronteras (corpus no isomorfos × observadores), T4 por
universo (estándar, multicapa, hipergrafo), la tabla de anclas y los
controles (relabeling + control negativo), y congela todo en un JSON.

Uso como librería::

    from graphkind_harness import bench
    res = bench.run(corpus="geng", n_max=7)
    print(bench.reporte(res))

Uso por CLI::

    graphkind-harness run --corpus geng --n-max 7 --out freeze.json
"""

from . import bench, corpus, observers  # noqa: F401

__version__ = "0.1.1"
DOI = "10.5281/zenodo.22747350"

__all__ = ["DOI", "__version__", "bench", "corpus", "observers"]
