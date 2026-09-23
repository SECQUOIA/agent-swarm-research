# The exact selection-free Lorentz exposed-rank frontier

Status: Proved; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the theorem and constants; novelty pending specialist review

## Result

Fix \(d\geq3\), put \(c=d-2\), and consider finite affine lifts of the
Euclidean ball \(B_2^s\) through products of Lorentz cones of real dimension
at most \(d\). Assume relative Slater and attainment of the genuine conic
dual certificates of every support inequality. For a lift \(\mathcal L\),
let \(\mathcal D_{\mathcal L}(v)\) be the **full** certificate fiber of
\(1-v^Tx\), and set

\[
 R(\mathcal L)=
 \max_{v\in S^{s-1}}\ \min_{Z\in\mathcal D_{\mathcal L}(v)}
       \sum_i\operatorname{rank}_J Z_i.                         \tag{1}
\]

Then the exact selection-free minimax frontier is

\[
 \boxed{\displaystyle
   \inf_{\mathcal L}R(\mathcal L)
      =q_{\rm sf}(s,d):=\left\lceil {s-1\over d-2}\right\rceil .}
                                                                    \tag{2}
\]

The lower bound follows by taking a semialgebraic minimum-rank certificate
selector and a semialgebraic primal contact selector, then restricting both
to a common full-dimensional \(C^1\) stratum. There the mixed-curvature
identity has rank \(s-1\), while one exposed Jordan-rank unit in a Lorentz
factor of dimension at most \(d\) carries at most \(d-2\) mixed directions.

The upper bound is attained by the explicit nested Lorentz chain below.
For this chain every support certificate is unique, has total rank at most
\(q_{\rm sf}\), and has rank exactly \(q_{\rm sf}\) on a dense open set.
Its primal boundary fiber is also unique. Both matrix-valued boundary
selections are globally Lipschitz and semialgebraic (they are built from
prefix norms), and analytic away from their rank-birth seams. Thus even
global bi-Lipschitz, \(W^{1,\infty}\), and almost-everywhere \(C^1\)
regularity do not restore the premium: everywhere \(C^1\) contact-support
regularity is substantive. There is no hidden higher-rank certificate in
the chain's fibers.

In contrast, the audited globally bi-\(C^1\) selected-sheet frontier is

\[
 h_d(s)=
 \begin{cases}
  1,&d\geq s+1,\\[1mm]
  \lceil s/(d-2)\rceil,&d<s+1.
 \end{cases}                                                     \tag{3}
\]

The two frontiers differ by one exactly in the strict-cap divisible cases
\(d<s+1\) and \(d-2\mid s-1\). Hence the divisibility premium in (3) is a
global contact-regularity cost, not an unconditional property of an affine
lift. The real, complex, and quaternionic \(2\times2\) Hermitian cones are
Lorentz cones of dimensions \(3,4,6\), so (2) specializes to

\[
 \left\lceil{s-1\over1}\right\rceil,\qquad
 \left\lceil{s-1\over2}\right\rceil,\qquad
 \left\lceil{s-1\over4}\right\rceil.                            \tag{4}
\]

The chain also separates exposed rank from standard-barrier complexity.
The restriction of its standard product log-determinant to the lifted
affine slice has exact self-concordant parameter

\[
                         \nu_{\rm slice}=2q_{\rm sf}-1.          \tag{5}
\]

For the first nontrivial real-PSD example \(s=d=3\), every certificate has
rank at most two, but \(\nu_{\rm slice}=3\). At the pole the first primal
\(2\times2\) block is zero and the second is rank one, so total primal
nullity is three. Smooth strict complementarity fails exactly where this
extra nullity is born.

A companion grouped rotated-Lorentz perspective shows that this rank birth
cannot be promoted to an every-completion theorem. For the same
\(q_{\rm sf}\), every boundary fiber of that lift contains a primal
completion of nullity exactly \(q_{\rm sf}\), and every support-certificate
fiber has maximum rank exactly \(q_{\rm sf}\). Its restricted standard
barrier still has parameter \(2q_{\rm sf}-1\), witnessed by higher-nullity
vertices inside one non-singleton pole fiber. See
[Rotated Lorentz perspectives refute the fiberwise nullity
premium](2026-09-04-rotated-lorentz-fiberwise-nullity-counterexample.md).

