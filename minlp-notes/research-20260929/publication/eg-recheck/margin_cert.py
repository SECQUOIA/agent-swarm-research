"""Reviewer's independent certifier (reviews/eg-retry-review-checks/indep_cert.py, imported
unchanged) with margin recording added.

MarginCertifier overrides three methods of indep_cert.Certifier with copies of the originals.
The only changes record, for every certified piece, the certificate used and its margin
(certified lower bound minus theta*), and return them to the caller.  Every changed or added
line ends with '# MARGIN'; check_copy.py prints the diff against the originals.  The
certification decisions (which certificate applies, the exact rational tests, the splitting)
are unchanged.

Margin of a piece:
  * row certificate: max_k (c_k + rmin_k) - theta* over the 24 objective rows (exact);
  * LP certificate: (weak-duality bound) - theta* (exact);
  * side-row infeasibility, Farkas certificate, empty box: +inf (no feasible point).
Margin of a leaf: the minimum over the pieces that certified it.  A leaf that was not
certified gets -inf.
Certificate codes (how): 0 row, 1 side, 2 lp, 3 farkas, 4 empty, 5 certified after splitting.
"""
import os
import sys

import numpy as np

REV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "reviews", "eg-retry-review-checks")
sys.path.insert(0, REV)
import indep_cert  # noqa: E402
from indep_cert import Certifier, F, lin_min_exact  # noqa: E402,F401

INF = np.inf


