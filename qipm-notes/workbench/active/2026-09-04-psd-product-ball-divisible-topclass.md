# The divisible PSD product-ball gap closes beyond the one-channel case

Status: Proved for \(q\geq2\); twice independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated regularity and standard-barrier scope

## Result

Let

\[
                 C=(B_2^s)^b,\qquad b\geq2,\quad s\geq3,
\]

and consider a strictly feasible affine lift over a finite product of real
PSD cones of order at most \(R\).  Assume that the full polar-extreme slack
has globally labelled \(C^1\) primal and dual PSD factors, and that the
entire selected primal boundary family belongs to the closure of the
affine slice on which the standard product log-determinant is restricted.
Put

\[
                         a=R-1
\]

and suppose that the formerly unresolved divisible case satisfies

\[
                         s-1=qa,\qquad q\geq2.             \tag{1}
\]

Then

\[
 \boxed{\displaystyle
       \nu_{\rm std,slice}\geq b(q+1).}                   \tag{2}
\]

The grouped Schur lift attains equality.  Consequently

\[
 \boxed{\displaystyle
       \nu_{\rm std,slice}^{\min}
          =b\left\lceil {s\over R-1}\right\rceil
          =b(q+1)\qquad(q\geq2).}                         \tag{3}
\]

Together with the previously proved nondivisible theorem, this proof
originally left only

\[
                         q=1,\qquad s=R\geq3,              \tag{4}
\]

among real PSD caps.  The independently audited
[all-field sequential contact-range theorem](2026-09-04-hermitian-sequential-contact-range-frontier.md)
now closes (4) at \(2b\).  The exception to the present top-class method
is not a defect of its rank
bookkeeping: its saturated phase map has the topologically permitted form
\(S^{R-1}\to\mathbb {RP}^{R-1}\).  The final section records precisely why
the existing even-quadratic obstruction for one ball does not automatically
exclude this map inside a product lift, and how sequential compression
bypasses the issue.

This is a standard-restricted-barrier theorem under global \(C^1\)
selection, not an arbitrary-barrier or iteration lower bound.

## 1. Private dimensions and the saturated-row cover

Write

\[
                       M=(S^{qa})^b.
\]

At a simultaneous product contact \(x\in M\), let

\[
 E_i(x)=\ker X_i(x),\qquad c_i(x)=\dim E_i(x),
 \qquad p_i(x)=\operatorname {rank}X_i(x).
\]

For source row \(d\), define

\[
 U_{id}(x)=\operatorname {Ran}Y_i^d(x_d),\qquad
 U_{i,-d}(x)=\sum_{e\ne d}U_{ie}(x),
\]

and its private quotient dimension

\[
 d_{id}(x)=\dim\frac{U_{id}(x)}
 {U_{id}(x)\cap U_{i,-d}(x)},\qquad
 D_d(x)=\sum_i d_{id}(x).                                 \tag{5}
\]

The cylindrical contact identities give the two pointwise inequalities

\[
 qa\leq\sum_i\operatorname {rank}H_i^d(x)
       \leq\sum_i p_i(x)d_{id}(x)\leq aD_d(x),             \tag{6}
\]

and

\[
                  \sum_dD_d(x)\leq\sum_ic_i(x)=:Z(x).    \tag{7}
\]

Here \(H_i^d\) is the positive-semidefinite mixed-curvature summand of
factor \(i\) in row \(d\).  In particular,

\[
                              D_d(x)\geq q.                \tag{8}
\]

Suppose for contradiction that

\[
                       \nu_{\rm std,slice}<b(q+1).         \tag{9}
\]

The determinant vanishing-order argument gives
\(\nu_{\rm std,slice}\geq Z(x)\) at every selected contact.  Since \(Z(x)\)
is integral, (9) implies

\[
                            Z(x)\leq b(q+1)-1.             \tag{10}
\]

Equations (7)--(10) show that at least one source is saturated:

\[
                             D_d(x)=q.                     \tag{11}
\]

Thus the saturated-row loci

\[
                       A_d=\{x\in M:D_d(x)=q\}            \tag{12}
\]

cover \(M\).  The dimensions in (5) need not be semicontinuous, so it
would be unjustified to call the sets \(A_d\) closed.  The closure argument
below is designed specifically to avoid that mistake.

## 2. Equality gives \(q\) private projective channels

Fix \(x\in A_d\).  Equality holds throughout (6).  Every private unit that
occurs has \(p_i=a\).  Since \(p_i+c_i\leq R=a+1\), it follows that

\[
                  (p_i,c_i,d_{id})=(a,1,1)                \tag{13}
\]

