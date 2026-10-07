# Prewriting mathematical audit: low-negative-inertia exact closure

Date: 2026-10-05. Reviewer: Sol. Scope: the requested low-rank QP,
MIQP, and mixed separable proof chain. This is an independent mathematical
reconstruction, not a literature or priority assessment.

## Verdict and changes recommended before manuscript writing

I found no fatal mathematical defect in the stated finite-law closure
results. The intrinsic Gaussian-like QP and MIQP conclusions are supported,
subject to the exact convex-QP and fixed-integer-dimension convex-MIQP
primitives specified below. The separable result with arbitrarily many
integer coordinates is also supported under its explicit rational-piece
model and product-domain assumptions.

There is one substantial simplification worth incorporating. The condition
`ker(P) subset ker(T)` in the continuous and general mixed closure notes
is unnecessary. It was used to make the continuous envelope differentiable,
but the needed estimate holds for **every attaining witness**, without
envelope differentiability. Optimal-set vertex extraction and scalar-section
counts also do not require that kernel inclusion. Section 3 below proves
the corrected common lemma. The intrinsic normalization supplies the
condition anyway, so removing it broadens the supplied-decomposition
statement and simplifies the main proof without changing the intrinsic
corollary. This is an avoidable restriction, not an error in the historical
theorems.

The most consequential manuscript risks are scope errors rather than broken
inequalities:

- The actual perturbation is one specifically constructed **finite rational
  product law**, fixed before sampling. Its accuracy and support are chosen
  using base-instance budgets. An exact real Gaussian is a proxy in the
  proof. The result does not cover arbitrary coarse Gaussian approximations
  or arbitrary density-bounded ambient laws.
- Exact correctness holds on every atom because of certified closure and an
  exact fallback on the same draw. The expectation is taken over all draws,
  including ties. No conditioning on successful optimization, rejection of
  difficult instances, or new objective perturbation is permissible.
- Uniform ambient noise gives the displayed rank-dependent powers of ambient
  dimension. That theorem is not an FPT theorem in negative inertia and a
  dimension-free numerical ratio. Gaussian weighting removes that loss.
- The separable theorem uses the rank and curvature of a **supplied concave
  factor**, not automatically intrinsic negative inertia or negative
  curvature of the full objective. Its rational breakpoints and product
  domain are essential.
- Optimizing the sampled objective exactly does not recover the unperturbed
  optimizer or improve the worst-case accuracy dependence for that problem.

No defect requires stopping the paper. None of these observations licenses
a claim of publication priority. The root should obtain the literature
judgment through the designated Luna lead.

## 1. Exact theorem contracts to use

### 1.1 Main intrinsic QP/MIQP contract

The input is a symmetric rational matrix A, rational vectors and constants
defining

    F(x) = x^T A x / 2 + b^T x + c,
    Pset = {x in R^n : Mx <= d},
    X = Pset intersect (Z^p times R^(n-p)),

where Pset is bounded, X is nonempty, and sigma is positive rational. The
base input length I includes sigma and all expanded rational data. Put
k = n_-(A) and nu = max(0,-lambda_min(A)). Empty feasibility can be
handled separately by the exact convex-MIQP primitive; nonemptiness can
instead be stated as a promise.

If k = 0, solve one exact convex QP or convex MIQP. If k > 0, deterministic
polynomial-bit preprocessing constructs rational alpha and a rational
k-by-n factor T with

    2 nu <= alpha < 4 nu,
    (63/64) I_k <= TT^T <= I_k,
    P = A + alpha T^T T >= 0.

The preprocessing does not need a real eigenbasis, nu, or a nonzero
eigenvalue gap as additional input. The factor has exactly k independent
rows. Its rational encoding length is polynomial in I.

There is a deterministically computed scalar finite rational law L,
sampled in bounded polynomial time with fair bits, such that independent
gamma_i drawn from L yield an always-terminating exact algorithm for
F_gamma(x) = F(x) + gamma^T x. Its output is an expanded rational feasible
optimizer and its exact rational value. Both have polynomial encoding
length. For suitable absolute constants C_0,C_1, the expected bit work is

    f(p) C_0^k (1 + H_G) (I+1)^C_1,

where the factor f(p) comes only from the established exact convex-MIQP
primitive, and

    H_G = product_i [2 + c_frame^(-1/2) (2 C_k+4)
                         + C_k alpha (u_i-l_i)/(sigma sqrt(2 pi))],
    C_k = 1+2k,
    c_frame = 63/64,
    l_i = min_Pset (Tx)_i,  u_i = max_Pset (Tx)_i.

The factor f(p) is absent for continuous QP. In particular, this is of
the form

    f_1(p,k,1 + nu diam(Pset)/sigma) (I+1)^C_1.

The polynomial exponent is independent of p and k. The numerical ratio
is a parameter in its actual magnitude; binary encoding alone does not
make an arbitrarily large ratio harmless. Growth, uniqueness, genericity,
strict complementarity, full-dimensional feasibility, and a supplied
independent global certificate are not assumptions.

The law is explicitly described by a bounded sampler and base-data
support/precision calculation, not by an exponentially long list of atom
masses. If Gaussian resemblance is stated formally, every coordinate has
Kolmogorov distance at most 2^(-b) from N(0,sigma^2), where the base-chosen
accuracy b is polynomially bounded in I. L is not an exact Gaussian.

