#!/usr/bin/env python3
"""Figure 4 (eg enclosures): why the eg certificates keep the signed Taylor moments.

Panel (a): median gap between the sampled minimum of a row over a box and three lower
bounds (natural interval extension, i.e. summed term ranges; the earlier attempt's natural
extension intersected with a mean-value form; the second-order Taylor model with signed
moments), against the relative box width, over 64 boxes x 24 rows of eg_int_s. Data:
research-20260929/open-instances-wave3/eg/retry/logs/cmp_bounds.log. This is numerical
evidence, not part of any proof.

Panel (b): cancellation at the eg_int_s point. For the active objective row e12 and the
active side row e26, the sum of the absolute values of the 97 kernel terms against the
absolute value of their sum. Data: research-20260929/reviews/eg-retry-review-checks/logs/
check_structure.log (line "e12: sum|w| ... ; e26: sum|w| ...").

Writes paper-open-minlplib/figures/fig-eg-enclosures.pdf. Grayscale; identity by marker.
Run from outside the source trees, for example
    cd /tmp && python3 <repo>/paper-open-minlplib/figures/make_fig_eg.py
"""
import re
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
R = HERE.parents[1] / 'research-20260929'
CMP = R / 'open-instances-wave3/eg/retry/logs/cmp_bounds.log'
STRUCT = R / 'reviews/eg-retry-review-checks/logs/check_structure.log'
OUT = HERE / 'fig-eg-enclosures.pdf'

INK = '#1a1a1a'
MID = '#7a7a7a'
LIGHT = '#d9d9d9'


def read_cmp():
    rows = []
    for line in CMP.read_text().splitlines()[1:]:
        if line.strip():
            rho, w3, nat, tm = (float(t) for t in line.split())
            rows.append((rho, w3, nat, tm))
    assert len(rows) == 5
    return rows


def read_cancel():
    txt = STRUCT.read_text()
    m = re.search(r'e12: sum\|w\| ([0-9.]+)\s+g (-?[0-9.]+) ; e26: sum\|w\| ([0-9.]+)\s+gauss part (-?[0-9.]+)',
                  txt)
    assert m, 'cancellation line not found'
    s12, g12, s26, g26 = (float(m.group(i)) for i in range(1, 5))
    return [('e26 (side row)', s26, abs(g26)), ('e12 (objective row)', s12, abs(g12))]


def main():
    rows = read_cmp()
    canc = read_cancel()
    plt.rcParams.update({'font.size': 7, 'font.family': 'DejaVu Sans', 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'pdf.fonttype': 42})
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.6, 2.3), gridspec_kw={'width_ratios': [1.25, 1]})

    rho = [r[0] for r in rows]
    series = [('summed term ranges', [r[2] for r in rows], 'o', 'white', MID, (0, (1, 1.2))),
              ('earlier attempt\n(ranges $\\cap$ mean-value form)', [r[1] for r in rows], 's', 'white', INK,
               (0, (4, 2))),
              ('Taylor model with\nsigned moments', [r[3] for r in rows], 'D', INK, INK, '-')]
    for label, ys, mk, mfc, col, ls in series:
        ax.plot(rho, ys, color=col, lw=1.0, ls=ls, marker=mk, ms=4, mfc=mfc, mec=col, mew=0.8, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.invert_xaxis()
    ax.set_xlabel('relative box width $\\rho$')
    ax.set_ylabel('median gap')
    ax.set_title('(a) enclosure quality on eg_int_s', fontsize=7.5, pad=3)
    ax.legend(loc='lower left', fontsize=6, frameon=False, handlelength=3.0, labelspacing=0.5)
    ax.set_xlim(0.45, 0.0006)
    ax.set_ylim(1e-7, 30)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

    ys = list(range(len(canc)))
    for y, (label, s, g) in zip(ys, canc):
        bx.plot([g, s], [y, y], color=LIGHT, lw=2.0, solid_capstyle='butt', zorder=1)
        bx.plot(s, y, marker='o', ms=5, mfc=INK, mec=INK, ls='', zorder=3)
        bx.plot(g, y, marker='o', ms=5, mfc='white', mec=INK, mew=0.8, ls='', zorder=3)
        bx.text((g * s) ** 0.5, y + 0.12, f'factor {s / g:.0f}' if s / g > 20 else f'factor {s / g:.1f}',
                fontsize=6, color=MID, ha='center', va='bottom')
    bx.set_yticks(ys)
    bx.set_yticklabels([c[0] for c in canc])
    bx.set_ylim(-0.6, len(canc) - 0.4)
    bx.set_xscale('log')
    bx.set_xlim(0.02, 1000)
    bx.set_xlabel('magnitude')
    bx.set_title('(b) cancellation at the optimum', fontsize=7.5, pad=3)
    bx.plot([], [], marker='o', ms=5, mfc=INK, mec=INK, ls='', label='$\\sum_m |a_m e^{E_m}|$')
    bx.plot([], [], marker='o', ms=5, mfc='white', mec=INK, mew=0.8, ls='', label='$|\\sum_m a_m e^{E_m}|$')
    bx.legend(loc='upper left', fontsize=6, frameon=False, handletextpad=0.3)
    for side in ('top', 'right'):
        bx.spines[side].set_visible(False)
    fig.tight_layout(w_pad=1.2)
    fig.savefig(OUT)
    print('wrote', OUT, rows, canc)


if __name__ == '__main__':
    main()
