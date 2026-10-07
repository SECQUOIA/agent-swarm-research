import os, sys, json, time
import period, bundle
T = int(sys.argv[1])
D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
k = json.load(open(sys.argv[2]))
for t in [int(a) for a in sys.argv[3].split(',')]:
    for name, prm in (('noprop', bundle.NOPROP), ('default', {})):
        r = period.solve_window(D, t, t + 1, k['lam'], k['mu'], 120, prm)
        print(t, name, r['status'], r['dual'], r['primal'], round(r['time'], 1), r['nodes'], flush=True)