For a supplied decomposition, the same theorem holds with rational alpha,
P = A + alpha T^T T >= 0, and a frame promise c_frame I <= TT^T <= I,
with fixed positive c_frame. The kernel inclusion can be omitted by the
proof in Section 3. The intrinsic conclusion uses normalization, not a
claim that an arbitrary supplied row number is minimum.

### 1.2 Aligned and uniform-ambient variants

Aligned noise perturbs the original linear coefficient by T^T xi, with
independent scalar factor coordinates xi_i on one base-chosen endpoint
grid in [-sigma,sigma]. It gives exact output at every draw and expected
work

    C^k (1+H_aligned) poly(I),
    H_aligned = product_i [3+(1+2k) alpha w_i/(2 sigma)],
    w_i = range_X(Tx)_i + 2 sigma/alpha.

For continuous QP this is an FPT bound in k and the displayed ratios,
under rational PSD recourse. It is a low-dimensional correlated law in
the original coordinates. It must not be described as independent
ambient coefficient noise.

Independent uniform original coefficients require a different proof and
different precision budget. Their expected count is

    H_ambient = product_i [2+(1+2k) alpha sqrt(n) w_i/(2 sigma)],
    w_i = range_Pset(Tx)_i + 2 sigma ||D_i||_1/alpha,
    D = (TT^T)^(-1)T.

After intrinsic normalization, this has a bound containing n^k. It is
polynomial for each fixed k under numerical bounds, with a rank-dependent
ambient-dimension exponent. For mixed recourse, multiply the oracle work
by f(p). The distinction from the Gaussian-like FPT result is real.

### 1.3 Mixed separable contract without an integer-count parameter

The input domain is a product of rational continuous intervals and
integer intervals with binary endpoints. Every unary phi_j is continuous
and convex, supplied by an explicit list of rational quadratic pieces
and rational breakpoints covering its interval. One-sided derivative
ordering and nonnegative piece curvatures are part of the model and can
be checked exactly. The objective is

    F(x) = sum_j phi_j(x_j) - alpha ||Tx||^2/2,

with rational alpha > 0. Round integer endpoints inward, reject empty
domains, and remove fixed coordinates first. The full-row-rank promise
on T applies **after** this preprocessing. Otherwise deleting columns
can destroy row rank. Fixed coordinates contribute affine and constant
terms and preserve unary convexity.

For k > 0 and full-row-rank T, no norm or conditioning promise is needed.
Put beta = alpha ||T||^2. A finite independent rational Gaussian-like
ambient product law gives exact rational output on every draw and expected
work

    f(k,1 + beta diam(X)/sigma) poly(I)

with an absolute polynomial exponent and no parameter for the number of
integer coordinates. The k = 0 branch separates. The parameters are those
of the supplied decomposition. The algorithm does not establish a
minimum-rank representation or remove dependent supplied rows.

This contract excludes coupled constraints and a general dense convex
residual. Rational polynomial coefficients without rational breakpoints
would not suffice: max(0,x^2-2)-x on [0,2] uniquely minimizes at sqrt(2).

## 2. Rational normalization reconstructed

Let A have rank d > 0 and let H >= ||A|| be a positive rational bound.
Clear the denominators of A by a positive integer D_0. The coefficient
of t^(n-d) in det(tI-A) is, up to sign, the product of its d nonzero
eigenvalues. Multiplying that coefficient by D_0^d gives a nonzero
integer. Consequently every nonzero eigenvalue has magnitude at least

    mu = D_0^(-d) H^(-(d-1)).

This proof works also for H < 1. mu <= H, and log(H/mu) has polynomial
input size. A denominator product suffices; no eigenvalue isolation
oracle is being hidden.

Find the exact rational range projector

    R_A = C(C^T C)^(-1)C^T

using independent columns C of A. Return early when A is PSD. Otherwise
halve a rational beta, starting from H, while A+(beta/2)I is PSD. Exact
PSD testing makes the final beta satisfy nu <= beta < 2nu. The number
of halvings is O(1+log(H/mu)), not necessarily O(log n). A large positive
eigenvalue beside a small negative eigenvalue is charged through input
precision rather than a nonconvex numerical multiplier.

Use exact rational orthogonal Jacobi rotations to obtain Q with

    Q^T A Q = diag(a_j) + E,  ||E|| <= e,
    e = mu^2/(16 n beta).

The rotation parametrization

    c_t=(1-t^2)/(1+t^2), s_t=2t/(1+t^2)

is exactly orthogonal. Its quartic off-diagonal numerator has opposite
signs at the stated bracket endpoints; bisection uses the full H in
its derivative tolerance. Reducing a maximum off-diagonal entry below
half its prior magnitude contracts off-diagonal Frobenius energy by a
factor at most 1-3/[2n(n-1)]. Hence there are polynomially many rotations.
Their common denominator bit lengths add under multiplication; they do
not recursively square the entire prior denominator at each step.

Eigenvalue perturbation selects exactly k columns B_- with a_j < -mu/2.
Writing Pi_- for the true negative projector as a proof device gives

    ||(I-Pi_-) q_j|| <= 2e/mu,
    ||B_- B_-^T-Pi_-|| <= 3n e/mu.

