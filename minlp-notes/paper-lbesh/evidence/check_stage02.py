"""Targeted checks of the manuscript's explicit algebra and source settings.

The analytic proofs are in the manuscript. These checks corroborate examples
and inspect selected frozen-source defaults; they do not prove the theorems
or certify floating-point solver outcomes. Supply the extracted research root;
source validation is mandatory and is never silently omitted.
"""
from pathlib import Path
import ast
import json
import math
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--research-root', type=Path, required=True,
                    help='Directory containing code/minlp_solver_lab from the research supplement')
root = parser.parse_args().research_root.resolve()
solver = root / 'code/minlp_solver_lab/lbesh/solver.py'
tree = ast.parse(solver.read_text())
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'LBESH')
methods = {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}
sep = methods['_separate_point']
defaults = dict(zip([a.arg for a in sep.args.args][-len(sep.args.defaults):], sep.args.defaults))
assert ast.literal_eval(defaults['lamtol']) == 1e-6
node_calls = [n for n in ast.walk(methods['_single_tree']) if isinstance(n, ast.Call)
              and isinstance(n.func, ast.Attribute) and n.func.attr == '_separate_point']
node_cutoffs = [ast.literal_eval(k.value) for n in node_calls for k in n.keywords if k.arg == 'lamtol']
assert node_cutoffs == [0.05]
lp_calls = [n for n in ast.walk(methods['_lp_phase']) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr == '_separate_point']
assert len(lp_calls) == 1 and all(k.arg != 'lamtol' for k in lp_calls[0].keywords)

zx = (162 + 20 * math.sqrt(157)) / 481
zy = .9 - .45 * zx
assert abs(zx*zx + zy*zy - 1) < 1e-14
assert .85 < zx < .87 and .50 < zy < .52
witnesses = []
for x, y in [(1.2, 1), (1.3, -2)]:
    witnesses.append({'point': [x, y], 'ecp_violation': x - 1.25,
                      'esh_violation': zx*x + zy*y - 1})
assert witnesses[0]['ecp_violation'] < 0 < witnesses[0]['esh_violation']
assert witnesses[1]['esh_violation'] < 0 < witnesses[1]['ecp_violation']

counts = []
for a in [2, 4, 10, 100]:
    assert (math.exp(a) - 1) / a > 2
    p, k = 2., 0
    while p > 1.1:
        v = math.expm1(a * (p-1))
        derivative = a * math.exp(a * (p-1))
        newton = p - v / derivative
        recurrent = p + math.expm1(-a * (p-1)) / a
        assert abs(newton - recurrent) < 1e-14
        assert 1 < recurrent < p
        assert p - recurrent < 1/a + 1e-15
        p, k = recurrent, k + 1
    assert k > a * .9
    counts.append({'a': a, 'cuts_to_geometric_error_point1': k})

# At z=.5, g(z)=-.75, g'(z)=1, so the complete constant is -1.25.
assert .5**2 - 1 - 1*.5 == -1.25
assert 1 - 1.25 <= 0 < 1 - .5
# Disk repair: p=(2,1), v=4, delta=1, anchor=(0,0), q=p/5.
q = [2/5, 1/5]
assert sum(t*t for t in q) <= 1
ratios = [1 / math.sqrt(e) for e in [1e-2, 1e-4, 1e-6]]
assert ratios == [10, 100, 1000]

print(json.dumps({'source_contract': {'lp_weight_cutoff': 1e-6,
                    'optional_node_weight_cutoff': node_cutoffs[0]},
                  'disk_boundary': [zx, zy], 'non_dominance_witnesses': witnesses,
                  'scalar_counts': counts, 'intersection_error_over_residual': ratios,
                  'checks': 'passed'}, indent=2))