### QIPM-facing movement consequence

At the hard support supplied by (2), **every** genuine exposing slack has
Jordan rank at least \(q_{\rm sf}\). Applying the audited exposed-rank
distance theorem to any one such slack gives, for a fixed interior
reference point \(X^c\),
\[
 d_F\!\left(X^c,\{\text{objective gap}\leq\epsilon\}\right)
   \geq \sqrt{q_{\rm sf}}\log(1/\epsilon)-O_{\mathcal L,X^c}(1).
                                                                    \tag{5a}
\]
The finite constant is the theorem's support-minor reference constant and
need not be uniform over formulations. The grouped chain shows that the
\(\sqrt{q_{\rm sf}}\) exposed-rank coefficient cannot be improved from
certificate rank alone, even though its full restricted barrier parameter
is \(2q_{\rm sf}-1\).

Equation (5a) is a path-independent metric-movement lower bound. It becomes
an iteration lower bound only for an algorithm model that bounds intrinsic
movement per counted round, such as a fixed number of strict Dikin chords;
it is not an unrestricted QIPM runtime lower bound.

## 1. Why every affine Lorentz lift pays \(q_{\rm sf}\)

All data of a finite affine Lorentz lift are semialgebraic. For each
\(v\in S^{s-1}\), choose a primal lift over the contact \(x=v\), and choose
from \(\mathcal D_{\mathcal L}(v)\) a certificate of minimum integer total
rank. The sets \(\{\sum_i\operatorname{rank}Z_i\leq k\}\) are closed
semialgebraic, so definable choice supplies semialgebraic selectors. A
finite common stratification makes both selectors \(C^1\) on some
full-dimensional stratum of the sphere.

On that stratum the genuine certificate identity

\[
          \sum_i\langle X_i(u),Z_i(v)\rangle=1-u^Tv             \tag{6}
\]

holds for every selected feasible primal point \(X(u)\). At \(u=v\),
termwise complementarity leaves only cross-Peirce derivatives. Twice
differentiating (6) in independent tangent directions gives the identity
map on \(T_vS^{s-1}\), of rank \(s-1\). In a Lorentz factor, the only
productive complementary ranks are \(p_i=q_i=1\); its cross-Peirce space
has dimension \(\dim Q_i-2\leq d-2\). Blocks with \(q_i=0\), \(q_i=2\),
or a ray face have zero mixed capacity. Therefore

\[
 s-1\leq\sum_i(\dim Q_i-2)q_i
          \leq(d-2)\sum_iq_i.                                   \tag{7}
\]

Because the selected certificate minimizes rank in its full fiber, (7)
proves \(R(\mathcal L)\geq q_{\rm sf}\). Relative Slater is only a clean
way to ensure the stated certificate fibers and contact selectors. After
facial reduction, every proper nonzero Lorentz face is a ray, which has
zero mixed capacity, so the same proof applies to a non-Slater
representation whenever all support certificates are attained.

## 2. The affine norm chain attaining the bound

Write
\[
 Q_{1+k}=\{(\tau,z)\in\mathbb R\times\mathbb R^k:
                              \tau\geq\|z\|_2\}.
\]
Put \(q=q_{\rm sf}(s,d)\), and partition the coordinates into nonempty
ordered groups \(G_1,\ldots,G_q\) with

\[
                  |G_1|\leq d-1,\qquad |G_j|\leq d-2\quad(j\geq2).
                                                                    \tag{8}
\]

Such a partition exists because its total capacity is
\((d-1)+(q-1)(d-2)=q(d-2)+1\geq s\). When \(q=1\), use the direct
constraint \((1,x)\in Q_{s+1}\). Suppose below that \(q\geq2\), and impose

\[
\begin{aligned}
 X_1&=(t_1,x_{G_1})\in Q_{1+|G_1|},\\
 X_j&=(t_j,t_{j-1},x_{G_j})\in Q_{2+|G_j|},
       &&2\leq j\leq q-1,\\
 X_q&=(1,t_{q-1},x_{G_q})\in Q_{2+|G_q|}.                       \tag{9}
\end{aligned}
\]

Every factor in (9) has dimension at most \(d\). The nested inequalities
give