Set U = R_A B_-. The exact range projection is essential: if A is
diag(-1,0), a tilted unit column b gives det(A+2bb^T) < 0 whenever
its kernel component is nonzero. Approximation without exact range
projection would be an actual error.

On range(A), A+2beta Pi_- has minimum eigenvalue at least mu. Replacing
Pi_- by UU^T costs at most 2beta(3n e/mu)=3mu/8, leaving 5mu/8.
Both terms vanish exactly on ker(A). Thus P=A+2beta UU^T is PSD,
U has rank k, and ||U|| <= 1. With T=U^T,

    TT^T = I-B_-^T(I-R_A)B_- >= (63/64)I,

because the leakage squared is at most 4k e^2/mu^2 <= 1/64.
All matrix operations, bisection tolerances, and output lengths are
polynomial in the rational input length. alpha=2beta gives the required
intrinsic curvature bound. No central inequality failed this audit.

## 3. Common exact algebra and the removable kernel assumption

### 3.1 Active upper-model lemma, including nonsmooth envelopes

Let X be any nonempty compact mixed or continuous feasible set and let
L be positive definite. Define

    W_r(a) = min_x [F(x)+r^T x+(a-Tx)^T L(a-Tx)/2],
    V(a) = W_r(a)+d^T a.

At any a=v, every attaining witness x_v gives a global upper quadratic
Q_x touching V at v, with linear vector

    g_x = L(v-Tx_v)+d.

Since V <= Q_x pointwise, min Q_x >= min V. Exact minimization of Q_x
therefore gives

    g_x^T L^(-1)g_x <= 2[V(v)-min_R^k V].             (A)

This holds for every active witness, including integer ties, continuous
flat faces, knots, and nondifferentiable value points. No derivative or
subgradient selection of W_r is needed. For L=alpha I it reads
||g_x||^2 <= 2alpha[V(v)-V*].

Square completion with gamma=T^T d+r gives

    V(a) = min_x [F_gamma(x)
             +(a-Tx+L^(-1)d)^T L(a-Tx+L^(-1)d)/2]
             -d^T L^(-1)d/2.                        (B)

Thus the auxiliary whole-space optimum equals F_gamma* minus the stated
constant. Any support-enlarged box containing Tx-L^(-1)d for all feasible
x contains every auxiliary minimizer. An exact auxiliary witness transfers
its gap to an original feasible witness without increasing it. At an
exact auxiliary optimum the witness attains the original optimum.

### 3.2 Polynomial continuous active-basis extraction

For a convex QP with Hessian P >= 0, obtain an exact optimizer x_0 and
let g_0 be its gradient. Its entire optimal set is the rational polytope

    O = X intersect {P(x-x_0)=0, g_0^T(x-x_0)=0}.       (C)

The identity follows because the objective gap is the sum of a nonnegative
first-order term and a nonnegative PSD quadratic term. Choose a vertex x
of O by rational LP. The restriction of P to the tangent of the original
active face at x is positive definite: otherwise a nonzero null tangent
v permits both small feasible displacements x +/- tv. First-order
optimality annihilates v, so both displacements are in O, contradicting
vertexhood.

The polyhedral normal-cone formula supplies nonnegative active-row
multipliers without Slater or full-dimensionality assumptions. Reduce
linear dependencies in their positive support while preserving
nonnegativity, then extend that independent support to a basis J of the
full active row space with zero added multipliers. This proves
nonsingularity of

    K_J = [[P,M_J^T],[M_J,0]].

The solution to the parameterized stationarity system is affine:
x_J(a,r)=X_J a+Y_J r+z_J. Primal feasibility and nonnegative multipliers
define a closed polyhedron R_J(r) on which this response is globally
optimal. Substitution defines a quadratic extension q_J. The algebraic
gradient identity is

    grad q_J(a,r) = L(a-Tx_J(a,r)).                     (D)

Indeed, differentiate the active equalities M_J x_J=d_J. The multiplier
term cancels because M_J dx_J=0. This is an identity of the extension,
not an inference from equality on a lower-dimensional region.

None of (C), basis extraction, or (D) uses ker(P) subset ker(T). At a
queried parameter, (D) is an active witness vector, so (A) applies even
if W_r is nonsmooth. All later closure, hyperplane, and section arguments
use these statements. This proves the recommended removal of the kernel
assumption from both continuous and fixed-label mixed closure. One need
not prove C^1 smoothness as a separate manuscript lemma.

In a fixed integer slice the continuous Hessian is P_cc >= 0. The same
argument applies directly; kernel inheritance is no longer needed.
It remains true under the original promise, but should not occupy a
separate step in the main proof.

### 3.3 Exact quadratic face minimization and unconditional fallback

For any rational quadratic on a nonempty compact rational polytope,
choose an optimizer on a face of smallest possible dimension. It is in
the relative interior of that face. Tangential stationarity and local
minimality make the tangent Hessian PSD. A null tangent preserves the
quadratic until the face boundary is reached, contradicting minimality.
The tangent Hessian is therefore positive definite, or the face is a
vertex.

An independent active-row basis yields a nonsingular stationary KKT
system recovering this optimizer. Enumerating all independent row
subsets and retaining every feasible nonsingular candidate therefore
finds a global optimum. Multiplier signs and definiteness tests are
unnecessary for this fallback, because all retained candidates are
feasible and one is optimal. Rational determinants prove a uniform
polynomial-height optimizer and optimum value.

