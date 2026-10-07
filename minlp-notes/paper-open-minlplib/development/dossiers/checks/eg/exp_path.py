import math, numpy as np
rng = np.random.default_rng(7)
x = rng.uniform(-700, 17, 2_000_000)
e_np = np.exp(x)                       # contiguous (SIMD path if dispatched)
e_lm = np.array([math.exp(v) for v in x.tolist()])   # glibc libm
xs = np.repeat(x, 2)[::2]              # strided view, same values
e_st = np.exp(xs)
e_sc = np.array([np.exp(np.float64(v)) for v in x[:200000].tolist()])  # numpy scalar path
print("contiguous np.exp vs glibc math.exp: differing results", int((e_np != e_lm).sum()), "of", x.size)
print("strided np.exp vs contiguous: differing", int((e_st != e_np).sum()))
print("strided np.exp vs glibc: differing", int((e_st != e_lm).sum()))
print("numpy scalar vs glibc (2e5): differing", int((e_sc != e_lm[:200000]).sum()), "; vs contiguous:", int((e_sc != e_np[:200000]).sum()))
d = np.abs(e_np - e_lm) / np.spacing(e_lm)
print("max |np - glibc| in ulps of glibc result:", float(d.max()))
import numpy._core._multiarray_umath as mu
print({k: v for k, v in mu.__cpu_features__.items() if v and k.startswith(("AVX512", "AVX2", "FMA"))})
import os
print(os.popen("ldd --version | head -1").read().strip())
