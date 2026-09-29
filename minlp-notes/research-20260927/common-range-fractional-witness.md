# Exact fractional optimizers from the common Hessian range

Date: 2026-09-28. Status: proof and fresh adversarial reviews completed;
no unresolved gap was found in the stated composition. This note supplies
the output step for
[the common-range affine-fractional value theorem](common-range-fractional-frontier.md).
It does not claim a new
algebraic recognition method.

One extra retained direction removes the apparent algebraic-coefficient
obstacle in recovering an optimal fractional solution. Retain the
denominator's linear direction together with the nonlinear coordinates.
The optimal-level equation then has rational coefficients on all remaining
variables. Its algebraic value occurs only on the right-hand side.

## 1. Statement and exact dependencies

Let \(F\subseteq\mathbb R^n\) be a rational closed convex feasible set
given by native PSD quadratic inequalities or affine second-order cone
inequalities, together with affine rows. For each cone, retain both its
squared residual and its affine right-hand-side sign. Let \(H_i\) denote
the Hessians of the native quadratic rows or squared cone residuals, and
write

\[
 K_0=\bigcap_i\ker H_i,\qquad r_0=n-\dim K_0.
\]

Let \(p,d\) be rational affine functions, with
\(d(x)>0\) for every \(x\in F\). Suppose

\[
       \theta=\min_{x\in F}\frac{p(x)}{d(x)}                 \tag{1}
\]

is finite and attained. The exact value \(\theta\) is supplied by its
primitive irreducible integer polynomial and a rational nonroot isolator.
Write \(D=[\mathbb Q(\theta):\mathbb Q]\), and let \(H\ge1\) bound
the coefficient and isolator bit lengths. Let \(N\ge2\) be the explicit
rational problem length.

The height and degree result below does not require (1): it applies to
every nonempty level \(F\cap\{p-\theta d=0\}\), and also to any
nonempty sublevel \(F\cap\{p-\theta d\le0\}\). More generally, it
applies to the simultaneous weak thresholds of Section 8. Use one
inequality for a threshold and two for an equality. Optimality is needed
for the recovery reduction using value comparisons.

**Encoding statement.** After a rational change of continuous coordinates
specified below, the level has a canonical point \((u_*,v_*)\), obtained
by minimizing \(\|u\|^2\) first and then \(\|v\|^2\) in that fiber.
For \(r\le r_0+1\),

\[
 [\mathbb Q(\theta,u_*,v_*):\mathbb Q]\le D\,3^{2r}.           \tag{2}
\]

Its coordinate minimal polynomials and a common rational univariate
representation, including \(\theta\), have total bit length at most

\[
                    f(r,D)(N+H)^C,                         \tag{3}
\]

where \(C\) is an absolute constant. A computable rational box containing
this particular canonical point has the same bit bound.

**Recovery statement.** Suppose exact fractional values on rational native
subdomains with common range at most \(r\) are computable in
\(g(r)M^c\) time, with an absolute input exponent \(c\). Then the
canonical point can be recovered exactly in
\(f(r,D)(N+H)^C\) time. The procedure uses only rational problem data
in its optimization calls; \(\theta\) enters exact comparisons and the
right-hand-side approximation used for a rational quadratic program.

This is an FPT interface, including its dependence on newly printed
precision and box coefficients. Substituting bounds
\(D\le f(k,\rho)\) and \(H\le f(k,\rho)N^C\) therefore preserves an
absolute input exponent. A fixed-parameter continuous value oracle is the
\(k=0\) case of the common-range fractional value result. This note does
not derive that value result from a decision oracle.

## 2. Retain the denominator direction

Write \(d(x)=d_x^Tx+d_c\). Choose

\[
 K_1=K_0\cap\ker d_x^T,\qquad
 x=T_1u+T_0v,\qquad \operatorname{range}T_0=K_1,              \tag{4}
\]

where \([T_1\ T_0]\) is rational and invertible. Rational elimination
produces such a matrix and its inverse with polynomial encoding length.
The coordinate \(u\) has dimension \(r\le r_0+1\).

Every native Hessian annihilates \(T_0\). Thus all original quadratic
and affine rows, including the cone signs, take the form

\[
                  Cv\le b(u),                              \tag{5}
\]

