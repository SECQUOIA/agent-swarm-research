# Rotated Lorentz perspectives refute the fiberwise nullity premium

Status: Proved; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High; priority not assessed

## Result

Fix a ball dimension \(s\geq2\) and a Lorentz-factor dimension cap
\(D\geq3\).  Partition \([s-1]\) into \(q\) nonempty groups
\(G\), each of size at most \(D-2\), where

\[
                         q=\left\lceil {s-1\over D-2}\right\rceil .
                                                               \tag{1}
\]

There is an exact affine lift of \(B_2^s\) through the product
\(\prod_G Q_{|G|+2}\), with full Slater, such that **every** boundary
fiber contains a primal tuple of total Jordan nullity exactly \(q\).
In fact, away from one pole the boundary fiber is unique and has nullity
\(q\).  Consequently, the proposed selection-free strengthening

\[
 \text{some }v\in S^{s-1}\text{ has every primal lift over }v
       \text{ of nullity at least }q+1                         \tag{2}
\]

is false.  For products of real \(2\times2\) PSD cones, take singleton
groups and \(D=3\).  Then \(q=s-1\), so there is no support direction at
which every primal lift has total nullity at least \(s\).

The same construction has a compact dual certificate fiber at every
support.  Every fiber contains a total-rank-\(q\) certificate, and no
certificate has larger total rank.  Thus neither aggregation of the
zero-order dual fiber nor a favorable choice of exposing certificate
recovers the missing unit.

The restricted standard product Lorentz barrier of the construction has
exact gradient parameter

\[
                              \boxed{\nu=2q-1}.             \tag{3}
\]

This separates three quantities that can otherwise be conflated:

* the minimum nullity in every boundary fiber is \(q\);
* the maximum exposed dual rank at every support is \(q\); but
* the standard restricted barrier parameter is \(2q-1\), witnessed by
  higher-nullity points in the non-singleton pole fiber.

The formulation is an elementary rotated-SOC perspective.  The useful
new conclusion here is the failure of the proposed **every-primal-fiber**
premium, not a claim that the underlying formulation is new.

## 1. Construction and exact projection

Write a projected point as \(x=(a,b)\), where
\(a\in\mathbb R^{s-1}\), and set

\[
                              \delta=1-b.
\]

For every group \(G\), introduce a scalar \(z_G\), impose

\[
 W_G=\left({\delta+z_G\over2},
           {\delta-z_G\over2},a_G\right)\in Q_{|G|+2},
 \qquad
                         \sum_Gz_G=1+b .                  \tag{4}
\]

The Lorentz condition in (4) is equivalent to the rotated inequality

\[
          \delta\geq0,\qquad z_G\geq0,qquad
                       \|a_G\|_2^2\leq\delta z_G.         \tag{5}
\]

Summing (5) and using the equality in (4) gives

\[
 \|a\|_2^2\leq(1-b)\sum_Gz_G=(1-b)(1+b)=1-b^2.           \tag{6}
\]

It also forces \(-1\leq b\leq1\), so the projection is contained in
\(B_2^s\).  Conversely, if \(\|a\|^2+b^2\leq1\) and \(b<1\), choose

\[
 z_G\geq{\|a_G\|^2\over1-b},\qquad
 \sum_Gz_G=1+b.                                          \tag{7}
\]

The required leftover in (7) is nonnegative by the ball inequality.  At
\(b=1\), necessarily \(a=0\), and any nonnegative \(z_G\) summing to two
is feasible.  This proves exactness.  At \(x=0\), the choice
\(z_G=1/q\) makes every inequality in (5) strict, so the lift has full
Slater and no initial facial reduction is hidden.

## 2. Every boundary fiber has minimum nullity \(q\)

Suppose \((a,b)\in S^{s-1}\) and \(-1<b<1\).  Equality holds in (6), so
equality must hold separately in every inequality (5):

\[
                         z_G={\|a_G\|^2\over1-b}.          \tag{8}
\]

Thus the fiber is unique.  Every \(W_G\) is a nonzero boundary point of
its Lorentz cone, including when \(a_G=0\), because then
\(W_G=((1-b)/2,(1-b)/2,0)\).  Hence every block has Jordan rank one and
nullity one.

