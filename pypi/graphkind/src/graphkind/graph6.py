"""graph6 (formato simple, n ≤ 62): parseo y emisión — stdlib.

`from_graph6(s) -> (n, edges)` y `to_graph6(n, edges) -> str`, con
round-trip garantizado (testeado). El formato simple codifica `n` y los
bits del triángulo superior, 6 bits por carácter (valor + 63).
"""

from __future__ import annotations


def from_graph6(s: str) -> tuple[int, list[tuple[int, int]]]:
    """graph6 -> (n, lista de aristas)."""
    data = [ord(c) - 63 for c in s.strip()]
    if not data:
        raise ValueError("graph6 vacío")
    if data[0] < 0 or data[0] > 62:
        raise ValueError("solo se soporta el formato simple (n <= 62)")
    n = data[0]
    bits = []
    for x in data[1:]:
        for i in range(5, -1, -1):
            bits.append((x >> i) & 1)
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if k < len(bits) and bits[k]:
                edges.append((i, j))
            k += 1
    return n, edges


def to_graph6(n: int, edges) -> str:
    """(n, aristas) -> graph6 (formato simple)."""
    if not (0 <= n <= 62):
        raise ValueError("solo se soporta el formato simple (n <= 62)")
    E = {tuple(sorted(e)) for e in edges}
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if (i, j) in E else 0)
    out = chr(63 + n)
    for k in range(0, len(bits), 6):
        grupo = bits[k:k + 6] + [0] * (6 - len(bits[k:k + 6]))
        v = 0
        for b in grupo:
            v = (v << 1) | b
        out += chr(63 + v)
    return out
