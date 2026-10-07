"""P profile of the maximal recursion around the first switch (float), close-switch toy."""
import json, numpy as np
from v_close import data, kkt_point
def prof(k1, k2, t1, t2, tk, guess, N):
    a, k = data(k1, k2, t1, t2, tk, N)
    u, sig, frac, viol, J = kkt_point(N, a, k, guess)
    h = 2.0 / N
    P = np.full(N + 1, np.nan); P[N] = 1.0
    fr = set(frac); br = None; M = np.full(N, np.nan)
    for t in range(N - 1, -1, -1):
        beta = P[t + 1] + k[t]; s = 0.0 if t in fr else abs(sig[t]); m = s / h + P[t + 1]; M[t] = m
        if m <= 0: br = t; break
        P[t] = h + P[t + 1] - beta * beta / m
    s1 = [t for t in range(1, N) if u[t] != u[t - 1]][0]
    sw2 = [t for t in range(1, N) if u[t] != u[t - 1]][-1]
    rows = [(t - s1, round(float(P[t + 1]), 3), round(float(P[t+1] + k[t]), 3), round(float(sig[t] / h), 3), round(float(M[t]), 3)) for t in range(s1 + 6, (br if br is not None else s1 - 25) - 1, -2) if t >= 0]
    return dict(N=N, s1=s1, s2=sw2, brk=br, eta_hat_after_s1=float(P[s1 + 2] + k[s1 + 1]), P_at_tk=float(P[int(tk / h) + 1]),
                rows_t_minus_s1__P_tp1__beta__sig_over_h__m=rows)
for N in (2000, 4000):
    print(json.dumps(prof(-0.5, 0.0, 0.6, 1.4, 0.59375, (0.5, 0.725), N)))