At the south pole \((a,b)=(0,-1)\), equation (4) forces every \(z_G=0\),
and

\[
                              W_G=(1,1,0)                 \tag{9}
\]

is again a nonzero extreme-ray point.  The total nullity is \(q\).

At the north pole \((a,b)=(0,1)\), the fiber is the simplex

\[
                         z_G\geq0,\qquad\sum_Gz_G=2.      \tag{10}
\]

Choosing every \(z_G>0\) makes

\[
                         W_G=(z_G/2,-z_G/2,0)             \tag{11}
\]

a nonzero extreme-ray point.  This tuple also has total nullity \(q\).
If some \(z_G=0\), that block is the cone vertex and contributes nullity
two instead, so the north-pole fiber contains higher-nullity tuples as
well.  We have therefore proved the sharper fiberwise identity

\[
 \boxed{
  \min_{W\text{ lifting }v}\sum_G\operatorname{nullity}_J W_G=q
  \quad\text{for every }v\in S^{s-1}.}                  \tag{12}
\]

This proves the counterexample to (2).

### Real \(2\times2\) PSD specialization

For singleton groups, (5) is the matrix constraint

\[
                 X_i=\begin{pmatrix}1-b&a_i\\a_i&z_i\end{pmatrix}
                         \succeq0,qquad
                         \sum_{i=1}^{s-1}z_i=1+b.        \tag{13}
\]

Thus (13) is an exact lift through \((\mathbb S_+^2)^{s-1}\).  At every
boundary point there is a lift in which all \(s-1\) matrices are nonzero
rank one.  For \(s=3\), two \(2\times2\) blocks already refute the claim
that some boundary support must force nullity three in every primal
completion.

## 3. The complete support-certificate fibers

Let the support direction be \(v=(c,\eta)\in S^{s-1}\), with the same
coordinate grouping.  Write a candidate dual Lorentz block as

\[
                         V_G=(A_G+\Gamma,A_G-\Gamma,-c_G). \tag{14}
\]

It belongs to \(Q_{|G|+2}\) exactly when

\[
                 A_G\geq0,\qquad\Gamma\geq0,qquad
                              4A_G\Gamma\geq\|c_G\|^2.   \tag{15}
\]

The Lorentz pairing with (4) is

\[
                         \langle W_G,V_G\rangle
                           =\delta A_G+z_G\Gamma-a_G^Tc_G. \tag{16}
\]

Coefficient matching on the affine equality \(\sum_Gz_G=1+b\) shows
that the full normalized certificate fiber is obtained by taking

\[
             \Gamma={1-\eta\over2},qquad
             \sum_GA_G={1+\eta\over2},                  \tag{17}
\]

together with (15).  Indeed, summing (16) then gives

\[
 \sum_G\langle W_G,V_G\rangle
   =(1-b){1+\eta\over2}+(1+b){1-\eta\over2}-a^Tc
   =1-a^Tc-b\eta.                                       \tag{18}
\]

If \(\eta<1\), positivity in (15) implies

\[
 A_G\geq {\|c_G\|^2\over2(1-\eta)}.                    \tag{19}
\]

Because \(\sum_G\|c_G\|^2=1-\eta^2\), the lower bounds in (19) sum to
\((1+\eta)/2\), exactly the required sum in (17).  Therefore every
inequality is an equality and the certificate is unique:

\[
                   A_G={\|c_G\|^2\over2(1-\eta)}.       \tag{20}
\]

Every block in (20) is a nonzero Lorentz rank-one element, even if
\(c_G=0\).  At \(\eta=-1\), this statement gives
\(A_G=0,\Gamma=1\), again one nonzero extreme ray per group.

At the north support \(\eta=1\), one has \(c=0,\Gamma=0\), and the full
dual fiber is the simplex

\[
                            A_G\geq0,qquad\sum_GA_G=1.   \tag{21}
\]

Choosing every \(A_G>0\) gives \(q\) nonzero rank-one blocks.  No member
of (21) has a block of rank two.  Consequently

\[
 \boxed{
   \max_{V\in\mathcal D(v)}\sum_G\operatorname{rank}_J V_G=q
   \quad\text{for every }v\in S^{s-1}.}                 \tag{22}
\]

