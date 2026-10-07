# Supplemental audit: the two-inertia capped-moment theorem

Date: 2026-10-05. Reviewer: Sol. This report preserves the conclusions of
prewrite-lowrank-sol.md and resolves the requested dependence question in
expected-smoothed-qp.md. No literature search, experiment rerun, or
manuscript edit was performed.

## Verdict

There is no mismatch between the claimed deterministic conditioning power
`Z^(k/2)` and the actual cell count when k is one or two. The source
algorithm's explicit retained-cell bound is

    2^r (sqrt(r kappa)+4)^r,

where r <= k is the number of auxiliary coordinates remaining after fixed
coordinates are removed. Its intrinsic normalization gives
kappa <= 2+4nu/g_* <= 6Z, with Z=max(1,nu/g_*). Child generation,
corner queries, and coordinate-reconstruction attempts introduce only
absolute constants when r <= k <= 2. Consequently the per-level cost
has the required numerical factor Z^(k/2), not Z^k. Arithmetic and
exact-recovery depth introduce only a fixed power of 1+log Z.

The finite rational-grid theorem in the historical note is sound. The
continuous proximal probability theorem alone is not a Turing exact-bit
algorithm on real coefficients. Its rational counterpart is provided by
uniform section complexity and finite-law transfer, with atoms paid by
the same-draw fallback. An optional extension to the finite Gaussian-like
law is proved in Section 5 below; it permits the old numerical bound to
share the manuscript's principal law if the precision budget is enlarged.

The older result is not wholly subsumed by closure. It gives linear
dependence on nu S/sigma for k <= 2, whereas the new Gaussian-weighted
closure count has degree k in a diameter ratio. Closure removes the
two-inertia restriction and gives an ambient-dimension-free FPT bound.
These are different numerical conclusions.

## 1. The deterministic growth-conditioned bound, unpacked

Let L be the rational length of one perturbed QP instance. Suppose its
optimizer x_* is unique and its global growth modulus g_* is positive.
The scalar perturbation changes the linear coefficient only, so its
Hessian, negative inertia k, and negative curvature nu are those of the
base matrix. The cases k=0, singleton feasibility, or no remaining
nonconstant auxiliary coordinate use a deterministic polynomial branch.
Below assume k in {1,2} and r in {1,...,k}.

The rational normalization constructs a contraction T and alpha with
2nu <= alpha < 4nu. For

    W(a)=min_X [F_xi(x)+alpha||a-Tx||^2/2],

the growth-transfer calculation gives

    W(a)-F_xi* >= g_W ||a-Tx_*||^2,
    g_W = g_* alpha/(2g_*+alpha||T||^2),
    kappa = alpha/g_W
          = 2+alpha||T||^2/g_*
          <= 2+4nu/g_* <= 6Z.                         (1)

The full matrix norm used in preprocessing affects polynomial input
precision. It is not an extra inverse-growth factor in (1).

At level j, let h_j=s 2^(-j), where s is the largest nonconstant
auxiliary side length. The historical growth algorithm uses a regular
isotropic lattice, with at most one clipped terminal interval per
coordinate. Its corrected-corner error is

    delta_j = r alpha h_j^2/8.

After original feasible witnesses update the incumbent U_j, every
retained cell has a corner v satisfying

    W(v)-F_xi* < 2delta_j,
    ||v-Tx_*|| < h_j sqrt(r kappa/4).                  (2)

This uses the original feasible incumbent, which can be smaller than
the auxiliary corner value. The proof still works: if U_j>F_xi*, an
optimal auxiliary cell survives and gives U_j<=F_xi*+delta_j; if
U_j=F_xi*, the same inequality is automatic.

An interval of radius h_j sqrt(r kappa/4) contains at most
sqrt(r kappa)+4 coordinate nodes of the regular lattice plus its clipped
terminal endpoint. The enclosing coordinate box therefore contains at
most (sqrt(r kappa)+4)^r grid nodes. Each corner is incident to at most
2^r cells. This proves the written retained-cell bound directly.

For r <= k <= 2 and Z >= 1, (1) gives

    2^r (sqrt(r kappa)+4)^r
       <= 4 (sqrt(12Z)+4)^r
       <= C Z^(r/2) <= C Z^(k/2),                    (3)

