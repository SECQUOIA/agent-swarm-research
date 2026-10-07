# First review of the constraints manuscript section

Date: 2026-10-05. Reviewed the complete `sections/constraints.tex` draft and
`sections/foundations.tex` and `sections/certificates.tex` for shared notation.
I captured the first constraints draft as one 62,909-character snapshot, then
read and checked all changes in the 65,055-character version produced while
the writer remained active. References below use theorem and equation labels
rather than moving line numbers. I changed only this review file.

**Assessment: the main proofs and developed examples are sound. Four local
corrections or explicit qualifications remain before approval of the section.**
The finite cover is complete, its invariance argument is correct, the repair
theorem has sufficient locality assumptions, and the recommended graph rate
$1/3$ is proved with the correct one-sided constant. The graph example also
validly develops a global rate $25/48$ and a constraint-tangent variant.

## Required corrections

### R1. Retain the distinction between a piece derivative and a support gradient

The latest version repairs `eq:basis-value-con`: it now states the exact affine
value on the closed basis region and identifies the gradient of that affine
function. This resolves the incorrect first-draft assertion that
$\nabla h_c=E^T\pi$ exists on the whole closed region.

The explanatory paragraph following `eq:lagrangian-derivative-con` still says
that the formula reduces to "$\nabla h_c=E^T\pi$" for a fixed matrix. Use
"the derivative of the certified affine value is $E^T\pi$" there as well.
At a shared boundary the support need not be differentiable: in
`ex:cutoff-con`, its slopes at $U=1$ are $1$ and $1/4$. A basis can also have
a lower-dimensional validity region, so its relative interior does not in
general give an ambient support gradient. The comparison theorem correctly
uses derivatives of the smooth representing functions and does not depend on
this unsupported gradient assertion.

### R2. An unchanged support does not always mean an unchanged current endpoint

The paragraph beginning "These results sort the directions" currently says
that $U\ge v_0(c_i)$ means direction $i$ cannot improve in the round.
`prop:threshold-con` proves only
$h_{c_i}(U)=h_{c_i}(U_0)$. An endpoint ceiling follows only if the current
endpoint already equals that old support.

For a counterexample, take $B=[0,1]^2$, the fixed row $x\le1/2$, and objective
$\psi(x,y)=y$. At $U_0=1$ the upper support of $x$ is $1/2$, and the least
objective on its optimal face is $v_0=0$. At the lower incumbent cutoff
$U=1/2\ge v_0$, the support is still $1/2$, but the current endpoint $p_x=1$
can still tighten by $1/2$. Both cutoffs are values of feasible incumbents.

Replace the sentence with: "If $U\ge v_0(c_i)$, the new support equals the old
support; when the current endpoint already equals that value, the direction
cannot move." Alternatively, explicitly impose the latter premise in the
three-class discussion. The propositions and their proofs need no change.

### R3. State the affine example's limit for every starting radius

`prop:equality-con` itself handles every regime correctly. Its interpretation
paragraph still calls $a=\sqrt U/2$ the positive-cutoff limit without the
condition $r_0\ge a$, then says that OBBT "reaches" the sublevel hull.

For all $U>0$ and $r_0\ge0$, the limiting radius is
$\min\{r_0,a\}$. The original sublevel hull within the initial box has
that radius as well. If $r_0>a$, the identity in the proposition gives
$r_{k+1}-a>0$ whenever $r_k>a$, so no finite iterate reaches $a$; convergence
is quadratic. If $r_0\le a$, the initial box is fixed. Say that OBBT
"converges to the box hull of the original cutoff set" and retain this
starting-box qualification. The one-round claim after eliminating the equality
is correct.

### R4. Close the zero-gauge case and declare the cutoff in the restricted tangent result

`prop:restricted-tangent-con` should explicitly set $U=f^*+\epsilon$ with
$\epsilon\ge0$. The surrounding setup defines the gauge and equality but
does not make that local cutoff assumption explicit. It is needed both for
retaining $x^*$ and for the displayed square root.

Its proof divides by $t^2$, whereas the statement admits $t=0$ at zero cutoff
slack and the foundations allow degenerate boxes. Add the direct case:
"If $t=0$, then $B=\{x^*\}$ and validity gives
$T_U(B)=\{x^*\}$; otherwise $t>0$." The rest of the proof is correct.

For positive $t$, interior minimality on the affine set gives
$\nabla f(x^*)^T\xi=0$ whenever $C\xi=0$. The uniform restricted expansion
then implies
$Q(d,\xi)\le\epsilon/t^2+\delta/2\le\delta$ for every retained point of
the comparison box $x^*+tD(d)$. Monotonicity transfers its support inclusion to
every actual box with gauge $t$. At gauges below
$\sqrt{2\epsilon/\delta}$, nesting suffices. Induction therefore gives
the stated maximum bound; no uniform expansion over every actual box shape is
being silently assumed. This is a useful complete constrained tangent result
after the two small additions above.

