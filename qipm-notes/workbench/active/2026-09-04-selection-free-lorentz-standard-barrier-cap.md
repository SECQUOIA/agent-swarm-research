# Selection-free Lorentz standard-barrier frontier off the bounded divisible seam

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the proved regimes; bounded divisible case open;
targeted literature screen complete

## Result

Let \(B_2^s\), \(s\geq2\), have a finite affine lift over a product of
Lorentz cones of dimensions at most \(d\geq3\) and rays.  Reduce once to
the minimal face and assume relative Slater.  Put

\[
 p=s-1,\qquad c=d-2,\qquad
 q=\left\lceil{p\over c}\right\rceil .                    \tag{1}
\]

Let \(F\) be the standard product Jordan log-determinant restricted to the
lifted affine slice.  Then every such lift satisfies

\[
                         \boxed{\nu(F)\geq q.}             \tag{2}
\]

The grouped Lorentz lift has exact restricted parameter

\[
 h_d(s)=
 \begin{cases}
  1,&d\geq s+1,\\
  \lceil s/(d-2)\rceil,&d<s+1.
 \end{cases}                                               \tag{3}
\]

Consequently (2) is the exact unrestricted affine-lift frontier whenever
\(d-2\nmid s-1\).  In the only gap regime

\[
             d<s+1,\qquad s-1=q(d-2),\qquad q\geq2,       \tag{4}
\]

one has \(h_d(s)=q+1\).  The stronger lower bound
\(\nu(F)\geq q+1\) holds for every lift whose total lifted feasible set is
unbounded.  Thus the sole open case is a bounded affine lift in the
divisible regime (4).

There is one further exact bounded result.  If (q=2) and the lift uses
exactly the two capacity-minimal factors (Q_d\times Q_d), then
\(\nu(F)=3=q+1\).  This is the independently audited
[two-factor compact rigidity theorem](2026-09-04-two-lorentz-factor-compact-ball-barrier-rigidity.md).
Accordingly, any quotient-two counterexample must use additional Lorentz
factors or rays and switch its two productive channels between labels.

This theorem has no global contact-selection assumption.  It is about the
specified restricted standard product barrier, not arbitrary barriers and
not unrestricted QIPM iteration complexity.

## 1. Generic curvature proves the universal value (q)

All fibers of a finite affine Lorentz lift are semialgebraic.  Choose a
primal lift over every boundary contact and a minimum-total-Jordan-rank
genuine support certificate.  Semialgebraic choice and a common finite
stratification make both selections \(C^1\) on a dense open subset of
\(S^{s-1}\).  On any full-dimensional stratum, mixed differentiation of

\[
               \sum_i\langle X_i(u),Y_i(v)\rangle=1-u^Tv \tag{5}
\]

has tangent rank \(p=s-1\).  A nonzero complementary Lorentz boundary
pair has one Jordan rank unit and cross-Peirce dimension at most
\(d-2=c\); an interior dual block or a ray has zero mixed capacity.
Therefore the selected certificate and primal tuple obey

\[
 p\leq c\sum_i\operatorname{rank}_JY_i
   \leq c\sum_i\operatorname{nullity}_JX_i.               \tag{6}
\]

Join this boundary tuple to a relative-Slater point.  Along the segment,
the product Jordan determinant vanishes to order exactly
\(z=\sum_i\operatorname{nullity}_JX_i\).  Restricting the barrier-gradient
inequality to this line gives \(\nu(F)\geq z\geq q\), proving (2).

If \(c\nmid p\), then
\(\lceil p/c\rceil=\lceil(p+1)/c\rceil=h_d(s)\) in the capped regime, so
the grouped construction proves exactness.  If \(d\geq s+1\), the direct
Lorentz slice has parameter one.

## 2. A recession direction supplies the divisible missing unit

The following symmetric-cone form of the two-scale determinant lemma is
the only extra ingredient.

