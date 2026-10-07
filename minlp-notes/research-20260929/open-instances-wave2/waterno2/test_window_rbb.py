"""rbb on a multi-period window: how far does the certified bound rise?"""
import os, sys, json, time
import numpy as np
import period, rbb, bundle

T = int(sys.argv[1])
D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
k = json.load(open(sys.argv[2]))
lam, mu = k['lam'], k['mu']
a, b = map(int, sys.argv[3].split('-'))
target = float(sys.argv[4])
W = rbb.Window(D, a, b)
c = W.objective(lam, mu)
obbt_vars = sorted({x for kind, args in W.auxdef for x in args if not W.isbin[x]})
res = rbb.solve(W, c, target, node_limit=int(sys.argv[5]), time_limit=float(sys.argv[6]), verbose=True,
                obbt_vars=obbt_vars)
print('window', a, b, 'target', target, 'result', {kk: res[kk] for kk in ('bound', 'nodes', 'open', 'status', 'time')})