## Results checked and accepted

### Linear supports, signs, and compactness

The latest opening correctly limits the polytope and affine-objective setting
to the LP subsections and returns to the general projected setting for the
affine and nonlinear rate examples. The signed order is consistently
$p=(-\ell,u)$ with lower-direction objectives $-e_i$ and upper-direction
objectives $e_i$. Affine objective constants are included through the cutoff
right-hand side $U-a_0$.

`prop:dual-envelope-con` is valid, including its developed finite dual-vertex
representation. The dual set is a pointed polyhedron in the nonnegative
orthant. For a parameter with a nonempty primal and nonempty dual, weak duality
bounds the primal above and the dual below; LP duality gives finite attained
equal values, and a dual optimum occurs at a vertex. There are finitely many
dual vertices, so their affine minimum is continuous, concave, and piecewise
affine on the feasible parameter polyhedron. No primal compactness is missing
from this argument: feasibility of both sides supplies the required finite
LP value. The polytope setting separately guarantees all projected and lifted
attainment needed by the endpoint map.

The cutoff multiplier has the correct sign. The old multiplier gives a lower
bound on the reduction and a new optimal multiplier gives an upper bound, as
proved by applying weak duality in both directions. The primal--dual bracket
and optimal-face no-change threshold are also correct. Exact old optimality,
fixed rows, and nonemptiness at the new cutoff are retained.

The complete basis-availability proof is correct under its explicit nonempty
polytope premise. A minimal nonnegative representation by active row normals
is independent and extends to a full active basis. The free-lift example
correctly explains why finite selected supports alone do not provide this
format. The latest cutoff example also correctly restricts the claim of a
unique optimal dual to $U\in(1,3)$, avoiding endpoint degeneracy.

### Rebuilt rows and the complete cover

`lem:frozen-con` distinguishes the valid frozen upper envelope from the actual
rebuilt map. After a completed first frozen Jacobi round, the added box rows
are redundant throughout $[p_1,p_0]$, so the frozen support is constant. Its
zero comparison matrix cannot bound the rebuilt operator.

`prop:corrected-dual-con` is an exact weak-duality correction for failed
stationarity after a rebuild. The sign and the interval maximum are correct.
The square example gives $41/64$ for the invalid uncorrected expression,
correction $15/32$, valid total $71/64$, and exact rebuilt support $41/40$.
Repeated use from $u_0=2$ remains in $[1,2]$ and contracts the error with ratio
at most $1/2$. The exact support instead satisfies
$F(u)-1=(u-1)^2/(2u)$ and converges quadratically. For precision, restrict
the displayed corrected polynomial $u-u^2/4+1/4$ to $1\le u\le2$; above
$2$ the residual changes sign and the interval correction uses the lower
bound instead.

`prop:rebuilt-basis-con` correctly differentiates the identity
$A_Iz_I=b_I$ and obtains
$\partial_jv_I=\pi^T(\partial_jb-\partial_jA\,z_I)$. The nonsingularity
set is open and contains the certified region. The latest explanation bounds
each *corner entry* separately, correctly allowing both contributions to add
for a square. This avoids omitting a factor of two in a square endpoint
derivative.

`thm:cover-con` supplies a complete proof across all switching boundaries.
Its finite interval-intersection premise gives a finite segment partition;
closed pieces share endpoint values because each represents the same support.
No separate continuity hypothesis for $F$ is missing. Bounds on the
representing functions' partial derivatives yield the required componentwise
matrix inequality by summing over that partition.

`prop:coverage-con` correctly handles strict violations, shared boundaries,
and lower-dimensional parameter polytopes. Allowing the slack variable to be
negative makes every auxiliary LP feasible, and compactness makes its maximum
attained. The regions cover exactly when every violation tuple has maximum
at most zero. The central-strip example demonstrates why membership of the
outer polytope's vertices in the union is insufficient. Coverage is checked for
every direction, not inferred from a current basis.

`cor:residual-input-con` has the required validity and monotonicity premises
explicitly in the latest draft. The same-cutoff protected box gives
$p_P\le F_U(p)\le p\le p_0$, proving nonemptiness, invariance, and a compact
convex endpoint region. Its extension to changing cutoffs correctly requires a
verified cover of a convex region in $(p,U)$. In the switching example,
$\ell=0$ throughout the region, so using a zero lower-direction derivative
in $\operatorname{diag}(0,1/2)$ is justified.

### Feasible repair and the developed graph rates

`thm:repair-con` and `cor:repair-rate-con` have sufficient local assumptions.
Their estimates are required for every retained relaxed point, not just a
support optimizer. The repair is original feasible, and the objective change
and growth bounds are imposed on it even when it leaves the current box.
The radius $\bar w+\kappa(\beta\bar w^2)^\alpha$ follows from the fact
that the box contains $x^*$, the residual bound, and the repair distance. It
gives a sufficient neighborhood for certifying the estimates. The complete
subbox-family premise keeps the iterates inside that neighborhood.

