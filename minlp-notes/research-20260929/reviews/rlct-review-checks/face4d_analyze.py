"""Compare face4d bisection leaves with the Theorem 3.1 face lower bound (d = 3,
face x = 0) and with the rate eps^(lambda - n/2) = eps^(-1/4) that the original
conjecture would predict from the full-dimensional RLCT (7/4, 1).
I_F(eps) = Gamma(3/2)^-1 int_0^inf t^(1/2) e^(-t eps) G(t)^3 dt, G(t) = int_{-0.4}^{0.5} e^(-t y^4) dy."""
import json
import math

from scipy.integrate import quad

alpha = 1.05


def G(t):
    return quad(lambda y: math.exp(-t * y ** 4), -0.4, 0.5, limit=200)[0]


def IF(e):
    f = lambda t: math.sqrt(t) * math.exp(-t * e) * G(t) ** 3
    brk = [0, 1, 1 / e ** 0.5, 1 / e, 10 / e, 60 / e]
    return sum(quad(f, brk[i], brk[i + 1], limit=400)[0] for i in range(len(brk) - 1)) / math.gamma(1.5)


rows = [json.loads(l) for l in open("logs/face4d.jsonl")]
prev = None
for o in rows:
    e = o["eps"]
    lb = (alpha * 3 / math.pi ** 2) ** 1.5 * IF(e)
    sl = "" if prev is None else f"{math.log(o['leaves'] / prev['leaves']) / math.log(prev['eps'] / e):7.3f}"
    print(f"eps={e:8.1e} leaves={o['leaves']:9d} faceLB={lb:10.1f} leaves/LB={o['leaves'] / lb:6.2f} "
          f"leaves*eps^0.75={o['leaves'] * e ** 0.75:7.2f} leaves*eps^0.25={o['leaves'] * e ** 0.25:9.1f} slope={sl}")
    prev = o
