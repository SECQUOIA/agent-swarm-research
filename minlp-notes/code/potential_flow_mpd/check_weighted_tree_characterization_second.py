"""Exact subdivided-cycle and restoration-constant checks."""
from fractions import Fraction as F
from itertools import product


def require(ok):
    if not ok:
        raise RuntimeError("weighted cycle construction check failed")


def run():
    scenarios = [(F(16, 3), F(-3, 8)), (F(24), F(-1, 4)),
                 (F(144), F(-1, 8))]
    states = controls = 0
    for lengths in product(range(1, 5), repeat=3):
        size = sum(lengths)
        branches = [0, lengths[0], lengths[0]+lengths[1]]
        for theta, q in scenarios:
            d = F(8, 3) if lengths[2] > 1 else F(0)
            beta = [F(1, lengths[0])]*lengths[0]
            beta += [F(1, lengths[1])]*lengths[1]
            beta += ([d/(lengths[2]-1)]*(lengths[2]-1) if lengths[2] > 1 else [])
            beta += [theta-d]
            flow = [q+2]*lengths[0]+[q-1]*lengths[1]+[q]*lengths[2]
            require(all(v > 0 for v in beta))
            pressure = [F(0)]
            balance = [F(0)]*size
            for i in range(size):
                pressure.append(pressure[-1]-beta[i]*flow[i]*abs(flow[i]))
                balance[i] += flow[i]
                balance[(i+1) % size] -= flow[i]
            require(pressure[-1] == 0)
            expected = [F(0)]*size
            for node, nomination in zip(branches, [2, -3, 1]):
                expected[node] = F(nomination)
            require(balance == expected)
            objective = sum(c*pressure[v] for c, v in zip([-5, 12, -7], branches))
            require(objective == F(-105, 4)-12*(q+F(1, 4))**2)
            require(objective == (F(-105, 4) if theta == 24 else F(-423, 16)))
            trial = [F(7, 4)]*lengths[0]+[F(-5, 4)]*lengths[1]+[F(-1, 4)]*lengths[2]
            energy = sum(c*abs(x)**3/3 for c, x in zip(beta, trial))
            require(energy == (468+theta)/192 < 4)
            if d:
                # Omitting the subtraction of fixed subdivision resistance
                # must destroy the claimed cycle law at the same flow.
                require(sum(c*x*abs(x) for c, x in zip(beta, flow))+d*q*abs(q) != 0)
                controls += 1
            states += 1
    for m in range(3, 101):
        R = 12*(10000*m*m)**3
        u = F(1, 10000*m*m)
        require(u**3 == F(12, R))
        error = 288*m*m*u
        require(error == F(18, 625) < F(3, 64))
        require(F(3, 16)-2*error > F(3, 32))
    print(f"PASS: {states} exact subdivided physical cycle states, {controls} "
          "subdivision negative controls, 98 exact restoration gap bounds.")


if __name__ == "__main__":
    run()
