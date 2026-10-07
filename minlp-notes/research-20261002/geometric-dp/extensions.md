# Arithmetic and private-recourse extensions

Date: 2026-10-02. Status: independent mathematical development and review of
[the main theorem](theorem.md). The structural recourse and rational-arithmetic
arguments also received separate agent derivations. This is not a literature
priority assessment. No project-wide checks or CI inspection were run.

## 1. Review of the upper-curvature hypothesis

The main note correctly weakens a full gradient Lipschitz bound to upper
coordinate curvature. If, with the other coordinates fixed,
\(u\mapsto F(x_{-i},u)-Lu^2/2\) is concave, Jensen's inequality gives the
claimed one-coordinate rounding inequality. Successively and independently
rounding coordinates gives its sum. Smoothness is unnecessary. This remains
valid at domain boundaries and when the reduced objective has downward
derivative jumps.

Independence is substantive under this weaker hypothesis. My earlier suggestion
that arbitrary feasible unbiased joint rounding would suffice needs a stronger
curvature assumption. For example, take \(F(x_1,x_2)=x_1x_2\). Its upper
coordinate curvature is zero. Unbiased rounding of \((0,0)\) to \((1,1)\)
or \((-1,-1)\), each with probability one half, gives expected objective one.
On the constrained diagonal \(x_1=x_2\), the endpoint lower bound with zero
correction is therefore one, while the true optimum is zero.

A valid generalization is available under the full upper Taylor bound

\[
 F(y)\le F(x)+g(x)^T(y-x)+(L/2)\|y-x\|^2.                         \tag{1}
\]

Any feasible joint rounding satisfying \(\mathbb EY=x\) and the same
coordinate variance bounds then works: expectation cancels the linear term
in (1). A differentiable globally semiconcave function satisfies (1), as does
a smooth function with \(\nabla^2F\preceq LI\). Upper coordinate curvature
alone does not control mixed covariances. Constraints still need an actual
feasible rounding construction; no such construction is asserted generally.

## 2. Exact integer optimization without knowing the growth constant

Use the notation and exact tables of the main note. All coordinates in this
section are integer. Try \(\theta_m=2^{-m-1}\), \(m=0,1,\ldots\), restarting
at a fixed feasible center. Let

\[
 J_m=\max\left\{0,
  \left\lceil\log_2(s\sqrt n/\theta_m)\right\rceil\right\}.
\]

In trial \(m\), run stages \(0,\ldots,J_m+1\), stopping whenever the
computed gap is exactly zero. This is a fully specified schedule; no growth
constant or objective separation needs to be supplied.

Let \(m^*\) be the first trial satisfying \(\theta_{m^*}^2\le c/(8L)\).
For this trial, the main theorem applies with
\(B=\max\{1,4L/(11c)\}\), and

\[
 B\le\frac1{4\theta_{m^*}^2}.
\]

Indeed \(1\le1/(4\theta^2)\), and the admissibility inequality implies
\(4L/(11c)\le1/(22\theta^2)\). At stage \(J_{m^*}\), therefore,

\[
 \|z_j-x^*\|^2\le Bnh_j^2\le1/4.
\]

The integral vector \(z_j\) equals \(x^*\). At the next stage it again
equals \(x^*\), and its immediately adjacent integer steps have length one,
since \(h_{j+1}\le\theta/(2\sqrt n)<2\). The correction is zero and the
certificate is exact.

The quantities \(J_m\) are nondecreasing. Thus the total table work over all
trials through \(m^*\) is at most

\[
 C^p(N+M)\theta_{m^*}^{-p}(J_{m^*}+2)^{p+1}
   /(1-2^{-p}),                                                  \tag{2}
\]

where \(M\) is the number of factors and \(p=w+1\). The same geometric
sum argument applies to any common nondecreasing bound on arithmetic cost
per table operation. This establishes the previously unspecified exact
unknown-constant variant of Section 7 of the main note.

## 3. Certified finite-precision tables

An exact arbitrary-real evaluation oracle is unnecessary for approximate
certification. In this section take a supplied rational upper curvature
bound \(L>0\), rational interval endpoints and initial centers, and rational
\(h_j,\theta\), so that grids and correction tables are rational. A
rational upper curvature bound can replace a known real one. Suppose that
at stage \(j\) each factor table has rational
approximations such that their sum \(\widetilde F\) obeys

