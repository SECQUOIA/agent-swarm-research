# Root independent Stage 2 checks

I read the new parity proofs and the full joint section. The following checks
are independent of the five reviewer reports.

- The even-threshold compactness argument preserves evenness and global
  nonnegativity. Its positive-error contacts are nonempty because otherwise
  an upward constant perturbation improves the error. The existing pinned
  proof needs only finite degree, global nonnegativity, and contact slack,
  so its reuse is valid. The F2=F1 chord proof covers lower-degree cases.
- The degree-six witness has positive derivative as a cubic in z>=-1 and
  a positive value at -1. Its binomial tail is below 1/32; the unrestricted
  G1 lies strictly below 1/32 and F2 lies strictly above it.
- The odd lower uses a trigonometric Taylor remainder, so its derivative
  constants remain explicit as n grows. Exterior Chebyshev at the zero
  forces a remainder of order Rbar^-n; n proportional to log(1/delta)
  therefore yields the extra logarithm. The upper checks the transition
  region and does not assume an unjustified monotone sign approximant.
- In the exterior joint lower, retaining the sine Taylor polynomial avoids
  an O(delta^2) rescaled-target error. The negative-angle inequality remains
  valid when n is much larger than delta^-2; the negative affine intercept
  only strengthens it. Factorial remainders control arbitrarily large n.
- The Fejer--Riesz finite-index endpoint argument uses K<G1<G0, making its
  difference of square roots uniformly positive. The fixed-radius branch
  excludes T<r+1 without a growth restriction on r. The margin comparison
  correctly applies the finite-index theorem at r-1.
- In the growing upper, the outer linear term is O(r^2*2^(2r)/k)=o(1),
  and the outer degree-2r term is controlled by a fixed large leading
  constant in k. The high-band exponents n+2-4/n and 3-4/n follow directly
  from k>=A*delta^(-1+1/n). Exponential-in-n factors are harmless under
  n=o(log(1/delta)), and are not incorrectly hidden in fixed constants.
- The additive log(1/delta) in the growing upper is negligible for r>=2.
  Away from an upper tier boundary, the root of the threshold margin is
  bounded below. The remaining r^2 factor is stated honestly.
- I inspected the diagnostic figure and script. The script computes the
  same positive series and pinned signed-error identity as the manuscript;
  it is appropriately described as a floating-point diagnostic, not a
  certificate of global contractivity.

Assessment and any repairs are recorded separately after all five reviews.