> **Lemma 1.**  Let \(D\ne0\) be a recession direction of a
> relative-Slater affine product-Lorentz slice, and let \(\bar X\) be a
> boundary point.  In factor \(i\), let \(f_i\) be the complementary face
> to the support idempotent of \(D_i\), and let \(C_i\) be the Peirce
> compression of \(\bar X_i\) to \(f_i\).  Put
> \[
>  r=\sum_i\operatorname{rank}_JD_i,
>  \qquad z=\sum_i\operatorname{nullity}_{J,f_i}C_i .      \tag{7}
> \]
> Then
> \[
>                              \boxed{\nu(F)\geq r+z.}     \tag{8}
> \]

Indeed, restrict the barrier to

\[
 X(\sigma,t)=(1-\sigma)\bar X+\sigma X^\circ+tD,
 \qquad \sigma>0, t\geq0.                                \tag{9}
\]

For fixed \(\sigma>0\), spectral decomposition and Schur--Peirce
complementation give

\[
 F(X(\sigma,t))=-r\log t+g(\sigma)+O_\sigma(t^{-1}).      \tag{10}
\]

After \(t\to\infty\), the remaining determinant is that of the
compression to \(f_i\); hence

\[
 g(\sigma)=-z\log\sigma+O(1).                             \tag{11}
\]

The mixed \((t,\sigma)\) Hessian entry vanishes in the iterated limit.
The two one-dimensional gradient/Hessian quotients therefore contribute
\(r\) and \(z\) additively, which proves (8).  For a Lorentz factor this
can also be checked directly from its quadratic determinant: an interior
recession component contributes two powers of \(t\), a nonzero boundary
component contributes one, and the complementary face is respectively
zero or the opposite boundary ray.

Now choose the generic contact and genuine certificate \(Y\) from Section
1.  The certificate identity holds along every recession direction, so
\(\langle D,Y\rangle=0\).  Termwise cone positivity puts \(Y_i\) in the
face complementary to \(D_i\), and complementarity with \(\bar X_i\)
gives

\[
 z\geq\sum_i\operatorname{rank}_JY_i\geq q.              \tag{12}
\]

Since \(D\ne0\), \(r\geq1\).  Lemma 1 yields
\(\nu(F)\geq q+1=h_d(s)\) in (4).

A closed finite-dimensional lifted spectrahedron is unbounded exactly
when it has a nonzero recession direction, after quotienting redundant
affine-variable kernels.  Hence only bounded total lifted sets remain.

## 3. Sharp scope of the remaining problem

In the bounded divisible regime, assume hypothetically that \(\nu(F)\leq
q\).  Every boundary tuple then has total Jordan nullity at most \(q\),
because its segment to Slater has determinant order equal to that nullity.
On the dense regular contact strata, all inequalities in (6) must be
equalities: exactly \(q\) full-capacity rank-one Lorentz channels carry
the tangent metric.  Their phase map is a local diffeomorphism to a
product of \(q\) spheres \(S^c\).

Compactness gives a sharper fiber dichotomy.  If a compact spectrahedral
fiber \(\mathcal P(v)=K\cap A_v\) is non-singleton and its minimum total
Jordan nullity is \(r\), then it contains a point of nullity at least
\(r+1\).  Indeed, a relative-interior point of the fiber lies in the
relative interior of the smallest product-cone face containing the fiber
and has the minimum nullity \(r\).  Move from it along any nonzero direction
in the affine hull until reaching an endpoint.  If the endpoint remained
in the relative interior of the same cone face, the line could be extended,
contradicting maximality.  At least one Lorentz eigenvalue therefore
vanishes, increasing total nullity.

It follows that under the hypothetical bound \(\nu(F)\leq q\), every
boundary fiber whose minimum nullity is already \(q\) must be a singleton.
In particular, the generic saturated fibers above are unique.  Any
projection-singular seam capable of evading the bound must first drop its
minimum fiber nullity to at most \(q-1\), then glue the unique generic
branches through a higher-dimensional fiber without creating a tuple of
nullity \(q+1\).  This is stricter than arbitrary branched-cover behavior.

