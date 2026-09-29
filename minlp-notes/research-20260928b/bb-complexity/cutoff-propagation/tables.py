"""Markdown tables for Section 9 of the note from logs/sweep*.jsonl.
Cell = nodes/relaxations (FBBT rounds).  Last columns: least-squares slope of
log10(nodes) against log10(1/eps) over the last four eps values, and the mean
increase of nodes per decade over the same range.
Run: python3 tables.py > logs/tables.md
"""
import json
import math
from collections import defaultdict


def load(paths):
    rows = []
    for p in paths:
        try:
            rows += [json.loads(l) for l in open(p)]
        except FileNotFoundError:
            pass
    return rows


def main():
    rows = load(['logs/sweep.jsonl', 'logs/sweep3.jsonl', 'logs/sweep_nd2.jsonl'])
    t = defaultdict(dict)
    for r in rows:
        t[(r['inst'], r['rep'], r['mode'])][r['eps']] = r
    order = ['nondeg1', 'nondeg1s', 'h1', 'nd2', 'iso2', 'iso3', 'rot1', 'rot0.1', 'rot0.01',
             'linediag', 'line3']
    for inst in order:
        keys = sorted(k for k in t if k[0] == inst)
        if not keys:
            continue
        eps_all = sorted({e for k in keys for e in t[k]}, reverse=True)
        print(f'\n**{inst}**\n')
        print('| rep | FBBT | ' + ' | '.join(f'{e:.0e}' for e in eps_all) + ' | slope | nodes/decade |')
        print('|---|---|' + '---|' * len(eps_all) + '---|---|')
        for k in keys:
            d = t[k]
            cells = []
            for e in eps_all:
                if e in d:
                    r = d[e]
                    ab = '*' if r.get('aborted') else ''
                    cells.append(f"{r['nodes']}{ab}/{r['relax']} ({r['rounds']})")
                else:
                    cells.append('')
            es = [e for e in eps_all if e in d and not d[e].get('aborted')][-4:]
            if len(es) >= 2:
                xs = [math.log10(1 / e) for e in es]
                ys = [math.log10(d[e]['nodes']) for e in es]
                mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
                sxx = sum((x - mx) ** 2 for x in xs)
                slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else float('nan')
                per_dec = (d[es[-1]]['nodes'] - d[es[0]]['nodes']) / (xs[-1] - xs[0])
                tail = f'{slope:.2f} | {per_dec:.0f}'
            else:
                tail = ' | '
            print(f'| {k[1]} | {k[2]} | ' + ' | '.join(cells) + f' | {tail} |')


if __name__ == '__main__':
    main()
