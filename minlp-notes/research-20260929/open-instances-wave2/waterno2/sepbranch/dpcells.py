"""Cells on the tank-level links of waterno2_T and the dynamic program over them.

For every link t (period t -> t+1) the cells form a binary tree rooted at the
level box of the link (core.level_box).  The leaves are the current cells.
For every period t a table holds one number per pair (entry leaf of link t-1,
exit leaf of link t); period 0 has the single entry "fixed start" and the last
period the single exit "free end".

The tables used:
  EST  planning values (SCIP primal values of the pair subproblems; +inf when
       SCIP reports the pair infeasible).  Not bounds.  ESRC: the record the
       value comes from; EOWN: the record evaluated on exactly this pair (-1
       if the value is inherited from an ancestor pair).
  CB   certified lower bounds (rbb).  CSRC: the certification record.

Shortest path:  V = min over leaf sequences of sum_t table_t(D_{t-1}, D_t).
"""
import math

import numpy as np

INF = math.inf


class CellPlan:
    def __init__(self, T, lam, mu, boxes):
        self.T, self.lam, self.mu = T, [list(map(float, l)) for l in lam], float(mu)
        self.cells = [[dict(lo=list(map(float, lo)), hi=list(map(float, hi)), parent=None, split=None)]
                      for (lo, hi) in boxes]
        self.leaves = [[0] for _ in range(T - 1)]
        self.tables = {}
        self.erecs = []
        self.crecs = []
        for name, fill, dt in (("EST", np.nan, float), ("ESRC", -1, np.int64), ("EOWN", -1, np.int64),
                               ("CB", -INF, float), ("CSRC", -1, np.int64)):
            self.tables[name] = [np.full((1, 1), fill, dtype=dt) for _ in range(T)]
        self.fills = {"EST": np.nan, "ESRC": -1, "EOWN": -1, "CB": -INF, "CSRC": -1}
        self.own_tables = ("EOWN",)   # reset to fill for split children

    # ------------------------------------------------------------ cells
    def cell_box(self, link, cid):
        if cid < 0:
            return None
        c = self.cells[link][cid]
        return (list(c["lo"]), list(c["hi"]))

    def leaf_id(self, link, pos):
        if link < 0 or link >= self.T - 1:
            return -1
        return self.leaves[link][pos]

    def split(self, link, pos, k, m):
        cid = self.leaves[link][pos]
        c = self.cells[link][cid]
        assert c["lo"][k] < m < c["hi"][k]
        lo1, hi1 = list(c["lo"]), list(c["hi"])
        hi1[k] = float(m)
        lo2, hi2 = list(c["lo"]), list(c["hi"])
        lo2[k] = float(m)
        n = len(self.cells[link])
        self.cells[link].append(dict(lo=lo1, hi=hi1, parent=cid, split=None))
        self.cells[link].append(dict(lo=lo2, hi=hi2, parent=cid, split=None))
        c["split"] = (k, float(m), n, n + 1)
        self.leaves[link][pos] = n
        self.leaves[link].append(n + 1)
        for name, tabs in self.tables.items():
            reset = name in self.own_tables
            t = link          # period `link`: exit cell = columns
            A = tabs[t]
            col = A[:, pos:pos + 1].copy()
            if reset:
                A[:, pos] = self.fills[name]
                col[:] = self.fills[name]
            tabs[t] = np.hstack([A, col])
            t = link + 1      # period link+1: entry cell = rows
            A = tabs[t]
            row = A[pos:pos + 1, :].copy()
            if reset:
                A[pos, :] = self.fills[name]
                row[:] = self.fills[name]
            tabs[t] = np.vstack([A, row])
        return n, n + 1

    def grid(self, link, breaks):
        """Split every leaf of `link` at the given breakpoints (breaks[k]: list)."""
        for k in range(3):
            for m in breaks[k]:
                changed = True
                while changed:
                    changed = False
                    for pos, cid in enumerate(self.leaves[link]):
                        c = self.cells[link][cid]
                        if c["lo"][k] < m < c["hi"][k]:
                            self.split(link, pos, k, m)
                            changed = True
                            break

    def is_ancestor(self, link, a, b):
        """a is an ancestor of (or equal to) b."""
        if link < 0 or link >= self.T - 1:
            return a == b == -1
        while b is not None:
            if b == a:
                return True
            b = self.cells[link][b]["parent"]
        return False

    def leaf_positions_under(self, link, cid):
        if link < 0 or link >= self.T - 1:
            return [0]
        if self.cells[link][cid]["split"] is None:   # a current leaf
            return [self.leaves[link].index(cid)]
        return [p for p, l in enumerate(self.leaves[link]) if self.is_ancestor(link, cid, l)]

    # ------------------------------------------------------------ DP
    def nrow(self, t):
        return 1 if t == 0 else len(self.leaves[t - 1])

    def ncol(self, t):
        return 1 if t == self.T - 1 else len(self.leaves[t])

    def dp(self, name):
        T = self.T
        B = self.tables[name]
        f = [None] * T
        f[0] = B[0][0, :].astype(float)
        for t in range(1, T - 1):
            f[t] = (f[t - 1][:, None] + B[t]).min(axis=0)
        V = float((f[T - 2] + B[T - 1][:, 0]).min())
        g = [None] * T
        g[T - 2] = B[T - 1][:, 0].astype(float)
        for t in range(T - 2, 0, -1):
            g[t - 1] = (B[t] + g[t][None, :]).min(axis=1)
        return V, f, g

    def through(self, t, f, g, name):
        T = self.T
        fin = np.zeros(1) if t == 0 else f[t - 1]
        gout = np.zeros(1) if t == T - 1 else g[t]
        return fin[:, None] + self.tables[name][t] + gout[None, :]

    def best_path(self, f, g, name):
        T = self.T
        B = self.tables[name]
        path = [None] * (T - 1)
        path[T - 2] = int(np.argmin(f[T - 2] + B[T - 1][:, 0]))
        for t in range(T - 2, 0, -1):
            path[t - 1] = int(np.argmin(f[t - 1] + B[t][:, path[t]]))
        return path

    def slopes(self, t):
        lin = self.lam[t - 1] if t > 0 else [0.0, 0.0, 0.0]
        lout = self.lam[t] if t < self.T - 1 else [0.0, 0.0, 0.0]
        return lin, lout
