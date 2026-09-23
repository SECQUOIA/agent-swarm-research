# Stage 3, round 1: independent review 4

Date: 2026-09-22. Scope: all newly authored consequences, hypothesis examples,
application, rational supplement, and their literature/coverage records. I read
the author report and snapshot, both new sections, the full application appendix,
the entire exact-check script, bibliography additions, literature followups,
and coverage mapping. I did not read another current review or alter sources.

## Verdict

Accept stage 3. No major or minor mathematical, application-validity, citation,
or reproducibility issue identified. Later frontier mathematics and the deferred
formal-consequences integration remain outside this verdict.

## Application review

- The local underestimator proof uses nonnegative inequality weights, so its
  sign direction is correct. Global validity of the aggregate comes from the
  original globally active rows; it does not depend on estimator validity
  outside the box. Positive box margin proves exclusion without any curvature
  assumption. PSD is used only for convexity and global tangent validity.
- The tangent claims distinguish separation of its expansion point from
  exclusion of the entire box. At a constrained minimizer, the first-order
  inequality has the required nonnegative sign for every box displacement,
  even when the minimizer is on the boundary.
- The DD LP projects exactly onto normalized symmetric diagonally dominant
  matrices with nonnegative diagonals: each absolute-value auxiliary can be
  set to its actual absolute value. The box-support auxiliaries are lower
  bounds on the negative parts, and nonnegative box widths preserve the
  lower-bound direction. Setting them to the negative parts attains the exact
  box minimum. Degenerate box widths cause no mathematical problem.
- The weighted-square identity proves PSD with the correct off-diagonal
  factor. Rational verification of nonnegative coefficients and margin is
  sufficient; the paper does not overstate diagonal dominance as necessary.
- Signed affine equalities are correctly added exactly to both expressions.
  The combined positive/negative-part normalization bounds their coefficients
  and allows equality-only certificates. The stated unbounded-margin example
  when only inequality weights are normalized is valid. Restricting this
  paragraph to affine equalities avoids invalid signed underestimation.
- Conditional rows retain the conjunction of their activation conditions.
  The appendix does not confuse an implication valid under those conditions
  with an unconditional inequality.
- I independently recalculated the rational example: both estimator
  factorizations, matrix determinants, sum-of-squares aggregate, value and
  gradient at `(1/5,1/5)`, tangent `x+y <= 7/20`, root lifted witness, and
  individual activation witnesses agree with the manuscript.
- The DD conditions reduce to `1/5 <= a <= 5/7`; the first affine coefficient
  changes sign at `5/9`. The two minimum formulas agree there and are increasing.
  The optimum is indeed `(5/7,2/7)` with margin `1/35`; the normalized
  illustrative margin is `7/300`. The paper compares matching normalizations.
- A PSD zero-diagonal matrix must vanish, establishing the purely bilinear
  limitation. A common Shor lift implies every PSD aggregate and its tangent;
  the example correctly claims improvement only over the complete termwise
  relaxation, not over that common lift.

## Other mathematical checks

The closed-system properness equivalence uses only inclusion and a proper
closed convex aggregate sublevel set; it does not assume density of the strict
feasible set. The three-regime corollary has the correct separate dimensions
for HHC-to-HC and the cited full hull description. The trace objective and
two signed objectives per linear coordinate exactly detect triviality on the
compact simplex slice, with infeasibility treated separately.

For the Shor result, the image-plus-orthant cone is correctly allowed to be
nonclosed. Its dual and bipolar relation have the right signs. The interior
addition argument is valid, and the quadratic mixing identity has a positive
covariance term in the cone. It proves closure equality; extrapolation followed
by a midpoint proves actual whole-space membership in the trivial-certificate
case. Thus no illicit inference from dense projection to full projection is
made. Both nonclosed-projection descriptions, endpoint exclusions, covariance
witnesses, and strict points check out. The four-row original closed set is
compact, while its projection remains nonclosed.

The stable-convexity implication follows from the displayed perturbation
formula. The A-versus-Q PDLC qualification correctly uses a strictly negative
constant certificate and the Schur complement. I checked both stable/HHC
nonimplication examples, the ordinary-HC full-image parameterization and
injective hyperplane obstruction, its three-row affine bound, the closed
counterexample's full-dimensional interior and two negative eigenvalues, and
the strip example's factored strict interval and Shor witness. No sign,
dimension, or missing-feasibility gap was found.

## Sources and supplement

I inspected the local primary Dong and Berthold--Witzig text around their
aggregation statements, which support the modest historical attributions.
I also read the relevant Fujie--Kojima Condition 1.2/1.4 and Theorem 2.1
excerpts and Kojima--Tuncel Theorem 4.2 in the retrieved primary texts.
The paper proves its own closure result and correctly avoids importing the
latter's unqualified equality. The compact example meets the standing
compactness qualification, rather than relying solely on the unbounded one.

Sheriff's actual neighborhood-based stable-convexity definition matches the
manuscript. I opened the [author-uploaded Polyak paper](https://www.researchgate.net/publication/226667003_Convexity_of_Quadratic_Transformations_and_Its_Use_in_Control_and_Optimization);
its web extraction is imperfect, as already recorded. The used three-real-form
implication is the classical one, also given in the previously inspected BDS
primary text. No new priority claim is attached to these results.

The rational script checks coefficient dictionaries for the displayed
polynomial identities, rather than merely evaluating a grid. Its lift checks
are finite exact witnesses and are accurately described as such; universal
validity is supplied by the accompanying mathematical proofs. The small
geometric arithmetic checks do not certify HHC and are not represented as
doing so. All mapped stage 3 developments have manuscript destinations.

## Targeted commands actually run

I used `cat`, `rg --files`, targeted `rg -n`, and `sed -n` for the source and
literature reads described above. From `paper-quadratic-aggregation/`:

```sh
python3 supplement/check_examples.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/quadratic-stage03-review4 main.tex
rg -n 'Warning|Overfull|Underfull|undefined' /tmp/quadratic-stage03-review4/main.log
```

The exact checks passed. The independent temporary-directory build passed and
produced 17 pages. The final log search found no matches. No project-wide test,
CI inspection, Lean run, or subagent was used.
