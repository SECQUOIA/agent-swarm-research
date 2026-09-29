# Review of quadratic-fractional optimizer recovery

Date: 2026-09-28. Status: the algorithmic composition passes,
conditional on its canonical joint-field and height bound and on the matching
quadratic-fractional value theorem. This review covers one rational PSD
quadratic numerator divided by one rational affine denominator that is
strictly positive throughout the original closed feasible set.
The final read of
[the saved optimizer manuscript](common-range-quadratic-fractional-witness.md)
found no unresolved algorithmic gap.

The review reconstructs the algorithm from
[the arbitrary-rank PSD optimization proof](common-range-optimization.md),
[the quadratic-programming charts](common-range-optimizer-witness.md),
[the affine-fractional output proof](common-range-fractional-witness.md),
and [common-field recognition](constructive-common-field-recovery.md).
It does not independently reprove the general mixed-integer value bound or
the arithmetic bound for the selected canonical point. The numerator's
Hessian is excluded from the native common-range parameter throughout.

## 1. Fix the continuous convex problem before selecting its gradient

After fixing any integer assignment, write the continuous numerator as

\[
 q(x)=\tfrac12x^TQx+a^Tx+c,\qquad Q\succeq0.
\]

Here \(a,c\) include the effects of the substituted integer coordinates.
Their bit lengths include those of the chosen assignment. A PSD Hessian in
all original mixed variables guarantees this continuous PSD property and
supports the separate mixed-integer threshold theorem.

Retain the denominator direction by intersecting the native common kernel
with \(\ker d_x^T\). With a rational split
\(x=T_1u+T_0v\), this gives

\[
 \dim u=r\le\rho+1,
 \qquad Cv\le b(u),
 \qquad d(x)=d_0(u),
\]

where \(C\) is rational and constant and \(b\) is quadratic. For
unbounded integer variables the split uses the cross-aware native kernel
before substitution, so the eliminated-variable matrix is constant
uniformly in the integer assignment. Squared SOC residuals retain their
affine sign rows, and actual native convex representations are used in
oracle calls.

Let \(\theta\) be a finite attained ratio minimum in this continuous
fiber, and put \(h=q-\theta d\). Positivity of \(d\) implies
\(h\ge0\) on the feasible set. The optimal set is

\[
 O=F\cap\{h\le0\}=F\cap\{h=0\}.
\]

It is closed and convex: \(h\) is convex even when \(\theta<0\).
For \(x,y\in O\), convexity of \(F\) and the exact midpoint identity
give

\[
 0\le h((x+y)/2)
   =-\tfrac18(x-y)^TQ(x-y).
\]

Positive semidefiniteness therefore gives \(Q(x-y)=0\). Thus the
**raw numerator gradient** \(g=Qx+a\) is constant throughout \(O\).
No claim about a constant gradient across different integer assignments
is justified. For example, \(z\in\{0,1\}\),
\(q(z)=(z-\tfrac12)^2\), and \(d=1\) have two optimal assignments
with different raw gradients.

## 2. The canonical point and its box must be fixed first

For each fixed \(u\) with an optimal-level point, the denominator is a
positive constant. The minimum of \(q(u,\cdot)\) on its polyhedral
native fiber is therefore finite, attained, and equal to
\(\theta d_0(u)\). The chart lemma represents its minimum-norm
optimizer by a rational polynomial map \(v_I(u)\) of degree at most
two. Write \(\phi_I(u)=q(u,v_I(u))\), which has degree at most four.

Consequently the projection of \(O\) is exactly

\[
 U^*=\bigcup_I
   \{u:Cv_I(u)\le b(u),\ \phi_I(u)=\theta d_0(u)\}.
\]

This finite union of closed sets proves closedness; convex projections
are not closed in general. Since \(U^*\) is also nonempty and convex,
it has a unique minimum-norm point \(u_*\). Select the minimum-norm
optimal fiber point \(v_*\) over it. It is the same QP-chart point
just described. In particular, after rational integer substitution,
\(v_*\) and the common gradient belong to \(\mathbb Q(u_*)\).

The separate field argument must supply effective common-field degree and
coordinate-height bounds for \((\theta,g,u_*,v_*)\), with an absolute
input exponent. Their exact numerical form is an input to this review.
A Cauchy root bound then prints a full transformed rational box
\([-B,B]^{\dim u+\dim v}\) containing this particular pair.

A box containing an unspecified optimizer suffices for gradient recovery
but does not suffice for recovering this canonical \(u_*\). Nor does
the chart argument above assert a canonical bound for arbitrary nonoptimal
quadratic sublevels. The finite optimal level is essential to its present
use of QP minimizers.

