# Selection-free Hermitian standard-barrier caps off bounded saturation

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; priority not assessed

## Theorem

Fix \(s\geq2\), \(R\geq2\), and
\(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), let
\(a=\dim_{\mathbb R}\mathbb F\in\{1,2,4\}\), and let \(B_2^s\) have a
finite affine lift over a product of Hermitian cones
\(H_+^{r_i}(\mathbb F)\), \(r_i\leq R\), and rays.  Reduce to the minimal
face and assume relative Slater.  Put

\[
                  B=a(R-1),qquad
                  q=\left\lceil{s-1\over B}\right\rceil .          \tag{1}
\]

For the standard product Jordan log-determinant restricted to the affine
lifted slice,

\[
                            \boxed{\nu_{\rm std,slice}\geq q.}       \tag{2}
\]

The grouped Hermitian Schur construction has exact parameter

\[
 \kappa_{\mathbb F,R}(s)=
 \begin{cases}
  1,&R=2, s=a+1,\\
  \lceil s/B\rceil,&\text{otherwise}.
 \end{cases}                                                        \tag{3}
\]

Hence (2) is the exact unrestricted affine-lift frontier whenever
\(B\nmid s-1\), and also in the direct rank-two spin cases in (3).  The
independently audited
[one-channel certificate-fiber theorem](2026-09-04-selection-free-hermitian-one-channel-rigidity.md)
closes every non-spin \(q=1\) divisible case over all three fields at value
two.

In every remaining divisible case, necessarily with \(q\geq2\),

\[
                         s-1=qB,                                   \tag{4}
\]

the grouped value is \(q+1\).  Every **unbounded** affine lift satisfies
the matching lower bound \(\nu_{\rm std,slice}\geq q+1\).  Therefore a
counterexample to the grouped frontier must be a bounded
projection-singular lift in the divisible regime with \(q\geq2\).  No
theorem for that last regime is claimed.

## 1. Generic Hermitian curvature

Choose a primal boundary lift and a minimum-total-rank genuine support
certificate semialgebraically.  On a common full-dimensional \(C^1\)
stratum of \(S^{s-1}\), differentiate the exact identity

\[
                 \sum_i\langle X_i(u),Y_i(v)\rangle=1-u^Tv.         \tag{5}
\]

At contact, write \(p_i=\operatorname{rank}_{\mathbb F}X_i\) and
\(q_i=\operatorname{rank}_{\mathbb F}Y_i\).  Complementarity gives
\(p_i+q_i\leq r_i\).  The real dimension of the Hermitian cross-Peirce
space is \(a p_iq_i\).  Thus the rank-\((s-1)\) tangent metric gives

\[
 \begin{aligned}
 s-1
 &\leq a\sum_i p_iq_i
 \leq a\sum_i(r_i-q_i)q_i\\
 &\leq a(R-1)\sum_iq_i
 \leq B\sum_i\operatorname{nullity}_{\mathbb F}X_i .              \tag{6}
 \end{aligned}
\]

Along the segment from this boundary tuple to a Slater point, the product
Jordan determinant vanishes to order exactly the total primal nullity.
The one-dimensional barrier-gradient inequality therefore proves (2).
The ceiling comparison with (3) is immediate.

This argument is local on a generic semialgebraic stratum.  It assumes no
global primal or dual selection and no constant-rank contact sheet.

## 2. Symmetric-cone recession lemma

Let \(D\ne0\) be a recession direction of the lifted affine slice and
\(\bar X\) a boundary tuple.  For each factor, compress \(\bar X_i\) to
the face complementary to the support idempotent of \(D_i\).  If \(C_i\)
is this compression, put

\[
 r=\sum_i\operatorname{rank}_{\mathbb F}D_i,qquad
 z=\sum_i\operatorname{nullity}_{\mathbb F,f_i}C_i .               \tag{7}
\]

Then

\[
                              \boxed{\nu_{\rm std,slice}\geq r+z.} \tag{8}
\]

To see this, restrict the barrier to

\[
 X(\sigma,t)=(1-\sigma)\bar X+\sigma X^\circ+tD .                  \tag{9}
\]

Peirce--Schur complementation first as \(t\to\infty\), then as
\(\sigma\downarrow0\), gives

\[
 F(X(\sigma,t))=-r\log t-z\log\sigma+O_\sigma(t^{-1})+O(1).       \tag{10}
\]

