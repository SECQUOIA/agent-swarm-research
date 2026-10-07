#!/usr/bin/env python3
"""Figure 5 (audit margins): margins of the refuted and (i-r) listed dual bounds.

For every conflict between a listed per-solver dual bound d (minimization) and the upper end phi
of the objective enclosure at an exactly feasible point (written f in the data files), the figure
plots the margin d - phi in units of the last displayed digit of d (x axis) against the relative
margin (d - phi)/|d| (y axis).

Data:
- class (i), 19 pairs: paper-open-minlplib/data/numbers.json, audit.pairs (d and the exact
  upper end f_upper_exact);
- rocket100/200/400 (outside the screen): numbers.json, audit.rocket (d and f_upper);
- class (i-r), 12 pairs on 4 instances: the exact values of Table "tab:audit-ir" (Appendix E),
  from research-20260929/publication/audit-ir/report.md; the spring value is the proved optimum
  (a0 + 9 a1) 0.283^3 x5*, x5* = (lambda 0.283/(9 K))^(1/3) (Proposition "prop:spring-opt").

Pairs with equal (d, f) are drawn once. Margins are computed with exact fractions and converted
to floats for plotting only; the printed margins in the paper come from numbers.json.

Run from outside the source trees, for example
    cd /tmp && python3 <repo>/paper-open-minlplib/figures/make_fig_audit.py
"""
import json
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

getcontext().prec = 60
HERE = Path(__file__).resolve().parent
NUMBERS = HERE.parent / 'data' / 'numbers.json'
OUT = HERE / 'fig-audit-margins.pdf'

INK = '#1a1a1a'
MID = '#7a7a7a'
LIGHT = '#bdbdbd'


def unit(s):
    """Unit of the last nonzero displayed digit of the decimal string s (s != 0)."""
    s = s.strip().lstrip('-')
    if '.' in s:
        a, b = s.split('.')
        b = b.rstrip('0')
        if b:
            return Q(1, 10 ** len(b))
        s = a
    return Q(10 ** (len(s) - len(s.rstrip('0'))))


def spring_optimum():
    a0, a1 = Decimal('1.570796327'), Decimal('0.7853981635')
    c, lam, K = Decimal('0.283'), Decimal('1.78571428571429e-3'), Decimal('6.95652173913044e-7')
    A = lam * c / (9 * K)
    x5 = A ** (Decimal(1) / 3)
    return Q((a0 + 9 * a1) * c ** 3 * x5)


def points():
    nums = json.load(open(NUMBERS))['audit']
    rows = {}
    for p in nums['pairs']:
        key = (p['d'], p['f_upper_exact'])
        cls = 'gross' if p['label'] == 'gross' else 'tol'
        rows.setdefault(key, [p['instance'], cls, set()])[2].add(p['solver'])
    for p in nums['rocket']:
        rows[(p['d'], p['f_upper'])] = [p['instance'], 'rocket', {p['solver']}]
    ir = [('eniplac', '-132117.', Q('-132117.08301998871378')),
          ('lop97icx', '4099.06', Q('4099.059953600000099')),
          ('spring', '0.84624567', spring_optimum()),
          ('stockcycle', '119949.', Q(71969213, 600))]
    for name, d, f in ir:
        rows[(d, f)] = [name, 'ir', set()]
    out = []
    for (d, f), (name, cls, solvers) in rows.items():
        dq, fq = Q(d), Q(f) if isinstance(f, Q) else Q(f)
        m = dq - fq
        assert m > 0, name
        out.append((name, cls, sorted(solvers), float(m / unit(d)), float(m / abs(dq))))
    return out


