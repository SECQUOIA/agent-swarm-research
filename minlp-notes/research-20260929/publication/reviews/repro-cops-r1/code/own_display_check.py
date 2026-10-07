"""Verifier's own exact check of displayed bound decimals and gaps (repro-cops review r1).

Reads the certified doubles from the committed files at commit c3514f03 (git show), takes
each double exactly (Fraction(float)), and compares it with the decimal displayed in the
notes / reviews / summary. A displayed decimal D is a valid lower bound only if D <= double.
Only fractions.Fraction is used for the comparisons.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, re, subprocess
from fractions import Fraction as F

REPO = (_PUBLIC_REPO)
C = "c3514f03"
R = "research-20260929/"

def show(path):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s%s" % (C, R, path)],
                          capture_output=True, text=True, check=True).stdout

def last_json_with(path, key):
    objs = []
    for line in show(path).splitlines():
        line = line.strip()
        if line.startswith("{") and key in line:
            objs.append(json.loads(line))
    return objs

out = []
def chk(label, dbl, display, where):
    d = F(dbl)                       # exact value of the binary64 number
    D = F(display.replace("−", "-"))
    out.append(dict(label=label, double_repr=repr(dbl), display=display, where=where,
                    display_minus_double=float(D - d), display_valid_as_lower_bound=(D <= d)))

# authors' chain bounds
chain_d = {}
for N in (50, 100, 200, 400):
    j = json.loads(show("open-instances-wave2/cops/logs/chain%d_bound.json" % N))
    chain_d[N] = j["bnb"]["bound"] if "bnb" in j else j["bound"]
disp_chain = {50: "5.072261493982863", 100: "5.0697846107387505", 200: "5.068917341793162", 400: "5.068621694604009"}
for N in disp_chain:
    chk("chain%d authors" % N, chain_d[N], disp_chain[N], "cops/report.md table")

# authors' catmix bounds
cat_d = {}
for N in (100, 200, 400, 800):
    j = json.loads(show("open-instances-wave2/cops/logs/catmix%d_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json" % N))
    cat_d[N] = j["dual_bound"]
disp_cat = {100: "-0.048069432038882705", 200: "-0.04805914560067171", 400: "-0.048056547950296354", 800: "-0.048055901841076894"}
for N in disp_cat:
    chk("catmix%d authors" % N, cat_d[N], disp_cat[N], "cops/report.md table")

# verifier catmix (cops-verification) and recheck
vA100 = last_json_with("reviews/cops-verification/logs/catmix100_cfgA.log", "dual_bound")[-1]["dual_bound"]
vB100 = last_json_with("reviews/cops-verification/logs/catmix100_cfgB.log", "dual_bound")[-1]["dual_bound"]
vA200 = last_json_with("reviews/cops-verification/logs/catmix200_cfgA.log", "dual_bound")[-1]["dual_bound"]
rc400 = last_json_with("reviews/catmix-recheck-checks/logs/catmix400_final.log", "dual_bound")[-1]["dual_bound"]
rc800 = last_json_with("reviews/catmix-recheck-checks/logs/catmix800_final.log", "dual_bound")[-1]["dual_bound"]
chk("catmix100 verifier cfgA", vA100, "-0.048069432031981114", "verification-report.md")
chk("catmix100 verifier cfgB", vB100, "-0.04806943203114456", "verification-report.md; summary bracket")
chk("catmix200 verifier cfgA", vA200, "-0.04805914559907277", "verification-report.md")
chk("catmix400 recheck", rc400, "-0.04805654782467129", "catmix-recheck.md")
chk("catmix800 recheck", rc800, "-0.04805590147967565", "catmix-recheck.md")
# summary range displays (lowest/highest)
chk("summary chain range low (chain400)", chain_d[400], "5.06862", "summary")
chk("summary chain range high (chain50)", chain_d[50], "5.07226", "summary")
chk("summary catmix range low (catmix100 best bound cfgB)", vB100, "-0.04806944", "summary")
chk("summary catmix range high (catmix800 authors)", cat_d[800], "-0.04805591", "summary")
chk("summary catmix range high (catmix800 recheck)", rc800, "-0.04805591", "summary")

# gaps: chain primal exact enclosures (committed verify.log of publication/primal/chain)
txt = show("publication/primal/chain/logs/verify.log")
objs = [json.loads(m) for m in re.findall(r"\{.*?\n\}", txt, flags=re.S)]
gaps = []
for o in objs:
    N = int(o["instance"][5:])
    hi = F(o["objective_hi"]); lo = F(o["objective_lo"])
    d = F(chain_d[N]); D = F(disp_chain[N])
    gaps.append(dict(instance=o["instance"], obj_hi=o["objective_hi"],
                     gap_vs_double=float(hi - d), gap_vs_display=float(hi - D),
                     committed_gap_abs_upper=o["gap_abs_upper"],
                     double_exact_matches_log=(F(o["dual_bound_double_exact"][:42]) - d) == 0 if False else None,
                     double_exact_log=o["dual_bound_double_exact"],
                     double_exact_mine_45digits="%s" % (lambda q: (q.numerator * 10**40 // q.denominator))(d)))
# catmix brackets (displayed primal values minus certified doubles)
gaps.append(dict(instance="catmix100", primal="-0.048069432030979596104 (Newton point, exact J display)",
                 gap_vs_cfgB_double=float(F("-0.048069432030979596104") - F(vB100))))
gaps.append(dict(instance="catmix800", primal="-0.0480559013312308003 (policy point)",
                 gap_vs_recheck_double=float(F("-0.04805590133123080033938") - F(rc800))))
gaps.append(dict(instance="catmix400", primal="-0.04805654775594407258228 (policy point)",
                 gap_vs_recheck_double=float(F("-0.04805654775594407258228") - F(rc400))))
res = dict(display_checks=out, gaps=gaps)
print(json.dumps(res, indent=1))