with a constant rational matrix \(C\), rational quadratic entries of
\(b\), and polynomial coefficient bit length. The native convex
representation is retained by the algorithm; (5) is used for proofs.
Since \(d_x^TT_0=0\),

\[
 d(x)=d_0(u),\qquad p(x)=p_v^Tv+p_0(u).
\]

Consequently the optimal-level equation is

\[
                p_v^Tv=\theta d_0(u)-p_0(u).                \tag{6}
\]

Represent (6) by two inequalities and append them to (5):

\[
                 C'v\le b_\theta(u).                       \tag{7}
\]

Crucially, \(C'\) is rational. Each right-hand-side entry is a
polynomial of total degree at most two in \((\theta,u)\), with rational
coefficients of polynomial bit length. No number-field linear program
is required. If \(d_x\) already annihilates \(K_0\), the extra retained
direction is unnecessary.

## 3. The projected canonical point has one small field

Farkas' lemma applied to the constant rational matrix \(C'\) describes
the projection of (7) as

\[
 U_\theta=\{u:P_j(u)\le0\ (1\le j\le S)\},                    \tag{8}
\]

where each \(P_j\) is quadratic over \(K=\mathbb Q(\theta)\).
Extreme rays of the nonnegative dependence cone can be scaled by rational
minors. Their rational coefficient lengths are polynomial in \(N\);
their count obeys \(\log(S+1)\le N^{O(1)}\). Each coefficient of
\(P_j\) is affine in \(\theta\), with polynomial-size rational
coefficients. The description is used only for bounds; its potentially
exponential family is never generated.

Equation (8) proves closedness. The original level is convex, so its
projection is convex. When nonempty, \(U_\theta\) therefore has the
unique point

\[
                   u_*=\arg\min_{u\in U_\theta}\|u\|^2.      \tag{9}
\]

