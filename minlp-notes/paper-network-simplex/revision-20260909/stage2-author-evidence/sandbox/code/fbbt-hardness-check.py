"""Exact arithmetic checks for the FBBT constructions; not a proof substitute."""

from fractions import Fraction as F
import random


class Model:
    def __init__(self):
        self.rows = []
        self.values = {}

    def node(self, op, args=(), value=None):
        name = len(self.rows)
        if op == "product" and args[0] == args[1]:
            copied = self.node("copy", (args[0],))
            args = (args[0], copied)
            name = len(self.rows)
        if value is None:
            vals = [self.values[a] for a in args]
            value = {
                "copy": lambda: vals[0],
                "sum": lambda: sum(vals),
                "average": lambda: sum(vals) / 2,
                "product": lambda: vals[0] * vals[1],
            }[op]()
        self.rows.append((name, op, args))
        self.values[name] = F(value)
        return name

    def pair_product(self, p, r, q, s):
        new_p = self.node("product", (p, q))
        partial = self.node("product", (p, s))
        new_r = self.node("sum", (r, partial))
        return new_p, new_r

    def check(self):
        for lhs, op, args in self.rows:
            assert len({lhs, *args}) <= 3
            assert 0 <= self.values[lhs] <= 1
            if op == "constant":
                assert self.values[lhs] in (0, F(1, 2), 1)
                continue
            vals = [self.values[a] for a in args]
            if op == "product":
                assert args[0] != args[1]
                rhs = vals[0] * vals[1]
            elif op == "average":
                rhs = sum(vals) / 2
            elif op == "sum":
                rhs = sum(vals)
            else:
                assert op == "copy"
                rhs = vals[0]
            assert self.values[lhs] == rhs, (lhs, op, args)

    def largest_scc(self):
        # Reachability suffices for these small audit models, without dependencies.
        adjacency = {lhs: set(args) for lhs, _, args in self.rows}
        reach = {}
        for lhs in adjacency:
            visited, stack = set(), [lhs]
            while stack:
                item = stack.pop()
                if item in visited:
                    continue
                visited.add(item)
                stack.extend(adjacency[item] - visited)
            reach[lhs] = visited
        return max(sum(v in reach[u] and u in reach[v] for v in reach) for u in reach)


def check_random_circuit(rng, depth):
    model = Model()
    zero = model.node("constant", value=0)
    one = model.node("constant", value=1)
    layer = [(zero, one, 0), (one, zero, 1)]
    scale = 1
    for level in range(depth):
        next_layer = []
        for _ in range(8):
            p, r, left = rng.choice(layer)
            q, s, right = rng.choice(layer)
            if level % 2 == 0:
                pair = (model.node("average", (p, q)), model.node("average", (r, s)))
                val = left + right
            else:
                pair = model.pair_product(p, r, q, s)
                val = left * right
            next_layer.append((*pair, val))
        scale = 2 * scale if level % 2 == 0 else scale * scale
        layer = next_layer
        for p, r, val in layer:
            assert model.values[p] == F(val, scale)
            assert model.values[p] + model.values[r] == 1
    p, r, output_u = rng.choice(layer)
    q, s, output_v = rng.choice(layer)
    c = model.node("average", (p, s))
    d = model.node("average", (r, q))
    cval, dval = model.values[c], model.values[d]
    aval = F(1) if cval <= F(1, 2) else dval / cval
    # Insert the feedback rows with their exact fixed-point values.
    a = model.node("sum", (d, -1), value=aval)
    copied_a = model.node("copy", (a,))
    square = model.node("product", (a, copied_a))
    v = model.node("product", (c, square))
    model.rows[a] = (a, "sum", (d, v))
    b = model.node("constant", value=F(1, 2))
    rb = model.node("constant", value=F(1, 2))
    for _ in range(depth + 2):
        b, rb = model.pair_product(b, rb, b, rb)
    bval = model.values[b]
    assert bval == F(1, 2 ** (2 ** (depth + 2)))
    assert bval <= F(1, 8 * scale)
    e = model.node("product", (rb, a))
    zval = bval / (1 - model.values[e])
    z = model.node("sum", (b, -1), value=zval)
    w = model.node("product", (e, z))
    model.rows[z] = (z, "sum", (b, w))
    if output_u <= output_v:
        assert aval == zval == 1
    else:
        assert 1 - aval >= F(1, scale)
        assert zval <= F(1, 8)
    model.check()
    assert model.largest_scc() == 4


def check_iteration_invariants(rng):
    for n in range(1, 5):
        b = F(1, 2 ** (2 ** n))
        c = 1 - b
        z = w = F(0)
        affine_count = 0
        for _ in range(100):
            if rng.randrange(2):
                old_z, old_w = z, w
                z = max(old_z, b + old_w)
                w = max(old_w, old_z - b)
                affine_count += 1
            else:
                old_z, old_w = z, w
                z = max(old_z, old_w / c)
                w = max(old_w, c * old_z)
            assert 0 <= w <= c * z <= c
            assert z <= 1 - c ** affine_count <= affine_count * b


if __name__ == "__main__":
    random_generator = random.Random(20260904)
    for depth in range(1, 6):
        for _ in range(10):
            check_random_circuit(random_generator, depth)
    check_iteration_invariants(random_generator)
    print("Passed: 50 exact circuit/gap/SCC checks and 400 primitive-update invariant checks.")
