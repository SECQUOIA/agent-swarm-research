# Recourse manuscript review, round 1

Reviewed the completed Section 10 and Appendix I on 2026-10-05. I read
`BRIEF.md`, `authoring/DECISIONS.md`, the actual input/output models,
Section 2 and the shared convex-value, Hoffman, cubic, and minimum-norm
selector proofs in Appendix C. The two prewrite audits were supplementary
background. I reconstructed the actual manuscript arguments rather than
treating an author report or prior audit as proof. Two independent
delegated analytic reviews checked the fallback/coupled interfaces and
the cubic fiber/lattice/completion chain; they refreshed after the author
completed. No manuscript file was edited.

The full V1–V5 and RQ1–RQ4 chain has no unresolved internal analytic
obstruction. It can remain an unconditional expected-work theorem under
the explicit optimization promises and the stated classical tool
contracts. The local corrections below are required for journal readiness;
none requires weakening a main result or replacing the all-dimensional
proof by an oracle assumption. Source verification and bibliography
integration remain separate from this analytic conclusion.

Reviewed file hashes:

- `sections/10-recourse.tex`: `0d44bbd004cd26f3044bb4bacb661bdb426138be538b97b4672fe457f31478d9`
- `appendices/I-recourse.tex`: `a38ad7007300b3ef385d3755519de6bca02b0765e80acf569a4713cb2db58bbc`

## Required local corrections

Line numbers refer to those completed author versions. Severity describes
the printed contract or proof defect, not the size of the repair.

| Severity | Location | Evidence and minimal repair |
| --- | --- | --- |
| Moderate | `appendices/I-recourse.tex:1365` and `:1472` | The declared computable constants must be rational, but the first formula uses `(n+1)^((D-1)/2)`, which can be irrational for even D, and the second uses `sqrt(m)`. These constants enter rational objective coefficients and tolerance schedules. Use `(n+1)^ceil((D-1)/2)` in the first majorant and a rational upper bound such as `ceil(sqrt(m))` or `m` in the second. Their polynomial bit bounds and all inequalities survive. |
| Moderate | `appendices/I-recourse.tex:42` | The interface accepts an arbitrary rational eta but gives cost depending only on `log(2+1/eta)`. A rational close to 1 can have an arbitrarily long numerator and denominator. The actual shared lemma at `sections/02-points.tex:128–140` counts its encoding length. Replace the cost by `P_D(L_Q + <eta>)`, or explicitly restrict to short dyadic tolerances. Every actual call already has polynomial encoding length. |
| Moderate | `appendices/I-recourse.tex:1019–1022` | Exact convex QP is invoked on a possibly thin fiber. Convexity on that fiber does not imply an ambient positive semidefinite Hessian: `-x^2` is convex on the singleton `x=0`. State that the fiber is first reduced to its rational affine hull. Its restricted constant Hessian is positive semidefinite, and the rational affine map preserves exact recovery. |
| Low | `sections/10-recourse.tex:457–458` | The lattice proof at `I-recourse.tex:1606–1609` applies the monomial Lipschitz bound on the unit box to the approximation as well as the true core. Add `hat a in [0,1]^r` to the lemma. The actual base stage already clips at `I-recourse.tex:1782`, so the algorithm needs no change. |
| Low | `appendices/I-recourse.tex:1458–1461` | The positive eigenvalue bound uses `lambda_0^A`, defined only when `H_A != 0`, also in the zero-Hessian branch. Guard this calculation by `H_A != 0`; when `H_A=0`, state `K_A=R^m` and `Pi=0`, so the transverse estimate is automatic. The remaining gradient-row/Hoffman argument covers affine fibers. |
| Low | `appendices/I-recourse.tex:1329–1330` | The necessity argument starts with membership in the displayed slice, then asserts the optimality it is meant to characterize. Change the antecedent to “if w is optimal, then E=0 and the bounds give Jd'=0.” The converse in the next lines is valid. |
| Low | `appendices/I-recourse.tex:1219–1220` and `:1236` | `B(0,R_0)` is explicitly an open ball, but `R_0=max{1,sum m_j}` only bounds the norm weakly. The interval `[-1,1]` can attain the radius. Set `R_0=1+sum m_j`, or use a closed outer ball and invoke the closed inner ball actually proved. Adding 1 is simplest. |
| Low | `appendices/I-recourse.tex:964` | Explicitly require `A=A^T` in the quadratic height lemma. The proof uses `grad q=Ax+c`. Every explicit quadratic objective has such a rational representation, so this only fixes the stated hypothesis. |
| Low | `appendices/I-recourse.tex:28` | Under the shared numerator-plus-denominator encoding, a generic sampled fraction adds `log M` bits to both. Replace `b <= L+log_2 M+2` by `b <= L+2 log_2 M+O(1)`. The polynomial sampling-bit conclusion is unaffected. |
| Low | `sections/10-recourse.tex:29–30` | Add “with expected polynomial running time” to the Las Vegas qualifier, as the later degree-four remark already does. Otherwise ordinary exact algorithms already meet the paper's Las Vegas definition. |
| Low | `sections/10-recourse.tex:25–26` | Qualify the residual-convexity-only guarantee by “On product boxes.” Coupled polytopes require the supplied joint core convexifier, as the definition and theorems correctly state. |

