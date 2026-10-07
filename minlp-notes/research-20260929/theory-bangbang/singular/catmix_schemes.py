"""Discrete singular points of catmix (reduced 1-D form) under four one-step
schemes, and the symbol of the discrete accessory (second-variation) problem.

For a time-invariant one-step map theta' = F(theta, u) with stage cost
L(theta, u), a stationary discrete singular point is a solution of
  F(theta, u) = theta,  q = L_theta / (1 - F_theta),  L_u + q F_u = 0,
with u interior.  With Lagr = L + q F, the second variation along
delta theta_{t+1} = F_theta delta theta_t + F_u delta u_t is a Toeplitz form
with symbol (per unit |delta u|^2, up to a factor 1/4)
  f(om) = Lagr_uu + 2 Lagr_thu Re G + Lagr_thth |G|^2,  G = F_u / (e^{i om} - F_theta).
f >= 0 on [0, pi] is necessary for a long run of fractional stages to be
locally optimal, and by the discrete KYP lemma it is the condition for a
stationary quadratic storage (calibration) phi = q theta + P theta^2/2 to be
exact at every such stage.  om = pi is the alternating ("chattering")
direction.  Schemes: Euler in theta, Euler in x (2-D), exact flow
(piecewise-constant control), trapezoidal rule (COPS, Cayley map in y).
"""
import mpmath as mp

mp.mp.dps = 50


def a_(t):
    return t * t - t


def b_(t):
    return 1 - 10 * t - t * t


def scheme(name, h):
    h = mp.mpf(h)
    if name == "Euler-theta":
        def FL(t, u):
            return t + h * (a_(t) + b_(t) * u), h * (-t + t * u)
    elif name == "Euler-x":
        def FL(t, u):
            m = 1 - h * (1 - u) * t
            return (t + h * (u * (1 - 11 * t) - (1 - u) * t)) / m, mp.log(m)
    elif name == "trapezoid":
        def FL(t, u):
            A = mp.matrix([[-u, 10 * u], [u, -10 * u - (1 - u)]])
            I = mp.eye(2)
            C = mp.inverse(I - h / 2 * A) * (I + h / 2 * A)
            z = C * mp.matrix([1 - t, t])
            c = z[0] + z[1]
            return z[1] / c, mp.log(c)
    elif name == "exact flow":
        def FL(t, u):
            # integrate thetadot = a + b u, cdot = -(1-u) theta over [0, h] (Taylor, high order)
            f = mp.odefun(lambda s, y: [a_(y[0]) + b_(y[0]) * u, -(1 - u) * y[0]], 0, [t, mp.mpf(0)])
            y = f(h)
            return y[0], y[1]
    else:
        raise ValueError(name)
    return FL


def derivs(FL, t, u, eps=mp.mpf(10) ** -12):
    """F, L and first/second partial derivatives by high-precision central differences."""
    def F(tt, uu):
        return FL(tt, uu)[0]

    def L(tt, uu):
        return FL(tt, uu)[1]

    out = {}
    for nm, fn in (("F", F), ("L", L)):
        out[nm] = fn(t, u)
        out[nm + "t"] = (fn(t + eps, u) - fn(t - eps, u)) / (2 * eps)
        out[nm + "u"] = (fn(t, u + eps) - fn(t, u - eps)) / (2 * eps)
        out[nm + "tt"] = (fn(t + eps, u) - 2 * fn(t, u) + fn(t - eps, u)) / eps ** 2
        out[nm + "uu"] = (fn(t, u + eps) - 2 * fn(t, u) + fn(t, u - eps)) / eps ** 2
        out[nm + "tu"] = (fn(t + eps, u + eps) - fn(t + eps, u - eps) - fn(t - eps, u + eps)
                          + fn(t - eps, u - eps)) / (4 * eps ** 2)
    return out


def fixed_point(FL, guess=(mp.mpf("0.0706"), mp.mpf("0.2271"))):
    def eqs(t, u):
        d = derivs(FL, t, u)
        q = d["Lt"] / (1 - d["Ft"])
        return [d["F"] - t, d["Lu"] + q * d["Fu"]]
    t, u = mp.findroot(eqs, guess, tol=mp.mpf(10) ** -30)
    d = derivs(FL, t, u)
    q = d["Lt"] / (1 - d["Ft"])
    return t, u, q, d


def symbol(d, q, om):
    Luu = d["Luu"] + q * d["Fuu"]
    Ltu = d["Ltu"] + q * d["Ftu"]
    Ltt = d["Ltt"] + q * d["Ftt"]
    G = d["Fu"] / (mp.expj(om) - d["Ft"])
    return Luu + 2 * Ltu * mp.re(G) + Ltt * abs(G) ** 2


if __name__ == "__main__":
    import sys
    names = ["Euler-theta", "Euler-x", "trapezoid", "exact flow"]
    hs = [mp.mpf(1) / 100, mp.mpf(1) / 200, mp.mpf(1) / 400]
    for nm in names:
        for h in hs:
            if nm == "exact flow" and h < mp.mpf(1) / 200:
                continue
            FL = scheme(nm, h)
            t, u, q, d = fixed_point(FL)
            fpi = symbol(d, q, mp.pi)
            oms = [mp.pi * k / 64 for k in range(1, 65)]
            fs = [symbol(d, q, om) for om in oms]
            kmin = min(range(len(fs)), key=lambda k: fs[k])
            # also the tangential stage curvature with discrete tangency:
            # rho_tu = 0 -> P = -Lagr_tu/(F_t F_u);  rho_uu = Lagr_uu + P F_u^2
            Luu = d["Luu"] + q * d["Fuu"]
            Ltu = d["Ltu"] + q * d["Ftu"]
            P = -Ltu / (d["Ft"] * d["Fu"])
            rho_uu = Luu + P * d["Fu"] ** 2
            print("%-12s h=1/%d theta_s^h=%.10f u_s^h=%.10f  f(pi)/h^2=% .6f f(pi)/h^3=% .5f  "
                  "min_om f/h^3=% .5f at om/pi=%.3f  f(pi/64)/h^3=% .4e  P_disc=% .5f  rho_uu/h^2=% .6f"
                  % (nm, int(1 / h), float(t), float(u), float(fpi / h ** 2), float(fpi / h ** 3),
                     float(fs[kmin] / h ** 3), float(oms[kmin] / mp.pi), float(fs[0] / h ** 3),
                     float(P), float(rho_uu / h ** 2)), flush=True)
