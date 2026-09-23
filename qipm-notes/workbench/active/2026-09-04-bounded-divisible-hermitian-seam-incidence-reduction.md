# Bounded divisible Hermitian lifts: the seam-incidence reduction

Status: Proved structural reduction; wide-cap branch excluded in companion theorem  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the reduction; no claim that the remaining lemma is true

## 1. Setting and conclusion

Let \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(a=\dim_{\mathbb R}\mathbb F\), fix a block-order cap \(R\geq2\), and set

\[
             B=a(R-1),\qquad n=s-1=qB,\qquad q\geq2.       \tag{1}
\]

Consider a bounded, relative-Slater affine lift of \(B_2^s\) by a finite
product of cones \(H_+^{r_i}(\mathbb F)\), \(r_i\leq R\), and rays.  Suppose,
for contradiction, that the standard product log-determinant restricted to
the lifted slice has parameter at most \(q\).  This is precisely the last
case not decided by the current Hermitian standard-barrier theorem.

The reduction below proves four facts.

1. Every boundary primal tuple has total nullity at most \(q\), and every
   normalized support certificate has total rank at most \(q\).
2. The full primal--dual contact incidence space is a compact cell-like
   resolution of the support sphere.  In particular, it has the same
   Cech cohomology as \(S^n\), even though its exceptional fibers can have
   positive dimension.
3. Over a dense open semialgebraic set, both primal and dual fibers are
   singletons, strict complementarity holds, and exactly \(q\) order-\(R\)
   blocks carry one productive \(\mathbb F\)-rank-one channel each.
4. A change of generic active-block pattern is impossible without a point
   at which a limiting primal tuple still has nullity \(q\) but its limiting
   certificate has rank at most \(q-1\).  If two pattern regions are actually
   separated, this failure occurs on a semialgebraic hypersurface.

Thus the remaining problem is not a missing compactness argument.  It is a
specific **no-fold/no-branch statement for strict-complementarity failure**.
The compact affine seam example in the two-factor note shows that such a
statement is false for arbitrary spectrahedral slices.  A proof, if true for
ball lifts, must use the global Lorentz slack identity.

The companion wide-cap theorem subsequently proves that the branch cannot
occur when \(B=a(R-1)\geq q-1\): a universal face-codimension budget forces
every boundary tuple to have nullity exactly \(q\), so every fiber is a
singleton and the channel labels cannot switch.  Therefore this note's
open no-fold problem is needed only in the narrow-cap range \(q\geq B+2\).

## 2. Uniform boundary-rank bounds

For \(v\in S^n\), write

\[
 \begin{aligned}
 \mathcal P(v)&=\{X\text{ feasible}:\pi X=v\},\\
 \mathcal D(v)&=\{Y\succeq0:\ \langle X,Y\rangle
                   =1-v^T\pi X\text{ on the whole affine slice}\}.
                                                               \tag{2}
 \end{aligned}
\]

The determinant-order test along a segment from any boundary tuple to a
Slater tuple gives

\[
             \operatorname{nul}X:=\sum_i\operatorname{nul}_{\mathbb F}X_i
                    \leq q
       \quad (X\in\mathcal P(v),\ v\in S^n).                \tag{3}
\]

For every \(X\in\mathcal P(v)\) and \(Y\in\mathcal D(v)\), (2) gives
\(\langle X,Y\rangle=0\).  Self-duality and termwise nonnegativity imply
blockwise complementarity.  Hence

\[
             \operatorname{rank}Y:=\sum_i\operatorname{rank}_{\mathbb F}Y_i
                    \leq \operatorname{nul}X\leq q.         \tag{4}
\]

This holds for every point of every fiber, not only for selected generic
points.  In particular, convexity is quite restrictive: if
\(Y,Z\in\mathcal D(v)\), then

\[
 \sum_i\dim_{\mathbb F}igl(operatorname{Ran}Y_i+operatorname{Ran}Z_i\bigr)
       =\operatorname{rank}(Y+Z)\leq q.                     \tag{5}
\]

Thus all certificates in one fiber lie in a common product-cone face of
total rank at most \(q\).  Notice, however, that (5) still permits one old
channel to vanish before a new channel appears.  It does not rule out the
desired switching mechanism.

## 3. The contact incidence space is cell-like over the sphere

Define

\[
 \Gamma=\{(v,X,Y):v\in S^n,\ X\in\mathcal P(v),\
                              Y\in\mathcal D(v)\}.          \tag{6}
\]

Boundedness makes every \(\mathcal P(v)\) compact.  If \(X^\circ\) is a
fixed product-interior tuple, normalization gives

