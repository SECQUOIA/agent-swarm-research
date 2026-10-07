"""C-computation-2: smallest Hessian eigenvalue of every planted instance used in Section 11."""
import sys
from pathlib import Path
import numpy as np
EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
from instances import planted  # noqa: E402

SEEDS = (101, 202, 303)
cases = {}
for kind, n in (('path', 16), ('tree', 16), ('band2', 12), ('band3', 8)):
    for s in SEEDS:
        cases.setdefault('E1', []).append((kind, n, 4, s))
for kt in (2, 4, 8, 16, 32, 64, 128, 256):
    for s in SEEDS:
        cases.setdefault('E2', []).append(('path', 16, kt, s))
for kt in (2, 4):
    for n in (4, 8, 16, 32, 64, 128):
        for s in SEEDS:
            cases.setdefault('E3', []).append(('path', n, kt, s))
for kind, n in (('path', 16), ('tree', 16), ('band2', 12), ('band3', 8), ('path', 32), ('path', 64), ('path', 128)):
    for s in SEEDS:
        cases.setdefault('E5', []).append((kind, n, 4, s))
for kind in ('path', 'tree', 'band2'):
    cases.setdefault('E4', []).append((kind, 6, 4, 4100))
for exp, lst in cases.items():
    worst = None
    for kind, n, kt, s in lst:
        p, _ = planted(kind, n, kt, s)
        H = np.array([[float(a) for a in row] for row in p.A])
        lam = float(np.linalg.eigvalsh(H)[0])
        if worst is None or lam > worst[0]:
            worst = (lam, kind, n, kt, s)
    print(exp, len(lst), 'largest lambda_min = %.4f' % worst[0], worst[1:])