For a box in k coordinates, the same argument gives at most 3^k face
choices. Fix endpoint coordinates, solve nonsingular free stationarity
systems, and include vertices. This exactly minimizes a covered cell.
Singular faces can be skipped; another smallest optimal face provides
a nonsingular candidate. The dimension factor does not enter the
input-polynomial exponent.

For bounded MIQP, enumerate the LP-bounded integer label box and apply
the continuous fallback to feasible slices. For mixed separable piecewise
quadratics, also enumerate continuous listed-piece choices. Both have
an exponential multiplier B with polynomial log B and polynomial bit
cost per candidate. They terminate correctly at ties and atoms.

## 4. Grid, incumbent, and exceptional-hyperplane inequalities

### 4.1 Local counting and corrected-corner bounds

For scalar curvature alpha, use equal subdivisions with nominal
h_j=s 2^(-j). Each coordinate's subdivision count is the least power of
two making h_ij <= h_j. A refined coordinate has h_j/2 < h_ij <= h_j;
an unrefined coordinate has only its two endpoints. This avoids a
tiny clipped last interval in the probabilistic count.

Independent mean-preserving corner rounding and coordinate semiconcavity
give the valid cell lower bound

    L(C) = min_corner V(v)-B_j,
    B_j = alpha sum_i h_ij^2/8.

Process the whole level, update the incumbent with all corner and exact
closure values, then retain unresolved cells satisfying L(C) <= U_j.
If a global-optimal cell has been closed, the incumbent is already exact.
Otherwise an optimal cell is processed and gives U_j-V* <= B_j. Every
retained unresolved cell consequently has a corner satisfying

    V(v)-V* <= 2B_j.                                   (E)

All corners must be queried and their returned certificates tested. The
proof needs the failed certificate at the near-optimal corner; testing
only a different corner is insufficient. After no unresolved cell remains,
closed local minima and previously discarded bounds certify the exact
global auxiliary optimum.

At an interior deterministic grid node, neighboring comparisons with
tolerance delta restrict d_i to a fixed interval, conditional on residual
r, of length at most alpha h_i+2delta/h_i. With delta=2B_j,

    interval length <= (1+2k) alpha h_ij.

For independent aligned continuous coefficients, the intervals' endpoints
depend only on the base function, so independence multiplies their
probability bounds. For a finite endpoint grid an interval of length ell
has probability at most ell/(2sigma)+1/N. The extra atom contribution
is level-independent only while N >= m_ij. The fixed closure cutoff is
what makes that requirement attainable before sampling.

A corner lies in at most 2^k cells; a retained cell has at most 2^k
children; processing uses at most 2^k corner queries and 3^k local
face candidates. Counts over the entire deterministic level grid cover
all adaptively visited corners without an independence claim about the
search tree.

### 4.2 Why one unresolved cell gives one fixed hyperplane event

For a returned branch q_J with gradient H_J a+p_J(r), use a base-only
bound ||H_J|| <= H_0. The response matrix X_J, and hence H_J, depend
only on fixed KKT matrices and T^T L. The sampled linear coefficient,
label values, and residual noise affect offsets. They must not enter
the denominator-clearing step used to select H_0.

For example, clearing the fixed response entries and using Cramer's rule
for a system of order at most 2n gives U=(2n)! C^(2n), and the scalar
curvature estimate H_0=alpha(1+nkU). A determinant denominator is a
nonzero integer after scaling; its absolute magnitude is at least one.
The potentially huge numerical H_0 enters the refinement cutoff through
logarithms, not as a multiplier of expected near-optimal counts.

By (A) and (E), at a retained corner

    ||H_J v+p_J(r)+d|| <= alpha sqrt(k/2) h_j.

If H_J is invertible and the returned region does not contain the cell,
a nonzero region row c^T a+b(r)<=0, true at v, is violated elsewhere
in the cell. Its boundary meets the segment between these points and
lies within sqrt(k)h_j of v. The affine map a -> -H_J a-p_J(r)
sends this boundary to a hyperplane. A normalized normal is parallel to
H_J^(-T)c, and its offset is affine in r. The noise d is within

    sqrt(k)(alpha+H_0)h_j

of that image. If H_J is singular, choose a fixed unit vector in
ker(H_J^T); the entire affine gradient image is already contained in
a hyperplane, and the active-vector estimate gives the same bound.
Zero region normals cannot be violated elsewhere in a cell containing
the queried parameter. Singleton regions and redundant inequalities
are included.

Thus the event that **any** retained unresolved cell exists is contained
in a union of a base-finite collection of hyperplane tubes. There is no
additional union over visited cells. The collection may be exponentially
large, but its count K has polynomial logarithm. It is a proof object;
the algorithm need not enumerate it.

For full-row-rank T, write d=D gamma, r=Pi gamma with
D=(TT^T)^(-1)T and Pi=I-T^T D. A factor hyperplane has equation

    u^T d+v^T r+c_0=0,  ||u||=1.

Its ambient normal is w=D^T u+Pi^T v and Tw=u. When ||T|| <= 1,
||w|| >= 1. Factor tubes of width tau are therefore contained in
ambient Euclidean tubes of width at most tau. Affine residual offsets
cannot cancel the ambient normal. The normals are fixed before the
draw even though their factor-coordinate offsets depend on r.