LABELS = {  # instance (or instance + solver) -> (text, dx points, dy points, ha)
    'glider100': ('glider100', -4, -9, 'right'),
    'topopt-cantilever_60x40_50': ('topopt', -5, 3, 'right'),
    'methanol50': ('methanol50', 5, 2, 'left'),
    'ghg_3veh': ('ghg_3veh', -5, 3, 'right'),
    'nuclear14': ('nuclear14', -5, -8, 'right'),
    'nd_netgen-2000-3-4-b-a-ns_7': ('nd_netgen', 5, -3, 'left'),
    'smallinvDAXr1b150-165': ('smallinvDAX (4)', 5, 3, 'left'),
    'watercontamination0303': ('watercont.', 5, -8, 'left'),
    'rocket400': ('rocket', 0, 8, 'center'),
    'spring': ('spring', -4, -8, 'right'),
    'eniplac': ('eniplac', -5, 0, 'right'),
    'stockcycle': ('stockcycle', -5, 0, 'right'),
    'lop97icx': ('lop97icx', 5, 0, 'left'),
}
LABEL_ONCE = {'sssd': ('sssd (4)', 5, -2, 'left')}

STYLE = {
    'gross': dict(marker='o', s=22, facecolor=INK, edgecolor=INK, label='class (i), $(d-\\varphi)/|d|>10^{-6}$'),
    'tol': dict(marker='s', s=20, facecolor=MID, edgecolor=INK, label='class (i), $(d-\\varphi)/|d|\\leq 10^{-6}$'),
    'rocket': dict(marker='D', s=18, facecolor='white', edgecolor=INK, label='rocket (outside the screen)'),
    'ir': dict(marker='^', s=24, facecolor='white', edgecolor=INK, label='class (i-r)'),
}


def main():
    pts = points()
    plt.rcParams.update({'font.size': 7, 'font.family': 'DejaVu Sans', 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'pdf.fonttype': 42})
    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-3, 1e13)
    ax.set_ylim(2e-10, 1e4)
    for x in (0.5, 1.0):
        ax.axvline(x, color=LIGHT, lw=0.8, zorder=0)
    for y in (1e-6, 1e-4):
        ax.axhline(y, color=LIGHT, lw=0.8, ls='--', zorder=0)
    ax.text(0.44, 5e3, 'half a unit (screen slack)', rotation=90, ha='right', va='top',
            color=MID, fontsize=6)
    ax.text(1.14, 5e3, 'one unit (Hypothesis H)', rotation=90, ha='left', va='top',
            color=MID, fontsize=6)
    ax.text(2e12, 1.25e-6, '$10^{-6}$', ha='right', va='bottom', color=MID, fontsize=6)
    ax.text(2e12, 1.25e-4, '$10^{-4}$', ha='right', va='bottom', color=MID, fontsize=6)
    done = set()
    for cls in ('ir', 'rocket', 'tol', 'gross'):
        sel = [p for p in pts if p[1] == cls]
        ax.scatter([p[3] for p in sel], [p[4] for p in sel], zorder=3, linewidths=0.7,
                   **STYLE[cls])
        for name, _, _, x, y in sel:
            if name.startswith('sssd'):
                if 'sssd' in done:
                    continue
                done.add('sssd')
                text, dx, dy, ha = LABEL_ONCE['sssd']
                x, y = max((p[3], p[4]) for p in sel if p[0].startswith('sssd'))
            elif name in LABELS and name not in done:
                done.add(name)
                text, dx, dy, ha = LABELS[name]
            else:
                continue
            ax.annotate(text, (x, y), xytext=(dx, dy), textcoords='offset points', ha=ha,
                        va='center', color=INK, fontsize=6)
    ax.set_xlabel('margin $d-\\varphi$ in units of the last displayed digit of $d$')
    ax.set_ylabel('relative margin $(d-\\varphi)/|d|$')
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.legend(loc='lower right', frameon=False, fontsize=6, handletextpad=0.3,
              borderaxespad=0.2)
    fig.tight_layout(pad=0.3)
    fig.savefig(OUT)
    for p in sorted(pts, key=lambda t: t[3]):
        print('%-28s %-7s %-22s units %.4g  rel %.4g' % (p[0], p[1], ','.join(p[2]), p[3], p[4]))
    print('wrote', OUT)


if __name__ == '__main__':
    main()