This local map need not extend as an unbranched covering.  Certificate
weights can vanish at lower-dimensional seams, and compact convex primal
fibers can contain several limiting saturated branches.  The
[PSD2 seam note](2026-09-04-selection-free-psd2-nullity-seam-obstruction.md)
gives an algebraic branched-cover obstruction and an exact compact
full-Slater example showing that boundary contact accessibility is not
automatic.  Thus no bounded divisible theorem is claimed here.

The two-factor rigidity theorem closes this seam when \(q=2\) and no
extra factors are present.  Its proof homogenizes the compact slice and
classifies the only possible linear-span dimensions: the endpoint
dimensions contradict the target light quadric, while the remaining
hyperplane either contains an order-three boundary ray or would give an
impossible injection
\(S^{2(d-2)}\hookrightarrow S^{d-2}\times S^{d-2}\).  The same note gives
a compact affine two-block seam of exact parameter two which is not a
ball lift.  Thus compactness and local determinant switching alone do not
eliminate the extra-factor case; the global ball slack identity is
essential.

The grouped construction proves the upper value \(q+1\), while the
selection-free exposed-rank theorem proves the lower value \(q\) and gives
unique globally Lipschitz norm-chain witnesses at that rank.  Closing the
one-unit interval requires affine or determinantal control of the bounded
branch locus.

### A general seam restriction for factor-count-minimal lifts

There is a further selection-free restriction when the lift uses exactly
the \(q\) capacity-minimal full-size factors \(Q_d\), with
\(c=d-2\) and \(s-1=qc\).  Assume hypothetically that
\(\nu(F)\leq q\), and let a boundary fiber contain a tuple of total
Jordan nullity \(q\).  If \(z\) blocks of this tuple are cone vertices,
then necessarily
\[
                              \boxed{zc\leq q-1.}          \tag{17}
\]

The homogenized kernel dimension is also sharply confined.  With the
notation below,
\[
                         \boxed{1\leq k\leq q-1.}         \tag{17a}
\]
Indeed, \(k=0\) would make \(\Pi|_L\) an isomorphism.  The target light
quadric would then be contained in the union of the zero sets of the
\(q\) pulled-back block determinants.  Irreducibility forces it to divide
one determinant, impossible because that determinant has matrix rank at
most \(d=c+2<qc+2\).

For the upper bound, take a generic regular support.  A rank-\(q\)
certificate annihilates every point in its compact primal fiber, so every
such point has nullity at least \(q\).  The hypothetical parameter bound
puts the reverse inequality on every boundary tuple.  The compact-fiber
dichotomy then makes this fiber a singleton.  Its homogenized inverse
face is one ray lying in the \(q\)-dimensional minimal product face \(E\)
formed by the \(q\) nonzero rank-one block rays.  Every nonzero point of
the inverse face has positive homogenizing height and normalizes into the
singleton base fiber, so scaling creates no additional branch.  Moreover,
the generic tuple is in the relative interior of the product face.  If
\(L\cap E\) had an independent second direction, small perturbations with
both signs would remain in that face; their target images average to an
extreme-ray point and hence remain in the same target ray, contradicting
the one-ray inverse face.  Thus \(\dim(L\cap E)=1\).  Grassmann's
inequality gives
\[
  1=\dim(L\cap E)\geq
  (qc+2+k)+q-(qc+2q)=k-q+2,
\]
which proves \(k\leq q-1\).  For \(q=2\), (17a) leaves only one
hyperplane case; this is exactly why the two-factor theorem can classify
the whole compact lift.

The top-kernel case \(k=q-1\) has a further rigidity alternative when
\(c\geq q-1\).  Put \(W=L^\perp\), so \(\dim W=q-1\).  If every
coordinate projection \(W\to(\mathbb R^d)^*\) has dimension at most one,
then no hypothetical parameter-\(q\) lift exists.  To see this, first note
that every projection must be a line spanned by a functional in
\(\operatorname {int}Q_d^*\), up to sign.  A zero projection, or a line
spanned by a functional having a nonzero cone zero, would put a nonzero
coordinate-cone ray in \(L\cap Q_d^q\); its base point has nullity
\(1+2(q-1)>q\).

