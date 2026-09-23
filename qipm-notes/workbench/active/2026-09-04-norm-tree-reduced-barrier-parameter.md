# Exact reduced barrier parameter of a capped Lorentz norm tree

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High in the exact self-concordance parameter and combinatorial optimum; no finite-precision claim

## Main theorem

Let \(T\) be a rooted norm tree with \(N\geq2\) leaves and \(L\) internal
nodes.  An internal node \(v\) has \(c_v\geq2\) children and contributes
one Lorentz block

\[
 (t_v,a_{v,1},\ldots,a_{v,c_v})\in Q_{c_v+1}.
\]

An internal child's axial coordinate is identified with the corresponding
parent slot; a leaf slot is a free projected coordinate.  Cone coordinates
that are not used are omitted.  On the linked cone, restrict the standard
product barrier

\[
 \Phi_T=-\sum_{v\ {\rm internal}}
 \log\!\left(t_v^2-\sum_{j=1}^{c_v}a_{v,j}^2\right).       \tag{1}
\]

After fixing the root axial coordinate to one, the exact self-concordance
parameter is

\[
 \boxed{
 \nu_T^{\rm red}=
 \begin{cases}
  2L-2,&\text{every root slot is an internal-child axis},\\
  2L-1,&\text{at least one root slot is a free leaf}.
 \end{cases}}                                               \tag{2}
\]

Thus the answer depends on the root incidence only, not on the root arity
or the shapes of the descendant subtrees.  The ambient linked product has
logarithmic-homogeneity degree \(2L\); fixing the root removes exactly two
units only when every root branch continues through another Lorentz block,
and exactly one unit otherwise.

## Exact optimum under a block-dimension cap

Fix a cap \(d\geq3\), so

\[
                 2\leq c_v\leq D:=d-1,
 \qquad          1\leq e_v:=c_v-1\leq a:=d-2.              \tag{3}
\]

Put

\[
 E=N-1,
 \qquad L_0=\left\lceil{E\over a}\right\rceil,
 \qquad
 \chi_{N,d}=
 \mathbf 1\!\left\{
 \begin{array}{l}
 L_0\geq3,\\[-1mm]
 E\leq (L_0-1)a+\min(D,L_0-1)-1
 \end{array}\right\}.                                     \tag{4}
\]

Equivalently, if \(\sigma=L_0a-E\in\{0,\ldots,a-1\}\) is the
unused arity capacity, then

\[
 \chi_{N,d}=1
 \quad\Longleftrightarrow\quad
 L_0\geq3\ \text{ and }\
 \sigma\geq\max\{0,d-L_0\}.                               \tag{4a}
\]

In particular, a count-minimal tree with an all-internal root always exists
once \(L_0\geq d\); below that threshold the exact answer depends on the
residual arity capacity.

Then the exact minimum of (1)'s reduced parameter over all such norm trees
is

\[
 \boxed{\quad
 \min_T\nu_T^{\rm red}=2L_0-1-\chi_{N,d}.
 \quad}                                                     \tag{5}
\]

The factor count \(L_0\) is always attainable.  The indicator in (4) says
exactly when a count-minimal tree can make every root child internal.  If
it cannot, adding one factor cannot help the parameter: it changes the best
possible value from \(2L_0-1\) to at least
\(2(L_0+1)-2=2L_0\).

Important edge cases are:

- If \(d\geq N+1\), then \(L_0=1\).  The direct
  \(Q_{N+1}\) representation has \(\nu_{\rm red}=1\).
- For \(d=3\), \(L_0=N-1\).  Equation (5) gives \(1\) for
  \(N=2\), \(3\) for \(N=3\), and \(2N-4\) for every
  \(N\geq4\).  In particular, it recovers the exact binary theorem.
- A binary comb always has a root leaf and hence parameter \(2N-3\).

## Comparison with the smooth grouped lift

In the genuinely capped regime \(3\leq d<N+1\), the contact-regular grouped
ball lift uses

\[
 h=\left\lceil{N\over d-2}\right\rceil                    \tag{6}
\]

Lorentz blocks and its explicitly reduced separable paraboloid barrier has
exact parameter \(h\).  In terms of \(L_0\),

\[
 h=L_0+\zeta_{N,d},
 \qquad
 \zeta_{N,d}=\mathbf1\{d-2\text{ divides }N-1\}.           \tag{7}
\]

Consequently the exact reduced-barrier gap is

\[
 \boxed{
 \min_T\nu_T^{\rm red}-\nu_{\rm grouped}^{\rm red}
 =L_0-1-\chi_{N,d}-\zeta_{N,d}\geq0.}                      \tag{8}
\]

