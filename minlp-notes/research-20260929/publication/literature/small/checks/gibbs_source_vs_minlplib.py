"""Compare the handbook GAMS Gibbs models (titan.princeton.edu, chapter 6,
ex6.2.5 and ex6.2.7, archived copies in ../sources/titan/) with the MINLPLib
scalar models (../sources/minlplib_gms/ex6_2_5.gms, ex6_2_7.gms).

The handbook objective is re-implemented here from the GAMS source text
(parameters copied by hand, formulas transcribed), evaluated in 40-digit
mpmath, and compared with the MINLPLib objective (parsed by compare_gms.py's
evaluator) at random points of the variable box.  This is numerical evidence
that the MINLPLib model is the handbook model with constants rounded to
double precision by GAMS Convert; it is not a proof.
Variable map (from the MINLPLib start values, which equal the handbook n.l):
  MINLPLib x2,x3,x4 = n(1,1),n(1,2),n(1,3); x5,x6,x7 = n(2,*); x8,x9,x10 = n(3,*).
"""
import random, sys, os
from mpmath import mp, mpf, log, exp
mp.dps = 40
here = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], 'x', 'x']
import importlib.util
spec = importlib.util.spec_from_file_location('cg', os.path.join(here, 'compare_gms.py'))
src = open(os.path.join(here, 'compare_gms.py')).read().split("a, b = sys.argv[1]")[0]
cg = {}
exec(src, cg)

def handbook(name, n):
    z = mpf(10)
    if name == 'ex6_2_7':
        T = mpf(295); P = mpf(1)
        liq = [1, 1, 1]; gform = None
        q = [mpf('2.2480'), mpf('7.3720'), mpf('1.8680')]; qp = list(q)
        r = [mpf('2.4088'), mpf('8.8495'), mpf('2.0086')]
        bina = [[0, mpf('247.2'), mpf('54.701')], [mpf('69.69'), 0, mpf('305.52')], [mpf('467.88'), mpf('133.19'), 0]]
        psi_rule = 'za'
    else:
        T = mpf('721.67659'); P = mpf('1.16996')
        liq = [1, 1, 0]
        gform = [mpf('-0.3658348'), mpf('-0.9825555'), mpf('-0.3663657')]
        q = [mpf('3.6640'), mpf('5.1680'), mpf('1.4000')]
        qp = [mpf('4.0643'), mpf('5.7409'), mpf('1.6741')]
        r = [mpf('3.9235'), mpf('6.0909'), mpf('0.9200')]
        bina = [[0, mpf('-193.141'), mpf('424.025')], [mpf('415.855'), 0, mpf('315.312')], [mpf('103.810'), mpf('3922.5'), 0]]
        psi_rule = 'zrzb'
    tau = [[exp(-mpf(bina[i][j]) / T) for j in range(3)] for i in range(3)]
    zr = [(z * q[i] / 2 - 1) / r[i] for i in range(3)]
    zrm = min(zr)
    zb = [sum(zr[j] - zrm for j in range(3) if j != i) for i in range(3)]
    za = zrm + sum(zr[i] - zrm for i in range(3))
    psi = [qp[i] + r[i] * (za if psi_rule == 'za' else zr[i] + zb[i]) for i in range(3)]
    g = mpf(0)
    for k in range(3):
        nk = [n[i][k] for i in range(3)]
        if not liq[k]:
            s = sum(nk)
            g += sum(nk[i] * (log(nk[i] / s) + log(P)) for i in range(3))
            continue
        if gform:
            g += sum(nk[i] * gform[i] for i in range(3))
        R = sum(r[j] * nk[j] for j in range(3)); Q = sum(q[j] * nk[j] for j in range(3))
        QP = sum(qp[j] * nk[j] for j in range(3))
        g += sum(nk[i] * (z * q[i] * log(q[i]) / 2 - zr[i] * r[i] * log(r[i])) for i in range(3))
        g += sum(za * r[i] * nk[i] for i in range(3)) * log(R)
        g += sum(zb[i] * r[i] * nk[i] * log(nk[i]) for i in range(3))
        g += sum(-zb[i] * r[i] * nk[i] * log(R) for i in range(3))
        g += sum((z / 2) * q[i] * nk[i] * log(nk[i]) for i in range(3))
        g += sum(-(z / 2) * q[i] * nk[i] * log(Q) for i in range(3))
        g += QP * log(QP)
        g += sum(qp[i] * nk[i] * log(nk[i]) for i in range(3))
        g += sum(-qp[i] * nk[i] * log(sum(qp[j] * tau[j][i] * nk[j] for j in range(3))) for i in range(3))
        g += sum(-psi[i] * nk[i] * log(nk[i]) for i in range(3))
    return g

random.seed(7)
for name in ['ex6_2_7', 'ex6_2_5']:
    eqs, bnd, pos, var = cg['parse'](os.path.join(here, '..', 'sources', 'minlplib_gms', name + '.gms'))
    lhs, kind, rhs = eqs['e1']
    worst = mpf(0)
    for _ in range(200):
        x = {'objvar': mpf(0)}
        for v in ['x%d' % i for i in range(2, 11)]:
            lo, up = bnd[v]['lo'], bnd[v]['up']
            x[v] = lo + (up - lo) * mpf(random.random()) ** 3   # favour small amounts
        # MINLPLib e1:  -(G) + objvar = 0  ->  G = value of the expression with objvar = 0, negated
        G_mlib = -(cg['ev'](lhs, x) - cg['ev'](rhs, x))
        n = [[x['x2'], x['x3'], x['x4']], [x['x5'], x['x6'], x['x7']], [x['x8'], x['x9'], x['x10']]]
        G_hb = handbook(name, n)
        d = abs(G_mlib - G_hb) / (1 + abs(G_hb))
        worst = max(worst, d)
    print(name, 'max |G_minlplib - G_handbook| / (1+|G|) over 200 random points:', mp.nstr(worst, 4))