Orient the spanning functionals \(a_i\) positively.  Then
\[
 W=\{(\lambda_1a_1,\ldots,\lambda_qa_q):\lambda\in H\}
\]
for a \((q-1)\)-plane \(H\subset\mathbb R^q\).  A product-interior point
of \(C\) gives a positive vector \(t\in H^\perp\), so
\(H=t^\perp\).  Separate Lorentz automorphisms and rescalings therefore
identify \(C\) with the cone over the direct product
\((B_2^{c+1})^q\).  An inverse image of a target extreme ray is a face
whose span has dimension at most \(k+1=q\).  The nonray proper faces of
this product-base cone have dimension at least
\(c+2>q\).  Thus every target extreme ray has a unique source extreme
ray, continuously, and one obtains an injection
\[
                       S^{qc}\hookrightarrow(S^c)^q.     \tag{17b}
\]
Invariance of domain would make (17b) a homeomorphism, contradicting
\(H^c(S^{qc};\mathbb Z)=0\) and
\(H^c((S^c)^q;\mathbb Z)\ne0\).

Consequently, in the range \(c\geq q-1\), any surviving minimum-factor
counterexample must either have \(k\leq q-2\), or have
\(k=q-1\) with some coordinate projection of the normal space
\(L^\perp\) of dimension at least two.  This is an affine-span
classification, not merely a regularity assumption.

Here is a dimension proof.  Homogenize the bounded slice to
\[
 C=L\cap Q_d^q \xrightarrow{\ \Pi\ } Q_{qc+2},
\qquad \ker\Pi\cap C=\{0\},
\]
and put \(k=\dim\ker(\Pi|_L)\).  A nullity-\(q\) tuple with \(z\) zero
blocks has exactly \(q-2z\) nonzero rank-one blocks and \(z\) interior
blocks.  Its minimal product-cone face therefore has dimension
\[
              0\cdot z+1\cdot(q-2z)+d\cdot z=q+zc.       \tag{18}
\]
Let \(E\) be the span of this face.  Since
\(\dim L=qc+2+k\) and \(\dim Q_d^q=qc+2q\),
\[
                  \dim(L\cap E)\geq k+2-q+zc.            \tag{19}
\]
The tuple is in the relative interior of its minimal face.  Hence every
direction in \(L\cap E\) is two-sided feasible locally.  Its image under
\(\Pi\) is two-sided feasible through an extreme ray of the target
Lorentz cone, so extremality puts that image in the span of the same ray.
Consequently
\[
                        \dim(L\cap E)\leq k+1.            \tag{20}
\]
Equations (19)--(20) give (17).  In particular, when \(c\geq q\), a
saturated tuple cannot trade a vanished block for an interior block:
all \(q\) blocks must remain nonzero rank one.

There is also a codimension bound for the only remaining switching set.
Let \(Z\subset S^{qc}\) be the semialgebraic set on which the span of all
normalized dual-certificate ranges has total Jordan rank at most \(q-1\).
On a common \(C^1\) stratum of dimension \(t\), restrict the full slack
identity to the two copies of that stratum.  The induced Euclidean tangent
pairing has rank \(t\), while at most \(q-1\) Lorentz rank-one channels
contribute, each with capacity \(c\).  Thus
\[
                       t\leq c(q-1),\qquad
                       \operatorname {codim}Z\geq c.      \tag{21}
\]
This explains why any counterexample must hide all label
switching in a high-codimension projection-singular set.  It still does
not provide a continuous extension of the phase sheets across that set,
so (17)--(21) are recorded as a structural reduction, not as a proof of
the full divisible conjecture.

### The certificate-collapse seam is unavoidable even with extra factors

