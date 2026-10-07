"""Base relaxation B = Shor + RLT + TRI (triangle separation to convergence) on a spar instance.
Usage: python spar_base.py name out.json [solver]"""
import sys, json, time, glob
import numpy as np
sys.path.insert(0, '.')
from relax import Relax, read_boxqp, separate_triangles
D = '../sources/BoxQP_instances-master/'

def opt_values():
    vals = {}
    for line in open(D + 'README.txt'):
        t = line.split()
        if len(t) == 2 and t[0].startswith('spar'):
            vals[t[0]] = float(t[1])
    return vals

def main():
    name, out = sys.argv[1], sys.argv[2]
    solver = sys.argv[3] if len(sys.argv) > 3 else 'clarabel'
    path = glob.glob(D + '*/' + name + '.in')[0]
    H, g = read_boxqp(path)
    R = Relax(H, g, name)
    t0 = time.time(); rounds = []
    for rnd in range(60):
        res = R.solve(solver)
        cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-6, cap=5000)
        rounds.append({'pobj': res['pobj'], 'safe': res['safe'], 'status': res['status'], 't': res['time_solve'], 'newtri': len(cuts)})
        if not cuts: break
        for c in cuts: R.add_triangle(*c)
    x = res['xv']
    opt = -opt_values()[name]
    rec = {'name': name, 'n': len(g), 'opt_min': opt, 'B': res['pobj'], 'B_safe': res['safe'], 'gap': opt - res['safe'],
           'relgap': (opt - res['safe']) / abs(opt), 'interior': int(((x > 1e-6) & (x < 1 - 1e-6)).sum()),
           'tri': len(R.tri_added), 'time_total': time.time() - t0, 'rounds': rounds, 'size': R.size()}
    json.dump(rec, open(out, 'w'))
    print(name, 'gap %.6f relgap %.2e' % (rec['gap'], rec['relgap']), 'interior', rec['interior'], 'time %.0f' % rec['time_total'])

if __name__ == '__main__':
    main()
