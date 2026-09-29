"""Three-variable sweep (Section 9.3 of the note).
Usage: OMP_NUM_THREADS=1 python3 sweep3.py [workers] > logs/sweep3.jsonl"""
import sys, json
from multiprocessing import Pool
from sweep import work

TASKS = []
for mode, rep in [('off', None), ('fix', 'exp')]:
    TASKS += [('iso3', rep, e, mode) for e in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6)]
for mode, rep in [('off', None), ('fix', 'exp'), ('fix', 'st'), ('10', 'st')]:
    TASKS += [('line3', rep, e, mode) for e in (1e-1, 1e-2, 1e-3, 1e-4)]

if __name__ == '__main__':
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as p:
        for r in p.imap_unordered(work, TASKS):
            print(json.dumps(r), flush=True)
