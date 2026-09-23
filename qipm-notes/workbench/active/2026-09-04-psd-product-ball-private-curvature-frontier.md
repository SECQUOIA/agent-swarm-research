# Private curvature closes every nondivisible PSD product-ball cap

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated regularity and standard-barrier scope

## Result

Let

\[
                    C=(B_2^s)^b,\qquad b\geq2,\ s\geq3,
                                                               \tag{1}
\]

and consider a strictly feasible affine lift over a product of real PSD
cones of order at most \(R\).  Assume the full extreme-row slack has
globally labelled \(C^1\) primal and dual factors, with the selected primal
boundary tuple lying in the closure of the same affine slice.  Let
\(\nu_{\rm std,slice}\) be the parameter of the standard product
log-determinant restricted to that slice.

Put

\[
                             a=R-1.
\]

Then

\[
\boxed{
 \nu_{\rm std,slice}\geq
 b\left\lceil{s-1\over a}\right\rceil+
 {\bf1}_{\,a\mid(s-1)}.}                                  \tag{2}
\]

The grouped Schur construction gives

\[
 \nu_{\rm std,slice}\leq b\left\lceil{s\over a}\right\rceil. \tag{3}
\]

Together with the independently audited divisible-case closure in
[The divisible PSD product-ball gap closes beyond the one-channel
case](2026-09-04-psd-product-ball-divisible-topclass.md) and the stronger
[all-field sequential contact-range
theorem](2026-09-04-hermitian-sequential-contact-range-frontier.md), the exact
globally selected standard-slice optimum is

\[
\boxed{
 \nu_{\rm std,slice}^{\min}
   =b\left\lceil{s\over R-1}\right\rceil.}                \tag{4}
\]

Indeed, this note closes every nondivisible residue.  If
\(s-1=q(R-1)\) with \(q\geq2\), the companion relative-top-class theorem
closes the former interval at its grouped-Schur endpoint \(b(q+1)\),
without any constant-rank assumption.  In the formerly exceptional case,
sequential compression gives

\[
                         s=R\geq3,
 \qquad \nu_{\rm std,slice}^{\min}=2b.                   \tag{5}
\]

The stronger factorization statement constructs one simultaneous contact
at which the blockwise spans of all dual contact ranges have total
dimension at least \(2b\).  It allows arbitrary switching of saturated rows
and labels; no persistent matching is assumed.

For \(R=2\), one has \(q=s-1\geq2\), so the companion theorem gives the
exact value \(bs\), consistently with the stronger Lorentz theorem for
\(\mathbb S_+^2\cong Q_3\).  Equation (2) alone is not sharp in that
divisible case.

This is a barrier-formulation theorem, not an iteration lower bound.

## Proof

Fix a simultaneous product contact
\(x\in(S^{s-1})^b\).  For PSD factor \(i\), write

\[
 E_i=\ker X_i(x),\qquad p_i=\operatorname{rank}X_i(x),
 \qquad c_i=\dim E_i.                                     \tag{6}
\]

For row \(d\), put

\[
 U_{id}=\operatorname{Ran}Y_i^d(x_d)\subseteq E_i,\qquad
 U_{i,-d}=\sum_{e\ne d}U_{ie},
 \qquad
 d_{id}=\dim {U_{id}\over U_{id}\cap U_{i,-d}}.            \tag{7}
\]

The cylindrical complementarity identities imply that the \(i\)-th
mixed-curvature channel for row \(d\) factors through the private quotient
in (7).  Hence

\[
                   \operatorname{rank}H_i^d\leq p_i d_{id}.
                                                               \tag{8}
\]

The row-\(d\) mixed slack form is the nondegenerate metric on
\(T_{x_d}S^{s-1}\), of rank \(s-1\).  Taking ranks in its decomposition
gives

\[
 s-1\leq\sum_i\operatorname{rank}H_i^d
     \leq\sum_i p_i d_{id}
     \leq a\sum_i d_{id}.
                                                               \tag{9}
\]

