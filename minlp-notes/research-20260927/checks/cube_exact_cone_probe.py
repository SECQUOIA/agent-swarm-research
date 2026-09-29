"""Exploratory exact-cone SDP probes; numerical output is not a proof."""

from itertools import permutations, product
from pathlib import Path
import json
import numpy as np
import cvxpy as cp


def main():
    rng = np.random.default_rng(20260927)
    A = cp.Variable((4, 4), symmetric=True)
    integ = np.full((4, 4), 0.25)
    integ[0, :] = integ[:, 0] = 0.5
    np.fill_diagonal(integ, [1, 1/3, 1/3, 1/3])
    constraints = [cp.sum(cp.multiply(A, integ)) == 1]
    for perm in permutations(range(3)):
        vertices = [np.zeros(3)]
        for i in perm:
            v = vertices[-1].copy()
            v[i] = 1
            vertices.append(v)
        V = np.vstack([np.ones(4), np.array(vertices).T])
        N = cp.Variable((4, 4), symmetric=True)
        constraints += [N >= 0, V.T @ A @ V - N >> 0]
    C = cp.Parameter((4, 4), symmetric=True)
    prob = cp.Problem(cp.Minimize(cp.sum(cp.multiply(C, A))), constraints)
    candidates = []
    for trial in range(300):
        mean = rng.uniform(0.05, 0.95, 3)
        root = rng.normal(size=(3, 3))
        cov = root @ root.T
        scales = [mean[i]*(1-mean[i])/cov[i,i] for i in range(3)]
        for i in range(3):
            for j in range(i+1, 3):
                if cov[i,j] > 0:
                    scales.append((min(mean[i], mean[j])-mean[i]*mean[j])/cov[i,j])
                else:
                    scales.append((max(0, mean[i]+mean[j]-1)-mean[i]*mean[j])/cov[i,j])
        cov *= min(scales) * rng.uniform(0.8, 1)
        C.value = np.block([[np.ones((1,1)), mean[None,:]],
                           [mean[:,None], np.outer(mean,mean)+cov]])
        prob.solve(solver='CLARABEL', tol_gap_abs=1e-8, tol_feas=1e-8,
                   tol_gap_rel=1e-8, max_iter=300)
        if A.value is None:
            continue
        a = A.value
        q = a[1:, 1:]
        ev = np.linalg.eigvalsh(q)
        minors = [q[i,i]*q[j,j]-q[i,j]**2 for i in range(3) for j in range(i+1,3)]
        if min(np.diag(q)) > 1e-4 and ev[0] < -1e-4:
            vertices = [np.r_[1, v] for v in product((0, 1), repeat=3)]
            item = {'trial': trial, 'objective': prob.value, 'A': a.tolist(), 'minors': minors,
                    'min_vertex': min(v@a@v for v in vertices)}
            candidates.append(item)
            print(trial, 'minors', np.round(minors, 5), 'min_vertex', item['min_vertex'], flush=True)
    out = Path(__file__).with_name('cube_exact_cone_probe.json')
    out.write_text(json.dumps({'seed': 20260927, 'trials': 300, 'cost_mode': 'PSD_RLT_covariance_ray',
                               'candidates': candidates}, indent=2))
    print('saved', out, 'candidates', len(candidates))


if __name__ == '__main__':
    main()