with an absolute C. At the next level each retained cell has at most
2^r children and each processed child has at most 2^r corners. At fixed
k <= 2 these multipliers are bounded constants. There is no operation
enumerating another k-dimensional grid per retained cell, and no extra
power of kappa is hidden in the processing step.

### Exact stopping depth and arithmetic

The smallest-optimal-face argument supplies a rational original optimizer
and optimum value of uniformly polynomial height. A relative-interior
minimizer on a smallest-dimensional optimal face has positive definite
tangent Hessian, or is a vertex; a null tangent would preserve the
quadratic until a smaller face is reached. An independent active-row
basis then gives a nonsingular rational stationary KKT system. Universal
determinant bounds give computable denominator bounds V for F_xi* and
R for every coordinate of the common auxiliary optimum a_*=Tx_*, with

    log V, log R <= Q(L)

for a fixed polynomial Q. The rational normalization and LP bounds also
give log-positive-size bounds for alpha and s polynomial in L. These
height bounds are derived from input matrices, not by face enumeration.

Once delta_j < 1/(2V^2), bounded-denominator reconstruction isolates
F_xi* inside the certified interval [lower_bound,U_j]. If the original
incumbent has that value, stop. Otherwise an optimal auxiliary cell
continues to be processed, and the best queried auxiliary corner v_j
satisfies

    ||v_j-a_*||^2 <= delta_j/g_W
                   = r kappa s^2 4^(-j)/8.            (4)

After the right-hand side is smaller than 1/(16R^4), coordinate
reconstruction in radius 1/(4R^2) intervals finds a_*. Evaluate the
convex recourse there and accept only a feasible witness whose original
objective equals the already isolated F_xi*. Premature candidates are
harmless. At a_* every recourse optimizer attains the original optimum
by square completion.

The sufficient value and coordinate conditions give

    J <= Q_1(L)+C_1 log kappa
       <= Q_2(L)+C_2 log Z                            (5)

with fixed polynomials and absolute constants for k<=2. The algorithm
does not need g_* or J to run; it attempts certified reconstruction at
successive levels. Its accepted answers are sound even at zero growth.

Level-j corners have rational bit length polynomial in L+j. The exact
convex-QP primitive, rational reconstruction, witness comparisons, and
bookkeeping therefore cost at most Q_3(L+j) per processed unit for one
fixed polynomial Q_3. Each query is formed from fixed matrices and the
current dyadic coordinates. Incumbent selection does not multiply all
oracle denominators together.

Combining (3)--(5) and summing the levels gives

    T_fast <= C Z^(k/2)(J+1)Q_3(L+J)
            <= P(L) Z^(k/2)(1+log Z)^d,               (6)

where d and P are absolute and uniform for k<=2. This is the needed
proof behind equation (8) of expected-smoothed-qp.md. Reading only the
coarser statement f(k,nu/g) poly(L) would not justify the exponent; the
explicit packing and recovery inequalities do.

## 2. Always-correct fallback and capped bit work

Let m be the number of supplied inequalities and B=max(2,2^m).
Enumerate all independent active-row subsets. For every nonsingular
stationary KKT system, retain its point if feasible and take the least
exact objective value. The smallest-optimal-face argument ensures the
list contains an optimum even with redundant rows, singular ambient
Hessian, lower-dimensional feasibility, or a continuum of optima.
Multiplier signs need not be checked in this enumeration because every
retained point is feasible. Each candidate takes polynomial rational
work. Hence

    T_fallback <= B P(L),                             (7)

after enlarging the polynomial in (6).

Interleave elementary bit operations of the two fixed programs on the
same draw. Two known machines can be simulated with a constant step
schedule on separate tapes; no entire uninterruptible oracle call must
finish before the other program resumes. Additional implementation
simulation costs, if used, can be absorbed into the fixed polynomial.
This needs neither a supplied g_* nor knowledge of P or running times.

For eta=k/2 in {1/2,1}, set Z=infinity at zero growth. Up to an absolute
factor, total work is bounded by

    P(L) min[B,Z^eta(1+log Z)^d]
    <= P(L)(1+eta^(-1)log B)^d min(B,Z^eta).            (8)

