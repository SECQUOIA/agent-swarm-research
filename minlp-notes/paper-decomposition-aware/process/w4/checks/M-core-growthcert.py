"""M-core: Lemma lem:growthcert(a) minorant and point/weighted growth on random
mixed-integer box QPs (exact), reusing the instance generator of M-core-trial.py.
usage: python3 M-core-growthcert.py SEED NINST"""
import sys, random
from fractions import Fraction as Fr
sys.argv = [sys.argv[0]] + sys.argv[1:]
import importlib.util
spec = importlib.util.spec_from_file_location("t", __file__.replace("M-core-growthcert.py", "M-core-trial.py"))
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NINST = int(sys.argv[2]) if len(sys.argv) > 2 else 50
sys.argv = [sys.argv[0], str(seed), "0"]
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
rng = random.Random(seed + 1000)
bad = 0
for k in range(NINST):
    I = t.make_instance(rng.randint(2, 5))
    n = I['n']
    for _ in range(400):
        x = [Fr(rng.randint(0, int(I['s'][i]))) if I['integer'][i] else I['s'][i] * Fr(rng.randint(0, 999), 999) for i in range(n)]
        d = [x[i] - I['xs'][i] for i in range(n)]
        Fx = t.Fval(I, x)
        if Fx < I['g'] * sum(di * di for di in d):
            bad += 1
        if Fx < I['gam'] * sum(I['L'][i] * d[i] * d[i] for i in range(n)):
            bad += 1
print("violations:", bad)
print("ALL OK" if bad == 0 else "SOME FAILURES")
