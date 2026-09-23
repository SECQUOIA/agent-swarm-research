# Face-capped grouping for products of spectral-norm balls

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the whole-row grouping model; novelty pending specialist review

## Result

For \(a=1,\ldots,k\), orient a real matrix variable as

\[
 X_a\in\mathbb R^{r_a\times c_a},\qquad r_a\leq c_a,
 \qquad \lVert X_a\rVert_{\rm op}\leq1.                 \tag{1}
\]

Given a group \(G\subseteq[k]\), put all of its rows in the shared-scale
spectral cone

\[
 \mathcal S_G=\{(t,(X_a)_{a\in G}):
                 \lVert X_a\rVert_{\rm op}\leq t\ \forall a\in G\}.
                                                               \tag{2}
\]

Let \(D\) cap the real dimension of every cone block, and let \(F\) cap
the maximum dimension of a proper exposed face.  In the whole-row model
defined below, a group \(G\) is feasible under both caps if and only if

\[
 \boxed{
 \sum_{a\in G}r_ac_a\leq D-1,
 \qquad
 \sum_{a\in G}r_ac_a-
       \min_{a\in G}(r_a+c_a-1)\leq F-1.}               \tag{3}
\]

Consequently, within the row-indivisible whole-row model, the exact
minimum block count is the minimum number of parts in a partition
\(\mathcal G\) of \([k]\) such that every part satisfies (3).  Shared
spectral cones attain this minimum.  For that attaining construction,
every such partition has exact ledgers

\[
 \begin{aligned}
 g&=|\mathcal G|,\\
 M_{\rm amb}&=\sum_{a=1}^kr_ac_a+g,\\
 \nu_{\rm amb}^{\rm opt}&=\sum_{a=1}^kr_a+g,\\
 \nu_{\rm fixed\ slice}^{\rm opt}&=\sum_{a=1}^kr_a.
 \end{aligned}                                           \tag{4}
\]

The ambient and slice barrier equalities hold against arbitrary coupled
self-concordant barriers on the displayed product cone or fixed-scale
domain, not merely for the separable determinant barrier.

For \(k\) equal \(r\times c\) matrix balls, one block can carry exactly

\[
 Q=\min\left\{
    \left\lfloor{D-1\over rc}\right\rfloor,
    \left\lfloor{F+r+c-2\over rc}\right\rfloor
          \right\}                                      \tag{5}
\]

rows, provided \(Q\geq1\).  Hence

\[
 g_{\min}=\left\lceil{k\over Q}\right\rceil,
 \quad M_{\min}=krc+g_{\min},
 \quad \nu_{\rm amb}^{\min}=kr+g_{\min},
 \quad \nu_{\rm slice}^{\min}=kr.                     \tag{6}
\]

The heterogeneous minimum-partition problem is strongly NP-hard, even for
vector rows \(r_a=1\) when the face cap is nonbinding.  Thus (3) is a
closed-form feasibility oracle, but computing the optimal heterogeneous
grouping is already as hard as bin packing.

## 1. A cone-independent whole-row lower bound

The cap law is not merely a property of the displayed spectral cone.  Put

\[
 \mathcal E_a=\{X\in\mathbb R^{r_a\times c_a}:XX^T=I_{r_a}\},
 \qquad
 \mathcal Z_a=\{uv^T:\lVert u\rVert=\lVert v\rVert=1\}. \tag{6a}
\]

These are respectively the extreme points of the spectral-norm ball and
of its nuclear-norm polar.  Let \(K\subseteq\mathbb R^m\) be any proper
cone.  A *whole-row full-slack factorization* of the rows in \(G\) consists
of maps

\[
 A:\prod_{b\in G}\mathcal E_b\longrightarrow K,
 \qquad B^a:\mathcal Z_a\longrightarrow K^*                 \tag{6b}
\]

satisfying, for every \(a\in G\),