## 5. Ambient probability and Gaussian weighted localization

### 5.1 Uniform ambient coefficients cannot be conditioned into independence

For cube noise, d and r are generally dependent. The correct bound uses
an invertible coordinate matrix S=[T^T,V], with V spanning ker T.
If a subset of t factor coordinates is constrained to residual-dependent
intervals of lengths L_i, integrate those fibers and the projection of
S^(-1)[-sigma,sigma]^n onto the remaining coordinates. Zonotope volume
and the complementary-minor identity give

    probability <= product_i L_i/(2sigma)^t
                       * sum_|K|=t |det((T^T)_(K,Q))|.

Cauchy--Binet and Cauchy--Schwarz bound the determinant sum by
n^(t/2) when ||T|| <= 1. The residual basis and its conditioning cancel
exactly. The local comparison intervals depend only on r, as required.
This establishes the uniform ambient count, with its real n^(k/2)
and auxiliary-width losses. Conditioning on r and asserting independent
uniform factor coefficients would be false.

### 5.2 Gaussian factor/residual independence and the density majorant

For the isotropic continuous proxy gamma ~ N(0,sigma^2 I), d and r
are jointly Gaussian and have zero cross-covariance. They are therefore
independent, and Cov(d)=sigma^2(TT^T)^(-1). With
c_frame I <= TT^T <= I, every t-coordinate marginal satisfies

    p_Q(z) <= c_frame^(-t/2) product_i phi_s(z_i),
    s = sigma/sqrt(c_frame),

because its covariance eigenvalues lie in [sigma^2,sigma^2/c_frame].
The proof works for every c_frame in (0,1], including 1/16 in the
anisotropic separable theorem. It does not require c_frame >= 1/2.

At a deterministic auxiliary node v, the local event E_v restricts
each interior d_i to a residual-dependent interval of length at most
C_k alpha h_i. Every active witness supplies the upper model (A),
and the necessary event also lies in the deterministic location interval

    J_i(v) = alpha[l_i-v_i,u_i-v_i]
                           +[-C_k alpha h_i/2,C_k alpha h_i/2].

It is the **event** that lies in the intersection. The entire comparison
interval need not be contained in J_i(v). A witness for W_r(v) can
be selected using r alone because the additive d^T v does not affect
inner minimization. This justifies Gaussian conditioning even for mixed
ties. The actual finite product law does not retain transformed
Gaussian independence; its events are transferred afterward.

The dominating product density gives

    Pr(E_v) <= c_frame^(-t/2) product_i
          min(1,C_k Delta_i sup_(z in J_i(v)) phi_s(z)),
    Delta_i = alpha h_i.

The outer c_frame^(-t/2) must remain outside the minimum. Moving it
inside without justification changes the bound.

### 5.3 Weighted lattice lemma and removal of auxiliary-box width

For any lattice spacing Delta, core interval [A,B] of width W, and
C>0, direct central-interval and tail summation gives

    sum_lattice_z min(1,C Delta sup_[A-z-C Delta/2,B-z+C Delta/2] phi_s)
                  <= C W phi_s(0)+2C+4.               (F)

The central interval contains at most W/Delta+C+2 nodes. Its contribution
is at most C W phi_s(0)+C+2. On each tail the summand decreases with
distance, and the sum is bounded by its first term plus its integral
divided by Delta, at most 1+C/2. This proves (F), including coarse meshes
and zero-width cores. Omitting the cap by 1 would lose the coarse-mesh
constant.

Apply (F) to the alpha-scaled auxiliary lattice and original projection
core [alpha l_i,alpha u_i]. Grid endpoints each contribute at most one
without a local comparison. Summing over interior-coordinate subsets
gives exactly H_G in Section 1. The density prefactor cancels the wider
Gaussian standard deviation in the core-width coefficient. The enlarged
auxiliary search box never appears in H_G. Proxy draws need not have
their auxiliary minimizers in that box; E_v is merely a necessary local
comparison event defined for every proxy draw.

## 6. Mixed integer gaps: a complete independent derivation

At a query v, solve the convex MIQP defining W_r(v) and retain one
winning integer tuple z_*. Every different tuple satisfies one of the
2p inequalities x_i <= z_*,i-1 or x_i >= z_*,i+1. The minimum over
these exact exclusion solves is the exact best-competing-label value.
Subtract W_r(v) to obtain Delta(v), including zero at ties and infinity
when no competitor exists. It is not a gap between the first two
arbitrarily returned points; distinct integer labels are required.

For a fixed feasible label z, subtract the common alpha||a||^2/2 from
its slice value. The result is an infimum of affine functions with slopes
-alpha Tx. For displacement h, every such slice's increment lies in the
same interval

    [min_X -alpha(Tx)^T h, max_X -alpha(Tx)^T h].

The difference between two increments is bounded by the width of this
interval, alpha diam(TPset)||h||, with no extra factor two. Put a
rational C_T >= max(1,diam(TPset)) and Lambda=alpha k C_T. A fixed-label
region containing the cell and Delta(v) >= Lambda h_j certify that label
throughout the cell. Equality is safe: another label may tie without
changing the value formula or the selected feasible witness.

If this gap test fails at the near-optimal corner (E), the winning and
best-competing witnesses have original values at most

    F_gamma* + 2B_j + Delta(v)
               <= F_gamma* + (k alpha s/4+Lambda) h_j,

