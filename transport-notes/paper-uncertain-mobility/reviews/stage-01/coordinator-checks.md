# Coordinator's independent Stage 01 checks

Date: 2026-09-07. These checks supplement, and do not replace, the five independent reviews. They concern the frozen Round 01 manuscript.

- Integration by parts in the coupled energy gives `Db partial_n f = K k(v-f_trace)` and wall generator `(D v')' + k(f_trace-v)`. The forward boundary loss is the stated adsorption-minus-desorption flux. The equilibrium measure and forcing satisfy `integral_bulk(u-V)=KPV`.
- Eliminating the surface variable gives constant term `KV^2 J`, cross term `-2KV integral(kh f_trace)`, and negative residual `-K S`. Dividing by `Z` produces the stated prefactor. Both the linear load and surface residual are invariant under the common constant gauge.
- In the finite-J energy completion, `||sqrt(k)h||_2^2 <= J`, so `||w||_2^2 <= k_max J`; thus the bulk load is bounded for each finite-J design. The completion argument does not need an L2 representative of h, and both sources vanish on zero-energy equivalence classes.
- The finite-time spectral integrand is `(1-exp(-lambda*t))/lambda - [1-exp(-lambda*t)*(1+lambda*t)]/(t*lambda^2)`, equivalently `1/lambda-(1-exp(-lambda*t))/(t*lambda^2)`. Its derivative in t is nonnegative. At lambda=0 it equals t/2, so trapped components with nonzero centered velocity correctly give infinite dispersion.
- A positive mobility floor controls the ordinary H1 derivative even for an unbounded L1 coefficient. The closure argument uses finiteness of D almost everywhere, not an unavailable coefficient upper bound.
- The Fourier estimate uses normalized mass one and positivity to bound each coefficient, while Parseval controls the high-frequency tail. Squaring the H^(-1/2) bound yields one logarithm in the bulk remainder, rather than a squared logarithm.
- For any information law the field mixture preserves the exact per-observation budget and is a continuous affine map in L1. Class inclusion gives the lower bound in the correct direction. Near-minimizing policies suffice for the upper bound; no measurable optimizer selection is used.
- The q<1 inequality uses subadditivity. The cosine bump applies pointwise to every field and offset in an event of probability 1/4, even when the field depends on that offset. Its energy scales as M/ell^2+ell^3 and numerator as ell^2, giving ell=M^(1/5).
- Dimensional conversion gives J_phys=(ell_ref/k_ref)J and chi_phys J_phys in units L^2/T. Surface longitudinal molecular diffusion with the isotropic choice adds KM/Z, which is bounded as M tends to zero.

No coordinator-identified mathematical defect is presently outstanding. Reviewer findings remain to be adjudicated. In final synthesis, the technical form material may be moved to an appendix to improve the reading order without shortening needed proofs.