\[
 |\widetilde F(y)-F(y)|\le\Delta_j
       \le Ln h_j^2/16                                           \tag{3}
\]

at every grid point. These error bounds must be certified uniformly over
the finite tables. Assigning absolute error at most
\(Ln h_j^2/(16M)\) to each of \(M\) factor evaluations suffices.

Minimize \(\widetilde F-D\) with exact rational table arithmetic, obtaining
\(y\). Return

\[
 \operatorname{LB}=\widetilde F(y)-D(y)-\Delta_j,
 \qquad
 \operatorname{UB}=\widetilde F(y)+\Delta_j.                       \tag{4}
\]

These are valid bounds: the corrected lower table lies below \(F-D\),
whose grid minimum is at most \(f^*\), and the upper bound dominates the
objective of feasible \(y\). Their gap is \(D(y)+2\Delta_j\).

Assume \(\theta^2\le\min\{1/4,c/(8L)\}\). The main contraction proof now
starts from \(cE_{\rm new}\le D(y)+2\Delta_j\), giving

\[
 E_{\rm new}\le\frac{2L}{5c}nh_j^2+E_{\rm old}/15.                \tag{5}
\]

With \(B_{\rm fp}=\max\{1,6L/(11c)\}\), induction yields

\[
 \|y_j-x^*\|^2\le B_{\rm fp}nh_j^2,
 \qquad
 \operatorname{UB}_j-\operatorname{LB}_j\le Ln h_j^2.             \tag{6}
\]

For the first inequality, the induction closes because
\(2L/(5c)+4B_{\rm fp}/15\le B_{\rm fp}\); stage zero follows as in
the main theorem. For the second,
\(\theta^2B_{\rm fp}\le1/4\), so \(D\le7Ln h_j^2/8\), and (3)
pays the remaining \(Ln h_j^2/8\).

Accordingly it suffices to use

\[
 J=\max\{0,\lceil\log_2(s\sqrt{Ln/\varepsilon})\rceil\}
\]

in every unknown-constant trial. The same table-count bound and geometric
overhead hold. Factor-evaluation precision is
\(O(1+\log_+(M/(Ln h_j^2)))\) bits after the radix point, plus the bits
needed for the magnitude of the result. Thus a certified evaluation routine
whose cost is polynomial in requested precision and grid input bit length
preserves a polylogarithmic accuracy dependence at fixed width and
conditioning.

This is not a claim about an ordinary floating-point DP. Exact comparisons
of rational approximate table entries avoid a separate accumulation of DP
roundoff. Floating-point message arithmetic would need its own directed
rounding or error budget.

With positive evaluation uncertainty, (4) does not generally produce an
exact zero gap, even after it identifies the correct integer vector. Exact
rational evaluation, a known objective-value lattice, or another exact
comparison certificate is needed for exact integer termination.

### A value lattice can replace exact evaluation

Suppose all feasible integer objective values belong to \(Q^{-1}\mathbb Z\)
for a known positive integer \(Q\). Certify the objective \(U\) of a
feasible point exactly by isolating it in a rational interval containing a
single value of this lattice. If a valid global lower bound satisfies
\(\operatorname{LB}>U-1/Q\), then \(U=f^*\): no smaller attainable
objective value lies in that interval. Rational polynomials on integer
boxes have such a lattice, with \(Q\) the least common multiple of their
coefficient denominators. Its bit length is at most the sum of those
denominator bit lengths. This observation permits certified finite-accuracy
evaluations to give an exact value certificate at precision determined by
\(Q\), even when a literal zero gap is unavailable.

## 4. Private recourse with fixed feasible sets

Let the exposed mixed variables \(x\) have the product domain and supplied
decomposition of the main theorem. For each factor introduce private variables
\(u_t\), used in no other factor, and put

\[
 f_t(x_{V_t})=\min_{u_t\in Y_t} g_t(x_{V_t},u_t).                  \tag{7}
\]

