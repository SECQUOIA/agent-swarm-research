"""Reject incomplete/duplicated benchmark grids in isolated temporary copies."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
data = json.loads((PAPER/'verification/stage06-benchmarks.json').read_text())


def omit_method(case, method):
    del case['warmup'][method]
    del case['summary'][method]
    for run in case['runs']:
        del run['measurements'][method]
        run['order'].remove(method)


mutations = {
    'duplicate_flat': lambda d: d['flat'].__setitem__(-1, deepcopy(d['flat'][0])),
    'missing_flat': lambda d: d['flat'].pop(),
    'duplicate_membership': lambda d: d['membership'].__setitem__(-1, deepcopy(d['membership'][0])),
    'missing_membership': lambda d: d['membership'].pop(),
    'wrong_membership_labels': lambda d: d['membership'][1].__setitem__('states', 127),
    'duplicate_optimization': lambda d: d['optimization'].__setitem__(-1, deepcopy(d['optimization'][0])),
    'missing_optimization': lambda d: d['optimization'].pop(),
    'optimization_order': lambda d: d['optimization'].reverse(),
    'missing_flat_method': lambda d: omit_method(d['flat'][0], 'two_state'),
    'missing_membership_method': lambda d: omit_method(d['membership'][0], 'global'),
    'missing_optimization_method': lambda d: omit_method(d['optimization'][1], 'global'),
    'wrong_rotation': lambda d: d['optimization'][0]['runs'][1]['order'].reverse(),
    'wrong_summary': lambda d: d['optimization'][0]['summary']['full']['total_seconds'].__setitem__('median', 999),
}
records = []
for name, mutate in [('unmodified', None), *mutations.items()]:
    changed = deepcopy(data)
    if mutate is not None: mutate(changed)
    with tempfile.TemporaryDirectory(prefix='network-simplex-grid-') as directory:
        root = Path(directory); verify = root/'verification'; verify.mkdir()
        shutil.copy2(PAPER/'verification/stage06-tables.py', verify/'stage06-tables.py')
        (verify/'stage06-benchmarks.json').write_text(json.dumps(changed))
        result = subprocess.run([sys.executable, str(verify/'stage06-tables.py')],
                                text=True, capture_output=True)
        files = list((root/'tables').glob('*.tex'))
        if mutate is None:
            assert result.returncode == 0 and len(files) == 5, result.stderr
        else:
            assert result.returncode != 0 and not files, (name, result.stdout)
        records.append(dict(case=name, exit_code=result.returncode,
                            generated_tables=len(files), expected_rejection=mutate is not None))
(HERE/'table-mutations.json').write_text(json.dumps(records, indent=2)+'\n')
print('PASS: valid grid generates five tables; all 13 independent private mutations rejected before output.')
