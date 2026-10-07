#!/usr/bin/env python3
"""Figure 1 (headline): relative distance of dual bounds to the certified primal value.

Usage (from anywhere outside the source trees):
    cd /tmp && python3 <repo>/paper-open-minlplib/figures/make_fig_headline.py

Reads (read only) paper-open-minlplib/data/numbers.json, written by data/make_tables.py,
which checks every plotted value in exact rational arithmetic: `headline_figure` (row
order and the distances below), `instances` (exact U, L, sense and relative-gap
displays) and `campaign.totals`. Writes exactly paper-open-minlplib/figures/fig-headline.pdf.

For a dual bound d the plotted quantity is s(U - d)/|U|, where U is the certified primal
value (upper end of the objective enclosure at an exactly feasible point; for the KAN
instances the objective at a point of R_P) and s = +1 (minimization) or -1 (pricing050).

Panel (a), in two columns: the 37 instances with exactly feasible points. Markers:
certified dual (filled square; an attained exact optimum is drawn in a separate column
left of an axis break); best listed dual (open circle); best one-hour dual with a
globality guarantee on the unmodified model (filled triangle); SCIP bound on a model
with tightened log/power argument bounds (open triangle); BARON value without a
globality guarantee (cross). An arrowhead at the right edge marks a missing finite
bound of that kind. Values below the axis cap 1e-20 are drawn in a
marked zone left of a second break and annotated with their relative-gap display.
Panel (b): the six KAN instances; the certified bound is a lower bound for the network
relaxation R, the listed and one-hour bounds are bounds for the stored models.

Checks (exit status 1 on failure): the row order; the counts of BARON values without a
guarantee and of SCIP bounds on tightened models agree with campaign.totals; no KAN row
has same-model values; only certified duals fall below the axis cap, and each annotation
bounds its plotted distance (exact). Grayscale only; identity is carried by marker shape.
"""
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = Path(__file__).resolve().parent
NUM = HERE.parent / 'data' / 'numbers.json'
OUT = HERE / 'fig-headline.pdf'

XCAP = 1e-20                       # axis cap; smaller certified distances go to the zone below
XLO, XOFF, XBRK = 10 ** -23.4, 10 ** -22.3, 10 ** -20.9
XMAX, XFLAG = 10 ** 12.7, 10 ** 11.8
NA, NB = 37, 6

INK = '#1a1a1a'
MID = '#6e6e6e'
LIGHT = '#d4d4d4'
BAND = '#efefef'
MS = 3.3
FAILS = []


def check(label, ok):
    if not ok:
        print('FAIL  ' + label)
        FAILS.append(label)


def load():
    num = json.loads(NUM.read_text())
    rows, inst, tot = num['headline_figure'], num['instances'], num['campaign']['totals']
    check('row order: 31 closures, 5 waterno2, ann_cumene_tanh, 6 KAN',
          len(rows) == NA + NB and all(inst[r['instance']]['status'] == 'closed' for r in rows[:31])
          and [r['family'] for r in rows[31:]] == ['waterno2'] * 5 + ['ann'] + ['kan'] * 6
          and [r['kan_descriptive'] for r in rows] == [False] * NA + [True] * NB)
    check('6 BARON values without a globality guarantee and 6 SCIP bounds on tightened models',
          sum(len(r['baron_disclaimed']) for r in rows) == tot['finite_without_globality_guarantee'] == 6
          and sum(len(r['scip_tightened']) for r in rows) == tot['tightened_argument_bounds'] == 6)
    check('KAN rows have only descriptive one-hour values',
          all(r['same_model'] is None and not r['baron_disclaimed'] and not r['scip_tightened']
              for r in rows[NA:]))
    out = []
    for r in rows:
        n = r['instance']
        rec = inst[n]
        kan = r['kan_descriptive']
        row = dict(instance=n, exact=r['certified_exact_optimum'], listed=r['listed'], certified=r['certified'],
                   guaranteed=r['solver'] if kan else r['same_model'],
                   tightened=r['scip_tightened'], no_guarantee=r['baron_disclaimed'],
                   gap=rec.get('gap_rel', {}).get('display'))
        for v in [row['listed'], row['guaranteed']] + row['tightened'] + row['no_guarantee']:
            check(f'{n}: only certified duals below the axis cap', v is None or v >= XCAP)
        if not row['exact'] and row['certified'] < XCAP:
            s = 1 if rec['sense'] == 'min' else -1
            U, L = Q(rec['U']['exact']), Q(rec['L']['exact'])
            check(f'{n}: annotation bounds the plotted distance',
                  row['gap'] is not None and s * (U - L) / abs(U) <= Q(row['gap']))
        out.append(row)
    return out


