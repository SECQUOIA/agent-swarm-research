"""Read the JSON-lines dumps written by the instrumented nlhdlr_quadratic.c (patch/).

One record per call of generateIntercut (SCIP main problem only).  Helpers rebuild, in the
space SCIP uses (constraint variables ordered [quadratic exprs, linear exprs, aux var]):
  S = {s : s^T Q s + b^T s + c <= 0}   (the side of the constraint that is violated),
  sbar = LP values, P = projected rays (columns), w = objective rates of the rays.
"""
import gzip, json
import numpy as np

SCIP_BASESTAT_LOWER, SCIP_BASESTAT_BASIC, SCIP_BASESTAT_UPPER, SCIP_BASESTAT_ZERO = 0, 1, 2, 3


def records(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                yield {'corrupt': True}


def quadratic(rec):
    """(Q, b, c) of the violated side, as SCIP sets it up (sidefactor applied)."""
    nq, nl = rec['nquad'], rec['nlin']
    aux = rec['auxvar'] is not None
    nv = nq + nl + (1 if aux else 0)
    Q = np.zeros((nv, nv))
    for i, a in enumerate(rec['qsqr']):
        Q[i, i] += a
    for i, j, a in rec['bilin']:
        Q[i, j] += a / 2.0
        Q[j, i] += a / 2.0
    b = np.zeros(nv)
    b[:nq] = rec['qlin']
    b[nq:nq + nl] = rec['lincoefs']
    sf = -1.0 if rec['over'] else 1.0
    const = rec['constant']
    if aux:
        b[-1] = -1.0
        c = sf * const
    else:
        c = (const - rec['rhs']) if sf > 0 else (rec['lhs'] - const)
    return sf * Q, sf * b, c


def rays(rec):
    """Projected rays P (nv x N), objective rates w (>= 0 up to sign errors), raw signs."""
    nv = rec['nv']
    N = rec['nrays']
    P = np.zeros((nv, N))
    for j, ent in enumerate(rec['rays']):
        for k, v in ent:
            P[k, j] = v
    rate = np.array(rec['rayrate'], float)
    stat = np.array(rec['raystat'], int)
    lppos = np.array(rec['raylppos'], int)
    w = np.empty(N)
    # columns: nonbasic at lower moves up (rate = redcost), at upper moves down (rate = -redcost)
    # rows: the ray moves the row activity away from its active side by one unit; rate = |dual|
    col = lppos >= 0
    w[col] = np.where(stat[col] == SCIP_BASESTAT_UPPER, -rate[col], rate[col])
    # row status in SCIP: LOWER = activity at lhs (dual >= 0 for min), UPPER = at rhs (dual <= 0)
    w[~col] = np.where(stat[~col] == SCIP_BASESTAT_UPPER, -rate[~col], rate[~col])
    return P, w, stat, lppos


def fixed_rays(rec, tol=1e-9):
    """Rays of nonbasic equality rows or fixed columns (width = ub - lb or rhs - lhs <= tol).
    Their lambda_j is 0 at every LP-feasible point, so they are not part of the LP corner."""
    if 'raywidth' not in rec:
        return np.zeros(rec['nrays'], bool)
    return np.array(rec['raywidth'], float) <= tol


def scip_steps(rec):
    """SCIP's step lengths (interpoints) per ray, inf for 'no intersection' (t >= 1e20)."""
    t = np.full(rec['nrays'], np.nan)
    coef = np.full(rec['nrays'], np.nan)
    mono = np.zeros(rec['nrays'], bool)
    for e in rec.get('perray', []):
        if e.get('fail'):
            continue
        tt = e['t']
        if tt is not None and 0 <= tt < 1e20:
            t[e['i']] = tt
        elif tt is None or tt >= 1e20:
            t[e['i']] = np.inf          # SCIP: no intersection (SCIPinfinity)
        # tt < 0: interpoint not computed (monoidal coefficient used); stays nan
        coef[e['i']] = e['coef']
        mono[e['i']] = bool(e['mono'])
    return t, coef, mono
