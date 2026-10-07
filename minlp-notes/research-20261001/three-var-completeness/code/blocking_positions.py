"""For each minimal blocking configuration B, search contact positions
theta for which the face F(B) contains p with p(0) >= delta (base
normalization <p,u> = 1).  Inner problem: min ||A(theta) p||^2 over the
base of P3plus with p(0) >= delta (SDP).  Outer: Nelder-Mead over theta."""
import sys, json, time, warnings, ast
import numpy as np, cvxpy as cp
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
from sdp3 import Separation, SOLVER_OPTS
from face_explore import lin_value, lin_deriv
from blocking2 import in_family_pattern

def rows_theta(config, theta):
    rows = []; it = iter(theta)
    for s in config:
        pt = [next(it) if c == -1 else float(c) for c in s]
        rows.append(lin_value(pt))
        for i in range(3):
            if s[i] == -1:
                rows.append(lin_deriv(pt, i))
    return np.array(rows)

class Inner:
    def __init__(self, delta=0.01):
        S = Separation()
        self.A = cp.Parameter((12, 10))
        self.pv = S.pv
        cons = S.prob.constraints + [self.pv[0] >= delta]
        self.prob = cp.Problem(cp.Minimize(cp.sum_squares(self.A @ self.pv)), cons)
    def __call__(self, config, theta):
        R = rows_theta(config, theta)
        Ap = np.zeros((12, 10)); Ap[:R.shape[0]] = R
        self.A.value = Ap
        try:
            self.prob.solve(solver='CLARABEL')
            return self.prob.value if self.prob.value is not None else 1e3
        except BaseException:   # includes pyo3 PanicException from Clarabel
            return 1e3

if __name__ == '__main__':
    infile, part, nparts, starts = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    skip = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    tag = sys.argv[6] if len(sys.argv) > 6 else str(part)
    count = int(sys.argv[7]) if len(sys.argv) > 7 else None
    configs = []
    for line in open(infile).read().splitlines()[1:]:
        i = line.index('((')
        configs.append(ast.literal_eval(line[i:].strip()))
    configs = configs[part::nparts][skip:]
    if count is not None:
        configs = configs[:count]
    inner = Inner()
    rng = np.random.default_rng(100 + part)
    out = []; t0 = time.time()
    for B in configs:
        m = sum(s.count(-1) for s in B)
        best = (np.inf, None)
        for s in range(starts):
            th0 = rng.uniform(0.1, 0.9, m)
            f = lambda th: inner(B, np.clip(th, 0.03, 0.97)) + 10 * np.sum(np.maximum(0, np.abs(th - 0.5) - 0.47)**2)
            r = minimize(f, th0, method='Nelder-Mead', options=dict(maxfev=60 * (m + 1), xatol=1e-6, fatol=1e-12))
            if r.fun < best[0]:
                best = (r.fun, np.clip(r.x, 0.03, 0.97).tolist())
            if best[0] < 1e-10:
                break
        fam = in_family_pattern(B)
        out.append(dict(config=B, resid=best[0], theta=best[1], family_sub=fam))
        print('%.3e' % best[0], 'family-sub' if fam else 'NEW', B, np.round(best[1], 4).tolist(), 'elapsed %.0f' % (time.time() - t0), flush=True)
    json.dump(out, open(f'../logs/blocking_positions_{tag}.json', 'w'))
