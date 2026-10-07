#!/usr/bin/env python3
"""Supplement S2 table: the exactly feasible point of each instance family (43 instances).

Usage (from anywhere outside the source trees):
    cd /tmp && python3 <repo>/paper-open-minlplib/data/make_points_table.py

Reads (read only):
  paper-open-minlplib/data/numbers.json      (written and checked by make_tables.py)
Writes exactly:
  paper-open-minlplib/tables/tab-points-all.tex

For each family the table gives the construction of Section 6.1, a short
description of the point and the arithmetic of its proofs (fixed text taken
from Supplement S2); the values U are those of the main-text Tables 2 to 4,
so the table has one row per family (round-1 revision, G7-18). The script
still checks with exact rational arithmetic that the primal display of each of
the 43 instances lies on the conservative side of its exact value (above it for
minimization, below it for the maximization instance pricing050), and that
every instance belongs to a row. It exits with status 1 if a check fails.
Standard library only.
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
NUMBERS = HERE / 'numbers.json'
OUT = P / 'tables' / 'tab-points-all.tex'
FAILS = []


def check(label, ok):
    print(('ok    ' if ok else 'FAIL  ') + label)
    if not ok:
        FAILS.append(label)


# Fixed descriptions (Appendix C). Columns: construction of Section 6.1 (named
# as in development/terminology.md), description of the point, arithmetic of
# the proofs (first; second), mpmath-free proof exists.
E2 = r'\arith{E}; \arith{E}'
DESC = {
    'lnts': ('existence proof', r'attaining point of \cref{thm:lnts-opt} (scalar root); a second point by a Krawczyk test (\cref{tab:points})',
             E2, 'yes'),
    'dtoc5': ('exact point', r'rational point: states rounded to 30 decimals, controls from the rows',
              r'\arith{E} (three readers)', 'yes'),
    'optcdeg2': ('existence proof', r'controls $\pm1/5$ with one switching control fixed and one bracketed (intermediate value theorem)',
                 r'\arith{E}; \arith{I}', 'yes'),
    'lukvle10': ('triangular', r'seeds with 640 decimals, forward recursion (\cref{rem:lukvle10-seeds})',
                 r'\arith{I}; \arith{E}', 'yes'),
    'chain': ('exact point', r'point in $\Q(\sqrt{R_N})$ (\cref{lem:pts-chain})', E2, 'yes'),
    'catmix': ('triangular', r'binary64 controls of a computed run, exact rational states', E2, 'yes'),
    'catmix800': ('triangular', r'binary64 controls of the dual certificate\textquoteright s policy, exact rational states', E2, 'yes'),
    'camshape': ('exact point', r'rational envelope point (\cref{lem:camshape-envelope})', E2, 'yes'),
    'ex62': ('exact point', r'rational point; linear rows exact; objective enclosed',
             r'rows \arith{E}, objective \arith{I}; \arith{E}', 'yes'),
    # pricing050: two separately written checks of the saved point (round-3 review sol-status 2):
    # development/dossiers/small-checks/pricing_check.py and small-checks/r2/pricing_check.py, written
    # in separate agent sessions; the later session did not read the earlier check before writing its own.
    'pricing050': ('interior point', r'rational interior point (17 digits)', r'\arith{I} (two codes)', 'no'),
    'etamac': ('triangular', r'17-digit decisions, forward definitions', r'\arith{I} (one code)', 'no'),
    'pindyck': ('existence proof', r'17-digit prices; states by recursion, one-dimensional interval test per supply row',
                r'\arith{I} (two codes)', 'no'),
    'pf': ('existence proof', r'Krawczyk test on an active-set square system near p1',
           r'\arith{I}; \arith{E}', 'yes'),
    'hvycrash': ('triangular', r'backward definitions from $\theta_{50}=3$ (\cref{prop:hvycrash-identity})',
                 r'written proof; \arith{I} (two codes for the first witness, a third for a second)', r'no\textsuperscript{b}'),
    'eg': ('interior point', r'decimal point, objective variable rounded up; strictly interior rows',
           r'\arith{E}; \arith{I}', 'yes'),
    'waterno2_06': ('exact point', r'MINLPLib\textquoteright s p4 made exact; rational or one quadratic field per row',
                    r'\arith{E} (three checkers)', 'yes'),
    'waterno2': ('exact point', r'algebraic point: rational or one quadratic field per row',
                 r'\arith{E} (three checkers)', 'yes'),
    'ann': ('triangular', r'rational inputs, forward definitions', r'\arith{I}; \arith{E}', 'yes'),
    'kan': ('triangular', r'point of $\RP$: binary64 inputs, forward definitions',
            r'\arith{I}; \arith{E}', 'yes'),
}


def key_of(n):
    if n.startswith('lnts'):
        return 'lnts'
    if n.startswith('chain'):
        return 'chain'
    if n == 'catmix800':
        return n
    if n.startswith('catmix'):
        return 'catmix'
    if n.startswith('camshape'):
        return 'camshape'
    if n.startswith('ex6_2'):
        return 'ex62'
    if n.startswith('powerflow'):
        return 'pf'
    if n.startswith('eg_'):
        return 'eg'
    if n == 'waterno2_06':
        return 'waterno2_06'
    if n.startswith('waterno2'):
        return 'waterno2'
    if n.startswith('ann'):
        return 'ann'
    if n.startswith('kan'):
        return 'kan'
    return n


def inst_tex(n):
    # macros.tex defines \inst as a URL-style command: underscores are passed
    # unescaped (an escaped \_ would print the backslash).
    return '\\inst{' + n + '}'


LABEL = {  # row label of each family key, in table order
    'lnts': r'\inst{lnts50}--\inst{lnts400}', 'dtoc5': r'\inst{dtoc5}', 'optcdeg2': r'\inst{optcdeg2}',
    'lukvle10': r'\inst{lukvle10}', 'chain': r'\inst{chain50}--\inst{chain400}',
    'catmix': r'\inst{catmix100}--\inst{catmix400}', 'catmix800': r'\inst{catmix800}',
    'camshape': r'\inst{camshape100}--\inst{camshape800}', 'ex62': r'\inst{ex6_2_5}, \inst{ex6_2_7}',
    'pricing050': r'\inst{pricing050}\textsuperscript{c}', 'etamac': r'\inst{etamac}', 'pindyck': r'\inst{pindyck}',
    'pf': r'the three \inst{powerflow} instances', 'hvycrash': r'\inst{hvycrash}', 'eg': r'the three \inst{eg} instances',
    'waterno2_06': r'\inst{waterno2_06}', 'waterno2': r'\inst{waterno2_09}--\inst{waterno2_24}',
    'ann': r'\inst{ann_cumene_tanh}', 'kan': r'the six KAN instances\textsuperscript{a}'}


def main():
    d = json.loads(NUMBERS.read_text())
    inst = d['instances']
    check('43 instances in numbers.json', len(inst) == 43)
    members = {}
    for n, r in inst.items():
        k = key_of(n)
        check(f'{n}: description exists', k in DESC and k in LABEL)
        if k not in DESC or k not in LABEL:
            continue
        members.setdefault(k, []).append(n)
        U = r['U']
        disp = U.get('table_display') or U['display']
        exact = Q(U['exact'])
        maximize = r['sense'] == 'max'
        ok = Q(disp) <= exact if maximize else Q(disp) >= exact
        check(f'{n}: U display {disp} on the conservative side of the exact value', ok)
    check('every instance in exactly one row', sum(len(v) for v in members.values()) == 43)
    rows = []
    for k, lab in LABEL.items():
        check(f'row {k} has members', k in members)
        cl, cons, arith, mpfree = DESC[k]
        rows.append(f'{lab} & {cl} & {cons} & {arith} & {mpfree} \\\\')
    check('19 family rows', len(rows) == 19)
    head = r"""% Generated by paper-open-minlplib/data/make_points_table.py from data/numbers.json.
