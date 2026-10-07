"""Driver: for each two-switch kappa=-0.5 grid of Section 9.1 (N <= 2000), find the best pattern by the
reviewer's exact scan around the author's switching stages, compare with the author's zbar (J and
fractional stage), then run the reviewer's exact box branch and bound (v_two_bb) on it."""
import json, subprocess, sys
from fractions import Fraction as Fr
from vtoy import traj, kkt_check
from v_two import toy2, scan, pattern
author = json.load(open('../../theory-bangbang/kneg/logs/two.json'))
cases = [r for r in author if r.get('kappa') == -0.5 and r['N'] <= 2000]
for r in cases:
    t1s, t2s = f"f:{r['t1']}", f"f:{r['t2']}"
    t1, t2 = Fr(float(r['t1'])), Fr(float(r['t2']))
    toy = toy2(Fr(1, 2), t1, t2)
    N = r['N']
    s1, s2 = r['switch_stages']
    res = scan(toy, N, s1, s2, 5)
    J, m1, v1, m2, v2 = res[0]
    h = toy.T / N
    E = traj(toy, N, pattern(N, m1, v1, m2, v2))
    ok, frac = kkt_check(E)
    # author's zbar J is not logged; reconstruct it from the logged switching stages / fractional value:
    # report the best pattern's frac and compare with the author's frac
    line = dict(t1=r['t1'], t2=r['t2'], N=N, author_frac=r['frac'], author_u_frac=r['u_frac'],
                best=dict(m1=m1, v1=float(v1), m2=m2, v2=float(v2), kkt=ok, frac=frac,
                          u_frac=[float(E['u'][t]) for t in frac]),
                second_best_gap_h2=float((res[1][0] - J) / h ** 2) if res[1][0] != J else 0.0)
    out = subprocess.run([sys.executable, 'v_two_bb.py', '1/2', t1s, t2s, str(N), str(m1), str(v1), str(m2), str(v2)],
                         capture_output=True, text=True, timeout=3600)
    bb = json.loads(out.stdout.strip().splitlines()[-1])
    line.update(bb_complete=bb['complete'], bb_nodes=bb['n_nodes'], bb_leaves=bb['n_leaves'], bb_ok=bb['all_leaves_ok'],
                bb_better=bb['better_point'], bb_target_frac=bb['target_frac'], bb_time=bb['time'])
    print(json.dumps(line), flush=True)
