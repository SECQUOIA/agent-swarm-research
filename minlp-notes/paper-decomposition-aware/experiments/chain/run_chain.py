"""Expanding-box chain G_m (Example ex:chain): certified grids vs exact messages.

G_m(S,z) = S_m^2 + sum_t (S_t - 2 S_{t-1} - z_t)^2 + (1/8) sum_t z_t (1 - z_t),
S_t in [0, 2^t - 1], z_t in [0, 1], S_0 = 0.  Unique minimizer 0, g = 1/8, L = 10.
Runs the unchanged reference solver, replays every certificate with the
independent checker, and records per-stage grid sizes.  One command:
    python3 run_chain.py   (writes results.json, results.csv, per_stage.csv next to this file)
"""
import csv, json, os, platform, sys, time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))  # outputs are written here, whatever the cwd
SOLVER = os.path.join(HERE, '../../../research-20261002-decomposition/solver')
sys.path.insert(0, os.path.abspath(SOLVER))
from certified_grid import BoxQP, solve            # noqa: E402
from verify_certificate import verify_certificate  # noqa: E402

EPS = Fr(1, 1000)
MS = [2, 4, 8, 16, 32, 64]


def chain(m):
    n = 2 * m
    S = lambda t: 2 * (t - 1)
    Z = lambda t: 2 * (t - 1) + 1
    A = [[Fr(0)] * n for _ in range(n)]
    b = [Fr(0)] * n

    def addsq(coefs):  # (sum c_i x_i)^2 contributes 2 c c^T to A in x'Ax/2
        for i, ci in coefs.items():
            for j, cj in coefs.items():
                A[i][j] += 2 * ci * cj
    for t in range(1, m + 1):
        r = {S(t): Fr(1), Z(t): Fr(-1)}
        if t >= 2:
            r[S(t - 1)] = Fr(-2)
        addsq(r)
        b[Z(t)] += Fr(1, 8)
        A[Z(t)][Z(t)] += Fr(-2, 8)
    A[S(m)][S(m)] += 2
    bounds = []
    for t in range(1, m + 1):
        bounds += [(0, 2 ** t - 1), (0, 1)]
    bags = [(S(1), Z(1))] + [(S(t - 1), S(t), Z(t)) for t in range(2, m + 1)]
    edges = [(k, k + 1) for k in range(len(bags) - 1)]
    return BoxQP(A=A, b=b, bounds=bounds, integers=[], bags=bags, edges=edges, name=f"chain{m}")


def main():
    rows, per_stage = [], []
    for m in MS:
        p = chain(m)
        t0 = time.perf_counter()
        cert = solve(p, epsilon=EPS, time_limit=120, max_stages=200, max_table_states=10 ** 7)
        t1 = time.perf_counter()
        ok = verify_certificate(cert)
        t2 = time.perf_counter()
        stages = cert['stages']
        for s in stages:
            per_stage.append({'m': m, 'stage': s['stage'], 'trial': s['trial'], 'h': s['h'],
                              'max_grid_nodes': max(len(g) for g in s['grids']),
                              'mean_grid_nodes': sum(len(g) for g in s['grids']) / len(s['grids']),
                              'table_states': s['table_states']})
        rows.append({'m': m, 'n': 2 * m, 'status': cert['status'], 'gap': float(Fr(cert['gap'])),
                     'lower': cert['lower'], 'upper': cert['upper'],
                     'stages': len(stages), 'trials': len({s['trial'] for s in stages}),
                     'table_states': cert['stats']['completed_table_states'],
                     'max_grid_nodes': max((len(g) for s in stages for g in s['grids']), default=0),
                     'solve_s': round(t1 - t0, 3), 'replay_s': round(t2 - t1, 3),
                     'replay_ok': bool(ok), 'message_piece_lower_bound': 2 ** (m - 1)})
        print(rows[-1], flush=True)
    meta = {'python': sys.version, 'platform': platform.platform(), 'epsilon': str(EPS),
            'load_avg': os.getloadavg()}
    with open(os.path.join(HERE, 'results.json'), 'w') as f:
        json.dump({'meta': meta, 'rows': rows, 'per_stage': per_stage}, f, indent=1)
    with open(os.path.join(HERE, 'results.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(HERE, 'per_stage.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(per_stage[0]))
        w.writeheader(); w.writerows(per_stage)


if __name__ == '__main__':
    main()
