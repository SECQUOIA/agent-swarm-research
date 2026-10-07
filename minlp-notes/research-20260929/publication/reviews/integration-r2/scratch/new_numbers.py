# Own exact checks of new numbers in the r1 response (Fraction arithmetic; no repo imports).
from fractions import Fraction as F
def sci(x, d=4): return f"{float(x):.{d}e}"
# eg_disc_s display vs its binary64 value
disp = F('5.760539610694994'); b64 = F(5.760539610694994)
print('eg_disc_s display - binary64 =', sci(disp - b64), 'positive:', disp > b64)
# historical closeness: listed MINLPLib duals vs certified values (summary table values)
cam_opt_lo = F('-4.28414712174675')   # exact optimum rounded down (display)
cam_listed = F('-4.28415233')
g = (cam_opt_lo - cam_listed)
print('camshape100 listed gap abs >=', sci(g), 'rel (|opt| ~ 4.28414712) =', sci(g / F('4.28414712174675')))
lnts_dual = F('0.5546687649381'); lnts_listed = F('0.55464755'); lnts_primal = F('0.5546687649387')
print('lnts50 rel (vs dual)', sci((lnts_dual - lnts_listed) / lnts_dual), ' (vs primal display)', sci((lnts_primal - lnts_listed) / lnts_primal))
# campaign SCIP camshape100 point
scip = F('-4.284147273656973595462088684200718802231')
print('SCIP point below exact-opt display by', sci(cam_opt_lo - scip), '(exact optimum >= display, so deficit >= this)')
print('row violation', sci(F('0.0000000007717445565323549220083254248281535238797')))
# spring bisection
print('spring diff', sci(F('0.846245665643154') - F('0.846245664643154')))
# GiB
print('GiB', float(F(49321416, 1024**2)))
# eg time sums verified separately (eg_times.py)
