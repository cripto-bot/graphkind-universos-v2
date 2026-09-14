#!/usr/bin/env python3
"""Subida a Zenodo por API REST — sin dependencias (usa curl).

Uso:
  python tools/zenodo_submit.py status <id>
  python tools/zenodo_submit.py create --title "..." [--out dep.json]
  python tools/zenodo_submit.py upload <id> archivo.zip
  python tools/zenodo_submit.py metadata <id> metadata.json
  python tools/zenodo_submit.py publish <id>

Token: `ZENODO_TOKEN` en el entorno, o `--token-file` (default
~/.config/zenodo/token). NUNCA commitear el token.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

API = "https://zenodo.org/api"


def get_token(args):
    if args.token_file:
        return Path(args.token_file).read_text().strip()
    t = os.environ.get("ZENODO_TOKEN")
    if t:
        return t
    p = Path.home() / ".config" / "zenodo" / "token"
    if p.exists():
        return p.read_text().strip()
    sys.exit("falta ZENODO_TOKEN (env o --token-file)")


def curl_json(token, method, url, body=None, retries=4):
    cmd = ["curl", "-s", "--max-time", "300", "-X", method,
           "-H", f"Authorization: Bearer {token}"]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json",
                "--data-binary", json.dumps(body)]
    cmd.append(url)
    last = ""
    for _ in range(retries):
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = r.stdout.strip()
        if out[:1] in ("{", "["):
            return json.loads(out)
        last = out[:200]
        time.sleep(4)
    sys.exit(f"fallo tras {retries} intentos: {last}")


def subir_archivo(token, dep_id, ruta, retries=4):
    url = f"{API}/deposit/depositions/{dep_id}/files"
    cmd = ["curl", "-s", "--max-time", "600", "-X", "POST",
           "-H", f"Authorization: Bearer {token}",
           "-F", f"name={Path(ruta).name}", "-F", f"file=@{ruta}", url]
    last = ""
    for _ in range(retries):
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = r.stdout.strip()
        if out[:1] == "{":
            d = json.loads(out)
            if d.get("filename"):
                return d
        last = out[:200]
        time.sleep(5)
    sys.exit(f"fallo la subida tras {retries} intentos: {last}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "create", "upload", "metadata",
                                    "publish"])
    ap.add_argument("id", nargs="?")
    ap.add_argument("extra", nargs="?")
    ap.add_argument("--title")
    ap.add_argument("--out", default="dep.json")
    ap.add_argument("--token-file")
    args = ap.parse_args()
    tok = get_token(args)

    if args.cmd == "status":
        d = curl_json(tok, "GET", f"{API}/deposit/depositions/{args.id}")
        print(json.dumps({"id": d.get("id"), "state": d.get("state"),
                          "title": d.get("title"),
                          "doi": (d.get("metadata", {})
                                  .get("prereserve_doi", {}).get("doi")
                                  or d.get("doi")),
                          "files": [(f.get("filename"), f.get("filesize"))
                                    for f in d.get("files", [])]},
                         indent=1, ensure_ascii=False))
    elif args.cmd == "create":
        d = curl_json(tok, "POST", f"{API}/deposit/depositions",
                      {"metadata": {"title": args.title,
                                    "prereserve_doi": True}})
        Path(args.out).write_text(json.dumps(d, indent=1))
        print(f"id={d['id']} DOI reservado="
              f"{d['metadata']['prereserve_doi']['doi']}")
    elif args.cmd == "upload":
        d = subir_archivo(tok, args.id, args.extra)
        print(f"subido: {d['filename']} {int(d['filesize'])} bytes "
              f"checksum {d['checksum']}")
    elif args.cmd == "metadata":
        d = curl_json(tok, "PUT", f"{API}/deposit/depositions/{args.id}",
                      json.loads(Path(args.extra).read_text()))
        print(f"metadata OK: {d['metadata']['title']}")
    elif args.cmd == "publish":
        d = curl_json(tok, "POST",
                      f"{API}/deposit/depositions/{args.id}/actions/publish")
        print(f"PUBLICADO: {d.get('doi')} | {d.get('links',{}).get('html')}")


if __name__ == "__main__":
    main()