\[
 \left\langle A((X_b)_b),B^a(Z)\right\rangle
                  =1-\langle X_a,Z\rangle_F.              \tag{6c}
\]

No continuity or differentiability of the maps is assumed.  Define

\[
 f(K)=\max_{0\ne y\in K^*}\dim\bigl(K\cap y^\perp\bigr),   \tag{6d}
\]

where face dimension means the dimension of its linear span.  Every
factorization (6b)--(6c) obeys

\[
 \boxed{
 m\geq1+\sum_{a\in G}r_ac_a,
 \qquad
 f(K)\geq1+\sum_{a\in G}r_ac_a
                 -\min_{a\in G}(r_a+c_a-1).}             \tag{6e}
\]

Here is a direct rank proof.  Rank-one matrices span
\(\mathbb R^{r_a\times c_a}\), and

\[
 {S_{a,-Z}+S_{a,Z}\over2}=1,qquad
 {S_{a,-Z}-S_{a,Z}\over2}=\langle X_a,Z\rangle_F,         \tag{6f}
\]

where \(S_{a,Z}=1-\langle X_a,Z\rangle_F\).  The constant and
all \(\sum_a r_ac_a\) coordinate functions are linearly independent on
\(\prod_a\mathcal E_a\).  Indeed, each \(\mathcal E_a\) is centrally
symmetric and spans the full matrix space: its convex hull is the
spectral-norm ball, which has nonempty interior.  Because every function
in (6f) is a linear functional of \(A((X_b)_b)\), their rank is at most
\(m\).  This proves the first inequality in (6e).

For the face bound, fix \(a\) and \(Z=uv^T\), and restrict to the contact
cylinder

\[
 \mathcal C_{a,Z}=\{(X_b)_b:\langle X_a,Z\rangle_F=1\}.    \tag{6g}
\]

Equation (6c) puts \(A(\mathcal C_{a,Z})\) in the exposed face
\(K\cap B^a(Z)^\perp\); the factor \(B^a(Z)\) is nonzero because its
pairing is not the zero function.  In orthogonal bases with
\(u=v=e_1\), equality in the contraction bound forces

\[
 X_a=\begin{pmatrix}1&0\\0&Y\end{pmatrix},
       \qquad YY^T=I_{r_a-1}.                             \tag{6h}
\]

The restrictions of (6f) to this cylinder span the constant, every
coordinate of every \(X_b\) for \(b\ne a\), and all
\((r_a-1)(c_a-1)\) coordinates of \(Y\).  These functions remain
independent by the same central-symmetry and full-span argument (with the
zero-size case interpreted as having no \(Y\)-coordinates).  Hence this
face has dimension at least

\[
 1+\sum_{b\ne a}r_bc_b+(r_a-1)(c_a-1)
 =1+\sum_b r_bc_b-(r_a+c_a-1).
\]

Maximizing over \(a\) proves the second inequality in (6e).  The shared
spectral cone attains both inequalities, as the next section shows.
Therefore (3) is necessary for *every* proper cone carrying the group as
one whole-row block and sufficient via \(\mathcal S_G\).

## 2. Exact face formula

The dual of (2), under the real Frobenius pairing, is

\[
 \mathcal S_G^*=\left\{(\alpha,(Z_a)):
           \alpha\geq\sum_{a\in G}\lVert Z_a\rVert_*\right\}. \tag{7}
\]

Take a nonzero boundary point of (7), let

\[
 J=\{a:Z_a\ne0\},\qquad h_a=\operatorname{rank}Z_a.
\]

Equality in spectral/nuclear duality characterizes the complementary
exposed face.  In singular-vector coordinates of a supported block,
\(X_a/t\) has a fixed negative identity on the \(h_a\)-dimensional support,
both cross rectangles vanish, and an arbitrary contraction remains on an
\((r_a-h_a)\times(c_a-h_a)\) rectangle.  Unsupported blocks remain
arbitrary \(r_a\times c_a\) contractions.  The common scale contributes
one dimension.  Therefore

