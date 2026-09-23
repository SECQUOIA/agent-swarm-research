"""Reproduce the convex-envelope contact example; illustrative, not a benchmark."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    out = Path(__file__).resolve().parent / 'figures'
    out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.7), layout='constrained')
    z = np.linspace(0, 1, 301)
    axes[0].plot(z, -z*z-z, color='#176b91', lw=2,
                 label=r'Original $\psi(z)=-z^2-z$')
    axes[0].plot(z, -2*z, color='#bf6b23', lw=2, ls='--',
                 label=r'Convex envelope $\psi^{**}(z)=-2z$')
    axes[0].scatter([0, 1], [0, -2], color='#176b91', s=35, zorder=4)
    axes[0].set(xlabel='Follower quantity z', ylabel='Cost before tariff',
                title='Equal values under linear tariffs')
    axes[0].legend(frameon=False, loc='upper right', fontsize=9)
    axes[1].plot([1, 2], [1, 1], color='#176b91', lw=2,
                 label='Actual global response')
    axes[1].plot([2, 3], [0, 0], color='#176b91', lw=2)
    axes[1].plot([2, 2], [0, 1], color='#bf6b23', lw=2, ls='--',
                 label='Added by convexification')
    axes[1].scatter([2, 2], [0, 1], color='#176b91', s=40, zorder=4)
    axes[1].axhline(.5, color='#555555', ls=':', lw=1.4,
                   label=r'Upper constraint $z=1/2$')
    axes[1].scatter([2], [.5], marker='x', color='#a3243b', s=70, zorder=4)
    axes[1].set(xlabel='Tariff x', ylabel='Follower quantity z',
                title='Different feasible follower choices', ylim=(-.08, 1.12))
    axes[1].legend(frameon=False, loc='upper right', fontsize=9,
                   bbox_to_anchor=(1.02, .82))
    for suffix in ('pdf', 'svg', 'png'):
        fig.savefig(out / f'convex_envelope_false_choices.{suffix}', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
