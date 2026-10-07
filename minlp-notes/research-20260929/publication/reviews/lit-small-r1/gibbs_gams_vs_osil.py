"""Reviewer check (lit-small r1): is the MINLPLib OSIL objective of ex6_2_5 / ex6_2_7
the handbook GAMS objective (titan.princeton.edu chapter 6 files) up to constant rounding?

Method: the handbook GAMS files are copied unchanged except that the final SOLVE line is
replaced by a loop that fixes n(i,k) at sampled points and solves a model containing only
the 'obj' equation (so GAMS itself evaluates the handbook expression, in double precision).
The OSIL objective is evaluated by the reviewer's own reader (osil_eval.py) in 40-digit
mpmath at the same decimal points. Variable map checked from the OSIL rows:
x_{2+3(i-1)+(k-1)} = n(i,k)  (component i, phase k).
Numerical evidence only, not a proof.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import os, random, subprocess, sys, re
from mpmath import mp, mpf
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from osil_eval import Model
mp.dps = 40
GAMS = (_PUBLIC_HOME + '/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams')
SRC = os.path.join(here, '..', '..', 'literature', 'small', 'sources', 'titan')
OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil')
NPTS = 60
random.seed(20261002)

def run(name, hb):
    m = Model(os.path.join(OSIL, name + '.osil'))
    # check the variable map from the mass-balance rows
    for r in range(m.m):
        cols = sorted(m.lin[r]); assert cols == [3 * r, 3 * r + 1, 3 * r + 2], (r, cols)
    ntot = [mpf(m.cons[r]['lb']) for r in range(3)]
    pts = []
    for p in range(NPTS):
        x = []
        for i in range(3):
            for k in range(3):
                if p % 2 == 0:   # log-uniform in the box
                    v = mpf(10) ** (mpf(random.uniform(-7, 0))) * ntot[i]
                    v = max(v, mpf('1e-7'))
                else:            # on the mass-balance face
                    v = None
                x.append(v)
        if p % 2 == 1:
            for i in range(3):
                w = [10 ** random.uniform(-6, 0) for _ in range(3)]
                s = sum(w)
                for k in range(3):
                    x[3 * i + k] = max(mpf('1e-7'), ntot[i] * mpf(w[k]) / mpf(s))
        x = [mpf(mp.nstr(v, 17)) for v in x]
        pts.append(x)
    gms = open(os.path.join(SRC, hb)).read()
    gms = re.sub(r'SOLVE gmin USING nlp MINIMIZING gfe;\s*$', '', gms.strip())
    lines = ['set pp /p1*p%d/;' % NPTS, 'parameter pt(pp,i,k), res(pp);']
    for p, x in enumerate(pts):
        for i in range(3):
            for k in range(3):
                lines.append("pt('p%d','%d','%d') = %s;" % (p + 1, i + 1, k + 1, mp.nstr(x[3 * i + k], 17)))
    lines += ['model ev / obj /;', 'option nlp = conopt;', 'option solprint = off;',
              'loop(pp, n.fx(i,k) = pt(pp,i,k); solve ev using nlp minimizing gfe; res(pp) = gfe.l;);',
              'file fo / "%s_res.txt" /; fo.nr = 2; fo.nd = 15; fo.nw = 25;' % name,
              'put fo; loop(pp, put res(pp) /;); putclose fo;']
    gpath = os.path.join(here, 'gams', name + '_eval.gms')
    open(gpath, 'w').write(gms + '\n' + '\n'.join(lines) + '\n')
    out = subprocess.run([GAMS, gpath, 'lo=2', 'o=' + os.path.join(here, 'gams', name + '_eval.lst'),
                          'curdir=' + os.path.join(here, 'gams'), 'threads=1'], capture_output=True, text=True)
    vals = [mpf(s) for s in open(os.path.join(here, 'gams', name + '_res.txt')).read().split()]
    assert len(vals) == NPTS, (len(vals), out.stdout[-500:])
    worst = mpf(0); worst_abs = mpf(0)
    for x, g in zip(pts, vals):
        f = m.objective(x)
        worst = max(worst, abs(f - g) / (1 + abs(g)))
        worst_abs = max(worst_abs, abs(f - g))
    print(name, 'points', NPTS, ' max |f_osil - f_gams_handbook|/(1+|f|) =', mp.nstr(worst, 3),
          ' max abs diff =', mp.nstr(worst_abs, 3))

run('ex6_2_7', 'ex6.2.7.gms')
run('ex6_2_5', 'ex6.2.5.gms')
