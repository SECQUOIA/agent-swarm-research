# Complete proof review: sparse and feasible-domain routes, r1

Reviewer: Sol. Date: 2026-10-05 local / 2026-10-06 UTC.

All manuscript locators below refer to the immutable directory
`evidence/snapshots/complete-proof-draft-r1/`, not the live author files.
I reviewed sections 05/06 and Appendices C/D, and the model, finite-tail,
and fallback interfaces needed by them. I consulted the original brief,
independent-review brief, earlier sparse reviews, integration contract and
decisions, and the shared-root development report. This is a mathematical
proof review before integration, not final publication approval.

## Decision

The intended extensions have coherent proofs and retain their stated count
factors. I verified the sparse box route, implicit graph rounding/count and
KKT tail, actuator reduction, and mixed-order transport/exposure/weighted
closure. The frozen simplex proof is not verified as written: its margin
lemma incorrectly includes unrestricted equality-budget multipliers, its
coarse corner definition conflicts with its rounding proof, and its patch
construction divides by zero for a fully fixed inequality block. These are
local repairs; none defeats the intended theorem. Point outputs also need
explicit evaluation branches before invoking the positive-dimensional GLS
lemma. Known integration issues remain pending in the frozen snapshot.

## Snapshot integrity

I checked SHA256 and byte counts against `manifest.json` for the seven
files used in this review. All matched. The checks were targeted to this
review, not project-wide verification.

| File | Lines | SHA256 |
| --- | ---: | --- |
| `sections/02-model.tex` | 460 | `143bedfa0aa700a84f0d912a0a7534a76126d2283ba8909defa30325006638f3` |
| `sections/03-counting.tex` | 584 | `f54a72dca58da3d71595a1e4159ad9c356555ba5ffa88b670fada18778535f83` |
| `sections/05-sparse.tex` | 929 | `4e901939543c8f88683525f931be1fd4934d01937298c7bee68ccc0c29d84733` |
| `sections/06-constraints.tex` | 741 | `3abea367a8f876908b3fca4b82129ff462f986dc65427014ce307af0754aed0a` |
| `appendices/A-finite-noise.tex` | 509 | `83943cf612ac484347b25ed583433c3c7abf1d120d5a73a4097d99c642784a7c` |
| `appendices/C-sparse.tex` | 272 | `28ca1ef81b4d15abfacd076ec1b604afea413f5e8e1d0e4eb54e324074a89d21` |
| `appendices/D-constraints.tex` | 994 | `82685cdb6e114ca01f3386491acead7f92004eb41455ff4f5ad93eac70c40e4c` |

## New findings

### S1. Major: equality-simplex multipliers invalidate the stated margin tail

Locations: `D-constraints.tex:471`–`:475`, `:512`–`:519`, `:529`–`:536`,
and its use at `:589`–`:591`; corresponding outline
`06-constraints.tex:579`–`:583`.

The closure premise and margin event refer to every active constraint.
The proof calls the multipliers nonnegative and says that a positive
coordinate in a tight block has derivative less than `-tau`. Those
statements apply to tight inequality budgets, not original equality
budgets. The multiplier of `sum x_i=1` is unrestricted. The tuple proof
itself correctly lists a budget multiplier only for a tight inequality
budget at `D:551`, so it does not prove the literal lemma.

Counterexample: let `F_0=0` on the probability simplex
`x_1+x_2=1`, `x>=0`, take degree bound one and `sigma=1`. On every draw
with `gamma_1!=gamma_2`, the unique optimizer is a vertex and its point
growth is `|gamma_1-gamma_2|/2>0`. When both coefficients are positive,
the equality multiplier is `-min{gamma_1,gamma_2}<0`, hence at most every
positive `tau`. Under the even grid law this event with unequal
coefficients has probability `1/4-1/(2M)`. Here the displayed constant is
`K_Delta=144`. With `M=2^16` and `tau=2^-16`, the claimed upper bound is
`288/65536`, whereas the event has probability `1/4-1/131072`.

Repair all margin and stopping statements to refer to **active inequality
constraints**: zero coordinates and tight budgets of inequality blocks.
Original equality budgets are imposed structurally and have no multiplier
margin requirement. In the KKT proof, `lambda_i>=0` for nonnegativity
constraints, `lambda_b>=0` for inequality budgets, and `lambda_b` is free
for equality budgets. Restrict `D:517`'s negative-anchor argument to
inequality blocks. For an equality block, the derivative difference from
any positive anchor still equals the zero coordinate's nonnegative
multiplier; its common equality multiplier cancels. With this repair,
the tuple count, the constant `K_Delta`, and the stated cutoff remain valid.

