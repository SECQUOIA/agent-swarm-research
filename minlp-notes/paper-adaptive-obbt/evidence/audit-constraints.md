# Independent audit of constrained OBBT and effort allocation

Date: 2026-10-05. Scope: constrained support sensitivity, nonlinear feasible
repair, progress extrapolation, and effort allocation. This audit preserves the
research inputs and changes only this file. It uses no new literature research
and reruns no numerical experiment.

I read the complete `theory/constrained-obbt.md`,
`theory/effort-allocation.md`, `document/constraints.tex`,
`document/allocation.tex`, and `reviews/theory-review.md` in
`research-20261003-adaptive-obbt/`, together with the manuscript brief and the
repository instructions. I also inspected the relevant exact checker code for
the graph and observed-decrement examples. The statements and proofs below are
independent derivations, not endorsements based on the previous review.

## Findings and inventory

The main inequalities are correct under their explicit mathematical
assumptions. Two qualifications should become explicit in the paper. First, the
ledger proof assumes serial admitted operations, or reservations that also
cover outstanding work. Its admission rule alone is insufficient for concurrent
admissions. Second, the finite-history counterexamples concern extrapolation
from positive observed changes. An exact zero residual for the unchanged
deterministic operator already certifies a fixed point, and nesting always gives
the trivial bound by the current box. Avoid a blanket claim that finite history
can never certify remaining benefit.

The prior review's blanket warning against subtracting an upper residual also
needs correction: after an exact first Jacobi update, a checked inequality
$\widehat d+Me\le e$ permits the tail bound $e-\widehat d$. Section 5 gives
the full argument and distinguishes it from an unrelated upper bound or an
inexact update.

The complete-cover sensitivity result is sound, but the source only identifies
multidimensional coverage as a separate obligation. Section 4 below supplies a
finite exact coverage certificate, including strict inequalities and boundary
cases. This closes a material missing step without assuming that a solver's
current basis covers every later box.

| Source result | Assessment | Required development or qualification |
| --- | --- | --- |
| C1: fixed-matrix dual envelope and cutoff multiplier | Correct | The multiplier gives a lower bound on support reduction. Exact old optimality is needed for the reduction measured from the old optimum. |
| C2: affine basis region | Correct, conditional | A valid independent basis proves an affine support on its entire primal-feasibility region. Finite attained support alone does not ensure that this certificate format covers every parameter. |
| C3: retained support witnesses | Correct | The upper benefit bound concerns one frozen support problem. Check all lifted coordinates and every changed row before reuse. |
| C4: complete cover gives a uniform matrix | Correct | Give an exact coverage procedure and prove invariance separately. A finite tail majorant is an additional condition. |
| C4's connection to upper-residual tails | Corrected prose | A checked upper-residual majorant permits the bound $Me\le e-\widehat d$ after a completed exact first Jacobi update. |
| C9: normalized changing-tangent example | Correct | Explain the equivalent fixed-matrix normalization for positive radius and the direct zero-radius case. |
| C10–C11: affine equality example | Correct | The exact map is for a frozen Jacobi round. The positive-cutoff limit is an exact floor only under the stated starting-radius condition. |
| C5: repair-based nonlinear width estimate | Correct | State validity at the optimizer, compact nonempty cutoff sets, uniform repair and growth neighborhoods, and assumptions on all relaxed points. |
| C15–C16: graph example | Correct; stronger rate recommended | Prove monotonicity of the whole construction and the quarter-product envelope gap. The original constants are valid. The direct repair-pair constant $L=1/2048$ gives the recommended rational rate $1/3$ under the same assumptions. |
| Finite-history examples | Correct within their information model | Include the positive-residual qualification and an explicit small-decrement counterexample. They are not examples of a standard McCormick family. |
| Enhanced-execution ledger | Correct for serial operations | Add initialization, nondecreasing charges, the serial premise, and the separate rejected-entry charge when needed. |
| Independent-baseline counterexample | Correct | It is an abstract search model. It refutes a deduction from the ledger, not a claim about a constructed SCIP instance. |
| Protected baseline scheduling and serial rescue | Correct | Retain the independent-state, fixed-work-trace, preemption, and charged-startup assumptions. These are work bounds, not measured wall-clock guarantees. |
| First-action selection example | Correct | All information available to a history-only selector must agree in the two environments. The claim is about its first action, not an impossibility of learning or competitive scheduling. |

Use the manuscript's signed order throughout: $p=(-\ell,u)$, with support
objectives $(-e_1,\ldots,-e_n,e_1,\ldots,e_n)$, extended by zeros on lifted
coordinates. The old constrained note uses $(u,-\ell)$ instead. Either ordering
works, but matrices, indices, and endpoint formulas must use one common order.
Use $\mathcal D$ for a parameter region so that $P$ remains available for a
protected coordinate hull, as required by the manuscript brief.

## 1. Scope of the support construction

Let

\[
R(\theta)=\{z\in\mathbb R^d:Az\le b+E\theta\},\qquad
h_c(\theta)=\max_{z\in R(\theta)}c^Tz.
\]

The data $A,c,b,E$ are fixed in this section.
Every parameter used has a nonempty relaxation and a finite attained support.
Equality rows can be eliminated or written as two inequalities. If $z$ is
lifted, $c$ selects an original coordinate with the appropriate sign; every
primal witness still includes all coordinates of $z$.

For exact numerical certificates, all row data and proposed primal and dual
data must be interpreted exactly. Rational arithmetic is one suitable format.
An exact support certificate proves the support of the supplied relaxation.
Validity of its rows for the original model and their node-local scope remain
separate premises.

For OBBT, let $F(p,U)$ collect these signed supports, and include every current
box row. Then $F(p,U)\le p$. If the *whole relaxation construction* is nested
when the box or cutoff is reduced, $F$ is also monotone. Neither property follows
from an arbitrary affine right-hand-side parametrization without the respective
box-row and nesting assumptions.

## 2. Dual and primal certificates give opposite benefit bounds

**Proposition 1 (global fixed-matrix dual envelope).** If $y\ge0$ and
$A^Ty=c$, then for every permitted $\theta$,

\[
h_c(\theta)\le D_y(\theta):=y^T(b+E\theta).
\]

The minimum of any nonempty finite collection of these affine expressions is
also an upper bound. No old primal point or basis needs to remain feasible or
optimal.

*Proof.* For every feasible $z$,
$c^Tz=y^TAz\le y^T(b+E\theta)$. Maximize over $z$. Every stored expression
bounds the same support, so their minimum does as well. This proof uses only
dual feasibility for the current fixed matrix. ∎

