#!/usr/bin/env python3
"""Figure 6 (camshape tolerance deficits): objective deficit below the exact optimum against the
largest violation, for tolerance-feasible camshape points, with the curves D_n(eps).

Reads
  - the MINLPLib OSIL files camshape{100,200,400,800}.osil (snapshot copies in
    research-20260929/publication/minlplib-status/pages/models/osil/),
  - the 50-digit evaluations of the one-hour-run savepoints
    (research-20260929/publication/solver-runs/point_checks.json),
  - the evaluated MINLPLib points p1/p2 (paper-open-minlplib/data/numbers.json, claims_table),
and writes paper-open-minlplib/figures/fig-camshape-deficit.pdf.

D_n(eps) follows the construction of the paper's appendix on the deficit bound (Proposition
"tolerance deficit"): beta = eps/(1-eps)^3, S_1 = 1/(u-bar + eps), R_j = 1/(S_j - beta W_j),
caps u-bar + eps and 2 + eps, slope alpha + 2 eps, min-plus envelope E^eps, and
D_n(eps) = c0 * sum_j (E^eps_j - E_j). Everything is computed in Python `decimal` with 60
significant digits. This is a picture only: the certified values are the exact rational ones of
the paper. The script asserts that its values agree with the table of D_n(eps) in the camshape
appendix and with the optimal values of the camshape theorem.

Run from outside the source trees, for example
    cd /tmp && python3 <repo>/paper-open-minlplib/figures/make_fig_deficit.py
"""
import json
import math
import xml.etree.ElementTree as ET
from decimal import Decimal, getcontext
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

getcontext().prec = 60
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OSIL = REPO / 'research-20260929/publication/minlplib-status/pages/models/osil'
POINTS = REPO / 'research-20260929/publication/solver-runs/point_checks.json'
NUMBERS = HERE.parent / 'data/numbers.json'
OUT = HERE / 'fig-camshape-deficit.pdf'

SIZES = (100, 200, 400, 800)
# Sequential gray ramp for n (light to dark); text stays in INK.
SHADE = {100: '#8f8f8f', 200: '#686868', 400: '#404040', 800: '#111111'}
INK = '#1a1a1a'
MID = '#7a7a7a'


def constants(n):
    root = ET.parse(OSIL / f'camshape{n}.osil').getroot()
    ns = {'o': root.tag.split('}')[0][1:]} if root.tag.startswith('{') else {}
    pre = 'o:' if ns else ''
    vars_ = root.findall(f'.//{pre}variables/{pre}var', ns)
    assert len(vars_) == 2 * n - 1
    ubar = Decimal(vars_[0].get('ub'))
    assert all(Decimal(vars_[j].get('ub')) == 2 for j in range(1, n))
    assert all(Decimal(vars_[j].get('lb')) >= 1 for j in range(n))
    alpha = Decimal(vars_[n + 1].get('ub'))
    assert all(Decimal(v.get('ub')) == alpha and Decimal(v.get('lb')) == -alpha
               for v in vars_[n + 1:])
    qt = root.findall(f'.//{pre}quadraticCoefficients/{pre}qTerm', ns)
    c = {Decimal(q.get('coef')) for q in qt
         if int(q.get('idx')) < n - 1 and int(q.get('idxTwo')) - int(q.get('idxOne')) == 2}
    assert len(c) == 1
    coef = root.findall(f'.//{pre}objectives/{pre}obj/{pre}coef', ns)
    c0 = {-Decimal(q.text) for q in coef}
    assert len(coef) == n and len(c0) == 1
    return c.pop(), ubar, alpha, c0.pop()


def envelope(n, c, ubar, alpha, eps):
    """E^eps of the deficit construction (E^0 = E, the optimal radii)."""
    beta = eps / (1 - eps) ** 3
    S = [Decimal(1), 1 / (ubar + eps)]
    U = [Decimal(1), c]
    for j in range(1, n):
        S.append(c * S[j] - S[j - 1])
        U.append(c * U[j] - U[j - 1])
    W = [Decimal(0), Decimal(0)]
    for j in range(2, n + 1):
        W.append(W[-1] + U[j - 2])
    B = [None]
    for j in range(1, n + 1):
        cap = ubar + eps if j == 1 else 2 + eps
        den = S[j] - beta * W[j]
        B.append(min(cap, 1 / den) if den > 0 else cap)
    slope = alpha + 2 * eps
    E = B[:]                      # min-plus envelope over j >= 2; r_1 has no slope row
    for j in range(3, n + 1):
        E[j] = min(E[j], E[j - 1] + slope)
    for j in range(n - 1, 1, -1):
        E[j] = min(E[j], E[j + 1] + slope)
    return E