### S2. Medium: coarse simplex cells need a different corner definition

Locations: `D-constraints.tex:350`–`:355`, `:372`–`:380`, `:438`, `:595`–`:596`;
`06-constraints.tex:549`–`:551`.

The appendix globally defines corners as the points of a block cell in
`(h Z)^b`. At levels with `h>1`, the cell is the whole unit simplex, whose
vertices are not in that lattice. For a probability-simplex block and an
integer coordinate of width two, the inherited initial mesh has `s=h_0=2`.
The literal corner set of the probability simplex is empty. The initial
allowed grid then has no feasible point, contradicting the rounding lemma
and the finite incumbent needed for pruning. For an inequality simplex,
the literal coarse corner set contains only zero and cannot preserve the
mean of a nonzero point. The proof already uses the intended vertices;
the definition must match it.

Repair: define the coarse block grid and corners explicitly as the
original simplex vertices when `h>=1`; when `h<=1`, use the feasible
`h`-grid cube corners. State the fine cube ranges
`k_i in {0,...,1/h-1}`. Without a range or an explicit reference to the
coordinate cells of `[0,1]`, exterior cubes can create extra boundary
singleton cells: in one dimension the parent `[0,1]` at `h=1` would have
four nonempty children at `h=1/2`, including `{0}` and `{1}`, rather than
the asserted two. With the intended ranges, child cover and the
`2^{|b|}` corner/child/incidence bounds are valid.

### S3. Medium: the simplex center construction divides by zero on a fixed inequality block

Location: `D-constraints.tex:490`–`:502`.

If all coordinates of an inequality block have been recorded as zero,
the set of unrecorded coordinates is empty and its remaining budget is
one. Neither forced-budget test at `:494`–`:495` fires. The expression
at `:498` then divides by `sum(u_i-l_i)=0`. This occurs on legitimate
ordinary draws, even while another block has free coordinates.

For example, use two one-coordinate inequality blocks and
`F_0=x_1+(x_2-1/2)^2` with `sigma=1/10`. The first derivative in block one
is strictly positive on every draw, so its coordinate is recorded as zero.
Block two has an interior optimum and retains a nonempty free interval.
The center routine must process the empty first block without division.

Repair: drop every block with no unrecorded coordinates before computing
`lambda`; containment of a global minimizer already certifies the fixed
block's budget feasibility. For an equality block with just one free
coordinate, fix that coordinate to its remaining budget and remove it.
Return a rational point if the resulting tangent dimension is zero. Then
compute the strict center, basis, and radii only in the positive-dimensional
remaining blocks. The center proof and weighted Hessian test work after
these branches.

### S4. Medium proof gap: evaluate point outputs before applying GLS

Locations: `D-constraints.tex:286`–`:295`, `:600`–`:617`, `:968`–`:987`;
compare the premise `k>=1` at `C-sparse.tex:66`.

These passages apply the convex-patch lemma on every ordinary draw,
although closure can return a point. The implicit case is consequential:
all retained coordinates can be fixed while its dependent roots are still
irrational. For example, take `x in [0,1]`, the monotone equation
`y^2=2+x` with `V=[1,2]` and derivative floor two, and `F_0=10x`, with
`sigma=1`. The reduced derivative exceeds `10-1-1/(2 sqrt(2))>0` on
every draw. Thus the retained optimum is zero, its dependent coordinate
is `sqrt(2)`, and closure can return a zero-dimensional retained patch.

Repair: before GLS, handle tangent dimension zero directly. For order and
simplex outputs, evaluate the rational point and value exactly. For an
implicit graph, evaluate the chart roots and objective with the already
proved oracle, using enough total coordinate width for the ambient
Euclidean tolerance. This takes `poly(I+q)` and needs no strong-convexity
optimization. This branch is separate from the previously accepted
all-fixed-input preprocessing correction: it is needed for point outputs
of nontrivial positive-dimensional input instances.

### S5. Minor interface and bound clarifications

- `D-constraints.tex:44` asserts `k^{D_g}<=n^{D_g}`, but `k` counts ambient
  parents and `n` is the retained dimension. A dependent node may have more
  than `n` parents. Use `|Lambda(y_j)|<=min{n,k^{D_g}}`, or simply use
  `k<=n+m` and omit the false inequality. Fixed degree still gives a
  polynomial-size expanded monomial list.
