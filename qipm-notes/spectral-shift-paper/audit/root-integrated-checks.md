# Root integrated proof and presentation check

I independently re-read every manuscript section after the Stage 4 freeze,
including all proofs in Sections 2–6, and compared the introduction and
conclusion against their precise parameter and oracle contracts. This pass
supplements the earlier root checks; it does not replace the required five
fresh whole-manuscript reviews.

- The general-parity implementation handles arbitrary completions by
  Hermitianization and a Laurent-polynomial walk reduction. The exact
  interval obstruction uses analyticity outside the correctness interval,
  where unitarity still applies.
- The exterior Chebyshev extremizer is nonnegative on all real inputs,
  including its negative Chebyshev lobes. The Taylor-limit lower bound
  uses compactness of coefficients and global nonnegativity of the limit,
  rather than asserting positivity of each Taylor truncation.
- Contact pinning controls the sign of the error at equality. The coarse
  constructions distinguish a high interval from the singleton high point.
  The even plateau proof uses convexity on the squared variable; the
  degree-six witness and odd logarithmic lower bound justify the table.
- The exterior joint proof keeps the sine target and factorial remainder.
  The independent square-factor proof treats both fixed and adaptive
  Cauchy radii. The growing-index upper explicitly retains exponential
  tail factors and controls both gate and polynomial terms on the high
  band. The intermediate result preserves its margin factor and does not
  claim a uniformly matched multiplicative law.
- The LP construction has the stated exact central point and a nontrivial
  feasible segment. Its dual direction, rather than its public primal
  direction, varies with the hidden parameter. The state lower bound
  counts every supplied oracle, and amplitude estimation gives the stated
  matching upper bounds. The compiler has a separate matrix-only contract,
  including the zero-query shortcut from public projectors.
- The abstract, figure, related-work distinctions, conclusion, and source
  ledger preserve these qualifications. All eight relevant theorem notes
  have explicit coverage or correction entries. The source package uses
  relative paths and includes the required figure and bibliography.

No new mathematical or presentation issue was identified in this pass.
The Stage 4 frozen-file checksum verification passed for every recorded
source and artifact. The unrelated concurrent `scalar-newton-paper/`
directory was not modified by this work.
