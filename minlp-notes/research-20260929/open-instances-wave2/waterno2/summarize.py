"""Per-period summary of a point: pump configuration, station flows, levels, costs."""
import sys, json
from fractions import Fraction
import period, evalpt

def summarize(D, x):
    M, S = D['M'], D['S']
    N = M['names']
    out = []
    for t in range(D['T']):
        vs = S['per_vars'][t]
        bins = [int(round(x[v])) for v in vs if M['vt'][v] == 'B']
        cost = sum(x[v] for v in vs if v in M['obj'])
        # levels: link vars
        Ls = [x[b] for (i, a, b) in S['link'][t - 1]] if t > 0 else None
        Le = [x[a] for (i, a, b) in S['link'][t]] if t < D['T'] - 1 else None
        h = [x[v] for v in D['hor'] if D['per_of'][v] == t][0]
        out.append(dict(t=t, bins=bins, cost=cost, QA=h, Ls=Ls, Le=Le))
    return out

if __name__ == '__main__':
    T = int(sys.argv[1])
    D = period.setup(T)
    if sys.argv[2].endswith('.json'):
        x = [float(v) for v in json.load(open(sys.argv[2]))['x']]
    else:
        xs, _ = evalpt.read_sol(sys.argv[2], D['M']['names']); x = [float(v) for v in xs]
    for r in summarize(D, x):
        print(r['t'], 'A', r['bins'][0:3], 'B1', r['bins'][3:5], 'B2', r['bins'][5:7], 'D', r['bins'][7:9],
              'cost %.4f' % r['cost'], 'QA %.4f' % r['QA'], 'Ls', None if r['Ls'] is None else ['%.4f' % v for v in r['Ls']],
              'Le', None if r['Le'] is None else ['%.4f' % v for v in r['Le']])