Equality occurs only when either \(L_0=2\) and
\(N-1=2(d-2)\), or \((N,d)=(4,3)\).  Otherwise the smooth
grouped formulation has a strictly smaller displayed reduced parameter,
despite using at most one more cone block:

\[
                         h\in\{L_0,L_0+1\}.                 \tag{9}
\]

For growing \(L_0\), (5) versus (6) is asymptotically a factor-two
separation.  Both formulations retain linear-size, constant-treewidth
expanded Newton systems.  This is therefore a genuine formulation
tradeoff: the count-minimal recursive norm computation does not convert its
one-block saving into a smaller restricted standard-barrier parameter, and
usually pays nearly twice the grouped lift's parameter.  This is an exact
comparison of the two displayed barriers, not an iteration lower bound and
not an optimality claim for the standard barrier on the norm-tree slice.
The grouped barrier, unlike the norm-tree standard barrier, is known to be
optimal over arbitrary coupled barriers on its own affine slice by its
embedded-cube section.

For a Cartesian product of independent balls with leaf counts \(N_j\), the
same statement adds exactly.  If
\(L_j=\lceil(N_j-1)/(d-2)\rceil\) and \(\chi_j\) is given by (4), then the
best product of capped norm-tree barriers has

\[
       \nu_{\rm forest}^{\rm red}
       =\sum_j(2L_j-1-\chi_j),                              \tag{9a}
\]

whereas the product of smooth grouped barriers has parameter
\(\sum_j\lceil N_j/(d-2)\rceil\).  This follows because the Hessian and
gradient split blockwise, so the squared dual gradient norms, including
their sharp limiting sequences, add.

## Intrinsic barrier floor for the extended slice

The linear growth is not only an artifact of the standard product barrier.
Let \(\mathcal D_T\) be the linked norm-tree domain with its root fixed to
one.  Every \(\nu\)-self-concordant barrier \(B\) on \(\mathcal D_T\),
including a custom coupled barrier unrelated to (1), satisfies

\[
                              \boxed{\nu\geq L.}            \tag{9b}
\]

Consequently every barrier on a dimension-\(d\)-capped norm-tree
formulation has \(\nu\geq L_0\).  For a forest of independent norm trees,
the same construction gives the sum of their factor counts.  Combined with
\(h\in\{L_0,L_0+1\}\), the smooth grouped barrier is therefore always
within one parameter unit of this intrinsic norm-tree lower bound.  If
\(h=L_0\), no custom norm-tree barrier can have a smaller numerical
parameter than the displayed grouped barrier.

To prove (9b), choose positive leaf values of squared sum one, and set every
internal \(t_v^*\) to the Euclidean norm of its descendant leaves.  Every
block

\[
 q_v^*=(t_v^*,y_v^*)
\]

is then a nonzero Lorentz-boundary vector, all its child slots are positive,
and the linked root is one.  Let
\(\widehat q_v^*=(t_v^*,-y_v^*)\), and intersect the linked affine slice
with the product of two-planes

\[
 q_v=\alpha_vq_v^*+\beta_v\widehat q_v^*.
\]

Lorentz membership in each plane is exactly
\(\alpha_v,\beta_v\geq0\), since its determinant is
\(4(t_v^*)^2\alpha_v\beta_v\).  The root and link equations become

\[
 \alpha_r+\beta_r=1,
 \qquad
 \alpha_w+\beta_w=\alpha_v-\beta_v
 \quad(w\text{ an internal child of }v).                  \tag{9c}
\]

These \(L\) independent equations in \(2L\) variables define a bounded
\(L\)-dimensional polytope.  Indeed, the \(L\) values \(\beta_v\) are
affine coordinates: starting at the root, (9c) determines every
\(\alpha_v\), sufficiently small recursively chosen positive \(\beta_v\)
give relative-interior points, and nonnegativity bounds every coordinate.
At

\[
                         \beta_v=0,\qquad\alpha_v=1
                         \quad\text{for every }v,           \tag{9d}
\]

exactly the \(L\) facets \(\beta_v=0\) are active, with independent
coordinate normals.  Restricting \(B\) to this affine section preserves its
parameter and gives a barrier for the polytope.  The classical
Nesterov--Nemirovskii independent-active-facet lower bound now yields
\(\nu\geq L\).

Before the root is fixed, the same construction gives a distinct conic
lower bound.  Every logarithmically homogeneous self-concordant barrier on
the full linked norm-tree cone satisfies

\[
                         \boxed{\nu_{\rm LH}\geq L+1.}      \tag{9e}
\]