- At `D-constraints.tex:10`, constant implicit roots need not be rational:
  `y^2=2`, `V=[1,2]`, and empty parent set are allowed. Formal constant
  elimination is harmless to the expanded decomposition, but it must not
  replace rational coefficients of the original fallback problem by an
  algebraic constant. Restrict rational substitution here to explicit
  constants and rational singleton brackets; retain other constant
  implicit equations in the chart oracle and original-domain fallback.
  Empty ancestor sets do not impair the running-intersection proof.
- `D-constraints.tex:163` associates `U_j` with the current grid minimizer
  `y^(j)`, although the minimum defining `U_j` can come from an earlier
  level. Store the point associated with the smallest certified upper
  bound. The pruning inequalities themselves use only `U_j>=f^*` and
  remain sound. Initialize `U_{-1}=+infinity` explicitly.
- The face-tail proofs at `D:548` and `:913` should state that a
  zero-dimensional face has one empty stationary tuple. The cited
  nonsingular-zero lemma is stated for positive dimension. This is the
  same elementary convention already made explicit at `A-finite-noise.tex:394`.

## Known accepted corrections still pending in the frozen corpus

These are not new findings. Their repairs were accepted after the early
reviews and are being integrated into live author files.

| Known item | Frozen locations | Status for this review |
| --- | --- | --- |
| Nonnegative actuator curvature choice | `06:426`–`:429`; `D:319`–`:321` | Pending; reduction checked conditional on a valid positive `L`. |
| Polynomial coefficient lengths and production cost in uniform families | `06:65`–`:78`; `D:47`, `:322`–`:323` | Pending; replace literal `I+b` by the proved polynomial bound. |
| Common-root fallback and degree/height budget | `02:265`–`:269`; `03:524`–`:550`; `A:428`–`:492` | Pending integration of the completed shared-root development. The frozen scalar fallback does not meet the common-root model contract. |
| Total fallback output length `B poly(I+b)` | `03:540` | Pending; `B` is an exponential work multiplier, not a bound independent of added precision. |
| All-fixed inputs before width maxima and division | `05:35`–`:41`, `:64`–`:65`, `:746`; actuator preprocessing | Pending direct branch. |
| Common descriptor permits sound singleton-hull fixing | `02:248`–`:249`; `05:112`, `:587` | Pending alignment. |
| Order transport replaces box property (P1) | `06:24`–`:25`, `:598`–`:600` | Pending introductory correction. |
| Scope of hardness/threshold explanation | `05:903`–`:906` | Pending explicit relation to the worked gap family. No new literature conclusion is made here. |

## Verified proof coverage

"Verified" below means that I re-derived the mathematical implication in
the frozen text, under its explicit valid premises and the classical
theorems it cites. It does not mean that literature identities or the
whole paper have been approved. Where a repair is necessary, the affected
literal claim is identified as not verified.

