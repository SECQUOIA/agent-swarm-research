# Certified filtered grids for coupled TU constraints

Date: 2026-10-02. Status: proved deterministic extension; targeted exact
checks and an independent review are recorded below. No publication-priority
claim. The new result is the complete optimization and exact quadratic-output
argument, not TU rounding itself.

## 1. What this completes

The earlier [TU rounding lemma](../../research-20261002/new-direction/tu-feasible-rounding.md)
already proves feasible mean-preserving rounding on aligned cells, including
fixed integer labels. The [TU chamber count](../../research-20261002/new-direction/tu-polyhedral-cell-count.md)
supplies a separate probabilistic count but leaves a complete constrained
algorithm open. Here deterministic quadratic growth replaces that counting
step. Uniform grids, exact min-marginals, and domain filtering give a full
algorithm for overlapping balance and resource constraints. Quadratic
objectives additionally admit exact rational output.

This is a fixed-width polynomial guarantee, with an exponent depending on
width. It does not reproduce the width-FPT bound of the box-only
[geometric-grid theorem](../../research-20261002/new-direction/pruned-coordinate-grid.md).
It uses curvature along feasible equality directions, or the stronger full
continuous-Hessian bound, rather than diagonal curvature. Both differences
from the box theorem are essential to the present proof.

## 2. Model and theorem

Let

\[
 X=\{(x,z): l\le x\le u,\ z_i\in Z_i,
                 Ax+Bz\le b\},                              \tag{1}
\]

where `l,u,b,B` are integral, `A` is totally unimodular, and each `Z_i`
is an explicitly listed nonempty finite set of integers. Equalities may be
represented by both signs. Only the continuous-column matrix `A` must be
TU; integer columns `B` may have arbitrary integer entries. Binary labels
are the main application. Eliminate fixed continuous coordinates first.
Let `n_c` be their remaining number, `d=max_i |Z_i|` (use `d=1` if none),
and `W=max_i(u_i-l_i)` (use `W=0` if none).

The rational objective `F` is a sum of supplied factors. Every factor and
every constraint row has its scope in a supplied tree-decomposition bag.
Write `p` for maximum bag size, `N` for the number of bags, and `I` for
the complete input length, including the finite labels and decomposition.
Assume exact factor evaluation at rational points has polynomial bit cost
and output length. Fixed-degree explicit rational polynomials satisfy this.
Supply a rational `L>0` such that, for every allowed `z`,

\[
 \nabla^2_{xx}F(x,z)\preceq L I
 \quad\text{throughout }[l,u].                              \tag{2}
\]

For quadratics, the maximum absolute row sum of the continuous Hessian,
or any larger positive rational, is an elementary verifiable choice.
For polynomials a rational polynomial/interval certificate for (2) is part
of the input contract; the algorithm does not silently solve that
certification problem. A supplied sum of absolute monomial Hessian bounds
is sufficient.

There is a useful weaker alternative to (2). If the original model includes
equalities `Cx+Ez=a`, it suffices to require
`d^T Hess_xx F(x,z) d <= L ||d||^2` for every `d in ker C`, throughout the
box and at every allowed label assignment. All rounded points preserve
these equalities and the same labels, so only these directions occur in
the proof. A common rational basis `Z` of `ker C` reduces verification to
`Z^T(LI-Hess_xx F)Z` positive semidefinite. This is a one-time curvature
check, not a substitution into objective factors; bag scopes do not change.

Suppose `X` is nonempty, its global optimizer `a=(x*,z*)` is unique, and

\[
 F(v)-f^*\ge g\|v-a\|_2^2\quad(v\in X),\qquad
 \kappa=\max\{1,L/g\}.                                    \tag{3}
\]

**Theorem 1.** There is a deterministic algorithm returning an exactly
feasible rational point and a rational interval containing the global
optimum with width at most `2^-q`. It requires no value or bound for `g`.
Put

\[
 K=\max\{d,\ 5+\lceil2\sqrt{n_c\kappa}\rceil\},\qquad
 K_0=\max\{d,W+1\}.
\]

