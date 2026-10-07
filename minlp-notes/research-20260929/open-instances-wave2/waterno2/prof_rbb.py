import cProfile, pstats, json
import period, rbb
D = period.setup(6)
k = json.load(open('logs/mult_06_w1.json'))
W = rbb.Window(D, 0, 1)
c = W.objective(k['lam'], k['mu'])
cProfile.run('r = rbb.solve(W, c, 167.1648, node_limit=400, time_limit=100)', '/tmp/prof_rbb.out')
print(r)
p = pstats.Stats('/tmp/prof_rbb.out'); p.sort_stats('cumulative').print_stats(18)
