"""Independent time-domain verification by exact Laplace inversion.

For k(s)=2(1-cos(s)), Ds=0, the integrated surface resolvent is
I(z)=2*pi/sqrt(z*(z+4)). No wall mesh or fitted power law is used.
Two inversion methods check equilibrium and bulk-injection asymptotics.
"""
import json
from pathlib import Path
import mpmath as mp


def main():
    mp.mp.dps = 45
    area, affinity, speed = mp.mpf(1), mp.mpf("0.1"), mp.mpf(1)
    perimeter = 2*mp.pi
    ztotal = area+affinity*perimeter
    v = speed*area/ztotal
    b = v*v*affinity/ztotal

    def integral(p):
        # Separate principal square roots preserve analyticity off [-4,0].
        return 2*mp.pi/(mp.sqrt(p)*mp.sqrt(p+4))

    def stat_var(p):
        return 2*v*v*affinity*integral(p)/(ztotal-affinity*p*integral(p))/p**2

    def injected_mean(p):
        return v/(p*p*(1-affinity*p*integral(p)/ztotal))

    def injected_second(p):
        return 2*v*v/(p**3*(1-affinity*p*integral(p)/ztotal)**2)

    rows = []
    for t in [10, 100, 1000, 10000, 100000, 1000000]:
        values = []
        for method in ["dehoog", "talbot"]:
            var_stat = mp.invertlaplace(stat_var, t, method=method)
            mean = mp.invertlaplace(injected_mean, t, method=method)
            second = mp.invertlaplace(injected_second, t, method=method)
            values.append((var_stat, mean, second-mean*mean))
        error = max(abs(a-c)/max(abs(a), 1) for a, c in zip(*values))
        assert error < mp.mpf("1e-15"), (t, error)
        var_stat, mean, var_inj = values[0]
        rows.append({"time": t,
                     "stationary_normalized_variance": float(var_stat/(mp.mpf(8)/3*b*mp.sqrt(mp.pi)*t**mp.mpf("1.5"))),
                     "injected_normalized_variance": float(var_inj/(mp.mpf(4)/3*b*mp.sqrt(mp.pi)*t**mp.mpf("1.5"))),
                     "normalized_injected_mean_correction": float((mean-v*t)/(2*v*affinity/ztotal*mp.sqrt(mp.pi*t))),
                     "stationary_to_injected_variance_ratio": float(var_stat/var_inj),
                     "inversion_method_relative_difference": float(error)})
    assert abs(rows[-1]["stationary_normalized_variance"]-1) < 1e-3
    assert abs(rows[-1]["injected_normalized_variance"]-1) < 1e-3
    result = {"parameters": {"area": 1, "affinity": 0.1, "bulk_velocity": 1,
                              "perimeter": float(perimeter), "surface_diffusivity": 0},
              "checks": rows,
              "interpretation": "Confirms known renewal initialization distinction within the new kinetic-minimum model; initialization exponents themselves are not novel."}
    Path("results").mkdir(exist_ok=True)
    Path("results/exchange-transient-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
