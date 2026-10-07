/* Exact-model branch-and-bound on the McCormick kink family (revision after review).
 *
 *   f = 2|x - a| - (x - a)(y - b) on [0,1]^2 (c = -1, L = 2), termwise McCormick.
 *   A box is open iff l_x < a < u_x and w_y (a - l_x)(u_x - a)/w_x > eps; its relaxation point is
 *   (a, l_y + rho w_y), rho = (a - l_x)/w_x.  Widest-side selection, ties to x.
 *
 *   rules:  clip TH           fixed clamp
 *           rclip T0 T1       theta ~ U[T0,T1] independently at every node
 *           kvar T0 T1        one draw per (variable, interval): all nodes that split the same
 *                             variable on the same interval share it (the scheme of Section 5)
 *           kshared T0 T1     one draw per interval (l,u) regardless of the variable (the scheme
 *                             the first version of sim_kink.py used)
 *           recenter TH       recentring clamp
 *
 *   usage: sim2d A RULE P1 [P2] EPS NRUNS SEED
 *   prints: mean, standard error, median, q90, q99, max, number of runs over the node cap
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint64_t s[4];
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t next(void) {
    uint64_t r = rotl(s[1] * 5, 7) * 9, t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45);
    return r;
}
static double unif(void) { return (next() >> 11) * 0x1.0p-53; }
static void seed(uint64_t x) {
    for (int i = 0; i < 4; i++) { x += 0x9e3779b97f4a7c15ULL; uint64_t z = x;
        z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL; z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
        s[i] = z ^ (z >> 31); }
}

/* keyed draws: open-addressing table, cleared after every run */
#define HBITS 20
#define HSIZE (1u << HBITS)
typedef struct { double l, u; int var, used; double th; } Slot;
static Slot *tab; static uint32_t *usedlist; static uint32_t nused;
static uint64_t hkey(int var, double l, double u) {
    uint64_t a, b; memcpy(&a, &l, 8); memcpy(&b, &u, 8);
    uint64_t h = a * 0x9e3779b97f4a7c15ULL ^ (b + 0x632be59bd9b4e019ULL) * 0xc2b2ae3d27d4eb4fULL ^ (uint64_t)var * 0x165667b19e3779f9ULL;
    return h ^ (h >> 29);
}
static double keyed(int var, double l, double u, double t0, double t1) {
    uint32_t i = (uint32_t)hkey(var, l, u) & (HSIZE - 1);
    while (tab[i].used) {
        if (tab[i].var == var && tab[i].l == l && tab[i].u == u) return tab[i].th;
        i = (i + 1) & (HSIZE - 1);
    }
    tab[i].used = 1; tab[i].var = var; tab[i].l = l; tab[i].u = u;
    tab[i].th = t0 + (t1 - t0) * unif();
    usedlist[nused++] = i;
    return tab[i].th;
}
static void clear_tab(void) { for (uint32_t k = 0; k < nused; k++) tab[usedlist[k]].used = 0; nused = 0; }

enum { CLIP, RCLIP, KVAR, KSHARED, RECENTER };
static int rule; static double P1, P2;

static double point(int var, double p, double l, double u) {
    double w = u - l, th;
    switch (rule) {
    case CLIP: th = P1; break;
    case RCLIP: th = P1 + (P2 - P1) * unif(); break;
    case KVAR: th = keyed(var, l, u, P1, P2); break;
    case KSHARED: th = keyed(0, l, u, P1, P2); break;
    default: /* RECENTER */
        th = P1;
        if (p < l + th * w) return l + fmax(th * w, 2 * (p - l));
        if (p > u - th * w) return u - fmax(th * w, 2 * (u - p));
        return p;
    }
    return fmin(fmax(p, l + th * w), u - th * w);
}

typedef struct { double lx, ux, ly, uy; } Box;
static Box *stack; static long cap = 1L << 24;

static long run(double a, double eps, long nodecap) {
    long top = 0, T = 0;
    stack[top++] = (Box){0, 1, 0, 1};
    while (top) {
        Box B = stack[--top];
        if (++T > nodecap) return -1;
        if (!(B.lx < a && a < B.ux)) continue;
        double wx = B.ux - B.lx, wy = B.uy - B.ly;
        if (wy * (a - B.lx) * (B.ux - a) / wx <= eps) continue;
        if (top + 2 >= cap) { fprintf(stderr, "stack\n"); exit(1); }
        if (wx >= wy) {
            double sp = point(0, a, B.lx, B.ux);
            stack[top++] = (Box){sp, B.ux, B.ly, B.uy};
            stack[top++] = (Box){B.lx, sp, B.ly, B.uy};
        } else {
            double rho = (a - B.lx) / wx;
            double sp = point(1, B.ly + rho * wy, B.ly, B.uy);
            stack[top++] = (Box){B.lx, B.ux, sp, B.uy};
            stack[top++] = (Box){B.lx, B.ux, B.ly, sp};
        }
    }
    return T;
}

static int cmp(const void *x, const void *y) { long a = *(const long *)x, b = *(const long *)y; return (a > b) - (a < b); }

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    double a = atof(argv[1]);
    const char *r = argv[2];
    int k = 3;
    if (!strcmp(r, "clip")) rule = CLIP; else if (!strcmp(r, "rclip")) rule = RCLIP;
    else if (!strcmp(r, "kvar")) rule = KVAR; else if (!strcmp(r, "kshared")) rule = KSHARED;
    else if (!strcmp(r, "recenter")) rule = RECENTER; else { fprintf(stderr, "rule\n"); return 1; }
    P1 = atof(argv[k++]);
    if (rule == RCLIP || rule == KVAR || rule == KSHARED) P2 = atof(argv[k++]);
    double eps = atof(argv[k++]); long n = atol(argv[k++]); uint64_t sd = strtoull(argv[k++], 0, 10);
    seed(sd);
    stack = malloc(sizeof(Box) * cap);
    tab = calloc(HSIZE, sizeof(Slot)); usedlist = malloc(sizeof(uint32_t) * HSIZE);
    long *T = malloc(sizeof(long) * n), capped = 0, nodecap = 2000000;
    double sum = 0, sum2 = 0; long m = 0;
    for (long i = 0; i < n; i++) {
        long t = run(a, eps, nodecap);
        clear_tab();
        if (t < 0) { capped++; continue; }
        T[m++] = t; sum += t; sum2 += (double)t * t;
    }
    qsort(T, m, sizeof(long), cmp);
    double mean = sum / m, sd2 = (sum2 - m * mean * mean) / (m - 1 > 0 ? m - 1 : 1);
    printf("{\"a\":%.17g,\"rule\":\"%s\",\"p1\":%g,\"p2\":%g,\"eps\":%g,\"n\":%ld,\"mean\":%.4f,\"sem\":%.4f,"
           "\"q50\":%ld,\"q90\":%ld,\"q99\":%ld,\"max\":%ld,\"capped\":%ld,\"seed\":%llu}\n",
           a, r, P1, P2, eps, n, mean, sqrt(sd2 / m), T[m / 2], T[(long)(0.9 * m)], T[(long)(0.99 * m)],
           T[m - 1], capped, (unsigned long long)sd);
    return 0;
}
