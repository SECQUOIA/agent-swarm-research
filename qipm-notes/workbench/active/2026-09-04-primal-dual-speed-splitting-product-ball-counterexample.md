# Exact primal--dual speed splitting and a product-ball primal-projection counterexample

Status: Exact identities, counterexample, and objective-sensitive path bounds
independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the calculations; novelty of the product-ball specialization has only received a targeted, not exhaustive, literature screen

## Main conclusion

The barrier-independent primal--dual distance theorem cannot be projected to
a primal distance lower bound whose coefficient depends only on the ambient
barrier parameter.  This failure already occurs for the explicit optimal
barrier on the one-cone homogenization of a product of Euclidean balls.

There are two exact facts.

1. Along every feasible primal--dual central path for a
   \(\nu\)-logarithmically homogeneous barrier, the squared primal and dual
   speeds satisfy a Pythagorean identity
   \[
       \|\dot x\|_x^2+\|\dot s\|_{s,*}^2=\nu,
   \]
   where the dot denotes differentiation with respect to \(\log\eta\).
   Thus the constant product speed \(\sqrt\nu\) need not appear in either
   projection separately.
2. For the product-ball cone \(\mathcal H_{k,s}\), a weighted support
   objective gives the exact primal speed
   \[
      \|\dot x(\eta)\|_{x(\eta)}^2
      =q_{\rm eff}(\eta)
      :=\sum_{a=1}^k
        \left(1-{1\over\sqrt{1+(\eta w_a)^2}}\right).                 \tag{1}
   \]
   The complementary dual speed is exactly \(k+1-q_{\rm eff}(\eta)\).
   Hence a precision-dependent **effective exposed-factor count**, not the
   ambient parameter \(k+1\), controls primal central-path movement.

With one weight equal to one and the other weights zero, the primal length is
at most \(\log(\eta_1/\eta_0)\), while the dual length is at least
\(\sqrt{k}\log(\eta_1/\eta_0)\).  The endpoint product distance is at least
\(\sqrt{(k+1)/2}\log(\eta_1/\eta_0)\), but the primal endpoint distance is at
most the dimension-free primal path length.  A variant with all weights
strictly positive has a unique product-ball optimizer and the same separation
up to a factor \(1+o(1)\) at any prescribed accuracy.

This is a counterexample to a **parameter-only** primal projection.  It does
not refute objective-aware primal lower bounds that include an exposed rank
and a scale term such as the geometric-mean \(\Delta\) in the symmetric-cone
support-minor theorem.  It also does not settle the harder uniformly weighted
product-vertex question for an arbitrary barrier.

## 1. A general central-velocity identity

Let \(K\) be a regular cone and let
\(F:\operatorname{int}K\to\mathbb R\) be a
\(\nu\)-logarithmically homogeneous self-concordant barrier.  Consider
\[
 \begin{array}{ll}
 \text{minimize}&\langle c,x\rangle\\
 \text{subject to}&Ax=b,\quad x\in K,
 \end{array}                                                        \tag{2}
\]
and its dual \(A^Ty+s=c\), \(s\in K^*\).  Assume strict primal and dual
feasibility.  Write \((x(\eta),s(\eta))\) for the exact central path, so
\[
              s(\eta)=-{1\over\eta}F'(x(\eta)).                     \tag{3}
\]
Let \(F_*\) be the conjugate barrier, let \(H=F''(x(\eta))\), and put
\(\lambda=\log\eta\).  Dots below mean \(d/d\lambda\).

