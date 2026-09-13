"""Universos de observación: la ley de T4 y su certificación.

Resultado del ciclo EXP-099..107 (validado 102/102 en EXP-105 y
re-validado en EXP-107):

    LEY:  T4(ι, f) VIVE  ⟺  ι es TRIVIAL  ∨  (ι es DUAL ∧ f(1) ≠ f(2))

donde:
  - f: N→N  comprime los conteos de vecinos por color en el refinamiento;
  - ι: una involución G→G (complemento, relabel, …);
  - TRIVIAL: g = identidad (relabels: el conteo no cambia);
  - DUAL: existen σ y g (inyectiva, g≠id) que transportan los conteos
    de la vecindad (el complemento);
  - LOCAL: no existe tal (σ, g) (cambios locales de aristas).

PODER:
  1. PREDECIR sin enumerar: dado un universo (f, ι) nuevo, el oráculo
     dice si T4 valdrá, sin correr millones de grafos.
  2. DISEÑAR representaciones seguras: la ley dice qué compresiones de
     conteo preservan la dualidad (f(1)≠f(2)) y cuáles la rompen.
  3. CERTIFICAR: si un universo con (dual, f(1)≠f(2)) falla el test,
     es un BUG del código, no matemática.
  4. HABILITAR el truco del lado ralo (refine_dual) solo donde T4 vive.
"""


def t4_garantizado(f1, f2, clase: str) -> bool:
    """La ley pura: ¿el universo admite T4 según su clase y f(1), f(2)?

    >>> t4_garantizado(1, 2, "dual")       # f distingue 1 de 2
    True
    >>> t4_garantizado(1, 1, "dual")       # colapsa 1 y 2
    False
    >>> t4_garantizado(1, 1, "trivial")    # los relabels viven siempre
    True
    >>> t4_garantizado(0, 1, "local")      # ninguna f la salva
    False
    """
    if clase == "trivial":
        return True
    if clase == "dual":
        return f1 != f2
    return False  # local


def _clases(labels):
    from collections import defaultdict
    by = defaultdict(set)
    for v, c in enumerate(labels):
        by[c].add(v)
    return by


def clasificar_involucion(n: int, adj, iota, sigma=None, f=None) -> str:
    """Clasifica ι sobre UN grafo: "trivial" | "dual" | "local".

    adj: lista de bitmasks (vecindad de cada vértice).
    iota: función (n, adj) -> adj' (la involución).
    sigma: biyección V→V declarada (default: identidad).
    f: la compresión de conteos usada para el refinamiento (default: id).

    Aplica la definición formal: matching de clases inducido por σ,
    conteos (m, m') por (clase, vértice), y g bien definida + inyectiva.
    """
    from collections import Counter, defaultdict
    import hashlib

    def h(s):
        return hashlib.sha256(s.encode()).hexdigest()[:12]

    if f is None:
        f = lambda k: k  # noqa: E731
    if sigma is None:
        sigma = lambda v: v  # noqa: E731

    def wl_labels(a):
        colors = [h(f"g|{a[v].bit_count()}") for v in range(n)]
        for _ in range(n + 2):
            new = []
            for v in range(n):
                cnt = Counter()
                m = a[v]
                while m:
                    u = (m & -m).bit_length() - 1
                    m &= m - 1
                    cnt[colors[u]] += 1
                new.append(h(f"{colors[v]}|"
                             f"{tuple(sorted((c, f(k)) for c, k in cnt.items()))}"))
            colors = new
        return colors

    ig = iota(n, adj)
    lg = wl_labels(adj)
    li = wl_labels(ig)
    by_g = _clases(lg)
    match = {}
    for c, vs in by_g.items():
        imgs = {li[sigma(v)] for v in vs}
        if len(imgs) != 1:
            return "local"
        match[c] = imgs.pop()

    vistos_def = {}
    vistos_iny = {}
    g_id = True
    for c, vs in by_g.items():
        ci_label = match[c]
        ci = {u for u, cc in enumerate(li) if cc == ci_label}
        for v in range(n):
            sv = sigma(v)
            m = sum(1 for u in vs if (adj[sv] >> u) & 1)
            mp = sum(1 for u in ci if (ig[v] >> u) & 1)
            venc = 1 if sv in vs else 0
            key = (len(vs), venc, m)
            key2 = (len(vs), venc, mp)
            if key in vistos_def and vistos_def[key] != mp:
                return "local"
            vistos_def[key] = mp
            if key2 in vistos_iny and vistos_iny[key2] != m:
                return "local"
            vistos_iny[key2] = m
            if mp != m:
                g_id = False
    return "trivial" if g_id else "dual"


def oraculo(n: int, adj, iota, f, f1, f2, sigma=None) -> dict:
    """Predice T4 para un universo (f, ι) SIN enumerar grafos.

    Devuelve {"clase", "f1", "f2", "t4_predicho"}.
    """
    clase = clasificar_involucion(n, adj, iota, sigma=sigma, f=f)
    return {"clase": clase, "f1": f1, "f2": f2,
            "t4_predicho": t4_garantizado(f1, f2, clase)}
