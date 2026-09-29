"""Independent exact C1 decisions for a sample of the note's Section 6 runs (own code, rc_common.py).
Compares with the note's stored decisions (exp_c1 output or the redecided file).
usage: python3 redecide_sample.py OUT NPROC"""
import sys, json, time
from multiprocessing import Pool
from rc_common import make_instance, decide_c1

# (p, k, n, rule, seed, note's decision, source)
RUNS = [
    (3200, 5, 121, 'sqrtn', 1007, 'fail', 'redecided'),
    (3200, 5, 121, 'sqrtn', 1001, 'C1', 'redecided'),
    (3200, 5, 121, 'sqrtn', 1004, 'C1', 'redecided'),
    (1600, 8, 74, '1.5', 1004, 'C1', 'redecided'),
    (1600, 8, 74, '1.5', 1006, 'C1', 'redecided'),
    (1600, 8, 89, '1.5', 1003, 'C1', 'redecided'),
    (800, 5, 100, 'sqrtn', 1002, 'C1', 'redecided'),
    (400, 8, 60, '1.5', 1005, 'C1', 'redecided'),
    (1600, 8, 89, '1.5', 1004, 'fail', 'exact'),
    (1600, 8, 74, '1.5', 1002, 'fail', 'exact'),
    (400, 20, 120, '1.5', 1001, 'C1', 'exact'),
    (400, 20, 120, '1.5', 1004, 'fail', 'exact'),
    (200, 8, 53, '1.5', 1001, 'fail', 'exact'),
    (200, 8, 53, '1.5', 1005, 'C1', 'exact'),
    (100, 8, 37, '1.5', 1007, 'fail', 'exact'),
]


def job(run):
    p, k, n, rule, seed, note, src = run
    t = time.time()
    X, y, lam, S = make_instance(n, p, k, seed, rule)
    d = decide_c1(X, y, lam, k, S)
    return dict(p=p, k=k, n=n, rule=rule, seed=seed, note=note, src=src, mine=d['status'], solved=d['solved'],
                fail=d['fail'], n_undecided=len(d['undecided']), undecided=d['undecided'][:5], fS=d['fS'],
                root_gap=d['fS'] - d['root_lb'], tau2=d['tau2'], time=time.time() - t)


if __name__ == '__main__':
    out, nproc = sys.argv[1], int(sys.argv[2])
    runs = sorted(RUNS, key=lambda r: -r[0])
    with Pool(nproc) as pool, open(out, 'w') as f:
        for res in pool.imap_unordered(job, runs):
            f.write(json.dumps(res) + '\n'); f.flush()
            print("p=%d k=%d n=%d rule=%s seed=%d  note: %s (%s)  mine: %s  solves %d  undecided %d  fail=%s  %.0fs" % (
                res['p'], res['k'], res['n'], res['rule'], res['seed'], res['note'], res['src'], res['mine'],
                res['solved'], res['n_undecided'], res['fail'], res['time']), flush=True)
