"""Check the CAMINO-benchmark Gurobi 13.0.0 results on eg_disc2_s, eg_disc_s, eg_int_s
against points of the MINLPLib AMPL .mod files that CAMINO's SCIP/Gurobi runs read.

For each instance:
  1. parse every row of sources/eg/minlplib_mod/<name>.mod (AMPL text written by GAMS Convert);
  2. evaluate every row, the variable bounds and integrality at the project's recorded point
     (open-instances-wave3/eg/retry/sol/<name>.retry.sol) in outward-rounded interval
     arithmetic (mpmath iv, 200-bit precision); the point's coordinates and every constant of
     the .mod are taken as the exact decimals written in the files;
  3. if every row holds on the whole enclosure, the point is a feasible point of the .mod model
     and its objective x8 is an upper bound on the .mod optimum; compare it with the
     Gurobi objective/bestbound and the SCIP bestbound from the CAMINO csv files.

Assumptions: mpmath's iv arithmetic (including iv.exp) is outward-rounded; this parser reads the
.mod rows correctly (row and variable counts are checked against the file header: 28 rows,
8 variables).
Usage: python3 checks/eg_camino_gurobi.py
"""
import csv
import re
from pathlib import Path

from mpmath import iv

iv.prec = 200
HERE = Path(__file__).resolve().parent.parent
MOD = HERE / 'sources/eg/minlplib_mod'
CAM = HERE / 'sources/eg/camino_benchmark'
SOL = HERE.parents[2] / 'open-instances-wave3/eg/retry/sol'
NUM = re.compile(r'(?<![\w.])(\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)')


def parse_mod(path):
    """Return (variables, rows): variables = [(name, is_integer, lb, ub)], rows = [(name, code, sense, rhs)]."""
    text = path.read_text()
    var_lines = re.findall(r'^var (\w+)( integer)?(?: := [^,;]+)?(?:, >= ([-\d.eE+]+))?(?:, <= ([-\d.eE+]+))?;',
                           text, re.M)
    variables = [(n, bool(integer), lb or None, ub or None) for n, integer, lb, ub in var_lines]
    body = text.split('subject to', 1)[1]
    rows = []
    for name, expr in re.findall(r'^(e\d+):(.*?);', body, re.S | re.M):
        expr = ' '.join(expr.split())
        m = re.fullmatch(r'(.*)\s(>=|<=|=)\s(-?[\d.eE+-]+)', expr)
        lhs, sense, rhs = m.groups()
        lhs = NUM.sub(lambda k: f"C('{k.group(1)}')", lhs.replace('^', '**'))
        rows.append((name, compile(lhs, name, 'eval'), sense, rhs))
    assert len(rows) == 28 and len(variables) == 8, (len(rows), len(variables))
    return variables, rows


def evaluate(variables, rows, point):
    """point: {variable name: decimal string}. Returns (in_bounds_and_integral, [(row, slack enclosure)])."""
    env = {'exp': iv.exp, 'C': iv.mpf}
    ok = True
    for vname, integer, lb, ub in variables:
        s = point[vname]
        val = iv.mpf(s)
        env[vname] = val
        if integer and float(s) != int(float(s)):
            ok = False
        if lb is not None and not val.a >= iv.mpf(lb).b:
            ok = False
        if ub is not None and not val.b <= iv.mpf(ub).a:
            ok = False
    slacks = []
    for rname, code, sense, rhs in rows:
        lhs = eval(code, env)
        if sense == '>=':
            slacks.append((rname, lhs - iv.mpf(rhs)))
        elif sense == '<=':
            slacks.append((rname, iv.mpf(rhs) - lhs))
        else:
            raise ValueError('equality row')
    return ok, slacks


def read_sol(path):
    vals = {}
    for line in path.read_text().split('\n'):
        if line.strip():
            k, v = line.split()
            vals['x8' if k == 'objvar' else k] = v
    return vals


def camino(solver):
    with open(CAM / f'noncvx_{solver}.csv') as f:
        return {r['path'].removesuffix('.mod'): r for r in csv.DictReader(f)}


def main():
    gurobi, scip = camino('gurobi'), camino('scip')
    for name in ('eg_disc2_s', 'eg_disc_s', 'eg_int_s'):
        variables, rows = parse_mod(MOD / f'{name}.mod')
        sol = read_sol(SOL / f'{name}.retry.sol')
        ok_bounds, slacks = evaluate(variables, rows, sol)
        ok_rows = all(sl.a > 0 for _, sl in slacks)
        min_slack = min(sl.a for _, sl in slacks)
        x8 = iv.mpf(sol['x8'])
        g, s = gurobi[name], scip[name]
        g_bound = iv.mpf(g['dual_obj'])
        print(f'{name}: rows {len(rows)}; point within bounds and integral: {ok_bounds}; '
              f'every row holds on the enclosure: {ok_rows}; smallest row slack (lower end) {float(min_slack):.3e}')
        print(f'   point objective x8 = {sol["x8"]}')
        print(f'   CAMINO Gurobi 13.0.0: obj {g["obj"]}, bestbound {g["dual_obj"]}, time {float(g["calc_time"]):.2f} s')
        print(f'   CAMINO SCIP 9.2.2:    obj {s["obj"]}, bestbound {s["dual_obj"]}, time {float(s["calc_time"]):.2f} s')
        print(f'   Gurobi bestbound - point objective in [{float(g_bound.a - x8.b):.6f}, {float(g_bound.b - x8.a):.6f}]'
              f' (positive => Gurobi bound invalid); relative {float(((g_bound.a - x8.b) / x8.b).a):.4f}')
        print(f'   SCIP bestbound <= point objective: {iv.mpf(s["dual_obj"]).b <= x8.a}')


if __name__ == '__main__':
    main()
