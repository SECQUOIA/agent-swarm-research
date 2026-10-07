"""Compare the bus loads (Pd, Qd) and bus shunts (Gs, Bs) of MATPOWER case30/case39 with the
power-balance rows of MINLPLib powerflow0030p, powerflow0039p and powerflow0039r.

This extends powerflow_data_match.py, which did not compare loads or shunts (review round 1, M2).

Method (exact rational arithmetic on the decimal strings of both files):
  * The last 2*nbus rows of each GAMS model are the balance rows, in four blocks: active rows of
    the generator buses (gen-table order), reactive rows of the generator buses, active rows of
    the other buses (increasing bus number), reactive rows of the other buses. The script
    asserts this layout: generator-bus rows contain exactly one variable with coefficient -1
    (the generator injection; for active rows it must be a cost variable of the objective),
    all other terms have coefficient +1.
  * Each row's right-hand side must equal -Pd/baseMVA (active) or -Qd/baseMVA (reactive) of the
    bus assigned to it. The same comparison is also made as an order-free multiset.
  * Shunts: a bus shunt contributes Gs/baseMVA * V^2 (active) and -Bs/baseMVA * V^2 (reactive)
    to the bus balance. The script reports whether any balance row contains a nonlinear term,
    and whether the numbers Gs/baseMVA or Bs/baseMVA occur anywhere in the GAMS file. To rule out
    a shunt folded into a branch-flow row, it also checks (case30 only) that every coefficient of
    a sqr(x) term in the branch-flow rows equals a pure branch quantity g, b or b - b_c/2 of
    some MATPOWER branch (g + j b = 1/(r + j x); relative tolerance 1e-12, because the GAMS
    file prints 15 significant digits).

    python3 powerflow_loads_shunts.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import re
from collections import Counter
from fractions import Fraction as F

SRC = (_PUBLIC_REPO + '/research-20260929/publication/literature/network/sources/')


def mp_table(text, name):
    m = re.search(r"mpc\.%s\s*=\s*\[(.*?)\];" % name, text, flags=re.S)
    rows = []
    for line in m.group(1).splitlines():
        line = line.split("%")[0].strip().rstrip(";")
        if line:
            rows.append(line.split())
    return rows


def gams_rows(text):
    return [(n, " ".join(b.split())) for n, b in re.findall(r"^(e\d+)\.\.(.*?);", text, flags=re.S | re.M)]


def parse_linear(body):
    """Return ({var: coef}, rhs) for a row 'sum of +-[c*]x =E= rhs'; None if any term is nonlinear."""
    lhs, rhs = body.split("=E=")
    terms = {}
    for sign, coef, var in re.findall(r"([+-]?)\s*(?:([\d.]+)\*)?(x\d+)(?![\w(])", lhs):
        terms[var] = (F(coef) if coef else F(1)) * (-1 if sign == "-" else 1)
    rebuilt = re.sub(r"([+-]?)\s*(?:([\d.]+)\*)?(x\d+)(?![\w(])", "", lhs).strip()
    if rebuilt:  # anything left over (sqr, *, sin, cos, ...) is a nonlinear term
        return None
    return terms, F(rhs.strip())


def check(case, gms):
    mtext = open(SRC + f"matpower_{case}.m").read()
    base = F(re.search(r"mpc\.baseMVA\s*=\s*([\d.]+)", mtext).group(1))
    bus = mp_table(mtext, "bus")
    gen = mp_table(mtext, "gen")
    nb = len(bus)
    pd = {int(r[0]): F(r[2]) / base for r in bus}
    qd = {int(r[0]): F(r[3]) / base for r in bus}
    gs = {int(r[0]): F(r[4]) / base for r in bus}
    bs = {int(r[0]): F(r[5]) / base for r in bus}
    genbus = []
    for r in gen:
        if int(r[0]) not in genbus:
            genbus.append(int(r[0]))
    others = sorted(b for b in pd if b not in genbus)
    ng, no = len(genbus), len(others)

    def idx(kind, b):  # position of the balance row of bus b within the last 2*nbus rows
        if b in genbus:
            return genbus.index(b) + (ng if kind == "Q" else 0)
        return 2 * ng + others.index(b) + (no if kind == "Q" else 0)

    text = open(SRC + gms).read()
    rows = gams_rows(text)
    obj_vars = set(re.findall(r"x\d+", rows[0][1]))
    bal = rows[-2 * nb:]
    print(f"===== MATPOWER {case} vs {gms}: balance rows {bal[0][0]}..{bal[-1][0]}")
    nonlin = [n for n, b in bal if parse_linear(b) is None]
    print(f"  balance rows with a nonlinear (e.g. V^2 shunt) term: {len(nonlin)} {nonlin}")
    layout_ok, load_mismatch = True, []
    for load, kind in [(pd, "P"), (qd, "Q")]:
        for b in pd:
            name, body = bal[idx(kind, b)]
            terms, rhs = parse_linear(body)
            neg = [v for v, c in terms.items() if c == -1]
            pos = [v for v, c in terms.items() if c == 1]
            if len(neg) + len(pos) != len(terms):
                layout_ok = False
            if b in genbus:
                if len(neg) != 1 or (kind == "P" and neg[0] not in obj_vars):
                    layout_ok = False
            elif neg:
                layout_ok = False
            if rhs != -load[b]:
                load_mismatch.append((kind, b, name, rhs, -load[b]))
    print(f"  row layout (blocks P-gen, Q-gen, P-other, Q-other; one -1 generator variable per gen-bus row; P generator variables are cost variables): {layout_ok}")
    print(f"  loads matched row by row (exact): {not load_mismatch}" + ("" if not load_mismatch else f" mismatches {load_mismatch}"))
    rhs_all = Counter(parse_linear(b)[1] for _, b in bal)
    exp_all = Counter([-v for v in pd.values()] + [-v for v in qd.values()])
    print(f"  loads matched as an order-free multiset (exact): {rhs_all == exp_all}")
    nums = Counter(F(s) for s in re.findall(r"(?<![\w.])(\d+\.\d+|\d+)(?![\w.])", text.split("Equations", 1)[1]))
    sh = [(b, gs[b], bs[b]) for b in sorted(pd) if gs[b] != 0 or bs[b] != 0]
    print(f"  MATPOWER buses with a shunt: {len(sh)}")
    for b, g, s in sh:
        ip, iq = idx("P", b), idx("Q", b)
        print(f"    bus {b}: Gs/base = {g}, Bs/base = {s} (= {float(s)}); "
              f"P row {bal[ip][0]}: '{bal[ip][1]}'; Q row {bal[iq][0]}: '{bal[iq][1]}'; "
              f"number Bs/base occurs anywhere in the GAMS file: {nums[s] > 0}"
              + (f"; number Gs/base occurs: {nums[g] > 0}" if g != 0 else ""))


    if case == "case30":
        br = mp_table(mtext, "branch")
        allowed = []
        for r in br:
            rr, xx, bc = F(r[2]), F(r[3]), F(r[4])
            z2 = rr * rr + xx * xx
            allowed += [rr / z2, xx / z2, xx / z2 - bc / 2]
        flow = [b for _, b in rows[1:] if ("cos(" in b or "sin(" in b)]
        coefs = [F(c) for b in flow for c in re.findall(r"([\d.]+)\*sqr\(x\d+\)", b)]
        bad = sorted({c for c in coefs if not any(abs(c - a) <= F(1, 10**12) * a for a in allowed if a)})
        print(f"  branch-flow rows: {len(flow)}; sqr(x) coefficients: {len(coefs)}; all equal a pure branch "
              f"quantity g, b or b - b_c/2: {not bad}" + ("" if not bad else f" (unexplained: {[float(c) for c in bad]})"))


check("case30", "minlplib_powerflow0030p.gms")
check("case39", "minlplib_powerflow0039p.gms")
check("case39", "minlplib_powerflow0039r.gms")
