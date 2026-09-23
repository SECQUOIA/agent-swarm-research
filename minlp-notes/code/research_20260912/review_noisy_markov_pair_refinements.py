"""Fresh exact review of scalar far/near local-residual covariance bounds.

References use covariance matrices built from independent-innovation loadings,
exact dense LDL solves, and gain products formed from dense prefix conditionals.
No author far-pair verification or proposed refined-bound code is imported.
"""

from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import hashlib
import json
from pathlib import Path
import random

from noisy_markov_spacing_bound import spacing_bound


def solve_spd(matrix, rhs):
    n = len(rhs)
    lower = [[F(i == j) for j in range(n)] for i in range(n)]
    diagonal = []
    for j in range(n):
        pivot = matrix[j][j]-sum((lower[j][h]**2*diagonal[h] for h in range(j)), F(0))
        assert pivot > 0
        diagonal.append(pivot)
        for i in range(j+1, n):
            lower[i][j] = (matrix[i][j]-sum((lower[i][h]*lower[j][h]*diagonal[h]
                                            for h in range(j)), F(0)))/pivot
    y = []
    for i in range(n):
        y.append(rhs[i]-sum((lower[i][j]*y[j] for j in range(i)), F(0)))
    x = [y[i]/diagonal[i] for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] -= sum((lower[j][i]*x[j] for j in range(i+1, n)), F(0))
    return x


def is_psd(matrix):
    """Exact Schur elimination; a zero PSD pivot must have a zero column."""
    matrix = [row[:] for row in matrix]
    for j in range(len(matrix)):
        pivot = matrix[j][j]
        if pivot < 0:
            return False
        if not pivot:
            if any(matrix[i][j] for i in range(j+1, len(matrix))):
                return False
            continue
        for i in range(j+1, len(matrix)):
            for h in range(j+1, len(matrix)):
                matrix[i][h] -= matrix[i][j]*matrix[j][h]/pivot
    return True


class InnovationModel:
    def __init__(self, initial, transitions, processes, measurement):
        self.n = len(measurement)
        self.a = tuple(map(F, transitions))
        self.r = tuple(map(F, measurement))
        primitive = [F(initial)]+list(map(F, processes))
        loading = [[F(0)]*self.n for _ in range(self.n)]
        for i in range(self.n):
            loading[i][i] = F(1)
            for j in range(i):
                value = F(1)
                for h in range(j, i):
                    value *= self.a[h]
                loading[i][j] = value
        self.K = tuple(tuple(sum((loading[i][h]*loading[j][h]*primitive[h]
                                  for h in range(self.n)), F(0))
                             for j in range(self.n)) for i in range(self.n))
        self.R = tuple(tuple(self.K[i][j]+(self.r[i] if i == j else 0)
                             for j in range(self.n)) for i in range(self.n))
        self.P = tuple(self.K[i][i] for i in range(self.n))
        self.b = max(map(abs, self.a), default=F(0))
        self.Pbar, self.rmin = max(self.P), min(self.r)

    def transition(self, s, t):
        value = F(1)
        for h in range(s, t):
            value *= self.a[h]
        return value

    @lru_cache(None)
    def conditional(self, t, history):
        coefficients = solve_spd([[self.R[i][j] for j in history] for i in history],
                                 [self.R[i][t] for i in history])
        row = [F(0)]*self.n
        row[t] = F(1)
        for j, coefficient in zip(history, coefficients):
            row[j] = -coefficient
        cross = tuple(sum((row[i]*self.R[i][j] for i in range(self.n)), F(0))
                      for j in range(self.n))
        assert all(cross[j] == 0 for j in history)
        variance = sum((row[j]*cross[j] for j in range(self.n)), F(0))
        return tuple(row), variance, cross

    def alpha(self, history):
        value = F(1)
        for i, t in enumerate(history):
            # 1-K = r/d, with d obtained from an exact dense conditional.
            value *= self.r[t]/self.conditional(t, history[:i])[1]
        return value

    def residuals(self, selected, L):
        histories = [tuple(j for j in selected[:i] if t-j <= L)
                     for i, t in enumerate(selected)]
        stats = [self.conditional(t, history) for t, history in zip(selected, histories)]
        covariance = [[sum((left[0][h]*right[2][h] for h in range(self.n)), F(0))
                       for right in stats] for left in stats]
        assert all(covariance[i][i] == stats[i][1] for i in range(len(stats)))
        return histories, stats, covariance


def subsets(n, gap=1):
    for size in range(n+1):
        for chosen in combinations(range(n), size):
            if all(v-u >= gap for u, v in zip(chosen, chosen[1:])):
                yield chosen


