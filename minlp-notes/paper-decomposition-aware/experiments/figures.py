"""Grayscale-safe figures from the saved CSV files (one PDF per experiment).

Identity is carried by marker shape and line style, not by color, so every
figure remains readable in grayscale print.
"""
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import median

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8, 'axes.labelsize': 8,
                     'legend.fontsize': 7, 'xtick.labelsize': 7, 'ytick.labelsize': 7,
                     'lines.linewidth': 1.2, 'lines.markersize': 4, 'axes.linewidth': 0.6,
                     'pdf.fonttype': 42, 'font.family': 'serif'})

STYLE = {
    'geometric_pruned': dict(color='0.0', ls='-', marker='o', label='graded, filtered'),
    'uniform_pruned': dict(color='0.35', ls='--', marker='s', label='uniform, filtered'),
    'geometric_unpruned': dict(color='0.55', ls='-.', marker='^', label='graded, no filtering'),
    'uniform_unpruned': dict(color='0.7', ls=':', marker='D', label='uniform, no filtering'),
    'geom_theorem': dict(color='0.0', ls='-', marker='o', label=r'graded, $\theta$ from theorem'),
    'geom_quarter': dict(color='0.45', ls='-.', marker='^', label=r'graded, $\theta=1/4$'),
    'unif': dict(color='0.3', ls='--', marker='s', label='uniform'),
}
TABLE_CAP_E1 = 100000


def read(path):
    with open(path) as fh:
        return list(csv.DictReader(fh))


def grid(ax):
    ax.grid(True, which='major', color='0.88', lw=0.5)
    ax.set_axisbelow(True)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)


def fig_e1(res, out):
    rows = read(res / 'E1_stages.csv')
    panels = [('path', 16, 'path, $n=16$, $p=2$'), ('tree', 16, 'random tree, $n=16$, $p=2$'),
              ('band2', 12, 'band, $n=12$, $p=3$'), ('band3', 8, 'band, $n=8$, $p=4$')]
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.5), sharey=True)
    for ax, (kind, n, title) in zip(axes, panels):
        for method in ('geometric_pruned', 'uniform_pruned', 'geometric_unpruned', 'uniform_unpruned'):
            data = defaultdict(list)
            for r in rows:
                if r['kind'] == kind and int(r['n']) == n and r['method'] == method:
                    data[int(r['stage'])].append(int(r['table_states']))
            # Plot a stage only when every seed completed it (no survivorship bias).
            nseeds = max((len(v) for v in data.values()), default=0)
            xs = sorted(j for j, v in data.items() if len(v) == nseeds)
            if xs:
                ax.plot(xs, [median(data[j]) for j in xs], **STYLE[method])
        ax.axhline(TABLE_CAP_E1, color='0.6', ls=':', lw=1.0, label='table cap')
        ax.set_yscale('log')
        ax.set_title(title)
        ax.set_xlabel('stage $j$ (mesh $h_j=2^{1-j}$)')
        grid(ax)
    axes[0].set_ylabel('table entries in stage $j$')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, loc='lower center', ncol=5)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(out / 'E1_states_vs_stage.pdf')
    plt.close(fig)


def plateau(rows, key, last=4):
    """Median over the last `last` completed stages of one run."""
    byrun = defaultdict(list)
    for r in rows:
        byrun[r['key']].append((int(r['stage']), float(r[key])))
    out = {}
    for k, v in byrun.items():
        v.sort()
        out[k] = median(x for _, x in v[-last:])
    return out


