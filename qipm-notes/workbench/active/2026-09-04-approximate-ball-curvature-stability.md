# Approximate balls: conditioned curvature stability and a metric obstruction

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the linear-algebra and counterexample; moderate on the best conditioning hypothesis

## Summary

The exact dimension-minus-two curvature theorem has a quantitative extension
for approximate ball lifts, provided the local cone factors remain
well-conditioned. The key observation is that geometric approximation does
not perturb the mixed derivative of the ball slack. It perturbs only
complementarity.

Let

\[
 B_2^N\subseteq C\subseteq(1+\varepsilon)B_2^N                       \tag{1}
\]

and suppose that \(C\) has a lift over definable proper cones
\(K_i\subset E_i\), of dimensions \(m_i\). After eliminating free variables
and reducing to the minimal face, let \(s_i\leq m_i\) be the dimensions of
the reduced factor faces in their spans. Local \(C^2\) primal and dual
factors on an orthonormal sphere chart satisfy

\[
 \sum_i\langle A_i(u),B_i(v)\rangle
 =h_C(\sigma(v))-\langle\sigma(u),\sigma(v)\rangle .                 \tag{2}
\]

Each summand is nonnegative. At the chart center, its diagonal value
\(\delta_i=\langle a_i,b_i\rangle\) satisfies

\[
 \delta_i\geq0,\qquad \sum_i\delta_i\leq\varepsilon.                 \tag{3}
\]

The support-function term in (2) depends only on \(v\). Mixed
differentiation therefore gives the exact identity

\[
 \sum_i-DA_i(0)^TDB_i(0)=I_{N-1}.                                  \tag{4}
\]

The lemma below shows that the \(i\)-th matrix in (4) is within an explicit
error \(e_i\) of a matrix of rank at most \(\max\{s_i-2,0\}\). Hence

\[
 \boxed{\sum_i e_i<1
 \quad\Longrightarrow\quad
 N-1\leq\sum_i\max\{s_i-2,0\}
 \leq\sum_i\max\{m_i-2,0\}.}                                      \tag{5}
\]

Under uniform lower bounds on active factor norms and upper bounds on their
first and second derivatives, \(\sum_i e_i=O(\sqrt\varepsilon)\) for a
bounded number of blocks. Thus sufficiently accurate, uniformly conditioned
approximate lifts obey the exact block-count lower bound.

Metric approximation alone cannot force the weighted curvature inequality at
*any* positive error if ray factors are allowed: arbitrarily accurate
circumscribed polytopes have lifts using only one-dimensional rays, so their
non-ray block count and weighted \((m_i-2)_+\) budget are both zero. This
does not evade a lower bound that counts every scalar inequality, because the
number of rays grows as accuracy improves.

There is also a fixed-error obstruction even when all blocks are counted.
For every \(d\geq3\),

\[
 C_d=B_2^{d-1}\times B_2^{d-1}\subset\mathbb R^{2(d-1)}             \tag{6}
\]

has a lift using two \(d\)-dimensional Lorentz blocks and satisfies

\[
 B_2^{2(d-1)}\subset C_d\subset\sqrt2 B_2^{2(d-1)},\qquad
 d_H(C_d,B_2^{2(d-1)})=\sqrt2-1.                                  \tag{7}
\]

The exact ball in this dimension needs at least

\[
 \left\lceil\frac{2(d-1)-1}{d-2}\right\rceil=3                     \tag{8}
\]

blocks of dimension at most \(d\). Thus even symmetric-cone lifts violate
the exact all-block count at multiplicative error \(\sqrt2\). A metric-only
all-block theorem must have a nontrivial small-error threshold.

## Quantitative near-complementarity lemma

Let \(A,B:U\to K\times K^*\) be \(C^2\), where \(K\subset E\) is an
\(m\)-dimensional proper cone, \(0\in U\subset\mathbb R^n\), and

\[
 g(u,v)=\langle A(u),B(v)\rangle\geq0.                              \tag{9}
\]

Assume the Euclidean ball of radius \(r\) is contained in \(U\). Put

\[
 a=A(0),\quad b=B(0),\quad X=DA(0),\quad Y=DB(0),\quad
 \delta=\langle a,b\rangle.                                       \tag{10}
\]

First suppose \(a,b\neq0\), and define

\[
 \begin{aligned}
 U_1&=\|X\|, &V_1&=\|Y\|,\\
 H_A&=\sup_{\|h\|=1,\ |t|\leq r}
 \left|\left\langle D^2A(th)[h,h],b\right\rangle\right|,\\
 H_B&=\sup_{\|h\|=1,\ |t|\leq r}
 \left|\left\langle a,D^2B(th)[h,h]\right\rangle\right|.
 \end{aligned}                                                     \tag{11}
\]