using h_j <= s and square completion (B). Even if neither queried
label is globally best, at least one differs from a globally best label.
Thus failure is contained in one original-label isolation event; adaptively
chosen corners create no new union factor.

For any finite label set in product integer bounds [L_i,U_i], and any
optimized continuous costs, condition on all noise except integer
coefficient gamma_i. Group values have the form a_t+t gamma_i. Distinct
integer slopes are separated by at least one. Their lower envelope has
at most U_i-L_i breakpoints. A near-winning distinct group forces a
breakpoint within epsilon of the coefficient: the selected pair crosses
within epsilon, and an intervening line can only produce a nearer
envelope change. Union over the integer coordinates gives

    Pr_grid(two original labels within epsilon of best)
            <= G(epsilon/sigma+1/N),
    G = sum_i (U_i-L_i).

For independent laws of Kolmogorov distance delta from the Gaussian,
the same conditional argument gives

    Pr(two original labels within epsilon of best)
            <= G(epsilon/sigma+2delta).

No ambient n factor is needed in this scalar conditional transfer.
All missing groups, nonproduct feasible label sets, endpoint ties, and
simultaneous breakpoints are covered. G may be exponentially large; it
enters a logarithmic cutoff and precision budget, not H_G.

The exact gap contract requires attained exact oracle values. Numerical
primal values or a solver's uncertified gap do not certify cell dominance.

## 7. Axis-section transfer, finite sampler, and fixed budgets

### 7.1 Uniform section bounds

On a line in one original noise coordinate at a fixed auxiliary query,
each continuous active basis gives a quadratic formula on a closed
interval. At most R possible bases cover the entire line. In continuous
recourse, valid formulas agree wherever their intervals overlap, so at
most 2R finite endpoints suffice to partition the line into quadratic
pieces. In separable mixed recourse, a selected scalar-state product
already certifies global optimality, so the same overlap agreement holds.

General mixed recourse is different: fixed-label regions alone do not
certify the mixed winner. Include all pairwise roots of the available
label quadratics. At most 2R^2 partition points suffice. Identical
polynomials add no root; singleton validity intervals and isolated
boundary values remain covered.

A local event uses at most 2k+1 query values and 2k quadratic weak
comparisons. Each common interval has at most 4k comparison roots.
Safe component counts are

    C_sec = [2(2k+1)R+1](8k+2),       continuous/separable,
    C_sec = [2(2k+1)R^2+1](8k+2),     general mixed.

The bounds hold for every fixed choice of the other coefficients,
including partially discrete laws in a telescoping replacement.
A union of C_sec intervals or points changes probability by at most
2 C_sec delta under scalar Kolmogorov error delta. Replacing independent
ambient marginals one at a time gives 2n C_sec delta per local event.
Using one-sided CDF limits includes open or closed endpoints and atoms.

### 7.2 Finite rational Gaussian-like sampler

The supplied sampler is adequate. At accuracy b, let K=b+20 and
e=2^(-(b+20)), use a power-of-two endpoint grid on [-K,K] with mesh
at most e/K, and approximate exp(-z^2/2) by dyadic weights within e/K.
Accept uniform proposals with their exact dyadic weights, for at most
ceil(16K(b+20)) trials; return zero after the cap.

Acceptance probability is at least 1/(16K), so the cap's failure mass
is at most exp(-(b+20)) <= e. Conditional on acceptance, the distribution
is proportional to the fixed weights. Lipschitz Riemann-sum, weight,
truncation, and cap errors give at most 22e < 2^(-b) in Kolmogorov
distance. Repeated proposals and dyadic acceptance use bounded polynomial
time and bits, even though the support grid is exponentially large.
Argument reduction, Taylor approximation on [0,1/2], and guarded dyadic
squaring compute the weights in polynomial bit work. Scaling by rational
sigma keeps all output coordinates rational and polynomial-height.

The zero atom caused by the cap is real and is included in the transfer
error. It cannot simply be ignored or conditioned away.

### 7.3 Why the budget is noncircular

For a trial support R_s=2^t, form the rational fixed auxiliary box using
row-sum bounds on D gamma. Let s(t) be its largest width. In continuous
QP, the terminal requirement is proportional to

    s(t) 2^(-J) <= sigma/[4k K B(alpha+H_0)].

Thus J(t) <= J(0)+t. In general MIQP the gap failure coefficient is

    C_bad(t) = K k(alpha+H_0)
                    +G[k alpha s(t)/4+Lambda],

and the terminal requirement is

    s(t) 2^(-J) <= sigma/[4B C_bad(t)].

Both s(t) and C_bad(t) are at most 2^t times their initial values, so
J(t) <= J(0)+2t. All log K, log B, log G, log H_0, and J(0) are
polynomial in the **base** input length. No sampled denominator is in
this calculation.

The deterministic node budget is Q_all=(J+1)(2^J+1)^k. Choose b so
2^b dominates both the bad-event accuracy budget and
2n C_sec Q_all, then increase t until 2^t >= b+20. Required b grows
only linearly in kt up to logarithms and polynomial base terms.
Exponential 2^t wins after polynomially bounded t; the resulting J,b,
box coordinates, and sampler outputs all have polynomial bit length.
All random draws occur after the budgets are fixed.

