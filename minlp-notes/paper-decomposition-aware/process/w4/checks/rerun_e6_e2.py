"""Re-run E6 (all 40 tasks) and the E2 CT runs with kappa_target >= 64 in memory
with the current code, and compare deterministic outputs with results/raw.
Nothing is written to experiments/results."""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[v] = '1'
EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
import run_all  # noqa: E402

RAW = EXP / 'results' / 'raw'


def one(item):
    key, kind, spec = item
    rec = run_all.TASKS[kind](spec)
    return key, rec


def summary(kind, rec):
    if kind == 'random_growth':
        runs = {str(q): (r['status'], r['stages'], r['trials'], r['max_nodes'], r['table_states'],
                         r.get('xhat_nodes_free_last_stage'), r['replay_valid'])
                for q, r in rec['runs'].items()}
        g = rec['growth']
        return (rec['status'], g['status'], g.get('gamma'), g.get('g_ub'), rec.get('xhat'), runs)
    return (rec['status'], rec['lower'], rec['upper'], rec['stats']['completed_stages'],
            rec['stats']['completed_table_states'], [s['trial'] for s in rec['stages']][-1],
            rec['verify']['valid'])


if __name__ == '__main__':
    tasks = [t for t in run_all.design()
             if t[2]['exp'] == 'E6'
             or (t[2]['exp'] == 'E2' and t[2].get('method') == 'default_schedule' and t[2]['kappa_target'] >= 64)]
    diffs = 0
    with ProcessPoolExecutor(max_workers=4) as pool:
        for key, rec in pool.map(one, tasks):
            old = json.loads((RAW / f'{key}.json').read_text())
            kind = next(t[1] for t in tasks if t[0] == key)
            a, b = summary(kind, json.loads(json.dumps(rec, default=str))), summary(kind, old)
            same = json.dumps(a, default=str) == json.dumps(b, default=str)
            diffs += not same
            print(key, 'same' if same else f'DIFF\n  new {a}\n  old {b}', flush=True)
    print('tasks', len(tasks), 'differences', diffs)