\[
 t_1^2\geq\|x_{G_1}\|^2,\qquad
 t_j^2\geq t_{j-1}^2+\|x_{G_j}\|^2,\qquad
 1\geq t_{q-1}^2+\|x_{G_q}\|^2.                                \tag{10}
\]

Thus feasibility implies \(\|x\|_2\leq1\). Conversely, take

\[
                 t_j=\left(\sum_{\ell=1}^j
                                      \|x_{G_\ell}\|^2\right)^{1/2}.
                                                                    \tag{11}
\]

Then (10) holds whenever \(\|x\|_2\leq1\), so the projection is exactly
\(B_2^s\). At \(x=0\), any \(0<t_1<\cdots<t_{q-1}<1\) gives Slater.
The fibers are compact. At a boundary point \(x=v\), all inequalities in
(10) are equalities, so the primal contact fiber is a singleton.

## 3. The full dual certificate fiber of the chain

For \(v\in S^{s-1}\), define

\[
       \rho_j=\left(\sum_{\ell=1}^j\|v_{G_\ell}\|^2\right)^{1/2},
       \qquad 1\leq j\leq q,                                   \tag{12}
\]

so \(\rho_q=1\). In the standard Euclidean self-dual pairing, set

\[
\begin{aligned}
 Z_1(v)&=(\rho_1,-v_{G_1}),\\
 Z_j(v)&=(\rho_j,-\rho_{j-1},-v_{G_j}),
               &&2\leq j\leq q.                               \tag{13}
\end{aligned}
\]

Every \(Z_j(v)\) is a Lorentz-boundary element, or zero, and the lifted
variables telescope:

\[
                 \sum_{j=1}^q\langle X_j,Z_j(v)\rangle=1-v^Tx. \tag{14}
\]

Thus (13) is a genuine certificate on the whole affine slice.

It is the only certificate. In an arbitrary candidate, let \(\alpha_j\)
be block \(j\)'s temporal coordinate. Coefficient matching forces its
spatial coordinates to be

\[
 -v_{G_1}\quad(j=1),\qquad
 (-\alpha_{j-1},-v_{G_j})\quad(j\geq2),\qquad \alpha_q=1.       \tag{15}
\]

Lorentz positivity yields

\[
 \alpha_1\geq\rho_1,\qquad
 \alpha_j\geq\sqrt{\alpha_{j-1}^2+\|v_{G_j}\|^2}\quad(j\geq2). \tag{16}
\]

Since \(\alpha_q=1=\rho_q\), backward equality forces
\(\alpha_j=\rho_j\) at every stage. Hence
\(\mathcal D(v)=\{Z(v)\}\), with

\[
 Q(v)=\#\{j:\rho_j>0\}\leq q.                                 \tag{17}
\]

On the dense open set \(v_{G_1}\ne0\), every prefix is positive and
\(Q(v)=q\). If \(v\) is supported in the final group, then only the final
block is nonzero and \(Q(v)=1\). Equations (7) and (17) prove (2).

### The binary real-PSD instance

For \(d=3\), every group after the first is a singleton, the first has two
coordinates, and \(q=s-1\). Under the standard isomorphism

\[
 M(\tau,u,w)=
 \begin{pmatrix}\tau+u&w\\w&\tau-u\end{pmatrix},
\]

the chain (9) becomes

\[
\begin{aligned}
 X_1&=M(t_1,x_1,x_2),\\
 X_j&=M(t_j,t_{j-1},x_{j+1}), &&2\leq j\leq s-2,\\
 X_{s-1}&=M(1,t_{s-2},x_s).
\end{aligned}                                                   \tag{18}
\]

The trace pairing obeys

\[
 \operatorname{tr}\!\left(
 M(a,b,c)\,{1\over2}M(d,e,f)\right)=ad+be+cf,
\]

so Lorentz certificates in (13) correspond to one-half the displayed PSD
matrices. For \(s=3\), if \(v=(c_1,c_2,e)\) and
\(\rho=\sqrt{c_1^2+c_2^2}\), then

\[
 Z_1(v)={1\over2}M(\rho,-c_1,-c_2),\qquad
 Z_2(v)={1\over2}M(1,-\rho,-e).                                \tag{19}
\]

