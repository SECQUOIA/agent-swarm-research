"""Confirmation check c3: lowest eigenvalue of an m-stage Toeplitz section with
a symbol that has a quadratic minimum at pi, f(pi) + (1/2) f''(pi) (pi/(m+1))^2
(Dirichlet-type ends), against the Hessian eigenvalues logged in
theory-bangbang/singular/logs/revision_catmix_C.log (log(J+1) units).
Symbol values from c1_symbol_independent.log."""
for N, m, obs_ref, obs_saddle, fpi_h3, f2_h3 in ((100, 59, -2.6178e-08, -3.3020e-08, -0.027286, 0.79058),
                                                 (200, 118, -3.3749e-09, -4.2154e-09, -0.027286, 0.79057)):
    h = 1.0 / N
    fpi, f2 = fpi_h3 * h ** 3, f2_h3 * h ** 3
    est = fpi + 0.5 * f2 * (3.141592653589793 / (m + 1)) ** 2
    print("N=%d m=%d f(pi)=%.4e finite-section estimate=%.4e smooth-reference min eig=%.4e (ratio %.4f); "
          "oscillating saddle min eig=%.4e (ratio %.3f)" % (N, m, fpi, est, obs_ref, obs_ref / est, obs_saddle,
                                                             obs_saddle / est))
