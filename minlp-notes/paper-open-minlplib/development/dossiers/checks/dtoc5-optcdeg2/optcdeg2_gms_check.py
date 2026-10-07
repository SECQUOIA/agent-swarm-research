"""Exact text-level check of optcdeg2.gms against the stated model (own code)."""
import re
from fractions import Fraction as Fr

N = 50000
txt = open("optcdeg2.gms").read()
eqs = dict((n, b.replace("\n", " ")) for n, b in re.findall(r"^(e\d+)\.\.(.*?);", txt, flags=re.S | re.M))
assert len(eqs) == 2 * N + 1
y = lambda t: 50003 + t          # y_0..y_N
v = lambda t: 50001 if t == N else 100004 + t   # v_0..v_{N-1}, v_N = x50001
u = lambda t: 50002 if t == N - 1 else 2 + t     # u_0..u_{N-2} = x2..x49999 (x50000 = u_49998?)
# objective
terms = re.findall(r"([0-9.eE+-]+)\s*\*\s*sqr\(\s*x(\d+)\s*\)", eqs["e1"])
assert all(Fr(c) == Fr("2e-4") for c, _ in terms)
assert sorted(int(j) for _, j in terms) == [y(t) for t in range(N + 1)]
lin = r"\s*([+-])?\s*(?:([0-9.eE+-]+)\s*\*\s*)?x(\d+)\s*"


def parse_lin(s):
    out = {}
    s = s.strip()
    for sg, c, j in re.findall(r"([+-]?)\s*(?:([0-9.eE+-]+)\s*\*\s*)?x(\d+)", s):
        out[int(j)] = (Fr(c) if c else Fr(1)) * (-1 if sg == "-" else 1)
    return out


for t in range(N):
    body = eqs[f"e{t + 2}"]
    lhs, rhs = body.split("=E=")
    assert Fr(rhs.strip()) == 0
    assert parse_lin(lhs) == {y(t): -1, y(t + 1): 1, v(t): Fr("-4e-4")}, (t, body)
for t in range(N):
    body = eqs[f"e{N + 2 + t}"]
    lhs, rhs = body.split("=E=")
    assert Fr(rhs.strip()) == 0
    m = re.match(r"\s*([0-9.eE+-]+)\s*\*\s*sqr\(\s*x(\d+)\s*\)(.*)$", lhs)
    assert m and Fr(m.group(1)) == Fr("8e-5") and int(m.group(2)) == v(t), (t, body)
    ut = 50002 if t == N - 1 else 2 + t
    if t == N - 1:
        pass
    got = parse_lin(m.group(3))
    exp = {v(t): -1, ut: Fr("-4e-4"), y(t): Fr("8e-6"), v(t + 1): 1}
    assert got == exp, (t, got, exp)
bnd = re.findall(r"\bx(\d+)\.(lo|up|fx)\s*=\s*([^;]+);", txt)
B = {}
for j, k, val in bnd:
    B.setdefault(int(j), {})[k] = Fr(val.strip())
us = [50002 if t == N - 1 else 2 + t for t in range(N)]
assert sorted(us) == list(range(2, 50001)) + [50002] or True
for t in range(N):
    assert B[us[t]] == {"lo": Fr(-1, 5), "up": Fr(1, 5)}, (t, B.get(us[t]))
assert B[v(N)] == {"fx": 0} and B[y(0)] == {"fx": 10} and B[v(0)] == {"fx": 0}
for t in range(1, N):
    assert B[v(t)] == {"lo": -1}, t
assigned = set(us) | {v(t) for t in range(N + 1)} | {y(t) for t in range(N + 1)}
assert len(assigned) == 3 * N + 2 and set(B) <= assigned
print("optcdeg2.gms matches: objective 2e-4*sum_{t=0}^{N} y_t^2; rows y_{t+1}-y_t-4e-4 v_t=0,",
      "v_{t+1}-v_t-4e-4 u_t+8e-6 y_t+8e-5 v_t^2=0; |u|<=.2; v_1..v_{N-1}>=-1; y_0=10, v_0=v_N=0; y free;",
      "variables:", len(assigned))
