"""Spot check: final JSON objects of track logs vs committed reviewer logs (c3514f03), timing masked."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, re, subprocess
TR = (_PUBLIC_REPO + '/research-20260929/publication/reproduction/cops/logs/')
def blob(p):
    return subprocess.run(["git", "-C", (_PUBLIC_REPO), "show", "c3514f03:research-20260929/" + p],
                          capture_output=True, text=True, check=True).stdout
def jsons(t):
    out = []
    for line in t.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try: out.append(json.loads(line))
            except Exception: pass
    return out
def strip(o):
    if isinstance(o, dict): return {k: strip(v) for k, v in o.items() if "seconds" not in k}
    if isinstance(o, list): return [strip(v) for v in o]
    return o
pairs = [
 ("v_catmix_dp_100_cfgB", "reviews/cops-verification/logs/catmix100_cfgB.log"),
 ("v_catmix_dp_100_cfgA", "reviews/cops-verification/logs/catmix100_cfgA.log"),
 ("v_catmix_dp_200_cfgA", "reviews/cops-verification/logs/catmix200_cfgA.log"),
 ("v_recheck_dp_400_final", "reviews/catmix-recheck-checks/logs/catmix400_final.log"),
 ("v_recheck_dp_800_final", "reviews/catmix-recheck-checks/logs/catmix800_final.log"),
 ("v_chain_bnb_100", "reviews/cops-verification/logs/chain100_200_bnb.log"),
 ("v_chain_bnb_200", "reviews/cops-verification/logs/chain100_200_bnb.log"),
 ("v_chain_bnb_400", "reviews/cops-verification/logs/chain400_bnb.log"),
 ("v_chain_bnb_50", "reviews/cops-verification/logs/chain50_bnb.log"),
]
for name, ref in pairs:
    a = [strip(o) for o in jsons(open(TR + name + ".log").read())]
    b = [strip(o) for o in jsons(blob(ref))]
    notin = [o for o in a if o not in b]
    print("%-24s track JSON objs %d, committed %d, track objs not in committed: %d" % (name, len(a), len(b), len(notin)))
    for o in notin[:3]: print("    ", json.dumps(o)[:300])
# text logs: policy_exact, lemma, side checks, negative controls
for name, ref in [("v_recheck_policy_exact_400", "reviews/catmix-recheck-checks/logs/policy_exact_400.log"),
                  ("v_recheck_policy_exact_800", "reviews/catmix-recheck-checks/logs/policy_exact_800.log"),
                  ("v_chain_checks_lemma", "reviews/cops-verification/logs/chain_lemma.log"),
                  ("v_chain_checks_lemma_adv", "reviews/cops-verification/logs/chain_lemma_adv.log"),
                  ("v_chain_checks_theorem", "reviews/cops-verification/logs/chain_theorem.log"),
                  ("v_chain_checks_struct", "reviews/cops-verification/logs/chain_struct.log"),
                  ("r_chain_negative_controls", "publication/reviews/primal-chain-r1/logs/rev_negative_controls.log"),
                  ("v_catmix_newton_100", "reviews/cops-verification/logs/catmix100_newton.log")]:
    m = lambda s: re.sub(r"\(?\d+(\.\d+)?s\)?|line \d+|/home/\S+", "X", s)
    a = [m(l) for l in open(TR + name + ".log").read().splitlines() if l.strip()]
    b = set(m(l) for l in blob(ref).splitlines())
    miss = [l for l in a if l not in b]
    print("%-26s lines %d, not in committed %d" % (name, len(a), len(miss)))
    for l in miss[:4]: print("     ", l[:200])