Its table work is

\[
 O\bigl(p(N+\#\mathrm{factors}+\#\mathrm{rows})
       [K_0^p+(J+1)K^p]\bigr),\quad
 J=O(I+q+1),                                               \tag{4}
\]

with a polynomial rational-arithmetic overhead of absolute exponent in
`I+J`. Factor evaluation costs are included in that overhead. For unit
continuous intervals and bounded finite label sets this is polynomial at
fixed `p` when `L/g` is polynomially bounded. The factor
`(n_c kappa)^(p/2)` prevents a claim of FPT in `(p,kappa)`.
For general integral capacities the initial `K_0^p` cost is
pseudopolynomial in their magnitudes. It is not polynomial merely in their
binary encoding lengths.

The same algorithm detects emptiness at the initial level and returns
certified approximations without uniqueness or growth; (3) is used only
to prove (4). Without it the retained tables can grow with accuracy.
When `n_c=0`, ordinary finite-label DP gives an exact answer immediately.

**Theorem 2.** For a rational quadratic `F`, the algorithm has an exact
variant returning the unique rational optimizer, its exact value, and
checkable global evidence. Replace `J` in (4) by
`poly(I)+O(log kappa)`. No growth constant is needed by the algorithm or
certificate checker. The dependence on capacities and width remains as in
Theorem 1. Every unique optimizer of a quadratic on (1) has some positive
growth constant; no useful bound on its magnitude is asserted.

## 3. Feasible rounding survives filtering

At level `j`, use `h=2^-j`. A retained continuous box has endpoints on
the previous grid; they therefore also lie on the current grid. Retained
integer-label sets may be arbitrary subsets of the original lists.
Fix any feasible point `(x,z)` in this restricted domain, hold `z` fixed,
and intersect its surrounding grid cell with its continuous fiber.

Writing `x=h(k+t)`, the fiber inequalities become

\[
 A t\le 2^j(b-Bz)-Ak,\qquad 0\le t\le1.                    \tag{5}
\]

All right sides are integral. Appending bounds preserves TU, so every
vertex is a zero-one vector. Express `t` as a convex combination of these
vertices. In original coordinates this gives a feasible random corner
`Y`, with `E Y=x`, unchanged `z`, and

\[
 E\|Y-x\|^2\le n_c h^2/4,\qquad
 E F(Y,z)\le F(x,z)+E_j,\quad E_j=n_cLh^2/8.                \tag{6}
\]

The last inequality follows from (2), or its equality-tangent alternative,
Taylor's upper bound on the segment,
and cancellation of the first-order term. Fixed grid coordinates have
zero variance. The distribution remains inside the current restricted
box. It need not be computed; its existence justifies the DP bounds.

Equation (5) explains why arbitrary integer columns are allowed: fixing
their labels leaves an integral right side. Arbitrary rational columns or
right sides would not have this property.

## 4. The complete algorithm and certificate

Initially retain all domains. At each level do the following.

1. Form each continuous uniform grid in its retained interval and use the
   retained discrete labels. Assign each factor and constraint row to one
   containing bag. A bag row violating an assigned constraint is infeasible.
2. Use exact min-sum DP in two tree passes to obtain the least feasible
   grid objective `v_j`, an attaining feasible point, and every coordinate
   min-marginal
   `M_i(t)=min{F(y):y feasible on the current grid, y_i=t}`.
   Missing completions have value `+infinity`, represented as infeasibility
   flags, not rational coefficients.
3. Keep a nonincreasing feasible incumbent value `U`, initialized by the
   first attaining point. The lower bound is `b_j=v_j-E_j`.
4. Retain a continuous adjacent interval `[s,t]` exactly when
   `min(M_i(s),M_i(t))-E_j<=U`. Replace that domain by the hull of all
   retained intervals. A singleton is tested using its only min-marginal.
   Retain a discrete label `t` exactly when `M_i(t)-E_j<=U`.
5. Stop when `U-b_j<=2^-q`; otherwise halve `h` and repeat.

The incumbent's coordinates always survive, since its objective is `U`
and, if it predates the current level, its old grid coordinates remain
current grid coordinates. Thus the stored point remains feasible in every
subsequent restricted domain. In particular `v_j<=U` after the incumbent
update, and (6) gives

\[
 b_j\le f^*\le U\le v_j\le f^*+E_j.                       \tag{7}
\]

Here after the update `U=min(U_old,v_j)` and the old incumbent is available
on the current grid, so in fact `U=v_j`; keeping the incumbent explicitly
makes the certificate convention clear.

For any feasible point whose continuous coordinate belongs to `[s,t]`,
the feasible distribution in (6) uses only its two endpoints in that
coordinate. Hence

\[
 \min\{M_i(s),M_i(t)\}-E_j\le F(x,z).                     \tag{8}
\]

For a fixed discrete label the same statement uses its sole min-marginal.
Every optimizer survives. If no initial feasible grid assignment exists,
(6) proves `X` empty; at later stages the incumbent precludes emptiness.

Save every grid, DP message, min-marginal, retained-domain decision, and
incumbent. The checker verifies bag feasibility and finite DP recurrences,
then (8) justifies each removal. Removed points have objective greater
than that stage's `U`, and therefore greater than the final `U`. The final
bound plus this history proves a bound on the original domain. Checking
TU can use a supplied structural certificate (such as a network-incidence
matrix) or a standard TU-recognition algorithm. A list of claimed TU entries
alone is not a certificate. No growth estimate is used in verification.

Two-pass calibrated tree DP computes all min-marginals in
`O(p(N+#factors+#rows)K_j^p)` table operations. Incoming child messages
are summed and excluded, never multiplied over children. This works on a
branching tree and does not assume bounded variable occurrence. Arithmetic
with infeasibility flags must exclude them from finite minima and must not
subtract infinities when forming outgoing messages; finite-sum plus
infeasible-count bookkeeping suffices.

## 5. Accuracy-independent state counts

For an endpoint satisfying `M_i(t)-E_j<=U`, or a retained discrete label,
a feasible full grid witness
`w` has `F(w)<=U+E_j<=f*+2E_j`. By (3),

\[
 \|w-a\|\le r_j:=\sqrt{n_c L/(4g)}h.                       \tag{9}
\]

Every retained continuous interval therefore lies in
`[a_i-r_j-h,a_i+r_j+h]`. Its hull has length at most `2r_j+2h`.
At the next level the grid has at most

\[
 (2r_j+2h)/(h/2)+1
       =5+2\sqrt{n_cL/g}                                  \tag{10}
\]

nodes per continuous coordinate. Discrete coordinates never have more
than `d` states. The initial level has at most `W+1` continuous states.
Taking `J` as the least nonnegative integer with `n_c L 4^-J/8<=2^-q`
gives (4). Compute it by rational comparisons with powers of four.
Node denominators are powers of two of at most `J` bits; coefficients,
finite labels, objective evaluations, and DP messages have polynomial
encoding length. This proves the asserted bit overhead.

The proof also explains the limit: it controls each coordinate by the
global rounding allowance `n_c L h^2/8`. It does not remove the global
dimension factor. The [global-error obstruction](../../research-20261002/new-direction/global-error-cell-barrier.md)
warns against replacing it by a bag-local error without a new argument.

## 6. Exact quadratic output

Write the full quadratic as
`F(v)=(v^T H v+c^T v+e)/D`, with integral symmetric `H`, integral `c,e`,
and positive integer `D`. Choose `C=max(1,max|H_ij|)` and, for `n_c>0`,

\[
 R=(4n_c C)^{2n_c},\qquad V=D R^2.                         \tag{11}
\]

These numbers have polynomial binary length. There exists an optimizer
whose coordinates share a denominator at most `R`, and the optimum value
has reduced denominator at most `V`. Every isolated optimizer satisfies
the coordinate statement.

To prove it, fix an optimal integer assignment and choose an optimizer on
a continuous face of smallest possible dimension. Independent active
constraint/bound rows form an integral matrix `C_T` with entries in
`{0,-1,1}`. On the face tangent space the quadratic Hessian is positive
definite: otherwise a nonzero null direction gives a constant-objective
line until a new bound/constraint becomes active, contradicting the face
choice. The saddle matrix

\[
 \begin{pmatrix}2H_{xx}&C_T^T\\ C_T&0\end{pmatrix}          \tag{12}
\]

is consequently nonsingular. Its dimension is at most `2n_c`, its entries
have magnitude at most `2C`, and its right side is integral after fixing
the integer labels. Cramer's rule and the determinant expansion bound its
absolute determinant by `R`. The objective denominator then divides
`D r^2` for some common coordinate denominator `r<=R`. At an isolated
optimizer the same null-direction argument applies directly to its face.
This is the usual rational-QP height argument, extended here from box
faces to the constrained faces in (1).

Continue the grid algorithm until `E_j<1/(4V^2)`, every continuous retained
hull has width less than `1/(4R^2)`, and each retained integer-label set
is a singleton. Reconstruct the unique rational with denominator at most
`V` in `[b_j,U]` and the unique rational of denominator at most `R` in
each continuous hull using continued fractions. Check the reconstructed
point against every original constraint and label list and check that its
exact objective equals the reconstructed value. Accept only after those
checks. Distinct reduced rationals of denominator at most `R` differ by
at least `1/R^2`, so uniqueness and existence follow from the height bound
and optimizer containment. This certifies the exact optimum without (3).

Under (3), (9) eventually eliminates every other integer label because
distinct labels differ by at least one. Equation (10)'s preceding hull
bound gives the reconstruction thresholds after
`poly(I)+O(log kappa)` levels. Thus exact termination has the stated cost.

Finally, the qualitative growth fact uses the closed polyhedral tangent
cone. If the ratio `(F(v)-f*)/||v-a||^2` tends to zero, uniqueness and
compactness force `v->a`, and finite integer labels eventually agree.
A convergent subsequence of normalized directions has a feasible short
ray in the continuous tangent cone. First-order optimality and the exact
quadratic expansion make its linear and quadratic terms zero, producing
a ray of optimizers and contradicting uniqueness. This gives existence
of `g`, but no favorable numerical conditioning guarantee.

## 7. Concrete scope and limitations

**Network balances.** Node-arc incidence equalities for continuous flows
have TU matrix `A`. Integral supplies may depend on finite integer switch
labels through integral `B`. Continuous flows with unit integral capacity
and binary decisions give `K_0=2`. Conservation rows must fit the supplied
bags, so high-degree nodes or broad nonlinear factors can increase `p`.
Large integral capacities incur the explicitly recorded initial grid cost.
This allows overlapping conservation equations and nonseparable nonconvex
quadratic factors. It does not require an affine repair or elimination
of the flow variables, which could enlarge objective scopes.

The initial mesh can be any supplied positive rational `delta` for which
`l/delta`, `u/delta`, and `(b-Bz)/delta` are integral at every listed integer
assignment. One can verify the last condition without enumerating products:
choose one reference label vector `z0`, check `(b-Bz0)/delta`, and check
each column increment `B_i(t-z0_i)/delta` for every listed `t in Z_i`.
Use `h_j=delta 2^-j`. The proof is unchanged with
`E_j=n_c L delta^2 4^-j/8` and initial continuous count `W/delta+1`;
the post-filter count (10) is unchanged. Include the supplied mesh's
encoding in `I`; the level bound gains `O(log_+ delta)`, already at most
linear in that encoding. All operations remain in the
original coordinates. Thus large capacities expressed in common integral
units need not incur a large initial table. Finding an advantageous mesh
beyond such directly checked divisibility is not assumed.

**Interval resource constraints.** If every row selects a contiguous block
of coordinates with unit coefficients, the resulting interval matrix is
TU (transpose it to use the consecutive-ones column criterion). Integral
resource bounds and integral finite-label contributions therefore fit (1).
Overlapping resource rows are allowed. Their full scopes still enter `p`;
a single broad budget is not a small-width constraint merely because its
matrix is TU. Laminar incidence systems are another standard TU example.

**Ignoring curvature normal to exact balances.** The equality-tangent
alternative is useful when an objective contains a large term
`rho ||Cx+Ez-a||^2` for the same exact balances. This term vanishes at every
feasible grid point, and its Hessian vanishes on `ker C`; it therefore
changes neither the rounding allowance nor any per-level filtering decision
when the same valid tangent bound `L` is used. The coefficient-based
quadratic height bounds in Section 6 can increase with `rho`, so that
particular exact reconstruction stopping rule can still take more levels.
Its ambient
Hessian norm can be arbitrarily large. For a quadratic, remove dependent
rows of `C` and compute the rational orthogonal projector
`P=I-C^T(CC^T)^(-1)C`. A rational maximum absolute row-sum bound on
`P Hess_xx F P` is a valid `L`; take any positive bound if that norm is zero.
The dense projector is used only in preprocessing. All DP factors and
constraints retain their original scopes. This does not add penalties to
the optimization problem or promise the analogous reduction for merely
active inequalities whose equality status is unknown.

**Arbitrary rational data.** A common denominator `D_0` can align rational
right sides and rational integer-column coefficients with mesh
`h_j=1/(D_0 2^j)` while leaving `A` TU. Rational bounds must also align.
The initial grid then costs up to `(D_0 W+1)^p` states. In the quadratic
height calculation use `R'=D_0 R` and `V'=D(R')^2`: the integral saddle
matrix is unchanged, but its right side can have denominator `D_0`.
This is a valid pseudopolynomial variant, not a polynomial-in-input extension. Clearing
denominators by multiplying the rows of `A` is not an equivalent TU proof.

**Why the assumptions are visible.** Correlated rounding for `x_1=x_2`
and `F=2x_1x_2` has positive quadratic error despite zero Hessian diagonal.
Unequal grids such as `{0,1/2,1}` and `{0,1/3,1}` can have a cell crossed
by `x_1=x_2` with no feasible corners. A rational equality `x=1/3` has no
dyadic feasible node at any level. Thus neither diagonal curvature,
independent geometric grids, nor an unaligned right side can be substituted
in this proof. The existing affine-constraint hardness construction uses
unaligned rational running-sum coefficients and is not contradicted.

General nonlinear constraints, arbitrary non-TU continuous matrices,
compressed very large integer label sets, width-FPT complexity, and the
one-draw exact smoothed TU theorem remain outside this result. The TU
chamber-count theorem may support a different smoothed extension; it is
not needed or claimed here.

## 8. Literature and verification

TU cell integrality and feasible corner distributions are established
polyhedral facts. Chervet, Grappe, and Robert,
[*Principally Box-integer Polyhedra and Equimodular Matrices*, Theorem 4.4](https://arxiv.org/abs/1804.08977),
states the Hoffman--Kruskal characterization in terms of fully box-integer
polyhedra. Our earlier TU rounding note already derives the exact lemma
used above. Finite-state tree DP, min-marginals, and rational reconstruction
are likewise established tools. The contribution of this note is their
deterministic growth-based composition, including constraint feasibility,
capacity dependence, and complete exact quadratic output.

Bienstock and Muñoz,
[*LP formulations for polynomial optimization problems*, Theorem 4](https://arxiv.org/abs/1501.00288),
give bounded-treewidth formulations for much broader constrained polynomial
problems with scaled feasibility and objective tolerances. Here feasibility
is exact, under the narrower integral TU-fiber assumptions. This is not an
improvement over their general class. The earlier
[TU separable-convex audit](../../research-20261002/prior-art/tu-equality-separable-convex-prior.md)
concerns exact convex recourse; it does not supply this sparse nonconvex
global algorithm. No new polyhedral integrality theorem is asserted.

Targeted implementation checks and the completed-text independent review
are listed in [README.md](README.md). They test finite instances and do
not establish asymptotic superiority over existing solvers.
