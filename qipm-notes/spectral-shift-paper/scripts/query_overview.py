#!/usr/bin/env python3
"""Plot proved fixed-accuracy exponents; no fitted or conjectured thresholds.

The threshold solver is shared with the supplementary joint diagnostics.
PDF/CSV output is deterministic apart from library-specific PDF metadata.
"""
from pathlib import Path
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from joint_accuracy_diagnostics import threshold


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / 'figures'
    out.mkdir(exist_ok=True)
    rho = 2.0
    G = np.array([0.5] + [threshold(r, rho)[0] for r in range(1, 6)])
    assert np.isclose(G[1], (3 - np.sqrt(17 / 2)) / 4, rtol=1e-13)
    assert np.all(np.diff(G) < 0)
    witness_bound = np.sqrt(5 / 2) * 5 / 128 * (3 / 5)**4 / (1 - 3 / 5)
    assert witness_bound < 1 / 32 < 1 / 24 and G[1] < 1 / 32
    with (out / 'query-overview.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['r', 'G_r', 'positive_tier_exponent'])
        for r, g in enumerate(G):
            writer.writerow([r, g, 0 if r == 0 else 1 - 1 / (2 * r)])

    plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix',
                         'font.size': 12, 'axes.titlesize': 12,
                         'axes.labelsize': 12, 'pdf.fonttype': 42,
                         'ps.fonttype': 42, 'axes.spines.top': False,
                         'axes.spines.right': False})
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.6), layout='constrained',
                             gridspec_kw={'width_ratios': [1.2, 1]})
    blue, orange, green = '#245a81', '#b95c14', '#357448'
    ax = axes[0]
    breaks = -np.log10(G)
    bounds = [0, *breaks[:5], breaks[4] + 0.7]
    exponents = [0, .5, .75, 5/6, 7/8, .9]
    for j, y in enumerate(exponents):
        ax.plot(bounds[j:j+2], [y, y], color=blue, lw=2)
    for j, x in enumerate(breaks[:5]):
        ax.plot(x, exponents[j], 'o', color=blue, ms=5, zorder=4)
        ax.plot(x, exponents[j+1], 'o', markeredgecolor=blue,
                markerfacecolor='white', ms=5, zorder=4)
        ax.axvline(x, color='0.8', lw=.6, ls=':', zorder=0)
    ax.set_xticks(breaks[:5], [rf'$G_{{{j}}}$' for j in range(5)])
    ax.set_yticks([0, .5, .75, 5/6, 1], ['$0$', '$1/2$', '$3/4$', '$5/6$', '$1$'])
    ax.set(xlim=(0, bounds[-1]), ylim=(-.04, 1.04),
           xlabel=r'Thresholds on a $\log_{10}(1/K)$ scale',
           ylabel=r'Optimal power $\alpha$', title=r'(a) Unrestricted conversion, $\rho=2$')
    ax.text(2.2, .18, r'$K\ \mathrm{decreases}\ \longrightarrow$', color='0.3')

    ax = axes[1]
    lo, cutoff, hi = 1/32, 1/24, 1/12
    ax.plot([lo, hi], [.5, .5], color=blue, lw=2,
            label='Unrestricted')
    # A small visual offset would falsify the power; use distinct dashes instead.
    ax.plot([lo, cutoff], [5/6, 5/6], color=orange, lw=2, ls='--',
            label='Even QSVT')
    ax.plot([cutoff, hi], [.5, .5], color=orange, lw=2, ls='--')
    ax.plot(cutoff, .5, 'o', color=orange, ms=5, zorder=5)
    ax.plot(cutoff, 5/6, 'o', markeredgecolor=orange,
            markerfacecolor='white', ms=5, zorder=5)
    ax.plot([lo, hi], [1, 1], color=green, lw=1.7, ls=':', label='Odd QSVT')
    ax.text(.054, .95, r'also $\log(1/\delta)$', color=green, fontsize=10.5)
    ax.axvline(cutoff, color='0.8', lw=.6, ls=':', zorder=0)
    ax.set_xticks([lo, cutoff, hi], ['$1/32$', '$1/24$', '$1/12$'])
    ax.set_yticks([.5, .75, 5/6, 1], ['$1/2$', '$3/4$', '$5/6$', '$1$'])
    ax.set(xlim=(lo-.002, hi+.002), ylim=(.43, 1.07), xlabel=r'Relative error $K$',
           title=r'(b) Proved parity separation, $\rho=2$')
    ax.legend(loc='center right', frameon=False, fontsize=10.5)
    for ax in axes:
        ax.tick_params(direction='out', length=3)
    fig.savefig(out / 'query-overview.pdf', metadata={'Title': 'Optimal query powers for unit-normalized shifting', 'Author': ''})
    fig.savefig(out / 'query-overview.png', dpi=180)
    print(f'Wrote {out / "query-overview.pdf"}; G1={G[1]:.15g}; witness upper bound={witness_bound:.15g}')


if __name__ == '__main__':
    main()
