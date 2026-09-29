"""Item (1): the top-K step of Theorem 4.1.

 (a) phi(t) - t Phibar(t) <= phi(t)/(1 + t^2) on a grid (the step giving
     N E(Z - t)_+ <= K at t = sqrt(2 log(N/K)));
 (b) Monte Carlo: T_K = sum of the K largest -g_i, g iid N(0,1), against
     E-bound K(t + 1) and the w.h.p. bound K(t + 1) + sqrt(2 K log N),
     for K = ceil(N/(4(2 beta - 1) rho)), including small K (rho ~ N);
 (c) size of kappa_rho = 1 - sqrt(2 L/(rho beta)) - 1/sqrt(rho beta),
     L = log(4(2beta-1) rho), and of the realised factor
     1 - T_K/(K sqrt(rho beta)), at practical rho.
"""
import numpy as np
from scipy.stats import norm


def main():
    t = np.linspace(0, 12, 120001)
    lhs = norm.pdf(t) - t * norm.sf(t)
    rhs = norm.pdf(t) / (1 + t ** 2)
    print("(a) max of (phi - t Phibar) - phi/(1+t^2) on [0,12]: %.2e (must be <= 0)" % np.max(lhs - rhs))
    rng = np.random.default_rng(11)
    print("(b) N beta rho K reps | mean T_K | K(t+1) | max T_K | K(t+1)+sqrt(2K log N) | exceedances of the w.h.p. bound")
    for N, reps in ((10 ** 4, 400), (10 ** 5, 100), (10 ** 6, 10)):
        L = np.log(N)
        for beta in (1.0, 2.0):
            for rho in (2.5 * L, 4 * L, 8 * L, N / (10 * beta), N / beta):
                K = int(np.ceil(N / (4 * (2 * beta - 1) * rho)))
                tt = np.sqrt(2 * np.log(N / K))
                T = []
                for _ in range(reps):
                    g = rng.standard_normal(N)
                    T.append(np.sort(-g)[::-1][:K].sum())
                T = np.array(T)
                eb = K * (tt + 1); wb = eb + np.sqrt(2 * K * L)
                print("   %7d %g %9.1f %6d %4d | %9.1f | %9.1f | %9.1f | %9.1f | %d"
                      % (N, beta, rho, K, reps, T.mean(), eb, T.max(), wb, int(np.sum(T > wb))), flush=True)
    print("(c) kappa_rho and the realised factor 1 - T_K/(K sqrt(rho beta)) (one draw, N = 1e6)")
    N = 10 ** 6; L = np.log(N)
    g = rng.standard_normal(N); srt = np.sort(-g)[::-1]
    for beta in (1.0, 2.0):
        for c in (2.0, 4.0, 8.0, 16.0):
            rho = c * L / beta if beta > 1 else c * L
            K = int(np.ceil(N / (4 * (2 * beta - 1) * rho)))
            Lr = np.log(4 * (2 * beta - 1) * rho)
            kap = 1 - np.sqrt(2 * Lr / (rho * beta)) - 1 / np.sqrt(rho * beta)
            kapN = 1 - np.sqrt(2 * L / (rho * beta))
            real = 1 - srt[:K].sum() / (K * np.sqrt(rho * beta))
            print("   beta=%g rho=%.1f (rho beta/log N = %.1f) K=%d: kappa_rho = %.3f, kappa_N = %.3f, realised %.3f"
                  % (beta, rho, rho * beta / L, K, kap, kapN, real))


if __name__ == "__main__":
    main()