The scaled mixed Hessian entry vanishes in the iterated limit, so the two
one-dimensional gradient/Hessian quotients add to \(r+z\).  This is the
same determinant calculation over real, complex, and quaternionic
Hermitian cones; the Jordan determinant has one power per positive
eigenvalue.

For the generic genuine certificate \(Y\) from Section 1,
\(\langle D,Y\rangle=0\).  Self-duality and termwise nonnegativity put
\(Y_i\) in the face complementary to \(D_i\).  Its contact with
\(\bar X_i\) gives

\[
                 z\geq\sum_iq_i\geq q.                            \tag{11}
\]

Since \(D\ne0\), \(r\geq1\), and (8) proves \(\nu\geq q+1\) in the
divisible case.  A closed finite-dimensional spectrahedron is unbounded
exactly when it has a nonzero recession direction after quotienting
redundant affine-variable kernels.

## 3. Bounded-fiber reduction

Assume (4), boundedness, and hypothetically \(\nu\leq q\).  Every boundary
tuple then has total nullity at most \(q\).  Equality holds throughout the
generic curvature chain (6): there are \(q\) rank units, every productive
block has order \(R\) and primal rank \(R-1\), and their cross-Peirce maps
jointly have full tangent rank.

A compact non-singleton spectrahedral fiber whose minimum nullity is
\(r\) contains a point of nullity at least \(r+1\).  A relative-interior
fiber point lies in the relative interior of the minimal product-cone face
and has minimum nullity; an endpoint of a maximal nonzero affine chord must
exit that cone-face interior and lose an eigenvalue.  Consequently every
generic minimum-nullity-\(q\) fiber is a singleton under the hypothetical
parameter bound.  A surviving bounded seam must first lower its minimum
fiber nullity below \(q\) and then glue the generic branches without ever
creating a tuple of nullity \(q+1\).

This is exactly the projection-singular mechanism not controlled by
generic semialgebraic selections.  The rotated-Lorentz perspective example
shows that minimum fiber nullity and maximum certificate rank can remain at
the generic lower value even though higher-nullity fiber points increase
the barrier parameter.  It supports, but does not prove, the conjectured
grouped value in the remaining Hermitian cases.

## 4. Every saturated escape needs a range-collapse seam

There is nevertheless a global structural restriction in every field.
Assume the divisible regime \(s-1=qB\), \(q\geq2\), and allow an arbitrary
finite number of factors \(H_+^{r_i}(\mathbb F)\), \(r_i\leq R\), and
rays.  For a support \(v\), let
\(E_i(v)\) be the \(\mathbb F\)-linear span of the ranges of the \(i\)-th
blocks over the entire normalized certificate fiber, and put

\[
 Z=\left\{v\in S^{s-1}:
       \sum_i\dim_{\mathbb F}E_i(v)\leq q-1\right\},                \tag{12}
\]
where a ray support has dimension zero or one.

If the lift is bounded and hypothetically
\(\nu_{\rm std,slice}<q+1\), then

\[
       \boxed{Z\ne\varnothing,\qquad
              \operatorname {codim}_{S^{s-1}}Z\geq B.}            \tag{13}
\]

Thus even a counterexample with arbitrarily many extra factors cannot glue its generic
rank-one contact branches while the full certificate-range span remains
saturated everywhere.  It must contain a genuine range-collapse seam.
This is a statement about the whole convex certificate fiber, not about
one possibly discontinuous selector.

The codimension estimate is local but selection-free.  The full
certificate incidence is semialgebraic, hence so is \(Z\).  On any common
\(C^1\) primal/certificate stratum of \(Z\), of real dimension \(t\),
differentiate the slack identity along the two copies of that stratum.
Its tangent pairing has rank \(t\).  If the selected certificate ranks
are \(q_i\), then \(\sum_iq_i\leq q-1\), while its mixed Peirce channels
have total dimension at most
\[
       a\sum_i p_iq_i
       \leq a\sum_i(R-q_i)q_i
       \leq B\sum_iq_i\leq B(q-1).                       \tag{13a}
\]
Thus every stratum of \(Z\) has dimension at most \(B(q-1)\).  Since the
support sphere has dimension \(qB\), the codimension claim follows.

