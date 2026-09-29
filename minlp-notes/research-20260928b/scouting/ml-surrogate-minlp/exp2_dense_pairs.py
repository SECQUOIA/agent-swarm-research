"""Experiment 2: facet counts of 1- and 2-neuron hulls with dense shared inputs over [0,1]^n."""
import random, time, collections
from hull_tools import graph_points, facets

random.seed(7)
def rand_neuron(n):
    while True:
        w = [random.choice([-4,-3,-2,-1,1,2,3,4]) for _ in range(n)]
        lo = sum(min(0, v) for v in w); hi = sum(max(0, v) for v in w)
        b = random.randint(-hi + 1, -lo - 1) if hi - lo > 2 else 0
        if lo + b < 0 < hi + b:
            return w, b

print("n  k  trials  mean_vertices  mean_facets  mean_joint  max_joint  mean_single_facets(sum)  sec")
for n in [2, 3, 4, 5]:
    for k in [1, 2]:
        trials = 20 if n <= 4 else 8
        V = []; Fn = []; J = []; S = []
        t0 = time.time()
        for _ in range(trials):
            neurons = [rand_neuron(n) for _ in range(k)]
            W = [w for w, _ in neurons]; b = [bb for _, bb in neurons]
            pts = graph_points(W, b, [0]*n, [1]*n)
            try:
                F = facets(pts)
            except AssertionError:
                continue
            V.append(len(pts)); Fn.append(len(F))
            J.append(sum(1 for f in F if sum(1 for c in f[1+n:] if c != 0) >= 2))
            if k == 2:
                s = 0
                for j in range(2):
                    Fj = facets(graph_points([W[j]], [b[j]], [0]*n, [1]*n))
                    s += sum(1 for f in Fj if f[1+n] != 0)
                S.append(s)
        ms = f"{sum(S)/len(S):.1f}" if S else "-"
        print(f"{n}  {k}  {len(V):6d}  {sum(V)/len(V):13.1f}  {sum(Fn)/len(Fn):11.1f}  {sum(J)/len(J):10.1f}  {max(J):9d}  {ms:>23}  {time.time()-t0:.1f}")
