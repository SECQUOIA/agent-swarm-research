# Universal contact-codimension frontier for whole-row cone factorizations

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the whole-row model; novelty pending specialist review

## Result

Let \(C_a\subset\mathbb R^{n_a}\), \(a=1,\ldots,k\), be compact
full-dimensional convex bodies with \(0\in\operatorname{int}C_a\). Write

\[
 E_a=\operatorname{ext}C_a,\qquad
 P_a=\operatorname{ext}C_a^\circ,\qquad
 F_a(z)=\{x\in C_a:\langle x,z\rangle=1\},              \tag{1}
\]

and define the largest extreme-normal contact dimension and its codimension

\[
 e_a=\max_{z\in P_a}\dim F_a(z),\qquad
 \lambda_a=n_a-e_a.                                     \tag{2}
\]

Face dimension is affine dimension. Since \(F_a(z)\) is a proper exposed
face, \(1\leq\lambda_a\leq n_a\).

Fix a nonempty row group \(G\subseteq[k]\). Let
\(K\subseteq\mathbb R^m\) be any proper cone, and suppose arbitrary maps

\[
 A:\prod_{b\in G}E_b\longrightarrow K,\qquad
 B^a:P_a\longrightarrow K^*                              \tag{3}
\]

factor every labelled full slack row:

\[
 \langle A((x_b)_b),B^a(z)\rangle=1-\langle x_a,z\rangle
       \qquad(a\in G,\ z\in P_a).                        \tag{4}
\]

No continuity, differentiability, semialgebraicity, or homogeneity is
assumed. Put

\[
 f(K)=\max_{0\ne y\in K^*}\dim\operatorname{span}(K\cap y^\perp). \tag{5}
\]

Every factorization (3)--(4) satisfies

\[
 \boxed{
 m\geq1+\sum_{a\in G}n_a,\qquad
 f(K)\geq1+\sum_{a\in G}n_a-\min_{a\in G}\lambda_a.}     \tag{6}
\]

Both bounds are sharp simultaneously. The shared homogenization cone

\[
 \mathcal H_G(C)=
 \{(t,(x_a)_{a\in G}):t\geq0,\ x_a\in tC_a\ \forall a\in G\} \tag{7}
\]

is proper, has dimension \(1+\sum_Gn_a\), carries (4) through

\[
 A(x)=(1,(x_a)_a),\qquad
 B^a(z)=(1,0,\ldots,-z,\ldots,0),                         \tag{8}
\]

and has exact maximum complementary-face dimension

\[
 f(\mathcal H_G(C))
   =1+\sum_{a\in G}n_a-\min_{a\in G}\lambda_a.           \tag{9}
\]

Moreover, equality in the dimension bound is rigid: if
\(m=1+\sum_Gn_a\), then \(K\) is linearly isomorphic to
\(\mathcal H_G(C)\), and the factorization (3)--(4) is the canonical one
(8) up to that invertible change of coordinates. Thus changing the cone
cannot improve any linear-isomorphism invariant, including its optimal
barrier parameter or face lattice, at minimum ambient dimension. This
rigidity also applies when \(K\) itself is a product and the slack rows are
split among its factors. If \(\prod_aE_a\) is connected, equality in
ambient dimension forces that product to have exactly one nonzero factor.

Consequently, if each whole-row cone block has dimension at most \(D\) and
maximum proper exposed-face dimension at most \(F\), a group \(G\) is
feasible if and only if

\[
 \boxed{
 \sum_{a\in G}n_a\leq D-1,\qquad
 \sum_{a\in G}n_a-\min_{a\in G}\lambda_a\leq F-1.}      \tag{10}
\]

This is exact across arbitrary proper cones in the row-indivisible
whole-row model, not only within (7). For \(k\) identical bodies with
dimension \(n\) and contact codimension \(\lambda\), the exact per-block
capacity and minimum block count are

\[
 Q=\min\left\{
      \left\lfloor{D-1\over n}\right\rfloor,
      \left\lfloor{F+\lambda-1\over n}\right\rfloor
    \right\},\qquad
 L_{\min}=\left\lceil{k\over Q}\right\rceil,             \tag{11}
\]

provided \(Q\geq1\).

## 1. Functional-rank lower bound