If Z^eta<=B, log Z<=eta^(-1)log B; otherwise the left side is at
most B. Equation (8) includes g_*=0 by its limiting convention. It
prevents arbitrarily small growth from forcing unbounded arithmetic
precision before the fallback completes. The probabilistic calculation
is about this capped runtime, not the uncapped growth solver.

## 3. Precise rational uniform-grid theorem

Let the base instance be a rational QP on a nonempty bounded rational
polytope, with k=n_-(A)<=2, rational sigma>0, and base input length I.
Let S be the sum of feasible coordinate widths. Put

    F_faces=2^m, D=8(F_faces+1)^2, B=max(2,2^m).

Choose **any** power of two M>=2nDB whose logarithm is polynomial in
I, and independently sample each original coefficient perturbation
uniformly on the M-point endpoint grid of [-sigma,sigma]. The least
sufficient power of two has log M=O(m+log(n+1)).

There is an always-terminating exact rational algorithm for the sampled
objective with expected bit work

    (I+1)^C (1+nu S/sigma)                            (9)

for an absolute C uniform over k<=2. It returns a feasible rational
optimizer and exact rational value for every draw, including ties.
Neither g_*,nu nor S must be supplied. The output solves the sampled
objective. Convex instances use one exact convex-QP solve.

To prove (9), use the proximal theorem and its uniform one-coordinate
bad-growth section count D to get, on this one fixed grid,

    Pr(g_*<epsilon) <= (S/sigma)epsilon+beta,
    beta=2nD/M, beta B<=1.                            (10)

The section count is independent of the threshold, fixed coefficients,
and grid precision. All polynomial-height sampled inputs obey one
uniform L<=Q_4(I), so P(L) can be bounded before taking expectation.
The grid is selected against B, not against a recovery denominator
bound depending on M.

Set r_0=nu S/sigma. For t>=1, (10) gives Pr(Z>t)<=r_0/t+beta.
The bounded tail integral yields

    E min(B,Z^eta)
       <= 1+r_0 integral_1^B t^(-1/eta) dt+beta(B-1).

For eta=1/2 this is at most 2+r_0. For eta=1 it is at most
2+r_0 log B. Since log B=O(m+1), (8) proves (9). All zero-growth
mass is included in beta B; no draw is discarded, resampled, or
conditioned on positive growth.

For k>2 this same moment proof produces a factor B^(1-2/k). It does
not establish polynomial expectation at larger negative inertia. That
limitation does not concern the later cell-closure proof.

## 4. Continuous probability versus exact Turing input

The sharp probability statement for independent continuous uniform
coefficients is valid:

    Pr(g_*<epsilon) <= (S/sigma)epsilon.

It can provide conditioning estimates in a separately specified real
arithmetic or oracle model. It does not supply exact real coefficients
or exact outputs as finite binary strings. For example, minimizing
x^2/2+gamma x over [-1,1] with continuous gamma has interior optimizer
-gamma, which is irrational with probability one conditional on being
interior. Exact rational optimizer/value language would be false there.

The historical expected-smoothed-qp theorem already states a finite
rational law, so no correction to its computational model is necessary.
When discussing its continuous proximal input, distinguish the
probability theorem from its Turing realization. Rational reconstruction
in (5) relies on rational sampled input and cannot simply be applied to
exact Gaussian or uniform real coefficients.

The finite-law residual in (10) is indispensable. Even a fine endpoint
grid can put positive mass at a tie. A high-probability conditioning
statement that ignores that mass cannot prove always-correct expected
bit work. For k=2 the continuous tail also does not bound the uncapped
inverse-growth moment: the integral of 1/t diverges. This says the
uncapped **bound** cannot be integrated, not that every such solver
must have infinite expectation.

## 5. Optional extension: the same linear bound under finite Gaussian-like noise

The two-inertia theorem can share the principal Gaussian-like law after
one extra accuracy requirement. This conclusion follows from the same
proof ingredients and does not require a new literature input.