def check_general(model, selected, L, counts):
    histories, stats, covariance = model.residuals(selected, L)
    kappa = model.Pbar/(model.Pbar+model.rmin)
    for i, t in enumerate(selected):
        alpha = model.alpha(histories[i])
        latent_cross = sum((stats[i][0][j]*model.K[t][j] for j in range(model.n)), F(0))
        assert latent_cross == stats[i][1]-model.r[t]
        counts["latent_residual_identities"] += 1
        for s in range(max(0, t-L)):
            expected = model.transition(s, t)*model.P[s]*alpha
            assert stats[i][2][s] == expected
            counts["excluded_observation_identities"] += 1
        for j in range(i):
            s, h = selected[j], t-selected[j]
            if h > L:
                exact = model.transition(s, t)*(stats[j][1]-model.r[s])*alpha
                assert covariance[i][j] == exact
                assert abs(exact) <= model.Pbar*model.b**h
                counts["far_pair_identities"] += 1
            else:
                bound = model.Pbar*kappa*sum((model.b**(h+2*d)
                            for d in range(L+1-h, L+1)), F(0))
                assert abs(covariance[i][j]) <= bound
                counts["general_near_pair_bounds"] += 1
    counts["general_subset_window_cases"] += 1


def phi_values(n, L, gap, b, P, r, stationary_near):
    kappa = P/(P+r)
    phi = [F(0)]*n
    for h in range(gap, n):
        if h > L:
            phi[h] = P*b**h
        else:
            factor = 1-kappa if stationary_near else F(1)
            first = max(gap, L+1-h)
            phi[h] = P*kappa*factor*sum((b**(h+2*d) for d in range(first, L+1, gap)), F(0))
    return phi


def enumerated_row_bound(phi, gap):
    # Exhaustively enumerate distance packs independently on each side.
    best = []
    for width in range(len(phi)):
        values = [F(0)]
        for chosen in subsets(max(0, width-gap+1), gap):
            values.append(sum((phi[j+gap] for j in chosen), F(0)))
        best.append(max(values))
    return max(best[t]+best[len(phi)-1-t] for t in range(len(phi)))