The extreme points \(P_a\) affinely span \(\mathbb R^{n_a}\), because
\(C_a^\circ=\operatorname{conv}P_a\) is full-dimensional. Therefore the
vectors \((1,-z)\), \(z\in P_a\), linearly span
\(\mathbb R^{1+n_a}\). The row functions

\[
                     S_{a,z}(x)=1-\langle x_a,z\rangle   \tag{12}
\]

span the constant and every coordinate function of \(x_a\). Over all
\(a\in G\), they span the constant plus all \(\sum_an_a\) coordinates.

These functions are independent on \(\prod_aE_a\). Indeed, \(E_a\)
affinely spans \(\mathbb R^{n_a}\), because
\(C_a=\operatorname{conv}E_a\) is full-dimensional. If an affine function
on the product vanishes at every product extreme point, successively fixing
all but one block shows that every coefficient and the constant vanish.
By (4), every row function is a linear functional of \(A(x)\), so the
function rank is at most \(m\). This proves the first inequality in (6).

## 2. Contact-face lower bound

Fix \(a\in G\) and \(z\in P_a\). On the contact cylinder

\[
 \mathcal C_{a,z}=(F_a(z)\cap E_a)\times
                       \prod_{b\ne a}E_b,                \tag{13}
\]

the row \(S_{a,z}\) vanishes. Hence

\[
 A(\mathcal C_{a,z})\subseteq K\cap B^a(z)^\perp.        \tag{14}
\]

The dual factor \(B^a(z)\) is nonzero because \(S_{a,z}\) is not the zero
function. The extreme points of an exposed face are exactly
\(F_a(z)\cap E_a\), and their convex hull is \(F_a(z)\). Thus the affine
function rank on (13) is

\[
              1+\sum_{b\ne a}n_b+\dim F_a(z).            \tag{15}
\]

Every affine coordinate function in (15) is the restriction of a linear
combination of rows (12), hence of a linear functional on \(A(x)\).
Therefore the image span in (14), and thus the exposed face itself, has
dimension at least (15). Choose \(z\) attaining \(e_a\) and maximize over
\(a\):

\[
 f(K)\geq\max_a\{1+\sum_{b\ne a}n_b+e_a\}
       =1+\sum_bn_b-\min_a\lambda_a.                     \tag{16}
\]

This proves the second inequality in (6).

## 3. Exact faces of the shared homogenization cone

The dual of (7) is

\[
 \mathcal H_G(C)^*=\{(\alpha,(z_a)_a):
                 \alpha\geq\sum_a h_{C_a}(-z_a)\},       \tag{17}
\]

where \(h_C(z)=\max_{x\in C}\langle x,z\rangle\). At a nonzero dual
boundary point let \(J=\{a:z_a\ne0\}\). Pairing a primal point
\((t,(tx_a)_a)\) with it gives

\[
 t\sum_{a\in J}
       \bigl(h_{C_a}(-z_a)+\langle x_a,z_a\rangle\bigr). \tag{18}
\]

Every summand is nonnegative. Equality leaves \(x_a\) unrestricted for
\(a\notin J\), while for \(a\in J\) it restricts \(x_a\) to the exposed
minimizer face of \(z_a\). Hence the complementary face dimension is

\[
 1+\sum_{a\notin J}n_a+
       \sum_{a\in J}\dim\arg\min_{x\in C_a}\langle x,z_a\rangle. \tag{19}
\]

Extreme polar normals determine the largest possible contact dimension.
Normalize any nonzero exposing normal to a boundary point
\(z\in C_a^\circ\), and write it as a finite convex combination of extreme
points \(z_i\in P_a\). If \(\langle x,z\rangle=1\), every inequality
\(\langle x,z_i\rangle\leq1\) is tight, so

\[
                        F_a(z)=\bigcap_iF_a(z_i).         \tag{20}
\]

Thus \(\dim F_a(z)\leq\max_i\dim F_a(z_i)\leq e_a\).
Equation (19) loses at least \(\lambda_a\) dimensions for every supported
block. One block with minimum \(\lambda_a\), using an extreme normal that
attains \(e_a\), realizes that loss. This proves (9), and (6) plus (9)
prove (10)--(11).

## 4. Rigidity at minimum ambient dimension

Put \(N_G=\sum_{a\in G}n_a\) and
\(\widehat C_G=\prod_{a\in G}C_a\). The polar of this product is

