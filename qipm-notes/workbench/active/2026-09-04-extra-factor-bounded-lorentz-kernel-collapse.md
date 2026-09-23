# Extra factors cannot evade the quotient-two bounded Lorentz barrier premium

Status: Proved and independently hostile-audited; superseded by the general
wide-cap theorem
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High; independent specialist audit still requested

## Result

The quotient-two bounded seam is impossible even with arbitrarily many
extra factors.  Let \(d\geq3\), put \(c=d-2\), and suppose

\[
                         s-1=2c.                         \tag{0}
\]

Every bounded, full-Slater affine lift of \(B_2^s\) over an arbitrary
finite product of Lorentz cones of dimensions at most \(d\) and
nonnegative rays has restricted standard product-barrier parameter

\[
                              \boxed{\nu(F)\geq3}.        \tag{0a}
\]

The grouped two-level norm lift has parameter three, so (0a) is exact.
Together with the recession-direction theorem for unbounded lifts, this
closes the full quotient-two Lorentz standard-barrier frontier.  In
particular, no compact real-PSD2 seam construction of parameter two can
project onto \(B_2^3\), regardless of how many PSD2 factors or rays it
uses.

The proof rests on a more general kernel-collapse result, which is useful
for the still-open quotients \(q\geq3\).

Let \(d\geq3\), put \(c=d-2\), and suppose

\[
                   s-1=qc,\qquad q\geq2.                 \tag{1}
\]

Consider a bounded, full-Slater affine lift of \(B_2^s\) over an
**arbitrary finite** product of Lorentz cones of dimensions at most \(d\)
and nonnegative rays.  Redundant affine-variable kernels are removed.  Let
\(F\) be the standard product Jordan log-determinant restricted to the
lifted affine slice.  If

\[
                              \nu(F)<q+1,                \tag{2}
\]

then the kernel of the homogenized projection has dimension

\[
                         \boxed{1\leq k\leq q-1}.         \tag{3}
\]

The important point is that (3) is independent of the total number of
cone factors.  Previous dimension reductions imposed the factor-count
minimality assumption.  In fact, all extra factors are interior at a
generic saturated contact, so their dimensions cancel from the
Grassmann count.

In particular, for \(q=2\), every possible bounded counterexample to the
grouped value \(q+1=3\), including one with arbitrarily many extra Lorentz
cones or rays, must have

\[
                              \boxed{k=1}.                \tag{4}
\]

Thus its homogenized fibers are at most two-dimensional cones and its
normalized fibers are points or intervals.  Before the topological
argument below, this says that a hypothetical real-PSD2 counterexample
for \(B_2^3\) would have only one scalar hidden variable after
homogenization, even if it used many cone factors.

There is also a factor-count-independent face-codimension restriction.
Let \(X\) be any lifted point over a boundary point of the ball, let \(E_X\)
be the span of its minimal product-cone face, let \(N\) be the ambient
product-cone dimension, and put

\[
                         D(X)=N-\dim E_X.                 \tag{5}
\]

Then every bounded proper lift, without assuming (2), satisfies

\[
                         \boxed{D(X)\geq qc+1=s.}         \tag{6}
\]

Consequently, under (2), if \(X\) has total Jordan nullity exactly \(q\)
and all its singular Lorentz factors have the full allowed dimension
\(d\), then the number \(z\) of zero Lorentz blocks obeys

\[
                             \boxed{zc\leq q-1}.          \tag{7}
\]

For \(q=2\) and \(c\geq2\), a saturated boundary tuple cannot contain a
zero cone block or a zero ray.  Its two singular factors must instead be
nonzero boundary rays of dimensions \(r_1,r_2\leq d\) satisfying

\[
                         r_1+r_2\geq2d-1.                \tag{8}
\]

Hence the only possibilities are dimensions \((d,d)\) or
\((d,d-1)\), up to order, and every other factor is interior.  The
real-PSD2 case \(c=1\) is exceptional: (6) still permits either one zero
\(Q_3\) block or one nonzero boundary \(Q_3\) block together with a zero
ray.  Thus vertex-based switching is confined to the smallest-capacity
case.  Interval switching through two nonzero boundary blocks is not
excluded when \(c\geq2\).