Assume \(Y_t\) is nonempty, compact, and independent of \(x\), and that
\(g_t\) is jointly continuous. Assume, uniformly over \(u_t\in Y_t\),
upper coordinate curvature \(L_{ti}\ge0\) in each exposed coordinate:

\[
 v\longmapsto g_t(x_{V_t\setminus\{i\}},v,u_t)-L_{ti}v^2/2
 \quad\hbox{is concave}.
\]

Then (7) has the same upper coordinate curvature. Subtract the common
quadratic before taking the infimum: an infimum of concave functions is
concave. The projected objective \(F=\sum_t f_t\) therefore has upper
coordinate curvature

\[
 L=\max_i\sum_{t:i\in V_t}L_{ti}.
\]

The global minimum of the original private-variable model equals
\(\min_x F(x)\). If this projected objective has the main theorem's global
quadratic growth, all its grid and contraction results apply to the exposed
variables. No uniqueness or growth assumption on private minimizers is
needed. The private sets may themselves have internal constraints, discrete
variables, or disconnected components. Their dimension does not increase
the exposed treewidth; their solution cost remains part of the algorithm.

For finite-accuracy computation, a private oracle at exposed grid point \(v\)
must return rational numbers \(\ell_t,u_t^{\rm val}\) and an actually
feasible private witness \(\widehat u_t\) satisfying

\[
 \ell_t\le f_t(v)\le g_t(v,\widehat u_t)\le u_t^{\rm val},
 \qquad u_t^{\rm val}-\ell_t\le\delta_t.                         \tag{8}
\]

Midpoints of these intervals fit Section 3 with
\(\Delta_j=\tfrac12\sum_t\delta_t\). At the selected exposed vector,
the private witnesses combine into a feasible original-model point because
the variables and feasible sets are private. Its objective is at most the
returned aggregate upper bound. A numerical upper value without a feasible
private reconstruction is insufficient.

The complexity is the outer table work plus

\[
 \sum_{j,t}\left(\prod_{i\in V_t}|G_{i,j}|\right)
       C_t(\delta_{t,j},\text{grid input size}),                  \tag{9}
\]

where \(C_t\) includes global certification and feasible reconstruction in
(8). A polylogarithmic accuracy claim for total runtime requires these
costs to be polynomial in requested precision, grid input bit length, and
the relevant local input sizes. Arbitrary nonconvex private minimizations
need not have this property. Compactness and continuity alone do not give
a computable oracle or finitely representable feasible witnesses.

Exact recourse minima with exact feasible reconstructions preserve the pure
integer exposed-variable theorem. Finite-accuracy recourse alone gives
approximate original-model certification; identifying an integer exposed
optimizer does not determine an exact continuous private optimizer.

### Why parameter-dependent feasible sets need another argument

Consider \(x\in[-1,1]\) and

\[
 f(x)=\min\{u:0\le u\le1,\ u\ge x,\ u\ge-x\}=|x|.
\]

For fixed \(u\), the objective is affine in \(x\); nevertheless \(|x|\)
has no finite upper semiconcavity constant. It even has projected quadratic
growth \(|x|\ge x^2\). On grid \(\{-1,1\}\), wrongly inheriting \(L=1\)
from the fixed-private objective gives penalty \(1/2\) and purported lower
bound \(1/2>f^*=0\). Thus even linear private constraints can invalidate
this extension when their feasible set depends on exposed variables. Such
models require a separately proved upper-curvature bound for their value
function.

## 5. A rational-polynomial bit-complexity theorem

Suppose the factors are sparse polynomials with rational coefficients. Let
\(T\) be the total number of monomials, \(d\) their maximum total degree,
and \(D=\max\{2,d\}\). Let \(b\ge1\) bound numerator and denominator bit
lengths of all coefficients, interval endpoints, the initial center, and the
supplied rational curvature bound \(L\). Include input reading separately.
Choose \(\theta=2^{-r}\), \(r\ge1\), and let \(J\) be the final stage.

For a universal constant \(C\), put

\[
 E=J+Cr2^r(J+1),\qquad
 H=O\bigl((T+nD+1)b+DE+\log(T+n+1)\bigr).
\]

All grid coordinates have \(O(b+E)\) bits. Every reduced rational factor
value, correction, DP message, and arithmetic intermediate has \(O(H)\)
bits. A sufficient bit-operation bound is

