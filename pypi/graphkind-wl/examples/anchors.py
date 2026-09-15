"""Run the three canonical anchors with graphkind-wl."""
from graphkind_wl import adj_from_edges, separa

C6 = adj_from_edges(6, [(i, (i + 1) % 6) for i in range(6)])
DOS_C3 = adj_from_edges(6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)])
PETERSEN = adj_from_edges(10, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
                               (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
                               (0, 5), (1, 6), (2, 7), (3, 8), (4, 9)])
PRISMA = adj_from_edges(10, [(i, (i + 1) % 5) for i in range(5)]
                        + [(i + 5, (i + 1) % 5 + 5) for i in range(5)]
                        + [(i, i + 5) for i in range(5)])

def rook_shrikhande():
    rook = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    u, v = a * 4 + b, c * 4 + d
                    if u < v and (a == c or b == d):
                        rook.append((u, v))
    shri = []
    for i in range(4):
        for j in range(4):
            u = i * 4 + j
            for di, dj in [(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)]:
                v = ((i + di) % 4) * 4 + ((j + dj) % 4)
                if u < v:
                    shri.append((u, v))
    return adj_from_edges(16, rook), adj_from_edges(16, shri)

for nombre, (a1, a2) in {
    "C6 vs 2·C3": (C6, DOS_C3),
    "Petersen vs prisma": (PETERSEN, PRISMA),
    "Rook vs Shrikhande": rook_shrikhande(),
}.items():
    res = ["separa" if separa(a1, a2, k) else "colisiona" for k in (1, 2, 3)]
    print(f"{nombre:22s} k=1 {res[0]:9s} k=2 {res[1]:9s} k=3 {res[2]}")
