# Affine PSD lifts need no selected contact sheets in the real one-channel regime

Status: Proved; aggregate-certificate strengthening independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the proof; priority not established

## Result

Let

\[
                 C=(B_2^s)^b,\qquad s\geq3,
\]

and let an exact finite affine lift of \(C\) use a product of real PSD
cones

\[
                 K=\prod_{i=1}^L\mathbb S_+^{r_i},
                 \qquad r_i\leq s.                       \tag{1}
\]

After the automatic initial reduction to the minimal face, assume relative
Slater.  Then there are genuine row-support dual certificates \(Y^d\) at a
simultaneous boundary point \(u=(u_1,\ldots,u_b)\) such that

\[
 \boxed{
   \sum_i\operatorname{rank}\left(\sum_{d=1}^b\lambda_dY_i^d\right)
      \geq2b\qquad(\lambda_d>0).
 }                                                                  \tag{2}
\]

Moreover, **every** lifted matrix tuple over \(u\) satisfies

\[
             \boxed{\sum_i\operatorname{nullity}X_i\geq2b.}          \tag{3}
\]

Thus the \(2b\) conclusion of the globally bi-\(C^1\) sequential
range-compression theorem is automatic for arbitrary finite affine PSD
lifts.  No primal or dual selection, differentiability, constant-rank
sheet, or proper contact incidence is needed.

The exposed-rank Dikin theorem therefore gives the selection-free,
path-independent feasible lifted-path coefficient in the restricted
standard log-determinant metric

\[
                 \sqrt{2b}\,\log(1/\epsilon)                         \tag{4}
\]

up to its stated finite reference-minor constant, for the weighted support
objective exposed by \(\sum_d\lambda_dY^d\).  If the affine slice carries
the restricted standard product log-determinant, (3) and the determinant
vanishing-order argument give

\[
                   \boxed{\nu_{\mathrm{std,slice}}\geq2b.}           \tag{5}
\]

The two-group Schur construction for each source ball attains (5).
Consequently \(2b\) is the exact standard-slice frontier for arbitrary
finite affine real-PSD lifts under the critical order cap \(r_i\leq s\),
not merely for lifts admitting global bi-\(C^1\) selected factors.

The central new point is an intrinsic one-ball lemma for the *whole convex
fiber of dual certificates*.  Convexity turns any attempted discontinuous
switch between rank-one certificates into a rank-two certificate at the
switch.  If switching never occurs, the certificate fiber is a singleton
and would embed a sphere in a projective space of no larger dimension,
which is impossible.

## 1. Affine-lift setup

After one initial minimal-face reduction, write the affine PSD lift as

\[
 \mathcal A(x,y)=\mathcal A_0+
       \sum_{a,j}x_{aj}\mathcal A_{aj}+
       \sum_{\ell}y_\ell\mathcal B_\ell\in K,             \tag{6}
\]

where each displayed matrix is a tuple with blocks of orders at most
\(s\).  Redundant affine variables cause no problem.  At a relative-Slater
center over \(x=0\), choose

\[
                         X^\circ=\mathcal A(0,y^\circ)\succ0.          \tag{7}
\]

Such a center exists because linear projection commutes with relative
interior and the origin is in the interior of the product of balls.

For a support direction \(v\in S^{s-1}\) in source row \(d\), conic
duality gives a nonempty fiber \(\mathcal D_d(v)\) of PSD certificates
\(Z=(Z_i)_i\) satisfying

\[
 \langle\mathcal B_\ell,Z\rangle=0,\quad
 \langle\mathcal A_{j},Z\rangle=-v_j,\quad
 \langle\mathcal A_0,Z\rangle=1,                         \tag{8}
\]

and zero coefficients on every other projected coordinate.  Equivalently,
every feasible lifted tuple obeys

\[
                         \langle X,Z\rangle=1-x_d^Tv.     \tag{9}
\]

Exactness of the projected product makes the support optimum one.  Relative
Slater and finiteness of that optimum give strong duality and attainment.
Moreover, (7)--(8) give

