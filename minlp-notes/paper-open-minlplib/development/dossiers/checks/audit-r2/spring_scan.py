import mpmath as mp
mp.mp.dps = 60
a0, a1 = mp.mpf('1.570796327'), mp.mpf('0.7853981635')
lam, K = mp.mpf('1.78571428571429e-3'), mp.mpf('6.95652173913044e-7')
C = [mp.mpf(s) for s in ('.207','.225','.244','.263','.283','.307','.331','.362','.394','.4375','.5')]
def h(x): return (4*x-1)/(4*x-4) + mp.mpf('0.615')/x   # x6 from e3
def e4(x, c): return mp.mpf('2546.47908913782')*h(x)*x/c**2
res = []
for n in range(1, 101):
    for c in C:
        lo = max(mp.mpf('1.1'), mp.mpf('.414')/c, mp.cbrt(lam*c/(K*n)))
        hi = min(mp.cbrt(mp.mpf('0.02')*c/(K*n)), (3-c)/c)
        r6 = (14 - mp.mpf('2.1')*c - mp.mpf('1.05')*c*n)*c/(1000*K*n)
        if r6 <= 0: continue
        hi = min(hi, mp.cbrt(r6))
        if lo > hi: continue
        # e4 sublevel set is an interval (convex g); find smallest x in [lo,hi] with e4 <= 189000
        g = lambda x: e4(x, c) - 189000
        if g(lo) <= 0:
            x = lo
        else:
            xm = 1 + mp.sqrt(3)/2   # minimiser of x*x6 on (1, inf)
            xs = min(max(xm, lo), hi)
            if g(xs) > 0: continue
            a, b = lo, xs
            for _ in range(200):
                mdl = (a+b)/2
                if g(mdl) > 0: a = mdl
                else: b = mdl
            x = b
        res.append(((a0 + a1*n)*c**3*x, n, c, x))
res.sort()
print('feasible assignments:', len(res))
for v, n, c, x in res[:3]: print(mp.nstr(v, 30), n, c, mp.nstr(x, 20))
fstar = (a0 + 9*a1)*mp.mpf('.283')**3*mp.cbrt(lam*mp.mpf('.283')/(9*K))
print('closed form f* =', mp.nstr(fstar, 40))
print('d - f* =', mp.nstr(mp.mpf('0.84624567') - fstar, 10), ' round(f*, 8) =', mp.nstr(mp.mpf(round(fstar*10**8))/10**8, 10))
print('bold primal 0.8462441 below f* by', mp.nstr(fstar - mp.mpf('0.8462441'), 6), '; =bestdual= 0.8462206712 below f* by', mp.nstr(fstar - mp.mpf('0.8462206712'), 6))
