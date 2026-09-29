# Root audit of the strict-convexity SOS descent counterexamples

Date: 2026-09-28. Status: full mathematical read completed. The root
contributed the final coefficient-field strengthening of the ternary
example, so this is an additional audit, not its fresh noncontributor
review. Those reviews are linked from the main notes.

The [three-variable integer quartic](ternary-rational-sos-convex-counterexample.md)
is the stronger main example. It has a rational positive definite
Hessian Gram matrix, Hessian at least the identity, minimum zero,
and no rational polynomial SOS. Its SOS and positive semidefinite
Gram coefficient fields are exactly the real fields containing
\(\mathbb Q(2^{1/5})\). The
[four-variable example](rational-sos-convex-descent.md) remains useful:
its simpler linear product-space obstruction differs from the
positivity obstruction in three variables.

## Independent reconstruction of the four-variable argument

The root read the integrated proof, the algebraic construction,
the primary-literature comparison, and the independent review in full.
For \(\alpha^3=2,\ \beta^3=5\), the trace argument proves that
\(\beta\notin\mathbb Q(\alpha)\). Indeed, writing
\(\beta=b_0+b_1\alpha+b_2\alpha^2\), equality of cubic fields would
give traces \(3b_0=0\) and \(12b_1b_2=0\). The remaining rational
cube equations are impossible. A reducible cubic over this real field
would contain its unique real root, so the joint field degree is nine.

The nine quadratic evaluations
\(1,x,y,z,w,xz,xw,yz,yw\) span that field. This proves that the
six displayed rational vanishing quadratics form the entire space
\(I_2\), not merely a subspace. Products within one block involve
no variable of the other block; products across blocks have degree at
most two in each. They cannot contain \(yz^3\).
The perturbation does contain that monomial, while its value and
gradient vanish at the specified point. A rational SOS quartic at
that zero would have all its factors in \(I_2\), giving the required
contradiction.

The root checked the square-Hessian Gram formula, including the
constant term at a rational center. Positive definiteness of the
reported Gram is established by retained exact arithmetic and
independent reconstruction, not by sampled Hessians. The full basis
contains the direction itself, so the strict Gram proves a uniform
Hessian lower bound.

## Independent reconstruction of the ternary obstruction

Put \(a^5=2\) and \(p=(a^{-1},a,a^{-3})\). Eisenstein gives degree
five. The evaluations of \(1,y,z,yz,x\) span
\(1,a,a^2,a^3,a^4\), so the five quadratics \(r_i\) in the
main note are a basis of all rational quadratics vanishing at \(p\).

The root independently checked the functional
\(\Lambda(P)=2[z]P+4[y^2]P\).
In the unscaled basis \(q_i=r_i/2\), only \(q_4^2\) and
\(q_0q_2\) can contribute either indicated monomial. The relevant
part of \(q_0q_2\) is \(y^2-2z\), which cancels under
\(\Lambda\); \(\Lambda(q_4^2)=1\). Hence
\(\Lambda(r_i r_j)=4\delta_{i4}\delta_{j4}\).

The explicit formula has \([z]F=2(8)(-12)=-192\) and
\([y^2]F=2(8)(6)-1=95\). Thus \(\Lambda(F)=-4\).
This conditional SOS obstruction suffices without the optional
fifteen-product determinant. It is essential that \(\Lambda\) is
positive only on the specified vanishing-space squares; it is not
a separating functional for the full real SOS cone.

The exact Hessian identity and positivity have two independent
verification routes: rational LDL pivots, and a separately reconstructed
matrix with positive exact leading principal minors. The root read
those formulas and records without repeating their computations.
The rational center and complete Gram basis make their implication
\(\nabla^2F\succeq I\) global. Since every residual vanishes at
\(p\), value and gradient vanish exactly despite the negative square.

## The field classification

The root first observed the prime-degree obstruction for fields of
degree not divisible by five. The author strengthened it to arbitrary
real coefficient fields. The root independently rechecked that stronger
proof: if \(T^5-2\) has a proper monic factor over
\(E\subseteq\mathbb R\), its constant is
\((-1)^r a^r\zeta_5^j\), with \(1\le r\le4\).
Reality forces \(\zeta_5^j=1\), and a Bézout identity for \(r,5\)
then gives \(a\in E\). Therefore, when \(a\notin E\), the same
five-dimensional quadratic evaluation kernel and coefficient
functional exclude an \(E\)-SOS.

The Gram necessity needs its own argument. It cannot rely on a
positive semidefinite matrix over a real field having an unweighted
square factorization over that field. If an \(E\)-valued Gram \(Q\)
exists, \(Qb(p)=0\) puts its rows in the quadratic evaluation kernel.
Writing its rational basis matrix as \(B\), a rational left inverse
\(C\) gives \(Q=BSB^{\mathsf T}\) with
\(S=CQC^{\mathsf T}\succeq0\). But then
\(\Lambda(F)=4S_{44}\ge0\), a contradiction.

For sufficiency the root supplied the explicit rational integration
identity

\[
 \int_0^1(1-t)(U+tV)^2\,dt
   =2\left(\frac{U+V/3}{2}\right)^2+\left(\frac V6\right)^2.
\]

First factor the rational Hessian Gram into rational squares using
rational LDL and rational four-square weights. Translation to \(p\)
and Taylor integration then use only coefficients in
\(K=\mathbb Q(a)\). This proves an actual \(K\)-SOS, without an
unjustified claim about positive elements of arbitrary number fields.
Fresh reviewers checked both this identity and the stronger necessity.

## Dimension, perturbations, and limits

The two-variable exclusion uses Scheiderer's classification of
nonnegative rational ternary quartic forms that are not rational SOS.
The strict full Hessian Gram makes the leading affine quartic positive
away from zero. Homogenization therefore has one real projective zero.
The classified product of four complex lines in general position
would have two distinct real conjugate-pair intersections, a
contradiction. The root checked this deduction; independent reviewers
inspected the published theorem. Three is minimal under these exact
Gram assumptions. It is not a dimension theorem for every weaker
notion of convexity.

For any positive rational \(\eta\), Taylor integration supplies a
Gram of \(F\) positive definite on the nonconstant centered
quadratics. Adding \(\eta\) fills the constant coordinate. The
coefficient equations are rational affine equations, whose rational
points are dense; their intersection with the open positive definite
cone consequently contains a rational point. This proves rational
SOS for \(F+\eta\). The root checked this rank and density argument
independently. It is qualitative and gives no bit bound as
\(\eta\) tends to zero.

These examples establish arithmetic nonattainment of rational
polynomial SOS lower bounds for an attained rational optimum.
They do not establish real SDP nonattainment, a duality gap,
optimization hardness, or failure of rational certificates with
denominators or multipliers. The separate denominator investigation
must be retained when assessing practical significance.

The exact checker commands and their outcomes belong to the author
and independent-review records linked from each main note. The root
did not rerun those computations. This audit is a mathematical
reconstruction and scope check; no Lean verification, project-wide
check, or CI inspection is claimed here.
