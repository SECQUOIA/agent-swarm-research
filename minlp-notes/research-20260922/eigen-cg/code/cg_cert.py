"""Exact certificates that a BQP_6 facet a.z + c >= 0 is a Chvatal-Gomory cut of
K = {z >= 0 : M(z) PSD}: find rational S PSD and N >= 0 with
    a.z + S_00 = <S, M(z)> + N.z   identically in z,   and  S_00 < -c + 1.
Then a.z >= -S_00 on K, and CG rounding gives a.z >= ceil(-S_00) = -c."""
import numpy as np
import cvxpy as cp
from fractions import Fraction as Fr
from bh import pairs
from facets import F13, F14, F15, parse
from verify import ldl


def margin_sdp(n, a, c, eps):
    """Find S >= eps*I, N >= eps (componentwise), S_00 <= c + 1 - eps."""
    P = pairs(n)
    S = cp.Variable((n + 1, n + 1), symmetric=True)
    cons = [S - eps * np.eye(n + 1) >> 0, S[0, 0] <= c + 1 - eps]
    for i in range(n):
        cons += [a[i] - 2 * S[0, i + 1] - S[i + 1, i + 1] >= eps]
    for k, (i, j) in enumerate(P):
        cons += [a[n + k] - 2 * S[i + 1, j + 1] >= eps]
    pr = cp.Problem(cp.Minimize(S[0, 0]), cons)
    pr.solve(solver=cp.CLARABEL)
    return S.value, pr.status


def exact_certificate(n, a, c, eps=0.01, den=10 ** 6):
    S, status = margin_sdp(n, a, c, eps)
    if S is None:
        return dict(status=status), None
    P = pairs(n)
    Sr = [[Fr(round(S[min(i, j), max(i, j)] * den), den) for j in range(n + 1)] for i in range(n + 1)]
    Nx = [a[i] - 2 * Sr[0][i + 1] - Sr[i + 1][i + 1] for i in range(n)]
    NX = [a[n + k] - 2 * Sr[i + 1][j + 1] for k, (i, j) in enumerate(P)]
    try:
        ldl(Sr)
        pd = True
    except ValueError:
        pd = False
    ok = pd and all(t >= 0 for t in Nx + NX) and Sr[0][0] < c + 1
    return dict(status=status, S00=Sr[0][0], S_pd=pd, minN=min(Nx + NX), certified=ok), Sr


if __name__ == "__main__":
    import json
    out = {}
    for name, s in (("(13)", F13), ("(14)", F14), ("(15)", F15)):
        a, c = parse(s)
        info, Sr = exact_certificate(6, a, c)
        print(name, info)
        if info.get("certified"):
            out[name] = [[str(t) for t in row] for row in Sr]
    json.dump(out, open("cg_certificates.json", "w"), indent=1)
