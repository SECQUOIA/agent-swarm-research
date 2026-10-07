"""Float DP (same grids as catmix_bound) and the gap, per stage, between the reference
cost-to-go at the reference ray and the DP lower-bound value there."""
import sys, numpy as np
sys.path.insert(0, '..')
import catmix_model as cmx, catmix_bound as cb
N = int(sys.argv[1]); dc = float(sys.argv[2]); Kw = int(sys.argv[3]); dw = float(sys.argv[4])
if len(sys.argv) > 5: cb.BAND = tuple(float(v) for v in sys.argv[5:8])
m, K = cmx.extract(N); fm = cmx.FloatModel(K, N)
a, b, c, ep, em = fm.a, fm.b, fm.c, fm.ep, fm.em
u = np.load('../logs/catmix%d_u.npy' % N)
grids, thstar, Jref = cb.make_grids(N, K, u, dc, Kw, dw)
J, g, xs = fm.J_grad(u)
ys = np.array([[(1 - a*u[i])*xs[i, 0] + b*u[i]*xs[i, 1], a*u[i]*xs[i, 0] + (em - c*u[i])*xs[i, 1]] for i in range(N)])
# reference cost-to-go per unit mass: (J + 1) / |y_i|_1 is the value of continuing with u along the reference
ref = (J + 1) / ys.sum(1)
def Mapply(uu, y1, y2):
    P11 = 1 + a*uu; P12 = -b*uu; P21 = -a*uu; P22 = ep + c*uu
    det = P11*P22 - P12*P21
    x1 = (P22*y1 - P12*y2)/det; x2 = (P11*y2 - P21*y1)/det
    return (1 - a*uu)*x1 + b*uu*x2, a*uu*x1 + (em - c*uu)*x2
def vmin(f, shape, extra):
    us = np.unique(np.concatenate([np.linspace(0, 1, 401), extra]))
    return np.stack([f(np.full(shape, uu)) for uu in us]).min(0)
th = grids[N-1]
w = vmin(lambda uu: (lambda P: ((P[1][1]*(1-th) - P[0][1]*th) + (P[0][0]*th - P[1][0]*(1-th))) /
                     (P[0][0]*P[1][1] - P[0][1]*P[1][0]))([[1 + a*uu, -b*uu], [-a*uu, ep + c*uu]]), th.shape, np.array([u[N]]))
out = []
for i in range(N - 1, 0, -1):
    out.append((i, ref[i] - np.interp(thstar[i], th, w)))
    thn = grids[i-1]
    w = vmin(lambda uu: (lambda z: (z[0] + z[1])*np.interp(z[1]/(z[0] + z[1]), th, w))(Mapply(uu, 1 - thn, thn)), thn.shape, np.array([u[i]]))
    th = thn
out.append((0, ref[0] - np.interp(thstar[0], th, w)))
for i, d in out[::max(1, N // 20)]:
    print('stage %4d  theta* %.5f  u_i %.4f  ref - W = %.3e' % (i, thstar[i], u[i], d))