The fibers are compact, convex, and semialgebraic.  For real PSD2, (14)
is equivalently

\[
 Y_i=\begin{pmatrix}\alpha_i&-c_i/2\\-c_i/2&\gamma\end{pmatrix},
 \quad
 \gamma={1-\eta\over2},
 \quad
 \sum_i\alpha_i={1+\eta\over2},                        \tag{23}
\]

with \(\alpha_i=c_i^2/[2(1-\eta)]\) off the north pole and the simplex
\(\alpha_i\geq0,\sum_i\alpha_i=1\) at the north pole.

## 4. Exact restricted standard-barrier parameter

The standard product Lorentz barrier on the displayed affine slice is,
up to an additive constant,

\[
 F(a,b,z)=-\sum_G\log\bigl((1-b)z_G-\|a_G\|^2\bigr).    \tag{24}
\]

To obtain the sharp upper parameter, homogenize with a scalar \(\tau\):

\[
 \delta=\tau-b,qquad \sum_Gz_G=\tau+b.                 \tag{25}
\]

The resulting cone is pointed and has compact base \(\tau=1\).  The
restriction of the product barrier to this homogeneous linear slice is a
\(2q\)-logarithmically homogeneous self-concordant barrier.  Let \(g,H\)
be its gradient and Hessian on the linear span, and let \(\ell\) denote
the functional \(\tau\).  Logarithmic homogeneity gives

\[
                         Hx=-g,qquad x^THx=2q.           \tag{26}
\]

On the base tangent space \(\ker\ell\), the squared dual norm of the
restricted gradient is

\[
 \min_{\alpha}(g-\alpha\ell)^TH^{-1}(g-\alpha\ell)
             =2q-{1\over\ell^TH^{-1}\ell}.              \tag{27}
\]

The Dikin ellipsoid is contained in the cone.  Since \(\ell\) is
nonnegative on the cone and \(\ell(x)=1\), this containment implies

\[
                          \|\ell\|_{x,*}\leq1,\qquad
                          \ell^TH^{-1}\ell\leq1.         \tag{28}
\]

Equations (27)--(28) prove that (24) has gradient parameter at most
\(2q-1\).  Restriction preserves the third-derivative
self-concordance inequality.

For the matching lower bound, use the north-pole tuple in which exactly
one \(z_G\) equals two and all others vanish.  One block then has Jordan
nullity one and the other \(q-1\) blocks are vertices of Jordan nullity
two.  Along a segment from a Slater point, the determinant product
therefore vanishes to exact order

\[
                              1+2(q-1)=2q-1.              \tag{29}
\]

The one-dimensional barrier-gradient inequality forces
\(\nu\geq2q-1\).  Together with (27)--(28), this proves (3).

## 5. Consequences and scope

The north-pole simplex is the mechanism missed by a single-valued
topological argument.  Choosing all simplex coordinates positive keeps
all primal blocks on nonzero extreme rays and realizes the generic
nullity \(q\).  Moving to a simplex vertex instead creates \(q-1\) zero
blocks and exposes the larger barrier parameter \(2q-1\).  Convex
fiber-valued switching therefore fills the projective seam without
forcing an extra nullity unit in **every** completion.

This counterexample does not refute lower bounds based on the existence of
one high-nullity boundary tuple, nor does it lower the exact standard
barrier parameter below \(2q-1\).  It specifically rules out upgrading
the selection-free exposed-rank/nullity value \(q\) to \(q+1\) with the
quantifier “every primal lift over one support.”

There is also an objective-specific metric distinction.  For the north
support objective, symmetry and strict convexity put the standard-barrier
minimizer on

\[
                 a=0,qquad z_G={1+b\over q}.
\]

Along this axis the barrier reduces to

\[
                 F(b)=-q\log(1-b^2)+q\log q.             \tag{30}
\]

Hence its Dikin length as \(b\uparrow1\) has leading term
\(\sqrt q\log(1/(1-b))\), not
\(\sqrt{2q-1}\log(1/(1-b))\).  The larger global parameter is witnessed
by auxiliary-fiber vertices that the north-objective central trajectory
does not approach.  This gives a concrete warning against substituting a
restricted barrier parameter for the exposed rank of the chosen linear
objective.