| Proof component | Frozen locator | Coverage |
| --- | --- | --- |
| Clipped coordinate grids, integer singletons, allowed-grid identity | `05:180`–`:246` | Verified for nonempty positive-dimensional preprocessed boxes. |
| Sparse messages and globally consistent min-marginals | `05:248`–`:314` | Verified; bounded-degree passes process stored rows without Cartesian products of adjacent tables. |
| Mean rounding, global error, pruning, witnesses | `05:320`–`:423` | Verified on every draw, including ties. |
| Deterministic-grid expectation and atomic correction | `05:427`–`:531` | Verified; no conditioning on adaptive survival. |
| Box closure soundness and stopping event | `05:573`–`:701` | Verified; original bounds, integer fixing, and free Hessian are used correctly. |
| Sparse base schedule, same-draw fallback, expected work | `05:710`–`:829` | Verified conditional on known shared fallback integration and valid `L`. |
| Convex-patch evaluator and quadratic face enumeration | `C:61`–`:272` | Verified; repairs weak feasibility and boundary/erosion effects, and handles quadratic ties. |
| Expanded chart decomposition | `D:9`–`:39` | Verified with the constant/parent-count clarifications in S5. |
| Explicit graph reduction and lift | `D:41`–`:81` | Verified conditional on known uniform-family and fallback corrections. |
| Implicit root smoothness, derivatives, oracle | `D:83`–`:144` | Verified; no exact algebraic-sum ordering is assumed. |
| Certified lower DP, count, and closure | `D:146`–`:200` | Verified; current incumbent-point wording needs S5. |
| Implicit active-root and growth tails | `D:202`–`:276` | Verified, including the bordered Jacobian and conditional noise. |
| Implicit every-draw output and evaluation | `D:278`–`:300` | Verified for positive-dimensional patches; point evaluation needs S4. Shared-root fallback remains pending. |
| Actuator invariance, adjoint, coefficients, trajectory distance | `D:304`–`:345` | Verified conditional on known curvature and family premises. |
| Simplex rounding and directional face count | `D:357`–`:444` | Fine-grid proof verified; coarse definition not verified until S2. |
| Simplex forcing, patch, and stopping | `D:446`–`:527` | Forcing and weighted Hessian implication verified; construction and equality-margin wording need S1/S3. |
| Simplex transformed-tuple margin count | `D:529`–`:573` | Verified for active inequalities; literal inclusion of equality multipliers is false. |
| Simplex schedule/evaluation | `D:575`–`:621` | Conditional on S1–S4 and known shared interfaces; not approved literally. |
| Mixed-order rounding, transport, sharper count | `D:631`–`:773` | Verified, including binary labels and tie faces. |
| Slice exposure, propagation, weighted closure | `D:775`–`:897` | Verified on every draw after binary singleton fixing. |
| Finite exposure gaps and order schedule | `D:899`–`:966` | Verified; direct finite sum-fiber count gives the required `2/M`. |
| Order rational repair and physical distance | `D:968`–`:994` | Verified for nonzero patch dimension; direct point branch needs S4. |
| TU preliminary rounding | `06:712`–`:728` | Verified at the stated integral, aligned, continuous scope only. |

## Re-derivations that support the coverage decisions

### Graph expansion and uniform conditioning

For retained `x_i`, the expanded occurrence set is the union of the
original occurrence subtrees of `x_i` and all its dependent descendants.
Consecutive parent-child occurrence subtrees intersect at the bag
containing the child's constraint scope. Therefore the union is connected,
even when the substitution has multiple paths. Factor scopes expand into
the union of their ancestors. Fixed depth and degree give polynomially
many explicit monomials; their coefficient heights are polynomial, not
necessarily bounded by the literal `I+b`.

Conditioning on dependent-coordinate noise leaves every retained ambient
coefficient independent with its original finite marginal. Uniform
curvature and derivative bounds are taken over all conditioned draws
before the law is selected. An arbitrary invertible change of ambient
coordinates would not supply this independence, and the manuscript does
not use one in these reductions.

### Implicit charts, pruning, KKT roots, and evaluation

The global monotonicity floor and endpoint signs give one root. The local
implicit function theorem agrees with that root at hull boundaries, so
two-sided derivatives there are legitimate. Differentiating the equation
through order three gives the displayed bounds. Value, gradient, and
Hessian entries are rational expressions at the roots with denominators
bounded away from zero on the whole hull times the bracket box. Root
bisection plus a rational derivative bound for each expression gives
certified enclosures in polynomial bit time. For a Hessian operator error
`epsilon_H`, entry precision at most `epsilon_H/n` followed by
symmetrization suffices; this conversion fits the oracle's work bound.

Let `H^-` be the sum of certified lower row costs and `D_j<=E_j` its total
error. The fixed-cell rounding gives `q_C^- - E_j <= G(x)`. The current
grid minimum gives a certified upper bound `m_j^-+E_j`; induction then
preserves every optimizer. A retained cell has a globally consistent
witness of true gap at most `4E_j`, yielding the interval factor `1+n`.
All deleted points have objective above a feasible certified upper bound;
different root brackets in different bags do not change the unique chart
whose row costs they enclose.

The larger witness tolerance gives distance
`h sqrt(nL/(2g_0))`, still bounded by the chosen `A h`. The old cap leaves
gradient margin at least `tau/4` after the two gradient errors and matrix
margin at least `g_0/4` after the two Hessian errors. For the active tail,
fix integer labels and a retained box face. The polynomial KKT system in
free coordinates, dependent coordinates, and graph multipliers has
`k+2m` variables and degree at most `max{2,d,e}`. Its constraint Jacobian
has invertible diagonal `q_y`. On the constraint tangent space, its
Lagrangian Hessian is the positive definite reduced Hessian supplied by
point growth. The bordered Jacobian is consequently nonsingular. Varying
the active coordinate's own coefficient leaves that stationary system
fixed and varies the active derivative with slope one. This proves the
root-count tail without assuming that other stationary components are
finite or that the reduced objective is polynomial.