def sci_tex(s):
    m, e = s.split('e')
    return rf'$\leq{m}\cdot10^{{{int(e)}}}$'


def draw_panel(axe, ax, rows, labels, ticklabels=True):
    """One panel: the exact-optimum column axe and the log axis ax, one row per instance."""
    n = len(rows)
    ys = list(range(n))[::-1]          # first instance at the top
    dy = 0.3
    for a in (axe, ax):
        a.set_ylim(-0.6, n - 0.4)
        a.tick_params(axis='y', length=0)
        for side in ('top', 'right'):
            a.spines[side].set_visible(False)
    ax.spines['left'].set_visible(False)
    # group bands: every second group is shaded and labelled at the right edge
    start = 0
    for gi, (label, cnt) in enumerate(labels):
        top, bot = ys[start] + 0.5, ys[start + cnt - 1] - 0.5
        if gi % 2 == 1:
            for a in (axe, ax):
                a.axhspan(bot, top, color=BAND, zorder=0, lw=0)
        ax.text(1.01, (top + bot) / 2, label, transform=ax.get_yaxis_transform(), rotation=90,
                va='center', ha='left', fontsize=5.5, color=MID)
        start += cnt
    ax.axvspan(XLO, XBRK, color=BAND, zorder=0, lw=0)
    for x in (1e-20, 1e-15, 1e-10, 1e-5, 1, 1e5, 1e10):
        ax.axvline(x, color=LIGHT, lw=0.4, zorder=0.5)

    def tri(x, y, filled):
        ax.plot(x, y, marker='^', ms=MS + 0.4, mfc=INK if filled else 'white', mec=INK, mew=0.6, ls='', zorder=4)

    def flag(y):
        ax.plot(XFLAG, y, marker='>', ms=MS, mfc='white', mec=INK, mew=0.6, ls='', zorder=4)

    for y, r in zip(ys, rows):
        xs = [v for v in [r['listed'], r['guaranteed']] + r['tightened'] + r['no_guarantee'] if v is not None]
        right = XFLAG if r['listed'] is None or r['guaranteed'] is None else max(xs)
        left = XLO if r['exact'] else XOFF if r['certified'] < XCAP else r['certified']
        ax.plot([left, right], [y, y], color=LIGHT, lw=0.6, zorder=1, solid_capstyle='butt')
        # certified dual (middle lane)
        if r['exact']:
            axe.plot(0.5, y, marker='s', ms=MS, mfc=INK, mec=INK, ls='', zorder=4)
        elif r['certified'] < XCAP:
            ax.plot(XOFF, y, marker='s', ms=MS, mfc=INK, mec=INK, ls='', zorder=4)
            ax.text(10 ** -20.4, y, sci_tex(r['gap']), va='center', ha='left', fontsize=5, color=INK)
        else:
            ax.plot(r['certified'], y, marker='s', ms=MS, mfc=INK, mec=INK, ls='', zorder=4)
        # one-hour values without a same-model guarantee (middle lane)
        for v in r['tightened']:
            tri(v, y, False)
        for v in r['no_guarantee']:
            ax.plot(v, y, marker='x', ms=MS, mec=INK, mew=0.7, ls='', zorder=4)
        # best one-hour dual with a globality guarantee (upper lane)
        if r['guaranteed'] is not None:
            tri(r['guaranteed'], y + dy, True)
        else:
            flag(y + dy)
        # best listed dual (lower lane)
        if r['listed'] is not None:
            ax.plot(r['listed'], y - dy, marker='o', ms=MS, mfc='white', mec=INK, mew=0.6, ls='', zorder=3)
        else:
            flag(y - dy)

    ax.set_xscale('log')
    ax.set_xlim(XLO, XMAX)
    ax.set_xticks([1e-20, 1e-10, 1, 1e10])
    ax.set_xticklabels(['$10^{-20}$', '$10^{-10}$', '$1$', '$10^{10}$'] if ticklabels else [])
    ax.minorticks_off()
    ax.set_yticks([])
    axe.set_xlim(0, 1)
    axe.set_xticks([0.5])
    axe.set_xticklabels(['exact\noptimum' if ticklabels else ''], fontsize=5.5)
    axe.set_yticks(ys)
    axe.set_yticklabels([r['instance'] for r in rows], fontsize=5.3, family='DejaVu Sans Mono')
    # axis breaks (two short slanted strokes on the bottom spine): left of the log axis,
    # after the exact-optimum column, and at the cap, after the zone of smaller values
    span = math.log10(XMAX) - math.log10(XLO)
    for xf in (0.0, (math.log10(XBRK) - math.log10(XLO)) / span):
        for off in (-0.008, 0.008):
            ax.plot([xf + off - 0.008, xf + off + 0.008], [-0.5 / n, 0.5 / n], transform=ax.transAxes,
                    color=INK, lw=0.6, clip_on=False, zorder=5)


