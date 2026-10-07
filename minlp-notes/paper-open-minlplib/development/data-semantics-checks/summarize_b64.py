"""Margins of the class (i) refutations and the rocket refutations under binary64 data
(reading (c)) next to the decimal reading (b). Reads the logs of run_audit_b64.sh and the
stored audit evidence (read-only)."""
import json
import os
import re
import sys
from fractions import Fraction as F

REPO = sys.argv[1]
L = sys.argv[2]
R = os.path.join(REPO, "research-20260929")
amap = json.load(open(os.path.join(R, "publication/reproduction/audit-map.json")))


def unit(d):
    s = d.lstrip('-')
    return F(1, 10 ** (len(s.split('.')[1]) if '.' in s else 0))


def obj_hi_b64(inst, pt):
    tag = f"{inst}.{pt}"
    if inst == "watercontamination0303":
        txt = open(f"{L}/b64_cert_linear_watercontamination0303.p2.log").read()
        o = json.loads(txt[txt.index("\n{") + 1:])
        return F(o["objective_exact_30"].replace("e-30", "")) / 10 ** 30 + F(1, 10 ** 30)
    if inst.startswith("nd_netgen"):
        txt = open(f"{L}/b64_cert_ndnetgen.p2.log").read()
        o = json.loads(txt[txt.index("\n{") + 1:])
        return F(o["objective_exact_30"].replace("e-30", "")) / 10 ** 30 + F(1, 10 ** 30)
    if inst.startswith("topopt"):
        txt = open(f"{L}/b64_cert_topopt.{pt}.log").read()
        o = json.loads(txt[txt.index("\n{") + 1:])
        return F(o["obj_hi"])
    line = open(f"{L}/b64_verify_{tag}.log").read().strip().splitlines()[-1].split()
    assert line[0] == tag and line[1] == "proved", line
    nums = [w for w in line if re.fullmatch(r"-?\d+\.\d+(e-?\d+)?", w)]
    return F(nums[1])


print(f"{'instance':30s} {'solver':9s} {'pt':3s} {'listed d':>14s} {'f_hi (b)':>22s} {'f_hi (c)':>22s} {'d - f_hi (c)':>13s} {'units (c)':>10s}")
for e in amap:
    for p in e.get("classified_pairs", []):
        if p.get("cls") != "i":
            continue
        d = F(p["d"])
        fb = F(p["obj_hi"])
        fc = obj_hi_b64(p["name"], p["point"])
        m = d - fc
        assert m > 0
        print(f"{p['name'][:30]:30s} {p['solver']:9s} {p['point']:3s} {p['d']:>14s} {float(fb):22.15g} {float(fc):22.15g} "
              f"{float(m):13.6g} {float(m / unit(p['d'])):10.4g}")
LINDO = {100: '-1.0128319', 200: '-1.01283563', 400: '-1.01283634'}
for n in (100, 200, 400):
    txt = open(f"{L}/b64_rocket_kraw_{n}.log").read()
    o = json.loads(txt[txt.index("{"):])
    assert o["box_ok"] and o["obj_hi_exact_below_lindo"]
    d = F(LINDO[n]); fc = F(o["outward_13dec"][1])
    print(f"{'rocket%d' % n:30s} {'LINDO':9s} {'own':3s} {LINDO[n]:>14s} {'(see audit 5.4)':>22s} {float(fc):22.15g} "
          f"{float(d - fc):13.6g} {float((d - fc) / unit(LINDO[n])):10.4g}")