For a positive-dimensional implicit patch, GLS value error
`min{2^-q, (g_0/2)(2^-q/(2K_psi))^2}` bounds retained distance and hence
exact lifted distance by `2^-q/2`. Total dependent root-bracket width
`2^-q/2` gives a rational ambient approximation within `2^-q`. Exact
feasibility belongs to the rational-anchor/algebraic-root lift, not to
the separate ambient rational approximation. For fallback evaluation,
choose retained coordinate error at most
`2^-q/(4n max{1,K_psi,G'})`, where `G'` bounds the reduced gradient's
one-norm. Clipping and exact integer extraction preserve this error;
the lift has the required distance and objective gap. The added precision
has polynomial encoding length and is paid by the same fallback factor.

### Actuators

Backward substitution of affine state recurrences gives the displayed
adjoint identity, including signed transition coefficients. The uniform
adjoint magnitude is `(C_s+sigma)/(1-a)`. It adds only unary polynomial
terms to the free objective for every horizon. Products of the supplied
rational transition coefficients add denominator lengths; the recurrence
does not square old denominators. Rational free approximants therefore
give rational exactly feasible trajectories of polynomial encoded length.
The geometric convolution matrix has row and column sums at most
`1/(1-a)`, giving the stated encoded Lipschitz bound. The objective gap
transfers by the exact adjoint identity.

### Simplices after the stated repairs

A fine cell scales to a unit cube with an integral sum cut, whose vertices
are cube corners. A mean-preserving distribution on them fixes coordinates
on grid hyperplanes and hence all overlapping bag whitelists. Blockwise
independent rounding and the block Hessian bound give the global
`nLh^2/8` allowance. A tight face has directions `e_i-e_anchor` of squared
norm two; a slack face uses `e_i`. Conditional anchor noise leaves a
different independent coefficient in each tested direction. Each face of
dimension `r` has `binom(1/h-1,r)` relative-interior grid points, which
cancels the `h^r` probability. Finite atoms contribute at most
`1/(Mh)<=1` under the geometric cutoff. The outside domain is fixed
because every bag contains entire blocks.

For the repaired active-inequality margin event, face stationarity depends
only on tangent noise. The transformation to differences and normal
coefficients is injective but does not preserve independence. Counting
at most `(2M-1)^k M^{n-k-1}` transformed tuples and at most
`tau(M-1)/sigma+1` normal labels per root gives
`2^k D^k(tau/sigma+1/M)`. Positive growth makes the actual face root
nonsingular. Equality-budget multipliers must stay outside this event.

The zero-coordinate and tight-inequality tests use feasible directions of
the original simplex, not artificial hull bounds. The patch Hessian
subtracts `(kappa_3 r^P+g_0) Z^T Z`, so it certifies curvature in the
physical metric after anchor elimination. Once empty and zero-dimensional
blocks are removed, the displayed rational center is strict in every
remaining inequality. Its rational slacks supply an encoded inner radius.
Projection onto the box-plus-sum slab is an exactly computable rational
repair: sort its clipping breakpoints and solve one linear equation.
Euclidean nonexpansiveness gives both feasible evaluation and fallback
distance/value-gap control.

### Mixed orders

The shared rounding threshold is monotone, fixes zero/one and all grid
nodes, and preserves both order constraints and every candidate cell.
Only continuous coordinates move, so its global allowance is
`n_c Lbar h^2/8`. In a fixed order-simplex face, the endpoint-preserving
piecewise-affine transport applies to one conditional attaining point.
Every moving coordinate has rate in `[0,1]` along a tie-block direction;
all binary coordinates remain fixed. Its second derivative is at most
`n_c Lbar`, regardless of the number of bag coordinates. The transported
fiber need not exhaust the true fiber; the upper support suffices.

The two comparisons confine one tie-block noise sum to an interval of
length `3 n_c Lbar h/2`. Disjoint direction supports permit conditioning
on all but one coefficient in each support. Each face has at most
`h^-k/k!` relative-interior grid points. Summing over face dimensions and
permutations gives exactly the stronger bracket
`[2+3 n_c Lbar/(4 sigma)]^{p_c}`, with `p_c! (p_c+1)` and only a
constant-base binary factor. This specializes to the continuous theorem.