\[
        \langle X^\circ,Y\rangle=1-v^T\pi X^\circ,
                                                               \tag{7}
\]

whose right-hand side is bounded above and bounded away from zero.  Minimal
face reduction therefore uniformly bounds all certificate fibers.  Their
graphs are closed, so \(\Gamma\) is compact.

For fixed \(v\), every primal in \(\mathcal P(v)\) is complementary to every
dual in \(\mathcal D(v)\), by the whole-slice identity (2).  Consequently

\[
                      \Gamma_v=\mathcal P(v)\times\mathcal D(v). \tag{8}
\]

Both factors are nonempty compact convex sets.  Every fiber of the proper
projection

\[
                         p:\Gamma\longrightarrow S^n          \tag{9}
\]

is therefore contractible.  The Vietoris--Begle mapping theorem gives

\[
              \check H^k(\Gamma;G)\cong \check H^k(S^n;G)
              \quad\text{for every }k\text{ and coefficient group }G.
                                                               \tag{10}
\]

This observation is useful because it prevents an imprecise ``the singular
fibers may add the missing topology'' explanation.  The *full convex
incidence resolution* adds no cohomology.  The real difficulty is that the
generic channel map ceases to be defined when ranks drop.

## 4. The generic graph and saturated channels

The generic exposed-rank theorem supplies a dense open semialgebraic set
\(U\subseteq S^n\) on which every normalized certificate has rank at least
\(q\).  Equations (3)--(4) force

\[
                   \operatorname{rank}Y=q,qquad
                   \operatorname{nul}X=q                    \tag{11}
\]

for all \(X\in\mathcal P(v)\), \(Y\in\mathcal D(v)\), \(v\in U\).

Both fibers are singletons on \(U\).  For the primal fiber, a nonzero
maximal affine chord has an endpoint on the boundary of its minimal
product-cone face, increasing total nullity beyond \(q\).  For the dual
fiber, (5) puts it in a product face of total rank \(q\); a nonzero maximal
affine chord in that face has an endpoint of rank below \(q\), contrary to
the definition of \(U\).  Thus

\[
             p^{-1}(U)=\{(v,X(v),Y(v)):v\in U\}.            \tag{12}
\]

On each top-dimensional smooth stratum, equality holds throughout the
Hermitian cross-Peirce capacity chain

\[
 n\leq a\sum_i p_iq_i
   \leq a\sum_i(r_i-q_i)q_i
   \leq a(R-1)\sum_iq_i=qB=n.                              \tag{13}
\]

Therefore every productive block has \(r_i=R\), \(q_i=1\), and
\(p_i=R-1\), and there are exactly \(q\) such blocks.  On every connected
component of \(U\), their product-block labels are constant.  The channel
lines define a semialgebraic map

\[
       \kappa_U:U\longrightarrow
       M:=\bigl(\mathbb F P^{R-1}\bigr)^q,qquad
       \dim_{\mathbb R}M=qB=n.                             \tag{14}
\]

The mixed derivative identity says that the primal and dual cross-Peirce
maps pair to the full tangent metric.  In particular, on every smooth
top-dimensional strict-complementarity stratum, the channel rotations use
all \(n\) dimensions.  This is the local source of the expected
degree obstruction.  It is not, by itself, a global degree theorem.

## 5. Switching forces a strict-complementarity branch locus

Take a sequence \(v_j\in U\) converging to \(v_0\).  Compactness gives a
subsequence

\[
          X(v_j)\to X_0\in\mathcal P(v_0),\qquad
          Y(v_j)\to Y_0\in\mathcal D(v_0).                 \tag{15}
\]

The \(q\) zero eigenvalues of \(X(v_j)\) cannot disappear in the limit, so
(3) implies

\[
                         \operatorname{nul}X_0=q.          \tag{16}
\]

By contrast, positive eigenvalues of \(Y(v_j)\) can tend to zero, so only
\(\operatorname{rank}Y_0\leq q\) is automatic.

Suppose two generic regions with different active-block patterns approach
the same support.  If both limiting certificates retained rank \(q\), their
sum would use more than \(q\) total range dimensions.  This contradicts
(5).  Hence at least one limiting pair satisfies

\[
             \boxed{\operatorname{nul}X_0=q,qquad
                    \operatorname{rank}Y_0\leq q-1.}       \tag{17}
\]

Thus a primal kernel channel persists, while its normalized dual weight
vanishes.  This is the exact strict-complementarity failure required for
label switching.