As \(v\to e_3\), the first block collapses at rate \(\rho\), while its
normalized support depends on \((c_1,c_2)/\rho\). The unique certificate
map is continuous, Lipschitz, semialgebraic, and compact-valued, but its
support has no continuous extension and the map is not two-sided
differentiable at the pole. Uniqueness, closed graph, compact fibers,
semialgebraicity, and Slater therefore do not recover the missing smooth
support sheet.

## 4. Exact restricted standard-barrier parameter

Let \(\Omega\) be the interior of the affine lifted slice (9), and let

\[
                    F=-\sum_{j=1}^q\log\det_J X_j.              \tag{20}
\]

The ambient product barrier is \(2q\)-logarithmically homogeneous. The
slice fixes the temporal coordinate of the final Lorentz block to one.
Let \(\ell\) extract that coordinate. For every ambient interior point
\(X\), \(\ell(X)=1\) on the slice and

\[
                  \|\ell\|_{F''(X),*}\leq\ell(X)=1.             \tag{21}
\]

Indeed, under quadratic scaling, the dual local norm of a positive Jordan
functional is the Euclidean norm of a positive Jordan element, while its
value on \(X\) is that element's trace; the Euclidean norm of a
nonnegative spectrum is at most its trace. The affine tangent space is
contained in \(\ker\ell\). The ambient Newton vector has squared norm
\(2q\), and its metric-orthogonal distance to \(\ker\ell\) is
\(\ell(X)^2/\|\ell\|_{F''(X),*}^2\geq1\). Orthogonal projection onto the
smaller affine tangent space therefore gives

\[
             \|F'|_{\Omega}\|_{(F|_{\Omega})'',*}^2
                         \leq2q-1.                              \tag{22}
\]

This is exactly the barrier-parameter inequality.

It is sharp. Choose the groups so the last group contains coordinate \(s\).
Start at the pole \(x=e_s,t_j=0\) and enter the slice along the affine ray

\[
 x_s=1-\varepsilon,\quad x_1=\cdots=x_{s-1}=0,\quad
 t_j=a_j\varepsilon,\qquad 0<a_1<\cdots<a_{q-1},               \tag{23}
\]

for sufficiently small \(\varepsilon>0\). Along this ray, the first
\(q-1\) determinants are positive constants times \(\varepsilon^2\), while

\[
 \det_J X_q
 =1-a_{q-1}^2\varepsilon^2-(1-\varepsilon)^2
 =2\varepsilon+O(\varepsilon^2).                               \tag{24}
\]

Thus

\[
 F(\varepsilon)=-(2q-1)\log\varepsilon+O(1),\quad
 F'(\varepsilon)=-{2q-1\over\varepsilon}+O(1),\quad
 F''(\varepsilon)={2q-1\over\varepsilon^2}+O(1).               \tag{25}
\]

Testing the local dual gradient norm on this one affine direction gives

\[
 \sup_{\Omega}\|F'\|_{F'',*}^2
   \geq\lim_{\varepsilon\downarrow0}{F'(\varepsilon)^2\over
                                               F''(\varepsilon)}
   =2q-1.                                                       \tag{26}
\]

Together with (22), this proves (5). The same proof covers \(q=1\), where
the direct ball slice has exact parameter one.

## 5. Product-ball consequence: what is and is not proved

For a lift \(\mathcal L\) of \(\prod_{a=1}^bB_2^{s_a}\) and fixed positive
weights \(\lambda_a\), define the favorable-certificate quantity
\[
 R_{\rm fav}(\mathcal L)=
 \sup_{\substack{u\in\prod_aS^{s_a-1}\\
                  Y^a\in\mathcal D_a(u_a)}}
 \sum_i\operatorname{rank}_J\!\left(\sum_a\lambda_aY_i^a\right).
\]
Sequential compression and separate norm chains give the exact
heterogeneous frontier
\[
 \boxed{\displaystyle
   \inf_{\mathcal L}R_{\rm fav}(\mathcal L)
      =\sum_{a=1}^b q_{\rm sf}(s_a,d).}                          \tag{27}
\]
It makes the gap from the bi-\(C^1\) value
\(\sum_a h_d(s_a)\) additive.

