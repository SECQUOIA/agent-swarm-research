"""Small diagnostic QPs and two unmodified, compatible QPLIB inputs.

All problems minimize 0.5*x'A*x + b'x + c.  Decimal source values are read
as exact rationals.  This module deliberately does not import the solver.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
from time import perf_counter


@dataclass
class Instance:
    name: str
    A: list
    b: list
    bounds: list
    integers: set
    c: F = F(0)
    description: str = ""
    source: str = "generated diagnostic"


def value(p, x):
    return p.c + sum((p.b[i] * x[i] + p.A[i][i] * x[i] ** 2 / 2
                      for i in range(len(x))), F(0)) + sum(
        (p.A[i][j] * x[i] * x[j]
         for i in range(len(x)) for j in range(i)), F(0))


def matrix(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def random_band(name, n, width, seed, integers=()):
    rng = Random(seed)
    a = matrix(n)
    for i in range(n):
        a[i][i] = F(rng.randint(-2, 4), 3)
        for j in range(max(0, i - width), i):
            a[i][j] = a[j][i] = F(rng.choice([-3, -2, -1, 1, 2, 3]), 3)
    b = [F(rng.randint(-4, 4), 5) for _ in range(n)]
    return Instance(name, a, b, [(F(-1), F(1))] * n, set(integers),
                    description=f"Seed {seed}; random signed band width {width}; no planted solution")


def generated_instances():
    cases = [random_band("random_path", 5, 1, 19),
             random_band("random_width2", 5, 2, 23),
             random_band("random_width3", 5, 3, 29),
             random_band("mixed_path", 5, 1, 31, (0, 3)),
             random_band("integer_path", 8, 1, 37, range(8))]
    branch = random_band("random_branch", 6, 1, 41)
    rng = Random(43)
    for i in range(6):
        for j in range(i):
            branch.A[i][j] = branch.A[j][i] = F(0)
    for i, j in ((0, 1), (0, 2), (0, 3), (3, 4), (3, 5)):
        branch.A[i][j] = branch.A[j][i] = F(rng.choice([-3, -2, -1, 1, 2, 3]), 3)
    branch.description = "Random coefficients on a branching tree; no planted solution"
    cases.append(branch)
    a = matrix(4)
    for i in range(3):
        a[i][i] += 2
        a[i + 1][i + 1] += 2
        a[i][i + 1] = a[i + 1][i] = F(-2)
    cases.append(Instance("flat_optimal_line", a, [F(0)] * 4,
                          [(F(-1), F(1))] * 4, set(),
                          description="Convex chain energy; all constant vectors are optimal"))
    a = matrix(4)
    a[0][0] = F(-2)
    a[1][1] = a[2][2] = F(2)
    a[1][2] = a[2][1] = F(-2)
    cases.append(Instance("tied_and_flat", a, [F(0)] * 4,
                          [(F(-1), F(1))] * 4, set(),
                          description="Two concave endpoints, a flat coupled pair, and a free variable"))
    for scale in (1, 256):
        a = matrix(4)
        a[0][0] = F(-1, 100)
        a[0][1] = a[1][0] = F(1, 20)
        for i in range(1, 4):
            a[i][i] = F(2 * scale)
        for i in (1, 2):
            a[i][i + 1] = a[i + 1][i] = F(-scale, 2)
        b = [F(0), F(-scale, 3), F(scale, 5), F(-scale, 7)]
        cases.append(Instance(f"near_convex_scale{scale}", a, b,
                              [(F(-1), F(1))] * 4, set(),
                              description="Same weak negative direction; positive block scaled by " + str(scale)))
    return cases


def read_qbn(code):
    """Read only the exact QBN format represented by these bundled files.

    QPLIB stores lower-triangular quadratic coefficients in 0.5*x'Q*x;
    hence an off-diagonal file coefficient is halved in symmetric A.
    Maximization is converted to minimization by negating the objective.
    """
    path = Path(__file__).parent / "data" / f"QPLIB_{code}.qplib"
    lines = iter(line.split("#", 1)[0].strip() for line in path.read_text().splitlines()
                 if line.split("#", 1)[0].strip())
    name, kind, sense = next(lines), next(lines), next(lines)
    assert kind == "QBN" and sense == "maximize", (kind, sense)
    n = int(next(lines))
    a = matrix(n)
    for _ in range(int(next(lines))):
        i, j, coefficient = next(lines).split()
        i, j, coefficient = int(i) - 1, int(j) - 1, F(coefficient)
        assert i >= j and not a[i][j]
        a[i][j] = a[j][i] = -coefficient / (1 if i == j else 2)
    b = [-F(next(lines))] * n
    for _ in range(int(next(lines))):
        i, coefficient = next(lines).split()
        b[int(i) - 1] = -F(coefficient)
    p = Instance(name, a, b, [(F(0), F(1))] * n, set(range(n)), -F(next(lines)),
                 "Unmodified objective and binary domain; sense reversed for minimization",
                 f"https://qplib.zib.de/QPLIB_{code}.html")
    # Independent file-format fidelity check against the library's supplied
    # feasible solution. Its value is an incumbent, not an optimum claim.
    solution = [F(0)] * n
    expected = None
    for line in path.with_suffix(".sol").read_text().splitlines():
        variable, number = line.split()
        if variable == "objvar":
            expected = -F(number)
        else:
            assert variable.startswith("b")
            solution[int(variable[1:]) - 2] = F(number)
    assert all(x in (0, 1) for x in solution)
    assert expected is not None and value(p, solution) == expected
    return p


def minimum_degree_decomposition(p):
    """A deterministic valid decomposition, with no claim of optimal width."""
    n = len(p.b)
    graph = {i: {j for j in range(n) if i != j and p.A[i][j]} for i in range(n)}
    bags, order = [], []
    while graph:
        v = min(graph, key=lambda i: (len(graph[i]), i))
        neighbors = graph[v]
        bags.append(tuple(sorted({v} | neighbors)))
        order.append(v)
        for u in neighbors:
            graph[u].update(neighbors - {u})
            graph[u].remove(v)
        del graph[v]
    positions = {v: i for i, v in enumerate(order)}
    roots, edges = [], []
    for i, bag in enumerate(bags):
        later = [positions[v] for v in bag if positions[v] > i]
        if later:
            edges.append((i, min(later)))
        else:
            roots.append(i)
    edges.extend(zip(roots, roots[1:]))
    return bags, edges


def linear_solve(a, b):
    n = len(b)
    aug = [list(row) + [rhs] for row, rhs in zip(a, b)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        if pivot is None:
            return None
        aug[j], aug[pivot] = aug[pivot], aug[j]
        divisor = aug[j][j]
        aug[j] = [x / divisor for x in aug[j]]
        for i in range(n):
            if i != j:
                factor = aug[i][j]
                aug[i] = [x - factor * y for x, y in zip(aug[i], aug[j])]
    return [aug[i][-1] for i in range(n)]


def exact_face_minimum(p):
    """Exponential independent oracle for small box MIQP only.

    Enumerate integer assignments and all continuous faces. A minimum in
    the interior of a singular stationary face can move along a null
    vector at constant value until reaching a lower-dimensional face.
    Thus nonsingular stationary faces and vertices include a minimizer.
    """
    start = perf_counter()
    n = len(p.b)
    assert n <= 8, "The exact reference is deliberately restricted to small cases"
    integers = sorted(p.integers)
    continuous = [i for i in range(n) if i not in p.integers]
    best, witness, visited = None, None, 0
    ranges = [range(int(p.bounds[i][0]), int(p.bounds[i][1]) + 1) for i in integers]
    for assignment in product(*ranges):
        integer_fixed = dict(zip(integers, map(F, assignment)))
        for face in product((-1, 0, 1), repeat=len(continuous)):
            visited += 1
            fixed = dict(integer_fixed)
            free = []
            for i, side in zip(continuous, face):
                if side:
                    fixed[i] = p.bounds[i][0 if side < 0 else 1]
                else:
                    free.append(i)
            stationary = linear_solve(
                [[p.A[i][j] for j in free] for i in free],
                [-p.b[i] - sum((p.A[i][j] * x for j, x in fixed.items()), F(0))
                 for i in free])
            if stationary is None:
                continue
            fixed.update(zip(free, stationary))
            x = tuple(fixed[i] for i in range(n))
            if any(not lo <= xi <= hi for xi, (lo, hi) in zip(x, p.bounds)):
                continue
            objective = value(p, x)
            if best is None or objective < best:
                best, witness = objective, x
    assert best is not None
    return {"objective": str(best), "point": list(map(str, witness)),
            "faces_visited": visited, "seconds": perf_counter() - start}


def instances(include_qplib=True):
    result = generated_instances()
    if include_qplib:
        result += [read_qbn("3852"), read_qbn("5881")]
    return {p.name: p for p in result}