% Do not edit by hand; rerun the script. Requires booktabs and array;
% \inst{} takes instance names with unescaped underscores (macros.tex).
\begin{table}[htbp]
\centering
\scriptsize
\setlength{\tabcolsep}{3pt}
\caption{The exactly feasible point of each instance family; the values $U$ are those of \cref{tab:closures,tab:unclosed,tab:kan}.
Construction (\cref{sec:points-constructions}): \emph{exact point}, explicit exact point; \emph{triangular}, triangular definitions; \emph{existence proof}, interval existence proof; \emph{interior point}, strictly interior point.
Arithmetic: tags of the first and of the separately written second proof (\arith{E} exact rational or algebraic, including integer and dyadic interval arithmetic; \arith{I} mpmath intervals).
No mpmath: a computer proof without mpmath exists.
\textsuperscript{a}Points of $\RP$; the stored models have no exactly feasible point (\cref{prop:kan-infeasible}).
\textsuperscript{b}The existence proof is a written proof (\cref{prop:hvycrash-identity}; evidence level \evid{hand}); the computer checks of the witnesses use mpmath.
\textsuperscript{c}Maximization: $U$ is the lower end, rounded down.}
\label{tab:points-all}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{3.0cm}>{\raggedright\arraybackslash}p{1.7cm}>{\raggedright\arraybackslash}p{5.2cm}>{\raggedright\arraybackslash}p{3.2cm}>{\raggedright\arraybackslash}p{1.4cm}@{}}
\toprule
instances & construction & point & arithmetic & no mpmath \\
\midrule
"""
    text = head + '\n'.join(rows) + '\n\\bottomrule\n\\end{tabular}\n\\end{table}\n'
    if FAILS:
        print(f'{len(FAILS)} check(s) failed; nothing written')
        sys.exit(1)
    OUT.write_text(text)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