The low-dimensional perturbation proof in
[the common-range witness note, Section 3](common-range-witness-recovery.md#3-a-classical-low-dimensional-arithmetic-bound)
extends over this explicitly represented field. Here is the dependence
needed for the FPT conclusion.

Choose an unknown box strictly containing \(u_*\), and generic integer
quadratic perturbations of the \(S\) inequalities and squared-norm
objective. The grid argument requires perturbation coefficient bits
\(O(r\log(S+1))+\operatorname{poly}(r)\), even though \(S\) may be
exponential. Outward bands and a vanishing objective perturbation make
every minimizing limit equal to \(u_*\). All artificial box rows are
therefore eventually inactive; their unknown endpoints enter no eventual
equation.

Pass to one active set of at most \(r\) perturbed rows. The full KKT
system has at most \(2r\) variables, total degree two in those variables,
and a nonsingular Jacobian. Its coefficient norms at all places of
\(K\) have averaged logarithmic bound
\(f(r,D)(N+H)^C\). Only the selected rows enter this bound. It does not
sum heights over all \(S\) inequalities.

Apply the purely algebraic
[finite-quotient lemma over \(K\)](algebraic-coefficient-span-precision.md#3-the-finite-quotient-lemma-over-k)
to this full system, with degree two. The quotient dimension is at most
\(L=3^{2r}\). For each coordinate, and every fixed \(K\)-linear
combination of the coordinates of this **same** point, it gives a
nonzero annihilator over \(K\) of degree at most \(L\). The
relative primitive-element argument gives

\[
       [K(u_*):K]\le3^{2r},\qquad
       [\mathbb Q(\theta,u_*):\mathbb Q]\le D\,3^{2r}.        \tag{10}
\]

Independent coordinate-degree bounds alone would not establish (10).
All coordinate outputs use one selected root sequence, support, and limit.

The field lemma's height bound is linear in the coefficient-norm budget
times a function of the quotient dimension and number of variables.
Local Cauchy bounds and the product formula then give absolute coordinate
heights of the form (3). The constants multiplying \(N+H\) may depend
on \(r,D\), but its exponent is absolute. No normal closure is taken,
and no optimization statement is made at another field embedding.

## 4. The affine fiber preserves that field

In the nonempty fiber at \(u_*\), let

\[
 v_*=\arg\min\{\|v\|^2:C'v\le b_\theta(u_*)\}.                \tag{11}
\]

For some independent active row set \(I\), the normal-cone condition
and the Gram formula give

\[
 v_*=(C'_I)^T(C'_I(C'_I)^T)^{-1}(b_\theta(u_*))_I.           \tag{12}
\]

The empty set covers \(v_*=0\). The matrix in (12) is rational with
polynomial coefficient bit length. It follows that
\(v_*\in K(u_*)^{n-r}\), proving (2). Its entries are rational
polynomials of degree at most two in \((\theta,u_*)\).

For the height bound, clear a common integralizing denominator for
\((\theta,u_*)\), square it for the quadratic evaluations in (12), and
clear the rational Gram denominators. Bounding every conjugate and taking
a field norm gives coordinate minimal-polynomial bits of the form (3).
There is no multiplication of one field degree per ambient coordinate.
The bounded primitive-element and trace-pairing argument from
[the common-field witness review, Section 6](algebraic-socp-witness-field-review.md#6-one-short-absolute-representation-including-the-input-generator)
then gives a short absolute representation of the whole tuple.

Cauchy's root bound now supplies a computable integer \(B\ge1\) whose
bit length has the form (3), and for which

\[
                  (u_*,v_*)\in[-B,B]^n.                     \tag{13}
\]

This box contains the specified canonical point. A box that merely met
the level would not justify the recovery argument below.

## 5. Rational value queries recognize the optimal level

Let \(F_B\) be the original rational feasible set intersected with the
box (13), expressed by rational affine rows in the original coordinates.
It is compact and contains the canonical optimal point. Since \(d>0\)
on the original \(F\), the ratio is continuous on \(F_B\).

For any rational additional affine rows in \(u\), and any rational
threshold \(t\ge0\) on \(\|u\|^2\), let \(G\) be the resulting
rational subdomain of \(F_B\). It is compact. If nonempty, its ratio
minimum \(\beta_G\) is attained and at least \(\theta\). Therefore

\[
 G\cap\{p-\theta d=0\}\ne\varnothing
 \quad\Longleftrightarrow\quad
 G\ne\varnothing\ \text{ and }\ \beta_G=\theta.               \tag{14}
\]

Use the exact rational fractional-value algorithm and ordinary univariate
real-algebraic comparison to evaluate (14). Discard each queried value
after comparison; do not form a compositum of all queried value fields.
Compactness is essential: equality of an
unattained infimum with \(\theta\) would not detect level membership.
The new squared-norm row has the rational cone form

\[
           \|(2u,t-1)\|_2\le t+1.                          \tag{15}
\]

If \(u=Lx\), its squared Hessian \(8L^TL\) annihilates \(K_1\).
Thus these calls have common range at most \(r\le r_0+1\).
For native convex quadratics one can instead append
\(\|u\|^2\le t\) directly. Affine bounds add no Hessian directions.
No algebraic coefficient is appended to these oracle inputs.

The box preserves the point \(u_*\), so \(u_*\) remains the unique
minimum-norm member of the projected optimal set in \(F_B\).
Use (14) to bisect its squared norm and then its coordinates exactly as
in the rational common-range witness algorithm. If a feasible norm upper
threshold is within \(\eta^2/16\) of \(\|u_*\|^2\), every projected
optimal point in that slice has distance at most \(\eta/4\) from
\(u_*\), by the convex projection inequality. Coordinate bisections
preserve a nonempty slice and produce coordinate error below \(\eta\).
Restart from (13) at each accuracy request and retain only current
endpoints. These are approximations to one fixed point.

The number of value queries and their input lengths are polynomial in
\(N,\log B,\log(1/\eta)\), with an absolute exponent. The assumed
coefficient-sensitive FPT value runtime therefore supplies the desired
FPT approximation oracle for \(u_*\).

## 6. Recover the remaining coordinates with rational QPs

Approximate the selected \(\theta\) by refining its input isolator and
approximate \(u_*\) by Section 5. Evaluate
\(b^*=b_\theta(u_*)\) to coordinate error \(\delta\), and round
outward:

\[
          b^*\le\widehat b\le b^*+2\delta\mathbf1.
\]

Solve the exact rational convex QP

\[
       v_\delta=\arg\min\{\|v\|^2:C'v\le\widehat b\}.         \tag{16}
\]

The proof and error estimate in
[the common-range witness note, Sections 5--5.1](common-range-witness-recovery.md#5-recover-the-affine-fiber-through-rational-quadratic-programs)
apply without change. For a computable rational-matrix Hoffman constant
\(H_{C'}\) with polynomial bit length, put
\(\zeta=2H_{C'}\delta\). If \(V\) is a bound for \(\|v_*\|\),
then

\[
 \|v_\delta-v_*\|
       \le\zeta+\sqrt{2V\zeta+\zeta^2}.                      \tag{17}
\]

Only \(O(p+\log V+\log H_{C'})\) precision bits are needed for
error \(2^{-p}\). Polynomial evaluation of \(b_\theta(u_*)\) has
the same FPT precision bound. All QPs in (16) are rational.

Apply [constructive common-field recovery](constructive-common-field-recovery.md)
to the fixed tuple \((\theta,u_*,v_*)\), using (2)--(3) and these
approximation procedures. The recognition, primitive-element search, and
coordinate interpolation have polynomial overhead in tuple length,
degree, and height. The total time therefore has the form (3). The
output includes the input value's selected embedding. Transform back to
\(x\), verify all original quadratic or cone rows and cone signs, and
verify \(d(x)>0\) and \(p(x)=\theta d(x)\) by exact field arithmetic.

If \(r=0\), the optimal-level fiber is already a rational-matrix
polyhedron with algebraic right-hand side. The \(u\) recovery is empty;
Sections 4 and 6 apply directly. If there are no \(v\) coordinates,
the QP step is empty. These cases need no separate optimization oracle.

## 7. Mixed-integer attainment and complete recovery

For an unbounded integer domain, the native cross-aware common kernel is
the continuous space annihilated by every full Hessian, including integer
cross blocks. Intersect that kernel with the denominator's continuous
linear kernel before choosing (4). This increases its codimension by at
most one and ensures that (5) has a constant rational matrix uniformly
in the integer assignment. With a supplied integer box, one can instead
use the continuous common kernel after substitution.

For MISOCP, the [fractional value theorem](common-range-fractional-frontier.md)
returns the exact finite infimum \(\theta\), with degree
\(D\le f(k,\rho)\) and representation bits \(H\le f(k,\rho)N^C\).
It also supplies an effective conditional bound \(M\le f(k,\rho)N^C\)
on the bit length of an attaining integer assignment, if one exists.
This bound alone does not decide attainment.

Fix one global rational split (4). For every integer assignment in that
box, substitution gives continuous data of length polynomial in \(N+M\).
The encoding result above applies to every nonempty \(\theta\)-level
fiber, independently of whether the level is globally optimal over real
integer coordinates. It yields one uniform transformed continuous box
(13), of bit length

\[
                f(r,D)(N+M+H)^C\le f(k,\rho)N^C,            \tag{18}
\]

containing that fiber's canonical level point whenever it exists.

Intersect the original model with both the integer box and this full
continuous box. Its mixed-integer feasible set is compact: there are
finitely many allowed integer assignments and each continuous fiber is
closed and bounded. The positive-denominator ratio is continuous on this
set. If the set is nonempty, its infimum \(\beta\) is therefore attained.
Use the exact fractional value theorem on this rational boxed instance.
Then

\[
 \theta\text{ is attained originally}
 \quad\Longleftrightarrow\quad
 \text{the boxed set is nonempty and }\beta=\theta.          \tag{19}
\]

For the forward direction, one small attaining integer assignment exists,
and its canonical level point belongs to the continuous box. The converse
uses attainment of the boxed minimum. If (19) fails, report that the
original finite infimum is unattained.

If (19) holds, bisect each integer coordinate interval, preserving
nonemptiness and boxed value equal to \(\theta\). Compactness makes this
equivalent to preserving an actual optimizer. Polynomially many exact
value comparisons fix one optimal integer assignment. Now use Sections
2--6 in that continuous fiber. The uniform box contains its canonical
point, and all subsequent norm cuts concern \(u\), so the common range
remains bounded by \(\rho+1\).

Every box, substituted coefficient, query, field representation, and
recognition precision has length \(f(k,\rho)N^C\). All algorithmic
dependencies have an absolute input exponent. Thus, together with the
value theorem, this proves full exact affine-fractional MISOCP optimization
in \(f(k,\rho)N^C\) time: feasibility, unboundedness below, finite
value, attainment, an optimal integer assignment when attained, and an
exact continuous optimizer. The same reasoning applies to a supplied
integer box with its corresponding continuous common-range parameter.
For that version, obtain the value bound from the finitely many fixed
integer fibers: the finite mixed infimum is one of their continuous
infima, whose degree and height have uniform bounds after substitution.
Use bounded-integer threshold feasibility for value recognition. This
avoids importing the unbounded cross-aware parameter into the supplied-box
claim.
The continuous encoding and recovery results also cover native PSD
quadratic constraints. The main fractional theorem now supplies the
matching value oracle for PSD, SOC, and mixed native constraints, so the
complete mixed-integer result applies to all these models.

## 8. A maximum of affine-fractional objectives

Consider

\[
                   \min_{x\in F}\ \max_{1\le j\le s}
                                      \frac{p_j(x)}{d_j(x)}, \tag{20}
\]

where each \(p_j,d_j\) is rational affine and every denominator is
strictly positive throughout the original closed feasible set. Let
\(\ell\) be the rank of the denominator gradients restricted to
\(K_0\). Equivalently, \(\ell\) is the codimension in \(K_0\)
of their common kernel. Retain all these directions:

\[
 K_1=K_0\cap\bigcap_j\ker d_{j,x}^T,\qquad
                       r\le r_0+\ell.                      \tag{21}
\]

At a known finite attained minimum \(\theta\), the optimal set is
exactly

\[
                F\cap\bigcap_j\{p_j-\theta d_j\le0\}.        \tag{22}
\]

Every point in this weak sublevel must attain \(\theta\), because it
cannot have objective less than the global infimum. No union of active
objective rows or strict inequality is needed. After (21), each added
row has the constant rational \(v\)-normal \(p_{j,v}\) and
right-hand side \(\theta d_{j,0}(u)-p_{j,0}(u)\).

The proof of Sections 3--6 therefore applies to (22) without change.
In particular, the joint field degree is at most \(D3^{2r}\).
The number of fractional terms enters the input length and the number
of affine rows; it does not enter the algebraic degree separately.
On every compact rational query domain, (20) is continuous and its
minimum equals \(\theta\) exactly when that domain meets (22).
Final verification checks every denominator sign and every inequality
in (22); the known global value then certifies the objective value.

The encoding argument applies to every nonempty weak threshold (22),
whether or not \(\theta\) is optimal there. It therefore supplies the
uniform box across bounded integer assignments needed in Section 7.
The mixed-integer composition of that section also applies. Combined with
the maximum-of-ratios value corollary for MISOCP, it gives full exact
optimization in \(f(k,\rho,\ell)N^C\) time. This statement is not FPT
in \((k,\rho)\) when \(\ell\) is unrestricted. All denominators
annihilate the retained kernel, so norm cuts in \(u\) do not require
any further denominator directions.

## 9. An explicitly positive denominator domain

The preceding algorithms also solve an input whose stated domain is
\(F\cap\{d_j>0\text{ for all }j\}\), where \(F\) is the original
closed rational SOC set and need not itself satisfy the denominator
positivity promise. Use one shared additional continuous variable \(s\)
and append the rational cones

\[
             \|(2,d_j(z,x)-s)\|_2\le d_j(z,x)+s
                                  \quad(1\le j\le m).       \tag{23}
\]

Each cone is equivalent to
\(d_js\ge1\) together with \(d_j+s\ge0\). The product is positive,
so both factors have the same sign; the sum excludes the negative sign.
Thus every lifted feasible point has \(d_j>0\) and \(s>0\).
Conversely, every original point with all \(d_j>0\) admits
\(s=\max_j 1/d_j\). The projection of this closed rational cone system
is therefore exactly the stated open positive domain.

Keep the original ratio objective, independent of \(s\). Feasibility,
infimum, unboundedness below, and attainment are preserved in both
directions. In particular, an original optimizer lifts to a finite
feasible \(s\), and a lifted optimizer projects to an original one.
The lifted model satisfies the positivity promise everywhere, so the
preceding complete algorithm applies; discard \(s\) from its output.

This construction also preserves the structural parameter. Let \(K_*\)
be the original cross-aware common kernel and let \(\ell\) be the rank
of the denominator continuous gradients restricted to \(K_*\). The
new squared residual is \(4-4d_js\). Its full Hessian annihilates
every \((0,v,0)\) with \(v\in K_*\) and \(d_{j,x}^Tv=0\).
Hence the new common-range codimension obeys

\[
                     \rho_{\rm new}\le\rho+\ell+1.          \tag{24}
\]

Moreover, the \(s\)-component of that Hessian applied to an arbitrary
continuous kernel direction \((v,\sigma)\) is
\(-4d_{j,x}^Tv\). It follows that all denominator gradients annihilate
the new common kernel: the new restricted denominator rank is zero.
The integer dimension is unchanged, and (23) has polynomial input
length.

Thus the positive-domain problem is fully solvable in
\(f(k,\rho,\ell)N^C\) time. For a single fraction,
\(\rho_{\rm new}\le\rho+2\). A number of denominators growing with
the input requires only one extra variable; their restricted gradient
rank, rather than their count, controls (24). This lifting is a standard
rotated-cone construction, not a novelty claim.

The returned point is the projection of a canonical point of the lifted
problem. It need not be a minimum-norm point of the original open domain.
The compact value tests are performed on the lifted closed system;
directly applying them to the original open domain would be unjustified.
The [separate positive-domain review](common-range-positive-domain-review.md)
checks the full Hessian kernel, integer cross terms, exact projection,
and attainment preservation independently.

## 10. Prior and limits

The ingredients are established low-dimensional critical-point bounds,
Farkas' lemma, minimum-norm selection, rational quadratic programming,
Hoffman's error bound, and algebraic recognition. Their primary-source
comparisons appear in the linked witness notes and the
[fractional value prior audit](quasiconvex-mixed-value-prior.md).
The contribution here is this specific FPT composition and
the denominator-direction reduction. No independent novelty or priority
claim is made.

Strict positivity throughout the closed feasible set used by the oracle
is a substantive assumption. Section 9 enforces it for explicitly open
positive-domain inputs. Without that lift, a rational box need not make
the ratio attain its infimum, and (14) would need another argument.
Nor is a known finite infimum assumed to be attained: Section 7 decides
attainment, and optimal-level recovery is used only after nonemptiness
of that level has been established.

Even when the original optimum is attained, an unbounded query domain
can cause a false level test. On \(w\ge0,\ y\ge1\), the ratio
\(w/y\) attains value zero. After the rational cut \(w\ge1\), its
infimum is still zero but no point has value zero. Keeping the full
finite box in Section 5 repairs this: for box radius \(B\ge1\), the
cut-domain minimum is \(1/B>0\).

## Verification record

The [field review](fractional-common-range-field-review.md) independently
checks the selected-support height bound, relative and absolute joint
degree, same-field affine fiber, common representation, and uniform
integer substitution. It also checks the maximum-of-ratios extension.
The [algorithm review](fractional-common-range-algorithm-review.md) checks
the compact value oracle, canonical-point selection, rational QP step,
uniform boxing, attainment, integer recovery, and the absolute input
exponent. Separate narrow reviewers checked the field arithmetic and
rational-QP adaptation. No unresolved gap was found.

One wording correction was incorporated: the value theorem supplies a
conditional integer-size bound; Section 7 supplies the additional compact
boxing and bisection argument needed for integer recovery. The supplied
integer-box variant now also states its finite-fiber value argument.

The reviewers ran exact inline SymPy checks of the denominator-kernel
refinement, norm-Hessian preservation, irrational optimality and fiber
identities, proper extension fields, and the unattained-cut example above.
These finite calculations do not establish the universal arithmetic or
complexity bounds. A targeted inline Python document check covers this
note and its two reviews: final newlines, whitespace, control characters,
paired math delimiters, and local Markdown links. No project-wide checks,
CI inspection, or Lean formalization are asserted.

The positive-domain review separately ran exact symbolic checks of the
cone identity, full Hessian action, correlated denominator directions,
constant denominators, and a denominator depending only on an integer
variable. Its final read of Section 9 found no gap. The targeted document
check was extended to include that review.
