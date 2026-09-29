/* Review code: exact-model branch-and-bound on the McCormick kink family (c = -1),
 * robust-branching.md Section 5. Independent of the author's sim_kink.py.
 *
 * A box is open iff lx < a < ux and wy (a-lx)(ux-a)/wx > eps. At an open box the relaxation point
 * is (a, ly + rho wy), rho = (a-lx)/wx. Selection: widest side, ties to x ("w"), or x only ("x").
 *
 * rules (applied to both coordinates):
 *   clip T        fixed clamp T
 *   rc T          recentring clamp T
 *   rclip T0 T1   theta ~ U[T0,T1] independently at every split
 *   kvar T0 T1    theta keyed on (variable, interval): one draw per distinct interval of each variable
 *   kshared T0 T1 theta keyed on the interval only, shared by x and y (as in the author's sim_keyed.py)
 *
 * usage: mc2d SEL RULE P1 [P2] A EPS NRUNS SEED
 * prints: mean sem q50 q90 q99 max ncapped
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static uint64_t rng_state;
static inline uint64_t splitmix64(uint64_t *x) {
    uint64_t z = (*x += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
static inline double u01(void) { return (splitmix64(&rng_state) >> 11) * (1.0 / 9007199254740992.0); }
static inline uint64_t dbits(double v) { uint64_t b; memcpy(&b, &v, 8); return b; }
static inline double keyed(uint64_t runseed, uint64_t var, double l, double u) {
    uint64_t h = runseed ^ (var * 0x9E3779B97F4A7C15ULL);
    uint64_t s = h;
    s ^= splitmix64(&h) ^ dbits(l);
    s = splitmix64(&s) ^ dbits(u);
    uint64_t z = splitmix64(&s);
    return (z >> 11) * (1.0 / 9007199254740992.0);
}

enum { CLIP, RC, RCLIP, KVAR, KSHARED };
static int rule; static double P1, P2; static uint64_t runseed;

static double point(int var, double p, double l, double u) {
    double w = u - l, th;
    switch (rule) {
    case RC:
        th = P1;
        if (p < l + th * w) return l + fmax(th * w, 2 * (p - l));
        if (p > u - th * w) return u - fmax(th * w, 2 * (u - p));
        return p;
    case CLIP: th = P1; break;
    case RCLIP: th = P1 + (P2 - P1) * u01(); break;
    case KVAR: th = P1 + (P2 - P1) * keyed(runseed, (uint64_t)var + 1, l, u); break;
    case KSHARED: th = P1 + (P2 - P1) * keyed(runseed, 0, l, u); break;
    default: abort();
    }
    return fmin(fmax(p, l + th * w), u - th * w);
}

typedef struct { double lx, ux, ly, uy; } Box;

static long run(double a, double eps, int widest, long cap) {
    static Box *st = NULL; static long cap_st = 0;
    if (!st) { cap_st = 1 << 16; st = malloc(sizeof(Box) * cap_st); }
    long n = 0, T = 0;
    st[n++] = (Box){0, 1, 0, 1};
    while (n) {
        Box b = st[--n];
        T++;
        if (T > cap) return -1;
        if (!(b.lx < a && a < b.ux)) continue;
        double wx = b.ux - b.lx, wy = b.uy - b.ly;
        if (wy * (a - b.lx) * (b.ux - a) / wx <= eps) continue;
        double rho = (a - b.lx) / wx;
        if (n + 2 >= cap_st) { cap_st *= 2; st = realloc(st, sizeof(Box) * cap_st); }
        if (!widest || wx >= wy) {
            double s = point(0, a, b.lx, b.ux);
            st[n++] = (Box){b.lx, s, b.ly, b.uy};
            st[n++] = (Box){s, b.ux, b.ly, b.uy};
        } else {
            double s = point(1, b.ly + rho * wy, b.ly, b.uy);
            st[n++] = (Box){b.lx, b.ux, b.ly, s};
            st[n++] = (Box){b.lx, b.ux, s, b.uy};
        }
    }
    return T;
}

static int cmp(const void *x, const void *y) {
    long a = *(const long *)x, b = *(const long *)y;
    return (a > b) - (a < b);
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage\n"); return 1; }
    int k = 1;
    int widest = strcmp(argv[k++], "w") == 0;
    const char *r = argv[k++];
    if (!strcmp(r, "clip")) rule = CLIP; else if (!strcmp(r, "rc")) rule = RC;
    else if (!strcmp(r, "rclip")) rule = RCLIP; else if (!strcmp(r, "kvar")) rule = KVAR;
    else if (!strcmp(r, "kshared")) rule = KSHARED; else return 2;
    P1 = atof(argv[k++]);
    if (rule == RCLIP || rule == KVAR || rule == KSHARED) P2 = atof(argv[k++]);
    double a = atof(argv[k++]), eps = atof(argv[k++]);
    long nruns = atol(argv[k++]);
    uint64_t seed = strtoull(argv[k++], NULL, 10);
    rng_state = seed * 0x2545F4914F6CDD1DULL + 1;
    long *Ts = malloc(sizeof(long) * nruns);
    long capped = 0, cap = 200000000L;
    double sum = 0, sum2 = 0;
    long m = 0;
    for (long i = 0; i < nruns; i++) {
        runseed = splitmix64(&rng_state);
        long T = run(a, eps, widest, cap);
        if (T < 0) { capped++; continue; }
        Ts[m++] = T; sum += T; sum2 += (double)T * T;
    }
    qsort(Ts, m, sizeof(long), cmp);
    double mean = sum / m, sd = sqrt(fmax(0, sum2 / m - mean * mean) * m / (m > 1 ? m - 1 : 1));
    printf("%.4f %.4f %ld %ld %ld %ld %ld\n", mean, sd / sqrt((double)m), Ts[(long)(0.5 * m)],
           Ts[(long)(0.9 * m)], Ts[(long)(0.99 * m)], Ts[m - 1], capped);
    return 0;
}
