"""Rerun the three frozen optimization cases; retain membership measurements.

Run at repository root with PYTHONPATH=code. The original data, including each
fixed objective, weight and additional row, are read from the hashed archive.
"""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import scipy

from network_simplex_benchmarks.baselines import block_chain
from network_simplex_benchmarks.paper_stage06 import local_labels_instance, opt_case

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = HERE/'round1-archive/paper-network-simplex/verification/stage06-benchmarks.json'
original = json.loads(SOURCE.read_text())
output = deepcopy(original)
assert not output['quick'] and output['repetitions'] == 5
assert output['versions'] == dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)
methods = [
    ['full','global','initial','eliminated','network_states','cuts'],
    ['full','global','initial','eliminated','cuts'],
    ['full','global','initial','eliminated','network_states'],
]
output['optimization'] = []
for index, prior in enumerate(original['optimization']):
    instance = local_labels_instance() if index == 2 else block_chain(seed=33, blocks=4, paths=5, states=128)
    objective = np.asarray(prior['objective_vector'])
    y = list(map(F, prior['y']))
    rows = [(np.asarray(row['coefficients']), F(row['rhs'])) for row in prior['extra_rows']]
    case = opt_case(instance, objective, y, rows, methods[index], 5)
    assert abs(case['objective']-prior['objective']) < 1e-7
    for key in ('name','unconstrained_resource','reference_resource','scope'):
        if key in prior: case[key] = prior[key]
    for key in ('edges','states','observations','observed_labels','y','objective_vector','extra_rows'):
        assert case[key] == prior[key], key
    output['optimization'].append(case)
    print(json.dumps({'case':case['name'], 'median_ms':
          {method:1000*stats['total_seconds']['median'] for method, stats in case['summary'].items()},
          'model_sizes':{method:record['stats'] for method, record in case['warmup'].items()}}), flush=True)
assert output['flat'] == original['flat'] and output['membership'] == original['membership']
assert output['cold'] == original['cold']
output['optimization_revision'] = {
    'utc':datetime.now(timezone.utc).isoformat(),
    'reason':'Joint full/global LPs now use fixed positive state flows and native scaled bounds.',
    'source_data_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source_archive':str(SOURCE.relative_to(ROOT)),
    'rerun':'All methods in all three unchanged optimization cases; one audited warmup and five rotated timed runs.',
    'unchanged':'All 16 flat cases, three many-label membership cases, and cold-library measurements are retained exactly from round 1.',
    'command':'PYTHONPATH=code python paper-network-simplex/verification/stage06-corrections/rerun_optimization.py',
}
target = ROOT/'paper-network-simplex/verification/stage06-benchmarks.json'
target.write_text(json.dumps(output, indent=2)+'\n')
print('PASS: all original optima reproduced; membership and cold records unchanged.', flush=True)