If two nonempty open pattern regions lie in different connected components
of the strict set, their common separating set in the \(n\)-sphere has
covering dimension at least \(n-1\).  Since all objects are semialgebraic,
the branch set then has a codimension-one stratum.  Therefore a putative
counterexample based on genuine label switching needs a **divisorial**
strict-complementarity failure set, not merely an isolated exceptional
support.

This conclusion is conditional on there being distinct pattern regions.
A single pattern can occupy a punctured sphere and collapse at a
nonseparating exceptional set.  Topology alone does not exclude this:
\(S^n\setminus\{p\}\cong\mathbb R^n\), and \(\mathbb R^n\) is the standard
affine cell in the equal-dimensional product \(M\).  Thus an argument based
only on invariance of domain on the generic set is incomplete.

## 6. The precise missing lemma

A sufficient closure statement is the following.

> **Ball-slack no-fold lemma (open).**  In the setting (1), a compact
> relative-Slater Hermitian-product lift whose boundary nullities are at
> most \(q\) cannot have a codimension-one locus of pairs satisfying (17),
> and its saturated channel map cannot compactify a single affine chart by
> collapsing channels over a lower-codimension exceptional set.

Equivalently, one may seek a current-theoretic version: the generic map
\(\kappa_U\) in (14) should extend through the cell-like incidence
resolution \(\Gamma\) with nonzero mod-two degree.  Such an extension would
immediately contradict (10).  Indeed, \(M\) has nonzero intermediate
cohomology (degree \(1\) for real projective factors, degree \(2\) for
complex factors, and degree \(4\) for quaternionic factors), whereas
\(\Gamma\) has the cohomology of \(S^n\).  A nonzero-degree map between
equal-dimensional compact mod-two homology manifolds injects cohomology.

The degree formulation must not be asserted without proving that the
rank-deficient locus carries no boundary current.  That is exactly where a
generic channel weight can vanish and a new projective line can enter.

## 7. Why determinant divisors and convexity do not yet prove the lemma

Along a generic branch the \(q\) active determinant factors vanish simply
in the inward primal direction.  At (17), one dual coefficient can vanish
with even or fractional Puiseux order after reparametrization.  The primal
kernel itself remains present by (16).  Affine matrix entries and
semialgebraicity do not prohibit this fold.

The compact PSD seam

\[
 X_1=\begin{pmatrix}x&0\\0&1-x\end{pmatrix},\qquad
 X_2=\begin{pmatrix}x+t&t\\t&1\end{pmatrix},
 \quad 0\leq x\leq1,\quad x+t-t^2\geq0                   \tag{18}
\]

has determinant product

\[
                         x(1-x)\,[x+t(1-t)].              \tag{19}
\]

Its restricted standard barrier has exact parameter two.  Over \(x=0\),
the fiber interval switches between its two endpoint degeneracies while
the interior has smaller nullity.  This proves that boundedness, affine
determinants, convex fibers, and the determinant-order bound all permit the
local mechanism needed at (17).  The example is not a ball lift, so it does
not refute the no-fold lemma; it shows why the global ball slack identity
must enter its proof.

## 8. Research consequence

The bounded divisible frontier is now reduced to one of two outcomes.

1. Prove the ball-slack no-fold lemma, preferably by showing that the
   cross-Peirce Jacobian has a fixed local degree and that the singular
   incidence fibers cannot absorb this degree.  This would give the sharp
   lower bound \(\nu_{\rm std,slice}\geq q+1\).
2. Construct a ball lift by globalizing (18): its generic channel map must
   occupy an affine cell of \(M\), its missing projective divisor must be
   represented by convex singular fibers, and every point of those fibers
   must retain total primal nullity at most \(q\).  Such a construction
   would disprove the grouped-barrier conjecture.

The wide-cap theorem rules out the former smallest case \(q=2\) completely,
even with arbitrary extra factors.  The smallest remaining pure-Lorentz
test is \(\mathbb F=\mathbb R\), \(R=2\), \(B=1\), \(q=3\): a compact affine
lift of \(B_2^4\) with standard parameter below four would have to globalize
the seam while satisfying the incidence constraints above.

## Audit checklist

1. Check compactness and the uniform dual bound in (7).
2. Check that the incidence fiber is exactly the product (8), hence acyclic.
3. Verify the Vietoris--Begle hypotheses and conclusion (10).
4. Check the singleton arguments on the generic rank-\(q\) locus.
5. Verify that equality in (13) forces \(q\) distinct rank-one channels in
   full order-\(R\) blocks.
6. Check the limiting-nullity direction in (16) and the range-union argument
   leading to (17).
7. Keep the no-fold statement explicitly conjectural.