The preceding reduction can be sharpened without any regularity
assumption.  Allow an arbitrary finite product of Lorentz factors of
dimensions at most \(d\) and rays.  Assume compactness, \(s-1=qc\),
hypothetically \(\nu(F)<q+1\), and
\[
                              c\geq1,qquad q\geq2.        \tag{22}
\]
Then the full-range-drop set \(Z\) in (21) is nonempty.  Combined with
(21), every counterexample, even with extra factors, therefore needs a
nonempty
semialgebraic certificate-collapse seam of codimension at least \(c\).
This conclusion concerns the span of the **entire** normalized
certificate fiber, not one chosen certificate.

Suppose for contradiction that \(Z\) is empty.  First, every support
\(v\in S^{qc}\) has a boundary-fiber point of total
nullity exactly \(q\).  Indeed, approach \(v\) by generic regular
supports.  Their fibers are singletons of nullity \(q\); compactness
gives a limiting point in the fiber over \(v\), nullity cannot decrease
under a matrix limit, and the parameter bound forbids nullity above
\(q\).  Because \(Z\) is empty, the full certificate-range span has rank
at least \(q\).  Complementarity places that span in the Jordan kernel of
the saturated point, so both have rank exactly \(q\).  Averaging finitely
many certificates gives one normalized certificate whose support is the
full span.  It forces every point in the primal fiber to have nullity at
least \(q\), hence exactly \(q\).  The compact-fiber chord lemma then
makes the fiber a singleton: a nontrivial fiber chord would have an
endpoint of nullity at least \(q+1\).

The singleton depends continuously on \(v\), by compactness and the
closed graph of the primal incidence.  On one dense generic stratum,
equality in the mixed-capacity chain selects exactly \(q\) full-size
Lorentz factors of nullity one and makes every extra factor interior.
Every individual block nullity is upper semicontinuous and the total is
identically \(q\), so the nullity vector is locally constant.  Connectedness
of the support sphere fixes the same \(q\)-label set \(J\) globally.  Write
the resulting nonzero Lorentz boundary phases as
\[
       P(v)=(p_i(v))_{i\in J}\in(S^c)^q .                 \tag{23}
\]
This map is injective.  If \(P(u)=P(v)\), use at \(v\) the certificate
with every block nonzero constructed above.  Each block of the lift at
\(u\) is then complementary to that certificate block, so the genuine
slack identity gives
\[
                         1-u^Tv=0,
\]
and the two unit vectors coincide.

Thus (23) is a continuous injection between closed
connected manifolds of the same dimension.  Invariance of domain and
compactness would make it a homeomorphism
\[
                         S^{qc}\cong(S^c)^q,
\]
contradicting the nonzero intermediate cohomology of the product.  Hence
the assumption \(Z=\varnothing\) is false.  The proof does not control what happens
on this seam, where at least one block vanishes from the range span of
the full certificate fiber; that is precisely the remaining obstruction.

## Literature boundary (targeted primary-source screen, 2026-09-04)