class MarginCertifier(Certifier):

    def certify_batch(self, lo, hi):
        """returns a boolean array: True where the box was certified (possibly after splitting)."""
        ok, mg, how = self._batch(lo, hi, 0)  # MARGIN
        self.stats["fail"] += int((~ok).sum())
        self.last_mg, self.last_how = mg, how  # MARGIN
        return ok

    def _batch(self, lo, hi, depth):
        M = self.M
        N = len(lo)
        self.stats["pieces"] += N
        ok = np.zeros(N, bool)
        mg = np.full(N, -INF)  # MARGIN
        how = np.full(N, -1, dtype=np.int8)  # MARGIN
        todo = []
        for s in range(0, N, 64):
            l_, h_ = lo[s:s + 64], hi[s:s + 64]
            c, r, beta, aL, aU = M.taylor(l_, h_)
            nlo, nhi = M.natural(l_, h_)
            for j in range(len(l_)):
                if self._one(l_[j], h_[j], c[j], beta[j], aL[j], aU[j], nlo[j], nhi[j]):
                    ok[s + j] = True
                    mg[s + j], how[s + j] = self._last  # MARGIN
                else:
                    todo.append(s + j)
        if todo and depth < self.max_depth and self.stats["pieces"] < self.max_pieces:
            clo, chi, owner = [], [], []
            for n in todo:
                for a, b in self._split(lo[n], hi[n]):
                    clo.append(a); chi.append(b); owner.append(n)
                self.stats["split"] += 1
            sub, submg, _ = self._batch(np.array(clo), np.array(chi), depth + 1)  # MARGIN
            owner = np.array(owner)
            for n in todo:
                ok[n] = bool(sub[owner == n].all())
                if ok[n]:  # MARGIN
                    mg[n], how[n] = submg[owner == n].min(), 5  # MARGIN
        return ok, mg, how  # MARGIN

    def _one(self, lo, hi, c, beta, aL, aU, nlo, nhi):
        """try the certificates on one box; exact rational arithmetic."""
        M = self.M
        th = self.theta
        if np.any(lo > hi):
            self.stats["empty"] += 1
            self._last = (INF, 4)  # MARGIN
            return True
        dl = [F(a) - F(b) for a, b in zip(lo, c)]
        dh = [F(a) - F(b) for a, b in zip(hi, c)]
        Bq = [[F(v) for v in beta[k]] for k in range(28)]
        # lower / upper bounds of each row over the box (affine or natural)
        rmin, rmax = [], []
        for k in range(28):
            lo_k = F(aL[k]) + lin_min_exact(Bq[k], dl, dh) if np.isfinite(aL[k]) else None
            hi_k = F(aU[k]) - lin_min_exact([-b for b in Bq[k]], dl, dh) if np.isfinite(aU[k]) else None
            nl, nh = F(nlo[k]) if np.isfinite(nlo[k]) else None, F(nhi[k]) if np.isfinite(nhi[k]) else None
            rmin.append(max([v for v in (lo_k, nl) if v is not None], default=None))
            rmax.append(min([v for v in (hi_k, nh) if v is not None], default=None))
        for k in range(24):
            if rmin[k] is not None and M.qc[k] + rmin[k] >= th:
                self.stats["row"] += 1
                best = max(M.qc[j] + rmin[j] for j in range(24) if rmin[j] is not None)  # MARGIN
                self._last = (float(best - th), 0)  # MARGIN
                return True
        for j in range(4):
            k = 24 + j
            if M.qghi[j] is not None and rmin[k] is not None and rmin[k] > M.qghi[j]:
                self.stats["side"] += 1
                self._last = (INF, 1)  # MARGIN
                return True
            if M.qglo[j] is not None and rmax[k] is not None and rmax[k] < M.qglo[j]:
                self.stats["side"] += 1
                self._last = (INF, 1)  # MARGIN
                return True
        # LP over the affine models (float data only proposes multipliers)
        rows, rhs, tags = [], [], []
        for k in range(24):
            if np.isfinite(aL[k]):
                rows.append(list(beta[k]) + [-1.0]); rhs.append(-(M.c[k] + aL[k])); tags.append(("obj", k))
        for j in range(4):
            k = 24 + j
            if M.qghi[j] is not None and np.isfinite(aL[k]):
                rows.append(list(beta[k]) + [0.0]); rhs.append(M.ghi[j] - aL[k]); tags.append(("up", k))
            if M.qglo[j] is not None and np.isfinite(aU[k]):
                rows.append(list(-beta[k]) + [0.0]); rhs.append(aU[k] - M.glo[j]); tags.append(("lo", k))
        if not any(t[0] == "obj" for t in tags):
            return False
        bounds = [(float(a), float(b)) for a, b in zip(dl, dh)] + [(None, None)]
        cost = np.zeros(M.d + 1); cost[-1] = 1.0
        res = indep_cert.linprog(cost, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=bounds, method="highs")  # MARGIN
        if res.status == 0:
            y = np.maximum(-np.asarray(res.ineqlin.marginals), 0.0)
            v = self._dual_value(y, tags, Bq, aL, aU, dl, dh)
            if v is not None and v >= th:
                self._margin(v)
                self.stats["lp"] += 1
                self._last = (float(v - th), 2)  # MARGIN
                return True
            return False
        if res.status == 2:
            # Farkas: side rows and objective cuts c_k + aL_k + beta_k . d <= theta*
            rows2, rhs2, tags2 = [], [], []
            for k in range(24):
                if np.isfinite(aL[k]):
                    rows2.append(list(beta[k]) + [-1.0]); rhs2.append(float(th) - M.c[k] - aL[k]); tags2.append(("cut", k))
            for (kind, k), row, b in zip(tags, rows, rhs):
                if kind != "obj":
                    rows2.append(row[:-1] + [-1.0]); rhs2.append(b); tags2.append((kind, k))
            res2 = indep_cert.linprog(cost, A_ub=np.array(rows2), b_ub=np.array(rhs2), bounds=bounds, method="highs")  # MARGIN
            if res2.status == 0:
                z = np.maximum(-np.asarray(res2.ineqlin.marginals), 0.0)
                if self._farkas(z, tags2, Bq, aL, aU, dl, dh):
                    self.stats["farkas"] += 1
                    self._last = (INF, 3)  # MARGIN
                    return True
        return False
