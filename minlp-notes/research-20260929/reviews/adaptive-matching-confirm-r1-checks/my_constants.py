"""Independent recomputation (confirm round 1) of the constants of adaptive-matching.md, Sections 2, 3.2,
3.3 (Remark 3.3, Corollary 3) and 4 (Corollary 4). Formulas retyped from the note; K_LS in closed form
(K_1(cK,0)^2 is affine in K), not by bisection. Double precision.
"""
import math, itertools, random

def C(k, w, kap, a):
    eta = (16*k*(k+1)*(w+1)*kap) ** -0.5
    t1 = [1/(32*k*k), eta/(8*k), 1/(648*k**4*(w+1)*kap)] + ([1/(k**1.5*math.sqrt(108*a))] if a > 0 else [])
    th1 = min(t1)
    cth = 18432*k**4*(2*k+1)*(k+1)*w*(w+1)
    th2 = eta/(2*kap*math.sqrt(cth))
    Q0 = (w+1)*(k-1)**2*kap*(144*k**3*(w+1)*kap + 12) + a/2
    Q = lambda g, th: Q0 + 2*g*kap*math.sqrt(w) + 288*k*(k+1)*w*g*g*th*th*kap*kap
    K1 = lambda g, th: max(32*k*k/eta, math.sqrt(16*k*(2*k+1)*Q(g, th))/eta)
    Ks = max(32*k*k/eta, math.sqrt(128*k*(2*k+1)*Q0/3)/eta, (512/3)*k*k*(2*k+1)*kap*math.sqrt(w*(w+1))/eta**2)
    ths = min(th1, th2)
    gam = 2*k*math.sqrt(w+1)*Ks
    # Corollary 4: least K >= 1 with K^2 >= max((32k^2/eta)^2, A + B K)
    c = 2*(k-1)*math.sqrt(w+1)
    A = 16*k*(2*k+1)*Q0/eta**2
    B = 16*k*(2*k+1)*2*c*kap*math.sqrt(w)/eta**2
    KLS = max(1.0, 32*k*k/eta, (B + math.sqrt(B*B + 4*A))/2)
    return dict(eta=eta, th1=th1, th2=th2, ths=ths, Ks=Ks, base=12*Ks + 4/ths + 4, fp=K1(gam, ths)/Ks,
                fp_parts=(16*k*(2*k+1)*Q0/eta**2/Ks**2, 16*k*(2*k+1)*2*gam*kap*math.sqrt(w)/eta**2/Ks**2,
                          16*k*(2*k+1)*288*k*(k+1)*w*gam**2*ths**2*kap**2/eta**2/Ks**2),
                K100=K1(0, 0), KLS=KLS, KLSchk=K1(c*KLS, 0)/KLS, K1=K1)

# path family of Section 8.1: M_a = 2.8 (|b| + 2), c_g = 0.1, alpha' A = 2*0.4 = 0.8
d = C(2, 1, 28.0, 8.0)
print("path family: eta=%.5g theta1=%.4g theta2=%.4g theta*=%.4g (2^%.2f) K*=%.4g R=3K*=%.4g base=%.4g" % (
    d["eta"], d["th1"], d["th2"], d["ths"], math.log2(d["ths"]), d["Ks"], 3*d["Ks"], d["base"]))
print("  K_1(gamma(K*),theta*)/K* = %.4f; parts of K_1^2/K*^2 (Q0, gamma, theta^2 gamma^2) = %.3f %.3f %.3f (bounds 3/8 3/8 1/4)" % (
    (d["fp"],) + d["fp_parts"]))
print("  K_1(0,0) = %.4g ; K_LS = %.4g (check K_1(cK_LS,0)/K_LS = %.6f)" % (d["K100"], d["KLS"], d["KLSchk"]))

# fixed-point parts bounded by 3/8, 3/8, 1/4 over a grid of parameters
worst = 0
for k, w, kap, a in itertools.product((2, 3, 5, 9), (1, 2, 4), (1.0, 3.0, 28.0, 300.0), (0.0, 1.0, 50.0)):
    if kap < 2/k: continue
    e = C(k, w, kap, a)
    p = e["fp_parts"]
    assert p[0] <= 3/8 + 1e-12 and p[1] <= 3/8 + 1e-12 and p[2] <= 1/4 + 1e-12, (k, w, kap, a, p)
    worst = max(worst, e["fp"])
print("grid of (k,w,kappa,a): max K_1(gamma(K*),theta*)/K* = %.4f (<= 1 required)" % worst)

# orders: exponents by log differences
def expo(f, s1, s2):
    return math.log(f(s2)/f(s1))/math.log(s2/s1)
