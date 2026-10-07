# Independent integration review

Date: 2026-10-02. Scope: the decomposition continuation and its integrated
technical report. This review concerns consistency of claims, hypotheses,
dependencies, implementation coverage, and evidence. It does not establish
publication priority or replace the focused mathematical and code reviews.
The final report, coverage map, result index, and scoped extension proofs
are consistent. No unresolved mathematical or implementation-coverage
mismatch was found in this integration review.

## Mathematical dependencies checked

The report's corrected-grid proof keeps certificate soundness separate from
the growth assumption used in its running-time analysis. The conditional
interpolation inequality justifies coordinate filtering, and its history
argument extends the final restricted-grid bound to the original box.
The unknown-conditioning schedule caps failed trials before large table
allocation. The logarithmic dimension term in the state count is absorbed
into parameter dependence and an absolute polynomial input exponent.

The exact quadratic theorem has a separate rational-height and acceptance
argument. It does not treat all feasible objective values as a rational
lattice. Its recovered vector is checked for feasibility and exact equality
to the isolated optimum value. The polynomial extension correctly limits
automatic exact output to native integer variables; continuous polynomial
output requires a separate certificate.

The new workstreams retain their material additional hypotheses:

- Affine convex recourse requires globally verified response and multiplier
  maps and a decomposition of the reduced attachment scopes. Its reduced
  positive-coordinate curvature bound is an additional condition; the
  negative-curvature pullback alone does not establish that bound.
- Changing-active-set convex value factors require independent private
  feasible polytopes that do not change with retained coordinates. Their
  value factors are concave, so the direct retained quadratic supplies an
  upper coordinate-curvature bound. Exact recovery uses the original
  rational quadratic over its polytope, not a quadratic height claim about
  the nonsmooth reduced value function.
- Conditional minimum-cut recourse requires coordinate concavity and
  favorable residual signs after coordinate reversals. The broader
  concave/convex construction also requires a PSD remaining continuous
  block and exact submodular optimization. Its mixed-domain oracle is
  broader than the all-continuous smoothed theorem to which it is applied.
- TU feasible rounding uses a full continuous Hessian bound and aligned
  grids with integral right-hand sides. Its resulting width dependence is
  XP, with an explicit initial-grid capacity cost, not the product-box FPT
  theorem with the same parameters.
- Unknown-growth discovery of a nonunique optimum is restricted to the
  stated diagonal-certificate class. Its candidate generator may use an
  incorrect growth guess, but the final KKT/PSD acceptance rule remains
  globally valid. The full-set descriptor is compact; it does not enumerate
  components or promise efficient projection onto the set.
- Polynomial active-face discovery includes the precision parameter
  `B_gamma`. Weak derivative signs preserve the minimum and a selected
  optimizer; they do not certify uniqueness in the original domain.

The endpoint full-set description uses nonnegative Bellman residuals and
the quadratic endpoint-variance identity. It retains the essential
independent-rounding support condition when a diagonal coefficient is zero.
Coordinate projections of endpoint optima alone would not suffice.

The conditional-moment example retains its precise target: local exact bag
measures with matching separator moments do not give a common global
conditioning of PSD covariances on coordinate cells. Its four-variable
family has fixed width, a unique optimum, a valid fixed growth constant,
and fixed negative curvature, while the specified relaxation keeps a
constant gap as cell widths shrink. The global PSD completion does not
supply a probability distribution. This refutes that proposed error
interface; it does not refute stronger consistency, adaptive filtering, or
the unrestricted negative-curvature algorithmic target.

Three report-level explicitness corrections were requested and incorporated:

1. The deterministic exact-core checker must verify the candidate value's
   denominator bound. Feasibility and membership in a narrow interval do
   not make an arbitrary feasible value exact. The implementation already
   contained the required check.
2. Affine reduction uses exact endpoint DP when every reduced diagonal is
   nonpositive; the positive-curvature theorem covers the other branch.
3. Polynomial midpoint derivative tests operate after integer labels have
   become singletons. A continuous-Hessian bound alone does not control a
   change of integer slice.

No algorithm or companion theorem needed modification for these three
points. They make the report match the already stated companion conditions.

