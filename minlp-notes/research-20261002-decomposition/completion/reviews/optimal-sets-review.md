# Independent optimal-set implementation review

Date: 2026-10-03. Scope: `solver/optimal_sets.py` and
`solver/verify_optimal_sets.py`, with inspection of the shared finite-grid DP,
rational LP interface, endpoint optimal-set identity, proximal-grid theorem,
and stationary-polytope exact-recovery lemma. This review did not run
project-wide verification or inspect CI.

**Result:** no unresolved certificate-soundness or mathematical-completeness
defect was found in the reviewed scope. The producer and verifier now implement
the two stated certificate classes. This conclusion does not establish general
unknown-optimal-set discovery or practical performance at large width.

## Findings and resolution

The first version did not pass the runtime budget into the exact LP oracle.
A lengthy selected-face recovery LP could therefore ignore the discovery
time limit. The author added a budget callback to the LP and independent
diagonal/PSD verifier. Inspection confirmed that budget exceptions propagate
to the producer's inconclusive status rather than becoming successful or
infeasible results. Targeted tests cover time, table, stage, and LP-pivot stops.

The selected-face LP implementation uses capped rational simplex. The theorem
allows a polynomial-time rational LP algorithm, but this particular simplex
implementation has no polynomial worst-case guarantee. The implementation
therefore supplies exact certificates and the stated finite search schedule;
its practical runtime should not be described as an implementation-level proof
of the theorem's FPT bit complexity.

## Mathematical and implementation checks

- Endpoint messages use consistent sorted separator labels even when bag
  orders differ and the decomposition branches. Local residuals are exact,
  nonnegative Bellman differences; each separator state attains zero residual.
  The verifier reconstructs the original factor assignment and checks both
  these properties, plus an attaining feasible point.
- Endpoint full-set membership enforces strict-negative-diagonal endpoint
  conditions and the support of every positive Bellman residual. Integer
  interior labels are retained precisely when they satisfy those equations.
  A fixed coordinate contributes no interpolation variance and may have
  positive diagonal curvature.
- Diagonal acceptance checks original box KKT and the exact maximal shift,
  then tests PSD including singular pivots with nonzero off-diagonal entries.
  Its kernel and endpoint-product equations describe every optimizer through
  the exact nonnegative identity. No guessed growth bound enters acceptance.
- Discovery minimizes the actual corrected proximal objective. Passing signed
  penalties into the shared DP is valid because the DP subtracts them as unary
  factors and never assumes their sign. Fresh boxes intersect the original
  box, and every trial restarts at the original lower endpoint vector.
- The conditioning, radius, proximal coefficient, target accuracy, and final
  stage agree with the earlier proximal/recovery proof. Fixed rational
  coordinates are substituted before computing the recovery height denominator.
  The selected-face LP uses original coefficients and original bounds, so
  rational grid coordinates do not enter its stationary equations.
- A false conditioning guess can converge to a nonglobal local minimum. The
  implementation rejects that candidate through independent diagonal PSD
  acceptance and returns no global certificate on the tested one-trial stop.

## Reproducible targeted checks

Run from the repository root:

```sh
python3 -B research-20261002-decomposition/completion/reviews/check_optimal_sets_review.py
```

The command passed in under one second on this run. It checks:

- 150 exact PSD decisions against the separate all-principal-minors criterion;
- 2,016 mixed endpoint-set membership comparisons against exact objective
  equality on 24 branching, permuted-bag QPs, including fixed positive diagonal
  coordinates and interior integer labels;
- 24 signed-penalty DP minima and every associated unary min-marginal against
  exhaustive finite-grid enumeration;
- 24 tampered Bellman residual rejections;
- 250 full-set membership checks for tilted, disconnected optimal continua;
- a complete invalid-conditioning trial on the documented proximal trap,
  with its final nonglobal candidate rejected;
- a complete final-stage rational LP recovery trial after fixed-coordinate
  substitution, with exact optimizer `(6/13, 1/13)`;
- five resource-limit status checks with no successful certificate attached.

These are bounded correctness checks, not speed or scalability benchmarks.