def fig_e2(res, out):
    rows = read(res / 'E2_stages.csv')
    runs = {r['key']: r for r in read(res / 'E2_runs.csv')}
    nodes = plateau(rows, 'max_nodes_free')
    rad = plateau(rows, 'radius_over_h_free')
    last = {}
    for r in rows:
        if r['key'] not in last or int(r['stage']) > int(last[r['key']]['stage']):
            last[r['key']] = r
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.4))
    kap = defaultdict(list)
    for r in runs.values():
        kap[int(r['kappa_target'])].append(float(r['kappa_lb']))
    xs_all = sorted(kap)
    for method in ('geom_theorem', 'unif', 'geom_quarter'):
        pts, rpts, gpts = defaultdict(list), defaultdict(list), defaultdict(list)
        for key, r in runs.items():
            if r['method'] == method and key in nodes:
                k = int(r['kappa_target'])
                pts[k].append(nodes[key])
                rpts[k].append(rad[key])
                st = last[key]
                h = float(st['h'])
                gpts[k].append(float(st['gap_U_minus_beta']) / (2 * int(r['n']) * h * h))
        xs = sorted(pts)
        axes[0].plot(xs, [median(pts[x]) for x in xs], **STYLE[method])
        axes[1].plot(xs, [median(rpts[x]) for x in xs], **STYLE[method])
        axes[2].plot(xs, [median(gpts[x]) for x in xs], **STYLE[method])
    # Both reference lines use kappa_lb (median over seeds), the lower end of the
    # certified kappa interval; the bound line is therefore the smallest bound
    # compatible with the certificate.
    axes[1].plot(xs_all, [4.2 * math.sqrt(16 * median(kap[x])) for x in xs_all], color='0.6', ls=':',
                 label=r'bound $4.2\sqrt{n\kappa}$')
    axes[1].plot(xs_all, [math.sqrt(16 * median(kap[x]) / 8) for x in xs_all], color='0.6',
                 ls=(0, (5, 2)), label=r'$\sqrt{n\kappa/8}$')
    axes[2].axhline(9 / 16, color='0.6', ls=':', lw=1.0, label='bound $9/16$')
    from matplotlib.ticker import FixedLocator, NullLocator, ScalarFormatter
    for ax in axes:
        ax.set_xscale('log', base=2)
        ax.set_yscale('log', base=2)
        ax.set_xlabel(r'target $\kappa$ (path, $n=16$)')
        grid(ax)
    for ax, ticks in ((axes[0], [8, 16, 32, 64]), (axes[1], [2, 4, 8, 16, 32, 64, 128, 256])):
        ax.yaxis.set_major_locator(FixedLocator(ticks))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.yaxis.set_major_formatter(ScalarFormatter())
    axes[0].set_ylim(7, 72)
    axes[0].set_ylabel('nodes per coordinate (plateau)')
    axes[1].set_ylabel('retained radius$/h_j$ (plateau)')
    axes[2].set_ylabel(r'$(U-\beta)/(Lnh_j^2)$ at last stage')
    axes[0].legend(frameon=False, loc='upper left')
    h1 = [l for l in axes[1].get_lines() if l.get_label().startswith(('bound', '$'))]
    axes[1].legend(h1, [l.get_label() for l in h1], frameon=False, loc='upper left')
    axes[2].legend([axes[2].get_lines()[-1]], ['bound $9/16$'], frameon=False, loc='upper left')
    fig.tight_layout()
    fig.savefig(out / 'E2_plateau_vs_kappa.pdf')
    plt.close(fig)


def fig_e3(res, out):
    rows = read(res / 'E3_stages.csv')
    runs = {r['key']: r for r in read(res / 'E3_runs.csv') if int(r['kappa_target']) == 4}
    sep = {r['key']: r for r in read(res / 'E3_runs.csv')
           if int(r['kappa_target']) == 2 and r['method'] == 'unif'}
    nodes = plateau(rows, 'max_nodes_free')
    rad = plateau(rows, 'radius_over_h_free')
    fig, axes = plt.subplots(1, 2, figsize=(5.6, 2.4))
    pts = defaultdict(list)
    for key, r in sep.items():
        if key in nodes:
            pts[int(r['n'])].append(nodes[key])
    xs = sorted(pts)
    axes[0].plot(xs, [median(pts[x]) for x in xs], color='0.75', ls='--', marker='s', mfc='none',
                 label=r'uniform, $\kappa\approx2$ (separable)')
    for method in ('geom_theorem', 'unif', 'geom_quarter'):
        pts, rpts = defaultdict(list), defaultdict(list)
        for key, r in runs.items():
            if r['method'] == method and key in nodes:
                pts[int(r['n'])].append(nodes[key])
                rpts[int(r['n'])].append(rad[key])
        xs = sorted(pts)
        axes[0].plot(xs, [median(pts[x]) for x in xs], **STYLE[method])
        axes[1].plot(xs, [median(rpts[x]) for x in xs], **STYLE[method])
    for ax in axes:
        ax.set_xscale('log', base=2)
        ax.set_xlabel(r'path length $n$ ($\kappa\in[4.0,4.45]$)')
        grid(ax)
    axes[0].set_ylabel('nodes per free coordinate (plateau)')
    axes[1].set_ylabel('retained radius$/h_j$ (plateau)')
    axes[0].legend(frameon=False, loc='upper left', fontsize=6)
    fig.tight_layout()
    fig.savefig(out / 'E3_plateau_vs_n.pdf')
    plt.close(fig)