The affine-selector recognition proof admits a useful simplification found
during this review. Every optimizer of the center convex QP has the same
gradient. Coordinates with nonzero central gradient must be fixed at the
corresponding bound in every globally affine response. Every other
coordinate must have identically zero gradient along that response: an
affine response is either interior on the parameter-box interior, or is
identically a bound; in the latter case its affine gradient has a fixed
sign and a zero at the center and is therefore identically zero. These
conditions and robust affine box feasibility are necessary and sufficient
KKT conditions. They reduce recognition to one center QP and one LP,
without the initially proposed coordinate-extremum LPs. The final theorem
and report incorporate this simpler procedure. Its diagnostic uses supplied,
verified central optimizers and bounded exact Fourier--Motzkin elimination;
it does not implement the theorem's general polynomial-time QP/LP backend.

## Implementation and evidence boundaries

The rational grid implementation supports certified approximation and
several exact exits. It does not implement the report's general continuous
rational reconstruction theorem. The mixed concave/convex recourse checker
uses small exact enumeration for diagnostics; it is not a general SFM or
oracle-LP implementation. Mathematical consequences of these theorems must
therefore remain distinct from software capabilities.

An independent read of the saved 60-run comparative result file found:

| Method | Requested tolerance reached | Resource-limited runs |
| --- | ---: | ---: |
| Geometric grids with pruning | 13 | 2 |
| Geometric grids without pruning | 13 | 2 |
| Uniform grids without pruning | 11 | 4 |
| SCIP numerical solve | 13 | 2 |

All 45 rational solver certificates report successful independent replay;
all 39 small-case rational runs enclose their exact reference optimum. The
two public instances use greedy decomposition widths 25 and 95, which are
upper bounds on treewidth. Neither public case reached its requested
tolerance under any method within the recorded limits. These results do
not establish general practical superiority, exact continuous optimization
by the prototype, or a growth-controlled scaling law. SCIP's numerical
dual bounds remain distinct from the rational certificates.

The final extension suite has 14 further runs and 11 further valid rational
certificates, bringing the total to 56. Independently reading the saved
fractions confirmed that all four affine-comparison intervals contain
their analytically known zero optimum. The larger paths have no claimed
exhaustive reference. The 256-variable pruned path stops at its time
limit; the unpruned path stops at its table limit. The reduced affine core
meets its target while the two stiffer original models stop at time limits.
Those are bounded comparisons on the documented fixtures, not a general
recognition-backend or performance benchmark.

## Final integration and verification

The final pass read the report's completed extension and computation
sections, its coverage map, and the continuation's result index and program
outcome. The source distinguishes proofs reproduced in the report from
longer companion arguments. It distinguishes complete mathematical
algorithms from finite diagnostics and production components. The result
index explicitly preserves the unresolved unrestricted negative-curvature,
coupled-constraint, conditional-message, and unknown-optimal-set questions.
Completing this finite development program is not represented as solving
all of those questions.

The reviewer independently ran short `python3` checks over the saved JSON
results to aggregate statuses, certificate checks, exact-reference
enclosures, and process times, and used `fractions.Fraction` to check the
four affine intervals against zero. The two suites' summed subprocess wall
times are 20.2282868 and 22.2320658 seconds, matching the rounded report
figures. Intermediate source-hash comparisons also matched their recorded
benchmark snapshots. These checks inspect saved evidence; they are not new
benchmark runs or a second execution of every certificate verifier.

The report author completed the targeted command
`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in the report
directory. The final artifact has 23 pages, with no reported TeX errors,
overfull boxes, or undefined citations/references; root observed only benign
underfull table paragraphs. The author checked all
50 report-local links. Root's final scoped checks found no trailing
whitespace in the continuation's 72 text/code sources and resolved all 216
local Markdown links; `git diff --check -- README.md .gitignore`
also passed. Root rendered the first PDF page and the scaling, affine-result,
and scope-table pages and inspected extracted text for readability, finding
no clipping. These are reported author/root checks, distinct from the
reviewer's reads and exact data aggregation.

The final affine-selector diagnostic was also reported passing: 15 rational
fixtures, comprising 11 affine and four non-affine cases, 32 exhaustive
active patterns, and 205 exact KKT checks. Its bounded elimination method
is accurately identified as a diagnostic rather than polynomial-time
performance evidence.

Only topic-specific verification was performed. No project-wide
verification or CI inspection was performed for this review.
