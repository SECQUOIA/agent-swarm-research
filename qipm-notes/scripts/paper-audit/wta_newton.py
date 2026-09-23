# Finding 1.1 -- Section 7 (winner-take-all), eq:wta-decrement / eq:wta-next-decrement.
#
# After the paper's exact elimination of the P path copies (orthogonal R_{g,i}),
# the function minimized on the root slice is
#
#     Psi(Z) = sum_g <Cbar_{h_g}, Z_g>  -  tau * sum_g log det Z_g ,
#     subject to  sum_g tr Z_g = 1,  Z_g > 0,        tau = mu * P = 1/G
#
# because mu = 1/(GP) in eq:wta-start-barrier.  For F standard self-concordant,
# tau*F is standard only when tau >= 1; here tau = 1/G < 1 for G >= 2.
#
# This script prints the Newton decrement in BOTH normalizations:
#   lam_phi  = decrement of Psi itself          (the paper's lambda; = 1/sqrt(150))
#   lam_std  = lam_phi / sqrt(tau) = sqrt(G/150) (the standard self-concordant one)
# The full-step estimate lam_next <= (lam/(1-lam))^2 needs lam_std < 1, which
# fails for G >= 150.  The *conclusion* nevertheless holds: lam_phi drops from
# 0.0816497 to about 2.9e-3, well under the claimed 0.0079048.

import numpy as np

H12 = np.zeros((3, 3)); H12[0, 1] = H12[1, 0] = 1
H13 = np.zeros((3, 3)); H13[0, 2] = H13[2, 0] = 1
H23 = np.zeros((3, 3)); H23[1, 2] = H23[2, 1] = 1
u = 0.1

def Ah(h):    return H12 + H23 + h*H13
def Cbar(h):  return 3*np.eye(3) + u*Ah(h)

def newton(G, hs, nsteps=4):
    """Exact Newton on the root slice from the public start Z_g = I/(3G)."""
    tau = 1.0/G
    Z = [np.eye(3)/(3*G) for _ in range(G)]
    print(f"  G={G:<5d} tau={tau:.4g}   (claimed bound on next decrement: 0.0079048)")
    for k in range(nsteps):
        Zinv = [np.linalg.inv(Zg) for Zg in Z]
        grad = [Cbar(hs[g]) - tau*Zinv[g] for g in range(G)]
        # Hessian action  H[Y]_g = tau * Zinv_g Y_g Zinv_g ;  H^{-1}[W]_g = Z_g W_g Z_g / tau
        Hinv = lambda Ws: [(Z[g] @ Ws[g] @ Z[g])/tau for g in range(G)]
        a = Hinv([-grad[g] for g in range(G)])
        b = Hinv([np.eye(3) for _ in range(G)])
        nu = (sum(np.trace(a[g]) for g in range(G))
              / sum(np.trace(b[g]) for g in range(G)))          # trace-constraint multiplier
        Y = [a[g] - nu*b[g] for g in range(G)]                  # Newton step, sum_g tr Y_g = 0
        lam2 = sum(np.sum(-(grad[g] + nu*np.eye(3)) * Y[g]) for g in range(G))
        lam = np.sqrt(max(lam2, 0.0))
        mineig = min(np.linalg.eigvalsh(Z[g] + Y[g]).min() for g in range(G))
        print(f"    step {k}:  lam_phi = {lam:.7f}   lam_std = lam_phi/sqrt(tau) = "
              f"{lam/np.sqrt(tau):.7f}   full-step min eig = {mineig:.4e}")
        if mineig <= 0:
            print("    FULL STEP INFEASIBLE"); return
        Z = [Z[g] + Y[g] for g in range(G)]

if __name__ == "__main__":
    print("one odd group (h_1 = -1, rest +1):")
    for G in (2, 10, 150, 1000):
        newton(G, [-1] + [1]*(G-1))
        print()