For an arbitrary shared-factor product lift, sequential Peirce compression
of genuine pure-row certificate fibers gives the same additive **existence**
lower bound: one can select supports and pure-row certificates so every
positive weighted sum of those selected rows has rank at least the right
side of (27). The
argument is as follows. After selecting rows \(e<a\), let \(c_i\) be the
join of their supports in factor \(i\), and put \(f_i=e_i-c_i\). Whole-
cylinder complementarity puts every primal lift with those earlier rows at
contact in the face \(V_i(f_i,1)\). Compress the entire genuine row-\(a\)
certificate fiber by \(P(f_i)\). Its image is a nonempty semialgebraic
family and preserves the exact pure-row identity against every primal
selection in the cylinder. The generic-stratum proof of (7), applied in
the remaining face cones, selects a support and an original certificate
whose compressed rank is at least \(q_{\rm sf}(s_a,d)\).

The support-join identity
\[
 \operatorname{rank}P(e-c)y
  =\operatorname{rank}(c\vee\operatorname{supp}y)
       -\operatorname{rank}c                                  \tag{28}
\]
makes these increments telescope. In a Lorentz cone, after a rank-one
support is used, its complementary face is a ray, so it has no further
mixed capacity. At the simultaneous contact, every primal lift is
complementary to every selected pure-row certificate. Consequently every
primal fiber there has total Jordan nullity at least the right side of
(27), and the support
of every positive weighted sum is the same final join, proving the claimed
aggregate rank.

This statement does not by itself say that every certificate of the final
aggregate objective has rank (27), nor that the minimum rank in that
aggregate certificate fiber is additive. A certificate of a sum need not
split into positive certificates of its summands. Without a separate
decomposition or global-fiber argument, the exact
\(\max_{\rm support}\min_{\rm aggregate\ cert}\) frontier for arbitrary
shared-factor product lifts remains open. Separate chains do attain (27)
for both minimum and maximum aggregate-certificate rank because their
pure-row factors are disjoint and every certificate is blockwise unique.
More explicitly, for positive row weights \(\lambda_a\), coefficient
matching in chain \(a\) forces its last temporal certificate coordinate to
be at least \(\lambda_a\); the global constant equation says that their sum
is exactly \(\sum_a\lambda_a\). Hence equality holds sourcewise and the
backward recursion makes the aggregate certificate unique.

## 6. Consequences and scope

1. The exact additive theorem \(\sum_a h_d(s_a)\) remains valid in its
   globally labelled bi-\(C^1\) primal/dual contact-sheet model. The norm
   chain lies outside that class precisely at its rank-birth seams.

2. A selection-free proof cannot use only the support span of the
   certificate fiber at the current objective. At a final-group pole, that
   span has total rank one, although arbitrarily nearby supports activate
   additional blocks with direction-dependent normalized ranges.

3. The norm chain alone does not refute selection-free primal-nullity
   theorems, but the companion rotated-Lorentz perspective does: every
   boundary fiber has a completion of nullity \(q_{\rm sf}\). What survives
   is the larger **global** restricted-barrier parameter
   \(2q_{\rm sf}-1\), witnessed by other points in the pole fiber.

4. In the standard-barrier distance theorem, a generic objective gives the
   coefficient \(\sqrt{q_{\rm sf}}\) from its unique exposed slack. The
   stronger \(\sqrt{h_d(s)}\) coefficient needs a smooth sheet or a
   different nullity/barrier argument.

## Independent audit record

Two independent hostile audits checked the exact projection, Slater point,
pairing normalization, complete coefficient-matching system, backward cone
inequalities, uniqueness of every certificate fiber, and all rank counts
for the binary chain. One audit independently established the
semialgebraic generic-stratum lower bound, including the
\(\max_v\min_{Z\in\mathcal D(v)}\) quantifiers. Both returned **PASS**.
A further hostile audit checked the arbitrary-\(d\) grouped chain.  Its
first block carries at most \(d-1\) original coordinates and every later
block carries the previous norm plus at most \(d-2\) new coordinates, so
exactly \(q_{\rm sf}\) blocks suffice, including a smaller final group.
The vector coefficient equations and backward Lorentz inequalities make
every certificate unique.  Finally, projecting the ambient Newton vector
away from the fixed final temporal coordinate gives the upper parameter
\(2q_{\rm sf}-1\), and the pole path has determinant order exactly
\(2q_{\rm sf}-1\).  The arbitrary-\(d\), product-scope, and standard-barrier
claims therefore also passed.

## Literature-positioning note

### Targeted primary-source screen (2026-09-04)