def main():
    data = {}
    for n in SIZES:
        c, ubar, alpha, c0 = constants(n)
        E0 = envelope(n, c, ubar, alpha, Decimal(0))
        vn = -c0 * sum(E0[1:])

        def D(eps, n=n, c=c, ubar=ubar, alpha=alpha, c0=c0, E0=E0):
            return c0 * sum(a - b for a, b in zip(envelope(n, c, ubar, alpha, eps)[1:], E0[1:]))
        data[n] = (vn, D)

    # Checks against the paper: optimal values (camshape theorem, part (d)) and the
    # D_n table of the camshape appendix (values rounded up there).
    floors = {100: '-4.28414712174675', 200: '-4.27850023299273',
              400: '-4.27568847892555', 800: '-4.27427414195420'}
    for n in SIZES:
        vn = data[n][0]
        assert Decimal(floors[n]) <= vn <= Decimal(floors[n]) + Decimal('1e-14'), (n, vn)
    table = [(100, '1e-10', '6.05e-7'), (100, '1e-8', '6.05e-5'), (200, '1e-10', '2.36e-6'),
             (400, '1e-10', '9.35e-6'), (400, '3e-10', '2.81e-5'), (800, '3e-10', '1.13e-4')]
    for n, e, up in table:
        d = data[n][1](Decimal(e))
        assert Decimal(up) * Decimal('0.99') < d <= Decimal(up), (n, e, d)
        print(f'D_{n}({e}) = {d:.5e}  (table: <= {up})')

    # Points: (n, largest violation, objective, kind)
    pts = []
    for p in json.loads(POINTS.read_text()):
        if p['instance'].startswith('camshape'):
            pts.append((int(p['instance'][8:]), Decimal(p['max_viol']), Decimal(p['obj']),
                        p['solver']))
    claims = json.loads(NUMBERS.read_text())['claims_table']
    for r in claims:
        if r['source'] == 'MINLPLib point' and r['model'].startswith('camshape'):
            pts.append((int(r['model'][8:]), Decimal(r['violation']), Decimal(r['value']),
                        f"MINLPLib {r['claim']}"))
    rows = []
    for n, eps, obj, kind in pts:
        vn, D = data[n]
        deficit = vn - obj
        bound = D(eps)
        assert deficit > 0 and deficit <= bound, (n, kind)
        rows.append((n, float(eps), float(deficit), kind, float(deficit / bound)))
        print(f'camshape{n:<4d} {kind:12s} eps={float(eps):.3e} deficit={float(deficit):.4e} '
              f'D={float(bound):.4e} ratio={float(deficit / bound):.3f}')

    plt.rcParams.update({'font.size': 7, 'font.family': 'DejaVu Sans', 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'pdf.fonttype': 42})
    fig, ax = plt.subplots(figsize=(5.0, 3.1))
    grid = [Decimal(10) ** (Decimal(k) / 4) for k in range(-56, -23)]   # 1e-14 .. 1e-6
    for n in SIZES:
        D = data[n][1]
        ys = [float(D(e)) for e in grid]
        xs = [float(e) for e in grid]
        ax.plot(xs, ys, color=SHADE[n], lw=1.3, zorder=2)
    marker = {'BARON': ('o', 'BARON (one-hour runs)'), 'GUROBI': ('s', 'Gurobi (one-hour runs)'),
              'SCIP': ('^', 'SCIP (one-hour runs)'), 'MINLPLib p1': ('D', 'MINLPLib points p1'),
              'MINLPLib p2': ('v', 'MINLPLib points p2')}
    seen = set()
    for n, eps, deficit, kind, ratio in rows:
        m, lab = marker[kind]
        ax.scatter([eps], [deficit], marker=m, s=26, facecolor=SHADE[n], edgecolor='white',
                   linewidths=0.8, zorder=4, label=None if kind in seen else lab)
        seen.add(kind)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-14, 2e-6)
    ax.set_ylim(1e-13, 1.0)
    # Curve labels along each line, rotated to its slope in display coordinates.
    fig.canvas.draw()
    for n, x0 in zip(SIZES, (4e-11, 7e-12, 1.2e-12, 2e-13)):
        D = data[n][1]
        y0 = float(D(Decimal(x0)))
        y1 = float(D(Decimal(x0) * 10))
        (px0, py0), (px1, py1) = ax.transData.transform([(x0, y0), (x0 * 10, y1)])
        angle = math.degrees(math.atan2(py1 - py0, px1 - px0))
        ax.text(x0, y0 * 1.35, f'$D_{{{n}}}(\\varepsilon)$', color=INK, fontsize=6.5,
                va='bottom', ha='center', rotation=angle, rotation_mode='anchor')
    ax.set_xlabel(r'largest row or bound violation $\varepsilon$ of the point')
    ax.set_ylabel(r'deficit $v_n - f$ below the exact optimum')
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.grid(True, which='major', color='#ececec', lw=0.5, zorder=0)
    handles, labels = ax.get_legend_handles_labels()
    order = [labels.index(marker[k][1]) for k in marker if marker[k][1] in labels]
    leg = ax.legend([handles[i] for i in order], [labels[i] for i in order], loc='lower right',
                    frameon=False, fontsize=6.3, handletextpad=0.3, borderaxespad=0.2)
    for h in leg.legend_handles:
        h.set_facecolor(MID)
    fig.tight_layout()
    fig.savefig(OUT)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
