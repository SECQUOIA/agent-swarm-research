"""Exact feasible common-mesh optimization on certified TU continuous fibers.

Objective is constant + b'x + x'Hx/2. Native discrete domains are explicit
integer label sets. Certificates retain the complete original-domain history.
Only the standard library and the shared finite-tree DP are required.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, lcm, prod
from time import perf_counter

from certified_grid import BoxQP, rational
from finite_dp import solve_tree
from rational_optimization import is_psd


def rref(rows, ncols):
    a = [list(map(F, row)) for row in rows]
    pivots = []
    for col in range(ncols):
        pivot = next((i for i in range(len(pivots), len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        k = len(pivots)
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][col]
        a[k] = [v / scale for v in a[k]]
        for i in range(len(a)):
            if i != k and a[i][col]:
                scale = a[i][col]
                a[i] = [v - scale * w for v, w in zip(a[i], a[k])]
        pivots.append(col)
    return a, pivots


def unique_solution(matrix, rhs):
    n = len(rhs)
    a, pivots = rref([list(row) + [v] for row, v in zip(matrix, rhs)], n)
    if len(pivots) != n:
        return None
    return tuple(a[i][-1] for i in range(n))


def determinant(matrix):
    a = [list(map(F, row)) for row in matrix]
    result = F(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[j], a[p] = a[p], a[j]
            result = -result
        pivot = a[j][j]
        result *= pivot
        for i in range(j + 1, len(a)):
            factor = a[i][j] / pivot
            for k in range(j + 1, len(a)):
                a[i][k] -= factor * a[j][k]
    return result


def nullspace(rows, n):
    a, pivots = rref(rows, n)
    basis = []
    for j in range(n):
        if j in pivots:
            continue
        v = [F(0)] * n
        v[j] = F(1)
        for i, p in enumerate(pivots):
            v[p] = -a[i][j]
        basis.append(v)
    return basis


def verify_tu(matrix, certificate, max_minors=100000):
    """Check a sufficient structural certificate or every square minor.

    The limit is a verifier policy, never taken from an untrusted certificate.
    Row sign changes preserve TU. For consecutive ones, column sign changes
    make every nonempty column a contiguous block of ones in the supplied order.
    """
    m, n = len(matrix), len(matrix[0]) if matrix else 0
    if any(v not in (-1, 0, 1) for row in matrix for v in row):
        raise ValueError("continuous matrix is not TU: entry outside {-1,0,1}")
    kind = certificate.get("kind")
    signs = certificate.get("row_signs", [1] * m)
    if len(signs) != m or any(type(v) is not int or v not in (-1, 1) for v in signs):
        raise ValueError("invalid TU row signs")
    a = [[signs[i] * v for v in row] for i, row in enumerate(matrix)]
    if kind == "network":
        for j in range(n):
            nonzero = [a[i][j] for i in range(m) if a[i][j]]
            if len(nonzero) > 2 or (len(nonzero) == 2 and sum(nonzero) != 0):
                raise ValueError("network TU certificate failed")
    elif kind == "consecutive_ones":
        order = certificate.get("row_order", list(range(m)))
        if len(order) != m or any(type(i) is not int for i in order) or sorted(order) != list(range(m)):
            raise ValueError("invalid consecutive-ones row order")
        for j in range(n):
            indices = [k for k, i in enumerate(order) if a[i][j]]
            if indices and (indices[-1] - indices[0] + 1 != len(indices)
                            or len({a[order[k]][j] for k in indices}) != 1):
                raise ValueError("consecutive-ones TU certificate failed")
    elif kind == "all_minors":
        count = sum(comb(m, k) * comb(n, k) for k in range(1, min(m, n) + 1))
        if count > max_minors:
            raise ValueError("TU minor-verification budget exceeded")
        for k in range(1, min(m, n) + 1):
            for rows in combinations(range(m), k):
                for cols in combinations(range(n), k):
                    if determinant([[a[i][j] for j in cols] for i in rows]) not in (-1, 0, 1):
                        raise ValueError("non-TU square minor")
    else:
        raise ValueError("unsupported TU certificate kind")


@dataclass
class ConstrainedQP:
    H: object
    b: object
    bounds: object
    labels: object
    rows: object
    rhs: object
    senses: object
    bags: object
    edges: object
    tu_certificate: object
    curvature: object = None
    constant: object = 0
    name: str = "tu_qp"
    max_tu_minors: int = 100000

    def __post_init__(self):
        if not isinstance(self.labels, dict):
            raise ValueError("labels must map coordinate indices to integer lists")
        labels = {}
        for key, values in self.labels.items():
            if type(key) is not int or key in labels:
                raise ValueError("invalid label coordinate")
            vals = tuple(rational(v) for v in values)
            if not vals or any(v.denominator != 1 for v in vals) or len(set(vals)) != len(vals):
                raise ValueError("labels must be distinct integers")
            labels[key] = tuple(sorted(vals))
        self.box = BoxQP(self.H, self.b, self.bounds, labels, self.bags,
                         self.edges, self.constant, self.name)
        self.H, self.b, self.bounds = self.box.A, self.box.b, self.box.bounds
        self.bags, self.edges, self.constant = self.box.bags, self.box.edges, self.box.constant
        self.labels = labels
        self.n = len(self.b)
        if any(rational(v).denominator != 1 for pair in self.bounds for v in pair):
            raise ValueError("continuous bounds must be integral for the initial unit mesh")
        # Native labels must lie inside the canonical integer-coordinate bounds.
        for i, values in labels.items():
            if not all(self.bounds[i][0] <= v <= self.bounds[i][1] for v in values):
                raise ValueError("label outside coordinate bounds")
        self.continuous = tuple(i for i in range(self.n) if i not in labels)
        self.rows = tuple(tuple(rational(v) for v in row) for row in self.rows)
        self.rhs = tuple(rational(v) for v in self.rhs)
        self.senses = tuple(self.senses)
        if len(self.rows) != len(self.rhs) or len(self.rows) != len(self.senses):
            raise ValueError("constraint dimensions disagree")
        if any(len(row) != self.n for row in self.rows):
            raise ValueError("constraint row has wrong length")
        if any(v.denominator != 1 for row in self.rows for v in row) or any(v.denominator != 1 for v in self.rhs):
            raise ValueError("constraint matrix and right sides must be integral")
        if any(s not in ("<=", "==") for s in self.senses):
            raise ValueError("constraint senses must be <= or ==")
        self.row_home = []
        for row in self.rows:
            scope = {i for i, v in enumerate(row) if v}
            home = next((t for t, bag in enumerate(self.bags) if scope <= set(bag)), None)
            if home is None:
                raise ValueError("a constraint scope is not covered by a bag")
            self.row_home.append(home)
        a = [[row[i] for i in self.continuous] for row in self.rows]
        verify_tu(a, self.tu_certificate, self.max_tu_minors)
        if self.curvature is None:
            upper = max((sum(abs(self.H[i][j]) for j in self.continuous)
                         for i in self.continuous), default=F(0))
            self.curvature = {"L": str(upper), "mode": "full"}
        self.L = rational(self.curvature["L"])
        if self.L < 0 or self.curvature.get("mode") not in ("full", "equalities"):
            raise ValueError("invalid curvature certificate")
        c = len(self.continuous)
        basis = [[F(i == j) for i in range(c)] for j in range(c)]
        if self.curvature["mode"] == "equalities":
            equalities = [[row[i] for i in self.continuous]
                          for row, sense in zip(self.rows, self.senses) if sense == "=="]
            basis = nullspace(equalities, c)
        residual = [[self.L * F(i == j) - self.H[u][v]
                     for j, v in enumerate(self.continuous)]
                    for i, u in enumerate(self.continuous)]
        projected = [[sum((a[i] * residual[i][j] * b[j]
                           for i in range(c) for j in range(c)), F(0))
                      for b in basis] for a in basis]
        if not is_psd(projected):
            raise ValueError("curvature upper bound failed exact PSD verification")
        self.curvature = {"L": str(self.L), "mode": self.curvature["mode"]}

    def value(self, point):
        return self.box.value(point)

    def feasible(self, point):
        if len(point) != self.n or not all(lo <= x <= hi for x, (lo, hi) in zip(point, self.bounds)):
            return False
        if any(point[i] not in labels for i, labels in self.labels.items()):
            return False
        for row, rhs, sense in zip(self.rows, self.rhs, self.senses):
            value = sum((v * x for v, x in zip(row, point)), F(0))
            if (sense == "==" and value != rhs) or (sense == "<=" and value > rhs):
                return False
        return True

    def local_value(self, bag_number, assignment):
        for k, (row, rhs, sense) in enumerate(zip(self.rows, self.rhs, self.senses)):
            if self.row_home[k] == bag_number:
                value = sum((row[i] * assignment[i] for i in assignment), F(0))
                if (sense == "==" and value != rhs) or (sense == "<=" and value > rhs):
                    return None
        value = self.constant if bag_number == 0 else F(0)
        for i in self.bags[bag_number]:
            if self.box.home[i] == bag_number:
                x = assignment[i]
                value += self.H[i][i] * x*x / 2 + self.b[i] * x
        for home, (i, j, a) in zip(self.box.factor_home, self.box.interactions):
            if home == bag_number:
                value += a * assignment[i] * assignment[j]
        return value

    def to_dict(self):
        return {"H": [[str(v) for v in row] for row in self.H],
                "b": list(map(str, self.b)), "bounds": [[str(v) for v in pair] for pair in self.bounds],
                "labels": {str(i): list(map(str, vals)) for i, vals in self.labels.items()},
                "rows": [[str(v) for v in row] for row in self.rows], "rhs": list(map(str, self.rhs)),
                "senses": list(self.senses), "bags": list(map(list, self.bags)),
                "edges": list(map(list, self.edges)), "tu_certificate": self.tu_certificate,
                "curvature": self.curvature, "constant": str(self.constant), "name": self.name}

    @classmethod
    def from_dict(cls, data, max_tu_minors=100000):
        args = dict(data)
        labels = args["labels"]
        if any(not isinstance(k, str) or str(int(k)) != k for k in labels):
            raise ValueError("noncanonical label index")
        args["labels"] = {int(k): v for k, v in labels.items()}
        args["max_tu_minors"] = max_tu_minors
        return cls(**args)


def height_bound(problem):
    """Common denominator bounds for an ORIGINAL-polytope QP optimum.

    Write F=(x'Qx+c'x+e)/D with integral Q,c,e. On a minimum-dimensional
    optimizer face the tangent Hessian is positive definite, so a nonsingular
    original-face KKT system of size <=2*n_c gives a common denominator R.
    Its integral entries have magnitude <=max(1,2*max|Q_cc|). Label magnitudes
    and right sides affect numerators, not this determinant bound.
    """
    D = lcm(*(v.denominator for row in problem.H for v in (x/2 for x in row)),
            *(v.denominator for v in problem.b), problem.constant.denominator)
    n = len(problem.continuous)
    M = max([1] + [abs(int(D * problem.H[i][j]))
                    for i in problem.continuous for j in problem.continuous])
    R = (2*n*M)**(2*n) if n else 1
    return {"D": D, "R": R, "V": D*R*R}


def uniform_grid(lo, hi, mesh):
    if (lo / mesh).denominator != 1 or (hi / mesh).denominator != 1:
        raise ValueError("retained bounds are not aligned to the common mesh")
    return tuple(mesh * k for k in range(int(lo/mesh), int(hi/mesh) + 1))


def filter_state(problem, grids, marginals, upper, error):
    state = []
    for i, grid in enumerate(grids):
        good = [v is not None and v - error <= upper for v in marginals[i]]
        if i in problem.labels:
            kept = tuple(x for x, keep in zip(grid, good) if keep)
        elif len(grid) == 1:
            kept = (grid[0], grid[0]) if good[0] else ()
        else:
            intervals = [k for k in range(len(grid)-1) if good[k] or good[k+1]]
            kept = (grid[intervals[0]], grid[intervals[-1]+1]) if intervals else ()
        if not kept:
            raise ArithmeticError("filter unexpectedly removed every optimizer")
        state.append(kept)
    return tuple(state)


def _face_candidates(problem, labels, check):
    """Original-face stationary points; yields None for singular/infeasible faces."""
    continuous, n = problem.continuous, len(problem.continuous)
    if not n:
        point = tuple(labels[i] for i in range(problem.n))
        yield point if problem.feasible(point) else None
        return
    eq, ineq = [], []
    for row, rhs, sense in zip(problem.rows, problem.rhs, problem.senses):
        target = rhs - sum((row[i] * labels[i] for i in labels), F(0))
        pair = ([row[i] for i in continuous], target)
        (eq if sense == "==" else ineq).append(pair)
    for j, i in enumerate(continuous):
        row = [F(k == j) for k in range(n)]
        ineq.extend([(row, problem.bounds[i][1]), ([-v for v in row], -problem.bounds[i][0])])
    independent = []
    rank = 0
    for pair in eq:
        newrank = len(rref([r for r, _ in independent] + [pair[0]], n)[1])
        if newrank > rank:
            independent.append(pair)
            rank = newrank
    linear = [problem.b[i] + sum((problem.H[i][j] * labels[j] for j in labels), F(0))
              for i in continuous]
    for size in range(n - rank + 1):
        for selection in combinations(ineq, size):
            check()
            active = independent + list(selection)
            k = len(active)
            matrix = [[problem.H[i][j] for j in continuous] + [row[u] for row, _ in active]
                      for u, i in enumerate(continuous)]
            matrix += [list(row) + [F(0)]*k for row, _ in active]
            rhs = [-v for v in linear] + [v for _, v in active]
            solution = unique_solution(matrix, rhs)
            point = dict(labels)
            if solution is not None:
                point.update(zip(continuous, solution[:n]))
                candidate = tuple(point[i] for i in range(problem.n))
                if problem.feasible(candidate):
                    yield candidate
                    continue
            yield None


def _encode_messages(messages):
    return [{"from": u, "to": v,
             "rows": [{"indices": list(key), "value": None if value is None else str(value)}
                      for key, value in sorted(rows.items())]}
            for (u, v), rows in sorted(messages.items())]


class _Limit(Exception):
    pass


def solve(problem, epsilon="1/1024", *, exact=False, max_stages=128,
          max_table_states=100000, time_limit=30, max_exact_faces=10000):
    """Return a JSON-serializable certificate, including explicit limit outcomes.

    Exact reconstruction terminates on unique QPs absent resource limits. The
    optional bounded original-face search also handles many nonunique cases;
    exhausting it never certifies optimality or emptiness.
    """
    epsilon = rational(epsilon)
    if epsilon < 0 or type(exact) is not bool:
        raise ValueError("invalid accuracy request")
    if any(type(x) is not int or x <= 0 for x in (max_stages, max_table_states)):
        raise ValueError("stage and table limits must be positive integers")
    if type(max_exact_faces) is not int or max_exact_faces < 0 or time_limit <= 0:
        raise ValueError("invalid face or time limit")
    started = perf_counter()

    def check():
        if perf_counter() - started > time_limit:
            raise _Limit("time limit")

    certificate = {"schema": "tu-constrained-grid-v1", "problem": problem.to_dict(),
                   "request": {"epsilon": str(epsilon), "exact": exact}, "stages": [],
                   "status": "limit", "reason": "stage limit", "point": None,
                   "lower": None, "upper": None, "exact_proof": None}
    state = tuple(problem.labels[i] if i in problem.labels else problem.bounds[i]
                  for i in range(problem.n))
    lower = upper = None
    incumbent = None
    height = height_bound(problem)
    faces = 0
    searched_labels = set()
    candidates = []
    try:
        for level in range(max_stages):
            check()
            h = F(1, 2**level)
            sizes = [len(state[i]) if i in problem.labels else int((state[i][1]-state[i][0])/h)+1
                     for i in range(problem.n)]
            states = sum(prod(sizes[i] for i in bag) for bag in problem.bags)
            if states > max_table_states:
                raise _Limit("table-state limit")
            grids = tuple(tuple(state[i]) if i in problem.labels else uniform_grid(*state[i], h)
                          for i in range(problem.n))
            tables = []
            for t, bag in enumerate(problem.bags):
                table = {}
                for number, indices in enumerate(product(*(range(sizes[i]) for i in bag))):
                    if number % 128 == 0:
                        check()
                    assignment = {i: grids[i][k] for i, k in zip(bag, indices)}
                    table[indices] = problem.local_value(t, assignment)
                tables.append(table)
            result = solve_tree(problem.bags, problem.edges, sizes, tables, check=check)
            stage = {"level": level, "grids": [list(map(str, row)) for row in grids],
                     "table_states": states, "messages": _encode_messages(result["messages"])}
            if result["lower"] is None:
                if level:
                    raise ArithmeticError("a later feasible grid vanished")
                stage["infeasible"] = True
                certificate["stages"].append(stage)
                certificate["status"], certificate["reason"] = "infeasible", "initial TU fiber grid is empty"
                break
            value = result["lower"]
            point = tuple(grids[i][k] for i, k in enumerate(result["point_indices"]))
            if upper is None or value < upper:
                upper, incumbent = value, point
            error = len(problem.continuous)*problem.L*h*h/8
            lower = max(value-error, lower) if lower is not None else value-error
            state = filter_state(problem, grids, result["marginals"], upper, error)
            stage.update({"point": list(map(str, point)), "grid_value": str(value),
                          "error": str(error), "lower": str(lower), "upper": str(upper),
                          "min_marginals": [[None if v is None else str(v) for v in row]
                                            for row in result["marginals"]],
                          "retained": [list(map(str, row)) for row in state]})
            certificate["stages"].append(stage)
            if lower == upper:
                certificate["status"], certificate["reason"] = "exact", "matching grid bounds"
                break
            if exact:
                # Candidate generation is untrusted; only the final feasibility
                # and rational-separation check can certify its global value.
                tentative = [None] * problem.n
                for i in range(problem.n):
                    tentative[i] = point[i] if i in problem.labels else ((state[i][0]+state[i][1])/2).limit_denominator(height["R"])
                candidate = tuple(tentative)
                if problem.feasible(candidate):
                    candidates.append(candidate)
                label_key = tuple((i, point[i]) for i in sorted(problem.labels))
                if label_key not in searched_labels and faces < max_exact_faces:
                    searched_labels.add(label_key)
                    for candidate in _face_candidates(problem, dict(label_key), check):
                        faces += 1
                        if candidate is not None:
                            candidates.append(candidate)
                        if faces >= max_exact_faces:
                            break
                if candidates:
                    candidate = min(candidates, key=problem.value)
                    candidates = [candidate]
                    value = problem.value(candidate)
                    if value >= lower and value-lower < F(1, value.denominator*height["V"]):
                        certificate["exact_proof"] = {"kind": "rational_separation", "point": list(map(str, candidate)),
                                                       "height": height, "comparison_lower": str(lower)}
                        lower = upper = value
                        incumbent = candidate
                        certificate["status"], certificate["reason"] = "exact", "original-face rational value separation"
                        break
            elif upper-lower <= epsilon:
                certificate["status"], certificate["reason"] = "epsilon", "requested certified gap"
                break
    except _Limit as exc:
        certificate["reason"] = str(exc)
    certificate.update({"point": None if incumbent is None else list(map(str, incumbent)),
                        "lower": None if lower is None else str(lower),
                        "upper": None if upper is None else str(upper),
                        "statistics": {"seconds": perf_counter()-started, "exact_faces_attempted": faces,
                                       "total_table_states": sum(s["table_states"] for s in certificate["stages"])}})
    return certificate