For \(q=2\), Section 4 upgrades the structural obstruction to the exact
lower bound (0a).  For \(q\geq3\), (3), (6), and (7) remain structural
reductions only.

## 1. Homogenized setup

Homogenize the compact lifted affine slice.  One obtains

\[
 C=L\cap K\ \xrightarrow{\ \Pi\ }\ Q_{s+1}=Q_{qc+2},    \tag{9}
\]

where \(K\) is the ambient product cone, \(L\) is a linear subspace, and

\[
                 \ker\Pi\cap C=\{0\}.                   \tag{10}
\]

The last property follows because the affine slice is a compact base of
\(C\): every nonzero point of \(C\) has strictly positive homogenizing
height.  Write

\[
 k=\dim\ker(\Pi|_L),\qquad
 \dim L=qc+2+k.                                          \tag{11}
\]

The segment from any lifted boundary point to a full-Slater point makes
the product determinant vanish to order equal to the total Jordan
nullity of the boundary tuple.  This order is an integer, so (2) implies

\[
       \text{every lifted boundary tuple has total nullity at most }q.
                                                                    \tag{12}
\]

## 2. Generic saturation and singleton fibers

The selection-free exposed-rank argument gives, on a dense open
semialgebraic subset of the support sphere, a genuine certificate of
total Jordan rank at least \(q\).  Complementarity and (12) force equality
throughout.  Equality in the mixed-capacity bound

\[
 qc\leq c\sum_i\operatorname{rank}_JY_i                \tag{13}
\]

has three consequences:

1. precisely \(q\) certificate blocks are nonzero boundary rays;
2. all of those blocks belong to full-size \(Q_d\) factors; and
3. every complementary primal block is a nonzero boundary ray, while
   every remaining Lorentz or ray factor is interior.

Every point in the same compact primal fiber is annihilated by the same
certificate, so it has nullity at least \(q\).  By (12), every such point
has nullity exactly \(q\).  A non-singleton compact spectrahedral fiber
contains an endpoint in a strictly smaller product-cone face than its
relative-interior points, which raises total nullity by at least one.
Therefore the generic saturated fiber is a singleton.

Let \(E\) be the span of the minimal product-cone face of this singleton.
If the ambient product cone has dimension \(N\), replacing each of the
\(q\) full \(Q_d\) factors by a ray lowers the face-span dimension by
\(d-1=c+1\).  All extra factors remain full-dimensional.  Hence

\[
                       \dim E=N-q(d-1).                  \tag{14}
\]

The homogenized inverse of the corresponding target extreme ray is also
a single ray.  Moreover

\[
                              L\cap E=\operatorname{span}\{X\}.      \tag{15}
\]

To justify the equality, take \(H\in L\cap E\).  Since \(X\) is in the
relative interior of \(K\cap E\), both \(X+\epsilon H\) and
\(X-\epsilon H\) lie in \(C\) for all sufficiently small
\(\epsilon>0\).  Their images are two-sided feasible perturbations of an
extreme ray of the target Lorentz cone, so both images remain in the span
of that ray.  Properness and singleton normalization then put both source
points on the unique inverse ray.  Thus \(H\) is proportional to \(X\).

Grassmann's inequality, (11), (14), and (15) now give

\[
  1=\dim(L\cap E)
   \geq(qc+2+k)+[N-q(d-1)]-N
   =k+2-q.                                                \tag{16}
\]

Therefore \(k\leq q-1\).

If \(k=0\), then \(\Pi|_L\) is a linear isomorphism.  Every point on the
target light quadric makes at least one pulled-back cone determinant
vanish.  The target quadratic is irreducible and its real light cone is
Zariski dense, so it divides one of the finitely many pulled-back
determinants.  A ray factor gives only a linear polynomial.  A Lorentz
factor gives a nonzero quadratic of matrix rank at most \(d\), whereas
the target determinant has matrix rank

\[
                   qc+2>d\qquad(q\geq2,c=d-2>0).         \tag{17}
\]

The two quadratics therefore cannot be proportional.  Relative Slater
excludes an identically zero pulled-back determinant.  This contradiction
proves \(k\geq1\) and completes (3).

