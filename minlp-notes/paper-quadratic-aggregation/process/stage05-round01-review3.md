# Stage 5, round 1, independent review 3

Date: 2026-09-22. Verdict: **accept stage 5; no major or minor correction required.**

I independently reviewed all of `sections/07-approximation.tex`, both new
Python scripts, the figure and supplement README, bibliography additions,
stage author/literature records, coverage additions, and source snapshot.
I read the underlying accuracy note and the concurrent formal fragment to
check the stated relationship between the proofs and constants. Earlier
accepted sections supply the identified good cone and exact closed hull.
Later formal integration and synthesis are outside this review. I did not
read other current reviewers' reports or coordinate findings with them.

## Findings

Major issues: none.

Minor issues requiring correction: none.

The argument proves the advertised rate for the prescribed good cuts,
including interior multipliers, in the original Euclidean coordinates.
The exposition distinguishes this result from arbitrary-quadratic
approximation, classical approximation exponents, and the cost of solving
one objective. I found no unsupported claim of a new general duality or
approximation principle.

## Mathematical audit

1. **Definition and upper bound** (`07-approximation.tex`, opening through
   `lem:angle-mesh`). Every relaxation contains the compact hull, and the
   extended Hausdorff convention handles empty multiplier families and
   unbounded relaxations correctly. The endpoint cuts imply both unit-ball
   bounds. The matrix row-sum bound is 5/2 and the second-derivative bound
   is 10. At an interior minimum, Taylor's upper bound and a sample within
   half the largest gap give the correct lower estimate, with defect
   `5 Delta^2/4`. Only the nonnegative test directions are needed; the
   manuscript does not incorrectly replace copositivity by positive
   semidefiniteness. The identity for `B(sx)` and the chosen contraction
   repair every admitted point. The displacement estimate proves the
   stated upper bound, including the two-endpoint case `N=2`.

2. **Exact rational construction** (`cor:rational-mesh`). For `m>=1`, the
   two lists have just one common multiplier/ray, so their union has
   `2m+1` elements. The reflected arctangent meshes include both endpoints
   and have maximum angular gap at most `1/m`. All multipliers satisfy
   the cone boundary identity exactly. The integer magnitude and binary
   digit bounds are valid, including the stated encoding of zero. The
   scope is correctly limited to multiplier entries. The explicit
   tolerance budget follows from an actual family, without assuming
   attainment of the infimum over all families.

3. **Lower bound for arbitrary good families** (the lower-bound proof).
   The Gram diagonal bounds and determinant lower bound `12/25` ensure
   realizability in dimension two and hence every replication dimension
   under consideration. The residual vector is correct. Zero-coordinate
   multipliers cannot exclude a witness. For other multipliers, replacing
   their third coordinate by `2 sqrt(lambda1 lambda2)` on both sides of
   the exclusion inequality gives the necessary ratio inequality even
   for interior cuts. Adding two such inequalities and applying AM–GM
   gives the stated strict separation condition. Substitution of
   `eta=1/(400N^2)` yields exactly
   `16((1+10eta)^2-1)=4/(5N^2)+1/(100N^4)<1/N^2` for every `N>=1`.
   Therefore one cut excludes at most one of the `N+1` grid witnesses.
   The finite pigeonhole step also permits fewer than `N` cuts and
   repeated rays at different scales.

4. **Conversion to Euclidean distance.** The separating aggregate at an
   admitted witness has value `2eta`. Its leading matrix is PSD of
   operator norm `tau+1/tau<=5/2`; its gradient norm on the convex product
   of balls is at most `5 sqrt(2)`. That product contains both the witness
   and every hull point, so the mean-value estimate applies along every
   required segment. Consequently the lower constant is indeed
   `sqrt(2)/2000`. No dimension-dependent norm conversion is hidden in
   this argument. This is stronger than both the old logarithmic bound
   and the concurrent formal fragment's reported `1/2000` bound. The
   stage records state this distinction explicitly and do not claim
   formal certification of the stronger constant.

5. **Support-function equality** (`eq:hausdorff-support`). Bounded finite
   relaxations are closed, convex, and nonempty, hence compact. The
   projection characterization of a supporting normal proves the reverse
   bound, and nearest-point distance proves the forward bound. The text
   correctly distinguishes a common relaxation valid uniformly over
   objectives from selecting a different cut for each objective.