Exposure is performed only after every binary hull is a singleton. The
continuous slice has zero-one vertices; if a proposed equality fails at
an optimizer, the face exposed by its true gradient has an opposite-face
vertex. This gives the threshold `n_c kappa_2 r`, and the exposure gap is
`n_c`-Lipschitz in the gradient's infinity norm. Merging active equalities,
contracting cycles, and propagating interval bounds preserves every
optimizer. Once forced singletons are removed, every remaining inequality
has a feasible point where it is strict, so the patch is full-dimensional.

For active-edge margins, vary two coefficients at fixed sum. The minimal
face stationary system stays fixed; the exposure gap at a counted root
varies with slope minus one. Counting the entire finite sum fibers gives
`tau/sigma+2/M`; it does not assume a uniform conditional density on a
sum fiber. Positive growth gives nonsingularity on the minimal face.
Empty opposite faces impose equalities already valid throughout the
slice and need no finite-gap event.

The block copy matrix has disjoint zero-one columns. Hessian variation
is bounded by `kappa_3 r_y D^T D`; the matrix test and stopping proof keep
that metric. Inactive inequalities remain in the patch, so no lower bound
on their slack is assumed. The rational inner-center LP has polynomial-bit
data. Clipping followed by predecessor maxima preserves feasibility and
infinity error once binary-forced bounds have propagated. The evaluation
tolerance charges `||D||_2<=sqrt(n_c)` to obtain the claimed physical
Euclidean distance.

## Law, cutoff, and bit-budget check

The graph, simplex, and order constants have logarithms polynomial in
base length: their face counts, bounded integer-label counts, nonsingular
root counts, and semialgebraic section bounds depend on format, not
sampled coefficient heights. Uniform derivative bounds are encoded
before sampling. With `B` fixed first, `rho=1/(4B)`, the displayed growth
and margin thresholds and the minimum required mesh have polynomial
encoding length. The least sufficient geometric level `J` is therefore
polynomial in `I`, and the least sufficient power-of-two `M` has
`log M=poly(I)`. For orders, the larger normal-fiber atom requires and
receives `M>=4K_preorder/rho`, rather than the box correction `2K/rho`.

At every level, generated cell and row counts are constant-base factors
times previous retained counts. Costs and sort keys have polynomial bit
length. Expected work follows from a deterministic full-grid count and
linearity of expectation. It does not require independence of the
adaptive lists. The exceptional probability is at most `2rho=1/(2B)`;
the factor `B` cancels in expected construction and arbitrary-precision
evaluation work. The same draw is always used for fallback. Requested
evaluation accuracy `q` does not change the sampled law.

The inner radii used for successful evaluations may be small in magnitude,
but their rational encoding lengths are polynomial. GLS uses their
encoding lengths and the verified modulus; it does not enumerate a mesh
proportional to a condition number. This distinction is preserved in the
actual evaluators, subject to the point branches in S4.

## TU scope and review limits

The TU paragraph proves only aligned continuous feasible rounding. For
integral TU `A`, integral `b`, and `h=2^-j`, the scaled cell has integral
right-hand side `b/h-Ak`; appended coordinate bounds preserve total
unimodularity. Its vertices are feasible cube corners. Mean rounding
fixes boundary nodes and, with a full Hessian upper bound along feasible
segments, gives `n Lbar h^2/8`. Bag-contained constraints permit the same
whitelist pruning. No input-controlled expected count, complete closure,
or margin theorem for arbitrary TU systems is proved or claimed here.
Rational right-hand sides and arbitrary mixed integer levels require
additional alignment/model work and are outside this preliminary result.

I verified the needed finite-section transfer and scalar canonical
fallback interfaces in Appendix A conditional on the cited classical
quantifier-elimination and root-isolation results. The common-root
conversion remains a known absent integration step in this snapshot;
I did not approve an unseen integration. I did not verify bibliography
identities, novelty, unrelated routes, or final packaging.

The actual targeted checks were numbered file reads and a Python manifest
check of SHA256 and byte counts for the seven listed files. No literature
search, experiment or saved-diagnostic rerun, delegation, TeX edit,
compilation, CI inspection, or project-wide check was performed. The only
written artifact is this review report. The final repeated integrity check
again matched all seven snapshot hashes and byte counts. The targeted
report check passed final-newline, trailing-whitespace, and paired-fence
checks.