\[
 O(AH^3),\qquad
 A=C^p\left[Np+T\bigl(1+p\log(d+1)\bigr)\right]
         2^{rp}(J+1)^{p+1}.                                    \tag{10}
\]

The cubic factor is a conservative elementary rational-arithmetic bound.
The factor \(Np\) covers message additions, indexing, comparisons, and
backtracking; child-message additions sum over tree edges. Evaluating a
monomial uses \(O(1+p\log(d+1))\) rational operations by repeated
squaring, and unary corrections add no higher order to this bound.

Here is the denominator argument, which also rules out an unnoticed
denominator explosion caused by recentering. Define

\[
 Q_i=\operatorname{lcm}\bigl(\operatorname{den}(a_i),
   \operatorname{den}(b_i),\operatorname{den}(z_{-1,i}),
   \operatorname{den}(s)\bigr).
\]

Each \(Q_i\) has \(O(b)\) bits. An untruncated distance after \(k\)
continuous steps at stage \(j\) equals

\[
 s2^{-j}\sum_{\ell=0}^{k-1}(1+2^{-r})^\ell.
\]

Its denominator divides \(\operatorname{den}(s)2^{j+r(k-1)}\), and
\(k\le C2^r(j+1)\). Taking a new center from the current grid only adds
rationals with denominators dividing the same \(Q_i\) times a power of two.
Clipping selects an original endpoint. Induction therefore shows that all
coordinate denominators through stage \(J\) divide \(Q_i2^E\). Their
magnitudes stay within the original box, giving the coordinate bit bound.

A common denominator for all factor values, unary corrections, and DP
messages is

\[
 Q=8\operatorname{den}(L)
       \left(\prod_{\text{coefficients }a}\operatorname{den}(a)\right)
       \left(\prod_i Q_i^D\right)2^{DE}.                         \tag{11}
\]

Every DP message is a sum of a subset of assigned factor values and unary
corrections at some grid assignment: taking a minimum selects one such
sum. Its denominator therefore divides (11), independently of tree depth
and branching. Absolute values are bounded by

\[
 T2^{(d+1)b}+n2^{3b+O(1)}.
\]

This proves the stated \(H\) bound. Rational fractions must be reduced
after arithmetic, or values can use a common integer scale; keeping
unreduced products of unrelated denominators would not satisfy this bound.

Choose a dyadic \(\theta\) within a fixed factor of the admissible threshold,
or use the unknown-constant trials. At fixed width and bounded conditioning
\(L/c\), (10) is then polynomial in the encoded input size and
\(\log(1/\varepsilon)\), provided the numerical degree \(d\) is
polynomially bounded in the input size. Unknown-constant
trials are covered too: their stage counts, denominator bounds, and arithmetic
costs are nondecreasing, so the geometric domination in Section 2 applies.
This is not a polynomial bound uniformly over arbitrarily large \(L/c\).

### Binary exponents are a real output-size obstruction

For \(k\ge3\), consider

\[
 F(x)=x^2+x^{2^k},\qquad 0\le x\le1/2.
\]

It has quadratic growth \(c=1\) at zero and upper curvature \(L=3\):
for \(d=2^k\ge8\), \(F''(x)\le2+d(d-1)2^{-(d-2)}<3\).
Nevertheless the exact rational value at mandatory endpoint \(1/2\) has
denominator \(2^{2^k}\). It takes \(\Omega(2^k)\) bits, despite fixed
width and conditioning and a binary exponent of length \(k+1\). Thus
exact rational tables cannot give a polynomial runtime in binary-exponent
input length alone. Approximate polynomial evaluation may avoid that output
obstruction, but needs a separate evaluation-complexity statement.

### Sharper arithmetic bound for pure integer boxes

All grid coordinates and retained interval lengths are integers. Their
objective and message denominators divide
\(8\operatorname{den}(L)\prod_a\operatorname{den}(a)\), with no
grid-denominator factor. In (10), one can replace \(H\) by

\[
 H_{\mathbb Z}=O\bigl((T+d+1)b+J+r+\log(T+n+1)\bigr).
\]