def local_floor(P, r, b, L, gap):
    value = P
    for _ in range(L//gap):
        value = P-b**(2*gap)*(P-r*value/(r+value))
    return r+value


def stationary_checks(counts):
    for n in range(1, 7):
        for rho in (F(-3, 4), F(0), F(2, 3)):
            for P, r in ((F(0), F(1, 3)), (F(1), F(1)), (F(3, 2), F(2, 5))):
                model = InnovationModel(P, [rho]*(n-1), [P*(1-rho*rho)]*(n-1), [r]*n)
                assert model.P == (P,)*n
                kappa = P/(P+r)
                for gap in range(1, min(3, n+1)+1):
                    for L in range(n+1):
                        floor = local_floor(P, r, abs(rho), min(L, n-1), gap)
                        phi = phi_values(n, L, gap, abs(rho), P, r, True)
                        far_only_phi = phi_values(n, L, gap, abs(rho), P, r, False)
                        row = enumerated_row_bound(phi, gap)
                        far_only_row = enumerated_row_bound(far_only_phi, gap)
                        if L >= n-1 or gap >= n:
                            row = far_only_row = F(0)
                        old = spacing_bound(n, L, gap, rho, P, r)
                        assert row <= far_only_row <= old["row_majorant"]
                        assert floor == old["innovation_floor"]
                        counts["row_majorant_comparisons"] += 1
                        delta = row/floor
                        for chosen in subsets(n, gap):
                            histories, stats, covariance = model.residuals(chosen, L)
                            for i, t in enumerate(chosen):
                                assert stats[i][1] >= floor
                                counts["innovation_floor_checks"] += 1
                                if histories[i]:
                                    assert model.alpha(histories[i]) <= 1-kappa
                                    counts["stationary_gain_products"] += 1
                                for j in range(i):
                                    assert abs(covariance[i][j]) <= phi[t-chosen[j]]
                                    counts["stationary_pair_bounds"] += 1
                            # Exact congruent form of the normalized covariance
                            # eigenvalue sandwich; no square-root rounding.
                            for sign in (-1, 1):
                                matrix = [[(delta*stats[i][1] if i == j else 0)
                                           +sign*(covariance[i][j]-(stats[i][1] if i == j else 0))
                                           for j in range(len(chosen))] for i in range(len(chosen))]
                                assert is_psd(matrix)
                                counts["exact_spectral_sandwich_matrices"] += 1
                            counts["stationary_subset_window_gap_cases"] += 1


def nonstationary_checks(counts):
    rng = random.Random(771809)
    for n in range(1, 7):
        for case in range(4):
            initial = F(0) if case == 0 else F(case, 2)
            a = [rng.choice((F(-9, 10), F(-1, 2), F(0), F(1, 3), F(4, 5))) for _ in range(n-1)]
            q = [F(0) if case <= 1 else rng.choice((F(0), F(1, 10), F(1, 2))) for _ in range(n-1)]
            r = [rng.choice((F(1, 5), F(1), F(3))) for _ in range(n)]
            model = InnovationModel(initial, a, q, r)
            counts["nonstationary_covariance_models"] += 1
            for selected in subsets(n):
                for L in range(n+1):
                    check_general(model, selected, L, counts)


def scope_counterexample():
    model = InnovationModel(F(1), [F(1, 2)]*2, [F(0)]*2, [F(1)]*3)
    history, stats, covariance = model.residuals((0, 1, 2), 1)
    actual = covariance[2][1]
    b, Pbar, rmin = F(1, 2), F(1), F(1)
    kappa = Pbar/(Pbar+rmin)
    wrong = Pbar*kappa*(1-kappa)*b**3
    assert actual == -F(1, 20) and wrong == F(1, 32) and abs(actual) > wrong
    return {"transitions": ["1/2", "1/2"], "process_variances": ["0", "0"],
            "measurement_variances": ["1", "1", "1"], "latent_variances": list(map(str, model.P)),
            "L": 1, "selected": [0, 1, 2], "Cov_Z2_Z1": str(actual),
            "incorrect_generalized_near_bound": str(wrong),
            "actual_alpha_at_2": str(model.alpha(history[2])),
            "incorrect_gain_product_bound": str(1-kappa)}


def large_probe():
    n, L, gap = 96, 13, 2
    b, P, r = F("0.6324555320336759"), F("0.00125"), F("0.00125")
    old = spacing_bound(n, L, gap, b, P, r)
    values = {}
    for name, refined_near in (("far_only", False), ("far_and_stationary_near", True)):
        phi = phi_values(n, L, gap, b, P, r, refined_near)
        best = [F(0)]*n
        for h in range(gap, n):
            best[h] = max(best[h-1], phi[h]+best[h-gap])
        row = max(best[t]+best[n-1-t] for t in range(n))
        delta = row/old["innovation_floor"]
        values[name] = {"delta": str(delta), "delta_float": float(delta),
                        "relative_reduction_from_old": float(1-delta/old["delta"])}
    return {"n": n, "L": L, "gap": gap, "rho": str(b), "latent": str(P), "nugget": str(r),
            "old_delta_float": float(old["delta"]), "refinements": values}


def geometric_sum_checks():
    count = 0
    for b in (F(0), F(1, 4), F(3, 5), F(9, 10)):
        for L in range(21):
            direct = sum((b**(h+2*d) for h in range(1, L+1)
                          for d in range(L+1-h, L+1)), F(0))
            formula = b**(L+2)*(1-b**L)*(1-b**(L+1))/((1-b)*(1-b*b))
            assert direct == formula
            count += 1
    return count


def main():
    counts = dict.fromkeys(("latent_residual_identities", "excluded_observation_identities",
                           "far_pair_identities", "general_near_pair_bounds", "general_subset_window_cases",
                           "row_majorant_comparisons", "innovation_floor_checks", "stationary_gain_products",
                           "stationary_pair_bounds", "exact_spectral_sandwich_matrices",
                           "stationary_subset_window_gap_cases", "nonstationary_covariance_models"), 0)
    nonstationary_checks(counts)
    stationary_checks(counts)
    counts["geometric_sum_identities"] = geometric_sum_checks()
    here = Path(__file__).resolve().parent
    report = {"status": "passed", "counts": counts, "scope_counterexample": scope_counterexample(),
              "n96_probe": large_probe(),
              "source_hashes": {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                                for name in ("review_noisy_markov_pair_refinements.py", "noisy_markov_spacing_bound.py")},
              "scope": "Fresh scalar mathematical review. No accepted production bound or certificate was changed."}
    output = here/"results"/"noisy-markov-pair-refinements-independent-review.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "counts": counts,
                      "n96_delta_old": report["n96_probe"]["old_delta_float"],
                      "n96_deltas_new": {name: row["delta_float"] for name, row in report["n96_probe"]["refinements"].items()}}, indent=2))


if __name__ == "__main__":
    main()