For the last inequality, \(d_{id}>0\) implies \(c_i\geq1\), and hence
\(p_i\leq r_i-c_i\leq R-1=a\); terms with \(d_{id}=0\) are harmless.

Thus every source row spends at least

\[
                         \sum_i d_{id}
                            \geq\left\lceil{s-1\over a}\right\rceil
                                                               \tag{10}
\]

private kernel dimensions.  For fixed \(i\), complements representing the
private quotients in (7) are jointly independent, so

\[
                             \sum_d d_{id}\leq c_i.         \tag{11}
\]

Summing (10) over sources and applying (11) yields the pointwise
nullity bound

\[
                 \sum_i c_i
                    \geq b\left\lceil{s-1\over R-1}\right\rceil.
                                                               \tag{12}
\]

Along a segment from this selected boundary tuple to an interior lift
point, the restricted product determinant vanishes to exact order
\(\sum_i c_i\).  The self-concordant gradient inequality therefore gives
the same lower bound for \(\nu_{\rm std,slice}\).

Write \(s-1=qa+r\), \(0\leq r<a\).  If \(r=0\), (12) is \(bq\) and
(2) needs one further unit.  Suppose for contradiction that
\(\nu_{\rm std,slice}<bq+1\).  The integer boundary-nullity order and
(12) force

\[
                         \sum_i c_i(x)=bq                 \tag{13}
\]

at every product contact.  Equality holds in every step of
(9)--(12).  Every productive singular block therefore has one private
direction, \(c_i=1\), \(p_i=R-1\), order \(R\), and complementary dual
rank one.  The fixed total nullity makes the \(bq\) active labels locally,
hence globally, persistent.  Their joint range map is an injective local
diffeomorphism

\[
       (S^{s-1})^b\longrightarrow
                 (\mathbb {RP}^{R-1})^{bq}.                \tag{13a}
\]

Local invertibility follows from equality in the mixed-curvature ranks;
full-slack cross-contact injectivity gives global injectivity.  This is
impossible because the source is simply connected while the target has
nontrivial fundamental group.  Thus
\(\nu_{\rm std,slice}\geq bq+1\).

If \(r>0\), (12) is already \(b(q+1)\).  For comparison, the older global
capacity correction gives

\[
 \left\lceil{b(s-1)+1\over a}\right\rceil
   =bq+\left\lceil{br+1\over a}\right\rceil
   \leq b(q+1),                                           \tag{14}
\]

because \(br+1\leq b(a-1)+1\leq ba\) for \(b\geq1\).
This proves (2).

Finally,

\[
 \left\lceil{s\over a}\right\rceil
 =\left\lceil{s-1\over a}\right\rceil
 \quad\Longleftrightarrow\quad a\nmid(s-1).               \tag{15}
\]

Equations (2), (3), and (15) prove the nondivisible part of (4).  The
divisible \(q\geq2\) part is the relative-top-class companion theorem, and
the independently audited sequential range-compression theorem proves
(5).  These cases exhaust the real PSD order caps.

## Equality structure in the divisible residue

The proof also sharply constrains the formerly hypothetical lower-endpoint
geometry.  At a contact where a source uses only \(q\) private
directions, equality holds throughout (9).  Every contributing channel
then has \(p_i=R-1\).  Since it has a nonzero private quotient,
\(c_i\geq1\), while \(p_i+c_i\leq R\); hence

\[
                         (p_i,c_i,d_{id})=(R-1,1,1).       \tag{16}
\]

Such a factor is private to exactly one source at that contact.  Thus the
former divisible question is no longer numerical curvature packing.  It is
whether globally \(C^1\) rank-\((R-1)\), nullity-one factors can switch
their source assignment so that fewer than one additional nullity
direction per source resolves all projective support obstructions.
The known codimension-one embeddings of products of spheres show that
bare support-map dimension cannot rule this out; the cylindrical
row-specific dual spaces must be used.

