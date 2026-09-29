/* Least guillotine certificate on a candidate grid, separable validity (review's own DP).
 * Box [x_a,x_b] x [z_c,z_d] is valid iff A[a][b] + B[c][d] >= thr.
 * Table T (uint8, saturating at 255 = "no certificate / too many") indexed
 * ((a*G1+b)*G2+c)*G2+d.  Intervals are processed by increasing x-length, then z-length,
 * so both halves of every cut are final when read.
 * Build: gcc -O2 -shared -fPIC -o libgdp8.so gdp8.c
 */
#include <stdint.h>
#include <stddef.h>

int gdp8(int G1, int G2, const double *A, const double *B, double thr, uint8_t *T)
{
#define ID(a,b,c,d) ((((size_t)(a)*G1+(b))*G2+(c))*G2+(d))
    for (int lx = 1; lx < G1; lx++)
        for (int lz = 1; lz < G2; lz++)
            for (int a = 0; a + lx < G1; a++) {
                int b = a + lx;
                double va = A[a * G1 + b];
                for (int c = 0; c + lz < G2; c++) {
                    int d = c + lz;
                    if (va + B[c * G2 + d] >= thr) { T[ID(a,b,c,d)] = 1; continue; }
                    int best = 255;
                    for (int k = a + 1; k < b; k++) {
                        int s = T[ID(a,k,c,d)] + T[ID(k,b,c,d)];
                        if (s < best) best = s;
                    }
                    for (int k = c + 1; k < d; k++) {
                        int s = T[ID(a,b,c,k)] + T[ID(a,b,k,d)];
                        if (s < best) best = s;
                    }
                    T[ID(a,b,c,d)] = (uint8_t)(best > 255 ? 255 : best);
                }
            }
    return T[ID(0, G1 - 1, 0, G2 - 1)];
#undef ID
}
