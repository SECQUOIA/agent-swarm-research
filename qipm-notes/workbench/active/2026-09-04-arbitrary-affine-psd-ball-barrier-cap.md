# Arbitrary affine PSD ball lifts: the cap frontier is proved off the divisible seam

Status: Partial theorems proved and independently hostile-audited;
bounded divisible multi-channel case open  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for Theorem 1, Lemma 2, and the escape example; conjectural statements are labelled

## Question and present answer

Let an exact finite affine lift of the Euclidean ball \(B_2^N\) use real
PSD blocks of orders \(r_i\leq R\), and assume relative Slater after the
usual minimal-face reduction.  Let

\[
                 F(X)=-\sum_i\log\det X_i                 \tag{1}
\]

be the standard product log-determinant restricted to the lifted affine
slice.  The selection-free cap conjecture is

\[
 \nu(F)\ \geq\ \left\lceil {N\over R-1}\right\rceil,      \tag{2}
\]

apart from the direct \(2\times2\) trace-one representation of \(B_2^2\),
which has parameter one.

The following part of (2) does not require compact primal fibers, a
continuous selection, or a proper homogenization.

> **Theorem 1 (all nondivisible cases, and the first divisible case).**
> For every such affine lift,
> \[
> \boxed{\displaystyle
> \nu(F)\geq\left\lceil {N-1\over R-1}\right\rceil.}       \tag{3}
> \]
> Consequently (2) holds whenever \(R-1\nmid N-1\).  It also holds when
> \(N=R\geq3\), by the intrinsic convex-certificate-fiber theorem.  Thus
> the only unresolved regime is
> \[
>                    N-1=q(R-1),\qquad q\geq2.             \tag{4}
> \]
> Even in (4), the conjecture holds whenever the lifted affine
> spectrahedron has a nonzero recession direction.  Hence a counterexample
> must have a bounded total lifted feasible set.

The norm-tree examples show why an exposed-dual-rank proof cannot settle
(4): a rank-one dual channel can disappear at a seam while the associated
primal block becomes zero and pays two units of nullity.  They do not
contradict (2).  No proof or counterexample for (4) is claimed here.

## 1. Compact dual fibers and possibly noncompact primal fibers

Write the reduced lift as

\[
 \mathcal A(x,y)=\mathcal A_0+\sum_{j=1}^N x_j\mathcal A_j
                         +\sum_\ell y_\ell\mathcal B_\ell\in
 K:=\prod_i\mathbb S_+^{r_i}.                             \tag{5}
\]

Choose a relative-Slater lift \(X^\circ=\mathcal A(0,y^\circ)\succ0\)
of the origin.  For \(v\in S^{N-1}\), SDP duality gives a nonempty fiber

\[
 \mathcal D(v)=\{Y\in K:\ \mathcal B^*Y=0,
       \ \langle\mathcal A_j,Y\rangle=-v_j,
       \ \langle\mathcal A_0,Y\rangle=1\}.               \tag{6}
\]

Every \(Y\in\mathcal D(v)\) and every primal lift \(X(x)\) obey

\[
                         \langle X(x),Y\rangle=1-x^Tv.    \tag{7}
\]

Moreover \(\langle X^\circ,Y\rangle=1\).  Positive definiteness of
\(X^\circ\) makes the union of the fibers in (6) bounded.  Their graph is
closed, so it is compact and semialgebraic.  In contrast, the primal
fibers need not be compact or even admit a locally bounded selection; see
Section 5.

The primal graph over the sphere and the dual graph (6) are nevertheless
semialgebraic.  Semialgebraic choice followed by a finite \(C^1\)
stratification supplies primal and dual selections \(X(u)\) and \(Y(v)\)
that are \(C^1\) on a common dense semialgebraic open subset
\(U\subset S^{N-1}\).
No behavior at the boundary of \(U\) is used below.  Equation (7) holds for
all \(u,v\in U\).

## 2. Local curvature proves (3)

Fix \(v\in U\), and put

\[
 p_i=\operatorname {rank}X_i(v),\qquad
 q_i=\operatorname {rank}Y_i(v),\qquad
 c_i=\operatorname {nullity}X_i(v).                       \tag{8}
\]

At diagonal contact, (7) and blockwise nonnegativity give
\(X_i(v)Y_i(v)=0\), hence \(q_i\leq c_i\) and
\(p_i+q_i\leq r_i\).  Mixed differentiation of (7) on the two copies of
the sphere gives the negative Euclidean tangent pairing.  In bases adapted
to the complementary ranges, the contribution of block \(i\) factors
through the real \(p_i\times q_i\) off-diagonal block.  Therefore

