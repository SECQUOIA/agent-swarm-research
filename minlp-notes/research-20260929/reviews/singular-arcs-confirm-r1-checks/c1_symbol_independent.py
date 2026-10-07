"""Confirmation check c1 (independent code; nothing imported from the note's
scripts).  COPS catmix in the projective coordinate, one-step maps written
from the linear system y' = A(u) y, A(u) = [[-u, 10u], [u, -1-9u]]:
  trapezoid (Cayley):  C(u) = (I - h/2 A)^{-1} (I + h/2 A)
  exact flow:          C(u) = expm(h A)
theta' = (C y)_2 / c, stage cost L = log c, c = (1,1) C y, y = (1-theta, theta).

For each scheme: stationary discrete singular point, accessory symbol f,
f(0), f(pi), f''(pi), exact zero om0 of f near pi, d0 = pi - om0, pi/d0;
the transfer-matrix half-trace of the linearized first-order recursion
(derived here from the stage Hessian, not from the note's closed form);
m+ = (1-a)^2 f(0), m- = (1+a)^2 f(pi).
Also: a small algebraic example for Remark 3.9's bullet "f > 0 on the
circle => eigenvalues real and negative".
"""
import mpmath as mp

mp.mp.dps = 40


def Amat(u):
    return mp.matrix([[-u, 10 * u], [u, -1 - 9 * u]])


def make(name, h):
    def FL(t, u):
        A = Amat(u)
        I = mp.eye(2)
        if name == "trapezoid":
            C = mp.inverse(I - h / 2 * A) * (I + h / 2 * A)
        else:
            C = mp.expm(h * A)
        z = C * mp.matrix([1 - t, t])
        c = z[0] + z[1]
        return z[1] / c, mp.log(c)
    return FL


def analyse(name, N):
    h = mp.mpf(1) / N
    FL = make(name, h)
    F = lambda t, u: FL(t, u)[0]
    L = lambda t, u: FL(t, u)[1]

    def eqs(t, u):
        Ft = mp.diff(F, (t, u), (1, 0))
        Fu = mp.diff(F, (t, u), (0, 1))
        Lt = mp.diff(L, (t, u), (1, 0))
        Lu = mp.diff(L, (t, u), (0, 1))
        q = Lt / (1 - Ft)
        return [F(t, u) - t, (Lu + q * Fu) / h]

    t, u = mp.findroot(eqs, (mp.mpf("0.0706"), mp.mpf("0.2271")))
    a = mp.diff(F, (t, u), (1, 0))
    c = mp.diff(F, (t, u), (0, 1))
    q = mp.diff(L, (t, u), (1, 0)) / (1 - a)
    Lag = lambda tt, uu: L(tt, uu) + q * F(tt, uu)
    Q = mp.diff(Lag, (t, u), (2, 0))
    S = mp.diff(Lag, (t, u), (1, 1))
    R = mp.diff(Lag, (t, u), (0, 2))

    def f(om):
        G = c / (mp.expj(om) - a)
        return R + 2 * S * mp.re(G) + Q * abs(G) ** 2

    f0, fpi = f(mp.mpf(0)), f(mp.pi)
    f2 = mp.diff(f, mp.pi, 2)
    out = dict(name=name, N=N, theta=t, u=u, f0_over_h=f0 / h, fpi_over_h3=fpi / h ** 3,
               f2_over_h3=f2 / h ** 3)
    if fpi < 0:
        om0 = mp.findroot(f, mp.pi - mp.mpf("0.26"))
        out["d0"] = mp.pi - om0
        out["pi_over_d0"] = mp.pi / out["d0"]
    # linearized first-order recursion, built from the stage Hessian:
    # unknowns (dth_t, lam_{t+1}); conditions
    #   S dth_t + R du_t + c lam_{t+1} = 0          (stationarity in u)
    #   lam_t = Q dth_t + S du_t + a lam_{t+1}      (costate)
    #   dth_{t+1} = a dth_t + c du_t                (state)
    # map (dth_t, lam_t) -> (dth_{t+1}, lam_{t+1}) computed numerically.
    def step(x):
        dth, lam = x
        # unknowns du, lamn: R du + c lamn = -S dth ; S du + a lamn = lam - Q dth
        M = mp.matrix([[R, c], [S, a]])
        rhs = mp.matrix([-S * dth, lam - Q * dth])
        du, lamn = mp.lu_solve(M, rhs)
        return (a * dth + c * du, lamn)
    c1 = step((mp.mpf(1), mp.mpf(0)))
    c2 = step((mp.mpf(0), mp.mpf(1)))
    Phi = mp.matrix([[c1[0], c2[0]], [c1[1], c2[1]]])
    out["det_Phi"] = mp.det(Phi)
    out["halftrace_Phi"] = (Phi[0, 0] + Phi[1, 1]) / 2
    out["m_plus_over_h3"] = (1 - a) ** 2 * f0 / h ** 3
    out["m_minus_over_h3"] = (1 + a) ** 2 * fpi / h ** 3
    if fpi < 0:
        out["cos_om0"] = mp.cos(mp.pi - out["d0"])
    return out


if __name__ == "__main__":
    T1, T2, J_CH = 0.136299034595, 0.725230107592, {100: -0.0480694320309772, 200: -0.0480591455801168,
                                                     400: -0.0480565477567615}
    for name, Ns in (("trapezoid", (100, 200, 400)), ("exact flow", (100, 400))):
        for N in Ns:
            r = analyse(name, N)
            line = "%s N=%d theta=%.12f u=%.12f f(0)/h=%.6f f(pi)/h^3=%.6f f''(pi)/h^3=%.5f " % (
                name, N, float(r["theta"]), float(r["u"]), float(r["f0_over_h"]), float(r["fpi_over_h3"]),
                float(r["f2_over_h3"]))
            if "d0" in r:
                line += "d0=%.6f pi/d0=%.4f cos(om0)=%.12f " % (float(r["d0"]), float(r["pi_over_d0"]),
                                                               float(r["cos_om0"]))
            line += "det(Phi)-1=%.1e trPhi/2=%.12f m+/h^3=%.5f m-/h^3=%.5f" % (
                float(r["det_Phi"] - 1), float(r["halftrace_Phi"]), float(r["m_plus_over_h3"]),
                float(r["m_minus_over_h3"]))
            print(line, flush=True)
            if name == "trapezoid":
                h = 1.0 / N
                pred = 0.5 * float(r["u"]) ** 2 * abs(float(r["fpi_over_h3"])) * h ** 3 * (T2 - T1) * N * (1 + J_CH[N])
                print("   predicted chattering gain (1/2)u_s^2|f(pi)|(t2-t1)N(J+1) = %.4e" % pred, flush=True)
    # Remark 3.9, bullet 2: f > 0 on the circle does not force negative eigenvalues.
    a, c, Q, S, R = mp.mpf("0.5"), mp.mpf(1), mp.mpf(1), mp.mpf(0), mp.mpf(1)
    fmin = min(R + 2 * S * mp.re(c / (mp.expj(w) - a)) + Q * abs(c / (mp.expj(w) - a)) ** 2
               for w in mp.linspace(0, mp.pi, 200))
    tr2 = (Q * c ** 2 - 2 * S * a * c + R * (1 + a ** 2)) / (2 * (a * R - c * S))
    print("toy n=1 (a, c, Q, S, R) = (0.5, 1, 1, 0, 1): min f = %.4f > 0; trPhi/2 = %.4f "
          "(eigenvalues %s)" % (float(fmin), float(tr2),
                                [float(tr2 + s * mp.sqrt(tr2 ** 2 - 1)) for s in (1, -1)]))