def fig_e4(res, out):
    rows = read(res / 'E4_exact.csv')
    fams = [('random', 'o', 'random, unplanted'), ('tied', 's', 'two isolated optima'),
            ('planted', '^', 'planted, unique'), ('flat', 'x', 'optimal segment (not reached)')]
    fig, ax = plt.subplots(figsize=(3.8, 2.6))
    xmax = max(float(r['required_gap_bits']) for r in rows)
    xs = [0, xmax * 1.05]
    ax.plot(xs, xs, color='0.75', lw=0.8, ls='-', label='stages = bits')
    ax.plot(xs, [2 * x for x in xs], color='0.75', lw=0.8, ls='--', label='stages = 2 bits')
    for fam, mk, lab in fams:
        sel = [r for r in rows if r['family'] == fam]
        if not sel:
            continue
        kw = dict(marker=mk, s=22, lw=0.8, label=lab)
        if mk == 'x':
            kw.update(color='0.0')
        else:
            kw.update(facecolor='none', edgecolor='0.0')
        ax.scatter([float(r['required_gap_bits']) for r in sel], [int(r['stages']) for r in sel], **kw)
    ax.set_xlabel(r'required gap bits $\log_2(\Omega W)$, row-sum constant')
    ax.set_ylabel('grid stages to exact output')
    grid(ax)
    ax.legend(frameon=False, loc='upper left')
    fig.tight_layout()
    fig.savefig(out / 'E4_exact_output.pdf')
    plt.close(fig)


def fig_e5(res, out):
    scip = read(res / 'E5_scip.csv')
    grid_runs = read(res / 'E5_grid_runs.csv')
    order = [('path', 16), ('tree', 16), ('band2', 12), ('band3', 8), ('path', 32), ('path', 64), ('path', 128)]
    groups = [g for g in order if any((r['kind'], int(r['n'])) == g for r in scip)]
    fig, ax = plt.subplots(figsize=(5.8, 2.6))
    def pick(rows, g, field, cond=lambda r: True):
        return [float(r[field]) for r in rows if (r['kind'], int(r['n'])) == g and cond(r)]
    series = [
        ('SCIP, reported abs. gap $\\leq10^{-6}$', 'o', dict(facecolor='none', edgecolor='0.0'), -1,
         lambda g: pick(scip, g, 'wall_s', lambda r: r['status'] != 'timelimit')),
        ('SCIP, 20 s limit, gap open', 'o', dict(color='0.0'), -1,
         lambda g: pick(scip, g, 'wall_s', lambda r: r['status'] == 'timelimit')),
        ('CT: solve', 's', dict(facecolor='none', edgecolor='0.35'), 0,
         lambda g: pick(grid_runs, g, 'solve_wall_s')),
        ('CT: replay', '^', dict(facecolor='none', edgecolor='0.55'), 1,
         lambda g: pick(grid_runs, g, 'verify_wall_s'))]
    for lab, mk, kw, off, get in series:
        first = True
        for gi, g in enumerate(groups):
            ys = get(g)
            if ys:
                ax.scatter([gi + off * 0.22] * len(ys), ys, marker=mk, s=20, lw=0.8,
                           label=lab if first else None, **kw)
                first = False
    names = {'path': 'path', 'tree': 'tree', 'band2': 'band', 'band3': 'band'}
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([f"{names[k]}\n$n={n}$" for k, n in groups])
    ax.set_yscale('log')
    ax.set_ylabel('wall time (s)')
    grid(ax)
    ax.legend(frameon=False, loc='upper left', ncol=2)
    fig.tight_layout()
    fig.savefig(out / 'E5_scip_comparison.pdf')
    plt.close(fig)


def fig_s1(res, out):
    rows = read(res / 'S1_localized.csv')
    fig, ax = plt.subplots(figsize=(3.8, 2.6))
    marks = {'path': 'o', 'tree': 's', 'band2': '^'}
    for kind, mk in marks.items():
        sel = [r for r in rows if r['kind'] == kind and r['local_first_stage'] not in ('', 'None')]
        ax.scatter([int(r['height_rule_stages']) for r in sel], [int(r['local_first_stage']) + 1 for r in sel],
                   marker=mk, facecolor='none', edgecolor='0.0', s=22, lw=0.8,
                   label={'path': 'path', 'tree': 'tree', 'band2': 'band'}[kind])
    miss = [r for r in rows if r['local_first_stage'] in ('', 'None')]
    if miss:
        ax.scatter([int(r['height_rule_stages']) for r in miss], [70] * len(miss), marker='x',
                   color='0.0', s=22, lw=0.8, label='not accepted in 60 stages')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('stages used by the height rule')
    ax.set_ylabel('stages to localized acceptance')
    grid(ax)
    ax.legend(frameon=False, loc='upper left')
    fig.tight_layout()
    fig.savefig(out / 'S1_localized_acceptance.pdf')
    plt.close(fig)


def make_all(res: Path, out: Path):
    out.mkdir(exist_ok=True)
    for name, fn in (('E1_stages.csv', fig_e1), ('E2_stages.csv', fig_e2), ('E3_stages.csv', fig_e3),
                     ('E4_exact.csv', fig_e4), ('E5_scip.csv', fig_e5),
                     ('S1_localized.csv', fig_s1)):
        if (res / name).exists():
            try:
                fn(res, out)
            except Exception as exc:  # a figure failure must not hide the data
                print(f'figure from {name} failed: {exc!r}')