Suppose only the cutoff row $a^Tz\le U$ changes, and a stored primal-dual pair
is exactly optimal at $U_0$. Write $\eta\ge0$ for that row's multiplier.
For a nonempty new relaxation at $U\le U_0$,

\[
h_c(U)\le h_c(U_0)+\eta(U-U_0),\qquad
h_c(U_0)-h_c(U)\ge\eta(U_0-U).
\]

The affine dual value agrees with the exact old support at $U_0$, and its only
changing term is $\eta U$, proving both statements. The sign is therefore a
*guaranteed reduction*, rather than a ceiling on the reduction. If $\eta=0$,
the conclusion is only the already valid nonincrease; a later active-set switch
can still produce useful tightening. If the old optimality gap is unverified,
the affine expression remains valid, but equality with $h_c(U_0)$ cannot be
assumed.

**Proposition 2 (retained witnesses and a support bracket).** Fix the box and
all rows except the cutoff. Let $p_i$ be the current signed endpoint, and let
$W_i$ contain fully feasible lifted points for those fixed rows. At a new cutoff
$U$, define

\[
W_i(U)=\{z\in W_i:a^Tz\le U\},\qquad
L_i(U)=\max_{z\in W_i(U)}c_i^Tz
\]

when $W_i(U)\ne\varnothing$. For an exact support $F_i(U)$ and any valid dual
envelope $D_i(U)$,

\[
L_i(U)\le F_i(U)\le\min\{p_i,D_i(U)\},
\]

and consequently

\[
\max\{0,p_i-D_i(U)\}\le p_i-F_i(U)\le p_i-L_i(U).
\]

*Proof.* Every retained point is feasible for the new support problem. The
upper bounds are the current box row and Proposition 1. Subtract these support
bounds from $p_i$. ∎

An old exact support witness $z^0$ proves $h_c(U)=h_c(U_0)$ for
$a^Tz^0\le U\le U_0$: the new relaxation is contained in the old one, while
$z^0$ still attains the old value. Among stored old optimal witnesses, the
smallest objective value provides the widest such interval. Computing the
smallest objective value over the whole optimal face is a separate optimization
problem; its cost and attainment assumptions cannot be hidden.

These statements do not cover rebuilt rows. When the box, cutoff expression,
or any local row changes, recheck each retained witness in the actual new lifted
relaxation. Exclusion of an old witness does not prove new tightening or
infeasibility. A whole-round benefit bound needs information for every direction
whose change is bounded. The result concerns one round, unless an additional
protected-box or uniform-tail certificate is established.

## 3. Exact basis regions and their availability

**Proposition 3 (exact basis region).** Choose $d$ row indices $I$ such that
$A_I$ is nonsingular. Set

\[
v_I=A_I^{-1}b_I,\qquad V_I=A_I^{-1}E_I,\qquad
z_I(\theta)=v_I+V_I\theta,
\]

and define $y_I=A_I^{-T}c$, extended by zero outside $I$. If $y_I\ge0$, then
on the closed polyhedron

\[
C_I=\{\theta:(AV_I-E)\theta\le b-Av_I\},
\]

the exact support is

\[
h_c(\theta)=c^Tv_I+c^TV_I\theta.
\]

The polyhedron and affine value formula are rational when their input data are
rational.

*Proof.* The definition of $C_I$ verifies every primal row. The extended $y$ is
nonnegative and has $A^Ty=c$. The rows in $I$ are tight, so
$c^Tz_I=y^TAz_I=y^T(b+E\theta)$. Proposition 1 gives a matching upper bound.
∎

All nonbasis residuals must be checked with the same exact arithmetic as the
basis solve. Exact arithmetic on the basis alone does not establish feasibility
of a point in a model containing unchecked floating residuals. Zero multipliers,
ties, and lower-dimensional regions are allowed. Rejecting a singular proposed
basis rejects that proposal, not the relaxation or the existence of a useful
certificate.

If a proposed parameter polytope is explicitly the convex hull of finitely many
vertices, checking all affine residuals at those vertices proves its containment
in $C_I$. The claim is containment, not coverage by a collection of regions.
In a scalar cutoff parameter, each residual is one affine inequality in $U$;
intersecting all of them gives the exact basis interval. The dual remains valid
outside that interval even though the primal formula need not be feasible.

The finite-cover hypothesis is substantive. A family can have nonempty sets and
finite attained supports in its selected directions but no independent $d$-row
basis. For example, let $s$ be the original coordinate and $t$ a free lifted
coordinate. Then $R=\{(s,t):s=0\}$ has attained supports $\max s=\max(-s)=0$,
but its two opposite constraint rows have rank one and no two-dimensional basis.
A numerical solver's
first active set is therefore not guaranteed to provide this certificate
format under the source's minimal support assumptions.

There is a simple sufficient condition for availability. If every $R(\theta)$
is a nonempty compact polytope, enumerate all independent $d$-row subsets and
retain those with $A_I^{-T}c\ge0$. Their regions cover all permitted parameters.
Indeed, an optimal vertex exists. Its active rows span $\mathbb R^d$, and LP
duality and complementary slackness express $c$ as a nonnegative combination of
its active row normals. Choose such a representation with a minimal number of
positive coefficients. Those normals are independent: a linear dependence
would permit moving the coefficients along the dependence until one becomes
zero, while preserving nonnegativity and the represented vector. Extend this
independent subset to $d$ independent active rows, assigning zero coefficients
to the added rows. It gives a basis $I$ with the optimal vertex $z_I(\theta)$
and $A_I^{-T}c\ge0$. This argument justifies exhaustive enumeration under the
additional compact-polytope premise; it is not an efficiency claim.

### Exact cutoff intervals and a zero old multiplier

Minimize $y$ over $0\le x\le3$, $0\le y\le4$, with
$x-y\le1$, $4x-y\le7$, and $x\le5/2$. Add $y\le U$ for
$0\le U\le4$, and maximize $x$ to tighten its upper endpoint. The exact
support is

\[
h_x(U)=\min\{1+U,7/4+U/4,5/2\}
=\begin{cases}
1+U,&0\le U\le1,\\
7/4+U/4,&1\le U\le3,\\
5/2,&3\le U\le4.
\end{cases}
\]

