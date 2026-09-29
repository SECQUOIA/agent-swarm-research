# Quadratic value separation from the span of the native Hessians

Date: 2026-09-27. Status: proof, primary-source check, and written adversarial
review completed; publication priority remains unestablished.

The number of independent native Hessian matrices can replace the number of
native quadratic inequalities in the repository's polynomial-encoding bound.
The objective Hessian does not enter this count. The value bound requires no
Slater condition. It also gives an exact feasibility algorithm, including
degenerate feasible sets, rather than only a penalty-encoding consequence.

The main proof below uses convexity, rational linear algebra, sparse conic
representations, and the same quantitative elimination theorem already used in
the fixed-constraint-count paper. It avoids relying on a stated but deferred
optimization theorem in the few-quadratic literature.

**Definitions and proposed value theorem.** Let

\[
 \theta=\min\{q_0(x):x\in P,\ q_i(x)\leq0\ (i=1,\ldots,m)\},
 \qquad q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i.
\]

All data are rational; all \(Q_i\), including \(Q_0\), are positive
semidefinite; \(P\) is a rational polyhedron with explicit finite coordinate
bounds; and the feasible set is nonempty. Let \(L\geq2\) be the total explicit
binary input length and

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

The proposed theorem is that \(\theta\) satisfies a nonzero integer polynomial
whose degree and coefficient bit lengths are at most
\(L^{O(h+1)}\). Consequently,

\[
 \theta\ne0\quad\Longrightarrow\quad
 |\theta|\geq 2^{-L^{O(h+1)}}.                 \tag{1}
\]

The constants in these bounds are absolute. No constraint qualification is
assumed. The statement concerns the encoding of a value, not a procedure for
discovering the active constraints used in the proof.

**Step 1: remove inactive constraints without changing the value.** Choose an
optimizer \(x^*\). Keep every original affine equality. Turn all affine
inequalities active at \(x^*\) into equalities, and delete the other affine
inequalities. Retain only the quadratic inequalities active at \(x^*\).

This reduced problem still has optimum \(\theta\). Indeed, if a retained
feasible point \(y\) had \(q_0(y)<q_0(x^*)\), every point sufficiently near
\(x^*\) on the segment toward \(y\) would satisfy the deleted constraints,
by their strict slack at \(x^*\). Convexity makes the retained quadratic
inequalities hold along that segment, and the retained affine equations hold
identically. Convexity of the objective gives a strictly better objective at
every nontrivial point of the segment. This contradicts original optimality.

Let \(I\) denote the retained quadratic indices. Choose
\(B=\{j_1,\ldots,j_s\}\subseteq I\), \(s\leq h\), whose Hessians form a
basis of the retained Hessian span. Rational linear algebra gives rational
vectors \(c_i\in\mathbb Q^s\) such that

\[
 Q_i=\sum_{j\in B}c_{ij}Q_j\qquad(i\in I).
\]

The polynomials

\[
 \ell_i(x)=q_i(x)-\sum_{j\in B}c_{ij}q_j(x)
\]

are affine. They vanish at \(x^*\), since every retained quadratic is active
there. Add the affine equations \(\ell_i(x)=0\) to the reduced problem.
This restriction keeps \(x^*\), so it also keeps the same optimum. This step
does not replace the quadratic inequalities by equalities and does not assert
that the resulting quadratic basis has nonnegative combination coefficients.

Let \(H\) be the affine space defined by all the equations now present.
Choose independent rational equations and eliminate them:

\[
 x=x_0+Vu,\qquad u\in\mathbb R^d.
\]

The free variables \(u\) can be chosen among the original coordinates.
All new rational coefficients have bit length polynomial in \(L\), by
determinant bounds for rational elimination. In particular, this bound does
not require knowing the coordinates of \(x^*\). On this affine space the
restricted quadratics, denoted \(\widetilde q_i\), obey the polynomial
identities

\[
 \widetilde q_i(u)=\sum_{j\in B}c_{ij}\widetilde q_j(u),
 \qquad
 \nabla\widetilde q_i(u)=
       \sum_{j\in B}c_{ij}\nabla\widetilde q_j(u).       \tag{2}
\]