The \(J+r\) term accounts for forming rational trial steps before taking
their integer floors. Combining this bound with Section 2 gives an exact
Turing-model algorithm for rational polynomial integer boxes under the
stated conditioning assumption, including when the growth constant is
unknown.

## 6. Fully enumerated finite-state variables need no growth or curvature

Separate the variables into gridded coordinates \(x\), which are continuous
or large-domain integers, and finite-state variables \(z\), whose complete
domains are explicitly retained by the DP. Finite states may be binary,
categorical, or integer; their labels need no numerical metric. Let \(n_x\)
be the number of gridded coordinates.

The common product domain of \(x\) is independent of \(z\). Coupled
feasibility restrictions involving \(x\) are not introduced by this
extension; they would need a separate feasible-rounding argument.

Assume upper coordinate curvature \(L\) only in \(x\), uniformly for every
fixed feasible finite-state assignment \(z\). Replace full mixed-space
quadratic growth by

\[
 F(x,z)-f^*\ge c\|x-x^*\|^2                                   \tag{12}
\]

for every feasible pair. This requires one optimal exposed vector \(x^*\),
but the optimal finite-state assignment need not be unique. Close objective
values for different finite states at the same exposed vector do not lower
the admissible \(c\). This is a weaker and more useful hypothesis than
quadratic growth in a metric on all mixed variables.

Use grids and corrections only for \(x\), and keep every allowed state of
\(z\). To prove the lower bound, independently round \(x\) while leaving
\(z\) fixed. The expectation proof is unchanged, and (12) bounds only the
gridded component of the corrected DP minimizer. Recenter on that component.
Every contraction, precision, and unknown-constant proof above goes through
with \(n_x\) in place of \(n\) and squared distances only in \(x\).

Equivalently, \(\min_z F(x,z)\) is a finite lower envelope and inherits
coordinate semiconcavity, while (12) gives its quadratic growth. The DP
retains \(z\) explicitly so that this mathematical interpretation does not
destroy the supplied sparse factorization by eliminating all discrete
variables into one function.

If all gridded coordinates are integer, the exact stopping argument remains
valid. Once their squared error is less than one, they equal \(x^*\). At
the next stage they again equal \(x^*\), their correction is zero, and the
DP identity forces the selected finite-state assignment to attain \(f^*\).
There is no need to identify one particular optimal \(z\). If \(n_x=0\),
one exact finite-state DP solves the model without any curvature or growth
assumption; the grid schedule is omitted.

For bag \(t\), let \(p_t\) count its gridded coordinates and let
\(d_t\) be the product of domain sizes of its finite-state variables.
Ignoring separately counted factor evaluation costs, table work in one trial
through stage \(J\) is bounded by

\[
 \sum_t C^{p_t}(1+|\operatorname{ch}(t)|)d_t
           \theta^{-p_t}(J+1)^{p_t+1}.                           \tag{13}
\]

This records the actual distinction: finite-state domain sizes multiply
table counts, while only gridded coordinates contribute powers of the
refinement logarithm. Across unknown-constant trials, geometric domination
applies to terms with \(p_t\ge1\). Terms with \(p_t=0\) may repeat for
every trial and require an additional factor \(m^*+1\) in this refined
bound. Alternatively, the coarser uniform bound using
\(\max_t p_t\ge1\) has the geometric overhead of the main theorem.
Discrete local feasibility relations can be represented
by forbidden finite-state table entries; rounding leaves those states fixed.
Their scopes must be included in the supplied tree decomposition.

The private-recourse extension also combines with this distinction. A private
feasible set may depend on fully enumerated local finite states, provided
it is independent of the gridded coordinates conditional on those states.
Uniform coordinate semiconcavity and the certified feasible-witness oracle
are then required for each allowed finite-state combination. This does not
permit dependence on a large-domain integer coordinate that is itself being
rounded on a compressed grid.

## 7. Verification status

The semiconcavity, finite-precision, and unknown-constant arguments above
were checked algebraically against the main proof. The bit bounds and
private-recourse statements each had an additional separate derivation.
These are mathematical checks, not external peer review. No new executable
checker was run for this extension note; the independent derivation records
the earlier targeted grid and integer-DP computations.
