"""Exact checks for the operating-constraint examples; no numerical solver."""

from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Quad:
    """The exact number a+b*sqrt(2), with rational coefficients."""

    a: F = F(0)
    b: F = F(0)

    def __add__(self, other):
        other = other if isinstance(other, Quad) else Quad(F(other))
        return Quad(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quad(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Quad) else -F(other))

    def __mul__(self, other):
        other = other if isinstance(other, Quad) else Quad(F(other))
        return Quad(self.a * other.a + 2 * self.b * other.b,
                    self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def sign(self):
        if not self.b:
            return (self.a > 0) - (self.a < 0)
        if not self.a:
            return (self.b > 0) - (self.b < 0)
        if (self.a > 0) == (self.b > 0):
            return (self.a > 0) - (self.a < 0)
        difference = self.a**2 - 2 * self.b**2
        magnitude_sign = (difference > 0) - (difference < 0)
        return magnitude_sign if self.a > 0 else -magnitude_sign


def check_rank_two_witness():
    theta = Quad(F(6), F(-4))
    q1, q2, one = Quad(F(2), F(-1)), Quad(F(-1), F(1)), Quad(F(1))
    edges = [(0, 1), (0, 2), (2, 1), (0, 3), (3, 1)]
    beta = [theta, Quad(F(1, 2)), Quad(F(1, 2)), one, one]
    flow = [one, q1, q1, q2, q2]
    potential = [theta, Quad(), theta * F(1, 2), theta * F(1, 2)]
    balance = [Quad() for _ in range(4)]
    for (u, v), resistance, value in zip(edges, beta, flow):
        require(value.sign() > 0 and (value - 2).sign() < 0, "flow bounds")
        require(resistance * value * value == potential[u] - potential[v],
                "original constitutive law")
        balance[u] = balance[u] + value
        balance[v] = balance[v] - value
    require(balance == [Quad(F(2)), Quad(F(-2)), Quad(), Quad()], "nominations")
    require(flow[0] == one, "target equality")
    require((theta - F(1, 3)).sign() > 0, "lower resistance bound")
    require((theta - F(3, 8)).sign() < 0, "upper resistance bound")
    require(theta * theta - 12 * theta + 4 == Quad(), "minimal polynomial")
    require(isqrt(128) ** 2 != 128, "irreducible quadratic discriminant")
    require(len(edges) - 4 + 1 == 2, "cycle rank")
    # Endpoint values are not roots of the necessary polynomial.
    for endpoint in (F(1, 3), F(3, 8)):
        require(endpoint**2 - 12 * endpoint + 4 != 0, "endpoint infeasibility")


def check_triangle_filter():
    # Entries: two path-edge resistances, direct resistance, path flow,
    # direct flow, and common terminal drop. Every value is rational.
    profiles = [
        (F(1, 2), F(1, 2), F(9), F(3, 4), F(1, 4), F(9, 16)),
        (F(9, 2), F(9, 2), F(1), F(1, 4), F(3, 4), F(9, 16)),
        (F(5, 2), F(5, 2), F(5), F(1, 2), F(1, 2), F(5, 4)),
    ]
    for r1, r2, direct, path_flow, direct_flow, drop in profiles:
        require(path_flow + direct_flow == 1, "triangle conservation")
        require((r1 + r2) * path_flow**2 == drop, "triangle path law")
        require(direct * direct_flow**2 == drop, "triangle direct law")
    for i in range(3):
        require((profiles[0][i] + profiles[1][i]) / 2 == profiles[2][i],
                "resistance midpoint")
    require(profiles[0][-1] <= 1 and profiles[1][-1] <= 1, "accepted endpoints")
    require(profiles[2][-1] > 1, "rejected midpoint")


def check_upper_capacity_witness():
    drop = Quad(F(6), F(-4))
    theta = drop + 1
    one = Quad(F(1))
    q1, q2 = Quad(F(2), F(-1)), Quad(F(-1), F(1))
    # Node indices u,v,r,w,z. The first two edges form the saturated cut.
    edges = [(0, 1), (0, 2), (2, 3), (3, 1), (2, 4), (4, 1)]
    beta = [theta, one, Quad(F(1, 2)), Quad(F(1, 2)), one, one]
    flow = [one, one, q1, q1, q2, q2]
    upper = [1, 1, 2, 2, 2, 2]
    potential = [theta, Quad(), drop, drop * F(1, 2), drop * F(1, 2)]
    balance = [Quad() for _ in range(5)]
    for (u, v), resistance, value, cap in zip(edges, beta, flow, upper):
        require(value.sign() >= 0 and (value - cap).sign() <= 0,
                "ordinary nonnegative upper capacities")
        require(resistance * value * value == potential[u] - potential[v],
                "strengthened original constitutive law")
        balance[u] = balance[u] + value
        balance[v] = balance[v] - value
    require(balance == [Quad(F(2)), Quad(F(-2)), Quad(), Quad(), Quad()],
            "strengthened nominations")
    require(sum(upper[:2]) == 2 and flow[0] + flow[1] == 2 * one,
            "cut saturation")
    require((theta - F(4, 3)).sign() > 0, "strengthened lower resistance")
    require((theta - F(11, 8)).sign() < 0, "strengthened upper resistance")
    require(theta * theta - 14 * theta + 17 == Quad(), "strengthened polynomial")
    require(isqrt(128) ** 2 != 128, "strengthened irreducibility")
    require(len(edges) - 5 + 1 == 2, "strengthened rank")


def check_scalar_ingredients():
    values = [F(i, 6) for i in range(-18, 19)]
    cases = 0
    for s in values:
        for t in values:
            require((s * abs(s) - t * abs(t)) * (s - t) >= abs(s - t)**3 / 2,
                    "quadratic monotonicity")
            require(abs(s * abs(s) - t * abs(t)) <= 6 * abs(s - t),
                    "pressure-law Lipschitz bound on [-3,3]")
            if s > t:
                require(s * abs(s) - t * abs(t) >= (s - t) * abs(t) / 2,
                        "one-sided cycle increment bound")
            cases += 1
    return cases


if __name__ == "__main__":
    check_rank_two_witness()
    check_upper_capacity_witness()
    check_triangle_filter()
    cases = check_scalar_ingredients()
    print("PASS: rank-two equality and ordinary-upper-capacity irrational witnesses;")
    print("triangle nonconvex pressure filter;")
    print(f"{cases} exact scalar monotonicity, cycle increment, and pressure-law cases.")
