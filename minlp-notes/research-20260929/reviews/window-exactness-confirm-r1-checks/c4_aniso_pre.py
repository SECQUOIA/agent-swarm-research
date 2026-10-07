"""Confirmation check: anisotropic margin of the Section 7.5 family on the pre-switch arc and in the layer.
Reuses c2_sh.sigma_fun (own ODE sigma); [E]'s continuous_family is the input being tested."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from c2_sh import EX, A, b, sigma_fun, continuous_family, find_switch
out = []
for nm, eps in (("A", 0.02), ("Aminus", 0.02), ("Azero", 0.02), ("Azero", 0.1)):
    p = EX[nm]; th = find_switch(p)[0]; Pf, _ = continuous_family(p, eps, delta1=0.1); sg = sigma_fun(p, th)
    hs = 1e-5
    def marg(t):
        P = Pf(t); dP = (-Pf(t + 2*hs) + 8*Pf(t + hs) - 8*Pf(t - hs) + Pf(t - 2*hs)) / (12*hs)
        M = dP + A.T @ P + P @ A + p.Hxx; M = (M + M.T) / 2
        beta = P @ b - p.w; s = abs(sg(t))
        return float(np.linalg.eigvalsh(M - 2*eps*np.eye(2) - 2.0/(2*s)*np.outer(beta, beta))[0])
    pre = [marg(t) for t in np.linspace(1e-3, th - 1e-3, 800)]
    lay = [marg(t) for t in np.linspace(th + 1e-3, th + 0.1 - 1e-3, 200)]
    rec = dict(example=nm, eps=eps, pre_min=min(pre), pre_max=max(pre), layer_min=min(lay), layer_max=max(lay))
    print(json.dumps(rec), flush=True); out.append(rec)
json.dump(out, open(os.path.join(HERE, "logs", "c4_aniso_pre.json"), "w"), indent=1)
