"""Scratch check: in Z[theta], theta^3=2, the unit eps=1+theta+theta^2 (norm 1,
sigma1(eps)>1).  Every point of {y in Z^3 : y = (1,0,0) mod p^j, y in Q} with
norm 1 is a unit eps^k (k>0, sigma1>0) with eps^k = 1 mod p^j.  The order of
eps modulo p^j grows by a factor p per level (lifting the exponent), so the
smallest optimal solution has about ord*log2(sigma1(eps)) bits."""
import math

def mul(x, y, m=2):
    a1, b1, c1 = x; a2, b2, c2 = y
    # (a1+b1 t+c1 t^2)(a2+b2 t+c2 t^2), t^3=m
    return (a1*a2 + m*(b1*c2 + c1*b2), a1*b2 + b1*a2 + m*c1*c2, a1*c2 + b1*b2 + c1*a2)

def order_mod(eps, q, m=2, cap=10**7):
    x = eps; k = 1
    while tuple(v % q for v in x) != (1 % q, 0, 0):
        x = tuple(v % q for v in mul(x, eps, m)); k += 1
        if k > cap:
            return None
    return k

eps = (1, 1, 1)
th = 2 ** (1/3)
s1 = 1 + th + th*th
assert mul(eps, eps)  # sanity
for p in (5, 7):
    prev = None
    for j in range(1, 6):
        o = order_mod(eps, p**j)
        bits = o * math.log2(s1)
        print(f'p={p} j={j} input~{j*math.log2(p):.1f} bits  ord(eps mod p^j)={o} '
              f'ratio={o/prev if prev else "-"}  min optimal solution ~{bits:.0f} bits')
        prev = o
