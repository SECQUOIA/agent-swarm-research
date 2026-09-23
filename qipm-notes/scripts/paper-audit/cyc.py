# Finding 1.2 -- Section 13, the sentence after thm:positive-face-repair:
#
#   "Together with the tail bound sum_{k>=t}(||p_F(r_k)||+||q_F(r_k)||) = O(mu_t),
#    these conditions give V_proj^realized <= K_0 + K_1 (L_infty + W_r)
#    in a fixed stable chart."
#
# Counterexample: the paper's own row-3-sparse family from
# prop:positive-cycling-proximal,
#     min sum_{j>=4} x_j   s.t.  x_1+x_2+x_3 = 1,  x >= 0,
# but with a VARIABLE face radius d_t = rho_{t mod 3} * mu_t.
# With rho = (1,3,1) every stated hypothesis holds (L_infty, W_r finite, tail
# exactly O(mu_t), centrality inside theta, OSS residual inside eta_n, bounded
# cross-gain) while V_proj grows linearly.  With rho = (1,1,1) it converges.
#
# Run with T <= ~250: beyond that mu_t underflows float64 and the growth
# artificially saturates.  See cyc2.py for the delta_t periodicity.

import numpy as np

U = [np.array([1., -1., 0.])/np.sqrt(2),
     np.array([0., 1., -1.])/np.sqrt(2),
     np.array([-1., 0., 1.])/np.sqrt(2)]

def run(n=64, a0=1.0, mu0=0.01, rho=(1., 3., 1.), T=240, theta=0.1):
    tau = a0/np.sqrt(n)
    A = np.zeros((1, n)); A[0, :3] = 1.0
    Q, _ = np.linalg.qr(np.array([[1., -1., 0.], [1., 1., -2.]]).T)   # 3x2, ker(1,1,1)
    V = np.zeros((n, n-1)); V[:3, :2] = Q; V[3:, 2:] = np.eye(n-3)
    assert np.allclose(A @ V, 0) and np.allclose(V.T @ V, np.eye(n-1))
    Z = Q                                        # orthonormal basis of ker A_B
    mus = [mu0*(1-tau)**t for t in range(T+2)]
    ds = [rho[t % 3]*mus[t] for t in range(T+2)]

    psi, M, rs, pF, resid, nbhd = [], [], [], [], [], []
    for t in range(T+1):
        j = t % 3
        x = np.empty(n); x[:3] = 1/3 + ds[t]*U[j]; x[3:] = mus[t]
        s = np.empty(n); s[:3] = 3*mus[t];         s[3:] = 1.0
        Moss = np.hstack([-(x[:, None]*A.T), s[:, None]*V])       # [-X A^T,  S V]
        f = (1-tau)*mus[t] - x*s
        z = np.linalg.solve(Moss, f); q = np.linalg.norm(z)
        psi.append(z/q); M.append(q/np.linalg.norm(f)*Moss)
        nbhd.append(np.linalg.norm(x*s - mus[t])/mus[t])
        r = np.zeros(n)                                           # realized-step OSS residual
        r[:3] = 3*mus[t]*(ds[t+1]*U[(j+1) % 3] - tau*ds[t]*U[j])
        rs.append(r); resid.append(np.linalg.norm(r)/np.linalg.norm(f))
        Gp = Z.T @ np.diag(s[:3]/x[:3]) @ Z                       # ker A_B^T = {0} => q_F == 0
        pF.append(np.linalg.norm(Z @ np.linalg.solve(Gp, Z.T @ (r[:3]/x[:3]))))

    delta = [np.linalg.norm(M[t+1] @ (psi[t+1] - psi[t])) for t in range(T)]
    Vproj = np.cumsum(delta)
    Wr = sum(np.linalg.norm(rs[t+1]/mus[t+1] - rs[t]/mus[t]) for t in range(T))
    Linf = sum(pF[:T+1])
    tail = max(sum(pF[t:T+1])/mus[t] for t in range(0, T, 20))
    G = max(np.linalg.norm(M[t] @ np.linalg.inv(M[j]), 2)
            for j in range(0, T, 60) for t in range(j, min(j+20, T)))

    print(f"n={n}  rho={rho}  tau={tau:.4f}  eta_n=1/sqrt(n)={1/np.sqrt(n):.4f}")
    print(f"  L_infty = sum_t ||p_F(r_t)||                  = {Linf:.4f}")
    print(f"  W_r     = sum_t ||r_{{t+1}}/mu_{{t+1}} - r_t/mu_t|| = {Wr:.4f}")
    print(f"  sup_t (sum_{{k>=t}} ||p_F(r_k)||)/mu_t          = {tail:.3f}   (tail = O(mu_t))")
    print(f"  max centrality ||XSe-mu e||/mu                = {max(nbhd):.4f}  (theta={theta})")
    print(f"  max relative OSS residual ||r||/||f||         = {max(resid):.4f}")
    print(f"  sup_{{t>=j}} ||M_t M_j^-1||  (sampled)          = {G:.3f}")
    for T0 in (33, 63, 93, 123, 153):
        print(f"  V_proj(T={T0:3d}) = {Vproj[T0-1]:8.3f}")

if __name__ == "__main__":
    run(rho=(1., 3., 1.)); print()
    run(rho=(1., 1., 1.))
