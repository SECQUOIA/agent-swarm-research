# Common finite-law budgets from input length

Date: 2026-10-05. Author: Sol. This report addresses the universal-law claims
in the current `sections/10-discussion.tex:66–71,132–136`. Author files are
active, so these locations identify the text read for this report rather
than a frozen final version. No TeX, literature record, or experiment was
changed, and no work was delegated.

**Conclusion.** The blanket limitation and open question are too broad.
For each polynomial-bit route, the existing effective bounds give a common
resolution for every valid input of length at most `I`, with degree and other
fixed format constants held fixed. The supplied noise scale still rescales
the law, and the theorem still specifies which coordinates are perturbed.
Uniform grids admit a common `M_d(I) = 2^{P_d(I)}`. The proved Gaussian-like
routes admit a common polynomial accuracy `b_d(I)` after uniformly solving
the support/precision budget. The structural and numerical factors in the
expected bounds are preserved, up to replacing a fixed polynomial in `I`
by another fixed polynomial.

General nonlinear boundary flow/TU has a different contract. The current
proof gives a common budget `M_d(I,K)` for a supplied upper bound `k <= K`,
with sampling, output, and work bounds parameterized by `K`. Taking the
maximum over all `k <= I` gives an input-length law, but need not preserve
the stated `f_d(k) poly_d(I)` bound for small actual `k`. The existing proof
does not establish a polynomial-bit law independent of the core-size
parameter for this family. This is a limitation of the available budget,
not an impossibility theorem about other laws or algorithms.

The uniformization below is an elementary consequence of the effective
complexity estimates already used to prove the algorithms. It should not be
presented as an independent novelty claim.

## A precise corollary for the polynomial-bit routes

Fix a theorem route and its fixed format constants: in particular the
polynomial degree, and any fixed graph dependency depth. Fix the oracle and
certificate-verification work model used by that theorem. Assume that the
base length counts all explicit data and supplied rational numerical bounds
as in `02-model.tex:11–17,46–69`.

There are effective nondecreasing integer polynomials, depending only on
these fixed choices, with the following properties.

1. For a route proved with uniform grids, choose
   `M(I) = 2^{P(I)}`. Every valid base instance of length at most `I` may use
   the marginal law `U_{sigma,M(I)}` instead of its individually selected
   minimum resolution. The aligned integer theorem uses the same `M(I)`
   in every row, with each row's supplied scale `sigma_i`.
2. For a route proved with Gaussian-like noise, choose the accuracy `b(I)`
   constructed below and use `G_{b(I),sigma}` independently in the coordinates
   specified by that theorem. Its support and the auxiliary search box are
   budgeted together before sampling.
3. Every-draw correctness, same-draw fallback, the output format, and the
   stated structural and numerical factors in the expected construction work
   remain valid. The bit polynomial may acquire a larger fixed exponent or
   constant, independent of the structural parameter. Arbitrary-precision
   output evaluation uses the same sampled instance and does not choose a
   new law for each evaluation precision.

This is a common **standardized scalar family**, not one identical
probability measure on the original vector space for different values of
`sigma`, different dimensions, or different ambient/core/aligned models.
For example, two supplied scales give two rescalings of the same normalized
grid. Nor does it claim that the grid and Gaussian-like families are
interchangeable: each route retains the law family its proof uses.

The polynomial can be taken to have the form `C_d (I+1)^{c_d}`, with effective
fixed constants enlarged to dominate the finitely many relevant format,
height, threshold, and depth bounds. A finite collection of polynomial-bit
routes can share one such envelope within each law family by enlarging these
constants. Fixed graph-depth or other format constants must be fixed across
that collection; an unbounded dependency depth is not covered merely by
calling the original degree fixed.

This construction evaluates a fixed envelope. It does not enumerate all
inputs of length `I`, materialize all atoms, or discover which input strings
satisfy the promises.

## Why the grid budget is uniform

The required separation is already explicit in the current mathematical
text. In `A-finite-noise.tex:457–490`, quantifier-elimination format and
polynomial degrees are bounded by `2^{poly_d(I)}` independently of the added
coefficient length. Coefficient heights contain only a fixed polynomial
dependence on `I+b`. The common-root conversion enlarges the base multiplier
but retains this separation. Thus a fixed implementation gives an effective
uniform bound

\[
 B_\Pi\le 2^{P_B(I)},\qquad
 W_{\rm fallback}(\Pi,\gamma,q)
 \le B_\Pi (I+b+q+1)^c,
\]

with fixed `c` and polynomial `P_B`, for every valid input in the route.

For the finite-tail constant, `03-counting.tex:387–451` gives

