/* Schnorr-Euchner enumeration for min (z-c)^T A (z-c), z in Z^r, value < radius2.
   Input: mu (r x r, row-major, mu[k*r+j] for j > k), d (r), c (r).
   (z-c)^T A (z-c) = sum_k d_k (z_k - c_k + sum_{j>k} mu_kj (z_j - c_j))^2.
   shrink = 1: return the minimum (radius shrinks to the best value found).
   Returns number of nodes; *found = 1 if a point was found; best z in zbest;
   *complete = 0 if max_nodes was hit.
   Build: gcc -O2 -shared -fPIC -o libenum.so enum.c -lm */
#include <math.h>
#include <stdlib.h>

long se_enum(int r, const double *mu, const double *d, const double *c,
             double radius2, long max_nodes, long *zbest, double *bestval,
             int *found, int *complete)
{
    long *z = calloc(r, sizeof(long));
    long *step = calloc(r, sizeof(long));
    long *z0 = calloc(r, sizeof(long));
    int *sgn = calloc(r, sizeof(int));
    double *ctr = calloc(r, sizeof(double));
    double *part = calloc(r + 1, sizeof(double));
    double best = radius2;
    long nodes = 0;
    int k = r - 1;
    *found = 0; *complete = 1;
    part[r] = 0.0;
    /* initialise level k */
#define INIT(k) do { \
        double s_ = 0.0; \
        for (int j_ = (k) + 1; j_ < r; j_++) s_ += mu[(k) * r + j_] * ((double)z[j_] - c[j_]); \
        ctr[k] = c[k] - s_; \
        z0[k] = (long)floor(ctr[k] + 0.5); \
        sgn[k] = (ctr[k] >= (double)z0[k]) ? 1 : -1; \
        step[k] = 0; z[k] = z0[k]; \
    } while (0)
    INIT(k);
    for (;;) {
        nodes++;
        if (nodes > max_nodes) { *complete = 0; break; }
        double y = (double)z[k] - ctr[k];
        double val = part[k + 1] + d[k] * y * y;
        if (val < best) {
            if (k == 0) {
                for (int j = 0; j < r; j++) zbest[j] = z[j];
                *found = 1; best = val;
                /* next candidate at level 0 */
            } else {
                part[k] = val;
                k--;
                INIT(k);
                continue;
            }
        } else {
            /* candidates at this level are in increasing distance: go up */
            k++;
            if (k == r) break;
        }
        /* next zig-zag candidate at level k */
        step[k]++;
        {
            long off = (step[k] + 1) / 2;
            z[k] = z0[k] + ((step[k] % 2 == 1) ? off * sgn[k] : -off * sgn[k]);
        }
    }
    *bestval = best;
    free(z); free(step); free(z0); free(sgn); free(ctr); free(part);
    return nodes;
}