The standard Lorentz determinant, its rank-two Jordan structure, and its
barrier parameter two are classical.  Ben-Tal--Nemirovski,
[*Lectures on Modern Convex Optimization*, Chapter
3](https://doi.org/10.1137/1.9780898718829.ch3), develop SOC modelling and
recursive lower-dimensional norm epigraphs, so the grouped/norm-chain upper
constructions are not novelty claims.  Cardoso--Vieira,
[*On the Optimal Parameter of a Self-Concordant Barrier over a Symmetric
Cone*](https://optimization-online.org/2003/11/774/), together with the
Güler--Tunçel homogeneous-cone parameter theorem, identifies ambient
symmetric-cone rank as the optimal barrier parameter.  Those results do not
compute the parameter after restricting a product determinant to an
arbitrary affine lift of a ball.

Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164), provide the general
slack-factorization characterization of cone lifts.  Gouveia--Robinson--
Thomas,
[*Lifts of Non-Compact Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1501.00115), extend that framework to
noncompact sets and recession-sensitive slack operators.  Fawzi,
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://doi.org/10.1007/s10107-018-1233-0), develops SOC
factorization rank, and Saunderson's face-chain method gives broader
product-cone lift obstructions.  These works constrain existence or size of
lifts; they do not optimize the restricted standard-barrier parameter or
derive a missing unit from simultaneous boundary and recession determinant
orders.

Nesterov--Todd's self-scaled and Hessian-Riemannian work supplies the
standard symmetric-cone metric and bounded-Dikin conversion.  The targeted
search did not locate the generic selection-free curvature inequality (6),
the two-scale recession lemma \(\nu\ge r+z\), or the exact off-divisible
frontier (2)--(4).  The conservative label is **candidate selection-free
standard-barrier frontier in the stated regimes**, assembled from classical
SOC modelling, cone-factorization, Peirce-rank, and self-concordant-metric
ingredients.  It is not a new SOC lift framework, an ambient optimal-barrier
theorem, or an arbitrary-barrier/QIPM lower bound.  The bounded divisible
case remains expressly open.  This was a targeted screen through 2026, not
an exhaustive novelty or priority determination.

## Audit checklist

1. Recheck the generic Lorentz mixed-capacity inequality (6).
2. Verify the Jordan-rank powers and iterated Hessian decoupling in Lemma 1.
3. Check that a genuine support certificate lies in the complementary
   face of every recession component and proves (12).
4. Verify the ceiling arithmetic and exact grouped upper bound.
5. Verify the homogenized kernel bounds (17a), including the singleton
   base-fiber to one-ray inverse-face step.
6. Verify the maximal-kernel normal-space classification and
   product-sphere obstruction (17b).
7. Verify the minimal-face dimension and two-sided extreme-ray argument
   in (17)--(20).
8. Verify semialgebraicity of the full-range-drop locus and the
   stratumwise mixed-rank estimate (21).
9. Verify the limiting saturated fiber, averaged full-support
   certificate, phase injection, and nonempty-seam conclusion (22)--(23).
10. Keep the bounded divisible case explicitly open.

## Independent hostile audit

The audit rederived the generic semialgebraic contact argument.  After
minimal-face reduction, a proper nonzero Lorentz face is a ray and has no
mixed channel; every productive complementary boundary pair has Jordan
ranks one and cross-Peirce dimension at most \(d-2\).  Thus (6), its
determinant-order consequence, and the ceiling arithmetic are exact.
The direct and grouped constructions give (3).

For Lemma 1, Peirce--Schur complementation gives one power of \(t\) for a
rank-one recession component and two for an interior Lorentz component.
The residual determinant lies on the complementary face and has exactly
the stated \(\sigma\)-order.  In the iterated limit the scaled mixed
Hessian term vanishes, so the two gradient quotients add.  A genuine
support certificate is orthogonal to every recession direction;
self-duality and termwise nonnegativity put it in the complementary face,
where contact with \(\bar X\) proves (12).  Hence every unbounded
divisible lift pays the missing unit.

Finally, a relative-interior point of a compact spectrahedral fiber lies
in the relative interior of its minimal product-cone face and has the
minimum Jordan nullity.  A maximal chord in any nonzero fiber direction
must end on the relative boundary of that face, adding a zero Jordan
eigenvalue.  This proves the compact-fiber dichotomy.  It does not exclude
a seam at which the minimum nullity first drops, so the bounded divisible
case is correctly left open.  No substantive defect was found.

A follow-up hostile audit checked the factor-count-minimal seam
restrictions (17)--(21).  A nullity-\(q\) tuple with \(z\) zero blocks has
\(q-2z\) nonzero boundary blocks and \(z\) interior blocks, so its minimal
face has dimension \(q+zc\).  Grassmann's inequality gives (19).  Because
the tuple is in the relative interior of that face, every direction in
\(L\cap E\) is locally feasible with both signs; the two images average to
an extreme target-cone point and must lie on its ray.  Rank--nullity then
gives (20) and \(zc\leq q-1\).

The full dual-support join and its rank-drop locus are semialgebraic by
quantifier elimination from the compact semialgebraic certificate graph.
On a common \(C^1\) stratum, any selected certificate has total Jordan
rank at most the rank of that join.  Interior dual blocks are complementary
to primal vertices and have zero two-sided primal derivative; each
productive boundary rank-one block has mixed capacity at most \(c\).
Mixed differentiation therefore gives
\(t\leq c(q-1)\) on every stratum of the drop locus, proving (21).  The
argument correctly bounds the full range-span drop set, not merely the
zero set of one selected certificate.  No defect was found.

The same follow-up audit verified (17a).  If \(k=0\), the homogenized
projection is a linear isomorphism.  The target light quadric is then
covered by the zero sets of the finitely many pulled-back block
determinants; irreducibility makes one target quadratic divide one block
quadratic, contradicting matrix ranks \(qc+2>c+2\).  At a generic support,
a rank-\(q\) certificate and the assumed parameter bound force every
point of the compact base fiber to have nullity exactly \(q\), so the
fiber is a singleton.  Positivity of the homogenizing height turns its
full conic inverse face into exactly one ray.  Since the selected tuple is
in the relative interior of its \(q\)-ray product face, any second
direction in \(L\cap E\) would give two-sided cone perturbations mapping
back to that target ray, a contradiction.  Thus
\(\dim(L\cap E)=1\), and Grassmann's inequality gives \(k\leq q-1\).
Non-base scalings and points mapping to zero create no exception because
\(\ker\Pi\cap C=\{0\}\).

The maximal-kernel normal-space alternative was also checked.  When
\(k=q-1\), the normal space has dimension \(q-1\).  A zero coordinate
projection, or a projected line whose functional has a cone zero, puts a
coordinate-supported extreme ray in \(C\); strict positivity of the
homogenizing height turns it into a base point of nullity
\(1+2(q-1)>q\).  Otherwise every projected normal line can be oriented by
an interior-dual functional \(a_i\).  Writing its coefficient space as a
\((q-1)\)-plane \(H\subset\mathbb R^q\), a product-Slater point supplies
a positive vector \(t\in H^\perp\), hence \(H=t^\perp\).  Independent
Lorentz automorphisms and positive rescalings then identify \(C\) with the
common-height cone over \((B_2^{c+1})^q\).

The faces of that cone have dimensions
\(1+m(c+1)\), \(m=0,\ldots,q\).  Since an inverse image of a target
extreme ray has span dimension at most \(k+1=q<c+2\) when
\(c\geq q-1\), it must be a single source ray.  Proper normalization gives
the continuous injection (17b), and invariance of domain plus intermediate
cohomology gives the contradiction.  Coordinate-supported rays, scaled
points, and independent block automorphisms therefore cause no exception.

The certificate-collapse seam theorem (22)--(23) received a separate
topological hostile audit.  Compactness and the closed primal incidence
	carry generic singleton lifts to saturated nullity-\(q\) points over every
	support.  If \(Z\) were empty, the full certificate support would have
	rank at least \(q\).  Lorentz complementarity and a finite convex average
	then give one certificate spanning the entire rank-\(q\) primal kernel;
	the compact-fiber chord lemma makes the fiber a singleton.  Equality in
	the capacity/nullity chain fixes exactly \(q\) full-size rank-one labels,
	while every extra factor is interior.  The resulting phase map is
	continuous and injective by the full slack identity.  Invariance of domain
	would give the impossible homeomorphism
	\(S^{qc}\cong(S^c)^q\).  The audit returned
	**PASS** under the broadened stated hypotheses: \(c\geq1\), \(q\geq2\),
	any finite number of capped Lorentz factors and rays, compactness, and
	restricted standard parameter at most \(q\).  The result proves that a
	high-codimension certificate-collapse seam is unavoidable; it does not yet
	rule out such a seam.