Logarithmic homogeneity gives
\[
 Hx=-F'(x),\qquad
 F'(x)^TH^{-1}F'(x)=\nu.                                            \tag{4}
\]
Conjugacy and (3) give
\[
                  F_*''(s)=\eta^2 H^{-1}.                           \tag{5}
\]
Differentiating (3) gives
\[
                  \eta\dot s=F'(x)-H\dot x.                         \tag{6}
\]
In whitened coordinates define
\[
 g=H^{-1/2}F'(x),\quad
 v=H^{1/2}\dot x,
 \quad d=H^{-1/2}\eta\dot s=g-v.                                   \tag{7}
\]
Primal and dual feasibility imply
\(A\dot x=0\) and \(\dot s\in\operatorname{range}A^T\).  Therefore
\[
                    \langle v,d\rangle
       =\eta\langle\dot x,\dot s\rangle=0.                          \tag{8}
\]
Equations (4)--(8) prove the exact identity
\[
 \boxed{
   \|\dot x\|_{F''(x)}^2
   +\|\dot s\|_{F_*''(s)}^2=\nu.}                                  \tag{9}
\]

In fact, (8) identifies both terms individually.  If
\[
       \mathcal U_x=H^{1/2}\ker A,
       \qquad
       \Pi_x=\text{Euclidean orthogonal projection onto }\mathcal U_x,
\]
then \(v\in\mathcal U_x\), \(d\in\mathcal U_x^\perp\), and \(g=v+d\).
Consequently
\[
 \boxed{
 \begin{aligned}
  \nu_{\rm P}(\eta)
    &:=\|\Pi_x H^{-1/2}F'(x)\|_2^2
      =\|\dot x\|_x^2,\\
  \nu_{\rm D}(\eta)
    &:=\|(I-\Pi_x)H^{-1/2}F'(x)\|_2^2
      =\|\dot s\|_{s,*}^2,\\
  \nu_{\rm P}(\eta)+\nu_{\rm D}(\eta)&=\nu.
 \end{aligned}}                                                    \tag{9a}
\]
Thus the exact primal central-path length over an interval is
\[
            L_{\rm P}=\int\sqrt{\nu_{\rm P}(\eta)}\,d\log\eta.      \tag{9b}
\]
When \(A\) has full row rank, this activity parameter also has the explicit
Schur-complement form
\[
 \nu_{\rm P}(\eta)=\eta^2 c^T
 \left[H^{-1}-H^{-1}A^T(AH^{-1}A^T)^{-1}AH^{-1}\right]c.            \tag{9c}
\]
Indeed, central stationarity writes
\(F'(x)+\eta c+A^T\ell=0\), and the projection in (9a) kills the
multiplier term.  Formula (9c) is the squared local dual norm of the
objective after quotienting out the equality multipliers.  It gives the
exact quantity that a primal-only movement argument would have to lower
bound along the path.

There is also an exact progress interpretation.  Let
\[
       p(\eta)=\langle c,x(\eta)\rangle,
       \qquad d(\eta)=\langle b,y(\eta)\rangle.
\]
Differentiating the primal central KKT system gives
\(\dot x=-\eta Mc\), where \(M\) is the bracketed matrix in (9c).  Since
\(p(\eta)-d(\eta)=\nu/\eta\), one obtains
\[
 \boxed{
   \nu_{\rm P}(\eta)=-\eta^2p'(\eta),
   \qquad
   \nu_{\rm D}(\eta)=\eta^2d'(\eta).}                               \tag{9d}
\]
If the optimal value \(p^*\) is finite and the central objectives converge
to it, then
\[
 \begin{aligned}
   p(\eta)-p^*&=\int_\eta^\infty{\nu_{\rm P}(u)\over u^2}\,du,\\
   p^*-d(\eta)&=\int_\eta^\infty{\nu_{\rm D}(u)\over u^2}\,du.
 \end{aligned}                                                      \tag{9e}
\]
Thus (9) is simultaneously a metric Pythagorean identity and a pointwise
allocation of the \(\nu/\eta\) central gap between primal and dual
objective progress.

No positive lower bound on \(\nu_{\rm P}\) follows from \(\nu\) alone:
if the affine equations fix \(x\), then \(\ker A=\{0\}\) and
\(\nu_{\rm P}=0\), while the dual projection carries all of \(\nu\).

This is the infinitesimal content behind Nesterov--Todd's constant-speed
primal--dual curve.  It also exposes the obstruction to projection: the
barrier axioms fix the norm of \(g\), while the affine constraints determine
how \(g\) splits between two orthogonal subspaces.  Either projection may
have arbitrarily small speed.

## 2. The one-cone product-ball model

Fix \(k\ge1\), \(s\ge1\), and define
\[
 \mathcal H_{k,s}
   =\{(t,y_1,\ldots,y_k):\|y_a\|_2\le t\text{ for every }a\}.
                                                                    \tag{10}
\]
The workbench note
[Bounded-face sharing sharp models](2026-09-04-bounded-face-sharing-sharp-models.md)
proves that
\[
 F(t,y)=-\sum_{a=1}^k\log(t^2-\|y_a\|_2^2)+(k-1)\log t              \tag{11}
\]
is a \((k+1)\)-LHSCB and that \(k+1\) is the optimal LHSCB parameter of
this cone.

Choose unit vectors \(u_a\in\mathbb R^s\) and weights \(w_a\ge0\).  Consider
the conic problem
\[
 \begin{array}{ll}
 \text{minimize}&-\sum_{a=1}^k w_a\langle u_a,y_a\rangle\\
 \text{subject to}&t=1,\quad (t,y)\in\mathcal H_{k,s}.
 \end{array}                                                        \tag{12}
\]
Its feasible set is exactly \((B_2^s)^k\).  If every \(w_a>0\), its unique
optimizer is \(y_a=u_a\) for all \(a\).

On the slice \(t=1\), (11) restricts to
\[
                         f(y)=-\sum_a\log(1-\|y_a\|_2^2).            \tag{13}
\]
The exact primal center at parameter \(\eta>0\) is
\[
 y_a(\eta)=r(\eta w_a)u_a,
 \qquad
 r(z)={\sqrt{1+z^2}-1\over z}
     ={z\over\sqrt{1+z^2}+1},                                      \tag{14}
\]
with \(r(0)=0\).  Indeed, each nonzero radial coordinate solves
\[
                         \eta w_a={2r\over1-r^2}.                    \tag{15}
\]

For \(z=\eta w_a\), differentiation of (15) with respect to
\(\lambda=\log\eta\) gives
\[
             {dr\over d\lambda}={r(1-r^2)\over1+r^2}.               \tag{16}
\]
The radial Hessian of the corresponding summand in (13) is
\[
                {d^2\over dr^2}[-\log(1-r^2)]
                  ={2(1+r^2)\over(1-r^2)^2}.                        \tag{17}
\]
Since \(dt=0\) and the \(y_a\)-blocks do not couple in (11), (16)--(17)
give
\[
 \begin{aligned}
 \|\dot x(\eta)\|_{x(\eta)}^2
   &=\sum_a {2r(\eta w_a)^2\over1+r(\eta w_a)^2}\\
   &=\sum_a\left(1-{1\over\sqrt{1+(\eta w_a)^2}}\right)
     =q_{\rm eff}(\eta).                                           \tag{18}
 \end{aligned}
\]
The second equality uses
\(\sqrt{1+z^2}=(1+r^2)/(1-r^2)\).  Combining (9) and (18) yields
\[
 \boxed{
 \|\dot s(\eta)\|_{s(\eta),*}^2=k+1-q_{\rm eff}(\eta).}           \tag{19}
\]

The function in each summand of (18) rises continuously from zero to one.
Thus \(q_{\rm eff}(\eta)\) is a soft count of the factors whose objective
weight is visible at scale \(1/\eta\).

## 3. An unbounded projection gap

First take
\[
                         w_1=1,\qquad w_2=\cdots=w_k=0.              \tag{20}
\]
For any \(0<\eta_0<\eta_1\), (18)--(19) imply
\[
 \begin{aligned}
 L_{\rm P}
   &=\int_{\log\eta_0}^{\log\eta_1}
       \sqrt{q_{\rm eff}(e^\lambda)}\,d\lambda
     \le \log{\eta_1\over\eta_0},\\
 L_{\rm D}
   &=\int_{\log\eta_0}^{\log\eta_1}
       \sqrt{k+1-q_{\rm eff}(e^\lambda)}\,d\lambda
     \ge \sqrt{k}\log{\eta_1\over\eta_0},\\
 L_{\rm PD}&=\sqrt{k+1}\log{\eta_1\over\eta_0}.                  \tag{21}
 \end{aligned}
\]
The primal Riemannian endpoint distance is no larger than \(L_{\rm P}\).
By Nesterov--Todd's \(\sqrt2\)-geodesic theorem, the product endpoint
distance satisfies
\[
 d_{F+F_*}\bigl(z(\eta_0),z(\eta_1)\bigr)
 \ge \sqrt{(k+1)/2}\log{\eta_1\over\eta_0}.                       \tag{22}
\]
Consequently
\[
 {d_{F+F_*}(z(\eta_0),z(\eta_1))
  \over d_F(x(\eta_0),x(\eta_1))}
 \ge \sqrt{(k+1)/2},                                                \tag{23}
\]
whenever the denominator is nonzero.  The ratio is unbounded with \(k\).

The central duality gap is \((k+1)/\eta\).  Taking
\(\eta_1=(k+1)/\epsilon\) therefore makes \(z(\eta_1)\) a strictly
feasible primal--dual point of gap exactly \(\epsilon\), while the primal
endpoint is in the primal \(\epsilon\)-objective-accuracy set.  Thus the
distance to that entire primal target set is at most
\(O(\log((k+1)/\epsilon))\), not
\(\Omega(\sqrt{k}\log((k+1)/\epsilon))\).

The same conclusion holds when the primal start is the analytic center
\(x(0)=(1,0,\ldots,0)\).  Since the single active summand satisfies
\(q_{\rm eff}(\eta)\le\eta^2/2\) for \(0<\eta\le1\), its path length from
\(\eta=0\) to \(\eta_1\ge1\) is at most
\[
                  {1\over\sqrt2}+\log\eta_1.                         \tag{23a}
\]
Thus the counterexample also directly refutes an analytic-center-to-primal-
accuracy lower bound with a parameter-only \(\sqrt{k}\) coefficient.

This example has a high-dimensional optimal face because the objective
ignores \(k-1\) balls.  The next variant removes that possible objection.

## 4. A unique-optimizer version at prescribed accuracy

Fix \(0<\epsilon\le1\), put \(\nu=k+1\), and choose
\[
        w_1=1,qquad
        w_a={\epsilon^2\over\nu^2}\quad(2\le a\le k),
        \qquad \eta_1={\nu\over\epsilon}.                            \tag{24}
\]
All weights are positive, so (12) has the unique optimizer
\((u_1,\ldots,u_k)\).  For \(1\le\eta\le\eta_1\), use
\[
              1-{1\over\sqrt{1+z^2}}\le {z^2\over2}                 \tag{25}
\]
to obtain
\[
 \begin{aligned}
 q_{\rm eff}(\eta)
 &\le1+{k-1\over2}
        \left({\eta\epsilon^2\over\nu^2}\right)^2\\
 &\le1+{(k-1)\epsilon^2\over2\nu^2}
  \le1+{\epsilon^2\over2\nu}.                                     \tag{26}
 \end{aligned}
\]
Therefore, between the central points at \(\eta_0=1\) and \(\eta_1\),
\[
 \begin{aligned}
 L_{\rm P}
  &\le \sqrt{1+{\epsilon^2\over2\nu}}
       \log{\nu\over\epsilon},\\
 L_{\rm D}
  &\ge \sqrt{k-{\epsilon^2\over2\nu}}
       \log{\nu\over\epsilon},\\
 d_{F+F_*}(z(1),z(\eta_1))
  &\ge\sqrt{\nu/2}\log{\nu\over\epsilon}.                       \tag{27}
 \end{aligned}
\]
Again, the endpoint gap is exactly \(\epsilon\), and the primal endpoint
distance is at most the first line of (27).  Hence even unique exposure of
the product vertex does not support a uniform parameter-only primal lower
bound at a prescribed accuracy: the small objective weights are invisible
at that accuracy.

The dependence of (24) on \(\epsilon\) is material.  For a single fixed
instance with all weights positive, every \(\eta w_a\) eventually becomes
large as \(\eta\to\infty\), and then \(q_{\rm eff}(\eta)\to k\).  Thus
this construction does not refute an asymptotic theorem whose constants are
allowed to depend on the smallest nonzero objective weight.  It does refute
a worst-case statement uniform over objectives and depending only on
\(k,\nu,\epsilon\).

## 5. Bounded primal Dikin moves

The separation is not merely between two path-length calculations.  A
primal-only trajectory can follow the curve (14).  In the one-active-factor
example, its local speed is at most one per unit change in \(\log\eta\).
Partitioning this curve into pieces of Riemannian length at most a fixed
\(R<1\) gives \(O(R^{-1}\log(\eta_1/\eta_0))\) feasible primal moves.  The
radial Hessian (17) increases with \(r\), so the starting-point Dikin norm of
each chord is at most the Riemannian length of its curve segment.  Thus every
chord has starting norm at most \(R\).

For the unique-optimizer version, the same conclusion follows either by
subdividing more finely and using self-concordant metric comparison, or
directly from (27).  The standard self-concordant comparison
\[
       d_F(x,y)\ge \log(1+\|y-x\|_x)
\]
shows that a curve segment of length at most \(\log(1+R)\) has endpoint
chord norm at most \(R\) at its starting point.  A curve of length \(L\)
can therefore be sampled into at most
\(\lceil L/\log(1+R)\rceil\) bounded-Dikin chords.  Hence a
\(\sqrt{k}\)-scaled lower bound on the number of **primal** bounded-Dikin
moves is false for this family, although the product-metric lower bound
remains valid.

## 6. What remains possible

The counterexample identifies the hypotheses a positive primal theorem must
add.

- The ambient LHSCB parameter alone is insufficient.  It counts dual radial
  motion caused by constraints that may be irrelevant at the requested
  primal accuracy.
- Merely requiring a unique optimizer is insufficient uniformly over the
  objective: arbitrarily small positive weights postpone movement in most
  factors beyond the requested precision.
- A viable theorem may use a precision-dependent exposed-factor count, or a
  scale such as the weighted geometric mean in the standard symmetric-cone
  support-minor bound.  Formula (18) gives an exact model for what such a
  quantity should measure.
- The uniformly weighted objective that exposes every product-ball factor
  has \(q_{\rm eff}(\eta)\to k\) and primal speed \(\sqrt{k}\) for this
  explicit barrier.  Whether every LHSCB on the product-ball cone forces a
  comparable primal distance under a quantitative nondegeneracy condition
  remains open here.

## 7. Literature boundary

The generic geometry is classical.  Nesterov and Todd,
[On the Riemannian Geometry Defined by Self-Concordant Barriers and
Interior-Point Methods](https://optimization-online.org/2001/08/363/),
prove that a primal--dual curve satisfying the conjugacy relation and
primal--dual tangent orthogonality has constant speed and is
\(\sqrt2\)-geodesic (Theorem 4.1), apply it to the feasible primal--dual
central path (Theorems 5.1--5.2), and explicitly state that they do not know
how to prove the analogous primal result.  Their Section 6.1 also gives a
noncentral curve whose primal projection has arbitrarily poor geodesic
efficiency.  Therefore (9) should be viewed as a transparent Pythagorean
rewriting of their established calculation, not a novelty claim.

Nesterov and Nemirovski,
[Primal Central Paths and Riemannian Distances for Convex
Sets](https://doi.org/10.1007/s10208-007-9019-4), give general comparisons
between primal central-path length and primal Riemannian distance.  Their
orthant example already shows that a primal central path can be much longer
than a shortcut to the same terminal hyperplane.  It does not contain the
product-ball speed law (18) or the primal-versus-dual allocation (19).

A targeted search of the local corpus and open primary literature did not
locate formulas (18)--(19), the weighted effective-factor interpretation, or
the unique-product-vertex counterexample (24)--(27).  These should be
described only as apparently unlocated specializations until a specialist
literature review and independent proof audit are complete.

## 8. Positive result: an objective-sensitive primal path bound

The exact activity formula also yields a positive primal-only theorem for
the **explicit barrier and support-objective family** in Sections 2--4.  It
does not apply to arbitrary barriers or arbitrary product-ball programs.

Define
\[
 h(z)=1-{1\over\sqrt{1+z^2}},
 \qquad
 Q_2(\eta)=\sum_{a=1}^k\min\{(\eta w_a)^2,1\}.                      \tag{28}
\]
The sharp global constant comparison
\[
 \left(1-{1\over\sqrt2}\right)\min\{z^2,1\}
 \le h(z)\le \min\{z^2/2,1\}                                     \tag{29}
\]
follows from
\[
 {h(z)\over z^2}
 ={1\over\sqrt{1+z^2}(1+\sqrt{1+z^2})}
\]
on \(0<z\le1\), and monotonicity of \(h\) on \([1,\infty)\).
Consequently, for every \(0\le\eta_0<\eta_1\), the primal central-path
length obeys
\[
 \boxed{
  \sqrt{1-1/\sqrt2}\;\mathcal J(\eta_0,\eta_1)
  \le L_{\rm P}(\eta_0,\eta_1)
  \le \mathcal J(\eta_0,\eta_1),}                                  \tag{30}
\]
where
\[
       \mathcal J(\eta_0,\eta_1)
       =\int_{\eta_0}^{\eta_1}\sqrt{Q_2(\eta)}\,{d\eta\over\eta}.
                                                                    \tag{31}
\]
Thus (31) is a sharp, universal-constant characterization of the primal
length in terms of the distribution of objective-weight scales.

For an explicit evaluation, sort
\(w_1\ge\cdots\ge w_k>0\) and put
\(B_j^2=\sum_{a>j}w_a^2\).  Between two consecutive breakpoints
\(1/w_j\) and \(1/w_{j+1}\),
\[
                         Q_2(\eta)=j+\eta^2B_j^2.                   \tag{32}
\]
For \(j>0\), an antiderivative of the integrand in (31) is
\[
 \Phi_j(\eta)=
 \sqrt{j+\eta^2B_j^2}
 +\sqrt j\log\!\left(
 {\eta B_j\over \sqrt j+\sqrt{j+\eta^2B_j^2}}
 \right),                                                          \tag{33}
\]
with the continuous limiting interpretations
\(\Phi_0(\eta)=\eta B_0\) and
\(\Phi_k(\eta)=\sqrt k\log\eta\).  Splitting at the breakpoints and
using (33) computes \(\mathcal J\) exactly.

### 8.1 Accuracy is controlled by a smoothed \(\ell_1\) count

Let
\[
 E(\eta)=\sum_{a=1}^k w_a[1-r(\eta w_a)]                            \tag{34}
\]
be the primal objective error of the central point (14), and define
\[
                       Q_1(\eta)=\sum_a\min\{\eta w_a,1\}.          \tag{35}
\]
Since
\[
 2-\sqrt2\le
 {1-r(z)\over\min\{1,1/z\}}
 \le1,                                                             \tag{36}
\]
where the ratio is interpreted separately on \(z\le1\) and \(z\ge1\),
one has the sharp constant comparison
\[
 \boxed{
   (2-\sqrt2){Q_1(\eta)\over\eta}
    \le E(\eta)\le {Q_1(\eta)\over\eta}.}                         \tag{37}
\]
Indeed, for \(z\le1\), \(1-r(z)\) decreases from one to
\(2-\sqrt2\).  For \(z\ge1\),
\(z[1-r(z)]=z+1-\sqrt{1+z^2}\) increases from \(2-\sqrt2\) to one.

Equations (30) and (37) give a complete constant-factor ledger: \(Q_1\)
determines when the central point is accurate, while the integral of
\(\sqrt{Q_2}\) determines the primal movement needed to reach it.

### 8.2 An effective-support theorem

Normalize the objective so that \(w_1\le1\), and sort the weights.  Suppose
for some \(m\ge1\),
\[
                       \sum_{a>m}w_a\le{\epsilon\over2},
 \qquad 0<\epsilon\le1.                                            \tag{38}
\]
Set
\[
                            \eta_f={2m\over\epsilon}.               \tag{39}
\]
Then the central point at \(\eta_f\) is primal \(\epsilon\)-accurate,
because
\[
 E(\eta_f)\leq\sum_{a\le m}{1\over\eta_f}+\sum_{a>m}w_a
                  \le\epsilon.                                    \tag{40}
\]

Moreover \(h(z)\le\min\{z,1\}\), and hence, for
\(1\le\eta\le\eta_f\),
\[
 q_{\rm eff}(\eta)
 \le Q_1(\eta)
 \le m+\eta\sum_{a>m}w_a
 \le2m.                                                            \tag{41}
\]
For \(0<\eta\le1\), (29) gives
\[
 q_{\rm eff}(\eta)\le{\eta^2\over2}\sum_a w_a^2,
 \qquad
 \sum_a w_a^2\le m+{\epsilon^2\over4}.                            \tag{42}
\]
Integrating (41)--(42) from the analytic-center limit \(\eta=0\) proves
\[
 \boxed{
 L_{\rm P}(0,\eta_f)
 \le \sqrt{m+\epsilon^2/4\over2}
      +\sqrt{2m}\log{2m\over\epsilon}.}                           \tag{43}
\]
In particular,
\[
                  L_{\rm P}=O\!\left(
                    \sqrt m\,[1+\log(m/\epsilon)]\right),          \tag{44}
\]
independently of the ambient factor count \(k\).

This scaling is sharp for this family up to constants.  If at least \(m\)
weights satisfy \(\eta w_a\ge1\) throughout an interval
\([\eta_-,\eta_+]\), then (29) gives
\[
 L_{\rm P}(\eta_-,\eta_+)
 \ge\sqrt{(1-1/\sqrt2)m}\log{\eta_+\over\eta_-}.                   \tag{45}
\]
Equal order-one weights attain the familiar
\(\Theta(\sqrt m\log(m/\epsilon))\) scale.  The improvement in (43) is
therefore an effective-support replacement \(k\mapsto m\), not an artifact
of a loose path estimate.

There is a useful full-certificate endpoint variant.  Put \(\nu=k+1\),
retain \(w_1\le1\), and suppose
\[
              \left(\sum_{a>m}w_a^2\right)^{1/2}
                    \le {\epsilon\sqrt m\over\nu}.                  \tag{45a}
\]
Follow the path to \(\eta_g=\nu/\epsilon\), whose ambient primal--dual gap
is exactly \(\epsilon\).  For every \(0<\eta\le\eta_g\),
\[
 q_{\rm eff}(\eta)
 \le m+{\eta^2\over2}\sum_{a>m}w_a^2
 \le {3m\over2}.                                                    \tag{45b}
\]
The same integration as above gives
\[
 L_{\rm P}(0,\eta_g)
 \le \sqrt{m+m\epsilon^2/\nu^2\over2}
       +\sqrt{3m/2}\log{\nu\over\epsilon}.                         \tag{45c}
\]
All tail weights may be strictly positive, so the true product-ball
optimizer may be unique.  This does not weaken the product-metric lower
bound: (19) shows that the dual projection carries the complementary
energy, at least \(\nu-3m/2\) along this path.

### 8.3 Explicit bounded-Dikin schedule

Let
\[
       \mathcal L(\eta)=
       \int_0^\eta\sqrt{q_{\rm eff}(u)}\,{du\over u}.               \tag{46}
\]
Fix a desired starting-point Dikin radius \(0<R<1\) and put
\(\ell_R=\log(1+R)\).  Starting with \(\eta_0=0\), choose
\(\eta_j\) successively so that
\[
        \mathcal L(\eta_j)=
        \min\{j\ell_R,\mathcal L(\eta_f)\},                        \tag{47}
\]
and output the exact central points from (14).  The scalar function in
(46) is continuous and strictly increasing whenever the objective is
nonzero, so each parameter can be found by one-dimensional bisection.

Each curve segment has Riemannian length at most \(\ell_R\).  The standard
self-concordant comparison
\[
             \log(1+\|x'-x\|_x)\le d_F(x,x')
\]
then implies \(\|x(\eta_{j+1})-x(\eta_j)\|_{x(\eta_j)}\le R\).
The number of feasible primal Dikin chords is exactly bounded by
\[
 N_R\le
 \left\lceil{L_{\rm P}(0,\eta_f)\over\log(1+R)}\right\rceil.        \tag{48}
\]
Combining (43) and (48) gives
\[
 N_R=O_R\!\left(\sqrt m\,[1+\log(m/\epsilon)]\right).              \tag{49}
\]

This is an explicit movement schedule, not an end-to-end runtime theorem.
The centers (14) are available in closed form for this support-objective
family.  In a generic program, evaluating \(q_{\rm eff}\), finding the
central points, reading the weights, or materializing a classical output
can cost \(\Omega(k)\).  Equation (49) neither hides those costs nor claims
that an arbitrary QIPM can realize the same schedule.  It certifies primal
objective error only.  At \(\eta_f=2m/\epsilon\), the ambient conic
primal--dual gap is \((k+1)\epsilon/(2m)\), which can be much larger than
\(\epsilon\).  Therefore the schedule does not contradict the
barrier-independent product-metric theorem for an \(\epsilon\)-gap output.

### 8.4 Geometrically decaying weights

Take
\[
                       w_a=2^{-(a-1)},\qquad 1\le a\le k.           \tag{50}
\]
For
\[
                m=\left\lceil\log_2{4\over\epsilon}\right\rceil
                \le k,                                             \tag{51}
\]
the tail after \(m\) has total weight at most \(\epsilon/2\).  Equations
(43) and (48) give
\[
             L_{\rm P},N_R
              =O_R\!\left(\log^{3/2}{1\over\epsilon}\right),        \tag{52}
\]
with no dependence on \(k\) beyond the requirement \(k\ge m\).

This order is also the actual central-path length.  On the dyadic interval
\(2^{j-1}\le\eta\le2^j\), the first \(j\) terms of \(Q_2\) are saturated,
while
\[
        \eta^2\sum_{a>j}w_a^2\le {4\over3}.                         \tag{53}
\]
Thus (29)--(31) make the contribution of that interval
\(\Theta(\sqrt j)\).  Summing for \(j\le m\) gives
\[
                 L_{\rm P}(0,2^m)=\Theta(m^{3/2}).                  \tag{54}
\]
For \(\epsilon\le1/2\), the remaining interval from \(2^m\) to
\(\eta_f=2m/\epsilon=\Theta(m2^m)\) contributes only
\(O(\sqrt m\log m)\); the omitted range \(1/2<\epsilon\le1\) changes only
absolute constants.  Hence (52) is tight for the displayed central path.
When \(k\gg\log(1/\epsilon)\), this can be arbitrarily smaller than the
generic ambient-parameter ledger
\(O(\sqrt k\log(k/\epsilon))\).  The gain comes entirely
from objective-scale nonuniformity and disappears once the requested
accuracy resolves all \(k\) weights.

### Independent audit of Section 8

An independent hostile audit verified the constants in (29) and (36), the
antiderivative (33), the head--tail estimates (38)--(43), and the dyadic
summation (50)--(54).  A follow-up audit verified the full-gap
\(\ell_2\)-tail variant (45a)--(45c), including its exact primal--dual gap
endpoint and complementary dual energy.  The analytic-center integral in (46) is finite
because \(q_{\rm eff}(\eta)=O(\eta^2)\) as \(\eta\downarrow0\).  For the
schedule (47), the global comparison
\(\log(1+\|x'-x\|_x)\leq d_F(x,x')\) and the fact that geodesic distance is
at most the intervening central-arc length give the starting-metric chord
bound in the claimed direction.  The only defect found was the corrected
missing relation symbol in (40).