For \(q\geq2\), the companion theorem rules out every value below the
grouped-Schur endpoint by a closure and relative-top-class argument.  For
\(q=1\), the sequential theorem bypasses global persistence: it fixes
source contacts one at a time, quotients every PSD block by the previously
accumulated dual ranges, and uses the real one-ball sole-factor exclusion
to force two new quotient dimensions per source.  The final simultaneous
contact therefore has total nullity at least \(2b\), proving (5).

## Constant-rank precursor to the unconditional divisible closure

The following earlier argument gives a shorter closure when boundary rank
changes are excluded.  It is retained because it exposes the topology,
but the companion theorem now removes this extra hypothesis.
Assume

\[
                    s-1=q(R-1),\qquad q\geq2,              \tag{17}
\]

and assume additionally that every primal nullity
\(c_i(x)=\operatorname{nullity}X_i(x)\) is constant on the product contact
manifold.  Then

\[
\boxed{\nu_{\rm std,slice}^{\min}=b(q+1)}                 \tag{18}
\]

within this constant-boundary-rank subclass.

Here is the argument.  Suppose instead that
\(\nu_{\rm std,slice}\leq b(q+1)-1\).  Put

\[
 D_d(x)=\sum_i d_{id}(x).
\]

Equations (9)--(11) give

\[
             D_d(x)\geq q,\qquad
             \sum_dD_d(x)\leq\sum_ic_i(x)
                         \leq b(q+1)-1.                   \tag{19}
\]

Thus at every point some source \(d\) is **cleanly saturated**:
\(D_d=q\).  Equality in (9) then says that row \(d\) has exactly \(q\)
nonzero mixed channels, each of rank \(R-1\), and every corresponding
factor has

\[
                  p_i=R-1,\qquad c_i=d_{id}=1.            \tag{20}
\]

Let \(N_d(x)\) be the number of nonzero row-\(d\) mixed channels, and let
\(I_1\) be the globally fixed set of labels with constant nullity one.
The clean locus can equivalently be written

\[
 E_d=\{x:N_d(x)=q,\ H_i^d(x)=0\text{ for every }i\notin I_1\}. \tag{21}
\]

Every active locus is open and \(N_d\geq q\), so (21) is closed.  The
sets \(E_d\) cover the compact product manifold by (19).  Partition
\(E_d\) by its exact \(q\)-element active label set \(J\subseteq I_1\).
As in the Lorentz \(C^1\) cover theorem, these finitely many strata are
clopen in \(E_d\), compact, and admit pairwise disjoint neighborhoods.

On a stratum, every active order-\(R\), nullity-one support gives a phase
in \(\mathbb {RP}^{R-1}\).  Cylindrical complementarity makes its
row-\(d\) phase depend only on \(x_d\).  Equality in the channel ranks
makes the joint phase map locally diffeomorphic:

\[
 S^{q(R-1)}\dashrightarrow
                  (\mathbb {RP}^{R-1})^q.                 \tag{22}
\]

The projected phase neighborhood is proper.  If it were the whole source
sphere, compactness would make (22) a finite covering.  For \(R=2\), its
target is a \(q\)-torus and has noncompact universal cover.  For \(R\geq3\),
pass to universal covers: \((S^{R-1})^q\), with \(q\geq2\), has nonzero
intermediate cohomology and cannot be a sphere.

Therefore the top class pulled back from the \(d\)-th source sphere
vanishes on a neighborhood of \(E_d\).  The neighborhoods for
\(d=1,\ldots,b\) cover the product.  Their relative cup product would
make the product of the \(b\) source top classes vanish, contradicting
the Kunneth theorem.  This proves (18).

The relative-top-class theorem shows that rank jumps do not provide an
escape for \(q\geq2\): compact closures of the saturated label strata and
top-eigenline spectral projectors recover the same contradiction.  For
\(q=1\), the projective phase can indeed be the universal double cover, so
that proof stops.  The sequential range-compression theorem closes the case
using full-slack contact ranges rather than product cohomology.

