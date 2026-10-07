import sys, time, numpy as np
sys.path.insert(0, '.')
from relax import Relax, read_boxqp, separate_triangles
D = '../sources/BoxQP_instances-master/'
name = sys.argv[1]; sub = sys.argv[2]
H, g = read_boxqp(D + sub + '/' + name + '.in')
R = Relax(H, g, name)
for rnd in range(30):
    t = time.time()
    res = R.solve('clarabel')
    cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-6, cap=2000)
    print(rnd, res['status'], 'obj %.6f safe %.6f' % (res['pobj'], res['safe']), 'iters', res['iters'],
          'tsolve %.1f tbuild %.1f' % (res['time_solve'], res['time_build']), 'newtri', len(cuts), 'maxviol %.2e' % mv, flush=True)
    if not cuts: break
    for c in cuts: R.add_triangle(*c)
x = res['xv']
print('interior x count', np.sum((x > 1e-4) & (x < 1 - 1e-4)), 'of', len(x))
print(R.size())