\[
 \widehat C_G^\circ
  =\{(z_a)_a:\sum_a h_{C_a}(z_a)\leq1\}.                \tag{20a}
\]

Its nonzero extreme points are exactly the vectors supported on one block
\(a\), with that block in \(P_a\). Indeed, a point with two positive gauge
contributions is a nontrivial convex combination of single-block points,
and a nonzero point with total gauge below one has a nontrivial radial
decomposition with zero. A single-block boundary point is extreme exactly
when its nonzero block is extreme in \(C_a^\circ\). Hence (4) is the
ordinary full slack operator of \(\widehat C_G\).

Assume now \(m=N_G+1\). Define the canonical rank factorization

\[
 U(x)=(1,x)\in\mathbb R^{N_G+1},\qquad
 V(a,z)=(1,0,\ldots,-z,\ldots,0).                       \tag{20b}
\]

Both \(\{U(x):x\in\prod_aE_a\}\) and
\(\{V(a,z):a\in G,z\in P_a\}\) span \(\mathbb R^{N_G+1}\), by Section 1.
The slack operator has rank \(N_G+1\), so the images of \(A\) and \(B\)
also span \(\mathbb R^{N_G+1}\). Uniqueness of a full-rank bilinear
factorization therefore gives an invertible linear map \(T\) with

\[
                  A(x)=TU(x),\qquad
                  B^a(z)=T^{-T}V(a,z).                  \tag{20c}
\]

For completeness, pairing with the spanning canonical and conic dual
families shows that a finite linear relation among the \(U(x)\)'s holds if
and only if the same relation holds among the \(A(x)\)'s. Thus the
assignment \(U(x)\mapsto A(x)\) extends to an invertible \(T\). Pairing
again gives \(B=T^{-T}V\).

Taking conic hulls in (20c) gives

\[
 T\mathcal H_G(C)\subseteq K,\qquad
 T^{-T}\mathcal H_G(C)^*\subseteq K^*.                  \tag{20d}
\]

The second inclusion dualizes to the reverse of the first, proving
\[
                         K=T\mathcal H_G(C).
\]
This proves the rigidity claim. In particular, if a row partition into
\(g\) blocks has the minimum possible total dimension
\(\sum_an_a+g\), every block is individually a linear image of its shared
homogenization cone. Any exact barrier law already known for those shared
cones therefore holds for every dimension-minimal whole-row formulation,
not merely for the displayed construction.

### Factor count at the absolute dimension minimum

The preceding argument does not need a row assignment when it is applied
to the complete cone \(K=\prod_{i=1}^L K_i\). Any possibly split-row
factorization through that product still obeys

\[
                  \sum_{i=1}^L\dim K_i\geq N_G+1.       \tag{20e}
\]

If equality holds, (20d) makes the entire product linearly isomorphic to
\(\mathcal H_G(C)\). The projectivized extreme rays of
\(\mathcal H_G(C)\) are naturally homeomorphic to
\(\operatorname{ext}\widehat C_G=\prod_aE_a\). On the other hand, the
projectivized extreme rays of a product of \(L\) nonzero proper cones are
the disjoint union of the \(L\) factor ray spaces: every product-cone
extreme ray is supported in exactly one factor. Each factor-supported
piece is nonempty and both open and closed in the extreme-ray space.
Therefore

\[
 L\leq \#\pi_0\!\left(\prod_aE_a\right)                  \tag{20f}
\]

whenever the number of connected components is finite. In particular,
if every \(E_a\) is connected, then \(L=1\). This conclusion allows each
row factor \(B^a(z)\) to have arbitrary components in every \(K_i^*\); it
is stronger than the row-indivisible scope of the cap law (10), but only
at the absolute total-dimension equality in (20e).

One unconditional capped consequence survives beyond equality. If
\(\prod_aE_a\) is connected and every factor has dimension at most
\(d<N_G+1\), one factor cannot supply the slack rank, while equality in
(20e) cannot use two factors. Integrality therefore gives

\[
 \boxed{\sum_i\dim K_i\geq N_G+2,\qquad
        L\geq\max\left\{2,\left\lceil{N_G+2\over d}\right\rceil\right\}.}
                                                               \tag{20g}
\]

This requires no selected-factor regularity and permits arbitrary row
splitting. It is only a one-dimension topological gap; stronger
dimension-minus-two ball bounds need the additional smooth-factor
hypotheses developed elsewhere.