The construction and the language around it have substantial antecedents.
They should not be presented as new.

- Ben-Tal and Nemirovski,
  [*Lectures on Modern Convex Optimization*, Chapter 3](https://doi.org/10.1137/1.9780898718829.ch3),
  treat conic quadratic programs over products of Lorentz cones and collect
  the standard SOC modelling calculus.  Their 2001
  [polyhedral-approximation paper](https://doi.org/10.1287/moor.26.2.193.10561)
  introduced the tower-of-variables decomposition used to reduce a large
  Lorentz constraint to small three-dimensional norm constraints before
  polyhedral approximation.
- Vielma, Ahmed, and Nemhauser,
  [*A Lifted Linear Programming Branch-and-Bound Algorithm for
  Mixed-Integer Conic Quadratic Programs*](https://doi.org/10.1287/ijoc.1070.0256),
  Section 3, explicitly write a high-dimensional Lorentz cone using paired
  norm variables, three-dimensional Lorentz cones, and a recursively
  smaller Lorentz cone.  Repeating the recursion yields a formulation using
  only three-dimensional Lorentz factors.  This is direct prior art for a
  balanced norm tree.  The ordered chain (9) is a simple variant chosen to
  make every dual fiber and its seam behavior transparent.
- Gouveia, Parrilo, and Thomas,
  [*Lifts of Convex Sets and Cone Factorizations*](https://doi.org/10.1287/moor.1120.0575),
  Theorem 2.4, identify proper cone lifts with factorizations of the full
  slack operator.  Their proof obtains a convex feasible set of dual
  certificates for each support functional and permits an arbitrary
  pointwise choice.  Thus genuine support-certificate fibers and the slack
  identity (6) are classical consequences of lift duality.
- Fawzi,
  [*On Representing the Positive Semidefinite Cone Using the
  Second-Order Cone*](https://doi.org/10.1007/s10107-018-1233-0),
  Definition 2 and Remark 2, defines the SOC rank of a matrix as the
  smallest number of three-dimensional Lorentz factors in a factorization,
  equivalently the smallest number of SOC-rank-one summands.  The paper
  also notes explicitly that higher-dimensional Lorentz cones have finite
  lifts by products of the three-dimensional cone.  Proposition 1 records
  the collinearity of Lorentz elements complementary to the same nonzero
  element, a close antecedent of the rank-one support geometry used here.

These notions optimize different objects.  Standard SOC rank minimizes the
number of factors needed for **one global slack factorization**.  The
quantity (1) fixes an affine lift, takes the minimum Jordan rank over the
entire attained certificate fiber separately at each support, then takes
the worst support, and finally optimizes over lifts with a factor-dimension
cap.  A lift may have many factors while its certificate at a seam has only
one nonzero Jordan-rank unit, so factor count does not determine (1).
Likewise, semidefinite extension degree minimizes the maximum LMI order and
deliberately ignores both the number of blocks and ranks of optimal dual
certificates.

Targeted searches through 2026 for “SOC/second-order-cone rank” of the
Euclidean-ball slack operator, minimum-rank SOCP dual solutions, capped
Lorentz lifts, and tower/nested Lorentz formulations found no primary
source that states any of the following:

1. the exact all-support minimax identity (2);
2. the semialgebraic generic-contact lower bound of \(d-2\) tangent
   directions per nonzero Jordan-rank unit;
3. uniqueness of every support-certificate fiber for the nested chain; or
4. the strict one-unit separation from the globally bi-\(C^1\) frontier in
   exactly the strict-cap divisible cases.

The exact restricted-slice value \(2q_{\rm sf}-1\) also was not located.
The classical ingredients are only that the Lorentz log barrier has
parameter two, product parameters add, and affine restriction preserves
self-concordance; they do not compute the least gradient parameter after
the linked variables and final temporal coordinate are fixed.

The conservative label is therefore **candidate exact selection-free
support-certificate minimax theorem and smooth-versus-seam separation;
specific synthesis not located**.  This is a targeted negative screen, not
an exhaustive priority claim.  Novelty should be attached to the quantifier
order in (1), the sharp lower bound and fiber-uniqueness calculation, and
the comparison with the smooth frontier—not to norm trees, cone
factorizations, Lorentz complementarity, or standard barrier facts.