def main():
    rows = load()
    if FAILS:
        sys.exit(f'{len(FAILS)} check(s) failed; figure not written')
    print('ok    all figure checks passed')
    plt.rcParams.update({'font.size': 6.5, 'font.family': 'DejaVu Sans', 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'xtick.major.size': 2.5, 'xtick.labelsize': 6,
                         'pdf.fonttype': 42})
    W, H, PITCH = 6.3, 3.85, 0.105      # inches; PITCH is the height of one instance row
    fig = plt.figure(figsize=(W, H))

    def axes(x, top, w, nrows):        # x, top and w in inches from the left and top edges
        return fig.add_axes([x / W, (H - top - nrows * PITCH) / H, w / W, nrows * PITCH / H])

    LAB, EX, GAP, MAIN = 0.75, 0.26, 0.03, 1.9       # label column, exact column, gap, log axis
    col = [0.02, 0.02 + LAB + EX + GAP + MAIN + 0.22]
    top_a = 0.2
    left_rows, right_rows = rows[:19], rows[19:NA]   # lnts50..camshape800 | ex6_2_5..ann
    pairs = []
    for x0, part in zip(col, (left_rows, right_rows)):
        pairs.append((axes(x0 + LAB, top_a, EX, len(part)), axes(x0 + LAB + EX + GAP, top_a, MAIN, len(part))))
    draw_panel(*pairs[0], left_rows, [])
    draw_panel(*pairs[1], right_rows, [('closures', 12), ('not closed', 6)])
    fig.text(col[0] / W, 1 - 0.04 / H,
             '(a) Instances with exactly feasible points',
             ha='left', va='top', fontsize=6.8)
    top_b = top_a + 19 * PITCH + 0.65
    bx = (axes(col[0] + LAB, top_b, EX, NB), axes(col[0] + LAB + EX + GAP, top_b, MAIN, NB))
    draw_panel(*bx, rows[NA:], [])
    bx[0].set_xticklabels([''])
    bx[0].tick_params(axis='x', length=0)
    fig.text(col[0] / W, 1 - (top_b - 0.04) / H,
             r'(b) KAN instances. Different models: certified lower bound for $\mathcal{R}$;' '\n'
             'listed and one-hour bounds for the stored models (descriptive)', ha='left', va='bottom', fontsize=6.8)
    bx[1].set_xlabel(r'relative distance $s\,(U-d)/|U|$ to the certified primal value', fontsize=6)
    handles = [
        Line2D([], [], marker='s', ls='', ms=MS, mfc=INK, mec=INK, label='certified dual bound'),
        Line2D([], [], marker='o', ls='', ms=MS, mfc='white', mec=INK, mew=0.6, label='best listed dual'),
        Line2D([], [], marker='^', ls='', ms=MS + 0.4, mfc=INK, mec=INK, mew=0.6,
               label='best one-hour dual, globality guarantee,\nunmodified model'),
        Line2D([], [], marker='^', ls='', ms=MS + 0.4, mfc='white', mec=INK, mew=0.6,
               label='SCIP, tightened log/power argument bounds'),
        Line2D([], [], marker='x', ls='', ms=MS, mec=INK, mew=0.7, label='BARON, no globality guarantee'),
        Line2D([], [], marker='>', ls='', ms=MS, mfc='white', mec=INK, mew=0.6, label='no finite bound'),
    ]
    fig.legend(handles=handles, loc='upper left', bbox_to_anchor=((col[1] + LAB) / W, 1 - (top_b - 0.3) / H),
               ncol=1, frameon=False, fontsize=6, handletextpad=0.4, labelspacing=0.45, borderaxespad=0)
    fig.savefig(OUT)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
