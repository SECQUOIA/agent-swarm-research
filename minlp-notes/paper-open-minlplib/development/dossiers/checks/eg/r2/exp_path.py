"""Which exp does numpy 2.5.1 run here?  Compare contiguous, strided and scalar np.exp with glibc
(math.exp) bit for bit, and print numpy's own dispatch report for the float64 exp loop."""
import math, numpy as np
from numpy.lib.introspect import opt_func_info
print("numpy", np.__version__, "; float64 exp loop dispatch:", opt_func_info(func_name='^exp$')['exp']['dd'])
rng = np.random.default_rng(7)
x = rng.uniform(-700, 17, 1_000_000)
c = np.exp(x)
g = np.array([math.exp(v) for v in x.tolist()])
s = np.exp(np.repeat(x, 2)[::2])
sc = np.array([np.exp(np.float64(v)) for v in x[:100000].tolist()])
print("contiguous vs glibc differ:", int((c != g).sum()), "of", x.size, "; max |diff| in ulp:", float(np.max(np.abs(c - g) / np.spacing(g))))
print("strided vs contiguous differ:", int((s != c).sum()), "; scalar vs contiguous differ:", int((sc != c[:100000]).sum()))