For the first interval, use the basis rows $x-y\le1$ and $y\le U$;
their multipliers are $(1,1)$ and their primal point is $(1+U,U)$.
The inequality $4x-y\le7$ becomes $4+3U\le7$, so its interval within
$[0,4]$ is exactly $[0,1]$. For the second interval, use $4x-y\le7$
and $y\le U$, with multipliers $(1/4,1/4)$ and point
$(7/4+U/4,U)$. Its first coupling row requires $U\ge1$ and its cap
$x\le5/2$ requires $U\le3$; the remaining rows hold throughout $[1,3]$.
For the third interval, use $x\le5/2$ and $y\le U$, with multipliers
$(1,0)$ and point $(5/2,U)$. The row $4x-y\le7$ requires $U\ge3$,
and the box requires $U\le4$. These verified closed intervals cover $[0,4]$.
Each point meets its dual bound, proving both the piecewise formula and cutoff
slopes $1,1/4,0$.

At $U_0=4$, the old cutoff multiplier is zero, but changing to $U=2$ reduces
the support from $5/2$ to $9/4$. The old optimal witness $(5/2,3)$ proves no
change only for $3\le U\le4$. The threshold $3$ is exact because any point
with $x=5/2$ needs $y\ge3$ by the second coupling row.

At $U_0=2$, the old dual remains feasible at $U=1/2$ and gives upper bound
$7/4+(1/2)/4=15/8$. Its extrapolated primal point is infeasible, since
$x-y=11/8>1$, but the actual support is $3/2$. The old multiplier therefore
guarantees reduction $3/8$, while the actual reduction is $3/4$. This explicitly
distinguishes a valid dual extrapolation from both an exact basis prediction
and an upper bound on tightening benefit.

## 4. A finite exact certificate of complete coverage

**Proposition 4 (coverage by strict-violation tests).** Let
$\mathcal D\subset\mathbb R^k$ be a nonempty compact rational polytope, and
let the proposed regions be

\[
C^r=\{p:H^rp\le h^r\},\qquad r=1,\ldots,K,
\]

with finite rational inequality lists. If a region has no inequalities, it
already covers $\mathcal D$. Otherwise, for every tuple $J=(j_1,\ldots,j_K)$
choosing one inequality from each region, consider the rational LP

\[
\begin{split}
\tau_J=\max_{p,t}\quad &t\\
\text{subject to}\quad &p\in\mathcal D,\quad t\le1,\\
&t\le H^r_{j_r}p-h^r_{j_r},\qquad r=1,\ldots,K.
\end{split}
\]

Then

\[
\mathcal D\subseteq\bigcup_{r=1}^K C^r
\quad\Longleftrightarrow\quad
\tau_J\le0\text{ for every tuple }J.
\]

*Proof.* Every displayed LP is feasible: choose any point of $\mathcal D$ and
let $t$ be sufficiently negative. Its maximum is finite and attained, since it
is the maximum over compact $\mathcal D$ of the continuous function
$\min\{1,H^1_{j_1}p-h^1_{j_1},\ldots,H^K_{j_K}p-h^K_{j_K}\}$.

If some $p\in\mathcal D$ lies outside every closed region, choose for each
region a row it strictly violates. The minimum of these finitely many positive
violations and $1$ is positive and supplies a feasible $t>0$ for the resulting
tuple. Conversely, any feasible point with $t>0$ strictly violates a row in
every region and lies outside their union. These implications prove the
equivalence. ∎

An exact dual feasible vector with objective at most zero for every tuple is a
finite coverage certificate; Proposition 1 verifies each LP upper bound. It
does not require a proposed primal optimum for those auxiliary tests. A positive
exact feasible $t$ supplies an explicit hole. Because $t$ is allowed to be
negative, no auxiliary infeasibility certificate is needed. Zero maxima correctly
handle shared boundaries. The number of tuples can be large; this is a finite
verification procedure rather than a claim of inexpensive coverage discovery.

Checking only the vertices of $\mathcal D$ for membership in the union is
insufficient. For $\mathcal D=[-1,1]^2$, the regions $x\le-1/2$ and
$x\ge1/2$ cover all four vertices but leave a central strip uncovered. The
single violation tuple has constraints $t\le x+1/2$ and $t\le-x+1/2$,
so its optimum is $1/2$, attained at $x=0$. Adding the two inequalities gives
the matching exact upper bound $2t\le1$. By contrast, the regions $x\le0$
and $x\ge0$ give $t\le x$, $t\le-x$, and optimum zero, proving coverage
including the common boundary.

Apply this test separately to each support direction's basis-region collection.
Every retained region must first satisfy Proposition 3. Completeness for one
direction does not imply completeness for the other coordinate supports.

## 5. A complete cover supplies the uniform comparison matrix

**Proposition 5 (uniform comparison across basis changes).** Fix the cutoff.
Let $\mathcal D$ be a convex parameter region. For each signed support
coordinate $i$, suppose finitely many verified closed polyhedral regions cover
$\mathcal D$, and the exact support on each region is

\[
F_i(p)=\alpha_{ir}+g_{ir}^Tp.
\]

If $M\ge0$ satisfies $|(g_{ir})_j|\le M_{ij}$ for every region and index,
then

\[
|F(p)-F(q)|\le M|p-q|\qquad(p,q\in\mathcal D)
\]

componentwise. For basis regions in Proposition 3, the gradient is
$g_{ir}=E_{I_r}^TA_{I_r}^{-T}c_i$ after absorbing the fixed cutoff into $b$
and restricting $E$ to its endpoint columns.

*Proof.* Parametrize the segment by $p(t)=p+t(q-p)$, $0\le t\le1$.
Convexity keeps it in $\mathcal D$. The intersection of each closed polyhedral
region with the segment is a closed interval, a point, or empty. Collect the
finitely many interval endpoints and the endpoints $0,1$. Between consecutive
breakpoints, choose a region covering the interval for direction $i$. On it the
support is the certified affine expression. At a breakpoint, the neighboring
closed regions give the same exact support, so telescoping introduces no jump.
On an interval of length $\Delta t$ its change has magnitude at most
$\Delta t\sum_jM_{ij}|q_j-p_j|$. Sum over the partition, whose lengths add
to one. This proves the bound for coordinate $i$, and hence for every coordinate.
∎

For an invariant order interval, suppose a protected signed endpoint vector
$p^P$ satisfies $F(p^P)=p^P$, the current vector is $p^0\ge p^P$, and the
whole construction is monotone and deflationary. Then

\[
p^P\le F(p)\le p\le p^0\qquad(p^P\le p\le p^0),
\]

which proves invariance of $[p^P,p^0]$. A protected box at a different cutoff
does not establish this statement unless its witnesses remain feasible at the
actual cutoff.

For completeness, the precise connection to a tail certificate is as follows.
Let $p^{k+1}=F(p^k)$ remain in $\mathcal D$, and set
$d_k=p^k-p^{k+1}\ge0$. Then