## 3. Rational value comparisons give an exact optimal-set oracle

Every query domain intersects the original rational native feasible set
with the entire box above and with additional rational affine or
\(u\)-norm cuts. It is compact. If nonempty, \(d\) stays strictly
positive, so \(q/d\) is continuous and attains a minimum \(\beta\).
Hence

\[
 \beta=\theta
 \quad\Longleftrightarrow\quad
 \text{the query domain meets }O.
\]

An empty domain returns false. There is no need to compute a positive
lower bound on \(d\). Exact comparisons of the individual algebraic
query values with \(\theta\) suffice; fields of different query values
are not accumulated.

Compactness cannot be omitted. For \(w\ge0\), \(y\ge1\), the
quadratic ratio \(w^2/y\) has attained minimum zero. The added rational
cut \(w\ge1\) leaves an unattained infimum zero. Thus an unboxed
value-equality test would incorrectly report an optimal-level point.
In the full box of radius \(B\ge1\), that cut has minimum
\(1/B>0\), and the proposed test correctly rejects it.

The rational threshold oracle keeps \(q-t d\le0\) as its one
arbitrary-rank PSD quadratic row. Norm cuts are native constraints:

\[
 \|u\|^2\le s
 \quad\Longleftrightarrow\quad
 \|(2u,s-1)\|\le s+1,\qquad s\ge0.
\]

If \(u=Lx\), their Hessians annihilate the refined kernel
\(\ker L\). Affine cuts and box rows add no curvature. Thus all
queries have native common range at most \(r\), while the objective
Hessian stays excluded. Neither \(\theta\) nor an approximate gradient
is inserted as a coefficient in a fractional-value call.

## 4. Approximation recovers one fixed tuple

Each component of \(Qx+a\) is a rational affine function. Because it
is constant on \(O\), rational scalar bisection using the compact
optimal-set oracle approximates its common value. A cut of the form
\((Qx+a)_i\le t\) meets \(O\) exactly when \(g_i\le t\).
The ambient number of gradient coordinates contributes only polynomial
overhead. A rational bound for them follows from \(B,Q,a,T_1,T_0\).

For \(u_*\), bisect the minimum squared norm on the boxed optimal
projection. The box contains \((u_*,v_*)\), so this selection agrees
with the original one. Given coordinate accuracy \(\eta\), choose a
rational feasible norm threshold within \(\eta^2/16\) of the minimum.
The convex projection inequality gives

\[
 \|y-u_*\|^2\le\|y\|^2-\|u_*\|^2\le\eta^2/16
\]

for every projected optimal point in that norm slice. Coordinate
bisections preserve a nonempty optimal slice and yield the requested
approximation. Each new precision request restarts from the original
full box. Otherwise a previous coordinate cut might have excluded
\(u_*\), despite preserving a nearby point.

Approximate \(\theta\) by refining its supplied isolator. These
procedures approximate one specified tuple \((\theta,g,u_*)\), as
required by common-field recognition; they do not pick unrelated points
at different precisions.

## 5. The optimal fiber has rational row normals

Put \(b_g=g-a\). Fix a rational linear map \(R\) satisfying
\(QRb=b\) for every \(b\in\operatorname{range}Q\), obtained by
rational elimination, and set \(x_0=Rb_g\). Complete the native fiber
at \(u_*\) with

\[
 Qx=b_g,\qquad
 a^Tx=\theta d_0(u_*)-c-\tfrac12x_0^TQx_0.
\]

The first equality gives \(x-x_0\in\ker Q\), so it fixes the
quadratic part at \(x_0^TQx_0\). The second fixes the remaining
linear part exactly. Together they are equivalent to optimality within
the native fiber. Gradient equations alone would omit that linear part.

After substituting \(x=T_1u_*+T_0v\), all coefficient matrices on
\(v\) are rational and constant. Their right-hand sides are rational
polynomials of total degree at most two in \((\theta,g,u_*)\).
Using \(g\) itself as a row normal, or leaving a denominator direction
among the \(v\) variables, would lose this rational-matrix property.

Represent each equality by two inequalities. Approximate all right-hand
sides outward, so the relaxed rational polyhedron contains the exact
optimal fiber. The unique minimum-norm solution of the relaxed rational
QP has norm at most \(\|v_*\|\). A rational-matrix Hoffman bound
then gives, for right-hand-side error at most \(2\delta\),

\[
 \|v_\delta-v_*\|
 \le\zeta+\sqrt{2V\zeta+\zeta^2},
 \qquad \zeta=2H_C\delta,\quad V\ge\|v_*\|.
\]

