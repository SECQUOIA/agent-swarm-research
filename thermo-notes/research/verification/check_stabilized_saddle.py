"""Check growth-rate reconstruction and finite-grid population bounds.

All correlations here are exact spectral sums. This does not test statistical
coverage for empirical correlations or the transfer of physical bath kinetics.
"""
from pathlib import Path
import json

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq


def decreasing_root(fun, target, upper):
    if fun(0.0) <= target:
        return 0.0
    for _ in range(80):
        if fun(upper) < target:
            return brentq(lambda x: fun(x) - target, 0.0, upper,
                          xtol=1e-13, rtol=1e-13)
        upper *= 2.0
    return np.inf


def exact_root(rates, weights, q):
    return decreasing_root(
        lambda s: np.sum(weights * rates / (rates + s)),
        1.0 / q, (q - 1.0) * np.dot(weights, rates) * 2.0,
    )


def grid_bounds(rates, weights, q, times):
    corr = np.exp(-np.outer(times, rates)) @ weights
    losses = -np.diff(corr)
    assert losses.min() >= -1e-14
    lo = lambda s: np.dot(losses, np.exp(-s * times[1:]))
    hi = lambda s: (np.dot(losses, np.exp(-s * times[:-1]))
                    + corr[-1] * np.exp(-s * times[-1]))
    bound = (q - 1.0) * np.dot(weights, rates) * 2.0
    lower = decreasing_root(lo, 1.0 / q, bound)
    upper = (np.inf if losses[0] >= 1.0 / q
             else decreasing_root(hi, 1.0 / q, bound))
    return lower, upper, corr


def main():
    rng = np.random.default_rng(20260907)
    worst = 0.0
    for _ in range(250):
        n = int(rng.integers(2, 16))
        raw = rng.normal(size=(n, n))
        h = raw.T @ raw + np.eye(n)
        raw = rng.normal(size=(n, n))
        mob = raw.T @ raw + 0.2 * np.eye(n)
        mval, mvec = eigh(mob)
        sqrt_m = (mvec * np.sqrt(mval)) @ mvec.T
        a = sqrt_m @ h @ sqrt_m
        rates, vec = eigh(a)
        u = rng.normal(size=n)
        v = sqrt_m @ u
        unnormalized = (vec.T @ v) ** 2 / rates
        c0 = unnormalized.sum()
        weights = unnormalized / c0
        q = rng.uniform(1.01, 6.0)
        k = q / c0
        direct = -eigh(a - k * np.outer(v, v), eigvals_only=True)[0]
        reconstructed = exact_root(rates, weights, q)
        worst = max(worst, abs(direct - reconstructed) / direct)
        assert np.isclose(direct, reconstructed, rtol=1e-10, atol=1e-10)
        lower = (q - 1.0) / np.dot(weights, 1.0 / rates)
        upper = (q - 1.0) * np.dot(weights, rates)
        assert lower <= reconstructed * (1.0 + 1e-11)
        assert upper >= reconstructed * (1.0 - 1e-11)
        times = np.linspace(0.0, 5.0 / reconstructed, 101)
        gl, gu, _ = grid_bounds(rates, weights, q, times)
        assert gl <= reconstructed * (1.0 + 1e-11)
        assert gu >= reconstructed * (1.0 - 1e-11)

    rates = np.array([1e-4, 1.0])
    weights = np.array([0.1, 0.9])
    q = 2.0
    rate = exact_root(rates, weights, q)
    example = {
        "rates": rates.tolist(), "weights": weights.tolist(), "q": q,
        "exact_growth": rate,
        "integrated_time_lower_bound": (q - 1.0) / np.dot(weights, 1.0 / rates),
        "initial_slope_upper_bound": (q - 1.0) * np.dot(weights, rates),
        "finite_grid_bounds": [],
    }
    for horizon in [1.0, 2.0, 5.0, 10.0, 20.0]:
        times = np.arange(0.0, horizon + 0.025, 0.05)
        lo, hi, corr = grid_bounds(rates, weights, q, times)
        example["finite_grid_bounds"].append({
            "horizon": horizon, "spacing": 0.05,
            "lower": lo, "upper": hi, "residual_correlation": float(corr[-1]),
        })

    # Two-mode distributions retain BOTH the rate and inverse-rate moments.
    mean_rate, mean_time = 3.0, 2.0
    sharpness = []
    for fraction in [1e-7, 1e-4, 0.1, 0.9, 1.0 - 1e-4, 1.0 - 1e-7]:
        low = fraction / mean_time
        high = (mean_rate - low) / (1.0 - mean_time * low)
        p = (high - mean_rate) / (high - low)
        a = np.array([low, high])
        w = np.array([p, 1.0 - p])
        assert np.isclose(np.dot(w, a), mean_rate, rtol=1e-8)
        assert np.isclose(np.dot(w, 1.0 / a), mean_time, rtol=1e-8)
        sharpness.append({"low": low, "high": high, "slow_weight": p,
                          "growth": exact_root(a, w, q)})

    result = {"random_cases": 250, "max_relative_eigenvalue_error": worst,
              "slow_mode_example": example, "fixed_moment_sharpness": sharpness}
    path = Path(__file__).with_name("stabilized-saddle-results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
