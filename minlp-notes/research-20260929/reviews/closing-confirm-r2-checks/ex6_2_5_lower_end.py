"""Recompute the lower end lb.a of the wave-2 verifier's Gibbs dual bound at 40 digits.

Runs reviews/wave2-small-verification/gibbs_bound.py unchanged, but in a temporary
working directory (it writes logs/<name>_bound.json relative to the cwd) and with
mpmath.nstr widened from 20 to 40 digits, so the stored round-to-nearest string can be
compared with the interval end it came from.
"""
import contextlib, io, json, os, shutil, sys, tempfile
import mpmath
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wave2-small-verification")
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import gibbs_bound
orig = mpmath.nstr
gibbs_bound.mpmath.nstr = lambda x, n=6, **k: orig(x, 40 if n == 20 else n, **k)
tmp = tempfile.mkdtemp()
os.makedirs(os.path.join(tmp, "logs"))
runs = [("ex6_2_5", "ex6_2_5_bb_type0_tau1e-17.json"), ("ex6_2_7", "ex6_2_7_bb_type0_tau6e-15.json")]
for name, bb in runs:
    for f in (bb, name + "_kkt.json"):
        shutil.copy(os.path.join(V, "logs", f), os.path.join(tmp, "logs", f))
os.chdir(tmp)
for name, bb in runs:
    with contextlib.redirect_stdout(io.StringIO()):
        gibbs_bound.main(name, {0: "logs/" + bb})
    d = json.load(open("logs/%s_bound.json" % name))
    print(name, "lb.a (40 digits) =", d["dual_bound"])
shown = mpmath.mpf("-70.75207783344770758")
mpmath.mp.dps = 50
lba = mpmath.mpf(json.load(open("logs/ex6_2_5_bound.json"))["dual_bound"])
print("ex6_2_5 summary display -70.75207783344770758 minus lb.a =", mpmath.nstr(mpmath.mpf("-70.75207783344770758") - lba, 4))
shutil.rmtree(tmp)
