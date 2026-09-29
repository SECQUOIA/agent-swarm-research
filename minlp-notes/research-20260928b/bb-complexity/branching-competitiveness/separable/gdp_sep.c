/* Exact least guillotine certificate on a 2D candidate grid for SEPARABLE validity.
 * Box [x_a,x_b] x [z_c,z_d] is valid iff V1[a*G1+b] + V2[c*G2+d] >= thr
 * (the caller passes V1 = F_1 values, V2 = F_2 values, thr = -eps + guard).
 * N is a uint16 table of size G1*G1*G2*G2; returns the root value (65535 = none).
 * Compile: gcc -O2 -shared -fPIC -o libgdp_sep.so gdp_sep.c
 */
#include <stdlib.h>
#include <stdint.h>
#define IDX(a,b,c,d) ((((size_t)(a)*G1+(b))*G2+(c))*G2+(d))
int gdp_sep(int G1, int G2, const double *V1, const double *V2, double thr, uint16_t *N)
{
    const uint16_t INF = 65535;
    for (int w1 = 1; w1 < G1; w1++)
     for (int w2 = 1; w2 < G2; w2++)
      for (int a = 0; a + w1 < G1; a++) {
        int b = a + w1;
        double f1 = V1[a*G1+b];
        for (int c = 0; c + w2 < G2; c++) {
          int d = c + w2;
          size_t id = IDX(a,b,c,d);
          if (f1 + V2[c*G2+d] >= thr) { N[id] = 1; continue; }
          unsigned best = INF;
          for (int k = a+1; k < b; k++) {
            unsigned s = (unsigned)N[IDX(a,k,c,d)] + N[IDX(k,b,c,d)];
            if (s < best) best = s;
          }
          for (int k = c+1; k < d; k++) {
            unsigned s = (unsigned)N[IDX(a,b,c,k)] + N[IDX(a,b,k,d)];
            if (s < best) best = s;
          }
          N[id] = best > INF ? INF : (uint16_t)best;
        }
      }
    return N[IDX(0,G1-1,0,G2-1)];
}
