# Stage 2 lead assessment

Round 1 review reports are independent; the lead also read both sections and
checked the original matrix-function and composition statements, the
statistical parameter choices, and the witness/path formulas. The diagnostic
script passes independently. All five reports are complete; none identifies
a major issue. Every reported minor issue is accepted below.

## Accepted corrections

1. State the default worst-case query and success-at-least-2/3 convention for
   all lower bounds, including quantum lower bounds, with explicitly stated
   confidence and distributional expected-cost contracts taking precedence.
   Say relative error epsilon explicitly in the path theorem.
2. Repeat the statistical theorem's parameter range in the coherent counting
   corollary. At kappa=1 its lower bound would be false; the intended range
   kappa>=4 and epsilon<=1/128 is used throughout the actual proof.
3. Define an oracle-preserving realization quantitatively: every granted
   sparse count/location/value, vector, norm, and sampling request, and any
   granted factor request, has an O(1)-hidden-query simulation. All concrete
   examples already have this property. Use it in both abstract compilers.
4. State nonconstant partial inner functions when invoking distributions on
   both fibers. A constant function has an empty fiber and a zero lower
   bound. Every application is nonconstant.
5. Keep the rational lower bound informative at s=9 by replacing its base
   with max{4,(s-1)/8}; the actual power-of-four gate is at least this large.
6. Define second-kind Chebyshev polynomials and distinguish polynomial U_j
   from clock gates U_t by context or notation.
7. Write the rational generator's coefficient test explicitly with the
   normalizing factor a: a[(mI+h Jhat)^(-1)]_(i,j)>9 tau/10, at the
   appropriate queried positions. Its witness already satisfies this test.

These are minor scope, contract and exposition repairs: the intended
nontrivial theorem ranges and all concrete reductions retain their proofs.
No change to a proved exponent or statistical factor is needed.

## Lead-only audit correction

The initial assessment incorrectly said the qualified coherent numerical
output paragraph was absent. The fixer verified that it is present in
`04-lower-bounds.tex`, immediately before the statistical subsection, and
the lead withdrew the absence claim. Retain that paragraph. The original
inverse-quadratic-lower note already retains q_* in its numerical-output
comparison, so the author record must not present it as a newly repaired
source error. Stage 3a will integrate and check this existing comparison
within the full coherent-access discussion.

## Substantive source repair verified

The author corrected an actual edge case in the notes: n=24 placed the two
outer weights at zero and M, where the decision is easy. The manuscript's
n>=200 keeps them in a central interval and the linear randomized/noisy
outer complexity follows. The kappa>=1024 path threshold is a consistent
convenient consequence. This repair was made before Round 1 and has been
checked by the reviewers; it is not an outstanding major finding.

## Status

All five reports assessed. Separate fixer assigned to implement all seven
accepted corrections and the audit routing correction. No second review
round is required by the requested protocol because no major issue remains;
root will check each edit and validation before Stage 3a begins.