Requiring the assumptions only on $K_U(B)$ is a valid weakening of the audited
all-point formulation for a fixed cutoff. In the graph example, all displayed
identities and constants hold on the entire graph relaxation, so its rates
remain valid uniformly for every nonnegative cutoff. The zero-slack width
ratio, positive-slack upper floor, and transfer to complete sequential passes
are all correctly scoped.

The graph construction's validity and whole-family monotonicity are proved,
including the bilinear estimator. Its repair stays in the original feasible
set, the secant gap is at most one quarter of the squared $x$ width, and the
bilinear gap is at most one quarter of the product of the two widths. The
one-sided identity

\[
f(x,x^2)-f(x,y)
=\delta\bigl(1/2048-2(x-1/64)^2-\delta\bigr)\le\delta/2048
\quad(\delta=y-x^2\ge0)
\]

gives $L=1/2048$ for every relaxed point. With
$\tau=1/64$, $K=1/4$, and $\mu=63/64$,
$\lambda_0^2=43/672$ and
$(13/48)^2-43/672=151/16128>0$. Thus the rational ratios are $25/48$
on the entire admitted outer-box family, whose widths are at most $1/2$,
and $1/3$ when the width is at most $1/8$. Both are conservative upper
ratios, not exact rates or evidence of a runtime advantage.

The additional variant that uses endpoint tangents for the *constraint*
$x^2\le y$ is also valid. Tangent monotonicity is proved in the latest
draft. For points below the graph, the same identity gives the one-sided
constant $9/64$, the residual still has bound $w^2/4$, and
$\lambda_0^2=13/63<1/4$. The resulting global ratio $3/4$ is correct
while the objective squares remain exact.

The following sentence about also replacing objective squares should describe
a *crude generic error estimate*, rather than imply a necessary lower bound
on every formulation's best constant. Coupling or shared lifts can prevent the
unconstrained quarter-width square error from being attained. A safe formulation
is: "Using the generic quarter-width square-error bound already makes this
sufficient estimate noncontractive; it does not prove failure of the resulting
OBBT operator." This preserves the intended distinction from the tangent-map
analysis.

### History and implementation scope

Both finite-history constructions are valid and monotone under the explicit
projected objectives in the latest draft. Their common prefixes, continuation
formulas, and small-decrement arithmetic are correct. The section expressly
preserves trivial nesting bounds and exact zero-residual fixed-point
certificates. The claims therefore concern extrapolation of positive progress,
as required by the audit.

The last paragraph correctly separates validation of a current inexact dual
from stored-dual reuse across changes. It makes no claim that the additional
experimental policy implements complete covers, protected-box machinery,
residual tails, or repair rates. This is a scope check, not a separate audit of
the experimental implementation.

## Shared-section issue

In the foundations snapshot, the closing inclusion chain says
$H_U\subseteq P\subseteq B_\infty$ for every fixed box $P$ in $B_0$.
The first inclusion is false for an arbitrary protected box. The certificates
section itself gives $f(x)=x$, $B_0=[0,1]$, $U=1$, and protected $P=\{1\}$,
whereas $H_U=[0,1]$. In general $H_U$ and $P$ are each contained in
$B_\infty$. This was sent to the root and the foundations reviewer, who
confirmed it and included it in that review. The constraints invariance proof
does not use the false inclusion and needs no corresponding change.

## Targeted verification actually run

I ran the following independent exact-arithmetic diagnostic from the repository
root. It passed. It checks the developed global and local graph constants,
the constraint-tangent variant, and the rebuilt-dual example. These are narrow
algebra checks supporting the analytic review, not numerical experiments.

```bash
python3 - <<'PY'
from fractions import Fraction as Q
mu, tau, K = Q(63,64), Q(1,64), Q(1,4)
assert 4*(tau+Q(1,2048)*K)/mu == Q(43,672)
assert Q(13,48)**2-Q(43,672) == Q(151,16128) > 0
assert Q(13,48)+Q(1,4) == Q(25,48) < 1
assert Q(13,48)+Q(1,16) == Q(1,3)
assert 4*(tau+Q(9,64)*K)/mu == Q(13,63)
assert Q(1,4)-Q(13,63) == Q(11,252) > 0
assert Q(1,2)+Q(1,4) == Q(3,4)
u = Q(5,4)
old_rhs = (u*u+1)/4
q = 1-u/2
assert old_rhs == Q(41,64) and q == Q(3,8)
assert old_rhs+q*u == Q(71,64)
assert (u*u+1)/(2*u) == Q(41,40) < Q(71,64) < u
print('PASS new global and local graph rates, endpoint-tangent variant, and rebuilt-dual example')
PY
```

The other commands were `cat`, targeted `sed` and `rg` reads, and an in-memory
comparison of the two constraints snapshots. I ran no manuscript build,
project-wide checks, experiment reruns, CI inspection, or independent
literature search. Citation and priority review remain with the literature
lead. No manuscript file was edited.
