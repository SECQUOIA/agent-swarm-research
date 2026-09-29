/* Clean model: f(x) = (x - xs)^2 on [0,1], fixed alphaBB shift rho, oracle incumbent f* = 0.
 * Node [l,u] (center m, half-width r) is expanded iff r^2 - (m - xs)^2/(1+rho) > eps/rho
 * (exact closed form of the alphaBB bound, see report). Branch at l + a (u - l).
 * usage: quadmodel xs rho eps lo hi N  -> raw int32 node counts (binary variant)
 */
#include <stdio.h>
#include <stdlib.h>
static double XS, RHO, EPS;
static long cnt(double l, double u, double a, int depth) {
    double m = 0.5*(l + u), r = 0.5*(u - l), d = m - XS;
    if (!(r*r - d*d/(1 + RHO) > EPS/RHO) || depth > 200) return 1;
    double p = l + a*(u - l);
    return 1 + cnt(l, p, a, depth + 1) + cnt(p, u, a, depth + 1);
}
int main(int argc, char **argv) {
    XS = atof(argv[1]); RHO = atof(argv[2]); EPS = atof(argv[3]);
    double lo = atof(argv[4]), hi = atof(argv[5]); long N = atol(argv[6]);
    int *buf = malloc(sizeof(int)*N); for (long i = 0; i < N; i++) { double a = lo + (hi - lo)*(double)i/(double)(N - 1); buf[i] = (int)cnt(0, 1, a, 0); } fwrite(buf, sizeof(int), N, stdout);
    return 0;
}