## 6. Exact heterogeneous-product extension

The construction tensorizes without loss.  For source balls
\(\prod_{a=1}^hB_2^{s_a}\), use an independent copy of (4) for each
source and put
\[
                 q_a=\left\lceil {s_a-1\over D-2}\right\rceil .
                                                                  \tag{31}
\]
At every simultaneous extreme contact
\((v_1,\ldots,v_h)\in\prod_aS^{s_a-1}\), the fiber is the Cartesian
product of the one-source fibers.  Hence
\[
 \min_{\text{primal fiber}}\sum\operatorname{nullity}_J
                    =\sum_aq_a.                                  \tag{32}
\]
For every aggregate support with strictly positive weights
\(\lambda_a\), coefficient matching is sourcewise and positive rescaling
does not change Jordan rank.  The full aggregate certificate fiber
therefore satisfies
\[
 \max_{\text{certificate fiber}}\sum\operatorname{rank}_J
                    =\sum_aq_a.                                  \tag{33}
\]
The positivity qualification matters: a zero source weight deletes that
source's certificate blocks.

Here is the no-transfer detail behind (33).  An aggregate certificate
decomposes over the disjoint source factors as affine nonnegative
functions
\[
                     \mu_a-\lambda_av_a^Tx_a .
\]
Validity on \(B_2^{s_a}\) forces \(\mu_a\geq\lambda_a\).  Matching the
global constant gives \(\sum_a\mu_a=\sum_a\lambda_a\), hence equality
holds sourcewise.  The aggregate fiber is therefore exactly the Cartesian
product of the positively rescaled one-source certificate fibers; no
constant mass can be shifted between sources to change the rank.

The restricted standard product barrier is the Cartesian sum of the
one-source barriers.  Its squared gradient norm is the sum of the
sourcewise squared norms, and the north-simplex vertex witnesses can be
approached independently.  Thus its exact parameter is
\[
                         \nu=\sum_a(2q_a-1).                       \tag{34}
\]
For a positive weighted sum of the north-pole objectives, the central
trajectory has \(1-b_a=\Theta_{\lambda_a}(1/\eta)\).  Equation (30)
then shows that its leading metric distance and arclength are
\[
              \left(\sqrt{\sum_aq_a}+o(1)\right)\log\eta.         \tag{35}
\]
For completeness, the lower distance statement does not assume that the
central axis is minimizing.  In one rotated block
\[
 f(\delta,z,a)=-\log(\delta z-\|a\|^2)
\]
satisfies
\(\|d\delta\|_{(\nabla^2f)^{-1}}=\delta\).  Metric
Cauchy--Schwarz therefore gives
\[
 ds^2\geq\sum_aq_a\,(d\log\delta_a)^2 .
\]
Since \(\delta_a=1-b_a=\Theta_{\lambda_a}(1/\eta)\), integration gives
the lower coefficient in (35), while the central axis supplies the
matching upper coefficient.

Thus the heterogeneous product preserves the exact separation between
minimum fiber nullity, maximum exposed rank, global barrier parameter, and
objective-specific movement.  Equations (32)--(35) concern this explicit
separate-factor construction; they do not assert an optimum over lifts
that share factors across sources.

## Independent audit record

An independent audit checked the grouped rotated-Lorentz isomorphism,
projection in both directions, every boundary fiber including both poles,
the complete dual coefficient system and cone inequalities, and all
rank/nullity counts. It also checked the homogenized base: the cone is
pointed, its \(\tau=1\) base is compact, and orthogonal projection of the
ambient Newton vector gives (27). Dikin containment proves (28), while a
north-simplex vertex has exact determinant order \(2q-1\). The parameter
and north-axis movement calculations therefore pass. Three malformed
LaTeX commands in the initial draft were repaired; no mathematical change
was needed.

A separate hostile audit checked the heterogeneous extension.  It verified
Cartesian additivity of minimum nullity and exact gradient parameters, and
identified the sourcewise constant-accounting and perspective-coordinate
metric arguments now written explicitly above.  With those details, the
full aggregate-certificate quantifier and the distance as well as
arclength coefficient in (35) pass.
