# The selection-free PSD2 nullity seam: an obstruction and its resolution

Status: Rigorous reduction and obstruction, independently hostile-audited;
main question subsequently refuted by an explicit compact lift  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the reduction and explicit negative resolution

## Question

Let \(B_2^s\), \(s\geq3\), have a finite affine lift over a product of
real \(2\times2\) PSD cones and scalar rays, after minimal-face reduction
and relative Slater.  Is there always a support point
\(v\in S^{s-1}\) such that **every** primal lift over \(v\) has total
PSD nullity at least \(s\)?

No.  The later
[rotated Lorentz perspective construction](2026-09-04-rotated-lorentz-fiberwise-nullity-counterexample.md)
is a compact full-Slater lift through \((\mathbb S_+^2)^{s-1}\) for which
every support fiber contains a tuple of total nullity exactly \(s-1\).
The reductions below remain useful because they identify precisely the
fiber-valued seam mechanism that this counterexample realizes.  This
negative answer does **not** settle the different conjecture that the
restricted standard log-determinant barrier must have parameter at least
\(s\); the counterexample's exact parameter is \(2s-3\).

The exact selection-free exposed-certificate rank is only \(s-1\).
Binary norm chains attain that value, but at their rank-birth poles their
unique primal fibers have nullity strictly larger than \(s-1\).  This
suggests a universal seam premium, but the arguments below do not prove
it.

## 1. A fiber-intrinsic range-span reduction

Let \(\mathcal P(v)\) be the full primal lift fiber over \(v\), and let
\(\mathcal D(v)\) be the full normalized dual-certificate fiber of the
support inequality \(1-v^Tx\).  For block \(i\), define

\[
 E_i(v)=\sum_{Y\in\mathcal D(v)}\operatorname {Ran}Y_i,\qquad
 e(v)=\sum_i\dim E_i(v),                                  \tag{1}
\]

with a scalar ray treated as a \(1\times1\) PSD block.  The full affine
slack identity holds for every \(X\in\mathcal P(v)\) and every
\(Y\in\mathcal D(v)\).  At contact it gives

\[
 \sum_i\operatorname {tr}(X_iY_i)=0.
\]

Every summand is nonnegative, hence \(X_iY_i=0\) for every pair
\((X,Y)\).  Therefore

\[
 E_i(v)\subseteq\ker X_i\quad
       \text{for every }X\in\mathcal P(v),
\]
and consequently

\[
 \boxed{\quad
   \min_{X\in\mathcal P(v)}
       \sum_i\operatorname {nullity}X_i\ \geq e(v).\quad} \tag{2}
\]

Thus \(e(v)\geq s\) at one support would prove the desired theorem,
simultaneously for every primal fiber.

The semialgebraic generic-curvature argument gives a sharp alternative.
Choose a minimum-total-rank certificate semialgebraically and a
semialgebraic primal selector.  On the dense open union of common
full-dimensional \(C^1\) contact strata, the sphere mixed metric has rank
\(s-1\), while each productive \(\mathbb S_+^2\) block carries at most one
mixed direction.  Hence the selected certificate has total rank at least
\(s-1\), and

\[
                         e(v)\geq s-1                    \tag{3}
\]

on that dense open set.

Suppose, in an attempted counterexample to the seam premium, that every
support fiber contains a primal point of nullity at most \(s-1\).
Equation (2) then gives \(e(v)\leq s-1\) everywhere.  Combining with (3)
shows

\[
                         e(v)=s-1                       \tag{4}
\]

on a dense open set.  Equality in the mixed-curvature chain forces exactly
\(s-1\) productive rank-one channels there.  On each fixed-label
regular stratum their normalized projective phases form a local
diffeomorphism to a product of \(s-1\) circles.

This reduction isolates the missing step: one must use the **affine slack
identities** to show that these saturated local phase charts cannot glue
across their lower-dimensional singular set without making \(e(v)\), and
hence every primal nullity, rise by at least one.

### A compact-fiber dichotomy

Compactness does give one useful pointwise alternative.  For any support
\(v\), let \(F(v)\) be the product PSD face consisting of tuples whose
\(i\)-th block is supported on \(E_i(v)^\perp\).  Full-fiber
complementarity and the affine lift equations give the exact identity

\[
                  \mathcal P(v)=\mathcal A_v\cap F(v),          \tag{4a}
\]

where \(\mathcal A_v\) is the affine space of lift equations with projected
coordinate fixed to \(v\).  Every point in the relative interior of
\(F(v)\) has total nullity exactly \(e(v)\).

If the compact convex set \(\mathcal P(v)\) is not a singleton, take the
affine line through two of its points.  Its intersection with \(F(v)\) is
a nondegenerate compact interval.  Each endpoint lies on the relative
boundary of \(F(v)\), and hence has at least one additional zero eigenvalue.
Therefore

\[
 \mathcal P(v)\text{ nonsingleton}
 \quad\Longrightarrow\quad
 \max_{X\in\mathcal P(v)}\sum_i\operatorname{nullity}X_i
       \geq e(v)+1.                                      \tag{4b}
\]

In particular, if every tuple in every boundary fiber has nullity at most
\(s-1\), then every fiber with \(e(v)=s-1\) is a singleton.  Any branching
capable of gluing the generic torus charts must occur where the **full**
dual range span drops to at most \(s-2\).  A disappearing selected
certificate is not enough.  The rotated-perspective counterexample below
illustrates the other branch of (4b): its north fiber is nonsingleton but
its full dual span retains dimension \(s-1\), so that fiber necessarily
contains higher-nullity vertices even though its minimum nullity stays
\(s-1\).

