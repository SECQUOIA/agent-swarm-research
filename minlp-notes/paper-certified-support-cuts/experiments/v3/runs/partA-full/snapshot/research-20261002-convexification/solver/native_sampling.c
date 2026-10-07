/* Floating-point candidate sampling only; this code does not certify cuts. */
#include <stddef.h>
#include <stdlib.h>

int sample_polynomials(
    size_t npoints, size_t ndim, size_t nfeatures,
    const double *points, const size_t *offsets, const double *coefficients,
    const unsigned int *xexponents, const unsigned int *yexponents,
    unsigned int xdegree, unsigned int ydegree, double *output)
{
    size_t nx = (size_t)xdegree + 1;
    size_t ny = (size_t)ydegree + 1;
    double *powers = malloc((nx + ny) * sizeof(double));
    if (powers == NULL) return 1;
    double *xp = powers;
    double *yp = powers + nx;
    xp[0] = yp[0] = 1.0;
    for (size_t i = 0; i < npoints; ++i) {
        double x = points[i * ndim];
        double y = ndim == 2 ? points[i * ndim + 1] : 0.0;
        for (unsigned int d = 1; d <= xdegree; ++d) xp[d] = xp[d - 1] * x;
        for (unsigned int d = 1; d <= ydegree; ++d) yp[d] = yp[d - 1] * y;
        for (size_t j = 0; j < nfeatures; ++j) {
            double value = 0.0;
            for (size_t k = offsets[j]; k < offsets[j + 1]; ++k)
                value += coefficients[k] * xp[xexponents[k]] * yp[yexponents[k]];
            output[i * nfeatures + j] = value;
        }
    }
    free(powers);
    return 0;
}
