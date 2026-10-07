"""Sampling check of the one floating-point assumption of indep_cert.py that is not proved:
numpy's float64 exp has relative error at most 1e-14 for arguments whose result is used
relatively (x >= -700; the certifier treats smaller arguments separately).  Evidence, not proof.
Reference: mpmath at 40 digits.  Argument families: uniform on [-700, 0] (term exponents E0 and
the natural-enclosure ends), uniform on [0, 20] (exp(ell), ell <= 16.97), small |x|, and the
float neighbours of k*ln2/2 (boundaries of common argument reductions)."""
import sys
import numpy as np
import mpmath as mp

mp.mp.dps = 40
rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 11)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
fam = {
    "uniform[-700,0]": rng.uniform(-700, 0, n),
    "uniform[0,20]": rng.uniform(0, 20, n // 4),
    "small": rng.uniform(-1, 1, n // 4) * 10.0 ** rng.uniform(-20, 0, n // 4),
}
k = np.arange(-2020, 60)
b = k * np.log(2.0) / 2
fam["near k ln2/2"] = np.concatenate([b, np.nextafter(b, -np.inf), np.nextafter(b, np.inf)])
fam["near k ln2/2"] = fam["near k ln2/2"][fam["near k ln2/2"] >= -700]
worst_all = 0.0
for name, x in fam.items():
    e = np.exp(x)
    worst, wx = 0.0, None
    for xi, ei in zip(x.tolist(), e.tolist()):
        t = mp.exp(mp.mpf(xi))
        r = float(abs(mp.mpf(ei) / t - 1))
        if r > worst:
            worst, wx = r, xi
    worst_all = max(worst_all, worst)
    print(f"{name}: {len(x)} arguments, max relative error {worst:.3e} (at x = {wx!r}), "
          f"= {worst / 2**-53:.3f} u", flush=True)
print(f"overall max relative error {worst_all:.3e}; assumption 1e-14 {'holds' if worst_all <= 1e-14 else 'FAILS'} on this sample")
import numpy
feats = getattr(numpy._core._multiarray_umath, "__cpu_features__", {})
print("numpy", numpy.__version__, "dispatch features in use:",
      [f for f in ("AVX2", "FMA3", "AVX512F", "AVX512_SKX") if feats.get(f)])
