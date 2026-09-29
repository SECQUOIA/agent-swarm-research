"""nd2 runs (Example 3.6(d)). Usage: OMP_NUM_THREADS=1 python3 sweep_nd2.py > logs/sweep_nd2.jsonl"""
import json
from multiprocessing import Pool
from sweep import work
TASKS = [('nd2', rep, e, mode) for mode, rep in [('off', None), ('fix', 'mono'), ('10', 'mono')]
         for e in (1e-2, 1e-4, 1e-6, 1e-8)]
if __name__ == '__main__':
    with Pool(6) as p:
        for r in p.imap_unordered(work, TASKS):
            print(json.dumps(r), flush=True)
