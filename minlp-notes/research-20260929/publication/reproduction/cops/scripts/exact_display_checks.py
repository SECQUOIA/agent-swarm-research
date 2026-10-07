"""Exact (rational) checks of the displayed certified numbers for chain/catmix, using the
reproduced outputs. Every certified bound below is a binary double d that a branch and bound
proved to be <= the optimum; its exact value is Fraction(d). A displayed decimal s is itself
a valid lower bound only if Fraction(s) <= Fraction(d). Also recomputes the gaps between the
exact primal enclosures (upper ends) and the bounds. Uses only fractions.Fraction.
usage: python3 exact_display_checks.py   (writes ../logs/exact_display_checks.json)
"""
import json
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "..", "logs")
WT = os.path.abspath(os.path.join(HERE, "../../../.."))


def objs(path):
    """all JSON objects printed in a log file"""
    s, out, dec, i = open(path).read(), [], json.JSONDecoder(), 0
    while True:
        j = s.find("{", i)
        if j < 0:
            return out
        try:
            o, k = dec.raw_decode(s[j:])
            out.append(o)
            i = j + k
        except ValueError:
            i = j + 1


def sci(x):
    return "%.3e" % float(x)


def trunc_down(q, digits):
    """decimal string with `digits` significant digits, rounded toward -infinity (so <= q)"""
    a, e = abs(q), 0
    while a >= 10:
        a /= 10
        e += 1
    while a < 1:
        a *= 10
        e -= 1
    k = digits - 1 - e                      # decimal places
    n = q * 10 ** k
    m = n.numerator // n.denominator        # floor
    sgn = "-" if m < 0 else ""
    m = abs(m)
    txt = str(m).rjust(k + 1, "0")
    out = sgn + txt[:-k] + "." + txt[-k:] if k > 0 else sgn + str(m)
    assert F(out) <= q
    return out


rows = []


def check(instance, source, d, display, primal_hi=None, primal_label=None):
    dq = F(d)
    sq = F(display)
    r = dict(instance=instance, source=source, certified_double=repr(d),
             display=display, display_valid=(sq <= dq), display_minus_double=sci(sq - dq),
             safe_display_17sig=None)
    # 40-decimal exact expansion of the double
    n = (dq * 10 ** 40)
    r["double_exact_40dp_floor"] = str((n.numerator // n.denominator)) + "e-40"
    r["safe_display_17sig"] = trunc_down(dq, 17)
    if primal_hi is not None:
        ph = F(primal_hi)
        r.update(primal_label=primal_label, primal_hi=primal_hi,
                 gap_vs_double=sci(ph - dq), gap_vs_display=sci(ph - sq),
                 rel_gap_vs_double=sci((ph - dq) / abs(dq)))
    rows.append(r)
    print(json.dumps(r))


# chain: author bound (chain_bound.py), verifier bound (v_chain_bnb.py), exact primal (verify_points.py)
ver = {o["instance"]: o for o in objs(os.path.join(LOGS, "p_chain_verify.log"))}
disp = {50: "5.072261493982863", 100: "5.0697846107387505", 200: "5.068917341793162", 400: "5.068621694604009"}
for N in (50, 100, 200, 400):
    a = json.load(open(os.path.join(WT, "open-instances-wave2/cops/logs/chain%d_bound.json" % N)))
    v = objs(os.path.join(LOGS, "v_chain_bnb_%d.log" % N))[0]
    assert a["bnb"]["unresolved"] == 0 and v["unresolved"] == 0
    ph = ver["chain%d" % N]["objective_hi"]
    check("chain%d" % N, "author chain_bound.py bnb.bound", a["bnb"]["bound"], disp[N], ph, "exact point, verify_points.py objective_hi")
    lo = v["min_leaf_lb"].strip("[]").split(",")[0].strip()
    print("  chain%d verifier min_leaf_lb %s >= target double: %s" % (N, lo, F(lo) >= F(v["target"])))
    check("chain%d" % N, "verifier v_chain_bnb.py certified_bound", v["certified_bound"], disp[N], ph, "exact point")
# chain: the truncated displays suggested by primal-chain-r1 (rev_gap_vs_display.log)
for N, s in ((50, "5.0722614939828627"), (100, "5.0697846107387505"), (200, "5.0689173417931616"), (400, "5.068621694604009")):
    a = json.load(open(os.path.join(WT, "open-instances-wave2/cops/logs/chain%d_bound.json" % N)))
    check("chain%d" % N, "suggested truncated display (primal-chain review)", a["bnb"]["bound"], s,
          ver["chain%d" % N]["objective_hi"], "exact point")

# catmix: author bounds (catmix_bound.py), verifier bounds (v_catmix_dp.py, recheck_dp.py)
cdisp = {100: "-0.048069432038882705", 200: "-0.04805914560067171", 400: "-0.048056547950296354", 800: "-0.048055901841076894"}
cprim = {}
for N in (100, 200, 400, 800):
    p = json.load(open(os.path.join(WT, "open-instances-wave2/cops/logs/catmix%d_primal.json" % N)))
    cprim[N] = p["exact_point_objective_enclosure"][1].strip("[]").split(",")[0].strip()
snap = json.load(open(os.path.join(WT, "open-instances-wave2/cops/logs/catmix800_primal_snap.json")))
cprim[800] = snap["exact_point_objective_enclosure"][1].strip("[]").split(",")[0].strip()
for N in (100, 200, 400, 800):
    a = json.load(open(os.path.join(WT, "open-instances-wave2/cops/logs/catmix%d_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json" % N)))
    check("catmix%d" % N, "author catmix_bound.py dual_bound", a["dual_bound"], cdisp[N], cprim[N], "authors' exact point (upper end of 60-digit enclosure)")
vb = {100: ("v_catmix_dp_100_cfgB.log", "-0.04806943203114456"), 200: ("v_catmix_dp_200_cfgA.log", "-0.04805914559907277"),
      400: ("v_recheck_dp_400_final.log", "-0.04805654782467129"), 800: ("v_recheck_dp_800_final.log", "-0.04805590147967565")}
# best exactly feasible primals named in the reviews: Newton point (catmix100), DP policy point (catmix800)
newton100 = "-0.048069432030979596104"   # v_catmix_newton.py: exact J of the final double controls (rounded to 21 digits)
for N, (log, s) in vb.items():
    o = [x for x in objs(os.path.join(LOGS, log)) if "dual_bound" in x][0]
    ph, lab = cprim[N], "authors' exact point"
    if N == 100:
        ph, lab = newton100, "reviewer Newton point (printed to 20 digits; evidence for the 1.65e-13 bracket)"
    if N == 800:
        pe = open(os.path.join(LOGS, "v_recheck_policy_exact_800.log")).read().split("(floor) = ")[1].split()[0]
        ph, lab = str(F(int(pe) + 1, 10 ** 30)), "reviewer DP-policy point (policy_exact.py, floor(J*1e30)+1)"
    check("catmix%d" % N, "verifier dual_bound (%s)" % log, o["dual_bound"], s, ph, lab)
# the summary's outward-rounded range ends
for inst, d_src, s in (("catmix100", cdisp[100], "-0.04806944"), ("catmix800", cdisp[800], "-0.04805591"),
                       ("chain400", disp[400], "5.06862"), ("chain50", None, "5.07226")):
    if d_src is None:
        d_src = repr(json.load(open(os.path.join(WT, "open-instances-wave2/cops/logs/chain50_bound.json")))["bnb"]["bound"])
    check(inst, "summary range end", float(d_src), s)
json.dump(rows, open(os.path.join(LOGS, "exact_display_checks.json"), "w"), indent=1)