## 2. Why topology and semialgebraicity alone do not close the gap

The global-\(C^1\) proof excludes a local diffeomorphism
\(S^{s-1}\to(S^1)^{s-1}\).  In the selection-free setting the phase
incidence may instead be a branched cover, and the derivative may lose
rank precisely on the branch locus while every individual phase remains
rank one.

This is not a merely hypothetical topological phenomenon.  In the first
case \(s=3\), a complex elliptic curve is a real two-torus, and quotienting
by the involution \(z\mapsto-z\) gives a degree-two map

\[
                            T^2\longrightarrow S^2        \tag{5}
\]

branched at four points.  In a projective Weierstrass model this is an
algebraic map to \(\mathbb {CP}^1\), so allowing a definable or analytic
branch locus does not remove the obstruction.  Equation (5) is **not** a
cone lift or slack factorization.  It proves only that compactness,
semialgebraicity, and the topology of the rank-one phase space cannot by
themselves upgrade the local phase argument to a global covering
contradiction.

Convex primal fibers do not immediately repair the proof.  If two
low-nullity branches meet in one fiber, averaging their PSD tuples joins
their ranges and can reduce, rather than increase, primal nullity.
Moreover, the maximum-rank point of a compact spectrahedral fiber need not
vary lower-semicontinuously at a projection-singular boundary point.
These are exactly the hypotheses missing from the audited
constant-boundary-nullity and contact-accessibility theorems.

### The bounded affine case is an exposed-face correspondence

There is additional structure beyond an arbitrary branched cover.  Suppose
the total lifted spectrahedron \(S\) is compact and \(\pi(S)=B_2^s\).  For
every \(v\in S^{s-1}\), strict convexity of the ball gives
\[
 \mathcal P(v)
   =\{X\in S:\pi X=v\}
   =\operatorname*{argmax}_{X\in S}\langle v,\pi X\rangle . \tag{6}
\]
Thus every boundary fiber is an exposed face of one compact
spectrahedron, and the full primal incidence is the restriction of its
normal-face correspondence to the linear family of normals \(\pi^*v\).
Any counterexample must realize the branched phase behavior inside this
cyclically monotone convex correspondence; an arbitrary semialgebraic
branched map such as (5) is not enough.

This observation still does not supply a continuous section.  Exposed
faces are generally only upper semicontinuous in the normal, and a face can
enlarge at a limiting normal.  Mathis and Meroni's
[*Fiber Convex Bodies*](https://doi.org/10.1007/s00454-022-00451-3),
Example 2.12, records a semialgebraic convex-body projection for which a
boundary fiber-body point has no continuous representative.  Equation (6)
is therefore a useful affine-integrability constraint, not a completed
selection theorem.

Even an exact compact full-Slater cone lift can have this failure.  Fix
\(x_0\in S^{s-1}\) and impose

\[
 0\leq z\leq1,
 \qquad (1-z,x-zx_0)\in Q_{s+1}.                         \tag{7}
\]

For fixed \(z\), its projection is
\(zx_0+(1-z)B_2^s\subseteq B_2^s\), while \(z=0\) already gives the whole
ball.  The lifted feasible set is compact and has full Slater, for example
at \(x=0\) and \(0<z<1/2\).  Strict convexity gives

\[
 \mathcal P(x)=\{(x,0)\}\quad(x\in S^{s-1},\ x\neq x_0),
 \qquad
 \mathcal P(x_0)=\{(x_0,z):0\leq z\leq1\}.              \tag{8}
\]

Hence none of the points with \(0<z\leq1\) in the exceptional fiber is
accessible from nearby boundary fibers.  This is not a counterexample to
the PSD2 nullity premium--it uses one larger Lorentz block and two rays--but
it rules out any proof that derives contact accessibility from compactness,
full Slater, convex fibers, and closed graph alone.

## 3. What the later counterexample must, and does, realize

Before the counterexample was found, an affirmative proof would have had
to establish at least one of the following additional facts from the
affine representation itself:

1. the intrinsic span \(E(v)\) is continuous through a saturated
   rank-\((s-1)\) branch, which restores the global torus-cover
   contradiction;
2. every branch point forces \(e(v)\geq s\), so (2) supplies the seam
   premium directly; or
3. a determinantal classification rules out affine
   \(Q_3^{\,s-1}\)-incidences realizing a branched phase map such as (5).

Conversely, a counterexample had to give an explicit affine lift whose every
boundary fiber contains a primal point of nullity at most \(s-1\).  A
purely topological branched cover is insufficient because it must also
satisfy all global linear slack identities and PSD positivity.

The binary norm chain shows why generic arguments cannot decide the
question: its exposed certificate rank drops at a pole, while its primal
nullity rises there.  The present note proves the intrinsic implication
(2), identifies the dense-open saturated alternative (4), and records the
branched-cover and compact-accessibility obstructions.  The rotated
perspective lift cited above closes the affine-integrability question in
the negative: its north-pole simplex supplies the required fiber-valued
seam without raising the minimum nullity.

## Independent hostile audit

The audit verified that full-fiber complementarity puts the span of every
dual certificate range in the kernel of every primal lift, proving (2).
It also checked the semialgebraic minimum-rank selection and the
dense-open saturation conclusion (3)--(4), including the local phase
maps.  The elliptic quotient \(T^2\to S^2\) is correctly used only to
show that an algebraic branch locus defeats a purely topological covering
argument; it is not presented as a cone lift.  Finally, convex averaging
can indeed join PSD ranges and lower nullity.  No correction was required.
