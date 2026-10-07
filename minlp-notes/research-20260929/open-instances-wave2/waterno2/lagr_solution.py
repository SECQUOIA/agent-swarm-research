"""Show the period solutions of the Lagrangian at given multipliers (SCIP, exploratory)."""
import sys, json
import period, bundle

T = int(sys.argv[1])
D = period.setup(T)
k = json.load(open(sys.argv[2]))
lam, mu = k['lam'], k['mu']
M, S = D['M'], D['S']
print('mu', mu)
for t in range(T):
    print('lam', t, ['%.4f' % v for v in lam[t]] if t < T - 1 else '')
tot = mu * float(D['hor_rhs'])
for t in range(T):
    r = period.solve_window(D, t, t + 1, lam, mu, 120, bundle.NOPROP)
    x = r['x']
    vs = S['per_vars'][t]
    bins = [int(round(x[v])) for v in vs if M['vt'][v] == 'B']
    cost = sum(x[v] for v in vs if v in M['obj'])
    Ls = ['%.3f' % x[b] for (i, a, b) in S['link'][t - 1]] if t > 0 else None
    Le = ['%.3f' % x[a] for (i, a, b) in S['link'][t]] if t < T - 1 else None
    h = [x[v] for v in D['hor'] if D['per_of'][v] == t][0]
    tot += r['dual']
    print(t, 'phi %.4f' % r['dual'], 'A', bins[0:3], 'B1', bins[3:5], 'B2', bins[5:7], 'D', bins[7:9], 'cost %.3f' % cost, 'QA %.4f' % h, 'Ls', Ls, 'Le', Le)
print('L =', tot)