This is the argument proved in
[the feasible-witness note](common-range-witness-recovery.md#5-recover-the-affine-fiber-through-rational-quadratic-programs).
Both signs of every equality are rounded outward independently. Singular
\(Q\), dependent or zero row normals, \(Q=0\), and zero-dimensional
coordinate blocks cause no new issue. Polynomial evaluation uses no
division by the denominator and needs only polynomial additional
precision in the available magnitude and height bounds.

Joint recognition of \((\theta,g,u_*,v_*)\) produces one field
representation. The exact final check substitutes the recovered point
into the original native inequalities, cone signs, affine rows,
\(d>0\), and \(q=\theta d\). The independently known global
value makes the final equality a valid optimality check.

## 6. Uniform boxing decides attainment and recovers integers

Suppose the value theorem supplies an effective bound \(M\) on the
bit length of some attaining integer assignment, conditional on
attainment. Every assignment in that integer box has rational substituted
continuous data of length polynomial in \(N+M\).

In any such fiber containing a \(\theta\)-level point, the global
mixed-integer lower bound \(\theta\) is also a lower bound on the
whole continuous fiber. Thus the level is optimal there, and the
canonical encoding argument applies. A uniform height bound prints one
continuous box containing the canonical point of every such nonempty
level. It need not contain every optimizer.

Intersecting both boxes with the mixed-integer domain gives finitely
many closed bounded continuous fibers. The result is compact, and its
ratio minimum is attained whenever it is nonempty. The original finite
infimum is attained if and only if this boxed domain is nonempty and its
value equals \(\theta\). Necessity uses the conditional integer-size
bound and the uniform continuous box; sufficiency uses compactness.

Integer interval bisection can then retain a half precisely when its
boxed value is \(\theta\). Each retained domain contains an actual
optimizer. After fixing all integer coordinates, apply the continuous
construction above. Its canonical point is still covered by the same
uniform box. The conditional integer-size bound alone would not establish
this recovery algorithm.

All printed box, cut, precision, substitution, and field lengths must
have bounds of the form \(f(k,\rho)N^C\), with absolute \(C\).
The number of oracle calls is polynomial in these lengths. Substituting
them into an oracle of cost \(f(k,\rho)L^c\), with absolute \(c\),
preserves FPT time. An oracle whose input exponent depends on \(k\) or
\(\rho\) would not supply this conclusion.

The manuscript's explicitly positive-domain extension uses the
[reviewed reciprocal cone lift](common-range-positive-domain-review.md).
The added cone has squared residual \(4-4ds\), forces \(d,s>0\),
and projects exactly onto the stated positive domain. The numerator is
unchanged and its Hessian gains a zero row and column. Thus its PSD
property and exclusion from the native range parameter are preserved.
The native cross-aware codimension grows by at most two. Full compact
query boxes include \(s\); the original open domain inside a box alone
would not justify a value-equality test. Projection of the exact lifted
optimizer preserves its original objective value and attainment.

## 7. Targeted verification and limits

One inline `python -` command with exact SymPy arithmetic checked
objective ranks \(1,2,7,12\), gradient constancy on a positive-dimensional
optimal set, the necessity of the scalar face equality, a singular
cross-coordinate Hessian and its rational range inverse, denominator-kernel
and norm-Hessian preservation, the quadratic-ratio unattained-cut example,
and the mixed-integer gradient counterexample. All assertions passed.
The rank examples use \(u\ge\sqrt2\), \(1\le w\le2\),
\(s\ge0\), \(t\ge1\), \(v_i\ge u\), and objective
\((\sum_i v_i^2+u+s)/w\). Their optimal value is
\(m+\sqrt2/2\), the numerator has rank \(m\), and the coordinate
\(t\) leaves a nontrivial optimal face.

A separately staffed narrow review checked the midpoint identity,
rational-normal face, compact affine-cut oracle, and fixed-integer
qualification. It found no gap and passed its own exact symbolic checks.
These finite examples do not establish the general field, value, or
complexity bounds. No project-wide checks, CI inspection, new primary-source
audit, or Lean formalization is claimed.

A final read checked every section of the saved optimizer manuscript,
including its uniform integer boxes, supplied-integer-box variant, and
positive-domain extension. One minor clarification was sent to the author:
an original-coordinate gradient bound computed from a transformed box
also uses the rational coordinate map. A scoped inline `python -` document
check passed final-newline, trailing-space, control-character,
paired-math-delimiter, and local-link checks for this review.