\[
 \dim \mathcal F(Z)=1+
   \sum_{a\notin J}r_ac_a+
   \sum_{a\in J}(r_a-h_a)(c_a-h_a).                     \tag{8}
\]

A supported block loses

\[
 r_ac_a-(r_a-h_a)(c_a-h_a)
       =h_a(r_a+c_a-h_a)                                \tag{9}
\]

dimensions.  For \(1\leq h_a\leq r_a\leq c_a\), (9) is minimized by
\(h_a=1\), with loss \(r_a+c_a-1\).  Supporting more than one block only
adds positive losses.  Hence the largest proper exposed face has dimension

\[
 f(\mathcal S_G)=1+\sum_{a\in G}r_ac_a-
                         \min_{a\in G}(r_a+c_a-1).       \tag{10}
\]

The cone dimension is \(1+\sum_{a\in G}r_ac_a\).  Equations (3) follow
immediately from these two exact formulas.

## 3. Barrier and storage ledgers

Put \(R_G=\sum_{a\in G}r_a\).  The determinant barrier

\[
 -\sum_{a\in G}\log\det(t^2I_{r_a}-X_aX_a^T)
                  +(R_G-1)\log t                       \tag{11}
\]

is an \((R_G+1)\)-logarithmically homogeneous self-concordant barrier.
Restricting every matrix to its rectangular diagonal subspace gives the
\((R_G+1)\)-dimensional \(\ell_\infty\)-epigraph cone and proves the
matching lower bound.  Direct-summing the corresponding sharp recession
certificates over groups proves

\[
 \nu_{\rm opt}\!\left(\prod_{G\in\mathcal G}\mathcal S_G\right)
       =\sum_G(R_G+1)=\sum_ar_a+g                    \tag{12}
\]

even for a coupled barrier.

Fixing every group scale at one restricts (11) to

\[
             -\sum_a\log\det(I_{r_a}-X_aX_a^T).         \tag{13}
\]

Its exact parameter is \(\sum_ar_a\): the upper bound is additive, while
the product of rectangular diagonal cubes gives the coupled lower bound.
The number of ambient real coordinates is the cone dimension summed over
the groups, namely \(\sum_ar_ac_a+g\).  This proves (4).

For equal matrix sizes, (3) is equivalent to \(|G|\leq Q\) with \(Q\) in
(5).  Packing \(k\) identical rows in groups of size at most \(Q\) proves
(6), including a possibly smaller last group.

## 4. Heterogeneous computational boundary

Set \(r_a=1\).  Then an item \(a\) has dimension weight \(c_a\), and the
first inequality in (3) is

\[
                       \sum_{a\in G}c_a\leq D-1.         \tag{14}
\]

Choose \(F\geq D-1\), making the second inequality redundant.  The minimum
number of groups is then exactly bin packing with item sizes \(c_a\) and
bin capacity \(D-1\).  The standard 3-PARTITION restriction proves strong
NP-hardness: its item magnitudes and total expanded matrix description are
polynomially bounded.  By the cone-independent necessity and spectral-cone
sufficiency in Section 1, this hardness applies to the optimal
row-indivisible whole-row grouping even when each part may use an arbitrary
proper cone.  It is not a lower bound for factorizations that split one row
family among several cone blocks, for nonlinear lifts, or for oracle queries.

## 5. Complex matrices

For complex \(r_a\times c_a\) variables with the real Frobenius pairing,
replace each matrix-coordinate weight \(r_ac_a\) by \(2r_ac_a\), and each
rank-one face loss \(r_a+c_a-1\) by \(2(r_a+c_a-1)\).  Thus (3) becomes

\[
 2\sum_{a\in G}r_ac_a\leq D-1,
 \qquad
 2\sum_{a\in G}r_ac_a-2\min_{a\in G}(r_a+c_a-1)\leq F-1. \tag{15}
\]