Without the root equation, the complementary-ray intersection is a regular
polyhedral cone of dimension \(L+1\).  At the nonzero ray
\(\beta=0,\alpha=1\), exactly the \(L\) independent \(\beta\)-facets are
active.  Hildebrand's sharpened conic active-facet theorem gives the extra
radial unit and hence (9e).  Equivalently, logarithmic homogeneity and the
root halfspace make root-slice restriction remove at least one parameter
unit, after which (9b) applies.  The extra unit in (9e) must not be asserted
for an arbitrary non-logarithmically-homogeneous barrier on the cone.

## 1. Root-slice identity

Before the root is fixed, (1) is logarithmically homogeneous of degree
\(2L\).  Its Hessian is positive definite on the linked cone and

\[
 Hx=-\nabla\Phi_T(x),
 \qquad
 \|\nabla\Phi_T(x)\|_{H^{-1}}^2=2L.                        \tag{10}
\]

Let \(e_t\) select the root coordinate \(t\).  Restricting a covector to
the tangent space \(e_t^Th=0\) is orthogonal projection in the
\(H^{-1}\) metric.  Therefore its exact squared dual norm on the slice is

\[
 \lambda_{\rm red}(x)^2
 =2L-{t^2\over e_t^TH^{-1}e_t}.                             \tag{11}
\]

Write

\[
 \beta_T(x)={e_t^TH^{-1}e_t\over t^2}.
\]

Restriction preserves standard self-concordance, so the exact parameter is

\[
 \nu_T^{\rm red}=2L-{1\over\sup_x\beta_T(x)}.              \tag{12}
\]

The problem is thus an exact root-leverage calculation.

## 2. A root leaf removes exactly one unit

The unit Dikin ellipsoid of (1) lies in the linked cone, which is contained
in the halfspace \(t>0\).  Applying Dikin containment in the direction
\(H^{-1}e_t\) gives

\[
                         e_t^TH^{-1}e_t\leq t^2.             \tag{13}
\]

Thus \(\beta_T\leq1\).  If a root slot is a free leaf, the bound is sharp.
Normalize \(t=1\), approach the root Lorentz boundary along that leaf,
scale every internal child subtree by the square of the root determinant,
and set the other leaf coordinates to zero.  The descendant axial
curvatures then decouple in the root Schur complement, while the selected
leaf gives the ordinary Lorentz boundary limit.  Hence

\[
                         \beta_T\longrightarrow1.           \tag{14}
\]

Equations (12)--(14) prove the second line of (2).

## 3. All-internal root removes exactly two units

Suppose the root has \(c\) internal children with axial coordinates
\(a_1,\ldots,a_c>0\).  Eliminate all strict descendants from the Hessian.
If \(h_i\) is child \(i\)'s resulting axial Schur curvature, Dikin
containment in that child cone gives

\[
                             h_i\geq a_i^{-2}.               \tag{15}
\]

Increasing any \(h_i\) can only increase the final root Schur complement.
It is enough to analyze

\[
 -\log\!\left(t^2-\sum_{i=1}^ca_i^2\right)
 -\sum_{i=1}^c\log a_i.                                    \tag{16}
\]

Normalize \(t=1\), and put

\[
 r=\sum_i a_i^2,
 \qquad q=1-r,
 \qquad
 Z=\sum_i{a_i^4\over q+2a_i^2}.                            \tag{17}
\]

A diagonal-plus-rank-one Sherman--Morrison elimination gives the root
Schur curvature \(S=(H^{-1})_{tt}^{-1}\):

\[
 S={2(1+r)-16Z/(q+4Z)\over q^2}.                            \tag{18}
\]

For fixed \(q\), the function

\[
 f(x)={x^2\over q+2x}
\]

has increasing ratio \(f(x)/x=x/(q+2x)\), and is therefore
superadditive.  Thus

\[
             Z\leq {r^2\over q+2r}={r^2\over1+r}.           \tag{19}
\]

The inequality \(S\geq2\) is equivalent to

\[
                  r(3-r)\geq4(2-r)Z.                        \tag{20}
\]

Substituting (19), the difference between the two sides is at least

\[
                         {3r(1-r)^2\over1+r}\geq0.          \tag{21}
\]

Therefore \(\beta_T\leq1/2\).  Conversely, scale every internal child
subtree by a common \(\epsilon\downarrow0\), keeping its normalized
interior point fixed.  The root cross terms vanish and \(S\to2\), so

\[
                         \sup_x\beta_T(x)={1\over2}.         \tag{22}
\]

Equations (12) and (22) prove the first line of (2), for every arity.

## 4. Exact tree combinatorics

Every rooted tree satisfies

\[
                         \sum_v(c_v-1)=N-1=E.               \tag{23}
\]

Since each increment \(e_v=c_v-1\) lies in \([1,a]\), (23) proves
\(L\geq L_0\), and distributing \(E\) among \(L_0\) such increments
constructs a tree attaining equality.

