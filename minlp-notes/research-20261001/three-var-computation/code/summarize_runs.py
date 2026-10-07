"""Summarize driver.py logs.  Usage: python summarize_runs.py log.jsonl [opt]
For each method: final primal objective (pobj) and safe dual bound, gap closed
relative to B (using opt if given, otherwise the best final bound over methods),
rounds, cumulative solve and separation time, last solve time, final size."""
import json
import sys
from collections import OrderedDict


def load(path):
    recs = [json.loads(l) for l in open(path)]
    by = OrderedDict()
    for r in recs:
        by.setdefault(r['method'], []).append(r)
    return by


def table(path, opt=None, out=sys.stdout):
    by = load(path)
    B = by['B'][-1]
    ref = opt if opt is not None else max(v[-1]['pobj'] for v in by.values())
    rows = []
    for m, rs in by.items():
        last = rs[-1]
        cum_solve = sum(r['time_solve'] for r in rs if m == 'B' or r['round'] not in (0, 100) or r is rs[-1])
        # each record carries the solve that produced its point; first record of a non-B method
        # repeats the starting solution, so exclude it from the cumulative time
        cum_solve = sum(r['time_solve'] for r in rs[1:]) if m != 'B' else sum(r['time_solve'] for r in rs)
        cum_sep = sum(r['time_sep'] for r in rs)
        s = last['size']
        closed = (last['pobj'] - B['pobj']) / (ref - B['pobj']) if ref != B['pobj'] else float('nan')
        closed_safe = (last['safe'] - B['safe']) / (ref - B['safe']) if ref != B['safe'] else float('nan')
        rows.append((m, last['pobj'], last['safe'], closed, closed_safe, len(rs) - (0 if m == 'B' else 1),
                     cum_solve, cum_sep, last['time_solve'], s['vars'], s['psd'], s['soc'], s.get('lin', 0),
                     s.get('psd_svec', 0), last['status']))
    print('%s  (reference value %.8f%s)' % (path, ref, ' = opt' if opt is not None else ' = best bound'), file=out)
    print('%-5s %16s %16s %8s %8s %4s %8s %7s %7s %7s %6s %6s %s' % (
        'meth', 'bound', 'safe', 'closed', 'cl_safe', 'rnd', 't_solve', 't_sep', 't_last', 'vars', 'soc', 'lin', 'psd blocks'), file=out)
    for r in rows:
        print('%-5s %16.8f %16.8f %8.4f %8.4f %4d %8.2f %7.2f %7.2f %7d %6d %6d %s %s' % (
            r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[11], r[12], r[10], r[14]), file=out)
    return rows


if __name__ == '__main__':
    table(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else None)
