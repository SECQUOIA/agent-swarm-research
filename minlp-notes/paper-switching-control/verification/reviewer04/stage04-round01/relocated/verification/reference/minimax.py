"""Exact one-switch worst-case CIA error on any rational finite grid.

Uses only standard-library rational arithmetic, O(N**2) arithmetic operations,
and constant-size compressed output. See notes/cia-reopened-finite-grid.md,
equations (2)-(7), for the formula, proof, and witness reconstruction.
"""
from fractions import Fraction as Q


def minimax(n, grid):
    """Return exact minimax and a compressed extremizer, using no LP solver.

    The witness has (a,b,family,[u1,u2,u3,v1,v2,v3,m1,m2,m3,E]);
    group 3 repeats n-2 times. All operations are exact Fraction arithmetic.
    The returned witness has at most two distinct component functions.

    n must be an integer at least 3. Grid endpoints must be int, Fraction,
    or rational strings, start at zero, and increase strictly. Floats and
    booleans are rejected rather than silently converted to rational values.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("mode count must be an integer")
    if n < 3:
        raise ValueError("mode count must be at least 3")
    endpoints = list(grid)
    if any(isinstance(t, bool) or not isinstance(t, (int, Q, str)) for t in endpoints):
        raise TypeError("grid endpoints must be int, Fraction, or rational strings")
    grid = list(map(Q, endpoints))
    if len(grid) < 2 or grid[0] != 0:
        raise ValueError("grid must contain at least two endpoints and start at zero")
    if any(a >= b for a, b in zip(grid, grid[1:])):
        raise ValueError("grid endpoints must increase strictly")
    N, T = len(grid) - 1, grid[-1]
    c = next(k for k in range(1, N + 1) if grid[k] >= T / 3)
    C = grid[c]
    best = min((T + C) / 4, (T - grid[c - 1]) / 2)
    special = max(Q(0), (C - T + 2 * best) / 2)
    bulk = min(C, T - 2 * best) / (n - 2)
    winner = (c, c, "high", [special, special, bulk, special, special,
                            bulk, best, best, (T - 2 * best) / (n - 2), best])
    for a in range(1, N + 1):
        for b in range(a, N + 1):
            A, B, P, R = grid[a], grid[b], grid[a - 1], grid[b - 1]
            if (n - 2) * (T - A) > (n - 1) * B:
                continue
            lower = max(T / 3, (n - 1) * T / n - B,
                        ((n - 1) * T - A - (n - 1) * B) / n)
            upper = min(A, ((n - 2) * A + B) / n, (n - 1) * T / n - P,
                        ((n - 1) * T - P - (n - 1) * R) / n,
                        (T - P + (n - 2) * A) / n)
            if upper < lower or upper <= best:
                continue
            best = E = upper
            M = max(T / n, T - A - E, (n - 1) * (E + R) - (n - 2) * T,
                    (n - 1) * E - (n - 2) * A)
            x = max(Q(0), (n - 1) * E - (n - 2) * A, A - T + M)
            y = max(x, B - T + M)
            u, v, m = (A - x) / (n - 1), (B - y) / (n - 1), (T - M) / (n - 1)
            winner = (a, b, "low", [x, u, u, y, v, v, M, m, m, E])
    # Validate the compact witness without numerical computation.
    a, b, family, z = winner
    u, v, m = z[:3], z[3:6], z[6:9]
    weights = (1, 1, n - 2)
    assert all(0 <= p <= q <= r for p, q, r in zip(u, v, m))
    assert sum(w * q for w, q in zip(weights, u)) == grid[a]
    assert sum(w * q for w, q in zip(weights, v)) == grid[b]
    assert sum(w * q for w, q in zip(weights, m)) == T
    assert m[0] >= m[1] >= m[2]
    assert T - grid[a] <= best + m[0] <= T - grid[a - 1]
    assert T - grid[b] <= best + m[1] <= T - grid[b - 1]
    assert u[1] + best <= grid[a] and v[0] + best <= grid[b]
    assert u[2] + best <= grid[a] if family == "low" else m[1] >= best
    assert z[9] == best
    return best, winner