\[
d_{k+1}=F(p^k)-F(p^{k+1})\le Md_k.
\]

If $e\ge0$ satisfies $d_0+Me\le e$, then for every $m\ge1$,

\[
\sum_{j=0}^{m-1}M^jd_0+M^me\le e,
\]

by induction: substitute $d_0+Me\le e$ in the final term. Hence
$\sum_{k=0}^{m-1}d_k\le e$, and nested endpoint limits give
$p^0-p^\infty\le e$. After the completed exact first Jacobi update, the
stronger tail bound is $p^1-p^\infty\le Me\le e-d_0$.

If only an upper residual $\widehat d\ge d_0$ is available and the checked
majorant satisfies $\widehat d+Me\le e$, then it is also valid to use
$p^1-p^\infty\le Me\le e-\widehat d$ after that exact first update.
Indeed, the same finite-partial-sum proof bounds the total by $e$, and its
image under $M$ bounds the sum starting with $d_1$. Thus the archived blanket
warning against subtracting an upper residual needs correction. An unrelated
upper bound cannot be subtracted from a certificate checked only against
$d_0$, and this argument does not apply after an arbitrary partial or inexact
update. A spectral radius below one is a sufficient route to a finite $e$,
not a consequence of complete coverage and not necessary for the displayed
majorant inequality. No tail claim follows from gradients certified only in
the present region.

### Fixed-matrix scope is useful and must remain explicit

Whole-family nesting alone does not preserve a stored dual when coefficients
change. For $0<r\le1$, consider

\[
R_r=\{x:0\le x\le r,\ rx\le r^2\}=[0,r],\qquad c=1.
\]

This family is valid for the singleton feasible set $\{0\}$ and is nested in
$r$. At $r=1$, multiplier one on the last row is an exact optimal dual.
Keeping that multiplier at $r=1/2$ and reusing its new right-hand-side value
would claim $h(1/2)\le1/4$, although $h(1/2)=1/2$. The stored multiplier
is no longer dual feasible: the changing row coefficient is $1/2$, not one.
Positive row normalization makes this particular family fixed-matrix, but a
general rebuilt McCormick family does not acquire this property automatically.

No general changing-matrix extension is needed to make the paper's stated
scope useful. Frozen-box cutoff reuse is already exact and useful. The next
example supplies a complete box-change certificate through an explicitly
valid normalization. A broader varying-coefficient theorem should not be
implied without separate primal, dual, derivative, and coverage verification.

### Complete changing-tangent example

For $x^2\le0$ and $0\le x\le r$, take tangents at
$t_1=r/2$ and $t_2=r/8+3/4$. Since
$x^2\ge2tx-t^2$, every true feasible point satisfies $2tx-t^2\le0$.
For $r>0$, both tangent locations are positive, so these rows are exactly
equivalent to

\[
x\le r/4,\qquad x\le r/16+3/8.
\]

Together with $x\ge0$ and $x\le r$, they are fixed-matrix rows with affine
right-hand sides. At $r=0$, the first tangent is the vacuous inequality
$0\le0$, but the box already fixes $x=0$; the normalized zero-radius family
is equivalent as a whole without dividing by zero. On $[0,8]$ the support is

\[
F(r)=\min\{r/4,r/16+3/8\}.
\]

The box upper row is redundant since $r/4\le r$. The two lines meet at
$r=2$, giving the complete regions $[0,2]$ and $[2,8]$. Their slopes are
$1/4$ and $1/16$. Thus $M=[1/4]$ is uniform, and $0\le F(r)\le r\le8$
proves invariance. The exact trajectory is

\[
8\longmapsto7/8\longmapsto7/32\longmapsto7/128\longmapsto\cdots.
\]

The first width ratio $7/64$ is smaller than the next ratio $1/4$. Its first
active region therefore does not supply the later contraction factor. This is
a certificate example, not a difficult optimization instance or performance
claim; direct propagation recognizes $x=0$ immediately.

## 6. An affine equality changes the exact OBBT map

Consider $f(x,y)=(x-y)^2=x^2+y^2-2xy$ on $[-r,r]^2$, retaining both squares
exactly. The McCormick upper estimator of $xy$ is

\[
m_r^U(x,y)=\min\{r^2+r(x-y),r^2-r(x-y)\}
=r^2-r|x-y|.
\]

Consequently the relaxed objective is
$\phi_r(x,y)=x^2+y^2-2r^2+2r|x-y|$. Without the equality, the two true
zero-objective points $(r,r)$ and $(-r,-r)$ retain every box face at cutoff
zero, so its Jacobi hull is unchanged.

**Proposition 6 (exact equality-constrained map and floor).** Impose the
affine equality $y=-x$ exactly. At a fixed cutoff $U\ge0$, a frozen Jacobi
round returns $[-G_U(r),G_U(r)]^2$, where

\[
G_U(r)=\min\{r,\sqrt{2r^2+U/2}-r\}.
\]

For $U=0$ and $r>0$, the exact radius ratio is $\sqrt2-1$. For $U>0$,
put $a=\sqrt U/2$. Every sequence starting at $r_0\ge a$ decreases to
$a$; if $r_0<a$, it remains equal to $r_0$.

*Proof.* On the equality, put $(x,y)=(t,-t)$. The relaxed cutoff is
$2|t|^2+4r|t|-2r^2\le U$. Its nonnegative root is
$\sqrt{2r^2+U/2}-r$, and the box limits $|t|$ to $r$. Symmetry gives
both signs of both coordinate supports, proving the Jacobi map.

For $r>a$, the root is strictly below $r$. It is at least $a$ because
$2r^2+2a^2-(r+a)^2=(r-a)^2\ge0$. Thus the sequence is decreasing and
bounded below by $a$. At a limit $L\ge a$, continuity gives $G_U(L)=L$;
the strict decrease for $L>a$ forces $L=a$. For $r\le a$ the root is at
least $r$, so the box is fixed. For $U=0$, factor $r$ out of the root. ∎

Eliminating the equality first gives $f(x,-x)=4x^2$. The exact convex cutoff
then returns radius $\min\{r,\sqrt U/2\}$ in one round. The iterative rate
belongs to the formulation and relaxation, not to the original constrained
problem alone. The source's assertion of the positive floor is correct for
$r_0\ge\sqrt U/2$; the condition should not be dropped.

For a general affine equality, an existing uniform tangent expansion can be
restricted to its exact nullspace. This observation is conditional on that
expansion, its admitted shape family, and the requisite strict support
contraction. It is not an additional unconditional rate theorem. Nonlinear
active constraints cannot simply be replaced by their first-order tangent cone:
finite-box residual and remainder bounds must still be proved. The next theorem
provides a fully stated alternative with such bounds.

