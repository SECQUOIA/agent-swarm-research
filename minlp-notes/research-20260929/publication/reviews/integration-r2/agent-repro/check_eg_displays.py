"""Integration review r2 (agent-repro): exact rational checks of the README EG displays.

Standard library only; reads saved text files; imports no repository module.
Run with:  python3 -I -B check_eg_displays.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json
import re
from fractions import Fraction as F

R = (_PUBLIC_REPO + '/research-20260929')
RETRY = R + "/open-instances-wave3/eg/retry"
README = open(R + "/publication/reproduction/README.md").read()
ok_all = True


def objvar(name):
    t = open(f"{RETRY}/sol/{name}.retry.sol").read()
    return re.search(r"^objvar\s+(\S+)$", t, re.M)[1]


def cert_lbs(logs):
    out = []
    for lg in logs:
        t = open(f"{RETRY}/logs/{lg}").read()
        out.append(re.search(r"certified lower bound np\.float64\(([0-9.e+-]+)\)", t)[1])
    return out


def chk(label, cond):
    global ok_all
    ok_all &= cond
    print(f"  {'PASS' if cond else 'FAIL'}: {label}")


rows = {
    "eg_int_s": (["int9_final.log"], "6.4531031529331155", "6.4531031593842275"),
    "eg_disc_s": (["disc9_p0.log", "disc9_p1.log"], "5.760539610694994", "5.7605396164535107"),
    "eg_disc2_s": ([f"disc2_9_p{k}.log" for k in range(8)], "5.642100574331458", "5.6421005799711068"),
}
for name, (logs, dual_disp, primal_disp) in rows.items():
    print(f"== {name}")
    line = re.search(rf"^\| {name} \|.*$", README, re.M)[0]
    chk(f"README row shows dual {dual_disp} / primal {primal_disp}", f"{dual_disp} / {primal_disp}" in line)
    ov = objvar(name)
    P, Pd = F(ov), F(primal_disp)
    print(f"  saved objvar {ov} = {P}; display {primal_disp}; display - objvar = {float(Pd - P):.3e}")
    chk("primal display >= saved objvar (exactly)", Pd >= P)
    lbs = cert_lbs(logs)
    lb_double = min(F(float(s)) for s in lbs)      # exact binary64 value of the smallest part bound
    lb_dec = min(F(s) for s in lbs)                # the decimal strings as printed
    D = F(dual_disp)
    print(f"  part bounds (repr) {sorted(set(lbs))}; min exact binary64 {float(lb_double)!r}")
    print(f"  dual display - min binary64 bound = {float(D - lb_double):.3e}; "
          f"dual display - min printed decimal = {float(D - lb_dec):.3e}")
    chk("dual display <= exact binary64 certificate", D <= lb_double)
    gap_rel = (Pd - D) / abs(Pd)
    print(f"  displayed relative gap (P-D)/|P| = {float(gap_rel):.3e}")
    chk("displayed gap <= 1e-9 rel. (summary column)", gap_rel <= F(1, 10**9))

# the display-check log of the package
print("== logs/integration-r1-displays.json")
recs = json.load(open(R + "/publication/reproduction/logs/integration-r1-displays.json"))
for r in recs:
    ex, d = F(r["exact"]), F(r["display"])
    good = d >= ex if r["direction"] == "up" else d <= ex
    print(f"  {r['name']}: exact {float(ex)!r} display {r['display']} dir {r['direction']}: "
          f"{'PASS' if good else 'FAIL'} (recorded passed={r['passed']})")
    ok_all &= good and r["passed"]
    if r["source"].endswith(".retry.sol"):
        nm = re.search(r"sol/(\w+)\.retry\.sol", r["source"])[1]
        same = F(objvar(nm)) == ex
        print(f"    exact equals saved objvar of {nm}: {same}")
        ok_all &= same
print("ALL PASS" if ok_all else "SOME CHECK FAILED")