For every root child to be internal, a tree with \(L\) internal nodes must
have root arity \(c\leq L-1\).  After choosing its increment \(c-1\), the
remaining \(L-1\) increments must sum to \(E-(c-1)\).  Hence a count-minimal
all-internal root exists exactly when

\[
 L_0\geq3,
 \qquad
 \max\{1,E-(L_0-1)a\}
 \leq c-1\leq\min(D,L_0-1)-1                               \tag{24}
\]

for some integer \(c-1\).  This is equivalent to the condition in (4).
The remaining increments can be realized as a forest of \(c\) rooted
subtrees because \(c\leq L_0-1\); attaching that forest below the root
gives the required tree.  Combining this feasibility criterion with (2)
proves (5).

## 5. Literature and novelty boundary

The standard calculus used here is classical.  Affine inverse images preserve
self-concordance, direct products add certified parameters, and the
logarithmically homogeneous Lorentz barrier has parameter two
[[nesterov1994-interior-point-polynomial-algorithms-convex]] p.31-48
[[nesterov1997-self-scaled-barriers-and-interior]] p.3-4.  Recursive SOC
representations of Euclidean norms are also standard modeling devices.
The \(k+1\) logarithmically homogeneous lower bound at a nonzero conic
boundary point with \(k\) independent local facets is due to Hildebrand,
[*A lower bound on the optimal self-concordance parameter of convex
cones*](https://doi.org/10.1007/s10107-012-0576-1), Theorem 6.1.

A targeted search of the local corpus and the open literature for norm-tree
barriers, affine restrictions of Lorentz-product barriers, and exact
self-concordance parameters found only the general barrier calculus and SOC
modeling constructions.  It found no statement of the root-incidence law
(2), the arbitrary-arity Schur identity (18), the capped optimum (5), or the
exact comparison (8), or the intrinsic polyhedral sections (9b)--(9e).  The
potentially new content is this combination,
especially the fact that every root arity has the same one-versus-two-unit
loss and the resulting exact cap-dependent dominance by the smooth grouped
lift.  A targeted search cannot guarantee priority, so novelty remains
subject to specialist review.

### A failed coupled-barrier shortcut

The factor-two gap in (8) is not removed by the most obvious
Vinberg-style correction.  Already for the two-block comb, the
logarithmically homogeneous candidate

\[
 \widetilde F(t,x,a,y,z)=
 -\log(t^2-x^2-a^2)-\log(a^2-y^2-z^2)+\log a              \tag{25}
\]

has degree three but is not standard self-concordant.  At

\[
 (t,x,a,y,z)=(7.53063308,0.65289344,1.09961357,
              0.70307764,0.26203492)
\]

both Lorentz determinants are positive.  In direction

\[
 h=(0.32084830,-0.81823023,0.73165228,
    -0.50144002,0.87916062),
\]

direct univariate differentiation gives

\[
 D^2\widetilde F[h,h]=9.3444005923,\qquad
 |D^3\widetilde F[h,h,h]|=59.6440220551
 >2(D^2\widetilde F[h,h])^{3/2}=57.1290718162.             \tag{26}
\]

Thus any improvement over the standard restricted barrier needs a less
naive coupled construction.  Equation (9b) gives the exact current lower
endpoint \(L\), but whether it is attainable remains separate from (2).

## 6. Scope and audit

The result concerns the standard product Lorentz barrier after the link
equalities and root fixing are imposed.  It does not change the exact
ambient normal-barrier value \(2L\), prove that (2) is the best parameter of
any barrier on the extended feasible slice, or give an IPM iteration lower
bound.  The latent constant-treewidth Newton expansions and their linear
exact-arithmetic solves are unaffected.

An independent hostile audit checked (18) numerically against direct Schur
complements with one, two, three, and five internal-child axes, verified the
superadditivity step and the exact residual (21), and checked both sharpness
limits.  It also
verified the increment identity, the all-internal-root feasibility
condition (24), the construction of the descendant forest, and the claim
that adding a factor cannot improve (5).

A second independent audit verified the intrinsic lower bound (9b).  It
checked existence of the fully positive boundary tuple, the complementary-
ray coordinates, all root and link equations, full dimension and
boundedness of the polytope section, relative-interior feasibility, and
independence of the \(L\) active facets.  It also confirmed applicability of
affine restriction and the classical polytope barrier lower bound.  The
unfixed-root extension was separately checked against Hildebrand's conic
theorem: the extra radial unit in (9e) is valid for logarithmically
homogeneous barriers, but not claimed for arbitrary barriers.  No algebraic
or combinatorial defect remains.
