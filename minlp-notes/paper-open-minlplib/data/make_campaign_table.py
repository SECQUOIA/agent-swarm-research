#!/usr/bin/env python3
"""Appendix H table: outcome and final dual bound of every one-hour run.

Usage (from anywhere outside the source trees):
    cd /tmp && python3 <repo>/paper-open-minlplib/data/make_campaign_table.py

Reads (read only):
  paper-open-minlplib/data/numbers.json      (written and checked by make_tables.py)
  research-20260929/publication/solver-runs/results_table.csv
Writes exactly:
  paper-open-minlplib/tables/tab-campaign-runs.tex

For each instance and solver the cell gives an outcome code and the relative
distance s(U - D)/|U| of the final dual bound D to the certified primal value U
(the quantity of Figure 1), rounded down to two significant digits. For the KAN
models U is the value at a point of R_P. The script checks with exact rational
arithmetic that every finite final dual is weaker than the certified dual L, and
that its outcome counts equal the per-solver counts in numbers.json. It exits
with status 1 if a check fails. Standard library only; about one second.
"""
import csv
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
CSV = P.parent / 'research-20260929' / 'publication' / 'solver-runs' / 'results_table.csv'
OUT = P / 'tables' / 'tab-campaign-runs.tex'
SOLVERS = ('BARON', 'GUROBI', 'SCIP')
FAILS = []


def check(label, ok):
    print(('ok    ' if ok else 'FAIL  ') + label)
    if not ok:
        FAILS.append(label)


def q(s):
    return Q(str(s).strip().replace('−', '-'))


def down2(x):
    """Round a positive Fraction down to two significant digits; LaTeX math string."""
    assert x > 0
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Q(10) ** e > x:
        e -= 1
    while Q(10) ** (e + 1) <= x:
        e += 1
    m = math.floor(x / Q(10) ** (e - 1))          # two digits, 10..99
    assert 10 <= m <= 99 and Q(m) * Q(10) ** (e - 1) <= x
    mant = f'{m // 10}.{m % 10}'
    if -2 <= e <= 2:
        v = Q(m) * Q(10) ** (e - 1)
        k = max(0, 1 - e)
        return f'${float(v):.{k}f}$'
    return f'${mant}\\cdot10^{{{e}}}$'


def code(row):
    st = row['status']
    if st == 'capability failure':
        return 'C'
    if st == 'interface/model-expression failure':
        return 'E'
    if st == 'stopped at the 8 GB memory limit':
        return 'M'
    if st == 'optimality claim contradicted':
        return 'O'
    assert st.startswith('time limit'), st
    return 'T'


def main():
    num = json.loads((P / 'data' / 'numbers.json').read_text())
    inst = num['instances']
    order = [r['instance'] for r in num['headline_figure']]
    check('43 instances in Figure 1 order', len(order) == 43 and set(order) == set(inst))
    rows = list(csv.DictReader(CSV.read_text().splitlines()))
    check('129 rows in results_table.csv', len(rows) == 129)
    by = {(r['instance'], r['solver']): r for r in rows}
    check('one row per instance and solver', len(by) == 129 and all((n, s) in by for n in order for s in SOLVERS))

    counts = {s: dict(C=0, E=0, M=0, O=0, finite=0, nog=0, tight=0, batch=0) for s in SOLVERS}
    lines = []
    for n in order:
        r = inst[n]
        sg = 1 if r['sense'] == 'min' else -1
        L, U = q(r['L']['exact']), q(r['U']['exact'])
        cells = []
        for s in SOLVERS:
            x = by[(n, s)]
            c = code(x)
            if c in counts[s]:
                counts[s][c] += 1
            marks = []
            if x['globality_warning'] == 'True':
                marks.append('g')
                counts[s]['nog'] += 1
            if x['scip_argument_bounds_tightened'] == 'True':
                marks.append('t')
                counts[s]['tight'] += 1
            if x['loaded_first_batch'] == 'True':
                marks.append('b')
                counts[s]['batch'] += 1
            lab = c + (f'$^{{\\mathrm{{{",".join(marks)}}}}}$' if marks else '')
            d = x['dual'].strip()
            if d in ('', 'Infinity', '-Infinity'):
                val = '--' if c not in ('C', 'E') else ''
            else:
                D = q(d)
                counts[s]['finite'] += 1
                check(f'{n}/{s}: final dual {d} weaker than certified L', sg * (L - D) > 0)
                val = down2(sg * (U - D) / abs(U))
            cells.append((lab + ' ' + val).strip())
        name = '\\inst{' + n + '}'  # URL-based \\inst: no escaping
        lines.append(' & '.join([name] + cells) + ' \\\\')
    per = num['campaign']['per_solver']
    for s in SOLVERS:
        p, c = per[s], counts[s]
        check(f'{s}: counts agree with numbers.json',
              (c['C'], c['E'], c['M'], c['O'], c['finite'], c['nog'], c['tight'], c['batch'])
              == (p['capability_failures'], p['other_failures'], p['memory_stops'], p['raw_optimality_claims'],
                  p['finite_final_duals'], p['finite_without_globality_guarantee'],
                  p['tightened_argument_bounds'], p['overloaded_first_batch']))
    if FAILS:
        print(f'{len(FAILS)} check(s) failed; table not written')
        sys.exit(1)
    head = ('% Generated by paper-open-minlplib/data/make_campaign_table.py from data/numbers.json and\n'
            '% research-20260929/publication/solver-runs/results_table.csv. Do not edit by hand.\n')
    body = r'''\begin{table}[p]
\centering
\scriptsize
\caption{Outcome of every one-hour run (\cref{sec:solvers-campaign}).
Each cell gives the outcome and the relative distance $\sense(\Uprim-D)/|\Uprim|$ of the final dual bound $D$ to the certified primal value $\Uprim$ (the quantity of \cref{fig:results-headline}), rounded down to two significant digits; for the KAN instances $\Uprim$ is the value at a point of $\RP$ and the certified dual bounds $\Rnet$.
Outcomes: O optimality claim; T time limit; M memory stop (bound of the kept attempt); C capability failure; E interface failure.
Marks: g no globality guarantee (BARON's own warning); t SCIP tightened log or power argument bounds to $10^{-9}$; b overloaded first batch.
A dash means that no finite dual bound was returned. Every finite final dual bound is weaker than the certified dual bound $\Lcert$.}
\label{tab:campaign-runs}
\begin{tabular}{@{}llll@{}}
\toprule
instance & BARON & Gurobi & SCIP \\
\midrule
''' + '\n'.join(lines) + r'''
\bottomrule
\end{tabular}
\end{table}
'''
    OUT.write_text(head + body)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