## 3. Universal face-codimension budget

The same two-sided extreme-ray argument gives (6) without genericity or
the barrier hypothesis.  For an arbitrary \(X\) over a target extreme
ray, every direction in \(L\cap E_X\) maps into the one-dimensional span
of that ray.  Therefore

\[
                         \dim(L\cap E_X)\leq k+1.         \tag{18}
\]

On the other hand, Grassmann's inequality gives

\[
 \dim(L\cap E_X)
 \geq(qc+2+k)+(N-D(X))-N
 =qc+2+k-D(X).                                           \tag{19}
\]

Combining (18) and (19) yields \(D(X)\geq qc+1\).

For reference, the contribution of one factor to \(D(X)\) is

\[
\begin{array}{c|c}
\text{state of a }Q_r\text{ factor}&\text{face codimension}\\ \hline
\text{interior}&0\\
\text{nonzero boundary ray}&r-1\\
\text{zero block}&r
\end{array}
\qquad
\begin{array}{c|c}
\text{state of a nonnegative ray}&\text{face codimension}\\ \hline
\text{positive}&0\\
\text{zero}&1.
\end{array}                                               \tag{20}
\]

If a nullity-\(q\) tuple has \(z\) zero full-size Lorentz blocks and all
other singular blocks are nonzero boundary points of full-size factors,
then there are \(q-2z\) such boundary blocks and

\[
 D(X)=z d+(q-2z)(d-1)
     =q(c+1)-zc.                                         \tag{21}
\]

Substitution into (6) gives (7).

For \(q=2\), \(c\geq2\), the possible total-nullity-two patterns can be
read directly from (20).  A zero \(Q_r\) factor gives
\(D(X)=r\leq d=c+2<2c+1\), and a zero ray plus one nonzero boundary
\(Q_r\) gives \(D(X)=r\leq d<2c+1\).  Both contradict (6).  The remaining
two-zero-ray pattern has \(D(X)=2<2c+1\) and is impossible as well.  Thus
there are two nonzero boundary Lorentz factors and

\[
 (r_1-1)+(r_2-1)=D(X)\geq2c+1=2d-3,
\]

which is exactly (8).

## 4. Quotient two: label switching is impossible

Assume \(q=2\) and, toward a contradiction, \(\nu(F)<3\).  Equation
(12) says that every tuple over the boundary sphere has total nullity at
most two.  Equation (6), now \(D(X)\geq2c+1\), excludes nullity zero and
nullity one.  Indeed, a nullity-one tuple has either one nonzero boundary
\(Q_r\) block, of face codimension

\[
                         r-1\leq d-1=c+1<2c+1,
\]

or one zero nonnegative ray, of face codimension one.  Thus

\[
 \boxed{\text{every point in every boundary fiber has total nullity two}.}
                                                               \tag{22}
\]

Every boundary fiber is a singleton.  Otherwise, start at a
relative-interior point of the compact fiber and move along a nonzero
fiber direction to an endpoint.  The endpoint must leave the relative
interior of the same product-cone face, so its total nullity strictly
increases, contradicting (22).  Denote the unique normalized lift over
\(v\in S^{2c}\) by \(X(v)\).  Compactness and the closed graph property
make

\[
                         v\longmapsto X(v)                \tag{23}
\]

continuous.

On a dense open semialgebraic subset, generic saturation from Section 2
says that exactly two full \(Q_d\) blocks are nonzero boundary rays and
all other factors are interior.  There are only finitely many unordered
label pairs.  Fix one pair \(\{i,j\}\) occurring on a generic stratum and
take a sequence in that stratum converging to any point in its closure.
Continuity and closedness of the cone boundary keep blocks \(i,j\)
singular.  Neither can converge to zero, because that would contribute
nullity two while the other still contributes at least one.  No
additional factor can become singular, since that would give total
nullity at least three.  Hence the closure retains exactly the same two
nonzero boundary labels.

Closures belonging to distinct label pairs are disjoint: a point in two
such closures would have at least three nonzero boundary blocks.  The
finite union of these closures covers \(S^{2c}\), because the generic
strata are dense.  Since the sphere is connected, only one label pair
can occur.  Therefore there are fixed full-size factors \(i,j\) such
that, for every \(v\in S^{2c}\),