\[
                         \langle X^\circ,Z\rangle=1.      \tag{10}
\]

Since every block of \(X^\circ\) is positive definite in the reduced
face, (10) bounds \(\sum_i\operatorname{tr}Z_i\) uniformly.  Hence every
\(\mathcal D_d(v)\) is nonempty, compact, and convex, and the union of these
fibers over the compact sphere is bounded.  Its graph is closed because
the defining linear equations depend continuously on \(v\).

## 2. Intrinsic one-ball certificate lemma

> **Lemma 1.**  For each \(v\in S^{s-1}\), let \(\mathcal E(v)\) be a
> nonempty compact convex family of PSD tuples of orders at most \(s\).
> Assume the union is bounded, the graph is closed, and every
> \(Z\in\mathcal E(v)\) satisfies
> \[
>                \langle X(u),Z\rangle=1-u^Tv
>                 \quad\text{for every }u\in B_2^s,                  \tag{11}
> \]
> for some fixed feasible primal tuple \(X(u)\) at each \(u\).  If
> \(s\geq3\), then some \(v\) and \(Z\in\mathcal E(v)\) satisfy
> \[
>                       \sum_i\operatorname{rank}Z_i\geq2.           \tag{12}
> \]

Suppose instead that every certificate in every fiber has total rank at
most one.  Equation (11) at \(u=-v\) rules out rank zero, so all certificates
have total rank exactly one.