Additional wording cleanup: at `sections/10-recourse.tex:343–347`, identify
delta and mu as supplied positive rational margins when asserting
computability and bit length. At `I-recourse.tex:841`, the incumbent may
be a witness from an earlier level; say “at a level at most J.” At
`:721`, use every finite `t <= g`, or state an extended-real convention
for the single-core case, rather than writing infinity times zero.
At `:1338–1339`, the example for `B_F` should be
`max{1,sum absolute entries}` to meet its stated lower bound.

## Reconstructed proof and coverage

**Every-draw cells and V1/V3.** In a product box, independently rounding
one core coordinate at a time preserves its mean and adds at most
`Lambda h^2/8` in expected objective. Holding the residual fixed makes
this a valid corner lower bound even though the projected value is
nonconvex. In a coupled polytope, the secant correction turns the supplied
convexifier into a convex polynomial on each rational cell intersection.
The shared convex-value lemma actually returns both an exactly feasible
rational witness and a certified lower bound, including in its part (b);
it is not merely a feasible-gap interface. The two-pass pruning uses the
final incumbent. Current and previously discarded cells cover the domain,
giving `[U-2e_h,U]`; every optimal core and the current incumbent survive.
Retained witness gaps are at most `4e_h`. Lower-dimensional cell domains
are covered by the shared relative-coordinate and feasibility-repair proof.

**All-dimensional count.** The maximum-simplex determinant sandwiches the
volume between `d(K)/k!` and `2^k d(K)`. Whole retained cells lie in the
padded convex near-optimal hull, so disjoint interiors give retained count
`<=2^k W` and generated count `<=4^k W` at every level and query. For
`Psi(c)=max_X(c'v-f)` and `Upsilon=Psi+||c||^2/(2 kappa_+)`, conjugacy gives
a `kappa_+`-Lipschitz gradient of `Upsilon*`. The pushforward measure has
the printed box-mass bound. Completing the square bounds the Fenchel
residual at a near-optimal core; smoothness and convexity extend it to
the padded hull. That hull maps into the radius `4 kappa_+ k h` ball.
The disjoint-ball selection proof covers every relevant center without
assuming a density for the pushforward measure. Summing its disjoint
masses gives the stated weak `(1,1)` tail in every dimension. A growth-only
count would have an unbounded cap moment for `k>=3`; it is not used to
justify the general theorem.

**Finite law and event format.** The all-scale event quantifies the scale,
Caratheodory witnesses, padding, and a QR factorization existentially,
then uses a single universal original competitor block. Positive diagonal
entries and product chains encode the strict absolute determinant
inequality with polynomial-size degree-two equations. No factorial
determinant expansion is hidden. Growth and margin events also have two
blocks. The scalar-section count is uniform in arbitrary fixed real
coefficients, thresholds, and original coefficient heights. The
endpoint-inclusive grid has CDF error `<=1/M`; replacement of independent
marginals one at a time gives `2kC/M`, including point atoms and ties.
There is no substitution of an almost-sure continuous statement for a
finite-grid guarantee and no union bound over requested precision.

**Projected growth and V2.** The shifted conjugate `Psi_t` has centered
core subgradients in `[-1/2,1/2]^k`. At differentiability points its tilt
map produces a core-growth witness. The proximal inverse is 1-Lipschitz
and maps the good set onto the inner coefficient cube up to a null set,
giving `Pr_cont(g<t)<=kt/sigma`. Compactness closes the good-growth event
at the threshold; block elimination transfers its complement to the grid.
The retained coordinate hull contains every optimal core and the
incumbent on every draw, so its rational diameter test certifies the
fixed selected core without deciding uniqueness. Growth is used only to
show that failure implies one base event. The cap and hull failures are
contained in `{W>Xi} union {g<g_0}` for all q. Integrating the truncated
weak tail proves the printed common factor and expected work.

**Base-only same-selector fallback.** The actual nested predicate has
linear Boolean size. The singleton formula enforces global optimality,
lexicographically least core, and the unique minimum-norm residual in
that core. Convex residual fibers establish that uniqueness in both
instance types. Separate coordinate formulas therefore select one point,
including tied cores and positive-dimensional optimal sets. With two
n-variable blocks, denominator clearing makes the realized height
`O(L+kb)`. Elimination and univariate isolation put every format power of
H into `Xi_0`, while coefficient height and q have absolute polynomial
exponents. Dyadic shortening and clipping or rational LP repair produce
short feasible outputs. The grid is selected after this base factor,
so its construction is not circular. Tilted baselines share the format
factor; no sampled-height-inflated heuristic replaces the exact fallback.

