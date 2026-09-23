"""Independent exact original-network certificates for quality-reset paths.

Only input qualities zero and one occur. Source and relay-output contracts
are replaced by upper bounds and the explicit theoretical throughput reward.
Certificates use actual arc constraints, with no hidden copy equalities.
"""
from fractions import Fraction as F
from itertools import product

from exact_shadow_check import instance, vertex, witness
from exact_physical_penalty_check import solve_square


def main():
    total = 0
    for n in range(2, 8):
        eps, c = instance(n)
        free_supplies = [eps ** (n - 1 - j) for j in range(n)]
        # (free-coordinate index, input quality, carries objective coefficient)
        chain = [(0, 1, True)]
        for j in range(1, n):
            chain.append((j, 0, True))
            if j < n - 1:
                chain.append((j, 1, False))
        m = len(chain)
        supplies = [free_supplies[j] for j, _, _ in chain]
        # An internal output is a relay iff its following input has quality one.
        relay_outputs = {i for i in range(1, m) if chain[i][1] == 1}
        width = 2*m
        penalty = 2 * width**width + 1
        for bits in product((0, 1), repeat=n):
            x = vertex(bits, eps)
            lam = witness(bits, eps)
            right = [supplies[i] * x[j] for i, (j, _, _) in enumerate(chain)]
            flow = [v for s, t in zip(supplies, right) for v in (s-t, t)]
            price = [F(1)]
            for i, (j, _, charged) in enumerate(chain):
                weight = (c[j] / supplies[i] if j < n-1 else lam) if charged else F(0)
                price.append(price[-1] + weight)
            assert all(0 <= v <= 2 for v in price)
            objective = [price[i+side] + penalty * (1 + ((i+side) in relay_outputs))
                         for i in range(m) for side in (0, 1)]
            rows, bounds = [], []
            for i, s in enumerate(supplies):
                row = [F(0)] * width
                row[2*i] = row[2*i+1] = 1
                rows.append(row)
                bounds.append(s)
            for i in sorted(relay_outputs):
                row = [F(0)] * width
                row[2*i-1] = row[2*i] = 1
                rows.append(row)
                bounds.append(supplies[i])
            row = [F(0)] * width
            row[0 if bits[0] else 1] = -1
            rows.append(row)
            bounds.append(F(0))
            for i in range(1, m):
                if i in relay_outputs:
                    continue
                j = chain[i][0]
                row = [F(0)] * width
                row[2*i-1] = 1
                row[2*i] = -1 if bits[j] else 1
                rows.append(row)
                bounds.append(F(0) if bits[j] else supplies[i])
            assert len(rows) == width
            assert all(sum(a*v for a, v in zip(row, flow)) == b
                       for row, b in zip(rows, bounds))
            dual = solve_square(list(map(list, zip(*rows))), objective)
            assert all(v > 0 for v in dual), (n, bits, dual)
            assert sum(v*b for v, b in zip(dual, bounds)) == sum(v*f for v, f in zip(objective, flow))
            # Verify every original physical upper capacity and quality row.
            assert all(0 <= flow[2*i+side] <= supplies[i]
                       for i in range(m) for side in (0, 1))
            for i in range(1, m):
                incoming = right[i-1] + flow[2*i]
                assert incoming <= supplies[i]
                quality_bound = F(1) if i in relay_outputs else F(1, 2)
                mass = chain[i-1][1]*right[i-1] + chain[i][1]*flow[2*i]
                assert mass <= quality_bound * incoming
            assert flow[0] <= supplies[0] and right[-1] <= 1
            contract_sum = sum(supplies) + sum(supplies[i] for i in relay_outputs)
            base_constant = sum(price[i]*supplies[i] for i in range(m))
            expected = penalty*contract_sum + base_constant + sum(ci*xi for ci, xi in zip(c, x)) + lam*x[-1]
            assert expected == sum(v*f for v, f in zip(objective, flow))
            total += 1
        print(f'n={n}, inputs={m}, arc variables={width}: {2**n} certificates PASS')
    print(f'PASS: {total} exact positive dual certificates; two input qualities, upper flows/qualities only.')


if __name__ == '__main__':
    main()