All retained quadratics remain convex. The dimension of their span as whole
polynomials, not just as Hessians, is now at most \(h\). This is the purpose
of the added affine equations.

If \(d=0\), the unique point in \(H\) is rational with polynomial bit
length and the claimed value bound follows directly. Assume henceforth that
\(d>0\). Let an integer \(D\geq1\), with polynomial bit length, bound the
absolute values of the original coordinates. Add

\[
 q_b(u)=\|u\|_2^2-(dD^2+1)\leq0.
\]

This ball is strict at the retained optimizer \(u^*\), contains that point,
and makes the new feasible set compact. Its optimum remains \(\theta\).

**Step 2: regularization and a sparse KKT certificate.** For
\(0<\varepsilon<1\), minimize

\[
 \widetilde q_0(u)+\varepsilon\|u\|_2^2
 \quad\text{subject to}\quad
 \widetilde q_i(u)\leq\varepsilon\ (i\in I),\qquad
 q_b(u)\leq\varepsilon.                              \tag{3}
\]

The point \(u^*\) is strictly feasible, the relaxed ball gives a common
compact bound, and the objective is strictly convex. An optimizer and
nonnegative KKT multipliers therefore exist. The optimal values
\(\theta(\varepsilon)\) converge to \(\theta\): using \(u^*\) gives the
upper limit, while bounded subsequences of minimizers give the lower limit
by continuity.

Let \(\lambda_i\) be the native multipliers in any KKT certificate at the
optimizer of (3), and keep the ball multiplier separate. Only rows with
\(\widetilde q_i(u)=\varepsilon\) can have a positive multiplier. By (2),
their total contribution to stationarity depends only on

\[
 \eta=\sum_{i\in I}\lambda_i c_i\in\mathbb R^s.
\]

Every vector in a finitely generated cone in \(\mathbb R^s\) is a
nonnegative combination of at most \(s\) of its generators. Apply this
fact using only the currently active rows. It gives new nonnegative native
multipliers, supported on at most \(s\leq h\) active constraints, with
the same \(\eta\). Equation (2) preserves stationarity. Each selected row
is active, so complementarity is also preserved. Retaining the ball
multiplier gives a KKT certificate with at most \(h+1\) nonzero
multipliers in total.

For completeness, the conic fact follows by taking a representation with
minimal support. If its positive-weight generators are linearly dependent,
choose a nonzero dependence, reverse its sign so some coefficient is
positive, and subtract the largest multiple that preserves all weights'
nonnegativity. At least one weight becomes zero, contradicting minimality.
This argument also covers \(\eta=0\), for which an empty representation
suffices.

The sparsification uses linear dependence of the coefficient vectors
\(c_i\), rather than linear dependence of numerical gradients at one
optimizer. The resulting bound is therefore \(h\), even when the primal
dimension is much larger.