The summed local-event discrepancy is at most one. At the terminal
level, the geometric/label contribution and finite-law contribution
each have probability at most 1/(4B). The same-draw fallback costs
B poly(I+b), so its unconditional expected contribution is polynomial.
The fallback cancels its **combinatorial multiplier**, not its entire
bit-work bound. This distinction avoids a precision circularity.

## 8. Anisotropic separable normalization and scalar certificates

For Gamma=TT^T > 0, a denominator/determinant bound gives a rational
mu <= lambda_min(Gamma) with polynomial-length logarithm. Exact rational
orthogonal Q makes

    Q Gamma Q^T = diag(a_i)+E, ||E|| <= mu/64.

Each a_i is a Rayleigh quotient in [mu,||T||^2]. Choose dyadic d_i
with 2a_i <= d_i^2 < 8a_i, put U=D^(-1)QT and
L=diag(alpha d_i^2). Then

    (1/16)I <= UU^T <= I, L_max < 8beta,
    U^T L U = alpha T^T T                            (G)

exactly. The Jacobi residual is used only to prove the frame bound;
it is neither discarded nor absorbed into a dense convex term. Thus
the supplied unary convex residual stays separable.

Choose dyadic rho_i with 1 <= L_i rho_i^2 < 4. Equal subdivisions
balanced by rho_i give

    B_j=sum_i L_i h_ij^2/8 <= k h_j^2/2,
    L_i h_ij^2 > h_j^2/4   for refined coordinates,
    local interval length <= (1+8k) L_i h_ij.

The weighted Gaussian lemma applies with spacing L_i h_ij, projection
core width L_i range(UX)_i, and frame constant 1/16. Hence

    H_L = product_i [2+4(2C_k+4)
                +C_k L_i range(UX)_i/(sigma sqrt(2pi))],
    C_k=1+8k.

No L_max/L_min or smallest singular value occurs in this count.
For closure, (A) and (E) imply ||g|| <= sqrt(2k L_max)h_j.
Cell diameter is at most h_j sum rho_i. The rational coefficient

    C_tube = k(1+L_max)+H_0 sum rho_i

bounds both contributions because k(1+L_max) >= sqrt(2k L_max).
Tiny curvatures may enlarge rho_i and C_tube, but only their logarithms
enter the cutoff. The support-loop growth is J(t)<=J(0)+t.

The scalar recourse certificates are global, which is why unrestricted
integer count is possible here. For integers, convex forward differences
are monotone, and a label z wins exactly when

    phi(z)-phi(z-1) <= lambda <= phi(z+1)-phi(z),

with missing endpoint neighbors omitted. Binary search takes logarithmic
time in the binary-encoded integer interval cardinality. For continuous
coordinates, positive-curvature pieces give affine responses and knots
give constant responses on derivative intervals. A flat piece at its
slope can use an endpoint knot. At most 2s_i+1 states suffice.

One state per coordinate defines at most 2n linear inequalities certifying
the entire separable mixed value function. There is no additional
best-other-label exclusion oracle here. Product state counts R and
fallback counts B have polynomial logarithms, even with arbitrarily many
integer variables. These counts affect precision, not expected local
counts. Replacing (G) by general intrinsic spectral normalization would
usually destroy separability and is not justified.

## 9. Proximal growth tail and the earlier capped-moment theorem

The sharp proximal theorem is sound and remains a distinct general
result. For continuous f on arbitrary nonempty compact X and independent
coefficient densities bounded by phi_i, let w_i be coordinate widths
and g_* the largest global quadratic-growth modulus at one optimizer,
zero at multiple optimizers. Then

    Pr(g_* < epsilon) <= 2epsilon sum_i phi_i w_i.

For singleton X use g_*=infinity. The good-growth set is closed by
compactness and continuity, so its complement is measurable.

To reconstruct the proof, define

    H(a)=max_X[a^T x-f(x)+epsilon||x||^2],
    lambda=2epsilon, Pprox=prox_(lambda H), Q=I-Pprox.

If H is differentiable at Pprox(z), every maximizer equals
x_*=Q(z)/lambda, and substituting z=Pprox(z)+2epsilon x_* gives
the full growth inequality. Let E be the preimage under Pprox of a
Borel null set covering H's nondifferentiability set. By the Lipschitz
area formula, det(DPprox)=0 almost everywhere on E. Since the eigenvalues
of DPprox lie in [0,1],

    1_E <= tr(I-DPprox)=sum_i partial_i Q_i

almost everywhere. Q_i is monotone and bounded in an interval of length
lambda w_i along every own-coordinate section. Its derivative integrates
to at most lambda w_i. Conditioning on the other coordinates and using
the density bounds proves the tail. The constant two is attained by a
centered uniform tilt of a linear objective on an interval.

The finite-grid transfer also passes. For a fixed coefficient line and
growth threshold, original and epsilon-modified quadratics have at most
F stationary face candidates apiece. Feasibility intervals and degree-two
comparison polynomials yield at most 8(F+1)^2 bad-growth components,
uniformly in the threshold and fixed other coefficients. Tensor-law
replacement gives

    Pr_grid(g_*<epsilon) <= (sum_i w_i/sigma) epsilon+beta,
    beta=2n[8(F+1)^2]/M.

