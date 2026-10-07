#!/usr/bin/env python3
"""Figure 2 (optcdeg2 calibration): control, velocity costate and curvature against time.

Reads the stored calibration arrays of the optcdeg2 certificate,
research-20260929/theory-bangbang/logs/optcdeg2_qcal_data.npz (binary64 arrays u, pv, q;
the paper reads them as exact rationals), and writes
paper-open-minlplib/figures/fig-optcdeg2-calibration.pdf.

This is a picture of stored data only; no certificate is computed here. The script checks
the facts that the caption and Section 4.3 state: fractional controls exactly at stages 3091
and 47290 and +-1/5 elsewhere; p^v > 0 on both u = -1/5 arcs; q = 0 exactly on stages
3091..47291 and nonzero elsewhere; q_0 = -34.10 and q_N = 0.286 to the printed digits.

Run from outside the source trees, for example
    cd /tmp && python3 <repo>/paper-open-minlplib/figures/make_fig_optcdeg2.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
NPZ = HERE.parents[1] / 'research-20260929/theory-bangbang/logs/optcdeg2_qcal_data.npz'
OUT = HERE / 'fig-optcdeg2-calibration.pdf'

H = 4e-4                      # step length h = 1/2500 (plot axis only)
S1, S2 = 3091, 47290          # switching stages

INK = '#1a1a1a'
MID = '#7a7a7a'
LIGHT = '#d9d9d9'


def check(u, pv, q):
    frac = np.where(np.abs(u) < 0.2)[0]
    assert list(frac) == [S1, S2], frac
    assert np.all(u[:S1] == -0.2) and np.all(u[S1 + 1:S2] == 0.2) and np.all(u[S2 + 1:] == -0.2)
    assert np.all(pv[1:S1 + 1] > 0) and np.all(pv[S2 + 2:] > 0)   # p^v_{t+1} > 0 on both u = -1/5 arcs
    assert np.all(q[S1:S2 + 2] == 0) and np.all(q[:S1] != 0) and np.all(q[S2 + 2:] != 0)
    assert round(q[0], 2) == -34.10 and round(q[-1], 3) == 0.286


def main():
    z = np.load(NPZ)
    u, pv, q = z['u'], z['pv'], z['q']
    check(u, pv, q)
    plt.rcParams.update({'font.size': 7, 'font.family': 'DejaVu Sans', 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(3, 1, figsize=(6.0, 4.2), sharex=True)
    tu = np.arange(len(u)) * H
    ts = np.arange(len(pv)) * H

    panels = [
        (u, tu, '(a) control $u_t$', 'linear'),
        (pv, ts, '(b) velocity costate $p^v_t$', 'symlog'),
        (q, ts, '(c) curvature $q_t$', 'symlog'),
    ]
    for ax, (y, t, label, scale) in zip(axes, panels):
        for s in (S1, S2):
            ax.axvline(s * H, color=MID, lw=0.6, ls=(0, (3, 2)), zorder=1)
        ax.axhline(0, color=LIGHT, lw=0.6, zorder=0.5)
        if label.startswith('(a)'):
            ax.step(t, y, where='post', color=INK, lw=1.0, zorder=2)
            ax.set_ylim(-0.26, 0.26)
            ax.set_yticks([-0.2, 0, 0.2])
            ax.set_yticklabels(['$-1/5$', '0', '$1/5$'])
        else:
            ax.plot(t, y, color=INK, lw=1.0, zorder=2)
            if label.startswith('(b)'):
                ax.set_yscale('symlog', linthresh=1.0, linscale=0.6)
                ax.set_yticks([-100, -10, -1, 0, 1, 10, 100])
                ax.set_yticklabels(['$-10^2$', '$-10$', '$-1$', '0', '1', '10', '$10^2$'])
                ax.set_ylim(-400, 400)
            else:
                ax.set_yscale('symlog', linthresh=0.1, linscale=0.6)
                ax.set_yticks([-10, -1, -0.1, 0, 0.1, 1])
                ax.set_yticklabels(['$-10$', '$-1$', '$-0.1$', '0', '0.1', '1'])
                ax.set_ylim(-60, 1.5)
                ax.annotate('$q_0=-34.10$', xy=(0, q[0]), xytext=(1.6, -30), fontsize=6.5, color=INK,
                            va='center', arrowprops=dict(arrowstyle='-', color=MID, lw=0.5))
                ax.annotate('$q_N=0.286$', xy=(len(q) * H - H, q[-1]), xytext=(17.3, 0.75), fontsize=6.5,
                            color=INK, va='center', ha='right',
                            arrowprops=dict(arrowstyle='-', color=MID, lw=0.5))
        ax.set_title(label, loc='left', fontsize=7, color=INK, pad=2)
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        ax.tick_params(axis='y', labelsize=6.5)
    axes[-1].set_xlim(0, 20)
    axes[-1].set_xlabel('time $th$')
    axes[0].text(S1 * H, -0.24, ' $t=3091$', fontsize=6, color=MID, va='bottom', ha='left')
    axes[0].text(S2 * H, -0.24, '$t=47290$ ', fontsize=6, color=MID, va='bottom', ha='right')
    fig.align_ylabels(axes)
    fig.tight_layout(h_pad=0.4)
    fig.savefig(OUT)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