\[
 X_i(v),X_j(v)\text{ are nonzero boundary rays, and every other block
 is interior}.                                           \tag{24}
\]

Normalize the two Lorentz ray directions.  Equation (24) and continuity
give a map

\[
             \phi:S^{2c}\longrightarrow S^c\times S^c.  \tag{25}
\]

This map is injective.  If \(\phi(v)=\phi(w)\), then \(X(v)\) and \(X(w)\)
lie in the relative interior of the same product-cone face span \(E\).
For either point, the singleton-fiber two-sided argument used in (15)
gives

\[
                            L\cap E=\operatorname{span}\{X(v)\}.
                                                               \tag{26}
\]

Thus \(X(w)\) is proportional to \(X(v)\).  Both have homogenizing height
one, so they are equal and \(v=w\).

The domain and target of (25) are compact connected manifolds of the same
dimension \(2c\).  Invariance of domain makes the image of the continuous
injection open; compactness makes it closed.  Hence (25) would be a
homeomorphism

\[
                            S^{2c}\cong S^c\times S^c,
\]

contradicting

\[
 H^c(S^{2c};\mathbb Z)=0,\qquad
 H^c(S^c\times S^c;\mathbb Z)\ne0.                       \tag{27}
\]

This contradiction proves (0a).  Notice that the proof also covers
\(c=1\): although the face-codimension budget alone permits isolated
zero-block patterns at total nullity two, no such pattern can lie in the
closure of a generic two-ray pattern without violating (22), and the
finite generic closures cover the entire sphere.

## 5. Why the local seam model does not globalize

For real PSD2 factors (\(Q_3\)), \(q=2\), and target \(B_2^3\), the kernel
reduction first forces any putative parameter-two construction to satisfy

\[
 \dim L=5,\qquad \dim\ker(\Pi|_L)=1.                    \tag{28}
\]

The compact local model

\[
  X_1=\begin{pmatrix}x&0\\0&1-x\end{pmatrix},\qquad
  X_2=\begin{pmatrix}x+t&t\\t&1\end{pmatrix},            \tag{29}
\]

has determinant product

\[
                         x(1-x)[x+t(1-t)]                \tag{30}
\]

and shows that interval switching is locally compatible with total
nullity two.  The global proof in Section 4 explains why it nevertheless
cannot occur over the ball sphere: every boundary fiber is a singleton
before a label can switch.  Thus the local model is a genuine warning
against purely local determinant arguments, but it is not extendable to
a lift of \(B_2^3\).

## Audit checklist

1. Verify that determinant order implies (12) for every point of every
   boundary fiber.
2. Recheck equality in the generic mixed-capacity estimate, including
   the exclusion of lower-dimensional active factors and zero/ray blocks.
3. Verify singleton generic fibers using compactness and the endpoint
   nullity increase.
4. Check the two-sided argument proving (15), including normalization of
   the homogenized inverse ray.
5. Check the irreducible-light-quadric argument excluding \(k=0\).
6. Verify the universal codimension budget (6) and the pattern arithmetic
   in (7)--(8).
7. For \(q=2\), verify (22), singleton continuity, disjointness of the
   finitely many generic-pattern closures, and injectivity of (25).

## Independent hostile audit and supersession

The audit verified the determinant-order bound on every point of every
boundary fiber, the universal face-codimension estimate, and the complete
classification of the \(q=2\) equality pattern.  In particular, total
nullity is exactly two; compact boundary fibers are singletons; the
singleton field is continuous; closures of distinct generic active pairs
cannot meet; and the resulting map
\(S^{2c}\to S^c\times S^c\) is an impossible continuous injection between
compact manifolds of equal dimension.  The local switching model in (29)
does not evade this global argument.  The audit returned **PASS**.

The later
[arbitrary-factor wide-cap theorem](2026-09-04-arbitrary-factor-q2-lorentz-barrier-rigidity.md)
extends the same conclusion from \(q=2\) to every
\(c=d-2\ge q-1\).  This note is retained as the more detailed quotient-two
precursor, not as the current frontier statement.
