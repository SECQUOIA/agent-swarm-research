# Stage 1, round 1: independent review 1

Reviewed `sections/02-model.tex`, `sections/03-exact.tex`, and
`sections/04-fixed-accuracy.tex` in full, together with the four Stage 1 source
notes listed in `audit/source-map.md`. I did not read other reviewer reports.
Joint accuracy, the LP application, and the full introductory literature review
are outside this review's scope.

**Result: 0 major issues and 1 minor issue.** The Stage 1 results and their
query exponents appear correct. The minor issue is a proof-scope clarification;
it does not change a theorem or the staircase.

## Finding

### R1.1 — Minor: justify the definite-parity statement for the full stated domain

**Location:** `sections/02-model.tex:17–20`, bounded polynomial implementation
lemma and its first proof paragraph.

The lemma covers every Hermitian contraction, and claims exactly `d` queries
for definite parity. Its explanation of the QSVT-to-eigenvalue step only says
that the applications are positive semidefinite. This establishes that step
for the applications, but leaves the stated general Hermitian case unstated.
The subsequent walk construction proves the general `O(d)` claim, rather than
the exact `d`-query assertion.

**Repair:** replace the PSD-only sentence with the general observation. For an
even polynomial, QSVT gives `p(|H|)=p(H)`; for an odd polynomial, the left/right
singular-vector signs give `sign(H)p(|H|)=p(H)`, with the zero eigenspace handled
by `p(0)=0`. Alternatively state the lemma only for PSD contractions, although
the general observation is preferable and costs one sentence. The cited source
also explicitly identifies singular-value and eigenvalue transformation for
Hermitian matrices in its discussion preceding Theorem 56.

## Substantive checks

- **Oracle completion and implementation.** The hermitianization has compressed
  block `(H+H*)/2=H` for every completion. On each walk subspace, the displayed
  walk matrix and its Hermitian part are correct. The centered polynomial
  `z^d p((z+z^-1)/2)` has degree at most `2d` and is bounded by one on the unit
  circle. Applying GQSP and then the inverse walk power therefore preserves
  unit normalization and uses `O(d)` original controlled queries. I found no
  hidden promise about the completion, postselection, or normalization loss.
- **All-circuit lower bounds.** Oracle-independent gates, controlled queries,
  and fixed output isometries preserve trigonometric degree at most the query
  count. Unitarity outside the correctness promise supplies the nonnegativity
  needed by the Taylor limit. The coefficient compactness argument is valid;
  pointwise convergence on each fixed real argument suffices to establish
  global nonnegativity of the limit. Odd-degree exclusion gives exactly the
  claimed exponent. The model's reusable-unitary and bounded worst-case
  assumptions are material and stated.
- **Exact and pairwise results.** The quadratic's endpoint bounds and error
  factorization are correct. The identity-theorem argument rules out finite
  exact conversion on an open interval for positive normalization below two.
  The approximate pairwise argument correctly allows complex output amplitudes:
  the complementary-norm bounds `sqrt(17 delta/8)` and
  `sqrt(93 delta/32)` follow from the stated error tolerance. The differentiated
  bound has the correct factors of the normalization. Its interpretation is
  appropriately qualified by exact impossibility.
- **Threshold formula and asymptotics.** Exterior Chebyshev extremality gives
  the lower bound on `G_r`. The negative-lobe estimate in the admissibility
  proof is sufficient, including large fixed band ratios. The stationary point
  is unique, successive thresholds strictly decrease, and the first-threshold
  formula is consistent with the extremizer. Expanding the stationary equation
  gives `t-a=1/(2r)+O(r^-2)` and the stated prefactor. Integer rounding is
  correctly retained as `O(1)` in the inverse formula.
- **Exact threshold construction.** The paired shifted kernels yield an even
  algebraic polynomial; periodicity and evenness remove the apparent
  square-root dependence. The tail estimate remains valid near both endpoints
  of `[-1,1]`. Global contractivity follows from the three-region split. On the
  low band, the extra two powers in the pinning estimate dominate every contact
  multiplicity and give the signed-error inequality even at contacts. On the
  high band, the loss term is indeed `O(delta^(4-2/r))=o(delta)`. Thus the proof
  achieves the exact threshold error, rather than an asymptotic overshoot.
- **Coarse tier.** The logarithmic interpolation lower bound has the correct
  Lagrange denominators and factorial estimate. It needs a positive-length high
  interval. The manuscript correctly separates `c=1`; the displayed quartic
  stays contractive, pins the low endpoint, vanishes at one, and achieves the
  coarse threshold itself. This repairs the overbroad coarse-tier claim in the
  source staircase note.
- **Parity separation.** The affine minimax constant, second Markov constant,
  and odd-parity Bernstein bound are correct. The squared Fejer construction
  gives the stated first-order coefficient after integer rounding and
  `O(delta^2)` high-band leakage. The final comparison is properly restricted
  to one definite-parity transform; it makes no unsupported claim about
  arbitrary QSVT compositions.

## Reference and numerical checks

I checked the implementation reference against [Gilyén et al., Corollary 18
and Theorem 73](https://arxiv.org/pdf/1806.01838). Corollary 18 provides the
bounded real definite-parity transform with coherent real-part extraction;
Theorem 73 supplies the attributed pairwise lower-bound method. The manuscript
does not mistake that pairwise method for the stronger Taylor-limit hierarchy.
I also checked [Motlagh–Wiebe, Theorems 3–4 and Corollary
5](https://doi.org/10.1103/PRXQuantum.5.020368): bounded ordinary polynomials on
the unit circle admit the completion used here. These references are relevant
and sufficient for the implementation claims reviewed here; a broad priority
assessment remains outside Stage 1.

As supplemental checks, a script run with
`/home/sgusev/miniconda3/envs/qipm/bin/python` tested the threshold formulas for
`rho` in `{1.01, 2, 10, 100}` and orders `r=1,...,6`, including sampled global
positivity, low-band error, strict threshold decrease, and the explicit first
threshold. All 24 cases passed. It also tested the `c=1` coarse quartic at the
exact threshold for those four ratios and three small positive values of
`delta`; all 12 cases passed. These numerical checks supplement the analytic
review and are not proof certificates.