## 5. Specializations

- If every \(C_a\) is strictly convex, every contact face is a point, so
  \(e_a=0\) and \(\lambda_a=n_a\). Equation (10) becomes

  \[
   \sum_Gn_a\leq D-1,\qquad
   \sum_Gn_a-\min_Gn_a\leq F-1.                          \tag{21}
  \]

  This includes smooth strictly convex norm balls but requires neither
  smoothness nor central symmetry.
  If additionally every \(n_a\geq2\), then
  \(E_a=\partial C_a\) is connected. Thus every possibly split-row
  product-cone factorization of absolute minimum dimension
  \(1+\sum_an_a\) has exactly one nonzero cone factor.

- For a Euclidean ball in \(\mathbb R^{s_a}\), (7) is the shared Lorentz
  homogenization cone, and (21) is the heterogeneous product-ball law.

- If \(C_a\) is a polytope, some extreme polar normal exposes a facet, so
  \(e_a=n_a-1\) and \(\lambda_a=1\). Thus flat contacts have the opposite
  extreme behavior from strictly convex bodies: a group of total dimension
  \(N_G\) forces a cone face of dimension at least \(N_G\), and (7) has
  such a facet. For identical \(n\)-dimensional polytopes, the face-cap
  term in (11) is \(\lfloor F/n\rfloor\).
  If the product body has a simple vertex, its \((N_G+1)\)-dimensional
  homogenization has a simple extreme ray. Hildebrand's conic
  independent-facet lower bound and the dimension-parameter universal
  barrier then give the exact *LHSCB* value
  \(\nu_{\rm opt}^{\rm LH}=N_G+1\) for this one cone; the fixed product
  slice has exact ordinary SCB parameter \(N_G\). This conclusion is not
  asserted for a polytope with no simple vertex, nor is additivity asserted
  for an arbitrary coupled barrier on a product of such cones.

- For the real spectral-norm ball in
  \(\mathbb R^{r_a\times c_a}\), \(r_a\leq c_a\), a rank-one nuclear-polar
  normal exposes a face affinely isomorphic to the
  \((r_a-1)\times(c_a-1)\) spectral ball. Hence

  \[
     n_a=r_ac_a,\qquad e_a=(r_a-1)(c_a-1),\qquad
     \lambda_a=r_a+c_a-1,                                \tag{22}
  \]

  and (10)--(11) are the audited spectral face-capped grouping formulas.
  The coisometry extreme manifold is connected when \(c_a>r_a\).
  Consequently, for products of strictly rectangular real spectral balls,
  equality in (20e) forces one cone factor even if rows may split. For
  complex spectral balls the Stiefel extreme manifold is connected also
  in the square case, so the same conclusion always holds. Real square
  blocks have the two components of \(O(r_a)\), and (20f), rather than the
  one-factor conclusion, is the safe statement.

- Rigidity upgrades the known barrier ledgers from constructions to
  dimension-minimality theorems. For any row partition of \(k\) Euclidean
  balls into \(g\) blocks, every whole-row formulation of the minimum total
  dimension \(\sum_as_a+g\) has product cone linearly isomorphic to the
  corresponding shared homogenization product. Its exact optimal ambient
  barrier parameter is therefore \(k+g\), even allowing a coupled barrier,
  and its fixed body slice has exact parameter \(k\). For spectral balls,
  with \(R=\sum_ar_a\) after orienting \(r_a\leq c_a\), the corresponding
  exact values for every minimum-dimensional whole-row formulation are
  \(R+g\) and \(R\). Thus an exotic cone can improve neither barrier ledger
  without first paying additional ambient dimension or leaving the
  whole-row model.

The theorem is structural. It gives exact factor count, ambient dimension,
and face-cap feasibility for whole-row partitions, but no universal barrier
parameter: that requires a barrier for the particular cone (7). It does
not cover factorizations that distribute one labelled row family among
several cone blocks or nonlinear extended formulations.  Moreover, the
\(M\geq N_G+2\) split-row gap in (20g) cannot be strengthened universally
to \(M\geq N_G+L\): an independently audited
[\(Q_{s+1}^L\) family with path-connected extreme
set](2026-09-04-connected-extremes-additive-factor-gap-counterexample.md)
attains \(M=N_G+2\) for arbitrarily large \(L\), so the deficit from the
proposed additive bound is the unbounded quantity \(L-2\). The stronger
additive law remains valid
for a linear image of one normalized product-cone base, but not after
arbitrary additional affine coupling.