\[
 \begin{split}
 N-1
 &\leq\sum_i p_iq_i
 \leq\sum_i (r_i-q_i)q_i\\
 &\leq (R-1)\sum_iq_i
 \leq (R-1)\sum_i c_i .                                  \tag{9}
 \end{split}
\]

Thus the selected boundary tuple has total nullity at least the right-hand
side of (3).  Join it to \(X^\circ\) inside the affine slice.  Along this
segment, \(\prod_i\det X_i\) vanishes to order exactly
\(c=\sum_i c_i\), so

\[
 F(\tau)=-c\log\tau+O(1),\quad
 F'(\tau)=-c/\tau+O(1),\quad
 F''(\tau)=c/\tau^2+O(1).                                \tag{10}
\]

The barrier-gradient inequality \(|F'|^2\leq\nu F''\) implies
\(\nu\geq c\), proving (3).  If \(R-1\nmid N-1\), the two ceilings
\(\lceil(N-1)/(R-1)\rceil\) and \(\lceil N/(R-1)\rceil\) coincide.

When \(N=R\geq3\), (9) gives only one.  The whole-fiber theorem in
[Affine PSD lifts need no selected contact sheets in the real one-channel
regime](2026-09-04-affine-psd-sequential-compression-without-selections.md)
shows that some support certificate has total rank at least two.  Its range
annihilates every primal lift over the contact, so every such lift has
total nullity at least two.  This proves (2) for the remaining case \(q=1\).
For \(N=R=2\), the direct \(Q_3\cong\mathbb S_+^2\) slice is the stated
exception.

## 3. A recession direction supplies the missing unit

The apparent noncompact escape can be excluded by a two-scale barrier
argument.

> **Lemma 2 (recession rank plus compressed boundary nullity).**  Let
> \(D=(D_i)\ne0\) be a recession direction of a relative-Slater affine PSD
> slice, and let \(\bar X\) be a boundary point of the same slice.  Put
> \[
> W_i=\operatorname {Ran}D_i,\quad
> d=\sum_i\dim W_i,\quad
> C_i=P_{W_i^\perp}\bar X_iP_{W_i^\perp},\quad
> c=\sum_i\operatorname {nullity}_{W_i^\perp}C_i.          \tag{11}
> \]
> Then
> \[
>                         \boxed{\nu(F)\geq d+c.}           \tag{12}
> \]

To prove the lemma, restrict \(F\) to the affine two-plane

\[
 X(s,t)=(1-s)\bar X+sX^\circ+tD,\qquad s>0,\ t\geq0.       \tag{13}
\]

In a basis adapted to \(W_i\), blockwise Schur complementation, first as
\(t\to\infty\) and then as \(s\downarrow0\), gives

\[
 \det X_i(s,t)
 =t^{\operatorname {rank}D_i}
  s^{\operatorname {nullity}C_i}\bigl(\gamma_i+o(1)\bigr),
 \qquad \gamma_i>0.                                      \tag{14}
\]

More explicitly, for fixed \(s>0\), the restriction \(f(s,t)=F(X(s,t))\)
has the \(C^2\) expansion
\[
 f(s,t)=-d\log t+g(s)+O_s(t^{-1}).
\]
The \(t\)-channel contributes \(d\) to the squared dual gradient norm and
its Hessian cross term with \(s\) vanishes in the limit.  If \(c>0\), then
\[
 g(s)=-c\log s+O(1),\qquad
 {g'(s)^2\over g''(s)}\longrightarrow c
                       \quad(s\downarrow0).
\]
Taking first \(t\to\infty\) and then \(s\downarrow0\) makes the two
singular contributions add.  If \(c=0\), the \(t\)-channel alone gives
the required lower bound \(d=d+c\); a nonsingular \(s\)-channel may add
more.  Thus the restricted squared dual gradient norm has liminf at least
\(d+c\), proving (12).

If \(Y\) is a genuine support certificate complementary to \(\bar X\),
then \(D\) is an admissible recession direction in the certificate
identity, so \(\langle D,Y\rangle=0\).  Blockwise PSD nonnegativity gives

\[
 \operatorname {Ran}Y_i\subseteq
 W_i^\perp\cap\ker\bar X_i,
 \qquad
 c\geq\sum_i\operatorname {rank}Y_i.                      \tag{15}
\]

At a generic contact from Section 2, the selected certificate has total
rank at least \(\lceil(N-1)/(R-1)\rceil\).  If (4) holds, this rank is at
least \(q\).  Every nonzero \(D\) has \(d\geq1\), and (12)--(15) yield

\[
                            \nu(F)\geq q+1.                \tag{16}
\]

Thus the cap conjecture holds for every unbounded lift in the remaining
divisible regime.  A nonempty closed convex set in finite dimensions is
unbounded only if it has a nonzero recession direction.  Since the
projected ball is compact, a lift with zero recession cone has a bounded
total feasible set.  The sole unresolved case is therefore a bounded
lift; noncompact primal fibers are not a viable counterexample mechanism.

## 4. What a counterexample in the remaining regime must do

Assume (4) and suppose, toward a counterexample, that every boundary lift
tuple has total nullity at most \(q\).  On every full-dimensional \(C^1\)
selection stratum, all inequalities in (9) are equalities.  Consequently:

- the selected primal tuple has total nullity exactly \(q\);
- exactly \(q\) dual rank units are present;
- every active block has order \(R\), primal rank \(R-1\), primal
  nullity one, and dual rank one; and
- the \(q\) off-diagonal channels jointly have full tangent rank
  \(q(R-1)=N-1\).

After fixing the active labels on a connected stratum, their kernel/range
lines therefore define a local diffeomorphism

\[
 U\longrightarrow(\mathbb {RP}^{R-1})^q.                 \tag{17}
\]

Boundedness gives one further global fact.  Let

\[
 \mathscr P_q=\{(v,X):v\in S^{N-1},\ X\text{ lies over }v,\ 
                    \sum_i\operatorname {nullity}X_i\geq q\}.        \tag{18}
\]

This is a compact semialgebraic set.  Section 2 shows that its projection
contains a dense open subset of the sphere.  Its projection is also compact
and hence closed, so it is the whole sphere.  Under the counterexample
assumption, every support direction therefore has at least one lifted tuple
of total nullity exactly \(q\).  Thus a seam cannot be covered only by
lower-nullity tuples; it must carry one or more saturated \(q\)-nullity
branches.

This is the exact local normal form.  Under global \(C^1\) selections,
(17) extends to a finite covering of the compact sphere and gives the known
topological contradiction.  Without selections, the only possible escape
is at lower-dimensional seams: rank-one certificate weights can vanish,
active labels can change, and different compact primal branches can meet
over the same projected support.  Convexity of a dual fiber forces the
union of all its range
spaces to have total dimension at most \(q\), but that span can lose
dimension when a certificate weight tends to zero.  Closed graph supplies
outer, not inner, semicontinuity.

Hence a counterexample to (2), if one exists, must simultaneously realize
all of the following:

1. the saturated projective chart (17) on a dense open set;
2. only \(q\) total primal nullity in **every** boundary fiber;
3. disappearance and rebirth of projective channels at seams without a
   zero block or an additional singular block; and
4. compact projection-singular branching in the primal fiber, so that
   distinct limiting tuples retain different kernel configurations while
   the common dual span drops.

Binary and balanced norm trees satisfy item 1 but fail items 2--3: at a
channel-death seam a scaled PSD block becomes zero, increasing total
nullity by exactly the missing unit.  This is evidence for (2), not a
proof.

For \(R=2\), the later
[rotated-perspective construction](2026-09-04-rotated-lorentz-fiberwise-nullity-counterexample.md)
shows that no proof can strengthen item 2 to a statement about the
*minimum* nullity in each fiber.  Its compact north-pole simplex contains
a completion of nullity \(q=N-1\), as does every other boundary fiber.
Nevertheless, the simplex vertices have nullity \(2q-1\), and the
restricted standard barrier has exact parameter \(2q-1\).  Thus the
standard-barrier conjecture can only require the existence of one
high-nullity tuple; it cannot require every completion over one support
to pay even \(q+1\).

## 5. Relative Slater alone does not give bounded boundary selections

The warning about escape is substantive.  The following exact affine PSD
lift projects onto \(B_2^2\) and has relative Slater, yet no primal
selection is locally bounded at \(e_1=(1,0)\).  Put
\(\delta=1-x_1\) and impose

\[
 \begin{pmatrix}1+x_1&x_2\\x_2&1-x_1\end{pmatrix}\succeq0,
 \qquad
 \begin{pmatrix}\delta&x_2\\x_2&u\end{pmatrix}\succeq0,
 \qquad
 \begin{pmatrix}\delta&u\\u&z-1\end{pmatrix}\succeq0.  \tag{19}
\]

The first block is exactly the disk.  For \(\delta>0\), the other two
blocks are feasible precisely when one can choose

\[
                 u\geq{x_2^2\over\delta},\qquad
                 z\geq1+{u^2\over\delta}.                \tag{20}
\]

At \(e_1\), they force \(u=0\) and permit \(z\geq1\).  On the circular
boundary \(x_1=1-\delta\), however,
\(x_2^2=2\delta-\delta^2\), so every feasible lift satisfies

\[
 u\geq2-\delta,\qquad
 z\geq1+{(2-\delta)^2\over\delta}\longrightarrow\infty. \tag{21}
\]

At \(x=0\), choices \(u>0\) and sufficiently large \(z\) make all three
blocks positive definite, so relative Slater holds.  Thus compactness of
the target and relative Slater by themselves do **not** justify a
compact-boundary-fiber or locally bounded-selection step.  Lemma 2 shows,
however, that such escape already raises the standard barrier parameter
enough for the conjecture.  A proof of the remaining bounded case must use
the compact primal/dual incidences or another invariant.

## 6. Attainment and research target

Grouped Schur blocks of width at most \(R-1\), with a single equation
summing their epigraph variables to one, attain parameter
\(\lceil N/(R-1)\rceil\).  Thus a proof of (2) in (4) would give the exact
standard-product-barrier frontier for **all** finite affine real-PSD lifts,
with no regularity assumption on contact sheets.

One strong sufficient statement for the unresolved case can be phrased
without barriers:

> If \(N-1=q(R-1)\) with \(q\geq2\), must some boundary fiber of every
> exact relative-Slater affine \(\prod_i\mathbb S_+^{r_i}\)-lift of
> \(B_2^N\), \(r_i\leq R\), contain a tuple with total nullity at least
> \(q+1\)?

An affirmative answer would settle the barrier conjecture by boundary
vanishing order.  A negative answer would not by itself refute the barrier
conjecture, because the global gradient norm can exceed every single
boundary determinant order.

The present work proves the generic value \(q\), identifies the saturated
local geometry, proves the \(q=1\) endpoint, and excludes every lift with a
nonzero recession direction.  It isolates compact projection-singular
branching as the remaining obstruction.  It does not claim that this
obstruction can or cannot occur.

## 7. Targeted literature boundary (2026-09-04)

Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone Factorizations*](https://doi.org/10.1287/moor.1120.0575),
provide the general lift/slack-factorization theorem and the convex dual
certificate fibers used in Section 1.  Fawzi and Parrilo,
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite
Extension Complexity*](https://arxiv.org/abs/1311.2571), prove strong
lower bounds for products of fixed-order PSD cones, but their invariant is
the number of factors needed for selected finite slack matrices, not the
gradient parameter of the product log-determinant after affine
restriction.  Fawzi's
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://doi.org/10.1007/s10107-018-1233-0) similarly studies global
SOC factor count and cone-factorization obstructions.  The 2026
Lorentz-factorization paper of Aubrun, La Piana, and Müller-Hermes,
[*Factorization through Lorentz cones*](https://arxiv.org/abs/2606.27825),
concerns factorization of positive maps through direct sums of Lorentz
cones, not restricted barriers or boundary nullity.

Targeted primary-source searches found no theorem combining a block-order
cap, generic support curvature, boundary determinant order, and a
recession-rank contribution to prove (3), (12), or (16).  No source was
located that settles the bounded branching problem in Section 6.  The safe
label is **candidate partial cap theorem and recession reduction; full
selection-free divisible frontier open**.  This is not an exhaustive
novelty or priority claim.

## Independent hostile audit

The audit rechecked the generic semialgebraic primal/dual selections,
the \(p_iq_i\) mixed-channel bound, and the determinant-order passage from
one selected boundary tuple to \(\nu(F)\), proving Theorem 1.

For Lemma 2, in a basis adapted to \(\operatorname {Ran}D_i\), the
positive part of \(D_i\) supplies exactly
\(\operatorname {rank}D_i\) powers of \(t\).  Schur complementation then
leaves the compression of \(\bar X_i\) to
\(\operatorname {Ran}D_i^\perp\), whose nullity supplies exactly the
stated powers of \(s\).  The iterated \(C^2\) expansion above makes the
two singular gradient/Hessian channels asymptotically orthogonal and
gives the additive constant \(d+c\).  Complementarity with a genuine
support certificate puts its range in both \(\ker D_i\) and
\(\ker\bar X_i\), proving (15).

Finally, a nonempty closed finite-dimensional spectrahedron is unbounded
exactly when it has a nonzero recession direction, after removing
redundant affine-variable kernels.  Hence (16) closes every unbounded
lift in the divisible regime.  The escape example was checked directly
and confirms that relative Slater alone does not give locally bounded
boundary selections.  No claim about the remaining bounded branching
case was introduced.
