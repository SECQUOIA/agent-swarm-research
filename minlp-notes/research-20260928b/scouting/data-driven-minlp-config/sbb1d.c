/* Tiny 1-D spatial branch-and-bound for a quartic f on [0,1] with an
 * alphaBB underestimator (box-dependent rho = max(0, -min f''/2)).
 * Sweeps a branching parameter over a grid and prints tree size per value.
 *
 * usage: sbb1d c0 c1 c2 c3 c4 eps mode rule lo hi N [lambda|beta]
 *   mode 0: oracle incumbent (UB = f* from the start; tree independent of node order)
 *   mode 1: dynamic incumbent (UB from f(xhat), f(mid)), best-first node selection
 *   rule 0: branch at l + a (u - l), sweep a in [lo,hi]
 *   rule 1: branch at clip(a*xhat + (1-a)*mid, [l+beta w, u-beta w]), sweep a (=lambda), extra arg beta
 *   rule 2: same formula, sweep beta in [lo,hi], extra arg lambda
 * env FIXEDRHO=1: use the root-box rho at every node (classic alphaBB with one alpha)
 * output lines: param nodes maxdepth
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static double C[5];
static int MODE, RULE;
static double EPS, EXTRA, RHO0 = -1;
#define CAP 200000

static double f(double x) { return (((C[4]*x + C[3])*x + C[2])*x + C[1])*x + C[0]; }
static double fp(double x) { return ((4*C[4]*x + 3*C[3])*x + 2*C[2])*x + C[1]; }
static double fpp(double x) { return (12*C[4]*x + 6*C[3])*x + 2*C[2]; }

static double minfpp(double l, double u) {
    double m = fmin(fpp(l), fpp(u));
    if (C[4] > 0) { double xv = -6*C[3]/(24*C[4]); if (xv > l && xv < u) m = fmin(m, fpp(xv)); }
    return m;
}

/* lower bound and minimizer of convex underestimator on [l,u] */
static double lbound(double l, double u, double *xh) {
    double rho = (RHO0 >= 0) ? RHO0 : fmax(0.0, -0.5*minfpp(l, u));
    #define GP(x) (fp(x) - rho*(l + u - 2*(x)))
    double x;
    if (GP(l) >= 0) x = l;
    else if (GP(u) <= 0) x = u;
    else {
        double a = l, b = u;
        for (int it = 0; it < 80; it++) { double m = 0.5*(a+b); if (GP(m) < 0) a = m; else b = m; }
        x = 0.5*(a+b);
    }
    *xh = x;
    return f(x) - rho*(x - l)*(u - x);
}

typedef struct { double l, u, lb, xh; int depth; long id; } Node;
static Node heap[2*CAP+10]; static int hn;
static int less(Node *a, Node *b) { return a->lb < b->lb || (a->lb == b->lb && a->id < b->id); }
static void push(Node x) { int i = hn++; heap[i] = x; while (i > 0) { int p = (i-1)/2; if (less(&heap[i], &heap[p])) { Node t = heap[i]; heap[i] = heap[p]; heap[p] = t; i = p; } else break; } }
static Node pop(void) { Node r = heap[0]; heap[0] = heap[--hn]; int i = 0; for (;;) { int a = 2*i+1, b = a+1, m = i; if (a < hn && less(&heap[a], &heap[m])) m = a; if (b < hn && less(&heap[b], &heap[m])) m = b; if (m == i) break; Node t = heap[i]; heap[i] = heap[m]; heap[m] = t; i = m; } return r; }

static double FSTAR, RHOROOT;

static void run(double a, long *nodes, int *maxd) {
    if (RULE == 3) RHO0 = a * RHOROOT;
    double UB = (MODE == 0) ? FSTAR : INFINITY;
    hn = 0; long created = 1, id = 0; int md = 0;
    Node r; r.l = 0; r.u = 1; r.depth = 0; r.id = id++; r.lb = lbound(0, 1, &r.xh);
    push(r);
    while (hn > 0) {
        Node nd = pop();
        if (MODE == 1) { UB = fmin(UB, f(nd.xh)); UB = fmin(UB, f(0.5*(nd.l+nd.u))); }
        if (nd.lb >= UB - EPS) continue;
        if (created >= CAP) { *nodes = CAP; *maxd = md; return; }
        double w = nd.u - nd.l, p;
        if (RULE == 0) p = nd.l + a*w;
        else if (RULE == 3) p = nd.l + EXTRA*w;
        else {
            double lam = (RULE == 1) ? a : EXTRA, beta = (RULE == 1) ? EXTRA : a;
            p = lam*nd.xh + (1-lam)*0.5*(nd.l+nd.u);
            double lo = nd.l + beta*w, hi = nd.u - beta*w;
            if (p < lo) p = lo; if (p > hi) p = hi;
        }
        Node c1 = {nd.l, p, 0, 0, nd.depth+1, id++}, c2 = {p, nd.u, 0, 0, nd.depth+1, id++};
        c1.lb = lbound(c1.l, c1.u, &c1.xh); c2.lb = lbound(c2.l, c2.u, &c2.xh);
        created += 2; if (nd.depth+1 > md) md = nd.depth+1;
        if (MODE == 1) { UB = fmin(UB, f(c1.xh)); UB = fmin(UB, f(c2.xh)); }
        push(c1); push(c2);
    }
    *nodes = created; *maxd = md;
}

int main(int argc, char **argv) {
    if (argc < 12) { fprintf(stderr, "usage\n"); return 1; }
    for (int i = 0; i < 5; i++) C[i] = atof(argv[1+i]);
    EPS = atof(argv[6]); MODE = atoi(argv[7]); RULE = atoi(argv[8]);
    double lo = atof(argv[9]), hi = atof(argv[10]); long N = atol(argv[11]);
    EXTRA = argc > 12 ? atof(argv[12]) : 0.0;
    if (getenv("FIXEDRHO")) RHO0 = fmax(0.0, -0.5*minfpp(0, 1));
    /* f* by dense grid + bisection on f' near best grid point */
    double best = INFINITY, bx = 0; int G = 200000;
    for (int i = 0; i <= G; i++) { double x = (double)i/G; double v = f(x); if (v < best) { best = v; bx = x; } }
    double a = fmax(0, bx - 1.0/G), b = fmin(1, bx + 1.0/G);
    if (fp(a) < 0 && fp(b) > 0) { for (int it = 0; it < 100; it++) { double m = 0.5*(a+b); if (fp(m) < 0) a = m; else b = m; } bx = 0.5*(a+b); best = fmin(best, f(bx)); }
    FSTAR = best; RHOROOT = fmax(0.0, -0.5*minfpp(0, 1));
    fprintf(stderr, "fstar %.17g at %.17g\n", FSTAR, bx);
    for (long i = 0; i < N; i++) {
        double t = lo + (hi - lo)*(double)i/(double)(N-1);
        long nodes; int md; run(t, &nodes, &md);
        printf("%.15f %ld %d\n", t, nodes, md);
    }
    return 0;
}