\[
 H_s=((2s+1)\max\{d,2\})^{a_R(N+1)^2},
 \qquad C_{\rm tail}=2H_s^3+1.
\]

Dimensions and explicitly listed data are bounded by the input length.
Native integer disjunctions can have exponentially many atoms, but
`log(s+1)` has a uniform polynomial bound in `I`. Consequently
`log C_tail <= P_C(I)`. The mixed-box active-gradient factor likewise has
`log K_act <= P_K(I)`. These are format bounds, not constants secretly
depending on the individual coefficient values.

Positive rational input numbers of encoding length at most `I` have
logarithmic magnitudes bounded by `O(I)`. Fixed-degree monomial derivative
bounds, rational matrix operations, determinant bounds, and rational LP
vertex bounds have effective polynomial encoding bounds. This controls the
logarithms of the widths, curvature bounds, inverse frame bounds, supplied
strong-convexity moduli, and reciprocal noise scales that enter the caps.
Large numerical ratios can still make the **expected count** large; bounding
their logarithms for choosing a law does not remove them from that count.

This uses the geometric contracts of the particular routes, not just the
abstract fixed-degree semialgebraic fallback. For example, the compact set
`1 <= x_0 <= 2`, `x_i = x_{i-1}^2` for `1 <= i <= N` has a degree-two
description of length `O(N log N)`, but its final-coordinate width is
`2^{2^N}-1`. The logarithm of that width is superpolynomial in the short
description length. Generic format and coefficient-height bounds therefore
do not by themselves give polynomial-bit width, derivative, and geometric
cap budgets on every compact semialgebraic domain. This chain is outside the
polynomial-bit box, rational-polytope, and fixed-depth graph routes. The
example disproves that broader inference; it does not prove that this simple
chain needs a difficult algorithm or a particular noise precision.

The sparse schedule at `05-sparse.tex:736–757` requires

\[
 M\ge\max\{2,2^{J_\Pi},4nC_{{\rm tail},\Pi}/\rho_\Pi,
                        2K_\Pi/\rho_\Pi\}.
\]

Each logarithm on the right is bounded by an effective polynomial in `I`.
The continuous recourse choices at `E-recourse.tex:276–299,715–737` have the
same property, including their three-block active-stratum format bound and
derived tube constant. Native integer recourse, interior flow, bilinear
flow/TU, and the constrained sparse extensions use the corresponding
polynomial-bit schedules. A single `P(I)` can dominate all their required
grid exponents. The at-most-two-negative-direction route has the simpler
condition `M >= 2n D B` at `04-quadratic.tex:240–252` and is covered too.

Keep the instance's thresholds and cap, and replace its selected minimum
grid resolution by this common larger resolution. For these schedules, the
proof uses `M` only through concentration bounds of the form
`length/(2 sigma) + 1/M`, finite replacement errors proportional to `1/M`,
and the requirement `M >= 2^J`. All these sufficient inequalities improve
with larger `M`; the support remains `[-sigma,sigma]`. Sampled coefficient
lengths are now uniformly polynomial in `I`. Fallback accounting retains the
same base multiplier and leaves a polynomial bit factor, so the same
structural/numerical expected-work form follows.

The lattice route needs one explicit adjustment. At
`08-integer.tex:535–568`, the proof takes `J = log_2 M`, obtains curvature
error `O(M^{-2})`, and uses the original-objective lattice spacing
`1/[D_0(M-1)]`. Any common larger `M` satisfying the base inequality works
if `J` is reset to `log_2 M`. The ratio of these two error scales improves
with `M`. The grid count is still valid through that new level, and the
number of levels is polynomial in `I`. Keep the common `M` across rows;
separate unrelated row denominators would lose the displayed simple lattice
bound.

For strong fields, distinguish the sufficient regime from the exact
distribution-dependent factor. At `08-integer.tex:458–491`, the theorem is
valid for every `M`, and its sufficient regime is

\[
 \sigma\ge8\Delta_+\max_i(a_iR_i),
 \qquad M\ge16\Delta_+\max_i a_i.
\]

The second condition has a polynomial logarithmic envelope, so the same
common grid can satisfy it. Together these inequalities still give
`4 Delta_+ beta <= 1/2`. However the exact interval probabilities `q_i(M)`
are **not monotone** in `M`: endpoint grids of sizes `M` and `2M` are not
nested. An interval avoiding the two-point grid can contain a point of the
four-point grid. Recompute `q_i` and `beta` for the common law. A previously
subcritical coarse grid, with no sufficient physical strong-noise premise,
cannot simply be declared subcritical after changing its resolution.

## The Gaussian support/precision loop can also be uniform

