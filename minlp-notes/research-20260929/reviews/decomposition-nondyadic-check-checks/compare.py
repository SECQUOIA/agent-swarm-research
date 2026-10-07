"""Compare the full-precision root bounds of the four pairing modes (logs written by run_all.sh).

  python3 compare.py      prints, per certificate: pairs dropped by the rounded closed test, pairs
                          with positive overlap missing from it (open minus closed), tol != exact,
                          l_r(closed) - l_r(exact), l_r(tol) - l_r(exact), l_r(open) - l_r(exact),
                          and whether l_r(open) <= f* (f* read from the run's own printout)
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MODES = ("closed", "tol", "exact", "open")
LINE = re.compile(r"^# (n=\d+ h=2\^-?\d+ theta=2\^-\d+ \w+)\s*: (.*)$")


def read(exp, mode):
    """Stat lines in order (keys may repeat across runs of E3, so keep a list)."""
    out = []
    for s in open(os.path.join(HERE, "logs", "%s_%s.log" % (exp, mode))):
        m = LINE.match(s)
        if m:
            f = [x.strip() for x in m.group(2).split("|")]
            g = f[1].split()
            out.append((m.group(1), "%s %s %s" % (g[1], g[3], g[2]), float(f[-1])))
    return out


def fstars(exp):
    """f* per certificate, in the order of the stat lines."""
    txt = open(os.path.join(HERE, "logs", "%s_exact.log" % exp)).read()
    if exp == "E3":
        return [float(v) for v in re.findall(r"f\*=(-?[\d.]+)", txt)]
    if exp == "E2":
        return [float(re.search(r"f\* = (-?[\d.]+)", txt).group(1))] * 16
    return None


for exp in ("E3", "E2", "E4m5", "E1x0"):
    rows = {m: read(exp, m) for m in MODES}
    fs = fstars(exp)
    print("## %s" % exp)
    print("# certificate | exact\\closed, open\\closed, tol!=exact | closed-exact | tol-exact | open-exact | open <= f*")
    for i, (key, dropped, rex) in enumerate(rows["exact"]):
        rc, rt, ro = rows["closed"][i][2], rows["tol"][i][2], rows["open"][i][2]
        assert rows["closed"][i][0] == key and rows["tol"][i][0] == key and rows["open"][i][0] == key
        ok = "" if fs is None else str(ro <= fs[i] + 1e-12)
        print("%-34s %12s %+.3e %+.3e %+.3e %s" % (key, dropped, rc - rex, rt - rex, ro - rex, ok))
