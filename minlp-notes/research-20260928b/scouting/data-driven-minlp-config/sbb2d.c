/* Tiny 2-D spatial branch-and-bound: f(x,y) = P1(x) + P2(y) + g*x*y on [0,1]^2,
 * P1, P2 quartics. alphaBB underestimator with fixed diagonal shifts rho1, rho2
 * (valid on the root box: rho_i = max(0, -(min P_i'' - |g|)/2)), projected Newton
 * for the convex node problem. Widest-edge branching (ties -> x), split at
 * l + a (u - l). Incumbent: oracle f* (mode 0) or dynamic best-first (mode 1).
 * usage: sbb2d p10..p14 p20..p24 g eps mode lo hi N
 * output: a nodes maxdepth
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static double A[5], B[5], G, EPS, R1, R2, FSTAR; static int MODE;
#define CAP 400000
static double q(const double *c, double x) { return (((c[4]*x + c[3])*x + c[2])*x + c[1])*x + c[0]; }
static double q1(const double *c, double x) { return ((4*c[4]*x + 3*c[3])*x + 2*c[2])*x + c[1]; }
static double q2(const double *c, double x) { return (12*c[4]*x + 6*c[3])*x + 2*c[2]; }
static double f(double x, double y) { return q(A, x) + q(B, y) + G*x*y; }
static double minq2(const double *c) { double m = fmin(q2(c, 0), q2(c, 1)); if (c[4] > 0) { double v = -6*c[3]/(24*c[4]); if (v > 0 && v < 1) m = fmin(m, q2(c, v)); } return m; }

typedef struct { double l1, u1, l2, u2; } Box;
static double gval(const Box *b, double x, double y) { return f(x, y) - R1*(x - b->l1)*(b->u1 - x) - R2*(y - b->l2)*(b->u2 - y); }
static double lbound(const Box *b, double *xo, double *yo) {
    double x = 0.5*(b->l1 + b->u1), y = 0.5*(b->l2 + b->u2);
    double v = gval(b, x, y);
    for (int it = 0; it < 100; it++) {
        double gx = q1(A, x) - R1*(b->l1 + b->u1 - 2*x) + G*y;
        double gy = q1(B, y) - R2*(b->l2 + b->u2 - 2*y) + G*x;
        double hxx = q2(A, x) + 2*R1, hyy = q2(B, y) + 2*R2, hxy = G;
        int fx = !((x <= b->l1 && gx > 0) || (x >= b->u1 && gx < 0));
        int fy = !((y <= b->l2 && gy > 0) || (y >= b->u2 && gy < 0));
        double dx = 0, dy = 0;
        if (fx && fy) { double det = hxx*hyy - hxy*hxy; if (det > 1e-14) { dx = -( hyy*gx - hxy*gy)/det; dy = -(-hxy*gx + hxx*gy)/det; } else { dx = -gx; dy = -gy; } }
        else if (fx) dx = -gx/fmax(hxx, 1e-12);
        else if (fy) dy = -gy/fmax(hyy, 1e-12);
        if (fabs(dx) + fabs(dy) < 1e-15) break;
        double t = 1.0, nx, ny, nv;
        for (int ls = 0; ls < 60; ls++) {
            nx = fmin(b->u1, fmax(b->l1, x + t*dx)); ny = fmin(b->u2, fmax(b->l2, y + t*dy));
            nv = gval(b, nx, ny);
            if (nv <= v - 1e-4*(gx*(x - nx) + gy*(y - ny)) || nv <= v) break;
            t *= 0.5;
        }
        if (nv > v) break;
        double step = fabs(nx - x) + fabs(ny - y);
        x = nx; y = ny; v = nv;
        if (step < 1e-15) break;
    }
    *xo = x; *yo = y; return v;
}
typedef struct { Box b; double lb, xh, yh; int depth; long id; } Node;
static Node heap[2*CAP+10]; static int hn;
static int less(Node *a, Node *b) { return a->lb < b->lb || (a->lb == b->lb && a->id < b->id); }
static void push(Node x) { int i = hn++; heap[i] = x; while (i > 0) { int p = (i-1)/2; if (less(&heap[i], &heap[p])) { Node t = heap[i]; heap[i] = heap[p]; heap[p] = t; i = p; } else break; } }
static Node pop(void) { Node r = heap[0]; heap[0] = heap[--hn]; int i = 0; for (;;) { int a = 2*i+1, b = a+1, m = i; if (a < hn && less(&heap[a], &heap[m])) m = a; if (b < hn && less(&heap[b], &heap[m])) m = b; if (m == i) break; Node t = heap[i]; heap[i] = heap[m]; heap[m] = t; i = m; } return r; }
static void run(double a, long *nodes, int *maxd) {
    double UB = MODE == 0 ? FSTAR : INFINITY; hn = 0; long created = 1, id = 0; int md = 0;
    Node r; r.b = (Box){0, 1, 0, 1}; r.depth = 0; r.id = id++; r.lb = lbound(&r.b, &r.xh, &r.yh); push(r);
    while (hn > 0) {
        Node nd = pop();
        if (MODE == 1) UB = fmin(UB, f(nd.xh, nd.yh));
        if (nd.lb >= UB - EPS) continue;
        if (created >= CAP) { *nodes = CAP; *maxd = md; return; }
        Node c1 = nd, c2 = nd; c1.depth = c2.depth = nd.depth + 1; c1.id = id++; c2.id = id++;
        double w1 = nd.b.u1 - nd.b.l1, w2 = nd.b.u2 - nd.b.l2;
        if (w1 >= w2*(1 - 1e-9)) { double p = nd.b.l1 + a*w1; c1.b.u1 = p; c2.b.l1 = p; }
        else { double p = nd.b.l2 + a*w2; c1.b.u2 = p; c2.b.l2 = p; }
        c1.lb = lbound(&c1.b, &c1.xh, &c1.yh); c2.lb = lbound(&c2.b, &c2.xh, &c2.yh);
        if (MODE == 1) { UB = fmin(UB, f(c1.xh, c1.yh)); UB = fmin(UB, f(c2.xh, c2.yh)); }
        created += 2; if (nd.depth + 1 > md) md = nd.depth + 1;
        push(c1); push(c2);
    }
    *nodes = created; *maxd = md;
}
int main(int argc, char **argv) {
    if (argc < 16) { fprintf(stderr, "usage\n"); return 1; }
    for (int i = 0; i < 5; i++) { A[i] = atof(argv[1+i]); B[i] = atof(argv[6+i]); }
    G = atof(argv[11]); EPS = atof(argv[12]); MODE = atoi(argv[13]);
    double lo = atof(argv[14]), hi = atof(argv[15]); long N = atol(argv[16]);
    R1 = fmax(0, -0.5*(minq2(A) - fabs(G))); R2 = fmax(0, -0.5*(minq2(B) - fabs(G)));
    /* f*: grid + local Newton polish via the same routine on a tiny box */
    double best = INFINITY, bx = 0, by = 0; int M = 2000;
    for (int i = 0; i <= M; i++) for (int j = 0; j <= M; j++) { double x = (double)i/M, y = (double)j/M, v = f(x, y); if (v < best) { best = v; bx = x; by = y; } }
    { double sR1 = R1, sR2 = R2; R1 = R2 = 0; Box bb = { fmax(0, bx - 2.0/M), fmin(1, bx + 2.0/M), fmax(0, by - 2.0/M), fmin(1, by + 2.0/M) }; double xx, yy; double v = lbound(&bb, &xx, &yy); if (v < best) best = v; R1 = sR1; R2 = sR2; }
    FSTAR = best;
    fprintf(stderr, "fstar %.17g near (%.6f, %.6f) rho %.6g %.6g\n", FSTAR, bx, by, R1, R2);
    for (long i = 0; i < N; i++) { double t = lo + (hi - lo)*(double)i/(double)(N - 1); long nodes; int md; run(t, &nodes, &md); printf("%.15f %ld %d\n", t, nodes, md); }
    return 0;
}