**Step 3: eliminate the primal variables using the sparse support.** There
are finitely many possible supports. Take any sequence
\(\varepsilon_\nu\downarrow0\), choose sparse KKT certificates, and pass
to a subsequence with one fixed native support \(J\), \(|J|\leq h\).
Always allow one ball multiplier, possibly zero. Write
\(k'=|J|+1\leq h+1\).

For this fixed support, stationarity has the form

\[
 M u=-a_0-\sum_{i\in J\cup\{b\}}\lambda_i a_i,
 \qquad
 M=Q_0+2\varepsilon I+
       \sum_{i\in J\cup\{b\}}\lambda_iQ_i\succ0,       \tag{4}
\]

where all quantities now refer to the restricted quadratics in \(u\).
Set

\[
 \Delta=\det M,\qquad
 p=-\operatorname{adj}(M)
       \left(a_0+\sum_{i\in J\cup\{b\}}\lambda_i a_i\right).
\]

Then \(u=p/\Delta\). For every retained constraint, including those
outside \(J\), define

\[
 G_i=\tfrac12p^TQ_ip+\Delta a_i^Tp+
                  (c_i^{\rm const}-\varepsilon)\Delta^2.
\]

Here \(c_i^{\rm const}\) denotes the constant coefficient of the
restricted quadratic; it is distinct from the coefficient vector \(c_i\)
in (2). Also define

\[
 G_0=\tfrac12p^TQ_0p+\Delta a_0^Tp+
                     (c_0^{\rm const}-w)\Delta^2+
                     \varepsilon p^Tp.
\]

Let \(\mathcal K_J(\varepsilon,w,\lambda)\) be the polynomial conditions

\[
 \Delta>0,\quad \lambda_i\geq0,\quad
 G_i\leq0\ (i\in I\cup\{b\}),\quad
 \lambda_iG_i=0\ (i\in J\cup\{b\}),\quad G_0=0.       \tag{5}
\]

All constraints, not merely the supported ones, occur in the feasibility
part of (5). For \(0<\varepsilon<1\), every solution of (5) reconstructs a valid KKT point for the
convex problem (3), and hence has \(w=\theta(\varepsilon)\). Conversely,
the selected subsequence of sparse KKT certificates satisfies (5).
Existence for every sufficiently small \(\varepsilon\) is unnecessary.

The polynomial degrees in (5) are \(O(d+1)\), and coefficient bit lengths
are polynomial in \(L\). A determinant coefficient sums at most
\(d!(k'+2)^d\) products of input coefficients; this bounds its bit length
without assuming a small number of expanded monomials. The same estimate
applies to the adjugate and the \(G_i\). To clear denominators, first take
one common positive denominator \(D_0\) for the polynomially many restricted
input coefficients. It has polynomial bit length. Denominators of the
determinant, adjugate, and \(G_i\) coefficients divide
\(2D_0^{O(d+1)}\), so a common positive clearing factor still has
polynomial bit length, regardless of the number of expanded monomials.
The number of constraint polynomials is polynomial in \(L\).

The scalar formula

\[
 \forall\gamma\;\left[\gamma\leq0\ \lor\
   \exists\varepsilon,w,\lambda\;
    \bigl(0<\varepsilon<1,\ \varepsilon<\gamma,
       -\gamma<w-a<\gamma,
       \mathcal K_J(\varepsilon,w,\lambda)\bigr)\right]      \tag{6}
\]

defines exactly \(\{\theta\}\). The fixed-support subsequence gives
witnesses when \(a=\theta\). Conversely, witnesses with
\(\gamma\downarrow0\) have \(w=\theta(\varepsilon)\to\theta\), hence
\(a=\theta\).

There are two quantifier blocks, of sizes \(1\) and at most \(h+3\),
and one free variable. Effective block quantifier elimination gives
degrees and coefficient bit lengths \(L^{O(h+1)}\). The precise tool is
Basu--Pollack--Roy, *Algorithms in Real Algebraic Geometry*, Theorem 14.16,
also stated in [Basu's survey, Theorem 2.27](https://arxiv.org/abs/1409.1534).
This is the coefficient-height conclusion, not merely the operation
count. The repository's existing fixed-count proof uses the same theorem
with the same constant number of quantifier blocks.

Remove identically zero polynomials from the resulting formula. Some
remaining polynomial must vanish at \(\theta\), because otherwise all
polynomial signs would be constant in a neighborhood of \(\theta\),
contradicting the singleton defined by (6). This proves the degree and
height statement. For \(\theta\ne0\), remove powers of the indeterminate
and apply a Cauchy bound to the reciprocal polynomial to obtain (1).

**An objective-independent error bound and penalty consequence.** Consider
the boxed mixed-integer model with convex quadratic continuous slices,
affine linking residual \(r(x,z)\), a nonempty global equality-feasible set
\(F\), and refined Slater on every equality-feasible integer slice.
Suppose the native continuous Hessians span a space of dimension at most
\(h\), uniformly over integer assignments. There is a global constant
\(C\geq1\) such that

\[
 \operatorname{dist}_2((x,z),F)\leq C\|r(x,z)\|_\infty
 \quad((x,z)\in X),\qquad
 \log_2 C\leq N^{O(h+1)}.                              \tag{7}
\]

To obtain this statement, apply (1) to the positive minimum residual on
every equality-infeasible slice and to the positive common nonlinear
Slater margin on every equality-feasible slice. Both auxiliary problems
have linear objectives and the same native Hessian span: the residual,
margin, and bound rows are affine. Thus their positive values
\(\delta_z\) and \(\sigma_z\) have reciprocals at most
\(2^{N^{O(h+1)}}\).

The objective-independent repair proof in
[the penalty frontier note, Section 4](penalty-frontier.md#4-a-global-error-bound-and-arbitrary-quadratic-objectives)
then applies without change. On a feasible slice, first repair the
affine equality with a rational Hoffman bound \(H\), then mix the
repaired point with a common-slack point. This gives
\(H(1+GD/\sigma_z)\|r\|_\infty\), where \(G\) bounds native gradients
and \(D\) the continuous box diameter. On an equality-infeasible slice,
use the full box diameter divided by \(\delta_z\). All these auxiliary
constants have polynomial-bit bounds apart from the margins already
controlled above. Their maximum proves (7).

For every objective with Lipschitz constant \(L_f\) on the full input
box, any \(\rho>L_fC\) gives zero-multiplier minimizer-set exactness.
In particular, for an arbitrary rational quadratic objective, including
an indefinite one of unrestricted rank, a sufficient integer penalty
has bit length \(N^{O(h+1)}\). The one-norm conclusion follows from
\(\|r\|_1\geq\|r\|_\infty\). The objective Hessian is excluded from
\(h\). Refined Slater is needed for (7) and this penalty consequence,
though not for the value theorem or the exact feasibility decision below.
No claim about efficient calibration of the smallest penalty follows.

If the aggregate native Hessian rank \(r\) is also available, the
independent rank argument gives the better of the two bounds:

\[
 \log_2 C\leq
 \min\{N^{O(h+1)},\;N^{O(1)}2^{O(r)}\},
\]

where each displayed bound has its own absolute constants. This is a
choice between two proved estimates, not a claim that the parameters
interchange in either proof.

**Exact feasibility consequence.** There is a direct route from (1) to an
\(N^{O(h+1)}\)-bit-time exact feasibility decision, hence polynomial time
for fixed \(h\), with no Slater assumption. The full proof and the
finite-precision source check are in
[the exact-feasibility note](hessian-span-exact-feasibility.md).

Put all inequality violations and both signs of every affine equality
into the convex function

\[
 v(x)=\max\{0,q_1(x),\ldots,q_m(x),
                  \text{affine inequality/equality violations}\}
\]

on the explicit rational input box. Let \(\alpha=\min v\). Compactness
implies \(\alpha=0\) exactly when the original system is feasible.
The epigraph formulation of this minimization has a linear objective and
the same native Hessian span \(h\). A rational upper bound on \(v\)
supplies a finite epigraph-variable box. The value theorem gives an
explicit asymptotic bound

\[
 \alpha=0\quad\text{or}\quad
 \alpha\geq\delta:=2^{-N^{C(h+1)}}
\]

for a sufficiently large universal constant \(C\).

After eliminating fixed coordinates and rescaling the box, \(v\) is an
explicit rationally evaluable Lipschitz convex function on a full-dimensional
cube. The relaxed sublevel set \(K_\delta=\{x:v(x)\leq\delta/2\}\) is
empty if the original system is infeasible. If the original system is
feasible, interpolate one of its points a little toward the cube's center.
Convexity and a rational Lipschitz bound then put a ball of explicitly
bounded radius inside \(K_\delta\). Its center need not be known.

An exact rational separator comes from a violated quadratic's gradient or
a violated box bound. The finite-precision central-cut method of
Grötschel--Lovász--Schrijver, Theorem 3.2.1, distinguishes the empty case
from the promised ball by its volume bound, using polynomial time in the
input and \(\log(1/\delta)\). The linked note verifies that the theorem's
membership branch, when supplied our exact oracle, accepts an actual
member of \(K_\delta\). No approximate-feasibility assertion about the
original system is substituted for exact decision.

The decision proof itself does not construct an exactly feasible point or
provide its representation. It instead certifies the zero-value case using
the separation theorem. The later
[algebraic witness theorem](algebraic-witness-recovery.md) supplies exact
coordinate descriptions by a separate recovery argument, without requiring
an input box. The broad statement for an unrestricted number of
independent quadratic forms is not established here.

For rational quadratic mixed-integer input of total degree at most two,
a fixed uniform span bound across bounded integer assignments lets the
same decision procedure verify a proposed integer assignment in polynomial
time. Consequently this boxed mixed-integer feasibility problem belongs
to NP. More general input representations need an explicit guarantee that
fixing a polynomial-bit integer assignment produces a polynomial-size
convex-quadratic instance. A continuous-convex quadratic objective-threshold
constraint increases the continuous Hessian span by at most one. These
claims concern exact decision and verification, not polynomial-time
mixed-integer optimization with an unrestricted integer dimension.

This distinction is necessary even with three independent Hessians. Let
\(t=\sqrt[3]{2}\) and consider, on \([0,2]^2\),

\[
 q_1=x^2-y,\qquad q_2=y^2-2x,\qquad
 q_3=(x-y)^2-y-2x+4.
\]

All three polynomials have integer coefficients and PSD rank-one Hessians.
Their common nonpositive set is the singleton \(\{(t,t^2)\}\). To prove
this, all three vanish at that point. The positive combination

\[
 p=(t^2-t/2)q_1+(1-t/2)q_2+(t/2)q_3
\]

has value and gradient zero there, and Hessian
\(\left[\begin{smallmatrix}2t^2&-t\\-t&2\end{smallmatrix}\right]\),
whose determinant is \(3t^2>0\). Thus \(p\geq0\), with equality only
at \((t,t^2)\). Every common feasible point has \(p\leq0\), proving the
claim. Since \(1<t<2\), all three weights are positive. In particular,
this feasible rational convex-quadratic system has no rational feasible
point. Its irrational certificate above is a mathematical proof, not the
output format assumed by the proposed decision algorithm.

**Why this parameter adds a class.** The span dimension can stay constant
while both the number of constraints and the aggregate Hessian rank grow.
For \(n=2r\), take arbitrarily many distinct rational \(t_i\) and

\[
 Q_r(t)=\begin{pmatrix}I_r&tI_r\\tI_r&t^2I_r\end{pmatrix}.
\]

Every \(Q_r(t_i)\) is PSD of rank \(r\), while the
Hessian span has dimension three when at least three \(t_i\) are distinct.
The sum of any two distinct matrices is positive definite, so the aggregate
Hessian rank is \(2r\). Affine terms can vary independently.

More strongly, any common family of nonzero PSD matrices that generates
these \(m\) matrices by nonnegative combinations must contain at least
\(m\) members, even if the generators lie outside their span. Indeed, a
positive PSD summand of \(Q_r(t_i)\) must have range contained in
\(\{(u,t_i u):u\in\mathbb R^r\}\). These ranges have zero intersection
for distinct parameters. Thus no nonzero generator can serve two inputs.
The [independent package assessment](hessian-package-assessment.md) gives
the full kernel argument and exact symbolic checks. This rules out a
bounded common-PSD-generator epigraph reduction for this family, not every
possible nonlinear extended formulation.

An earlier diagonal moment-curve example separated span from rank and
input-cone extreme-ray count, but had three external PSD generators. The
replacement above establishes the stronger distinction needed here.

For span dimension at most two, a simpler epigraph reformulation is
available: the finitely generated pointed cone of nonzero PSD Hessians in
a two-dimensional space has at most two extreme rays. Representatives
can be chosen from the input matrices, and rational conic coefficients
give at most two quadratic epigraph inequalities. The proof above extends
beyond that simple case.

**Prior work examined and an alternate route.**

- [Grigoriev--Pasechnik, *Polynomial-time computing over quadratic maps I*](https://logic.pdmi.ras.ru/~grigorev/pub/quadric_cc.pdf),
  Theorem 1.2, gives sampling degree and coefficient-height bounds.
  Theorem 1.5 states the corresponding exact-optimization bound but defers
  its proof to a continuation. The main proof above does not require that
  deferred proof.
- [Kamminga--Rudolph, arXiv:2411.03096v2](https://arxiv.org/pdf/2411.03096v2),
  Sections 6.2--6.3, gives reduced-variable formulas for quadratic maps;
  Section 8.5 treats bounded QCQP with few total constraints. These are
  substantial few-quadratic precedents, rather than sources of the active
  affine reduction proved here.
- An alternate proof would turn all active quadratics into equalities,
  eliminate their Hessian dependencies as affine equations, add a sphere
  slack, and use those reduced-variable formulas for the attained objective
  values. This route was examined before the sparse KKT proof was found.
  In the inspected Kamminga--Rudolph rank argument, deleting one row from
  a matrix guaranteed to have rank at least \(d-k+1\) guarantees only
  \(d-k\). The safe count is therefore at most \(k\) free primal
  coordinates. Grigoriev--Pasechnik's original variable-reduction discussion
  and Lemma 5.2 support this corrected count. The correction preserves
  the \(O(k)\)-variable bound, but a citation must not reproduce the
  stronger row-deleted rank claim.

The alternate argument and its independent source review are recorded in
[the few-quadratic value-bound evidence note](few-quadratic-value-bound-evidence.md).

The contribution proposed here is the native-Hessian-span value bound,
its resulting error bound and penalty encoding, and the exact-feasibility
consequence. It is not a new few-quadratic sampling
algorithm or a new quantifier-elimination theorem. Searches for Hessian
span, linearly dependent quadratic Hessians, and independent quadratic
forms did not identify an equivalent stated encoding theorem. That search
is limited and does not establish novelty.

[The separate prior-work audit](hessian-span-prior.md) compares the stronger
nearby results in detail: Nie--Ranestad's algebraic-degree formulas,
Grigoriev--Pasechnik and Kamminga--Rudolph's few-quadratic algorithms,
Del Pia's exact one-quadratic mixed-integer result, and the relevant
convex-oracle literature. In particular, a polynomial degree statement
for a fixed number of quadratic constraints is established prior work;
the proposed addition concerns the native matrix-span parameter, coefficient
heights, degeneracies, and the stated decision consequences.

[The depth-limitations note](penalty-depth-limitations.md) records the
discarded structural alternatives. Ignoring affine dependency edges hides
arbitrarily long squaring chains. Even independent quadratic caps with a
general affine residual encounter square-root-sum separation. A restricted
monotone forward system has a simple denominator bound exponential in its
nonlinear depth, but that result does not cover general linking residuals.

**Verification and remaining work.** The
[written adversarial review](hessian-span-review.md) checks the full value
proof and the exact-feasibility implication. The reviewer supplied the
sparse KKT support argument, after independently examining the proposed
active-affine reduction; that part of the process was collaborative rather
than a wholly independent post hoc review. Other researchers separately
rechecked the resulting proof, source-height application, and finite-precision
algorithm. The record distinguishes these roles rather than treating a
positive review as a proof of correctness.
No Lean proof, solver experiment, or repository-wide checks have been run
for this note. Source inspection does not verify every theorem on which
the proof relies.

A targeted Python/SymPy calculation was run with an inline script. It reduced
the three constraint values and the two components of \(\nabla p\) at
\((t,t^2)\) modulo \(t^3-2\), obtaining five exact zeros; it also verified
the displayed Hessian and determinant \(3t^2\). This independently checks
the algebra of the irrational-singleton example. The inequalities
\(1<t<2\), positivity of the weights, and the argument that the common
sublevel set is a singleton are proved above rather than inferred from
numeric output. No project-wide or CI checks were run.

The targeted command
`python research-20260927/check_hessian_span_review.py` was also run and
passed all three exact checks: the irrational singleton, the many-exposed-ray
example, and an aggregate-polynomial identity after compressing seven active
multiplier weights to three. A separate inline Python check found no
trailing whitespace and confirmed a final newline in this note. These
checks do not verify the general value theorem or the ellipsoid algorithm.

The remaining work includes a wider novelty comparison and assessment of
the most consequential extensions. The coefficient-height application and the
finite-precision ellipsoid source have received separate checks. Potential practical
value comes from certifying precision thresholds and recognizing families
with many constraints but few independent curvature matrices. No usable
numerical penalty formula or observed solver speedup is claimed.
