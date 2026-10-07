"""Compare the data of MINLPLib powerflow0030p and powerflow0039p/r with the MATPOWER
case files case30.m and case39.m (downloaded to ../sources/).

Checks (multiset comparisons, no variable mapping):
  * generator cost coefficients (per unit: c2*100^2, c1*100, constant c0 summed);
  * single-variable bound rows of the GAMS model versus bus voltage limits and
    generator P/Q limits (MW/MVAr divided by 100);
  * thermal-limit rows  sqr(.) + sqr(.) =L= s^2  versus rateA (s = rateA/100);
  * transformer branches (ratio != 0): does the series admittance appear untapped
    (g, b) or tapped (g/tau^2, b/tau^2, g/tau, b/tau) among the GAMS coefficients?
    Coefficients are matched to 1e-9 relative.

    python3 powerflow_data_match.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import re
from collections import Counter

SRC = (_PUBLIC_REPO + '/research-20260929/publication/literature/network/sources/')


def mp_table(path, name):
    t = open(path).read()
    m = re.search(r"mpc\.%s\s*=\s*\[(.*?)\];" % name, t, flags=re.S)
    rows = []
    for line in m.group(1).splitlines():
        line = line.split("%")[0].strip().rstrip(";")
        if line:
            rows.append([float(v) for v in line.split()])
    return rows


def gams_rows(path):
    t = open(path).read()
    return [(n, " ".join(b.split())) for n, b in re.findall(r"^(e\d+)\.\.(.*?);", t, flags=re.S | re.M)]


def coefs(rows):
    out = []
    for _, b in rows:
        out += [float(c) for c in re.findall(r"(?<![x\w.])(\d+\.\d+|\d+)(?=\*)", b)]
    return out


def near(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def check(case, gms_files):
    print(f"===== MATPOWER {case} vs {', '.join(gms_files)}")
    bus = mp_table(SRC + f"matpower_{case}.m", "bus")
    gen = mp_table(SRC + f"matpower_{case}.m", "gen")
    br = mp_table(SRC + f"matpower_{case}.m", "branch")
    gc = mp_table(SRC + f"matpower_{case}.m", "gencost")
    for g in gms_files:
        rows = gams_rows(SRC + g)
        obj = rows[0][1].replace(" ", "")
        # costs
        q = sorted(float(c) for c in re.findall(r"([\d.]+)\*sqr\(x\d+\)", obj))
        lin = sorted(float(c) for c in re.findall(r"(?:^|\+)([\d.]+)\*x\d+", obj))
        const = re.search(r"=E=([-\d.]+)$", obj)
        mq = sorted(r[4] * 1e4 for r in gc)
        ml = sorted(r[5] * 1e2 for r in gc)
        mc = sum(r[6] for r in gc)
        print(f"{g}: quadratic cost coefs match: {len(q) == len(mq) and all(near(a, b) for a, b in zip(q, mq))};"
              f" linear: {len(lin) == len(ml) and all(near(a, b) for a, b in zip(lin, ml))};"
              f" objective constant {(-float(const.group(1))) if const else 0.0} vs MATPOWER sum c0 {mc}")
        # single-variable bounds
        single = Counter()
        for _, b in rows:
            m = re.fullmatch(r"(x\d+) =([LG])= ([-+]?[\d.eE+-]+)", b)
            if m:
                single[(m.group(2), round(float(m.group(3)), 9))] += 1
        exp = Counter()
        if g.endswith("p.gms"):
            for r in bus:
                exp[("L", round(r[11], 9))] += 1
                exp[("G", round(r[12], 9))] += 1
        for r in gen:
            exp[("L", round(r[8] / 100, 9))] += 1   # Pmax
            exp[("G", round(r[9] / 100, 9))] += 1   # Pmin
            exp[("L", round(r[3] / 100, 9))] += 1   # Qmax
            exp[("G", round(r[4] / 100, 9))] += 1   # Qmin
        missing = exp - single
        print(f"  bound rows: every MATPOWER voltage/generator limit present as a single-variable row: {not missing}"
              + ("" if not missing else f" (missing {dict(missing)})"))
        if g.endswith("r.gms"):
            vr = Counter()
            for _, b in rows:
                m = re.fullmatch(r"sqr\(x\d+\) \+ sqr\(x\d+\) =([LG])= ([\d.eE+-]+)", b)
                if m:
                    vr[(m.group(1), round(float(m.group(2)), 9))] += 1
            ve = Counter()
            for r in bus:
                ve[("L", round(r[11] ** 2, 9))] += 1
                ve[("G", round(r[12] ** 2, 9))] += 1
            th = Counter({k: v for k, v in vr.items() if k not in ve})
            print(f"  rectangular voltage rows match (V^2 bounds): {not (ve - vr)}")
        # thermal limits
        thr = Counter()
        for _, b in rows:
            m = re.fullmatch(r"sqr\(x\d+\) \+ sqr\(x\d+\) =L= ([\d.eE+-]+)", b)
            if m:
                thr[round(float(m.group(1)), 9)] += 1
        the = Counter()
        for r in br:
            if r[5] > 0:
                the[round((r[5] / 100) ** 2, 9)] += 2  # both ends
        if g.endswith("r.gms"):
            for r in bus:
                the[round(r[11] ** 2, 9)] += 1
        print(f"  thermal-limit rows (rateA, both ends) match as multisets: {thr == the}")
        # transformers
        cs = coefs(rows)
        ntr = 0
        res = Counter()
        for r in br:
            tau = r[8]
            if tau == 0:
                continue
            ntr += 1
            z2 = r[2] ** 2 + r[3] ** 2
            gg, bb = r[2] / z2, r[3] / z2
            ref = bb if bb != 0 else gg
            untapped = any(near(c, ref) for c in cs)
            tapped = any(near(c, ref / tau ** 2) or near(c, ref / tau) for c in cs) if tau != 1 else None
            res[(untapped, tapped)] += 1
        print(f"  transformer branches with ratio != 0: {ntr}; (untapped coef found, tapped coef found) -> {dict(res)}")
        # line charging: the reactive-flow coefficient of v_from^2 is b_s - b_c/2 (b_s = x/(r^2+x^2))
        chg = Counter()
        for r in br:
            if r[4] == 0:
                continue
            z2 = r[2] ** 2 + r[3] ** 2
            chg[any(near(c, r[3] / z2 - r[4] / 2) for c in cs)] += 1
        print(f"  branches with line charging b_c != 0: {sum(chg.values())}; coefficient b_s - b_c/2 found: {dict(chg)}")


check("case30", ["minlplib_powerflow0030p.gms"])
check("case39", ["minlplib_powerflow0039p.gms", "minlplib_powerflow0039r.gms"])