Write

\[
 \psi_r(\delta,H)=\inf_{0<s\leq r}
 \left(\frac{\delta}{s}+\frac{Hs}{2}\right),                       \tag{12}
\]

and set

\[
 \widehat\alpha=\frac{\psi_r(\delta,H_A)}{\|b\|},\qquad
 \widehat\beta=\frac{\psi_r(\delta,H_B)}{\|a\|},\qquad
 \gamma=\frac{\delta}{\|a\|\|b\|}.                                 \tag{13}
\]

If \(m\geq2\), there is a matrix \(R\) of rank at most \(m-2\) such that

\[
 \boxed{\|X^TY-R\|\leq
 U_1\widehat\beta+V_1\widehat\alpha
 +\widehat\alpha\widehat\beta\gamma+U_1V_1\gamma.}                 \tag{14}
\]

For a one-dimensional ray factor, take \(R=0\) and

\[
 \|X^TY\|\leq\widehat\alpha\widehat\beta.                           \tag{15}
\]

If \(a=0\), then \(X=0\), because every two-sided directional derivative
of a cone-valued map at the vertex belongs to
\(K\cap(-K)=\{0\}\). Similarly, \(b=0\) implies \(Y=0\).

### Proof

For a unit vector \(h\), \(f(t)=\langle A(th),b\rangle\) is nonnegative,
has \(f(0)=\delta\), and satisfies \(|f''(t)|\leq H_A\). Taylor's
theorem at the endpoint whose sign is opposite to \(f'(0)\) gives, for
every \(0<s\leq r\),

\[
 |f'(0)|\leq\frac{\delta}{s}+\frac{H_As}{2}.
\]

Taking the infimum and supremum over \(h\) shows

\[
 \|X^Tb\|\leq\psi_r(\delta,H_A).                                   \tag{16}
\]

The same argument bounds \(Y^Ta\).

Let \(\widehat a=a/\|a\|\), \(\widehat b=b/\|b\|\), and let
\(P_a,P_b\) project orthogonally onto their perpendicular hyperplanes.
Decompose

\[
 X=P_bX+\widehat b c^T,\qquad
 Y=P_aY+\widehat a d^T,                                            \tag{17}
\]

where \(\|c\|\leq\widehat\alpha\) and
\(\|d\|\leq\widehat\beta\). Expanding \(X^TY\) shows that its distance
from \(X^TP_bP_aY\) is at most

\[
 U_1\widehat\beta+V_1\widehat\alpha+
 \widehat\alpha\widehat\beta\gamma.                                \tag{18}
\]

The singular values of \(P_bP_a\) are \(1\), with multiplicity \(m-2\),
together with \(\gamma\) and \(0\). Thus \(P_bP_a\) is within operator
norm \(\gamma\) of rank at most \(m-2\). Multiplication by \(X^T,Y\)
adds \(U_1V_1\gamma\), proving (14). For \(m=1\), (15) follows directly
from (16), since both derivatives are normal components.

The estimate is invariant under reciprocal scalar gauge
\(A\mapsto sA,\ B\mapsto s^{-1}B\). No invariance under arbitrary
cone-coordinate isomorphisms is claimed.

## Conditioned approximate-lift theorem

In (1)--(4), apply (14)--(15) in the span of every reduced factor face and
call the right-hand side \(e_i\). Zero-dimensional factors, and factors
whose selected primal or dual value is zero, have \(e_i=0\). There are
matrices \(R_i\) satisfying

\[
 \operatorname{rank}R_i\leq\max\{s_i-2,0\},\qquad
 \|-DA_i(0)^TDB_i(0)-(-R_i)\|\leq e_i.                              \tag{19}
\]

By (4),

\[
 \left\|I_{N-1}-\sum_i(-R_i)\right\|\leq\sum_i e_i.                 \tag{20}
\]

If the right side is below one, then \(\sum_i(-R_i)\) is invertible.
Rank subadditivity proves (5).

Suppose along a family with \(\varepsilon\downarrow0\) that all active
factors satisfy

\[
 \|a_i\|,\|b_i\|\geq\mu>0,\quad U_{1,i},V_{1,i}\leq L,\quad
 H_{A,i},H_{B,i}\leq H,\quad r\geq r_0>0,                           \tag{21}
\]

and the number of blocks is bounded. Take \(H>0\) as a fixed upper bound
(also covering factors whose individual second-derivative bound is zero).
Once \(\sqrt{2\delta/H}\leq r\),

\[
 \psi_r(\delta,H)\leq\sqrt{2H\delta}.
\]

Equations (3), (14), and Cauchy--Schwarz give

\[
 \sum_i e_i=O(\sqrt\varepsilon).                                   \tag{22}
\]

There is also a useful explicit contrapositive. Suppose every active
reduced factor has dimension at least two and the uniform bounds in (21)
hold for \(k\) active factors. Since
\(\sum_i\sqrt{\delta_i}\leq\sqrt{k\varepsilon}\) and
\(\sum_i\delta_i^2\leq\varepsilon^2\), equations (13)--(14) give

\[
\sum_i e_i\leq
 \frac{2L\sqrt{2Hk\varepsilon}}{\mu}
 +\frac{L^2\varepsilon}{\mu^2}
 +\frac{2H\varepsilon^2}{\mu^4}.                                  \tag{23}
\]

Consequently, if the formulation is under capacity,

\[
 \sum_i\max\{s_i-2,0\}<N-1,
\]

then the right-hand side of (23) must be at least one. In a regime where
the sum of the last two terms is at most \(1/2\), this forces

\[
 L\sqrt H\geq
 \frac{\mu}{4\sqrt{2k\varepsilon}}.                                \tag{24}
\]

The constant in (24) is deliberately relaxed. One-dimensional ray factors
can be included by adding at most \(2H\varepsilon/\mu^2\) to (23), using
(15); then the same conclusion follows when the sum of all three remainder
terms is at most \(1/2\). Thus an under-capacity family cannot keep all of
\(\mu^{-1},L,H,k\) bounded as \(\varepsilon\downarrow0\).

The assumptions in (21) are substantive. Definability supplies local
\(C^2\) strata for each fixed lift, but not bounds uniform over a family.
Factors can approach the cone vertex, or their derivatives can diverge,
allowing combinatorial switching to replace smooth curvature.

If approximation is stated as
\[
 (1-\eta)B_2^N\subset C\subset(1+\eta)B_2^N,
\]
rescaling reduces it to (1) with outer excess \(2\eta/(1-\eta)\).

## Deriving (2) from a general lift

After the standard reduction, write

\[
 C=\{\pi z:z\in K,\ Mz=b\},\qquad K=\prod_iK_i,                    \tag{25}
\]

with a strictly feasible point. For \(x=\sigma(u)\), choose the
minimum-norm point \(A(u)\) in its primal fiber. For \(y=\sigma(v)\),
conic duality gives a nonempty closed set of optimal multipliers. Choose
its unique minimum-norm member \(\lambda(v)\), and set

\[
 B(v)=M^*\lambda(v)-\pi^*y\in K^*,\qquad
 \langle b,\lambda(v)\rangle=h_C(y).                               \tag{26}
\]

Therefore

\[
 \langle A(u),B(v)\rangle
 =h_C(\sigma(v))-\langle\sigma(u),\sigma(v)\rangle.                 \tag{27}
\]

Minimum-norm selection and definable \(C^2\) stratification give a common
full-dimensional \(C^2\) cell for \(A\circ\sigma\) and
\(\lambda\circ\sigma\), hence also for \(B\circ\sigma\). The theorem is
conditional on the numerical bounds there. For an orthonormal sphere chart,
\(D\sigma(0)^TD\sigma(0)=I_{N-1}\), so mixed differentiation gives (4).

## Arbitrarily accurate ray-only obstruction

Fix \(\varepsilon>0\), and choose a finite \(\delta\)-net
\(\mathcal U\subset S^{N-1}\) with

\[
 \frac{1}{1-\delta^2/2}\leq1+\varepsilon.
\]

The circumscribed polytope

\[
 P_{\mathcal U}=\{x:\langle u,x\rangle\leq1
                  \text{ for every }u\in\mathcal U\}               \tag{28}
\]

contains \(B_2^N\). If \(x\in P_{\mathcal U}\), choose
\(u\in\mathcal U\) within distance \(\delta\) of
\(x/\|x\|_2\). Since
\[
 \left\langle u,\frac{x}{\|x\|_2}\right\rangle
 =1-\frac12\left\|u-\frac{x}{\|x\|_2}\right\|_2^2
 \geq1-\frac{\delta^2}{2},
\]
we have \(\|x\|_2\leq(1-\delta^2/2)^{-1}\). Therefore

\[
 B_2^N\subseteq P_{\mathcal U}\subseteq(1+\varepsilon)B_2^N.       \tag{29}
\]

Introducing one nonnegative slack for every inequality in (28) is an exact
lift over a product of one-dimensional proper cones. Thus for every positive
accuracy there is an approximate ball lift with

\[
 \sum_i\max\{m_i-2,0\}=0
\]

and no non-ray blocks. This rigorously rules out any unconditional extension
of the exact weighted curvature-capacity inequality based on Hausdorff or
multiplicative approximation alone. It does not rule out lower bounds on the
*total* number of ray blocks; the net construction uses more inequalities as
\(\varepsilon\) decreases.

## Two-block metric counterexample

If \(\|(u,v)\|_2\leq1\), then \(\|u\|_2,\|v\|_2\leq1\), proving the
first inclusion in (7). If \((u,v)\in C_d\), then
\(\|(u,v)\|_2^2\leq2\), proving the second. Both bounds are attained, and
because the smaller ball lies in \(C_d\),

\[
 d_H(C_d,B_2^{2(d-1)})
 =\max_{z\in C_d}(\|z\|_2-1)=\sqrt2-1.
\]

Finally,
\[
 C_d=\{(u,v):(1,u)\in Q_d,\ (1,v)\in Q_d\},
\]
so two \(d\)-dimensional Lorentz blocks suffice, while (8) is the sharp
exact-ball lower bound.

## Literature boundary

Gouveia, Parrilo, and Thomas,
[*Approximate cone factorizations and lifts of
polytopes*](https://doi.org/10.1007/s10107-014-0848-z), convert
approximate slack-matrix factorizations into inner and outer approximations.
Their paper does not appear to contain the local near-complementarity
rank-\((m-2)\) estimate (14).

Ben-Tal and Nemirovski,
[*On Polyhedral Approximations of the Second-Order
Cone*](https://doi.org/10.1287/moor.26.2.193.10561), construct compact
lifted polyhedral approximations of Lorentz constraints.  In their notation,
an \(\epsilon\)-approximation of the \((k+1)\)-dimensional Lorentz cone is a
polyhedral extended formulation whose projection \(\widehat L_k\) satisfies

\[
 L_k\subseteq\widehat L_k
 \subseteq\{(y,t):\|y\|_2\leq(1+\epsilon)t\}.
\]

Their Theorem 1.1 constructs such a formulation with
\(p_k+q_k=O(k\log(2/\epsilon))\) auxiliary variables plus inequalities for
\(0<\epsilon\leq1\), while Proposition 3.1 proves
\(q_k=\Omega(k\log(1/\epsilon))\) inequalities for every such formulation
when \(0<\epsilon\leq1/2\).  Thus the ray-only obstruction above has a sharp
prior-art qualification: weighted non-ray curvature can be zero at arbitrary
accuracy, but a lifted polyhedral approximation pays
\(\Theta(N\log(1/\epsilon))\) scalar inequalities/ray factors in this
Lorentz-cone approximation model.  Their result reinforces the caveat:
increasingly accurate metric approximations can shift complexity from smooth
curvature capacity into a growing number of singular scalar factors.

There is a direct ambient-barrier corollary for that explicit LP
realization. Introducing one nonnegative slack per inequality makes its cone
\(\mathbb R_+^{q_k}\). Every possibly coupled LHSC barrier on this ambient
orthant has parameter at least \(q_k\), and the standard logarithmic barrier
attains \(q_k\). Hence the optimal ambient parameter within the
Ben-Tal--Nemirovski orthant formulation is

\[
                 \nu=\Theta(N\log(1/\epsilon)),
\]

versus \(\nu=2\) for the exact single Lorentz cone. This is a
formulation-dictionary tradeoff, not an intrinsic lower bound for treating
the projected polyhedral cone as one custom factor, and not by itself an IPM
iteration lower bound.

No source was found in the targeted search that states (4)--(5), the
projection estimate (14), or the example (6)--(8) as a boundary for
curvature-capacity arguments. This is a literature screen, not proof of
novelty.

## Interpretation for QIPM lower bounds

A QIPM formulation cannot evade the exact block budget through a
factorization satisfying these uniform, coordinate-dependent conditioning
bounds: sufficiently small error still forces the same number of cone blocks.
An evading family must violate at least one sufficient hypothesis, through
factor degeneration in the chosen coordinates, derivative blow-up, growth in
active pieces, or non-small approximation error. No intrinsic algorithmic
penalty for such a violation is proved here. Turning it into an iteration or
linear-system cost is a separate step; this is a geometric block lower bound,
not yet a complete QIPM runtime lower bound.
