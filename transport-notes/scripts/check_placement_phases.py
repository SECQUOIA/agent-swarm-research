"""Check the finite-rate-floor mobility-placement phase diagram.

Uses analytic candidate profiles, independent quadrature and a discrete convex
Lipschitz-constrained optimization. All variables are dimensionless.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize, LinearConstraint, Bounds


ONSET = 8/(3*np.sqrt(3))
MERGER = 3/np.sqrt(2)


def candidate(eta):
    if eta <= ONSET:
        left = right = intercept = 0.0
        phase = "zero mobility"
    elif eta < MERGER:
        total = brentq(lambda s: s+s**3/4-eta, 2/np.sqrt(3), np.sqrt(2), xtol=1e-14)
        gap = np.sqrt(3*total**2-4)
        left, right = (total-gap)/2, (total+gap)/2
        intercept = 6/(4+total**2)
        phase = "two flanks"
    else:
        left = 0.0
        right = (np.sqrt(2) if eta == MERGER else
                 brentq(lambda r: (1+r*r)*(6+r*r)/(8*r)-eta,
                        np.sqrt(2), max(10.0, 4*eta**(1/3)), xtol=1e-14))
        intercept = right/eta+1/(1+right*right)
        phase = "central support"

    def h(x):
        z = np.abs(np.asarray(x))
        return np.where((z >= left) & (z <= right) & (right > left),
                        intercept-z/eta, 1/(1+z*z))

    def mobility(x):
        z = np.abs(np.asarray(x))
        if phase == "zero mobility":
            return np.zeros_like(z)
        if phase == "two flanks":
            val = (z-left)**2*(z-right)**2/4
        else:
            val = z*(right-z)**2*(2*right*z+right*right-2)/(8*right)
        return np.where((z >= left) & (z <= right), val, 0.0)

    mass = 2*quad(lambda z: float(mobility(z)), left, right, epsabs=1e-13)[0]
    j = np.pi+2*(intercept*(right-left)-(right*right-left*left)/(2*eta)
                    -np.arctan(right)+np.arctan(left))
    gain = 2*eta*eta*quad(lambda z: (1+z*z)*(float(h(z))-1/(1+z*z))**2,
                         left, right, epsabs=1e-13)[0]
    assert abs(mass+eta*eta*j-(eta*eta*np.pi-gain)) < 1e-9*max(1, eta*eta)
    result = {"eta": eta, "phase": phase, "left": left, "right": right,
              "mass": mass, "surface_integral": j, "cost": mass+eta*eta*j,
              "gain_over_zero_mobility": gain}
    return result, h, mobility


def discrete_dual(eta, n=480, cold_start=False):
    info, h, _ = candidate(eta)
    extent = max(4.0, 1.5*info["right"])
    dx = 2*extent/n
    x = -extent+(np.arange(n)+0.5)*dx
    k = 1+x*x

    def objective(z):
        return dx*np.dot(k, z*z)-2*dx*np.sum(z)

    def jac(z):
        return 2*dx*(k*z-1)

    constraint = np.zeros((n-1, n))
    i = np.arange(n-1)
    constraint[i, i], constraint[i, i+1] = -1, 1
    initial = np.zeros(n) if cold_start else h(x)
    result = minimize(objective, initial, jac=jac, method="SLSQP",
                      constraints=[LinearConstraint(constraint, -dx/eta, dx/eta)],
                      bounds=Bounds(np.zeros(n), np.full(n, np.inf)),
                      options={"ftol": 1e-11, "maxiter": 200})
    assert result.success, result.message
    numerical = -eta*eta*result.fun+eta*eta*(np.pi-2*np.arctan(extent))
    return {"eta": eta, "n": n, "cold_start": cold_start,
            "numerical_cost_with_exact_tail": numerical,
            "candidate_cost": info["cost"], "relative_difference": numerical/info["cost"]-1,
            "iterations": int(result.nit),
            "maximum_slope_constraint_error": float(np.max(abs(constraint@result.x))-dx/eta)}


def main():
    selected = [candidate(e)[0] for e in [1.0, 1.6, 1.8, 2.0, MERGER, 3.0, 10.0, 100.0]]
    duals = [discrete_dual(e) for e in [1.0, 1.6, 1.8, 3.0, 10.0]]
    duals += [discrete_dual(e, n=240, cold_start=True) for e in [1.8, 3.0]]
    onset = []
    for excess in [1e-2, 1e-3, 1e-4, 1e-5]:
        item = candidate(ONSET+excess)[0]
        q = item["right"]-item["left"]
        onset.append({"excess_eta": excess,
                      "mass_over_q5_div60": item["mass"]/(q**5/60),
                      "gain_over_q7_div560": item["gain_over_zero_mobility"]/(q**7/560),
                      "gap_squared_over_prediction": q*q/(2*np.sqrt(3)*excess)})
    assert all(abs(d["relative_difference"]) < 1e-3 for d in duals)
    result = {"onset_eta": ONSET, "support_merger_eta": MERGER,
              "candidate_profiles": selected, "independent_convex_dual": duals,
              "onset_asymptotics": onset}
    Path("results").mkdir(exist_ok=True)
    Path("results/placement-phase-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
