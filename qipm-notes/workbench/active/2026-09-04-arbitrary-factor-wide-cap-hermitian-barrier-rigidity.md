# Arbitrary-factor wide-cap Hermitian barrier rigidity

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; targeted surrounding-literature screen
complete, but specialist priority review remains necessary

## Theorem

Let \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(a=\dim_{\mathbb R}\mathbb F\), fix \(R\geq2\), and set

\[
                         B=a(R-1).                       \tag{1}
\]

Let \(q\geq2\) satisfy the wide-cap condition

\[
                         B\geq q-1.                      \tag{2}
\]

Every bounded, relative-Slater affine lift of

\[
                         B_2^{qB+1}                     \tag{3}
\]

over an arbitrary finite product of cones
\(H_+^{r_i}(\mathbb F)\), \(r_i\leq R\), and nonnegative rays has
restricted standard product-logdet parameter

\[
                    \boxed{\nu_{\rm std,slice}\geq q+1}. \tag{4}
\]

The grouped Hermitian Schur lift attains \(q+1\).  The audited
recession-direction theorem gives the same lower bound for every
unbounded lift in the divisible regime.  Hence (4) is the exact
standard-barrier frontier among all finite affine lifts in every
divisible wide-cap case, with no factor-count-minimality assumption and
no global selection hypothesis.

For fixed block type, the only bounded divisible cases still open after
this theorem have

\[
                         q\geq B+2.                      \tag{5}
\]

The identical spin-factor argument, with \(B=d-2\), is recorded in the
[arbitrary-factor wide-cap Lorentz
theorem](2026-09-04-arbitrary-factor-q2-lorentz-barrier-rigidity.md).
In particular, every quotient-two case \(q=2\) is closed over all three
Hermitian fields and for every \(R\geq2\).

## 1. Universal face-codimension budget

Homogenize the compact affine slice to a proper conic lift

\[
              C=L\cap K\ \xrightarrow{\ \Pi\ }\ Q_{qB+2}. \tag{6}
\]

Let \(X\in C\) lie over a target extreme ray, let \(E_X\) be the linear
span of its minimal product-cone face, let \(N=\dim K\), and put

\[
                         D(X)=N-\dim E_X.                 \tag{7}
\]

If \(k=\dim\ker(\Pi|_L)\), every \(H\in L\cap E_X\) gives two-sided small
perturbations \(X\pm\epsilon H\in C\).  The space of actual two-sided
feasible directions at a relative-interior point of a Lorentz extreme ray
is the span of that ray, so

\[
                 \Pi(L\cap E_X)\subseteq\operatorname{span}\{\Pi X\},
 \qquad
                 \dim(L\cap E_X)\leq k+1.                \tag{8}
\]

Since \(\dim L=qB+2+k\), Grassmann's inequality gives

\[
 k+1\geq\dim(L\cap E_X)
       \geq(qB+2+k)+(N-D(X))-N,                           \tag{9}
\]

and hence the factor-count-independent bound

\[
                         \boxed{D(X)\geq qB+1}.           \tag{10}
\]

This lemma uses only bounded properness and the target Lorentz face; it is
valid for every product-cone dictionary.

## 2. Wide caps force constant boundary nullity

Write

\[
 h_a(r)=\dim_{\mathbb R}H^r(\mathbb F)
       =r+{a r(r-1)\over2}.                              \tag{11}
\]

If a block of order \(r\leq R\) has \(\mathbb F\)-nullity \(m\), the
codimension of its minimal face is

\[
 \begin{aligned}
 h_a(r)-h_a(r-m)
 &=m+{a m(2r-m-1)\over2}\\
 &\leq m\,[1+a(R-1)]
   =m(B+1).                                               \tag{12}
 \end{aligned}
\]

A zero nonnegative ray also obeys the same per-nullity bound.  Summing over
all factors yields

\[
                         D(X)\leq(B+1)\operatorname{nul}_{\mathbb F}X. \tag{13}
\]

Suppose for contradiction that \(\nu_{\rm std,slice}<q+1\).  Determinant
orders are integers, so the segment-to-Slater test gives

\[
                         \operatorname{nul}_{\mathbb F}X\leq q          \tag{14}
\]

for every tuple in every lifted boundary fiber.  If the nullity were at
most \(q-1\), (2), (10), and (13) would give

\[
 qB+1\leq D(X)\leq(q-1)(B+1)
                 =qB+1-(B-q+2)<qB+1,                    \tag{15}
\]

a contradiction.  Therefore

\[
                  \boxed{\operatorname{nul}_{\mathbb F}X=q}            \tag{16}
\]

at every point of every boundary fiber.

Every boundary fiber is a singleton.  Otherwise, a maximal nonzero affine
chord from a relative-interior point of the fiber ends on the boundary of
its minimal product-cone face, where total nullity is at least \(q+1\).
Let \(X(v)\) denote the unique normalized lift of \(v\in S^{qB}\).
Compactness and the closed graph property make

\[
                         v\longmapsto X(v)                \tag{17}
\]

continuous.

## 3. Saturation fixes the same \(q\) blocks globally

The generic Hermitian exposed-rank theorem and (14) force equality
throughout the cross-Peirce capacity chain on a dense open semialgebraic
subset:

\[
 qB\leq a\sum_i p_iq_i
     \leq a\sum_i(r_i-q_i)q_i
     \leq B\sum_iq_i
     \leq qB.                                             \tag{18}
\]