## 7. Nonlinear constraints through a feasible repair

Let $S$ be the original feasible set and $x^*\in S$ a minimizer with value
$f^*$. Consider boxes $B$ containing $x^*$ in a fixed neighborhood and the
projected relaxed objective $\phi_B$. Equivalently, use the value $+\infty$
outside the projection of the lifted feasible rows. Write

\[
K_U(B)=\{x\in B:\phi_B(x)\le U\},\quad
T_U(B)=\operatorname{box}K_U(B),\quad
w(B)=\max_i(u_i-\ell_i).
\]

Assume validity at $x^*$, $\phi_B(x^*)\le f^*$, and compactness of each
cutoff set. Let $\nu(x)\ge0$ be a constraint residual that vanishes on $S$.
For all projected feasible relaxed points, assume uniform constants
$a,b,\kappa,L\ge0$, $\mu>0$, and $0<\theta\le1$ such that

\[
\phi_B(x)\ge f(x)-aw(B)^2,\qquad
\nu(x)\le bw(B)^2,
\]

and a feasible repair $y\in S$ exists with

\[
\|x-y\|_\infty\le\kappa\nu(x)^\theta,\qquad
f(y)\le f(x)+L\|x-y\|_\infty,\qquad
f(y)\ge f^*+\mu\|y-x^*\|_\infty^2.
\]

The repair need not lie in $B$, but it must lie in the feasible-growth
neighborhood and in the domain of the objective-change estimate. These are
assumptions on all pertinent relaxed points, including infeasible points, not
only on a support optimizer or a point with a small KKT residual. A Lipschitz
bound on a neighborhood containing the repair pairs suffices, but only the
displayed one-sided inequality is needed.

**Theorem 7 (repair-based width bound).** For $U=f^*+\epsilon$ with
$\epsilon\ge0$, set $w=w(B)$ and $r=\kappa(bw^2)^\theta$. Then

\[
w(T_U(B))\le2r+2\sqrt{\frac{\epsilon+aw^2+Lr}{\mu}}.
\]

If $\theta=1$, define $K=\kappa b$ and
$q=2\sqrt{(a+LK)/\mu}$. If $q<1$, choose an admitted width bound
$\overline w>0$ with $\lambda=q+2K\overline w<1$. For every such box of
width at most $\overline w$,

\[
w(T_U(B))\le\lambda w(B)+c,\qquad c=2\sqrt{\epsilon/\mu}.
\]

For nested iterates $B_{k+1}=T_U(B_k)$ starting in that width neighborhood,

\[
w(B_k)\le\lambda^kw(B_0)+c\frac{1-\lambda^k}{1-\lambda},
\qquad
\limsup_{k\to\infty}w(B_k)\le\frac{c}{1-\lambda}.
\]

At $\epsilon=0$, the widths contract with upper ratio $\lambda$.
If $K=0$, set $\lambda=q$ on any neighborhood where the other assumptions
hold. Any larger constant below one can replace the displayed $\lambda$.

*Proof.* Validity at $x^*$ implies $x^*\in K_U(B)$, so the set is nonempty.
For $x\in K_U(B)$, the objective error gives
$f(x)\le f^*+\epsilon+aw^2$. Its repair has distance at most $r$ and
objective at most $f^*+\epsilon+aw^2+Lr$. Feasible growth therefore gives

\[
\|y-x^*\|_\infty\le\sqrt{(\epsilon+aw^2+Lr)/\mu}.
\]

The triangle inequality adds $r$ to bound $\|x-x^*\|_\infty$. Each
coordinate range of $K_U(B)$ is at most twice this common radius, proving the
first inequality. For $\theta=1$, $r=Kw^2$ and

\[
w(T_U(B))\le2Kw^2+qw+2\sqrt{\epsilon/\mu}
\le(q+2K\overline w)w+c.
\]

Here $\sqrt{s+t}\le\sqrt s+\sqrt t$ splits off the cutoff slack. Because
$T_U(B)\subseteq B$, nesting keeps widths at most $\overline w$ and keeps
all original points in the original box neighborhood. Validity keeps $x^*$ in
every iterate. The assumptions separately keep repairs in their prescribed
neighborhood. Induction on the scalar recurrence proves the finite-$k$ bound,
and taking the limit gives the upper floor. ∎

The one-step proof does not require an active-set guess. It also does not prove
its own repair, error, or growth constants. The positive-slack expression is an
upper bound on the limiting width, not an exact floor; nesting also gives the
trivial upper bound $w(B_0)$.

For $\theta<1$, write $r=Cw^{2\theta}$ with $C=\kappa b^\theta$.
At zero slack and $LC>0$, the bound contains
$2\sqrt{LC/\mu}\,w^\theta$, whose ratio to $w$ grows as $w\downarrow0$.
This estimate alone therefore does not certify linear contraction. It does not
prove a stall. A local repair-pair constant $L_B=O(w^{2-2\theta})$ makes the
square-root term $O(w)$, but the separate repair term must also be $O(w)$.
For fixed positive $C$, this requires $\theta\ge1/2$ under these particular
bounds, and a strict rate still requires sufficiently small leading constants.
For $\theta<1/2$, a stronger repair-distance estimate or other structure would
be needed by this argument.

## 8. Fully worked nonlinear graph example

Let

\[
S=\{(x,y):y=x^2\}\cap([-1/4,1/4]\times[0,1/16]),\qquad
f(x,y)=x^2+y^2-xy/16.
\]

For a box $B=[\ell,u]\times[0,v]$ with
$-1/4\le\ell\le0\le u\le1/4$ and $0\le v\le1/16$, use its box rows,
the graph relaxation

\[
x^2\le y\le(\ell+u)x-\ell u,
\]

and the objective estimator

\[
m_B^U(x,y)=\min\{uy,\ell y+v(x-\ell)\},\qquad
\phi_B(x,y)=x^2+y^2-m_B^U(x,y)/16.
\]

The estimator is convex: it is the maximum of two convex quadratics obtained
by subtracting each affine upper-estimator row. The feasible graph relaxation
is convex as the intersection of a square epigraph, an affine halfspace, and
the box. The origin is feasible, with $\phi_B(0,0)=0$, and all cutoff sets
for $U\ge0$ are compact and nonempty.

### Validity and whole-construction monotonicity

For $x\in[\ell,u]$,

\[
(\ell+u)x-\ell u-x^2=(x-\ell)(u-x)\ge0,
\]