## Literature and novelty boundary

The slack-factorization/lift equivalence is classical; see Gouveia,
Parrilo, and Thomas, [*Lifts of Convex Sets and Cone
Factorizations*](https://optimization-online.org/2011/11/3249/).
Exposed-face polarity and the convex-hull theorem for extreme points are
standard finite-dimensional convex analysis, and uniqueness of a
full-rank bilinear factorization up to an invertible basis change is
elementary linear algebra. The spectral specialization
uses the classical face description in E. M. de Sá,
[*The faces of the unit balls of \(c\)-norms and \(c\)-spectral
norms*](https://doi.org/10.1016/0024-3795(94)00351-3).
The simple-vertex barrier corollary uses Hildebrand,
[*A lower bound on the optimal self-concordance parameter of convex
cones*](https://optimization-online.org/2011/06/3068/), Theorem 6.1, and
Lee and Yue, [*Universal Barrier is
\(n\)-Self-Concordant*](https://arxiv.org/abs/1809.03011), Theorem 2.
The fixed-slice lower is Nesterov--Nemirovskii, Proposition 2.3.6, as
quoted precisely in Lee--Yue's Remark 2; Lee--Yue supplies the matching
universal-barrier upper. These hypotheses are why no all-polytope or
coupled-product barrier equality is claimed.

A targeted title/abstract and full-text search for cone-factorization lower
bounds based on contact-face dimension or minimum-dimensional cone lifts
found the general lift framework and facial obstructions, but not the exact
arbitrary-body theorem (6), the attaining shared cone (7)--(9), the
rigidity conclusion (20a)--(20d), or the two-cap partition law (10). Their
priority remains subject to specialist review.

## Audit targets

1. Check that extreme points of each body and polar affinely span the full
   spaces and that this proves the exact function rank in Section 1.
2. Check the extreme points of an exposed face, and the image-rank-to-face
   step in (15)--(16).
3. Check the dual cone (17), face dimensions in (19), and extreme-normal
   reduction (20), including nonsmooth bodies.
4. Check the characterization of the product-polar extreme points and the
   full-rank factorization uniqueness in (20a)--(20d).
5. Check the projective extreme-ray topology of a product cone and the
   component bound (20f), the capped consequence (20g), and real and
   complex Stiefel manifolds.
6. Check both cap inequalities and the floors in (11).
7. Verify the strictly convex, polyhedral, and spectral specializations and
   every scope limitation.

## Independent audit record

An independent hostile audit passed the original five targets. It checked the affine
spans of both extreme sets, the exact restricted function rank on every
contact cylinder, and the passage from that rank to the span dimension of
the complementary cone face. It also rederived (17)--(20), including the
finite extreme-point decomposition of a nonextreme polar normal and the
intersection identity for its contact face. The dimension losses add across
supported blocks, so one block of minimum contact codimension gives the
unique maximum formula (9). The two cap inequalities, identical-body
floors, and strictly convex, polyhedral, and rectangular spectral
specializations all check. No regularity assumption was used.

A follow-up hostile audit passed the minimum-dimension rigidity theorem.
It checked the product-polar extreme-point characterization, the common
invertible change of basis forced by full-rank bilinear-factorization
uniqueness, and both conic-hull inclusions in (20d). The canonical primal
rays generate \(\mathcal H_G(C)\), and the canonical dual row rays generate
its entire dual, so dualizing does force equality rather than only an
intermediate cone.

A third hostile audit checked the split-row topological consequence. After
normalizing rays by an interior dual functional, the extreme-ray space of a
finite cone product is the clopen disjoint union of its factor-supported
ray spaces. For \(\mathcal H_G(C)\), the \(t=1\) section identifies that
space with \(\prod_aE_a\). Thus the component bound (20f) is invariant
under the isomorphism from the rigidity theorem. The connectedness claims
for strictly convex boundaries and real rectangular or complex Stiefel
manifolds were checked separately. The auditor also checked (20g): rank
forces \(M\geq N_G+1\), the component obstruction excludes equality under
a strict cap, and integrality plus \(M\leq Ld\) gives exactly the displayed
factor-count floor.
