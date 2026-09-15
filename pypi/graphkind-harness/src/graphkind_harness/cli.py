"""CLI del harness: ``graphkind-harness run|anclas|reporte``."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__, bench


def _add_common(p):
    p.add_argument("--observadores", default=None,
                   help="lista separada por comas (default: todos)")
    p.add_argument("--seed", type=int, default=7)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="graphkind-harness",
        description="Benchmark de invariantes estructurales sobre universos "
                    "(GraphKind). Mide colisiones, fronteras, T4 y controles.")
    ap.add_argument("--version", action="version",
                    version=f"%(prog)s {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="corrida completa (corpus -> JSON)")
    r.add_argument("--corpus", default="geng",
                   choices=["geng", "all", "pairs", "random", "file"])
    r.add_argument("--n-max", type=int, default=7)
    r.add_argument("--n-min", type=int, default=1)
    r.add_argument("--path", default=None, help="archivo para --corpus file")
    r.add_argument("--out", default=None, help="ruta del JSON de salida")
    r.add_argument("--hipergrafo-n", type=int, default=5)
    r.add_argument("--hipergrafo-m", type=int, default=40)
    r.add_argument("--solo-json", action="store_true",
                   help="no imprimir el reporte de texto")
    _add_common(r)

    a = sub.add_parser("anclas", help="tabla de los pares canónicos")
    _add_common(a)

    rep = sub.add_parser("reporte", help="reporte de texto de un JSON")
    rep.add_argument("json_path")

    args = ap.parse_args(argv)

    if args.cmd == "run":
        res = bench.run(corpus=args.corpus, n_max=args.n_max, n_min=args.n_min,
                        observadores=args.observadores, seed=args.seed,
                        path=args.path, hipergrafo_n=args.hipergrafo_n,
                        hipergrafo_m=args.hipergrafo_m)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2, sort_keys=True)
                f.write("\n")
            print(f"JSON: {args.out}", file=sys.stderr)
        if not args.solo_json:
            print(bench.reporte(res))
        return 0

    if args.cmd == "anclas":
        from .observers import observadores
        obs = observadores(args.observadores)
        filas = bench.anclas(obs)
        cab = ["par", "n"] + list(obs)
        print("  ".join(c.ljust(10) for c in cab))
        for f in filas:
            print("  ".join(str(f[c]).ljust(10)
                            for c in cab))
        return 0

    if args.cmd == "reporte":
        with open(args.json_path, encoding="utf-8") as f:
            print(bench.reporte(json.load(f)))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