Thus exactly \(q\) full order-\(R\) blocks have certificate rank one and
primal rank \(R-1\); every other block is interior.  Equivalently, the
generic primal tuple has one null line in each of \(q\) full blocks.

There are finitely many possible active block sets.  Fix one such set
\(I\).  Along a convergent sequence in its generic region, continuity of
(17) preserves its \(q\) null directions.  An active block cannot lose a
second eigenvalue, and an inactive block cannot acquire a zero eigenvalue,
because either event would violate (16).  Hence the closure of the region
for \(I\) retains exactly the same active blocks, each of corank one.

Closures belonging to distinct active sets are disjoint.  Their finite
union covers \(S^{qB}\), because the generic set is dense.  Connectedness
therefore forces one fixed set of \(q\) full order-\(R\) blocks to be active
for every support direction; every other factor is interior everywhere on
the lifted boundary sphere.

## 4. Projective-product contradiction

The \(q\) null lines define a continuous map

\[
       \Phi:S^{qB}\longrightarrow
       M:=\bigl(\mathbb F P^{R-1}\bigr)^q,
       \qquad \dim_{\mathbb R}M=qB.                       \tag{19}
\]

This map is injective.  If \(\Phi(v)=\Phi(w)\), the two tuples \(X(v)\) and
\(X(w)\) lie in the relative interior of the same product face span \(E\):
in each active block, \(E\) consists of Hermitian matrices supported on
the common null-line orthogonal complement, and all inactive factors are
unrestricted.

For \(H\in L\cap E\), both \(X(v)\pm\epsilon H\) lie in \(C\) for small
\(\epsilon\).  Their target images are two-sided perturbations of an extreme
Lorentz ray, so \(\Pi H\in\operatorname{span}\{\Pi X(v)\}\).  After positive
height normalization, both perturbed tuples lie in the boundary fiber over
\(v\).  Its singleton property gives

\[
                         L\cap E=\operatorname{span}\{X(v)\}.            \tag{20}
\]

Thus \(X(w)\) is proportional to \(X(v)\).  Equal homogenizing height gives
\(X(w)=X(v)\), and hence \(w=v\).

Invariance of domain now makes (19) a homeomorphism, because its source and
target are compact connected manifolds of dimension \(qB\).  This is
impossible.  With mod-two coefficients, \(M\) has nonzero intermediate
cohomology in degree \(a\) (degree one, two, or four in the real, complex,
or quaternionic case), whereas

\[
                         H^a(S^{qB};\mathbb Z/2)=0         \tag{21}
\]

because \(0<a<qB\).  The contradiction proves (4).

## 5. Consequence for the remaining seam problem

The projection-singular seam can survive only when \(q\) is large compared
with the block capacity:

\[
                         q\geq B+2.                       \tag{22}
\]

Only in this narrow-cap regime does the universal codimension budget allow
a boundary fiber point of nullity below \(q\).  Such a point is necessary
for a positive-dimensional compact fiber and hence for generic active
blocks to switch.  The incidence-space reduction in the companion note
describes the remaining strict-complementarity branch locus.

The theorem concerns the standard product Jordan log-determinant after
affine restriction.  It does not lower-bound arbitrary custom barriers or
unrestricted quantum query complexity.

## Audit checklist

1. Verify the universal face-codimension bound (10) over all three fields.
2. Recheck the Hermitian face-dimension formula (12), including quaternionic
   real dimensions.
3. Check the strict wide-cap comparison in (15), especially \(B=q-1\).
4. Verify the compact-fiber singleton argument and continuity of (17).
5. Check saturation in (18) and the fixed-active-set closure argument.
6. Verify injectivity in (19)--(20), invariance of domain, and the three
   projective-space cohomology obstructions.

## Independent hostile audit

The audit reconstructed the proof without using factor-count minimality.
For a target extreme ray, every direction in the source minimal-face span
is two-sided feasible at the lifted point.  Its image must lie in the
one-dimensional lineality of the target extreme ray, so Grassmann's
inequality gives \(D(X)\geq qB+1\) exactly as in (8)--(10).

For \(\mathbb F=\mathbb R,\mathbb C,\mathbb H\), respectively,
\[
 h_a(r)=\frac{r(r+1)}2,\quad r^2,\quad 2r^2-r.
\]
Subtracting \(h_a(r-m)\) gives (12).  Removing each null direction costs
at most \(1+a(R-1)=B+1\), including quaternionic blocks, while a zero ray
costs one.  At the endpoint \(B=q-1\),
\((q-1)(B+1)=qB\), still one below the required \(qB+1\), so (15) is
strict in the full claimed range.

The audit also checked the global step.  Constant nullity \(q\) makes
every compact boundary fiber a singleton and its inverse continuous.
Equality in (18) forces exactly \(q\) full-order, rank-one certificate
blocks: a smaller block or a certificate rank above one makes the
capacity inequality strict, and a ray has zero mixed capacity.  Along a
closure, an old active block cannot gain another null direction and a
new block cannot become singular.  Hence closures of different finite
label sets are disjoint and cover the connected sphere, fixing one label
set globally.

Finally, equal projective kernel lines put two lifted tuples in the
relative interior of the same product-face span.  The two-sided
extreme-ray argument and singleton normalization force this intersection
with \(L\) to be one ray, proving injectivity.  Invariance of domain
would identify \(S^{qB}\) with
\((\mathbb F P^{R-1})^q\), contradicted by nonzero mod-two cohomology in
degree \(a\) for the product and its vanishing on the sphere.  No
mathematical defect was found.
