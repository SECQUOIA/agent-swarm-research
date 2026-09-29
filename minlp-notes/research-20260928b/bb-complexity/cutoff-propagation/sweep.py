"""Run the node-count sweep of the note (Section 9) in parallel; JSONL output.

Usage: OMP_NUM_THREADS=1 python3 sweep.py [workers] > logs/sweep.jsonl
"""
import sys
import json
import time
from multiprocessing import Pool
import bb
import instances as I

E1 = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
E2 = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
E3 = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]

TASKS = []
for mode_rep in [('off', None), ('fix', 'u'), ('fix', 'mono'), ('10', 'mono')]:
    TASKS += [('nondeg1', mode_rep[1], e, mode_rep[0]) for e in E1]
for mode_rep in [('off', None), ('fix', 'centered'), ('fix', 'exp'), ('10', 'exp')]:
    TASKS += [('nondeg1s', mode_rep[1], e, mode_rep[0]) for e in E1]
for mode_rep in [('off', None), ('fix', 'exp'), ('10', 'exp'), ('3', 'exp')]:
    TASKS += [('h1', mode_rep[1], e, mode_rep[0]) for e in E1]
for mode_rep in [('off', None), ('fix', 'exp'), ('10', 'exp')]:
    TASKS += [('linediag', mode_rep[1], e, mode_rep[0]) for e in E2]
for mode_rep in [('fix', 's'), ('10', 's'), ('3', 's')]:
    TASKS += [('linediag', mode_rep[1], e, mode_rep[0]) for e in E3]
for mode_rep in [('off', None), ('fix', 'exp'), ('10', 'exp')]:
    TASKS += [('iso2', mode_rep[1], e, mode_rep[0]) for e in E3]
for kappa in ('rot0.01', 'rot0.1', 'rot1'):
    for mode_rep in [('off', None), ('fix', 'st'), ('fix', 'exp'), ('10', 'exp')]:
        TASKS += [(kappa, mode_rep[1], e, mode_rep[0]) for e in E3]


def work(t):
    name, rep, eps, mode = t
    inst = I.make(name)
    t0 = time.time()
    res = bb.run(inst, rep, eps, mode)
    return dict(inst=name, rep=rep or '-', mode=mode, eps=eps, secs=round(time.time() - t0, 2), **res)


if __name__ == '__main__':
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    with Pool(workers) as p:
        for r in p.imap_unordered(work, TASKS):
            print(json.dumps(r), flush=True)
