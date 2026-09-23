# Root review of the sharp positive-multilinear growth theorem

Date: 2026-09-04. Reviewed the full written version of
`results/positive-multilinear-sharp-degree-growth.md`, including its optimized
mixture and the nonnegative-box extension. This is an internal independent
mathematical review; publication priority is assessed separately.

No mathematical defect was found. The root independently reconstructed the
harmonic normalization, gain estimates, and leading-constant refinement from
the first candidate derivations, then read the complete proof.

The key checks are:

- The deficiency representation uses simultaneous comonotone attainment of
  every positive monomial's concave envelope. All deficiencies are pointwise
  nonnegative, so mixing couplings cannot lose contributions from other terms.
- Every coupling is global, depending on the marginal vector and degree bound,
  rather than on an individual monomial. The harmonic conditional failure
  probability integrates exactly to the prescribed failure marginal, including
  its cutoff at one; zero failure probability is handled separately.
- For a unique-low-anchor term, the inactive failure mass is at most rt/M<=t.
  The refined integration interval lies inside the anchor's active interval.
  The lower bound on the sum of conditional failure probabilities is at most
  1/(ln L)^2 there, which justifies the quadratic exponential estimate even
  if the actual sum is larger.
- The interval's logarithmic length is b-3 ln b. With b>=6 it is positive.
  The stated h is therefore valid and positive. The inverse-guarantee mixture
  weights yield one uniform guarantee T/Z for every term, with
  Z=1/h+L/b^2+2/(1-exp(-1)) asymptotic to L/ln L.
- The audited dyadic lower family has degree 2^(ell-1)+1 and ratio
  ell/log_2 ell asymptotically. Selecting the largest admissible ell gives the
  same leading constant for every sufficiently large degree bound, not merely
  a subsequence. Dimension padding establishes the corresponding n-variable
  supremum.
- The extension to a finite nonnegative box compares the original, unexpanded
  term-by-term gap with that of the positive expansion. Concave envelopes add
  by comonotonicity; convex-envelope superadditivity gives the required
  inequality in the correct direction. Fixed coordinates are removed first.

Thus the worst ratio, by degree or by dimension, is asymptotic to ln t/ln ln t.
This conclusion includes a leading constant of one. It does not determine the
exact finite-degree optimum or give an oracle for evaluating convex envelopes.

Two separate agents also reviewed the proof. The lower construction and exact
finite-family formula have separate independent audits. A failed literature
search does not itself establish novelty.
