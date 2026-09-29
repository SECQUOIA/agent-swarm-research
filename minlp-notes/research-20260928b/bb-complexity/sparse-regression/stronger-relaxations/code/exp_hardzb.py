"""Root values of zb (Clarabel for p <= 50, SCS eps 1e-6 otherwise) and SDP1 (Clarabel) on the pure-noise instances of PT Table 6.4
(p = 10k, n = round(alpha k log p), lam = 0.75 sqrt(2 n log p), b = 0), compared with the exact OPT and the
certified perspective conflict clique stored in ../../data/hard_k3-8.jsonl (and hard_noise_k9-10.jsonl).
usage: exp_hardzb.py OUT nproc [kmax]"""
import os, sys, json, time
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from multiprocessing import Pool
import relax
from relax import instance, sdp1, zb
relax.SCS_OPTS.update(eps=1e-6, max_iters=40000)

HERE = os.path.dirname(os.path.abspath(__file__))


def job(r):
    X, y, _, S = instance(r['n'], r['p'], r['k'], b=0.0, sigma=0.5, seed=r['seed'], lam=r['lam'])
    t = time.time()
    out = dict(p=r['p'], k=r['k'], n=r['n'], alpha=r['alpha'], seed=r['seed'], lam=r['lam'], opt=r['opt'],
               persp_root=r['root'], clique=r.get('clique'), nodes=r['nodes'])
    out['zb'] = zb(X, y, r['lam'], r['k']) if r['p'] <= 50 else zb(X, y, r['lam'], r['k'], solver='SCS')
    out['zb_solver'] = 'CLARABEL' if r['p'] <= 50 else 'SCS(eps=1e-6)'
    out['sdp1'] = sdp1(X, y, r['lam'], r['k'])
    out['time'] = time.time() - t
    return out


if __name__ == '__main__':
    OUT, nproc = sys.argv[1], int(sys.argv[2]); kmax = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    rows = []
    for fn in ('hard_k3-8.jsonl',):
        for l in open(os.path.join(HERE, '..', '..', 'data', fn)):
            r = json.loads(l)
            if r['b'] == 0.0 and r['done'] and r['k'] <= kmax:
                rows.append(r)
    done = set()
    if os.path.exists(OUT):
        done = {(json.loads(l)['k'], json.loads(l)['alpha'], json.loads(l)['seed']) for l in open(OUT)}
    rows = [r for r in rows if (r['k'], r['alpha'], r['seed']) not in done]
    rows.sort(key=lambda r: (r['k'], r['alpha'], r['seed']))
    with Pool(nproc) as pool, open(OUT, 'a') as f:
        for res in pool.imap_unordered(job, rows):
            f.write(json.dumps(res) + '\n'); f.flush(); print(res['k'], res['alpha'], res['seed'], '%.1fs' % res['time'], flush=True)
