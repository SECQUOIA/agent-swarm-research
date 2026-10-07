"""Rerun selected package smoke checks in the reviewer's relocated copy (main tree hidden)."""
import json, subprocess, sys, time, os
T = open(os.path.join(os.path.dirname(__file__), '..', 'tree.txt')).read().strip()
R = T + '/minlp-notes/research-20260929'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'smoke'); os.makedirs(OUT, exist_ok=True)
CHECKS = [
    ("lnts50-tight", "reviews/open-instances-verification", ["v_lnts.py", "50"]),
    ("optcdeg2", "theory-bangbang", ["optcdeg2_qcal_recheck.py"]),
    ("chain50", "open-instances-wave2/cops", ["chain_bound.py", "1e-14", "50"]),
    ("ex6_2_7", "reviews/wave2-small-verification", ["gibbs_bound.py", "ex6_2_7", "0=logs/ex6_2_7_bb_type0_tau6e-15.json"]),
    ("powerflow0030p-stored", "reviews/wave3-verification/powerflow", ["run_root.py", "powerflow0030p"]),
    ("waterno2_06-cellslopes", "reviews/waterno2-cellslopes-review-checks", ["ind_verify_cs.py", "../../open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz", "logs/rev_ind_verify_certB.json", "../../open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json"]),
    ("audit-ghg_3veh", "reviews/bound-audit-verification", ["run_kraw.py", "ghg_3veh.p2"]),
]
sel = sys.argv[1:] or [c[0] for c in CHECKS]
res = {}
if os.path.exists(os.path.join(OUT, 'results.json')):
    res = json.load(open(os.path.join(OUT, 'results.json')))
for name, cwd, args in CHECKS:
    if name not in sel or name in res: continue
    cmd = [os.path.join(HERE, 'sandbox.sh'), T, f"{R}/{cwd}", 'timeout', '120', 'python3'] + args
    t0 = time.monotonic(); p = subprocess.run(cmd, capture_output=True, text=True); w = time.monotonic() - t0
    open(os.path.join(OUT, name + '.log'), 'w').write(p.stdout + p.stderr)
    res[name] = dict(cwd='$R/' + cwd, command='python3 ' + ' '.join(args), exit=p.returncode, wall_s=round(w, 2))
    print(name, res[name], flush=True)
    json.dump(res, open(os.path.join(OUT, 'results.json'), 'w'), indent=1)