for every productive factor.  There are exactly \(q\) such factors, each
curvature form \(H_i^d(x)\) has rank \(a\), and every other
\(H_j^d(x)\) is zero.  A factor in (13) is private to row \(d\), because
its one-dimensional kernel cannot contain a second row's nonzero dual
range without destroying privacy.

For a \(q\)-element label set \(J\subseteq[L]\), let

\[
 A_{d,J}=\{x\in A_d:\{i:H_i^d(x)\ne0\}=J\}.              \tag{14}
\]

These finitely many sets partition \(A_d\).  Put

\[
                             K_{d,J}=\overline {A_{d,J}}.  \tag{15}
\]

The crucial replacement for nonexistent rank semicontinuity is the
following elementary closure fact.

**Closure lemma.**  For fixed \(d\), the nonempty compact sets \(K_{d,J}\)
are pairwise disjoint.  At every \(x\in K_{d,J}\),

\[
 \sum_{i\in J}H_i^d(x)=g_d(x),\qquad
 \operatorname {rank}H_i^d(x)=a\ (i\in J),\qquad
 H_i^d(x)=0\ (i\notin J),                                 \tag{16}
\]

where \(g_d\) is the positive-definite sphere metric in row \(d\).

*Proof.*  On \(A_{d,J}\), the corresponding identities hold by equality
in (6).  All curvature matrices are continuous because the factor maps are
\(C^1\), so the sum and zero identities pass to the closure.  Along
\(A_{d,J}\), every \(Y_i^d\), \(i\in J\), is a nonzero rank-one matrix.
Its rank cannot increase in a matrix limit.  If the limiting dual matrix
is zero, its derivative and mixed channel are zero by two-sided positivity.
Otherwise its rank is one, and complementarity with an order-at-most
\(R=a+1\) primal matrix gives
\(\operatorname {rank}H_i^d\leq\operatorname {rank}X_i\leq a\).
The sum in (16) has rank \(qa\), while it is a sum of \(q\)
positive-semidefinite matrices of rank at most \(a\).  Hence every limiting
summand still has rank \(a\).  If \(J\ne J'\), choose
\(i\in J\setminus J'\).  At a point of
\(K_{d,J}\cap K_{d,J'}\), the \(J\)-limit would give
\(\operatorname {rank}H_i^d=a\), while the \(J'\)-limit would give
\(H_i^d=0\), a contradiction.  \(\square\)

Notice that this lemma permits arbitrary rank changes, disappearing dual
factors, and shared higher-nullity blocks away from the saturated loci.
None has to be stratified.

## 3. Proper projective phase neighborhoods

For \(i\in J\) and \(x\in K_{d,J}\), the rank-one limit observation in
the closure lemma gives
\(\operatorname {rank}Y_i^d(x_d)\leq1\).  Equation (16) makes this rank
nonzero: if a two-sided \(C^1\) map into the PSD cone has value zero, its
derivative is zero, and hence its mixed-curvature channel is zero.  We
therefore have
\[
 a=\operatorname {rank}H_i^d(x)
   \leq\operatorname {rank}X_i(x)\,
          \operatorname {rank}Y_i^d(x_d).
\]
Complementarity and the order cap then force \(Y_i^d(x_d)\) to have rank
one and \(X_i(x)\) to have rank \(a\) and nullity one.  In particular,
the block order is exactly \(a+1=R\), so its kernel line belongs to
\(\mathbb {RP}^{a}\).

Rank one is not an open condition, so one should not normalize the entire
range on a neighborhood.  Instead, on the compact set
\(\pi_d(K_{d,J})\), the unique positive eigenvalue of \(Y_i^d(u)\) is
bounded uniformly away from zero.  On a sufficiently small open
neighborhood it remains separated from every other eigenvalue.  Its
\(C^1\) spectral projector defines a top-eigenline projective phase

\[
                         \phi_i^d(u)\in\mathbb {RP}^{a},
                         \qquad u=x_d.                     \tag{17}
\]

This phase depends only on \(u\), not on the remaining source coordinates.
At a rank-one PSD value, the kernel--kernel compression of \(dY_i^d\)
vanishes: every scalar function \(w^TY_i^d(u)w\), for
\(w\in\ker Y_i^d(u)\), is nonnegative and has an interior minimum zero.
Thus the derivative of the top eigenline captures exactly the off-diagonal
support derivative used by the contact-curvature channel.  The PSD
contact-curvature formula and (16) imply that the joint phase

\[
 \Phi_{d,J}=(\phi_i^d)_{i\in J}:
       P_{d,J}\longrightarrow(\mathbb {RP}^{a})^q         \tag{18}
\]

is a local diffeomorphism on some open neighborhood \(P_{d,J}\) of
\(\pi_d(K_{d,J})\) in \(S^{qa}\).  Indeed, the spectral gap and
invertibility of the joint phase differential are open conditions
depending only on \(u\); compactness supplies one common neighborhood.

The neighborhood \(P_{d,J}\) is proper.  Otherwise (18) would be a local
diffeomorphism from the compact sphere onto the connected compact target,
hence a finite covering.  If \(a=1\), the target is the \(q\)-torus, whose
universal cover is noncompact.  If \(a\geq2\), the universal cover is
\((S^a)^q\), which has nonzero intermediate cohomology when \(q\geq2\),
whereas \(S^{qa}\) does not.  Either alternative is impossible.

Let \(u\in H^{qa}(S^{qa};\mathbb R)\) be the orientation generator and
\(u_d=\pi_d^*u\).  A proper open subset of a connected closed oriented
manifold has zero ordinary top cohomology.  Therefore

\[
                       u_d|_{\pi_d^{-1}(P_{d,J})}=0.       \tag{19}
\]

## 4. Relative top-class contradiction

For each fixed \(d\), the finitely many nonempty \(K_{d,J}\) are disjoint
compact sets.  Choose pairwise disjoint open neighborhoods

\[
 K_{d,J}\subseteq W_{d,J}
       \subseteq\pi_d^{-1}(P_{d,J}),\qquad
 U_d=\coprod_JW_{d,J}.                                    \tag{20}
\]

Then \(u_d|_{U_d}=0\).  Moreover, the sets \(U_1,\ldots,U_b\) cover \(M\):
the original saturated loci cover \(M\), hence so do the unions of their
closures contained in the corresponding \(U_d\).

Lift \(u_d\) to \(H^{qa}(M,U_d;\mathbb R)\).  Their relative cup product
lies in

\[
 H^{bqa}\!\left(M,\bigcup_dU_d;\mathbb R\right)
       =H^{bqa}(M,M;\mathbb R)=0.                          \tag{21}
\]

Its image in absolute cohomology is \(u_1\smile\cdots\smile u_b\), but
the Kunneth formula says

\[
             u_1\smile\cdots\smile u_b\ne0
             \quad\hbox{in }H^{bqa}((S^{qa})^b;\mathbb R).\tag{22}
\]

This contradiction proves (2).  The usual grouped Schur lift partitions
the \(s=qa+1\) coordinates of each ball into \(q+1\) groups of size at most
\(a\), and its restricted log-determinant parameter is \(b(q+1)\).  This
proves (3).

## 5. Why the top-class proof stops at \(q=1\), and how compression closes it

When \(q=1\), the same closure proof reaches a phase map

\[
                         S^a\longrightarrow\mathbb {RP}^a.             \tag{23}
\]

It may be the universal double cover, so \(P_{d,J}=S^a\) is no longer
contradictory and the row top class need not vanish.  This is the only point
where the proof above uses \(q\geq2\).

For a *single* ball with no residual factors, the full slack forces the
complementary rank-\(a\) sheet to be an affine PSD pencil.  Homogenization
and adjugate differentiation recover the sphere coordinate as an even
quadratic function of the lifted kernel vector, contradicting the
surjectivity of the double cover.  That argument does not directly apply
to a saturated row inside a product lift.  Other blocks can be
curvature-inactive for this row on \(K_{d,J}\) yet still contribute to
off-diagonal values of its full slack.  Thus the unique active block need
not equal the entire two-variable ball slack, and the affine-pencil
reconstruction cannot discard those residual PSD terms.

This was the precise obstruction left by the top-class method.  Before the
sequential compression theorem, the two possible resolutions were:

1. prove that curvature-flat residual PSD terms cannot distinguish the two
   sheets of the projective phase cover without creating an additional
   private kernel direction somewhere; or
2. construct a globally \(C^1\) full product-slack factorization in which
   such residual terms do distinguish the sheets, thereby disproving the
   \(2b\) lower bound.

Bare topology, pointwise private-dimension counting, rank
semicontinuity, and the sole-factor even-quadratic lemma do not settle this
case directly.  The independently audited
[all-field sequential contact-range theorem](2026-09-04-hermitian-sequential-contact-range-frontier.md)
does settle it: it fixes source contacts successively, quotients each PSD
block by every earlier dual contact range, and applies the sole-factor
one-ball obstruction in the quotient.  Each row adds at least two new
range dimensions, giving total simultaneous nullity at least \(2b\).
Thus (4) is now closed at the grouped-Schur endpoint.

There is an exact scalar identity showing why curvature alone cannot
discard the residual:

\[
 1-u^Tv={1\over2}\bigl(1-(u^Tv)^2\bigr)
             +{1\over2}(1-u^Tv)^2.                       \tag{24}
\]

The first summand has the saturated order-\(R\) PSD factorization

\[
 {1\over2}\bigl(1-(u^Tv)^2\bigr)
   =\operatorname {tr}\!\left[
       (I-uu^T)\,{vv^T\over2}\right],                     \tag{25}
\]

whose phase is the universal cover \(S^{R-1}\to\mathbb {RP}^{R-1}\).
The second summand is nonnegative, positive at the other sheet \(v=-u\),
and has zero contact curvature.  Formula (24) is not by itself a capped
PSD lift with low boundary nullity: the immediate Gram representation of
the square uses the \(R+1\) features \((1,u)\), one beyond the cap.
Nevertheless, it proves that any resolution of the \(q=1\) case must use
the PSD-factor and private-nullity structure of the curvature-flat
remainder, rather than merely its sign or second-order jet.

The companion
[curvature-flat residual theorem](2026-09-04-q1-curvature-flat-residual-nullity.md)
makes this precise for the canonical split.  For all \(b\) labelled
second summands in (24), any PSD factorization with block orders at most \(s=R\)
has some simultaneous contact with total primal nullity at least \(b\).
It also needs at least
\[
 b+\left\lceil
 {b(s-1)+1\over s(s+1)/2}
 \right\rceil>b
\]
residual factors.  Therefore \(b\) separate canonical projective blocks
plus a separately factorized residual have maximum boundary nullity at
least \(2b\) and use at least \(2b+1\) capped factors.  This eliminates the
most natural counterexample architecture.  Sequential compression is
stronger because it does not require an arbitrary full-slack factorization
to admit such a positive canonical splitting.

The same companion proves a broader orientation-residual theorem and a
partial-saturation corollary.  If a set \(J\) of \(j\) source rows has
\(D_d(x)=1\) at every contact, each unique active projective label
persists.  Its full-curvature identity uniquely reconstructs the primal
matrix from \(x_d\), so its own-row term is automatically cylindrical.
Removing the \(j\) persistent labels leaves deck-separating residuals on
\(J\) and the unchanged full slacks on the other rows.  The orientation
theorem charges \(b\) remaining primal nullities, giving
\(\nu_{\rm std,slice}\geq b+j\).  For \(J=[b]\), this is \(2b\), matching
grouped Schur.  This was a useful partial result; sequential compression
now rules out the switching escape as well.

## Audit checklist

- Re-derive positivity and continuity of every mixed-curvature summand.
- Check that equality \(D_d=q\) forces exactly \(q\) order-\(R\),
  nullity-one, rank-\(a\) projective channels and zeros all other row
  curvatures.
- Stress-test the closure lemma without assuming semicontinuity of
  \(d_{id}\) or constancy of \(c_i\).
- Verify that the projective phase and its derivative depend only on the
  row coordinate on a neighborhood of the projected compact closure.
- Check the covering obstruction separately for \(a=1\) and \(a\geq2\).
- Preserve the distinction between this note's \(q\geq2\) top-class proof
  and the separate sequential theorem that resolves \(q=1\).

## Independent hostile audit

An independent auditor rederived the result conditional only on the
previously proved private-channel rank inequality and determinant
vanishing-order lemma.  It specifically checked the nonclosed
private-dimension loci.  Continuity preserves the metric-sum and zero
identities on their closures; rank-one dual matrices cannot gain rank in a
limit; a zero limiting PSD value has zero derivative; and the order cap
then bounds every limiting curvature rank by \(a\).  This verifies both
full rank of the surviving labels and disjointness of distinct label
closures without any rank-constancy assumption.

The audit also caught and checked the need for the top-eigenline spectral
projector rather than an open rank-one locus.  The compact projected
closure gives a uniform eigenvalue gap, PSD positivity zeros the
kernel--kernel derivative, and the curvature equality makes the joint
projector differential invertible.  Finally, it independently checked
both covering cases, the disjoint-neighborhood construction, and the
relative cup product.  No mathematical gap remained after the spectral
projector and exact-order clarifications.

A second hostile auditor independently rechecked the repaired closure rank
control, spectral top-eigenline extension, local phase diffeomorphism,
properness, and relative top-class contradiction.  It also returned PASS
without a further correction.