**V4 and V5.** Joint-convex probes exclude all optimal cores and the
incumbent whenever their certified lower bound exceeds U. A failing probe
returns a near-optimal witness. Binary search only maintains those two
facts; it does not require monotone outcomes. Growth bounds the final
enclosure width, and its single exceptional event pays for fallback,
giving expectation at most 2. For quadratics, tangent stationarity on the
smallest active face makes the quadratic constant on a rational
stationary-face polytope. The lexicographic optimum is its vertex, giving
the determinant denominator bound even when the complete QP is
nonconvex. Continued fractions recover the selected core from a short
Cauchy output. Exact convex QP on its fiber completes some rational
optimizer and the exact value, exactly as the corollary claims; it does
not promise the minimum-norm residual in this exact-output corollary.

**RQ1/RQ2 supplied convexifiers.** The surrogate's minimum set is exactly
`{a} times S(gamma)`. For cubics, relative coordinates precede the PSD
Hessian inference. Reflection around a rational interior point gives a
common rational Hessian kernel. The transverse estimate, gradient row,
and core rows characterize the whole optimal slice; only the right-hand
side involves the unknown core. For globally convex higher degree, the
real-coefficient Bregman/interpolation lemma bounds gradient coefficients
without computing the unknown linear tilt. Adding the core rows removes
that tilt from the zero slice. Rational Hoffman bounds give one uniform
effective modulus. Regularization uses the original norm on the original
fixed domain, and its objective perturbation budget transfers a short
rational core query to the exact surrogate. The required precision is
`O_D(q)+poly_D(L)`, not `L^k`. The verifiable affine-power subclass follows
by a fixed-degree identity check and exact PSD testing.

**RQ3/RQ4 cubic fibers and full selector.** Product-box reflection proves
the fixed face kernel and the center lower margin. Only one gradient row
of the original matrix varies; every minor therefore has degree at most
two, and the uniform denominator/height bound does not enumerate minors
or faces or introduce uncontrolled row-compression coefficients. The two
printed obstructions are valid: `v z^2` has no core-uniform residual
modulus or joint core convexifier, and `gamma v-v^2 z`, `gamma>1`, makes
exact residual minimizers at positive approximate cores converge to the
wrong residual selector at the endpoint.

Neighboring tilts fix endpoints soundly for every optimal core. A missed
endpoint requires an interval of conditional noise of length t. The LLL
lattice consists exactly of `(h,h'omega)`. The relation multiplier h is
already the first s integer coordinates of a returned vector, so its
height and output work are covered by exact polynomial-time LLL.
Acceptance is an integer squared-norm comparison and certifies every
bounded-height quadratic at the true core. The success proof correctly
uses the larger height `R_s=2^s 4sB`. Identically zero minor polynomials
are harmless; all other minors receive certified positive margins.

Interior contact slopes are unique and locally U-Lipschitz. Disjointifying
a countable local cover transfers the quadratic small-sublevel volume
bound to noise probabilities. The rotated mixed-term slices have the
required projected volume, and the `8 sqrt(eta)` bound is valid. The
finite-law two-block event includes any global minimizer, not a presumed
continuous residual selector. The single base rejection event has
probability `<=1/(4Xi)`. Accepted completion regularizes the residual at
the certified face; projection/clipping preserves core error and uniform
objective perturbation gives residual error e. Its precision is
`8q+poly(L)` with absolute exponents. Rejection uses the same singleton
selector. Summing the `2k+1` inherited work factors and the rejection
factor needs no independence. Quartic and unsupplied coupled-domain
completion are correctly left outside this theorem.

## Source and document readiness

The root reports that Luna cleared the primary Renegar 1992 Part III,
Theorem 1.1, printed pp. 330–331, including fixed-block output degree,
count, coefficient-height, and sequential bit-work bounds. That is the
decisive separated-height contract. This review uses that vetted result;
I did no literature research. The completed author asks Luna to confirm
the real-coefficient structural use and BPR univariate chapter pinpoints.
Those requests should be resolved through the designated literature
agent, together with the already pending shared GLS contract. No new
nonclassical source contract arose from proof reconstruction.

The targeted recourse reference check found 68 distinct references and
no undefined labels. It found 12 citation keys, with these eight absent
from the current `references.bib`: `AndroulakisMaranasFloudas1995`,
`BasuPollackRoy2006`, `EvansGariepy2015`, `Hoffman1952`, `Renegar1992QE`,
`Rockafellar1970`, `Schrijver1986`, and `SpielmanTeng2004`. Their insertion
and vetted pinpoints are a submission-readiness requirement, not proof
evidence supplied by a failed citation check.

## Verification actually performed

- Read-only `cat`, `sed`, `nl`, `rg`, and `sha256sum` inspections of the
  assigned manuscript, shared interfaces, and supplementary audits.
- An inline Python document check of references and citation keys used
  only by `sections/10-recourse.tex` and `appendices/I-recourse.tex`:
  all 68 reference labels resolve; eight citation keys remain missing.
- `git diff --check -- paper-exact-arithmetic/evidence/reviews/recourse-r1.md`:
  passed. A scoped text check of this owned review file also passed.

No experiments, mathematical scripts, historical checker reruns,
project-wide verification, CI inspection, or literature browsing ran.
These document checks are distinct from analytic proof reconstruction
and from CI.
