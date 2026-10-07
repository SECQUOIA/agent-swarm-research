"""Cost estimate for an exp-audited rerun: time the certifier on a few hundred leaves of
eg_disc2_s part 1 and compare np.exp with a rigorous interval exp on the same arguments."""
import sys, time, glob, numpy as np
sys.path.insert(0, '../kiv')
import kan_iv as K
import indep_cert as IC
lo = np.concatenate([np.load(f)['lo'] for f in sorted(glob.glob('../res/p1_c*.npz'))])
hi = np.concatenate([np.load(f)['hi'] for f in sorted(glob.glob('../res/p1_c*.npz'))])
rng = np.random.default_rng(1)
sel = rng.choice(len(lo), 512, replace=False)
C = IC.Certifier('eg_disc2_s', "5.642100574331458")
M = C.M
# count and time np.exp calls inside the certifier
calls = {'n': 0, 'elems': 0, 't': 0.0}
_exp = np.exp
def counting_exp(x, *a, **k):
    t0 = time.perf_counter(); y = _exp(x, *a, **k); calls['t'] += time.perf_counter() - t0
    calls['n'] += 1; calls['elems'] += np.size(x); return y
IC.np = type(sys)('npwrap'); IC.np.__dict__.update(np.__dict__); IC.np.exp = counting_exp
t0 = time.perf_counter(); ok = C.certify_batch(lo[sel], hi[sel]); T = time.perf_counter() - t0
print(f"certified {int(ok.sum())}/{len(sel)} random part-1 leaves in {T:.1f} s = {1000*T/len(sel):.1f} ms/leaf; stats {C.stats}")
print(f"np.exp: {calls['n']} calls, {calls['elems']} arguments, {calls['t']:.2f} s ({calls['elems']/len(sel):.0f} arguments per leaf)")
# cost of a rigorous enclosure for the same number of arguments (finite, |x| <= 700)
x = rng.uniform(-700, 17, 2_000_000)
t0 = time.perf_counter(); E = K.iexp_pt_fast(x); t1 = time.perf_counter() - t0
t0 = time.perf_counter(); e = _exp(x); t2 = time.perf_counter() - t0
print(f"2e6 arguments: np.exp {t2:.3f} s, kan_iv.iexp_pt_fast {t1:.3f} s ({1e9*t1/x.size:.0f} ns/arg)")
inside = (E.lo <= e) & (e <= E.hi)
relw = float(np.max((E.hi - E.lo) / E.lo))
print(f"np.exp inside the rigorous enclosure for all 2e6: {bool(inside.all())}; max rel width of enclosure {relw:.2e}")
est = calls['elems'] / len(sel) * 1e-9 * (1e9 * t1 / x.size)
print(f"estimated audit overhead {1000*est:.1f} ms per leaf (vs {1000*T/len(sel):.1f} ms/leaf certification)")