Let each original coefficient law L_i be finite and rational, sampled
in bounded polynomial time with uniformly polynomial output bit length,
and have
Kolmogorov distance at most delta_i from an independent continuous proxy
law with density bounded by phi_i. For the QP bad-growth event, every
axis section still has at most D=8(2^m+1)^2 interval components.
One-coordinate CDF transfer and product telescoping therefore give

    Pr_finite(g_*<epsilon)
       <= a epsilon+beta,
    a=2 sum_i phi_i w_i,
    beta=2D sum_i delta_i.                            (11)

The count D is uniform in epsilon and in the fixed other coefficients,
including mixed real/discrete laws encountered during replacement.
Assume beta B<=1. Equations (6)--(8) and the same bounded moments then
give exact expected bit work

    poly(I)(1+nu a).                                  (12)

Every sampled objective is rational, and the same fallback handles all
atoms. The actual finite law need not have a density, and no transformed
coefficient independence is being assumed.

For the isotropic Gaussian proxy phi_i=1/(sigma sqrt(2pi)), so
a=sqrt(2/pi) S/sigma. Use the bounded rational Gaussian-like sampler
with accuracy b chosen so

    2^b >= 2nDB.

Its error delta<=2^(-b) makes beta B<=1, and its radius b+20 and
sampling work are polynomial. Here b=O(m+log(n+1)) suffices; no
critical-region curvature budget is needed for this moment argument.
Consequently (12) becomes

    poly(I)(1+nu S/sigma)

under this specified finite Gaussian-like product law, still for k<=2.
If the manuscript uses the finer law from Gaussian closure, add
2nDB to that law's accuracy budget. The support loop still terminates:
this extra budget has polynomial logarithm and is independent of trial
support. No additional precision circle arises. The two algorithms can
then target exactly the same sampled objective.

## 6. Scope decision and relation to later closure

Retain the theorem if the manuscript wants the stronger numerical bound
for k<=2. Its distinctive conclusion is the linear ratio nu S/sigma,
not a new rank range or a real-Gaussian exact-input model.

The Gaussian-like closure theorem has a count of the form

    C^k(1+nu diam(X)/sigma)^k

up to rank-dependent constants, and applies to arbitrary negative
inertia. At k=2 this has quadratic dependence on the diameter ratio.
The moment theorem has linear dependence on the summed-width ratio.
For a fixed domain and large curvature/noise ratio, that is a different
and potentially sharper numerical dependence. Since S<=n diam(X), it
also supplies an at-most-linear diameter-ratio bound with an additional
ambient-dimension factor absorbed into the input polynomial. Unknown
polynomial constants prevent a practical runtime comparison.

The original uniform-grid precision is determined by n,m alone, while
closure's grid also accounts for region curvature and terminal local-event
budgets. The moment theorem remains valid at any finer common endpoint
grid with polynomial log M. Thus closure and moment bounds can be
combined under a common sufficiently fine uniform law if desired.
Section 5 similarly combines them under one Gaussian-like finite law.

For k=1, the numerical degree is already linear in both approaches,
although the geometric quantities and perturbation laws differ. For
k>2, use closure; the capped-moment calculation does not imply a
larger-rank theorem.

Recommended manuscript statement: an exact finite-law two-inertia
corollary with bound (9), followed by a short explanation that closure
allows any negative inertia while the two-inertia moment argument offers
a sharper numerical bound. Do not label the older result fully
superseded, and do not infer it solely from a generic f(k,nu/g) bound.
If length requires omitting it, mark it as an intentionally omitted
distinct quantitative refinement in the coverage record, not an invalid
or subsumed theorem.

## 7. Targeted verification record

I reread expected-smoothed-qp.md and the packing, exact-recovery, and
finite-tail sections of negative-inertia-qp.md and proximal-growth-tail.md.
The checks above are analytic derivations of the conditioning power,
bit-depth bound, capped moments, and rational Gaussian-like transfer.
The commands used were scoped cat, sed, and rg reads. No original
diagnostic, computational experiment, literature search, project-wide
check, or CI inspection was run.

A scoped `python -` read only this report and checked its final newline,
absence of trailing whitespace, paired code fences, and the expected
conditioning/grid-budget content markers. It passed on the 371-line
report before this verification paragraph was appended.