Fix \(v\).  If \(Z,Z'\in\mathcal E(v)\) use different blocks, then their
average has rank one in two blocks.  If they use the same block but
different range lines, their average has rank two in that block.  Both
contradict the assumption.  Therefore all members of \(\mathcal E(v)\)
lie on one rank-one ray in one block.  Pairing with the common tuple
\(X(0)\) gives the fixed positive value one and hence fixes the scale on
that ray.  Thus

\[
                              \mathcal E(v)=\{Z(v)\}.     \tag{13}
\]

The map \(v\mapsto Z(v)\) is continuous.  Indeed, if \(v_n\to v\),
uniform boundedness gives a convergent subsequence of \(Z(v_n)\); the
closed-graph hypothesis puts every limit in \(\mathcal E(v)\), whose
member is unique.  The same argument for every subsequence gives full
convergence.

The active block label is locally constant: its nonzero block remains
nonzero under a small perturbation, while total rank one forbids another
active block.  Connectedness of \(S^{s-1}\) therefore fixes one block,
say of order \(r\leq s\), globally.  Its range defines a continuous map

\[
                    h:S^{s-1}\longrightarrow\mathbb {RP}^{r-1}.      \tag{14}
\]

This map is injective.  If two values have the same range line, pairing
with \(X(0)\) makes their certificates equal.  Equation (11) for the two
support directions then
gives \(u^T(v-w)=0\) for every \(u\in B_2^s\), hence \(v=w\).

Put \(n=s-1\geq2\).  There is no topological embedding
\(S^n\hookrightarrow\mathbb {RP}^{r-1}\) when \(r-1<n\), by monotonicity
of covering dimension.  If \(r-1=n\), invariance of domain makes the
image of (14) open; compactness makes it closed.  Hence it is all of the
connected \(\mathbb {RP}^n\), making \(S^n\) homeomorphic to
\(\mathbb {RP}^n\).  This contradicts their fundamental groups for
\(n\geq2\).  Lemma 1 follows.

This argument also pinpoints why semialgebraic seams do not obstruct the
affine-lift theorem.  One need not construct a semialgebraic selection.
If two rank-one branches meet in the same convex certificate fiber, their
average already proves (12); if they never meet, compactness forces the
unique branch to be continuous and topology excludes it.

## 3. Sequential compression by genuine global certificates

We choose \(u_1,\ldots,u_b\) successively while retaining genuine dual
certificates of the original reduced affine lift.  Suppose the first
\(d-1\) directions and certificates \(Y^e\in\mathcal D_e(u_e)\) have been
chosen, and put

\[
 W_i^{d-1}=\sum_{e<d}\operatorname{Ran}Y_i^e,
 \qquad P_i^{d-1}=P_{(W_i^{d-1})^\perp}.                 \tag{15}
\]

For any primal lift fiber with \(x_e=u_e\), row-\(e\) contact gives
\(\langle X,Y^e\rangle=0\).  Every block pairing is nonnegative, so

\[
                 W_i^{d-1}\subseteq\ker X_i,
                 \qquad X_i=P_i^{d-1}X_iP_i^{d-1},        \tag{16}
\]

for **every** lifted tuple in the entire future-coordinate cylinder.

For \(v\in S^{s-1}\), compress the whole original row-certificate fiber:

\[
 \mathcal E_d(v)=\left\{
   \bigl(P_i^{d-1}Y_iP_i^{d-1}\bigr)_i:
                       Y\in\mathcal D_d(v)\right\}.      \tag{17}
\]

These image fibers are nonempty, compact, and convex.  They have uniformly
bounded union, and their graph is closed: from a convergent compressed
sequence, choose the uniformly bounded original certificates and pass to a
convergent subsequence in the closed graph of \(\mathcal D_d\).

Choose, for every \(u\in B_2^s\), any feasible lifted tuple with the first
\(d-1\) coordinates fixed at their contacts, the \(d\)-th coordinate
equal to \(u\), and fixed feasible values for later coordinates.  Equations
(9) and (16) show that every \(Z\in\mathcal E_d(v)\) satisfies

\[
                         \langle X(u),Z\rangle=1-u^Tv.    \tag{18}
\]

Thus Lemma 1 applies directly to the compressed images of the **global**
certificate fibers.  It supplies \(u_d\) and
\(Y^d\in\mathcal D_d(u_d)\) such that

\[
 \sum_i\operatorname{rank}
       (P_i^{d-1}Y_i^dP_i^{d-1})\geq2.                  \tag{19}
\]

Update \(W_i^d=W_i^{d-1}+\operatorname{Ran}Y_i^d\).  For PSD \(Y=CC^T\)
and \(P=P_{W^\perp}\),

\[
 \operatorname{rank}(PYP)=\operatorname{rank}(PC)
   =\dim(W+\operatorname{Ran}Y)-\dim W.                 \tag{20}
\]

Consequently (19) is exactly the new total range dimension, and

\[
 \sum_i\dim W_i^b\geq2b.                                \tag{21}
\]

At the final simultaneous contact, every lift fiber has
\(W_i^b\subseteq\ker X_i\), proving (3).  More strongly, for arbitrary
positive weights \(\lambda_d\),

\[
 Y(\lambda)=\sum_d\lambda_dY^d
\]

is a genuine original-slice certificate for the weighted support slack
\(\sum_d\lambda_d(1-x_d^Tu_d)\).  PSD range additivity gives

\[
 \sum_i\operatorname{rank}Y_i(\lambda)
   =\sum_i\dim\left(\sum_d\operatorname{Ran}Y_i^d\right)
   =\sum_i\dim W_i^b\geq2b,                             \tag{22}
\]

which proves (2).  This avoids a subtle extension issue that would arise
if one took arbitrary certificates only after stagewise facial reduction:
the matrices \(Y^d\) here are global dual certificates from the outset.

## 4. Standard-barrier consequence and attainment

Because (22) is an original-slice dual certificate exposing the weighted
simultaneous support point, the companion exposed-rank theorem applies
without any selected factor sheets.  Its path-independent Dikin-length
lower bound has coefficient \(\sqrt{2b}\) in front of
\(\log(1/\epsilon)\), with the theorem's explicit finite reference-minor
constant.  This is an affine-lift movement statement, not merely a
standard-barrier parameter count.

Suppose first that the original affine slice has a strictly feasible
point.  Join it by a line segment to any lifted tuple over the contact
found above.  Along this feasible interior segment, the determinant of
block \(i\) vanishes at the endpoint to order
\(\operatorname{nullity}X_i\).  The standard one-dimensional
self-concordant barrier inequality therefore implies

\[
              \nu_{\mathrm{std,slice}}
                    \geq\sum_i\operatorname{nullity}X_i\geq2b.       \tag{23}
\]

For a lift with a forced common kernel, the same statement applies after
the initial facial reduction, which is the only cone on which the
restricted standard log-determinant is finite.

For the upper bound, split the \(s\) coordinates of each source into two
groups of size at most \(s-1\).  For every group use the Schur block

\[
                         \begin{pmatrix}t_G&w_G^T\\w_G&I\end{pmatrix}
                         \succeq0,
              \qquad \sum_{G\text{ in source }a}t_G=1.               \tag{24}
\]

This gives an exact order-at-most-\(s\) lift of each ball and has restricted
standard parameter two per source.  Products attain \(2b\), proving the
claimed exactness.

## 5. Higher-rank span control and the norm-tree seam test

The certificate-fiber method has one useful higher-rank remnant.  If every
member of a convex PSD certificate fiber \(\mathcal D(v)\) has total rank
at most \(q\), then

\[
 E_i(v)=\sum_{Z\in\mathcal D(v)}\operatorname{Ran}Z_i
 \quad\Longrightarrow\quad
                  \sum_i\dim E_i(v)\leq q.               \tag{25}
\]

Indeed, if finitely many certificates span more than \(q\) total range
dimensions, their positive average has blockwise range equal to the sum of
their ranges and hence total rank greater than \(q\).  Finite-dimensionality
then proves (25).  This does **not** automatically make \(E(v)\) continuous,
even on a constant-dimension locus: closed graph gives only outer control
of certificate limits, while a spanning certificate direction can vanish
in norm and a new direction can appear in the limiting fiber.  Continuity
would follow from an additional inner-semicontinuity condition with locally
persistent spanning certificates, but that condition is not automatic for
an affine lift.

The fibers are more structured than an arbitrary multifunction.  For one
source row, let \(\mathscr B_d\) be the normalized dual base consisting of
all \(Z\succeq0\) that annihilate the auxiliary and other-row coefficients
and satisfy \(\langle\mathcal A_0,Z\rangle=1\).  Let \(\pi_d(Z)\) be its
row-\(d\) coefficient vector.  This is a compact spectrahedron and

\[
                              \pi_d(\mathscr B_d)=B_2^s.              \tag{26}
\]

Indeed, every \(Z\in\mathscr B_d\) certifies
\(1-x_d^T\pi_d(Z)\geq0\) on the projected ball, so its image has norm at
most one.  Conversely, every unit \(v\) has an attained certificate by
Slater duality.  Convexity of \(\mathscr B_d\), or explicitly convex
combinations of certificates at \(v/\|v\|\) and its antipode, supplies
every interior \(v\).  Thus the higher-rank question is a boundary-rank
problem for a compact spectrahedron projecting linearly onto the entire
ball, not a free-standing selection problem.

There is nevertheless a selection-free global invariant.  Let

\[
 \mathscr D_d=\{(v,Z):v\in S^{s-1},\ Z\in\mathcal D_d(v)\}.            \tag{27}
\]

This incidence space is compact, and its projection to \(S^{s-1}\) is a
proper surjection with nonempty compact convex, hence acyclic, fibers.  The
Vietoris--Begle mapping theorem therefore gives

\[
             \check H^*(\mathscr D_d;G)\cong H^*(S^{s-1};G)          \tag{28}
\]

for every coefficient group \(G\).  Thus the full certificate incidence
retains the sphere's cohomology even when no continuous certificate or
support selection exists.  A possible higher-rank route is to classify
the rank-saturated incidence inside the product of low-rank PSD strata and
derive the projective-cover contradiction from (27).  What is missing is
the lift-intrinsic local capacity theorem that would force every
certificate in a saturated fiber to have the same maximal rank and support
type.

For \(q=1\), normalization collapses the whole fiber to one matrix and the
support equations make its range map injective; this is exactly Lemma 1.
For \(q>1\), neither conclusion follows.  A positive-dimensional convex
fiber can encode several support directions inside the same fixed support
face, so the span map need not be injective.  This is the precise unresolved
obstruction to repeating the projective-cover proof.

There is a decisive obstruction to extending the **exposed-dual-rank**
conclusion.  Put
\(M(\tau,z_1,z_2)=\left[\begin{smallmatrix}\tau+z_1&z_2\\
z_2&\tau-z_1\end{smallmatrix}\right]\).  A binary norm chain lifts
\(B_2^s\) with \(s-1\) copies of \(\mathbb S_+^2\):

\[
 X_1=M(t_1,x_1,x_2),\quad
 X_j=M(t_j,t_{j-1},x_{j+1})\ (2\leq j\leq s-2),\quad
 X_{s-1}=M(1,t_{s-2},x_s).                              \tag{29}
\]

For a support vector \(v\), let
\(\rho_j=(\sum_{\ell\leq j+1}v_\ell^2)^{1/2}\).  The dual certificate is
unique and equals

\[
 Z_1={1\over2}M(\rho_1,-v_1,-v_2),\qquad
 Z_j={1\over2}M(\rho_j,-\rho_{j-1},-v_{j+1}).             \tag{30}
\]

The trace pairings telescope to \(1-v^Tx\).  Conversely, the coefficient
equations and PSD inequalities force the scalar coordinates successively
to \(\rho_j\), proving uniqueness.  Each \(Z_j\) has rank one when
\(\rho_j>0\) and is zero otherwise.  Hence **every** support certificate
has total rank at most \(s-1\), whereas the globally bi-\(C^1\) Hermitian
formula at real order two is \(\kappa_{\mathbb R,2}(s)=s\).  Unique fibers,
semialgebraicity, global continuity, and generic analyticity therefore do
not make the smooth exposed-rank theorem automatic.

This does not refute a selection-free **primal-nullity or standard-barrier**
extension.  At a norm-tree seam, vanished dual blocks correspond to primal
vertex blocks, and each \(2\times2\) zero block contributes nullity two.
For instance, two \(H_+^2(\mathbb C)\cong Q_4\) norm-tree blocks lift
\(B_2^5\) and have generic primal nullity two, but the seam has nullity
three, matching \(\kappa_{\mathbb C,2}(5)=3\); two quaternionic
\(Q_6\) blocks similarly lift \(B_2^9\) and attain seam nullity three.
Thus the higher-rank frontier splits: intrinsic aggregate exposed rank is
false in this generality, while a seam-sensitive every-fiber nullity theorem
remains plausible and open.

The companion [exact selection-free PSD2
theorem](2026-09-04-selection-free-psd2-product-ball-exposed-rank.md)
turns this obstruction into a sharp heterogeneous product law: the exact
affine-lift minimax aggregate exposed rank for \(\prod_dB_2^{s_d}\) over real
PSD2 blocks and rays is \(\sum_d(s_d-1)\), attained by independent binary
chains.

This limitation agrees with parametric-optimization sensitivity theory.
Continuity of selected solutions generally needs lower semicontinuity or a
metric/strong-regularity hypothesis, not merely uniqueness of a regularized
minimizer; see Terazono--Matani,
[*Continuity of Optimal Solution Functions and their Conditions on
Objective Functions*](https://doi.org/10.1137/110850189), and Han--Pang,
[*Continuous Selections of Solutions to Parametric Variational
Inequalities*](https://doi.org/10.1137/22M1514982).  Recent SDP stability
results likewise impose metric regularity or growth conditions to obtain
Hölder or Lipschitz control.  Thus a minimum-Frobenius-norm or
relative-analytic-center certificate is not automatically a continuous
support selector at a changing optimal face.

## Scope and novelty boundary

The theorem concerns finite affine real-PSD lifts, their intrinsic dual
certificate fibers, and the restricted standard product log-determinant.
It does not assert that arbitrary slack factorizations admit continuous
factors, and it does not apply to custom coupled barriers or directly give
an oracle/query lower bound for a QIPM.

The proved theorem is special to the critical real one-channel case.
Section 5 records the surviving set-valued span and incidence lemmas, gives
a unique-fiber counterexample to a blanket higher-rank exposed-rank upgrade,
and separates that failure from the still-open primal-nullity question.

The companion
[globally smooth sequential theorem](2026-09-04-q1-sequential-range-compression-closure.md)
uses selected factors and the even-quadratic sole-factor obstruction.  The
present intrinsic certificate-fiber argument removes that hypothesis and
also strengthens its boundary conclusion from one selected primal tuple to
every fiber over the constructed contact.  A targeted local literature
screen found no proof of the full selection-free capped-PSD product-ball
frontier below.  This is a claim about an apparently unlocated synthesis,
not about novelty of convex certificate sets, PSD kernel compression,
singleton continuity, or invariance of domain separately.  Priority remains
subject to specialist review.

### Primary-source provenance audit (2026-09-04)

The closest source is more direct than a generic citation to conic duality.
In the proof of Theorem 2.4 of Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone Factorizations*](https://doi.org/10.1287/moor.1120.0575),
the primal factor over \(x\) is chosen from the full convex lift fiber and the
dual factor over a support functional is chosen as **any** point in a
nonempty convex dual feasible set obtained by Slater duality.  Their affine
identity holds for every point of the lifted slice.  Consequently, the
existence of the convex certificate fibers in (8), and the fact that one
zero-slack certificate annihilates every primal lift over its exposed
contact, are classical consequences of that proof.  The cited theorem makes
arbitrary pointwise choices; it does not analyze all members of the dual
fiber simultaneously, require a continuous choice, or extract rank from the
topology of the support-parameter space.

Fawzi, Gouveia, Parrilo, Robinson, and Thomas,
[*Positive Semidefinite Rank*](https://doi.org/10.1007/s10107-015-0922-1),
provide three further direct antecedents.  Proposition 6.1 views the set of
valid factors on one side, after fixing the other side, as an SDP feasible
set and selects low-rank members.  Section 7 treats the complete space of
finite-matrix PSD factorizations as a topological space: Proposition 7.3
identifies it with a space of nested PSD-cone images in the dimension-tight
case, and Proposition 7.9 proves connectedness for ordinary rank three and
PSD rank two.  Most importantly for Section 3 here, Theorem 2.10 derives a
block-triangular PSD-rank lower bound by putting the span of a family of
factor ranges into the common kernel of the orthogonal factors and
compressing to that span and its orthogonal complement.  Thus PSD
orthogonality, common-kernel statements, and range compression are prior
art.  That theorem concerns a finite zero pattern and already chosen
factors; it does not recursively compress a parameterized family of global
dual-certificate fibers or preserve a single original affine-slice identity
for the final positive aggregate.

Two newer topology/fiber papers narrow the distinction further.  Dawson,
Hoşten, Kubjas, and Metsälampi,
[*Uniqueness of size-2 positive semidefinite matrix
factorizations*](https://arxiv.org/abs/2410.18891) (v2, 2026), characterize
local and global uniqueness up to the \(GL(2)\) action using rigidity theory.
Their object is the factorization space of one finite nonnegative matrix,
not a convex dual-certificate fiber indexed by all support directions; their
argument does not produce the map (14) or use invariance of domain to rule it
out.  Vill,
[*Integrating Spectrahedra*](https://doi.org/10.1007/s00454-025-00719-4),
studies whole compact **primal** PSD fibers under a linear projection and
their measurable sections.  Theorems 2.8 and 2.12 transfer facial and normal
cone information to the fiber body, and Proposition 2.19 gives continuity of
finitely many fixed-rank points under transversality.  This is genuine
whole-fiber spectrahedral topology, but it averages primal fibers rather
than using support-indexed dual certificate fibers; the paper explicitly
lists the dual convex body and KKT certificates as a direction for further
study.

Finally, the initial minimal-face reduction is classical; see Borwein and
Wolkowicz,
[*Facial reduction for a cone-convex programming
problem*](https://doi.org/10.1017/S1446788700017250).  Facial reduction also
supplies the general precedent that an exposing certificate can force an
entire feasible set into a proper face.  It does not give the source-wise
support certificates or the \(2b\) cumulative rank at one simultaneous
product-ball contact.

Within these primary sources and targeted searches through 2026, no theorem
was located that combines the following two steps:

1. convexity of every support-certificate fiber turns total rank one into a
   normalized singleton, whose closed graph yields a continuous injective
   map \(S^{s-1}\to\mathbb {RP}^{r-1}\), followed by the covering-dimension
   and invariance-of-domain obstruction; and
2. the one-ball obstruction is applied stagewise to compressed images of
   the **original global** certificate fibers, so the chosen uncompressed
   certificates remain genuine pure-row duals and every positive weighted
   aggregate has rank at least \(2b\), while every primal lift at the final
   contact has nullity at least \(2b\).

The safe novelty label is therefore **candidate selection-free critical-real
affine-lift theorem; exact synthesis not located**.  The primitives and
several proof motifs have clear antecedents, and the negative search is not
an exhaustive priority determination.  In particular, do not advertise
“the first use of certificate fibers,” “the first topological study of PSD
factorizations,” or “a new PSD compression method.”

## Audit checklist

1. Verify compactness and closed-graph continuity of the certificate fiber,
   including redundant affine variables and relative facial reduction.
2. Check that rank-one convexity really forces a singleton after the
   strictly feasible normalization.
3. Check the embedding obstruction for every \(s\geq3\) and every reduced
   order \(r\leq s\).
4. Verify that the minimal face of the entire future-coordinate cylinder
   is unnecessary after compressing the original global certificate
   fibers, and that the compressed image fibers have closed graph.
5. Verify (15)--(20), especially that (18) holds on the whole future
   cylinder and that compressed rank is exactly the new range dimension.
6. Check that \(\sum_d\lambda_dY^d\) is a genuine original-slice weighted
   support certificate, so exposed rank, every-final-fiber nullity, and the
   standard-logdet-only conclusion all have their stated scopes.

## Independent hostile audit

The first audit passed the intrinsic singleton/projective-embedding lemma,
every-final-fiber nullity conclusion, and restricted standard-barrier
scope. It also caught the need for equality \(\sum_Gt_G=1\) in (24),
which avoids an extra scalar slack.

A second hostile audit checked the stronger
compressed-global-certificate proof. The image fibers in (17) are compact
and convex; uniform boundedness of the original certificate fibers and
their closed graph let every convergent compressed sequence be lifted
along a convergent subsequence, proving the image graph is closed.
Normalization in Lemma 1 is supplied by the same whole-cylinder primal
tuple \(X(0)\), and (16) makes the pure-row identity survive compression
for every future fiber.

The audit also verified that (20) is exactly the new full-range dimension,
even though the chosen original certificate can have components in the
old range. Each chosen \(Y^d\) remains a genuine pure-row certificate of
the original reduced affine lift, so positive weighted sums are genuine
support-objective certificates and PSD range additivity gives (22).
Consequently the exposed-rank Dikin theorem applies in the restricted
standard log-determinant metric with coefficient \(\sqrt{2b}\); it is not
an arbitrary-barrier or primal--dual product-metric statement. No
mathematical defect remained after that scope wording was clarified.

A third audit checked the higher-rank scope.  It verified the span bound,
the normalized dual-base projection (26), and the Vietoris--Begle incidence
argument.  It also rederived the binary norm-chain coefficient equations:
PSD recursion and final normalization uniquely force (30), so no hidden
higher-rank dual certificate exists.  The audit confirmed the distinction
between the resulting exposed-rank counterexample and the extra primal
nullity contributed by vertex blocks at norm-tree seams.