Suppose instead that \(Z=\varnothing\).  Generic curvature saturation and
the parameter bound make the generic primal fiber a singleton of total
nullity \(q\).  Given any support \(v\), approach it through this dense
generic set.  Compactness gives a limiting primal point over \(v\);
nullity cannot decrease under a matrix limit, while the determinant-order
test forbids nullity above \(q\).  Hence the fiber over every support
contains a point \(X(v)\) of total nullity exactly \(q\).

Complementarity puts every \(E_i(v)\) inside the corresponding kernel of
this point.  Since \(v\notin Z\), the total range-span dimension is at
least \(q\), and the total kernel dimension is \(q\); equality holds.
A finite convex average of normalized certificates has support exactly
\(\bigoplus_iE_i(v)\).  It therefore forces every other point of the
primal fiber to have total nullity at least \(q\), hence exactly \(q\).
The compact-fiber chord lemma makes the fiber a singleton, since an
endpoint of any nontrivial fiber chord would lose one more eigenvalue.
The singleton map \(v\mapsto X(v)\) is continuous by compactness and the
closed primal incidence.

On the dense generic set, equality in the mixed-capacity chain selects
exactly \(q\) fixed full-size blocks, each of nullity one, while every
other Hermitian or ray factor is interior.  Here “fixed” initially means
on one generic stratum.  Each individual block nullity is upper
semicontinuous under the continuous singleton map and their total is
identically \(q\).  Hence the nullity vector is locally constant and,
because the support sphere is connected, the same \(q\)-label set \(J\)
is active everywhere.  Every block in \(J\) has a continuous projective
kernel line \(K_i(v)\in\mathbb FP^{R-1}\).  This gives

\[
 K:S^{q a(R-1)}\longrightarrow\prod_{i\in J}\mathbb FP^{R-1},
       \qquad K(v)=(K_i(v))_{i\in J}.                              \tag{14}
\]

The map is injective.  If \(K(u)=K(v)\), take at \(v\) a convexly averaged
certificate whose support is \(\bigoplus_iK_i(v)\).  Every block of
\(X(u)\) is complementary to the corresponding certificate block, so the
genuine slack identity gives \(1-u^Tv=0\), and the unit vectors satisfy
\(u=v\).

The source and target of (14) are compact connected manifolds of the same
real dimension.  Invariance of domain would make (14) a homeomorphism,
but the product has nonzero intermediate cohomology while the sphere does
not (also when an individual rank-two projective line happens to be a
sphere).  This contradiction proves (13).

For Lorentz factors this specializes to the companion seam theorem.
Equation (13) does not exclude the seam; the bounded divisible
standard-barrier frontier remains open for \(q\geq2\).

## Scope

Equation (2) and the recession closure concern the specified restricted
standard product log-determinant.  They are not lower bounds for arbitrary
barriers or unrestricted QIPM iterations.  The local support certificate
also gives the corresponding exposed-rank metric-movement bound under the
separate audited Dikin theorem.

## Audit checklist

1. Verify the factor \(a\) in the real mixed-channel dimension.
2. Check (3), especially the direct \(H_+^2(\mathbb F)\) spin exceptions.
3. Recheck the Peirce determinant powers and Hessian decoupling in (8).
4. Verify the recession/certificate face inclusion and (11).
5. Verify the full-fiber range-collapse theorem (12)--(14), especially
   the saturated limiting fiber, constancy of the active label set despite
   extra factors, kernel-line continuity, and projective product
   obstruction.
6. Keep bounded divisible saturation explicitly open.

## Independent hostile audit

The audit verified the real cross-Peirce dimension
\(a p_iq_i\), including the quaternionic factor \(4\) rather than \(8\),
and the capacity chain (6).  It checked that the grouped formula (3)
agrees with the direct rank-two spin realization at \(s=a+1\), and that
the nondivisible ceiling comparison is exact.

For the recession lemma, block Peirce--Schur complementation gives one
power of \(t\) per positive Jordan eigenvalue of \(D\), followed by one
power of \(\sigma\) per zero eigenvalue of the complementary compression.
The mixed scaled Hessian term vanishes in the stated iterated limit, so
the two gradient/Hessian quotients add.  The identity
\(\langle D,Y\rangle=0\), self-duality, and termwise nonnegativity place
each \(Y_i\) in the complementary face; complementarity there proves
(11).  The compact-fiber chord argument also checks: a nontrivial affine
fiber chord can end only on the boundary of its minimal product-cone face,
where total nullity increases.  The audit returned **PASS**, with the
minor repair that the theorem now states \(R\geq2\) explicitly.
