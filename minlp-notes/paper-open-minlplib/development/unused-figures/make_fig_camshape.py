#!/usr/bin/env python3
"""Unused figure (camshape profiles): the optimal radii E_j and the comparison line R_j = 1/S_j.

Moved out of figures/ in round 2 (adjudication G2-07): no source includes it and it
supports no statement of the paper.

Reads the MINLPLib OSIL files camshape100.osil and camshape800.osil (the snapshot copies in
research-20260929/publication/minlplib-status/pages/models/osil/) and writes
paper-open-minlplib/development/unused-figures/fig-camshape-profiles.pdf.

The constants c, u-bar and alpha are read from the OSIL decimal strings. S, R = 1/S, the
bounds B and the min-plus envelope E (Section 5.1 of the paper) are computed in Python
`decimal` arithmetic with 80 significant digits. This is a picture only: the certified
values come from the exact rational computation described in the paper. The script also
prints the phase lengths (contact, maximal slope, r = 2) and the number of active convexity
rows, which must match the exact computation (64/30/6 and 63 rows for n = 100; 513/236/51
and 512 rows for n = 800).

Run from outside the source trees, for example
    cd /tmp && python3 <repo>/paper-open-minlplib/development/unused-figures/make_fig_camshape.py
"""
import xml.etree.ElementTree as ET
from decimal import Decimal, getcontext
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

getcontext().prec = 80
HERE = Path(__file__).resolve().parent
OSIL = HERE.parents[2] / 'research-20260929/publication/minlplib-status/pages/models/osil'
OUT = HERE / 'fig-camshape-profiles.pdf'

INK = '#1a1a1a'
MID = '#7a7a7a'
LIGHT = '#d9d9d9'
BAND = '#f2f2f2'


def constants(n):
    root = ET.parse(OSIL / f'camshape{n}.osil').getroot()
    ns = {'o': root.tag.split('}')[0][1:]} if root.tag.startswith('{') else {}
    pre = 'o:' if ns else ''
    vars_ = root.findall(f'.//{pre}variables/{pre}var', ns)
    assert len(vars_) == 2 * n - 1
    ubar = Decimal(vars_[0].get('ub'))
    alpha = Decimal(vars_[n + 1].get('ub'))
    assert Decimal(vars_[n + 1].get('lb')) == -alpha
    qt = root.findall(f'.//{pre}quadraticCoefficients/{pre}qTerm', ns)
    c = {Decimal(q.get('coef')) for q in qt
         if int(q.get('idx')) < n - 1 and int(q.get('idxTwo')) - int(q.get('idxOne')) == 2}
    assert len(c) == 1
    return c.pop(), ubar, alpha


def envelope(n, c, ubar, alpha):
    S = [Decimal(1), 1 / ubar]
    for j in range(1, n):
        S.append(c * S[j] - S[j - 1])
    R = [None] + [1 / S[j] if S[j] > 0 else None for j in range(1, n + 1)]
    B = [None, ubar] + [min(R[j], Decimal(2)) if R[j] is not None else Decimal(2)
                        for j in range(2, n + 1)]
    E = [None, ubar] + [min(B[k] + alpha * abs(j - k) for k in range(2, n + 1))
                        for j in range(2, n + 1)]
    return R, E


def phases(n, R, E):
    tol = Decimal('1e-60')
    contact = [j for j in range(1, n + 1) if R[j] is not None and abs(E[j] - R[j]) < tol]
    cap = [j for j in range(1, n + 1) if abs(E[j] - 2) < tol]
    m, k = max(contact), min(cap)
    assert contact == list(range(1, m + 1)) and cap == list(range(k, n + 1))
    return m, k


def main():
    plt.rcParams.update({'font.size': 7, 'font.family': 'DejaVu Sans', 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(1, 2, figsize=(5.6, 2.3), sharey=True)
    for ax, n in zip(axes, (100, 800)):
        c, ubar, alpha = constants(n)
        R, E = envelope(n, c, ubar, alpha)
        m, k = phases(n, R, E)
        # active convexity rows: u-form slack e_j(w) = 0 for w = 1/E, w_0 = 1
        w = [Decimal(1)] + [1 / E[j] for j in range(1, n + 1)]
        active = sum(1 for j in range(1, n) if abs(w[j - 1] - c * w[j] + w[j + 1]) < Decimal('1e-60'))
        print(f'n={n}: contact 1..{m} ({m}), maximal slope {m + 1}..{k - 1} ({k - 1 - m}), '
              f'r=2 {k}..{n} ({n - k + 1}); active convexity rows {active}')
        dth = 72.0 / (n + 1)                  # angle step in degrees (2*pi/5 = 72 deg)
        th = [j * dth for j in range(0, n + 2)]
        Ef = [1.0] + [float(E[j]) for j in range(1, n + 1)] + [2.0]
        Rf = [(j * dth, float(R[j])) for j in range(1, n + 1) if R[j] is not None and R[j] < 2.35]
        # phase bands
        ax.axvspan(th[m] + dth / 2, th[k] - dth / 2, color=BAND, lw=0, zorder=0)
        ax.axhline(2.0, color=MID, lw=0.6, ls=(0, (1, 1.5)), zorder=1)
        ax.plot([t for t, _ in Rf], [r for _, r in Rf], color=MID, lw=1.0, ls=(0, (4, 2)), zorder=2)
        ax.plot(th, Ef, color=INK, lw=1.4, zorder=3)
        ax.set_title(f'$n = {n}$', fontsize=7.5, pad=3)
        ax.set_xlim(0, 72)
        ax.set_ylim(0.95, 2.35)
        ax.set_xticks([0, 18, 36, 54, 72])
        ax.set_xlabel('angle $j\\,\\Delta\\theta$ (degrees)')
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        ymid = 1.08
        ax.text(th[m] / 2, 1.72, 'contact\n$E_j = R_j$', ha='center', va='bottom', fontsize=6, color=MID)
        ax.text((th[m] + th[k]) / 2, ymid, 'maximal\nslope', ha='center', va='bottom', fontsize=6,
                color=MID)
        ax.text((th[k] + 72) / 2, ymid, '$r = 2$', ha='center', va='bottom', fontsize=6, color=MID)
    axes[0].set_ylabel('radius')
    ax = axes[1]
    ax.text(48.0, 2.27, '$R_j = 1/S_j$', fontsize=6.5, color=MID, ha='right')
    j40 = round(40.0 / (72.0 / 801))          # index at about 40 degrees (n = 800)
    ax.annotate('optimal radii $E_j$', xy=(j40 * 72.0 / 801, float(E[j40])), xytext=(4.0, 1.48),
                fontsize=6.5, color=INK, ha='left', va='bottom',
                arrowprops=dict(arrowstyle='-', color=INK, lw=0.5, shrinkA=1, shrinkB=2))
    ax.text(71.0, 2.03, 'cap', fontsize=6, color=MID, ha='right', va='bottom')
    fig.tight_layout(w_pad=1.0)
    fig.savefig(OUT)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
