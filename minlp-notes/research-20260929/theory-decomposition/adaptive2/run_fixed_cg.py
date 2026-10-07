"""GR with the conditioning held fixed across sizes (adaptive-matching.md, Sections 8.3-8.4, revision
after review).

  python3 run_fixed_cg.py path THETA_INV EPS JMAX n:b [n:b ...]       # c = 0, R = 4, x0 = 0.5*ones
  python3 run_fixed_cg.py tree THETA_INV EPS JMAX m:b [m:b ...]       # c = 0, R = 4, x0 = 0.5*ones

The couplings b are chosen (cg_by_size.py) so that the lower bound 0.9 - b rho(A)/2 on c_g, and with
it the local constant 1 - b rho(A)/2 at x* = 0, is the same for every size. Reuses run_gr.run (path)
and tree_gr.run_gr_tree (tree) unchanged; JMAX caps the stage index. Floating point illustrations.
"""
import sys
import time
import numpy as np
import run_gr
import tree_gr as TG

fam, theta, eps, jmax = sys.argv[1], 1.0 / float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
for spec in sys.argv[5:]:
    n_s, b_s = spec.split(":")
    n, b = int(n_s), float(b_s)
    rho = np.linalg.eigvalsh(np.diag(np.ones(n - 1), 1) + np.diag(np.ones(n - 1), -1))[-1] if fam == "path" else None
    if fam == "path":
        print("path n=%d b=%.6f: 0.9 - b rho/2 = %.4f" % (n, b, 0.9 - b * rho / 2), flush=True)
        run_gr.B = b
        run_gr.run(n, np.zeros(n), eps, np.full(n, 0.5), theta, 4.0, np.zeros(n), 0.0,
                   "fixedcg-path-b%.4f" % b, jmax=jmax)
    else:
        A = np.zeros((n, n))
        v = np.arange(1, n)
        A[(v - 1) // 2, v] = A[v, (v - 1) // 2] = 1
        rho = np.linalg.eigvalsh(A)[-1]
        print("tree m=%d b=%.6f: 0.9 - b rho/2 = %.4f" % (n, b, 0.9 - b * rho / 2), flush=True)
        t0 = time.time()

        def log(r):
            r["m"] = n
            print(TG.fmt(r), flush=True)
        res, recs = TG.run_gr_tree(n, b, 0.1, np.zeros(n), eps, np.full(n, 0.5), theta, 4.0, jmax=jmax,
                                   xstar=np.zeros(n), fstar=0.0, log=log)
        print("SUMMARY fixedcg-tree m=%d b=%.4f eps=%.0e theta=1/%d R=4 done=%s stages=%s size=%s "
              "size_per_bag=%.0f created=%d processed=%d max_split=%d max_zloc=%.3f wide=%d time=%.1fs" % (
                  n, b, eps, round(1 / theta), res["done"], res.get("j"), res.get("size"),
                  (res.get("size") or 0) / (n - 1), res["created"], res["processed"],
                  max(r.get("split_leaf_max", 0) for r in recs), max(r["zloc"] for r in recs),
                  sum(r.get("wide", 0) for r in recs), time.time() - t0), flush=True)