The atomic residual is uniform in epsilon and cannot be omitted.
The same fixed distribution therefore supports the inverse-growth
integration used in expected-smoothed-qp.md.

For k=1 or 2, the growth-conditioned exact algorithm costs
P(L) Z^(k/2)(1+log Z)^d, where Z=max(1,nu/g_*). Interleave bit
operations with the unconditional B P(L) fallback. Capping logarithms
by log B and integrating the bounded inverse-growth moment gives

    E min(B,Z^(1/2)) <= 2+nu sum_i w_i/sigma,
    E min(B,Z) <= 2+(nu sum_i w_i/sigma)log B,

when beta B <= 1. This proves the earlier linear-ratio expected bound
for k<=2. For k>2 the same integration has a generally exponential
B^(1-2/k) term. That is a limitation of this argument, not a lower
bound or an obstruction to the later closure theorem.

The Gaussian-like closure theorem supersedes the restriction to at most
two negative directions for exact expected FPT work. It does not make
the earlier theorem wholly redundant: the earlier theorem uses a
different uniform-grid perturbation law and gives a linear numerical
ratio bound for k<=2, whereas H_G has degree k in its numerical ratio.
The sharp proximal tail itself applies far beyond QP and is not superseded
by algebraic closure. It supplies no optimization oracle for arbitrary f.

The approximation-only semiconcave cell theorem remains useful as the
common counting/algorithmic base. Its finite grid chosen for requested
accuracy does **not** alone support exact optimization at arbitrarily
fine levels under one fixed law. Exact closure and same-draw fallback
are the additional ingredients. Historical recovery arguments should
not be substituted into the finite-law proof in a way that makes the
noise precision depend on the sampled input's recovery precision.

## 10. Remaining dependencies and recommended manuscript organization

The mathematical chain depends on standard rational LP and an exact
polynomial-bit convex-QP primitive that returns an attained rational
optimizer/value, including singular Hessians and lower-dimensional
polytopes. Nonnegative multipliers can be recovered by rational LP.
The general mixed theorem additionally depends on an exact convex-MIQP
primitive with cost f(p) times a polynomial having an absolute exponent,
and attained optimizer/value semantics. The root has been asked to have
the Luna literature lead confirm the latter primary statement.

Bounded integer labels have polynomial height from LP coordinate ranges.
Fixing the oracle's returned label and polishing its continuous convex
slice produces uniformly polynomial-height downstream data. This prevents
a merely f(p)-dependent output-length bound from multiplying subsequent
oracle-instance sizes. Exclusion problems add one inequality and keep
the same p. No integer oracle is claimed polynomial for unbounded p.

Recommended common lemmas, in proof order:

1. Rational quadratic smallest-face candidate and height lemma, including
   exact box-face minimization and fallback.
2. Rational intrinsic normalization with exact kernel projection and
   constant lower frame bound.
3. Square completion, semiconcavity, and the every-active-witness estimate
   (A), stated once in a diagonal auxiliary metric.
4. Equal-subdivision meshes, corrected-corner invariant, and deterministic
   local comparison intervals.
5. Continuous active-basis extraction and mixed separable scalar-state
   extraction, both returning an extension gradient and a closed global
   validity region.
6. Fixed-hyperplane tube obstruction and ambient normal pullback.
7. Gaussian product-density majorant and weighted lattice count.
8. Uniform axis-section/Kolmogorov transfer and bounded rational sampler.
9. Best-competing-label certificate, increment bound, and original-label
   isolation for general mixed recourse.
10. Fixed support/precision budget and unconditional expected fallback
    accounting.

Use Gaussian-like closure as the principal low-rank result. Present
aligned and uniform ambient variants as explicit distribution-dependent
corollaries or intermediate theorems, without development-history prose.
Keep the proximal tail and k<=2 uniform-law moment theorem where their
distinct generality and numerical dependence justify their length.
State the separable supplied-factor boundary alongside its theorem,
and use its anisotropic normalization to remove factor conditioning.

Do not claim fast numerical critical-region extraction, stability of
floating-point certificates, competitive performance, or empirical
expected runtimes. Existing exact small-instance diagnostics support
identities and invariants; they do not implement the production primitives
or establish asymptotic probability theorems experimentally.

The instance-dependent finite law is a material model restriction.
A universal accuracy budget for a fixed input-length class may be possible
from explicit uniform height bounds, but it is not established by replacing
unspecified polynomial bounds with a claim about one universal law. Keep
the actual constructed-law contract unless that strengthening is separately
proved.

## 11. Verification record for this audit

I read the twelve requested mathematical notes, the supporting
negative-inertia-qp.md, and relevant original adversarial reviews, then
re-derived the central bounds analytically. I did not browse, search
literature, edit historical notes, inspect CI, run project-wide checks,
delegate, or rerun computational experiments. The existing experiment
records remain author-run evidence rather than new reviewer-run checks.

Targeted commands actually used were cat, wc -l, and scoped rg --files
to locate and inspect the requested notes/reviews, plus mkdir for the
authorized report/verification destinations. The mathematical checks
above are proof diagnostics, not executable optimization tests.

A targeted `python -` command using pathlib read only this report and
checked its final newline, absence of trailing whitespace, paired code
fences, and presence of the corrected kernel-condition discussion. It
passed on the 914-line initial report. No solver diagnostic was run.