Increasing Gaussian-like accuracy enlarges the support to
`[-sigma(b+20),sigma(b+20)]`. Therefore replacing an individually selected
accuracy by a larger input-length bound while keeping its old auxiliary box
is not a valid argument. Recompute the support box and cap together.

The checked low-rank budget has a particularly simple uniform envelope.
For trial support radius multiplier `R = 2^t`, the ordinary continuous and
anisotropic separable routes satisfy

\[
 J_\Pi(t)\le J_\Pi(0)+t,
\]

and the general mixed quadratic route satisfies

\[
 J_\Pi(t)\le J_\Pi(0)+2t.
\]

The latter has one factor of `2^t` from the search-box width and another
from the label-gap coefficient. The base logarithms are uniformly
polynomial in `I`. With
`Q_all = (J+1)(2^J+1)^k`, the required transfer accuracy satisfies a bound

\[
 b_{{\rm req},\Pi}(t)\le A(I)+D(I)t
 \qquad(t\ge0),
\]

for effective nondecreasing integer polynomials `A,D >= 1`. They dominate
the bad-event budget, `log(2n C_sec Q_all)`, the label-gap atomic budget,
and any at-most-two-direction tail budget included in the route. The
logarithm of `J+1` can be bounded by a polynomial base term plus `t`.
The dimension `k` is at most the explicit input size, and normalization
increases that size only polynomially. Thus the slope `D` has a uniform
polynomial bound as well.

An explicit common solution is

\[
 H(I)=A(I)+D(I)+21,
 \qquad t(I)=\lceil4\log_2H(I)\rceil,
 \qquad b(I)=A(I)+D(I)t(I).
\]

For `H >= 3`, using `t <= 4 log_2 H + 1` and `log_2 H <= H` gives

\[
 b(I)+20\le H+4H^2\le H^4\le2^{t(I)}.
\]

Hence the common sampler support fits the common trial radius, and
`b(I) >= b_req,Pi(t(I))` for every instance. Both `b(I)` and the individual
caps computed at that trial radius are polynomial in `I`; in fact the trial
radius is itself at most `2 H(I)^4`, a polynomial magnitude. A rounded
integer expression for `t` can be used instead of numerical logarithms.
All choices occur before drawing noise.

The Gaussian-weighted count controls the enlarged auxiliary box by the
original projected widths, rather than charging its full support-enlarged
width as a new numerical factor. Thus enlarging the trial support changes
the depth and bit cost by polynomial factors and preserves the stated
`H_G` or anisotropic count factor. The fixed section bound applies uniformly
to all coefficient values, so its transfer budget is not compromised by the
larger support. The source derivations are at
`smoothed-gaussian-cell-closure.md:290–327`,
`anisotropic-gaussian-separable-closure.md:313–351`, and the mixed budget in
`prewrite-lowrank-sol.md:665–700`; I rechecked their inequalities for this
uniform envelope.

This argument applies to the Gaussian-like routes actually proved in the
paper. It does not introduce Gaussian noise into a graph or recourse theorem
whose supplied curvature bound was proved only over a uniform-noise cube.

## What must be included in the model

The uniform budget uses the stated total base length. In particular it
includes the supplied scale `sigma`, coordinate bounds, decompositions,
convexifiers, frame or chart bounds, and any supplied residual modulus.
If `sigma` or a positive modulus were an external number of arbitrarily
large encoding length, there would be no corresponding bound in the old
`I`. That is not the manuscript's current model.

A certificate's encoding length is part of `I`; verification work remains
part of the algorithm's work. Uniformization neither verifies a promise nor
turns a general polynomial-inequality check into a cheap operation. A
curvature or chart premise must remain valid on the whole domain required
by its theorem. The all-noise interiority promise for interior flow at
`08-integer.tex:283–288` already ranges over the entire coefficient cube,
so replacing one grid by another grid in that cube preserves the premise.

For oracle theorems, keep the same box-stable oracle contract on every
rational query and every sampled coefficient in the new support. The
recourse and native-integer models describe the actual residual domain
explicitly; the common tail and fallback budgets do not depend on an
unencoded arbitrary set hidden behind an oracle. Oracle work is charged at
its stated query cost. A common complexity constant for a collection of
arbitrary oracle programs with unrelated polynomial exponents is not
implied. The corollary fixes the theorem's oracle implementation or retains
its cost as an explicit oracle factor. An oracle promised correct only on
one old grid would not suffice; the current contracts are broader.

Nor does a common finite law support indefinitely refined raw grids.
`03-counting.tex:239–258` still applies: atoms can make expected retained
counts grow at arbitrarily deep levels. Exact closure or lattice termination
occurs at the cap budgeted for the common law. Later `q`-bit evaluation
refines an exact descriptor. If an approximation-only grid theorem instead
uses a target accuracy in choosing its cap, that accuracy must be included
in its input budget or stated separately as `M(I,q)`.