The scale remains one real coordinate.  The exact barrier parameters in
(4) are unchanged, while
\(M_{\rm amb}=2\sum_ar_ac_a+g\).
The whole-row proof also extends over \(\mathbb C\): use real linear spans,
the real Frobenius pairing, and the complex coisometry contact set.  Its
free complement has \(2(r_a-1)(c_a-1)\) real coordinates, which gives
exactly the doubled losses in (15).

## Scope and novelty boundary

The shared spectral cone, its determinant barrier, and spectral/nuclear
duality are classical.  The facial structure of spectral-norm balls is
also classical; see E. M. de Sá, [*The faces of the unit balls of
\(c\)-norms and \(c\)-spectral
norms*](https://doi.org/10.1016/0024-3795(94)00351-3).  Coey,
Kapelevich, and Vielma record the spectral cone, its nuclear-norm dual, and
the \(r+1\) barrier in [Section
4.7](https://optimization-online.org/wp-content/uploads/2020/05/7776.pdf).
The use of slack-operator factorizations as certificates for proper cone
lifts is due to Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://optimization-online.org/2011/11/3249/).
The companion
[shared-spectral note](2026-09-04-spectral-norm-product-sharing.md) proves
the exact cone, face, and barrier formulas used here.  The candidate new
contribution is the cone-independent whole-row rank/face theorem (6e), the
combined cap law (3), its exact resource frontier (4)--(6), and the
heterogeneous complexity boundary.  No priority claim is made pending a
specialist review.  A targeted title/abstract and full-text search over
spectral-ball faces, slack factorizations, and cone-lift lower bounds found
the ingredients above but no statement of (6e) or the two-cap exact
partition frontier; this is evidence, not a proof, of novelty.

The later
[universal contact-codimension theorem](2026-09-04-universal-whole-row-contact-codimension.md)
subsumes (6e) for arbitrary convex bodies and proves that equality in the
dimension bound is rigid up to a linear isomorphism of the shared
homogenization cone.  The present note retains the concrete matrix face
formula, capacity, barrier ledger, and complexity specialization.

This theorem optimizes over row-indivisible partitions: all rank-one polar
rows belonging to source \(a\) are assigned to one cone block, although
that block may be any proper cone.  It does not claim that a factorization
which splits one source row family among several blocks, or a nonlinear
extended formulation, must obey the same partition law.  The barrier
equalities in (4) concern the attaining shared-spectral construction; (6e)
does not by itself lower-bound the barrier parameter of every arbitrary
attaining cone.

## Audit targets

1. Check the function-rank argument in (6f), including the characterization
   and full linear span of rectangular spectral-ball extreme points.
2. Check the contact-cylinder normal form (6h), its restricted function
   rank, and the passage from image rank to exposed-face dimension.
3. Recheck the complementary-face dimension (8), especially rectangular
   and full-rank supported blocks, and verify the maximization in (10).
4. Check every floor and the smaller-last-group case in (5)--(6).
5. Verify the arbitrary-coupled ambient and slice barrier lower bounds.
6. Check the strong 3-PARTITION claim and the complex real-dimension factors.

## Independent audit record

An independent hostile audit passed all six targets.  Rectangular
coisometries are exactly the extreme points needed here; their convex hull
is the full spectral ball, so their real linear span is the full matrix
space.  On a contact cylinder, the fixed corner and vanished cross blocks
leave a coisometry of size \((r_a-1)\times(c_a-1)\), proving the restricted
function rank in (6e).  For a supported dual block of rank \(h\), the exact
face loss is \(h(r+c-h)\), minimized at \(h=1\), and losses add across
supported blocks.  The capacities, floors, smaller last group, storage,
and coupled barrier ledgers all check.  With \(r_a=1\) and \(F\geq D-1\),
the second cap is redundant and the problem is exactly bin packing;
strong 3-PARTITION keeps the explicit matrix description polynomial.
Over \(\mathbb C\), matrix and face dimensions double over the real
pairing, while the scale coordinate and barrier ranks remain unchanged.
