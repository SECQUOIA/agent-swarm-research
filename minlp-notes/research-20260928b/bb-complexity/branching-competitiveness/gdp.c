/* Exact minimum guillotine certificate on a 2D candidate grid.
 *
 * Grid lines x_0 < ... < x_{G1-1} and z_0 < ... < z_{G2-1}.  A box is
 * [x_a, x_b] x [z_c, z_d].  valid(a,b,c,d) is supplied as a byte table
 * V[((a*G1 + b)*G2 + c)*G2 + d] (only a<b, c<d used).  Returns the least
 * number of leaves of a guillotine partition of the whole grid box into
 * valid grid boxes (cuts only on grid lines), or -1 if none exists.
 * Compile: gcc -O2 -shared -fPIC -o libgdp.so gdp.c
 */
#include <stdlib.h>
#include <string.h>

#define IDX(a, b, c, d) ((((size_t)(a) * G1 + (b)) * G2 + (c)) * G2 + (d))

int guillotine_dp(int G1, int G2, const unsigned char *V, int *out_root)
{
    const int INF = 1 << 29;
    size_t n = (size_t)G1 * G1 * G2 * G2;
    int *N = (int *)malloc(n * sizeof(int));
    if (!N) return -2;
    for (int w1 = 1; w1 < G1; w1++)
        for (int w2 = 1; w2 < G2; w2++)
            for (int a = 0; a + w1 < G1; a++)
                for (int c = 0; c + w2 < G2; c++) {
                    int b = a + w1, d = c + w2;
                    size_t id = IDX(a, b, c, d);
                    if (V[id]) { N[id] = 1; continue; }
                    int best = INF;
                    for (int k = a + 1; k < b; k++) {
                        int s = N[IDX(a, k, c, d)] + N[IDX(k, b, c, d)];
                        if (s < best) best = s;
                    }
                    for (int k = c + 1; k < d; k++) {
                        int s = N[IDX(a, b, c, k)] + N[IDX(a, b, k, d)];
                        if (s < best) best = s;
                    }
                    N[id] = best;
                }
    int r = N[IDX(0, G1 - 1, 0, G2 - 1)];
    *out_root = r >= INF ? -1 : r;
    free(N);
    return 0;
}