Uniformization preserves the exact sampled-optimization contracts, not the
identity of the sampled distribution. It also preserves the distinction
between compact ordinary descriptors, expected-size proof traces, rare
large fallback outputs, and componentwise algebraic sums. For Gaussian-like
noise, the all-draw original-objective regret bound must use the new support
radius `sigma(b(I)+20)`. A small-noise regret calibration using an old,
smaller instance-specific support radius must be redone. The grid support
radius remains `sigma`.

## The nonlinear boundary flow/TU qualification

The current theorem at `08-integer.tex:370–397` and the TU transfer use

\[
 J_\Pi,\log_2 M_\Pi\le F_d(k)P_d(I),
\]

with an effective parameter function. Its source is the conversion of
distance from chart zeros into a positive chart-value margin. The
fixed-block elimination format can have
`E_d(k) = (k+1)^{O_d(k^2)}`, and that factor enters coefficient **bit
length**, not just the logarithm of an analysis-only degree. Consequently
the existing budget need not be polynomial in `I` uniformly over `k <= I`.
This distinction is recorded in `prewrite-recourse-sol.md:158–172` and
`smoothed-boundary-core-flow.md:239–325`.

Let `K` be a supplied upper bound on `k`, and choose an effective monotone
envelope `F_d^+(K)` for these budget functions. Then

\[
 M_d(I,K)=2^{\lceil F_d^+(K)P_d(I)\rceil}
\]

is a common resolution for all such instances with length at most `I` and
`k <= K`. Use each instance's own valid thresholds and cap. The support is
unchanged, while the finite atomic terms decrease. Sampling and all subsequent
coefficient/query costs now contain `F_d^+(K)`, so the correct resulting
contracts are, after enlarging an effective parameter function,

\[
 \text{sampling/output length}\le \widetilde F_d(K)\operatorname{poly}_d(I),
 \qquad
 \mathbb E W\le \widetilde F_d(K)Q_{\rm ex}(\Pi)
                         \operatorname{poly}_d(I),
\]

and output evaluation has the corresponding
`F_tilde_d(K) poly_d(I+q)` bound. The polynomial exponents remain independent
of `K`. The upper bound's encoding is included in the supplied data; there
is no need to use a bound larger than the explicit ambient dimension.

Taking `K = I` supplies a common input-length law in a purely computability
sense. It can nevertheless impose a superpolynomial sampling cost even on
a one-dimensional-core instance. A uniform endpoint-grid draw uses exactly
`log_2 M` fair bits, which must be charged. Thus this particular
uniformization need not preserve `f_d(k) poly_d(I)` with the **actual**
parameter `k`. The parameter-dependent upper bound is not a lower bound on
necessary precision, so this observation does not prove that a better
polynomial-bit law is impossible. Interior and bilinear flow/TU avoid this
issue and are covered by the polynomial-bit corollary above.

## Suggested changes in the scientific discussion

Replace the blanket limitation at `10-discussion.tex:66–71` by the precise
point that finite laws need sufficient resolution for the format, depth,
and fallback budgets. Add that the polynomial-bit routes admit common
input-length resolution bounds, after scaling by the supplied noise scale.
Distinguish the general nonlinear boundary flow/TU budget and retain the
failure of arbitrary coarse laws. Also retain the lattice and strong-field
exceptions to rare fallback.

Remove the unrestricted universal-law question from
`10-discussion.tex:132–136`. If retained as an open question, narrow it to
whether the parameter-dependent precision for general nonlinear boundary
flow/TU can be replaced by polynomial sampling precision while preserving
the stated parameter dependence. The separate question about short exact
algebraic outputs on every draw is unaffected. The model's base-chosen-law
paragraph can continue to describe the law used by the presented algorithm,
but should not suggest that instance-specific accuracy beyond input length
is necessary in the polynomial-bit routes.

## Verification record

I read the manuscript brief, integration decisions and contract, the current
model/counting/finite-noise files, the current discussion, and the relevant
quadratic, sparse, recourse, and integer schedules. I read the prewriting
route audits and the local mathematical support/precision and flow-margin
derivations cited above. Read-only commands were scoped `cat`, `rg --files`,
`rg -n`, `nl -ba` with `sed`, and `git status --short` for the four active
scientific files named in the task. The conclusions and budget inequalities
were checked analytically. No literature research, optimization experiment,
project-wide verification, or CI inspection was performed.

A targeted report-only check was run after writing for final newline,
trailing whitespace, paired display-math delimiters, and existence of the
named source artifacts. It passed. This report does not approve the active
manuscript or resolve its unrelated pending proof and citation corrections.
