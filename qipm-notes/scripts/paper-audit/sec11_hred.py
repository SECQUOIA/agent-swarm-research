# Section 11, thm:sdp-schur: the reduced barrier Hessian on the feasible tangent.
# Definition def:reduced-kappa says H_red = W^T grad^2 F W with F = -sum log det X.
# The theorem displays (mu0^2/mu) I; the true value is (mu0/mu)^2 I.
import numpy as np
k, mu0 = 3, 0.05
for mu in (0.05, 0.01, 0.002):
    t = mu / mu0
    for tau in (1, -1):
        X = np.zeros((k+1, k+1)); X[:k, :k] = t*np.eye(k); X[0, 0] += 1
        X[:k, k] = tau*np.eye(k)[0]; X[k, :k] = tau*np.eye(k)[0]; X[k, k] = 1
        S = np.zeros((k+1, k+1)); S[:k, :k] = mu0*np.eye(k)
        S[:k, k] = -mu0*tau*np.eye(k)[0]; S[k, :k] = -mu0*tau*np.eye(k)[0]
        S[k, k] = mu + mu0
        assert np.allclose(X @ S, mu*np.eye(k+1)), "XS != mu I"
        Xi = np.linalg.inv(X)
        vals = []
        for a in range(k):
            for b in range(a, k):
                H = np.zeros((k+1, k+1))
                H[a, b] = H[b, a] = 1/np.sqrt(2) if a != b else 1.0
                vals.append(np.trace(Xi@H@Xi@H) / np.sum(H*H))
        v = np.array(vals)
        print(f"mu={mu:g} tau={tau:+d}  W^T grad^2F W range=[{v.min():.6g},{v.max():.6g}]"
              f"  (mu0/mu)^2={(mu0/mu)**2:.6g}  mu0^2/mu={mu0**2/mu:.6g}")
