"""Compare the face candidate of Corollary cor:local (rule of Section 6.5) with the
incumbent-face candidate used by experiments/localized.py, on the S1 instances.

Runs only the grid solve (no height-rule run). Exact arithmetic throughout.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
from instances import random_small  # noqa: E402
from certified_grid import solve  # noqa: E402
from localized import narrowed_box, local_accept, first_acceptance, _solve_linear  # noqa: E402


def face_candidate(problem, y, box):
    """Rule of the paper: copy y outside the continuous coordinates of J_+;
    fix a continuous coordinate of J_+ at a bound of X_i contained in B'_i;
    solve the stationarity equations of the rest."""
    n = len(y)
    H, b = problem.A, problem.b
    x = list(y)
    free = []
    for i in range(n):
        lo, hi = box[i]
        if i in problem.integers or lo == hi:
            continue
        l0, u0 = problem.bounds[i]
        if lo <= l0 <= hi:
            x[i] = F(l0)
        elif lo <= u0 <= hi:
            x[i] = F(u0)
        else:
            free.append(i)
    if free:
        fixed = [i for i in range(n) if i not in free]
        sol = _solve_linear([[H[i][j] for j in free] for i in free],
                            [-b[i] - sum(H[i][j] * x[j] for j in fixed) for i in free])
        if sol is None:
            return None
        for i, v in zip(free, sol):
            x[i] = v
    return tuple(x)


def main():
    seed = 7000
    rows = []
    for n in (4, 6, 8, 12, 16):
        for kind in ('path', 'tree', 'band2'):
            for rep in range(2):
                seed += 1
                problem = random_small(n, kind, 1 + (n >= 8), seed)
                cert = solve(problem, epsilon=F(1, 2**60), max_stages=60, time_limit=60,
                             max_table_states=300000, convex_presolve=False)
                inc_stage, xinc, _ = first_acceptance(problem, cert)
                face_stage, xface = None, None
                for st in cert['stages']:
                    box = narrowed_box(problem, st)
                    y = tuple(F(v) for v in st['grid_point'])
                    # y lies in the narrowed box (shown in the paper); check it here
                    assert all(lo <= v <= hi for v, (lo, hi) in zip(y, box)), problem.name
                    xh = face_candidate(problem, y, box)
                    if xh is not None and local_accept(problem, xh, box, F(st['upper'])):
                        face_stage, xface = st['stage'], xh
                        break
                same = (None if xinc is None or xface is None
                        else problem.value(xinc) == problem.value(xface))
                rows.append((problem.name, inc_stage, face_stage, same))
                print(problem.name, 'incumbent-face:', inc_stage, 'face-candidate:', face_stage,
                      'same value:', same, flush=True)
    acc_inc = sum(r[1] is not None for r in rows)
    acc_face = sum(r[2] is not None for r in rows)
    print('accepted: incumbent-face', acc_inc, 'face candidate', acc_face, 'of', len(rows))
    print('max stage: incumbent-face', max(r[1] for r in rows if r[1] is not None),
          'face candidate', max(r[2] for r in rows if r[2] is not None))


if __name__ == '__main__':
    main()
