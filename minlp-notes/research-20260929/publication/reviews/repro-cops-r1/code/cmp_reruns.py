"""Compare the verifier's reruns (/tmp/rcv_r1/tree, logs/v_*) with the track's logs and with
the committed blobs at c3514f03. Timing values are masked; everything else must be equal."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, os, re, subprocess, sys, difflib, hashlib
RV = (_PUBLIC_REPO + '/research-20260929/publication/reviews/repro-cops-r1')
TR = (_PUBLIC_REPO + '/research-20260929/publication/reproduction/cops/logs')
T = "/tmp/rcv_r1/tree/"
R = "research-20260929/"
pairs = {  # my run -> (track run, outputs relative to research-20260929)
 "v_a_chain_bound_50": ("a_chain_bound_50", ["open-instances-wave2/cops/logs/chain50_bound.json", "open-instances-wave2/cops/logs/chain50_primal.txt"]),
 "v_a_chain_bound_400": ("a_chain_bound_400", ["open-instances-wave2/cops/logs/chain400_bound.json", "open-instances-wave2/cops/logs/chain400_primal.txt"]),
 "v_p_chain_build_50": ("p_chain_build_50", ["publication/primal/chain/points/chain50_box.json", "publication/primal/chain/points/chain50_generator.json"]),
 "v_p_chain_build_100": ("p_chain_build_100", ["publication/primal/chain/points/chain100_box.json", "publication/primal/chain/points/chain100_generator.json"]),
 "v_p_chain_build_200": ("p_chain_build_200", ["publication/primal/chain/points/chain200_box.json", "publication/primal/chain/points/chain200_generator.json"]),
 "v_p_chain_build_400": ("p_chain_build_400", ["publication/primal/chain/points/chain400_box.json", "publication/primal/chain/points/chain400_generator.json"]),
 "v_p_chain_verify": ("p_chain_verify", ["publication/primal/chain/logs/verify.log"]),
 "v_p_chain_scip": ("p_chain_scip_crosscheck", []),
 "v_r_chain_exact": ("r_chain_exact", []),
 "v_a_catmix_primal_100": ("a_catmix_primal_100", ["open-instances-wave2/cops/logs/catmix100_primal.json", "open-instances-wave2/cops/logs/catmix100_primal.txt", "open-instances-wave2/cops/logs/catmix100_u.npy"]),
 "v_a_catmix_snap_800": ("a_catmix_primal_snap_800", ["open-instances-wave2/cops/logs/catmix800_u_snap.npy"]),
 "v_a_catmix_snap_eval_800": ("a_catmix_primal_snap_eval_800", ["open-instances-wave2/cops/logs/catmix800_primal_snap.json", "open-instances-wave2/cops/logs/catmix800_primal_snap.txt"]),
 "v_v_chain_bnb_50": ("v_chain_bnb_50", []),
 "v_v_chain_bnb_400": ("v_chain_bnb_400", []),
 "v_a_catmix_bound_200": ("a_catmix_bound_200", ["open-instances-wave2/cops/logs/catmix200_bound_1e-05_200_1e-07_band0.0685_0.0725_1e-06.json"]),
 "v_v_catmix_selftest_100": ("v_catmix_selftest_100", ["reviews/cops-verification/logs/catmix100_theta_traj.npy"]),
 "v_v_catmix_dp_100_cfgA": ("v_catmix_dp_100_cfgA", []),
 "v_rc_selftest_800": ("v_recheck_selftest_800", ["reviews/catmix-recheck-checks/logs/catmix800_theta_traj.npy"]),
 "v_rc_dp_800_final": ("v_recheck_dp_800_final", ["reviews/catmix-recheck-checks/logs/tree800_final.json", "reviews/catmix-recheck-checks/logs/catmix800_final_policy_traj.npy", "reviews/catmix-recheck-checks/logs/catmix800_final_policy_u.npy"]),
 "v_rc_policy_exact_800": ("v_recheck_policy_exact_800", []),
}
def mask(s):
    s = re.sub(r'("[a-z_]*seconds[a-z_]*"|"seconds_total"|"seconds_bound"): *[0-9.e+-]+', r'\1: T', s)
    s = re.sub(r'\b\d+(\.\d+)?\s?s\)', 'Ts)', s)
    s = re.sub(r'\(\d+(\.\d+)?s', '(Ts', s)
    s = re.sub(r'\b\d+(\.\d+)?s\b', 'Ts', s)
    s = re.sub('/tmp/rcv_r1/tree|/home/[^/]+/repo/minlp-notes-clean|/home/[^/]+/repo/minlp-notes', 'ROOT', s)
    s = re.sub(r'line \d+', 'line L', s)
    return s
def blob(p):
    r = subprocess.run(["git", "-C", (_PUBLIC_REPO), "show", "c3514f03:" + R + p], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def strip(o):
    if isinstance(o, dict): return {k: strip(v) for k, v in o.items() if "seconds" not in k and k != "source_point"}
    if isinstance(o, list): return [strip(v) for v in o]
    return o
only = sys.argv[1:]
for mine, (theirs, outs) in pairs.items():
    if only and mine not in only: continue
    mp = os.path.join(RV, "logs", mine + ".log")
    if not os.path.exists(mp) or "exit:" not in open(os.path.join(RV, "logs", mine + ".meta")).read():
        print("%-28s not finished" % mine); continue
    ex = re.search(r"exit: (\d+)", open(os.path.join(RV, "logs", mine + ".meta")).read()).group(1)
    a = mask(open(mp).read()).splitlines(); b = mask(open(os.path.join(TR, theirs + ".log")).read()).splitlines()
    d = [l for l in difflib.unified_diff(b, a, lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
    res = []
    for o in outs:
        p = T + R + o
        if not os.path.exists(p): res.append("MISSING " + o); continue
        cur = open(p, "rb").read(); bl = blob(o)
        if bl is None: res.append("untracked " + os.path.basename(o)); continue
        if cur == bl: res.append("identical " + os.path.basename(o)); continue
        try:
            res.append(("json-equal-masked " if strip(json.loads(cur)) == strip(json.loads(bl)) else "JSON-DIFF ") + os.path.basename(o))
        except Exception:
            res.append("BYTES-DIFF " + os.path.basename(o))
    print("%-28s exit=%s log-diff-lines-vs-track=%d %s" % (mine, ex, len(d), res))
    for l in d[:12]: print("      ", l[:220])