print("exponent of k in K* (w=1,kappa=100,a=0): %.3f; in 1/theta*: %.3f" % (
    expo(lambda s: C(s, 1, 100., 0)["Ks"], 64, 128), expo(lambda s: 1/C(s, 1, 100., 0)["ths"], 64, 128)))
print("exponent of kappa in K* (k=4,w=1): %.3f; in 1/theta*: %.3f" % (
    expo(lambda s: C(4, 1, s, 0)["Ks"], 1e4, 2e4), expo(lambda s: 1/C(4, 1, s, 0)["ths"], 1e4, 2e4)))
print("exponent of w in K* (k=4,kappa=100): %.3f; in 1/theta*: %.3f" % (
    expo(lambda s: C(4, s, 100., 0)["Ks"], 64, 128), expo(lambda s: 1/C(4, s, 100., 0)["ths"], 64, 128)))
for k in (8, 32, 128):
    e = C(k, 1, 2/k*1.0001, 0)
    rev = k**4*1*(2/k)**1.5          # review's order k^4 w^1.5 kappa^1.5 (no constant)
    note = k**4*1*(2/k)*(1+math.sqrt(2/k))
    print("  k=%d kappa=2/k: binding %s, 1/theta*=%.3g, 1/theta*/[k^4 w^1.5 kap^1.5]=%.3g, 1/theta*/[k^4 w kap(1+sqrt(w kap))]=%.3g" % (
        k, "theta_1" if e["th1"] < e["th2"] else "theta_2", 1/e["ths"], 1/e["ths"]/rev, 1/e["ths"]/note))

# Remark 3.3 growth condition -> (Loc_T): random check of K_1(c_T K_T, theta_T) <= K_T
random.seed(1)
bad = 0
for _ in range(100000):
    k = random.randint(2, 9); w = random.randint(1, 6)
    A0, A1, A2 = (10**random.uniform(-3, 6) for _ in range(3))
    th0 = 10**random.uniform(-8, 0)
    cT = 2*(k-1)*math.sqrt(w*(w+1))
    thT = min(th0, 1/(2*A2*cT))
    KT = max(0.5, 4*A0, 16*A1*A1*cT)
    th = thT*random.random()
    if A0 + A1*math.sqrt(cT*KT) + A2*th*cT*KT > KT*(1 + 1e-12): bad += 1
print("Remark 3.3 growth condition: violations of K_1(c_T K_T, theta) <= K_T in 1e5 random cases: %d" % bad)
# K_1 = 1 + gamma: no fixed point
print("K_1 = 1+gamma: min over k>=2,w>=1 of c_T = %.4f (> 1, so 1 + c_T K > K for all K)" % (2*math.sqrt(2)))

# Corollary 3: j* <= lambda_eps + r* - 1 for r* >= ceil(0.5 log2(C_term N)) + 1, mu* >= 1
bad = 0
for _ in range(200000):
    s0 = 10**random.uniform(-2, 2); eps = 10**random.uniform(-12, 3); CN = 10**random.uniform(-6, 40)
    js = max(0, math.ceil(math.log2(s0*math.sqrt(CN/eps))))
    lam = max(0, math.ceil(math.log2(s0/math.sqrt(eps))))
    rstar = max(1, math.ceil(0.5*math.log2(CN)) + 1)
    if js > lam + rstar - 1: bad += 1
print("Corollary 3 stage cap: violations of j* <= lambda_eps + r* - 1 in 2e5 random cases: %d" % bad)
# sum_{r<=R} r 2^r <= 2 R 2^R
print("sum_{r<=R} r 2^r <= 2R 2^R for R=1..60:", all(sum(r*2**r for r in range(1, R+1)) <= 2*R*2**R for R in range(1, 61)))

# Remark 3.3 counterexample: V_p={1,2}, V_t={1,2,3}, children {1,3,5}, {2,3,6}
bags = {"p": {1, 2}, "t": {1, 2, 3}, "u1": {1, 3, 5}, "u2": {2, 3, 6}}
par = {"t": "p", "u1": "t", "u2": "t"}
def connected(S):
    S = set(S); roots = [s for s in S if par.get(s) not in S]
    return len(roots) == 1
Ti = {i: [b for b in bags if i in bags[b]] for i in (1, 2, 3, 5, 6)}
print("counterexample: T_i connected:", all(connected(v) for v in Ti.values()), " k =", max(len(v) for v in Ti.values()),
      " w =", max(len(b) for b in bags.values()) - 1,
      " bags of sub(t) meeting S_t={1,2}:", [b for b in ("t", "u1", "u2") if bags[b] & {1, 2}],
      " max over i in S_t of |sub(t) cap T_i|:", max(sum(1 for b in ("t", "u1", "u2") if i in bags[b]) for i in (1, 2)))