## The \(q=1\) orientation residual

There is an exact decomposition that explains why the projective support
map alone cannot close \(s=R\).  For \(x,z\in S^{s-1}\), put
\(t=x^Tz\).  Then

\[
  1-t={1\over2}(1-t^2)+{1\over2}(1-t)^2.                 \tag{23}
\]

The first term has a single order-\(s\), nullity-one PSD factor:

\[
 X_{\rm proj}(x)=I-xx^T,\qquad
 Y_{\rm proj}(z)={1\over2}zz^T,\qquad
 \operatorname{tr}(X_{\rm proj}Y_{\rm proj})
                     ={1\over2}(1-t^2).                  \tag{24}
\]

Its support map is exactly the projective double cover
\(S^{s-1}\to\mathbb {RP}^{s-1}\), and it carries the entire rank-\((s-1)\)
mixed contact metric.  The residual

\[
                         K(x,z)={1\over2}(1-x^Tz)^2       \tag{25}
\]

is nonnegative and has zero mixed contact Hessian at \(x=z\), yet it is
what distinguishes the two orientations \(x\) and \(-x\).  Thus a
second-order curvature or support-phase proof cannot charge (25).

For \(b\) source balls, \(b\) copies of (24) spend only \(b\) nullities,
and the separate residual theorem charges another \(b\) for that canonical
split.  The sequential theorem is stronger because it does not assume such
a positive splitting.  After fixing a source contact, it compresses every
block orthogonally to the ranges already forced into its primal kernel.
The next row remains an exact one-ball factorization; contributing only one
new range dimension would give the forbidden real sole-factor equality.
Iteration forces \(2b\) range dimensions at one simultaneous contact.  Thus
(23) still explains why curvature alone was insufficient, but it no longer
leaves an open factorization gap.

## Novelty and scope

The private-quotient construction and the strict total-capacity theorem are
proved in
[PSD column packing shares full product-ball slack
rows](2026-09-04-psd-column-packing-product-balls.md).  The new step is to
retain the full rank \(s-1\) of each source metric in (9), rather than only
using its nonvanishing.  This gives a per-source private-curvature budget
and closes every nondivisible cap residue.  The separately audited
sequential theorem closes the last divisible residue \(s=R\geq3\), yielding
the exact formula (4) for every real PSD order cap in the stated class.

A targeted search for the parent PSD packing result did not locate this
product-ball private-curvature frontier in the open literature.  Novelty
is plausible subject to specialist review.  The theorem remains
conditional on globally labelled \(C^1\) full-contact selections and
concerns the restricted standard log-determinant.  It is not an
unconditional SDP extension-complexity theorem, an arbitrary coupled
barrier lower bound, or an IPM/QIPM iteration lower bound.

## Independent hostile audit

The auditor independently checked the private-quotient rank factorization,
the implication \(d_{id}>0\Rightarrow p_i\leq R-1\), the summation of
private dimensions into total primal nullity, and every residue
calculation.  It also rederived the divisibility equality case: a
hypothetical parameter below \(bq+1\) fixes all contact nullities, forces
globally persistent order-\(R\), rank-\((R-1)\) blocks, and produces the
impossible projective local diffeomorphism (13a).  The audit caught and
corrected an imprecise first-draft attribution of this \(+1\) to the
order-only capacity inequality; the equality-rigidity argument is
essential.  No correction to the original private-curvature bounds was
needed.

The final \(q=1\) closure received a separate hostile audit.  It checked the
connected-sphere reduction to one fixed rank-one dual label, the exact
order-\(s\) sole-factor contradiction, preservation of the slack identity
under orthogonal compression, and the PSD quotient-rank identity.  It also
verified that later coordinate choices preserve all previously accumulated
contact ranges.  The audit found no substantive error, so (4)--(5) now
include the one-channel case.