so the secant is valid. The two bilinear errors are
$(u-x)y$ and $(x-\ell)(v-y)$, both nonnegative on the box; hence
$m_B^U\ge xy$ and $\phi_B\le f$.

For a nested box $B'=[\ell',u']\times[0,v']$, the factors
$x-\ell'\le x-\ell$ and $u'-x\le u-x$ show that its graph secant is
no higher on $B'$. Its first bilinear upper row satisfies $u'y\le uy$.
For its second upper row,

\[
\ell'y+v'(x-\ell')\le\ell'y+v(x-\ell')
\le\ell y+v(x-\ell).
\]

The first inequality uses $x\ge\ell'$ and $v'\le v$; the second uses
$(\ell'-\ell)(y-v)\le0$. Thus $m_{B'}^U\le m_B^U$ and
$\phi_{B'}\ge\phi_B$ on $B'$. The projected feasible rows and objective
sublevels both become smaller. This proves nesting of the whole construction.
Since the origin remains feasible and every relaxed $y$ is nonnegative, OBBT
keeps the lower $y$ bound equal to zero, so its descendants remain in this box
family.

### Uniform repair and objective error

Every relaxed point has the feasible repair $(x,y)\mapsto(x,x^2)$.
It lies in the same box because $0\le x^2\le y\le v$. Its infinity-norm
distance is exactly $\delta=y-x^2$, and

\[
0\le\delta\le(x-\ell)(u-x)\le(u-\ell)^2/4\le w(B)^2/4.
\]

The quarter bound follows from
$(x-\ell)(u-x)=(u-\ell)^2/4-(x-(\ell+u)/2)^2$.
Take $\nu(x,y)=|y-x^2|$, $b=1/4$, $\kappa=1$, and $\theta=1$.

For nonzero $d=u-\ell$ and $v$, put $t=(x-\ell)/d$ and $s=y/v$.
Then

\[
m_B^U-xy=dv\min\{(1-t)s,t(1-s)\}\le dv/4.
\]

If $s\le t$, the first expression is at most $t(1-t)$; if $s\ge t$,
the second expression is at most $t(1-t)$. In either case
$t(1-t)\le1/4$. When either width is zero, the product is exact directly.
Thus

\[
0\le f-\phi_B\le\frac{(u-\ell)v}{64}\le\frac{w(B)^2}{64},
\]

and $a=1/64$ is valid for every admitted box shape.

### The source constants and rate

The outer rectangle contains each repair pair and the segment joining it.
Since $\partial_xf=2x-y/16$ and $\partial_yf=2y-x/16$,

\[
|\partial_xf|+|\partial_yf|
\le(2+1/16)(|x|+|y|)
\le(2+1/16)(1/4+1/16)=165/256.
\]

This is a Lipschitz constant with respect to the infinity norm, so
$L=165/256$ satisfies the required one-sided bound. On the feasible graph,

\[
f(x,x^2)=x^2(1-x/16+x^2)\ge(63/64)x^2
=(63/64)\|(x,x^2)\|_\infty^2.
\]

Here $|x|\le1/4$ implies $|x^2|\le|x|$ and $x/16\le1/64$.
Thus the origin is the unique minimizer, $f^*=0$, and $\mu=63/64$ works
throughout the repair neighborhood.

With $K=1/4$,

\[
q^2=4\frac{a+LK}{\mu}=\frac{181}{252}<\frac{49}{64}.
\]

Consequently, for boxes of width at most $1/8$,
$q+2K(1/8)<7/8+1/16=15/16$, and Theorem 7 gives the valid rational bound

\[
w(T_U(B))\le\frac{15}{16}w(B)+2\sqrt{64\epsilon/63}.
\]

The starting box for this contraction claim must already have width at most
$1/8$. The larger outer rectangle is the domain on which the constants are
proved; it is not an initial box covered by this rate claim. At zero cutoff,
the descendants contract uniformly across all box shapes in the specified
width neighborhood. The constants are sufficient bounds, not exact rates.
The example uses exact square epigraphs; the measured finite-tangent LP needs
its own objective and residual error bounds and does not inherit this rate.

### Recommended stronger rate from the repair-pair constant

The source's conservative constant is valid, but the paper should use the
stronger direct repair-pair estimate. The theorem needs only the one-sided
objective change, and for every graph-relaxed point, with $\delta=y-x^2\ge0$,

\[
\begin{split}
f(x,x^2)-f(x,y)
&=\delta(x/16-2x^2-\delta)\\
&=\delta\bigl(1/2048-2(x-1/64)^2-\delta\bigr)
\le\delta/2048.
\end{split}
\]

Thus $L=1/2048$ is valid under the same all-point assumptions, without changing
the repair or any domain. The identity does not require the cutoff. It gives

\[
q^2=4\frac{1/64+(1/2048)(1/4)}{63/64}=\frac{43}{672},\qquad
\left(\frac{13}{48}\right)^2-\frac{43}{672}=\frac{151}{16128}>0.
\]

At $w(B)\le1/8$ one may therefore use $\lambda=1/3$, because
$q+1/16<13/48+1/16=1/3$. The recommended bound is

\[
w(T_U(B))\le\frac13w(B)+2\sqrt{64\epsilon/63}.
\]

This is an analytic sharpening beyond transcription of the archived example.
It still does not establish an exact rate or a runtime advantage.

## 9. What positive observed progress cannot establish

**Proposition 8 (arbitrarily long common histories).** Fix $N\ge2$, set
$a=1/2$, $\delta=1/(2N)$, $b=a-\delta>0$, and $q=1/4$. On $[0,1]$,
define

\[
F_{\rm stall}(s)=\min\{s,\max\{b,s-\delta\}\},
\]

and

\[
F_{\rm shrink}(s)=
\begin{cases}
qs,&0\le s\le b,\\
qb+(b-qb)(s-b)/(a-b),&b\le s\le a,\\
s-\delta,&a\le s\le1.
\end{cases}
\]

Both maps are continuous and nondecreasing, with $0\le F(s)\le s$.
The trajectories from $s_0=1$ agree through
$s_{N+1}=b$, after which one stays at $b$ and the other converges to zero.

*Proof.* The stall map is $s$ below $b$, $b$ on $[b,a]$, and $s-\delta$
above $a$, giving continuity, nonnegative slopes, and $F\le s$. For the
shrink map, its pieces meet at values $qb$ at $b$ and $b=a-\delta$ at
$a$. Every slope is nonnegative. The inequality $F\le s$ holds at both
endpoints of each affine piece, and hence throughout each piece. From one,
both maps subtract $\delta$ until $s_N=a$ and then $s_{N+1}=b$. Thereafter
$F_{\rm stall}(b)=b$, while the shrink map multiplies each subsequent value
by $q$. ∎

Every shared ratio before reaching $b$ is at least $1-1/N$, since the input
radius is at least $a$. Thus arbitrarily many ratios can be close to one while
the eventual total reduction after the common history is either zero or $b$.
Each $R_s=[0,F(s)]$ is a valid nested outer relaxation of the singleton feasible
set $\{0\}$, and its upper OBBT support is exactly $F(s)$. No standard
McCormick construction is claimed for these families.

There is also a direct counterexample to extrapolating a *small decrement
ratio*. Define each map by linear interpolation between its listed knots:

\[
\begin{array}{ll}
\text{stall:}&(0,0),\ (899/1000,899/1000),\
 (9/10,899/1000),\ (1,9/10),\\
\text{shrink:}&(0,0),\ (1/10,0),\ (899/1000,1/10),\
 (9/10,899/1000),\ (1,9/10).
\end{array}
\]

The knot values are nondecreasing and lie between zero and their input
coordinates. The interpolated maps therefore have the same validity and
nesting properties as above. Both trajectories begin
$1,9/10,899/1000$. The observed decrements are $1/10$ and $1/1000$, whose
ratio is $1/100$. The stall map then stays at $899/1000$; the shrink map
continues to $1/10$ and then zero. An unsupported geometric estimate would
predict total movement after the first round of at most

\[
\frac{1/1000}{1-1/100}=1/990,
\]

whereas the shrinking trajectory actually moves $9/10$. The missing premise
is a uniform inequality for future displacements, such as the certified
comparison matrix of Proposition 5; the observed ratio does not provide it.

The conclusion must retain its scope. Nesting always bounds future movement by
the current endpoints. Moreover, if a completed exact round returns exactly the
same box for an unchanged deterministic operator and cutoff, the box is a fixed
point, and its future OBBT movement is zero. The examples refute a general
inference from *positive* observed changes to a small tail or eventual stall;
they do not refute exact residual certificates, protected boxes, or
structure-specific screening methods.

## 10. A ledger bounds work on the enhanced execution

**Proposition 9 (serial enhancement ledger).** Initialize $E=0$ and let $N$
be nonnegative, nondecreasing native work charged on one enhanced execution.
Let optional operations be serial, and admit an operation only when
$E<b+\eta N$, with $b,\eta\ge0$. Suppose every increment of $E$ belongs
to an admitted operation and every such operation, including all surrounding
work, adds at most $\delta\ge0$ to $E$. At every completed operation,

\[
E\le b+\eta N+\delta,\qquad
N+E\le(1+\eta)N+b+\delta.
\]

If an enforced whole-operation upper bound $r$ is reserved before admission,
and admission requires $E+r\le b+\eta N$, then $\delta$ can be omitted.

*Proof.* Immediately before a completed admitted operation, the admission
inequality holds. Since operations are serial, no earlier operation contributes
additional uncharged cost after that admission. Its increment is at most
$\delta$, and any simultaneous or later native charge can only increase
$b+\eta N$. This establishes the first inequality after every admitted
operation; intervals containing only native work preserve it. If no operation
has been admitted, $E=0$. Add $N$ for the second inequality. With an advance
reservation, the completed increment is at most $r$ and the admission
inequality directly gives $E\le b+\eta N$. ∎

The serial premise is material to the stated rule. With $b=1$, $\eta=0$,
$\delta=1$, and initially $E=N=0$, three operations can all be admitted
before any charges are added. If each then costs one, $E=3>1+1$. A concurrent
implementation needs admission to include outstanding reservations as well as
completed charges. Serial callbacks require only the simpler proposition above.

Charge discovery, model assembly, screening, optimization, verification,
bookkeeping, and failed admitted attempts. A time limit only on an auxiliary LP
does not establish a bound on this whole operation. If rejected callbacks or
admission checks incur unreserved work $J$, apply the proposition to $E$
excluding those charges, and total charged work is

\[
N+E+J\le(1+\eta)N+b+\delta+J.
\]

Without a bound on $J$, there is no total enhancement-overhead guarantee. An
unknown noninterruptible overrun likewise cannot be replaced by a nominal LP
limit. Work and elapsed time agree only when the charge model accounts for
the elapsed costs being claimed.

Here $N$ is native work on the **enhanced trajectory**. It is not the independent
baseline requirement $N_0$. The ledger contains no premise connecting the two.

### An explicit logical counterexample to a baseline runtime bound

For each $M\ge1$, let a deterministic abstract search procedure have two
legal choices at its first decision. The default ordering obtains a complete
proof after one work unit. A redundant row changes the ordering, and that legal
execution obtains a proof after $M$ work units. Generating the row costs a fixed
$b>0$. Reserve that cost at the start, using $\eta=0$. The admission
$E+b\le b$ holds at $E=N=0$, and the completed enhancement has $E=b$.
Thus the strongest reservation ledger is respected, while

\[
N_0=1,\qquad N=M,\qquad
\frac{N+E}{N_0}=M+b,
\]

which is unbounded. This is an abstract search model showing exactly which
premise is absent from the attempted deduction. It is not a constructed SCIP
or QCQP instance, and it predicts no solver's actual runtime.

Similarly, a certified bound on remaining endpoint or width movement measures
the stated OBBT operator. It does not bound remaining search time. Turning
width benefit into saved seconds needs an additional validated performance
model; a soundness certificate does not provide that model.

## 11. An independent baseline supplies a different bound

**Proposition 10 (protected baseline allocation).** In an ideal preemptible
work model, run solvers $A$ and $H$ on the same original input, with independent
states and fixed random tapes. Their progress after a specified amount of work
must be the same as in their standalone executions. Let their standalone
completion requirements be $T_A,T_H$. For $0<\alpha<1$ and $h\ge0$, suppose
that by aggregate work time $t$, before either completes, $A$ receives at least
$(1-\alpha)t-h$ work and $H$ receives at least $\alpha t-h$ work. Then the
first complete answer occurs by

\[
\min\left\{\frac{T_A+h}{1-\alpha},\frac{T_H+h}{\alpha}\right\}.
\]

*Proof.* If neither has finished by
$t_A=(T_A+h)/(1-\alpha)$, the allocation premise gives at least $T_A$
work to $A$, which would finish by its unchanged work trace, a contradiction.
The same argument applies at $t_H=(T_H+h)/\alpha$. The first completion
therefore occurs no later than either bound. ∎

In particular, equal shares with zero lag give at most twice the standalone
work of the faster solver. The coefficient $\alpha$ is a share of aggregate
work, whereas $\eta$ in Proposition 9 budgets enhancement work relative to
native work; these are different accounting roles.

For serial rescue, run $H$ for at most $b$ fully charged work. If it has not
completed, discard it and start unchanged $A$ with its original input, initial
state, and random tape. Its total work is at most $b+T_A$. Charge the startup of
$H$ inside $b$ and the startup of $A$ inside $T_A$. If the enforced cap permits
an overrun $\delta$, the corresponding bound is $b+\delta+T_A$ instead.

These are work statements under explicit trace and scheduling assumptions.
Shared resource exhaustion, cache or memory contention, uncharged startup,
wall-clock-dependent search, and communication that changes the baseline state
can invalidate the premises. In particular, injecting an incumbent or a row
from $H$ into $A$ does not preserve the unchanged baseline trace automatically.
The empirical study did not deploy this protected scheduling construction, so
its measured policy does not inherit the bound.

## 12. What reward history says about a first action

Suppose two actions each cost one unit. A selector's entire available pre-action
information is identical in two environments. In environment 1, only action 1
reveals a proof in one unit; in environment 2, only action 2 does. Every
deterministic selector makes the same first choice in both and fails to choose
the proof-producing action first in one environment. If a randomized selector
chooses action 1 with probability $p$, its first-action success probabilities
are $p$ and $1-p$, so at least one is at most $1/2$.

This proves the stated information limit. It does not establish an unbounded
competitive ratio, rule out a good second choice, or invalidate learning under
statistical or structural assumptions. Additional model information that
distinguishes the environments lies outside the example's identical-information
premise.

An optional action should therefore report its actual model, node domain,
relaxation, cutoff, cost allowance, and a verified inference, a verified ceiling
in a stated benefit measure, or an unresolved status. Exhausting a budget is
unresolved. Heuristic action rankings can guide probes, but cannot become
feasibility or remaining-benefit certificates. Full-run performance comparisons
must include selection and validation work. These contracts do not themselves
establish a universal selector or a positive net runtime benefit.

## Verification actually performed

I ran two independent targeted `python3` heredocs from
`/workspace/minlp-notes`. Both used only `fractions.Fraction` and passed.
The exact commands are reproduced below. The first checked the original and sharper
graph constants, exact primal/dual values for the two-region coverage boundary
and uncovered strip, the source's observed-decrement trajectories and false
geometric estimate, and the concurrent-admission counterexample. These checks
supplement the uniform proofs above. They do not implement or exhaustively
test a general multidimensional cover checker.
The second checked the recommended graph rate's exact positive rational margin.

No archived numerical experiment, solver benchmark, project-wide verification,
or CI inspection was run. I did not run the source's general check scripts or
attribute their previously reported results to this audit. The file reads and
`rg` inspections were source inspection, not verification runs.

```bash
python3 - <<'PY'
from fractions import Fraction as Q

# The original graph constants and a sharper one-sided repair constant.
a, K, L, mu = Q(1,64), Q(1,4), Q(165,256), Q(63,64)
assert 4*(a+L*K)/mu == Q(181,252) < Q(7,8)**2
assert Q(7,8)+2*K*Q(1,8) == Q(15,16)
L_pair = Q(1,2048)
assert 4*(a+L_pair*K)/mu == Q(43,672) < Q(13,48)**2
# x/16 - 2*x*x = 1/2048 - 2*(x-1/64)^2.
assert Q(1,2048) - 2*Q(1,64)**2 == 0
assert 4*Q(1,64) == Q(1,16)

# Exact primal/dual values for the cover test on two vertical cells.
# D=[-1,1]^2. Cells x<=beta and -x<=beta cover iff beta>=0.
for beta, expected in [(Q(0), Q(0)), (Q(-1,2), Q(1,2))]:
    x, t = Q(0), -beta
    assert t <= x-beta and t <= -x-beta and t <= 1
    dual_value = Q(1,2)*(-beta) + Q(1,2)*(-beta)
    assert dual_value == t == expected

# The source's exact observed-decrement counterexample.
fast = [(Q(0),Q(0)), (Q(1,10),Q(0)), (Q(899,1000),Q(1,10)),
        (Q(9,10),Q(899,1000)), (Q(1),Q(9,10))]
stall = [(Q(0),Q(0)), (Q(899,1000),Q(899,1000)),
         (Q(9,10),Q(899,1000)), (Q(1),Q(9,10))]
def interpolate(knots, x):
    for (l, fl), (u, fu) in zip(knots, knots[1:]):
        if l <= x <= u:
            return fl + (x-l)*(fu-fl)/(u-l)
    raise AssertionError('outside domain')
paths = []
for knots in [fast, stall]:
    assert all(0 <= y <= x for x,y in knots)
    assert all(fl <= fu for (_,fl),(_,fu) in zip(knots,knots[1:]))
    path = [Q(1)]
    for _ in range(4):
        path.append(interpolate(knots,path[-1]))
    paths.append(path)
assert paths[0][:3] == paths[1][:3] == [Q(1),Q(9,10),Q(899,1000)]
assert paths[0][-1] == 0 and paths[1][-1] == Q(899,1000)
r = (paths[0][1]-paths[0][2])/(paths[0][0]-paths[0][1])
assert r == Q(1,100)
assert (paths[0][1]-paths[0][2])/(1-r) == Q(1,990)

# The omitted serial-admission assumption is material in an abstract ledger.
b, eta, delta, E_at_admission, N = map(Q,[1,0,1,0,0])
assert all(E_at_admission < b+eta*N for _ in range(3))
E_after_all = 3*delta
assert E_after_all > b+eta*N+delta
print('PASS exact graph constants, coverage certificates and hole, observed-decrement example, concurrent-admission boundary')
PY
```

```bash
python3 - <<'PY'
from fractions import Fraction as Q
q_squared = 4*(Q(1,64) + Q(1,2048)*Q(1,4))/Q(63,64)
assert q_squared == Q(43,672)
assert Q(13,48)**2 - q_squared == Q(151,16128) > 0
assert Q(13,48) + Q(1,16) == Q(1,3)
print('PASS exact recommended graph-rate comparison: q^2=43/672, positive margin=151/16128, lambda=1/3')
PY
```

No new citation is asserted by this audit. The classical attribution boundaries
in the source remain appropriate. The paper's literature lead should supply
the vetted sources for LP duality and parametric regions, error-bound transfer,
and independent work scheduling; this audit neither claims priority nor uses
unverified literature to enlarge the theorem scope.