6. **One-objective exactness** (`prop:one-objective`, especially lines
   274–319). The vector quadratic is convex in the order induced by the
   dual good cone. Its upper image `E` is therefore convex. A fixed
   `x` plus the positive orthant supplies nonempty interior. The point
   `(0,v)` belongs to `E` and cannot be interior, since each lower point
   on that vertical line is excluded. For a full-dimensional convex set,
   the interiors of the set and its closure agree, so this point remains
   a boundary point of the closure. Thus the support argument does not
   need the unproved assertion that `E` is closed. The recession
   directions give the correct dual signs. Strict negativity of every
   nonzero good aggregate at zero rules out a zero objective coefficient;
   a nonzero objective then rules out a zero aggregation multiplier.
   Evaluation at a hull minimizer gives complementarity and establishes
   a common attained minimum on the one-cut relaxation. The proof is
   complete even when that relaxation is unbounded.

## Primary literature and novelty scope

- I opened the author-hosted primary report for
  [Rote's Sandwich algorithm paper](https://page.mi.fu-berlin.de/rote/Papers/pdf/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.pdf).
  Theorems 1–2, their corollaries and sharpness discussion support the
  finite-slope univariate `N^-2` comparison. Section 5 and Theorem 3
  treat polygonal Hausdorff approximation of planar convex figures.
  The manuscript uses this close antecedent accurately, without assigning
  report theorem numbering to the journal version or claiming that
  the classical exponent is new.

- I read the local Bronshteyn–Ivanov primary full-text extraction, including
  the theorem, construction, and final lower-bound remark, as well as its
  bibliographic record. It concerns polyhedral approximation controlled
  by vertex counts in the ambient dimension. The manuscript's brief
  comparison is supported and does not turn this result into a theorem
  about the prescribed quadratic cuts. The cited publication record is
  [Bronshteyn–Ivanov (1975)](https://doi.org/10.1007/BF00967115).

- I opened [Arya–da Fonseca–Mount, version 2](https://arxiv.org/html/2306.15648v2),
  independently checking its date, introduction, related-work comparison,
  and Theorems 1–2. Those results concern outer polytopes and piecewise
  affine lower approximations, with constants depending on ambient
  dimension and stated width/Lipschitz assumptions. The manuscript
  identifies their appropriate contextual role and does not import their
  conclusions under missing hypotheses. Its version-specific citation
  is accurate.

- I opened the coauthor-hosted primary copy of
  [Boyd–Vandenberghe, Convex Optimization](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf),
  checking Section 5.9.1, printed pages 264–265, especially dual-cone
  signs and the generalized Slater condition with dual attainment.
  This supports the classical-duality attribution. In the manuscript,
  the primal order cone is the dual of the good multiplier cone, which
  is the correct direction. The supplied proof establishes the needed
  specialization independently; it does not mistake the origin for a
  feasible point of the original three strict inequalities.

I also ran the bounded online searches `"quadratic aggregation"
"Hausdorff" approximation` and `"quadratic" "aggregations"
"approximation" "N" convex hull`. They returned the already-discussed
aggregation literature and unrelated results, without a verified earlier
instance of this particular two-sided bound. This search outcome is not
a proof of priority. The section's precise contribution statement and
explicit classical context are appropriately restrained.

## Supplement, figure, and checks actually performed

- Ran `python3 paper-quadratic-aggregation/supplement/check_approximation.py`:
  PASS, 64 rational meshes, 606 exact Gram witnesses, radial identities.
  I read the script and checked its use of exact `Fraction` arithmetic.
  Its stated limits correctly exclude certification of the universal
  pigeonhole, Hausdorff, and separation arguments.
- Copied only `plot_aggregation_slice.py` into a temporary directory and
  executed the copy with `runpy.run_path(..., run_name='__main__')`.
  PASS: boundary checks at 8,001 directions. Outputs were confined to
  `/tmp/stage05-review3-y5heyquf/figures`; no manuscript artifact changed.
- Independently derived the smaller-root quartic radius and the radial
  bound for each mesh cut. The formulas, containment tests, and nested
  `N=3,5,9` families are consistent. Visually inspected the supplied PNG:
  curves, labels, legend, and enlargement are legible. The caption
  accurately limits the image to a planar illustration.
- Recomputed every SHA-256 in `stage05-author-snapshot.json`: all 20
  files matched at review time, including the manuscript, figure,
  bibliography, source provenance, and deferred formal fragment.
- Searched the existing stage-5 `main.log` and `main.blg` for `Warning`,
  `Overfull`, `Underfull`, and `undefined`: no matches. I did not rebuild
  LaTeX or independently inspect every manuscript PDF page; this is not
  a claim of a fresh build.

No global verification, CI inspection, formal rerun, or subagent work was
performed. Only this review report was written in the repository.
