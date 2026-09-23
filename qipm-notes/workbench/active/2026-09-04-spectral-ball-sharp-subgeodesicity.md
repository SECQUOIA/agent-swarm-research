# Sharp subgeodesicity and optimal Dikin movement on spectral-norm balls

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the stated standard-barrier family; novelty priority still needs specialist review

## Headline

Let \(\mathbb F=\mathbb R\) or \(\mathbb C\), \(p\le q\), and
\[
 {\mathbb B}_{p,q}=\{X\in\mathbb F^{p\times q}:\|X\|_{\rm op}<1\},
 \qquad
 \phi(X)=-\log\det(I_p-XX^*).
                                                                    \tag{1}
\]
For the support problem
\[
 \min_{X\in{\mathbb B}_{p,q}}-\operatorname{Re}\operatorname{tr}(C^*X),
                                                                    \tag{2}
\]
write the positive singular values of \(C\) as
\(w_1\ge\cdots\ge w_r>0\).  This note records four exact or sharp facts.

1. The standard-barrier distance from the analytic center depends only on
   transformed singular values and has a closed variational reduction.
2. The shortest distance to the \(\epsilon\)-objective sublevel is a
   strictly convex one-multiplier water-filling problem.
3. This distance characterizes the minimum number of arbitrary feasible
   forward Dikin moves up to radius-dependent constants.
4. The exact central path has worst-case arclength overhead
   \(\Theta(\sqrt{\log r})\), both to its own endpoint and to the closest
   \(\epsilon\)-accurate endpoint.  A matching discrete separation holds
   for fixed-radius central-neighborhood sequences with arbitrary reference
   labels, including a
   conventional fixed Newton-decrement neighborhood.

These are barrier-geometric movement results for an explicit unconstrained
family.  They do not by themselves give a quantum runtime or oracle-query
advantage.

## 1. Exact distance and water filling

Define
\[
 \rho(x)=\int_0^x{\sqrt{2(1+t^2)}\over1-t^2}\,dt,\qquad0\le x<1.
                                                                    \tag{3}
\]
If \(\sigma_i(X)\) are the singular values of \(X\), then
\[
 \boxed{
 d_\phi(0,X)=
 \left[\sum_{i=1}^p\rho(\sigma_i(X))^2\right]^{1/2}.}              \tag{4}
\]
More generally,
\[
 d_\phi(X,Y)\ge
 \|\rho(\sigma(X))-\rho(\sigma(Y))\|_2,                            \tag{5}
\]
with equality when \(X,Y\) share an ordered singular frame.  Thus every
fixed-singular-frame slice is a Euclidean orthant in \(\rho\)-coordinates.

The proof uses the Hermitian dilation
\[
 {\cal S}(X)=\begin{pmatrix}0&X\\X^*&0\end{pmatrix},\qquad
 g(\lambda)=-\tfrac12\log(1-\lambda^2).
 \]
The spectral-trace Hessian formula and convexity of \(g\) show along every
absolutely continuous path that
\[
 \|\dot X\|_X^2\ge
 \sum_i {2(1+\sigma_i^2)\over(1-\sigma_i^2)^2}\dot\sigma_i^2
 =\left\|{d\over dt}\rho(\sigma(X))\right\|_2^2.                  \tag{6}
\]
Integrating gives the lower bound; moving linearly in \(\rho\) in a fixed
singular frame attains equality.  The argument includes repeated and zero
singular values and uses the real Hessian in the complex case.

For \(0<\epsilon<\|C\|_*\), let
\[
 L_{\rm opt}(\epsilon)
 =\inf\{d_\phi(0,X):\|C\|_*-\langle C,X\rangle\le\epsilon\}.
 \]
Von Neumann's inequality and (4) give the exact reduction
\[
 \boxed{
 L_{\rm opt}(\epsilon)=
 \min_{\substack{0\le x_i<1\\
                  \sum_iw_i(1-x_i)\le\epsilon}}
 \left[\sum_{i=1}^r\rho(x_i)^2\right]^{1/2}.}                     \tag{7}
\]
The squared problem is strictly convex.  Its unique solution has an active
constraint and a unique \(\lambda>0\) satisfying
\[
 2\rho(x_i)\rho'(x_i)=\lambda w_i,\qquad
 \sum_iw_i(1-x_i)=\epsilon.                                      \tag{8}
\]

A convenient surrogate is
\[
 D_{\log}(\epsilon)=
 \min_{\substack{s_i\ge0\\\sum_iw_ie^{-s_i}\le\epsilon}}\|s\|_2.
                                                                    \tag{9}
\]
The scalar bounds
\[
 \log{1\over1-x}\le\rho(x)\le
 \sqrt2\log{1\over1-x}
 \]
give
\[
 D_{\log}(\epsilon)\le L_{\rm opt}(\epsilon)
 \le\sqrt2D_{\log}(\epsilon).                                    \tag{10}
\]
The logarithmic optimizer is explicit up to one scalar:
\[
 s_i=W(\gamma w_i),\qquad
 \sum_iW(\gamma w_i)=\gamma\epsilon.                              \tag{11}
\]

Full proofs are in Sections 5.1--5.2 of the
[objective-rank-adaptive spectral path note](2026-09-04-spectral-ball-low-rank-objective-path.md).

## 2. Optimal arbitrary bounded-Dikin movement

Let \(T_R^\star(\epsilon)\) be the minimum number of feasible chords from
zero to any \(\epsilon\)-accurate endpoint, allowing arbitrary noncentral
intermediate points, with
\(\|X^{j+1}-X^j\|_{X^j}\le R<1\).  Then
\[
 \boxed{
 {L_{\rm opt}(\epsilon)\over-\log(1-R)}
 \le T_R^\star(\epsilon)
 \le\left\lceil{L_{\rm opt}(\epsilon)\over\log(1+R)}\right\rceil.} \tag{12}
\]
The lower bound concatenates the straight segments, each of length at most
\(-\log(1-R)\).  For the upper bound, follow the globally shortest
\(\rho\)-linear path to the water-filled endpoint and partition it into
arcs of length \(\log(1+R)\).  The self-concordant chord inequality makes
every forward chord valid.

For a product of spectral balls, pool all nonzero objective singular
values.  Product distances add in squares, so (7)--(12) remain exact.

## 3. Sharp central-path distortion

The exact central path is
\[
 X(\eta)=\eta(I+\sqrt{I+\eta^2CC^*})^{-1}C.
                                                                    \tag{13}
\]
Its transformed singular-coordinate velocities, with \(s=\log\eta\) and
\(a_i=-\log w_i\), are
\[
 v_i(s)=
 \left(1-{1\over\sqrt{1+e^{2(s-a_i)}}}\right)^{1/2},
 \qquad v_1\ge\cdots\ge v_r\ge0.                                 \tag{14}
\]
Put
\[
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
             =1+\tfrac14\log r+O(1).
 \]
The prefix decomposition of every decreasing nonnegative vector gives
\[
 d_\phi(0,X(\eta_f))
 \le L_{\rm CP}(0,\eta_f)
 \le\Gamma_r\,d_\phi(0,X(\eta_f)).                               \tag{15}
\]
This \(\Theta(\sqrt{\log r})\) same-endpoint factor is sharp.

The same order remains exact when the endpoint may vary.  If
\(\eta_\epsilon\) is the first central parameter with objective error at
most \(\epsilon\), define
\[
 c_\star=\max_{y>0}{p^{-1}(yp'(y))\over y},\qquad
 p(y)=b'(\rho^{-1}(y)),\quad b(x)=-\log(1-x^2).
\]
The independently audited
[`exact scalar-dilation note`](2026-09-04-exact-scalar-centrality-dilation.md)
proves \(1<c_\star<69/50\).  Then
\[
 \boxed{
 L_{\rm CP}(\epsilon)
 \le c_\star\Gamma_rL_{\rm opt}(\epsilon)
 <{69\over50}\Gamma_rL_{\rm opt}(\epsilon),\qquad
 \sup_{w,\epsilon}{L_{\rm CP}(\epsilon)\over L_{\rm opt}(\epsilon)}
 =\Theta(\sqrt{\log r}).}                                       \tag{16}
\]
For the upper bound, use the exact optimizer \(x_i^\star\) in (7), put
\(y_i^\star=\rho(x_i^\star)\), and let \(\lambda\) be its KKT multiplier.
If \(b(x)=-\log(1-x^2)\) and
\(p(y)=b'(\rho^{-1}(y))\), an exact scalar calculation gives
\[
                         p(c_\star y)\ge yp'(y).                \tag{16a}
\]
This is the definition of \(c_\star\); the companion note proves that the
maximum is attained and supplies the analytic \(69/50\) certificate.  At central parameter
\(\eta=\lambda/2\), its transformed coordinates satisfy
\(p(y_i^{\rm c})=y_i^\star p'(y_i^\star)\).  Monotonicity of \(p'\) shows
\(y_i^{\rm c}\ge y_i^\star\), so this point is accurate, while (16a) gives
\(y_i^{\rm c}\le c_\star y_i^\star\).  Thus the first accurate central
endpoint has distance at most \(c_\star L_{\rm opt}\), and (15) proves the
upper bound.  The number \(\kappa_0\) is a certified uniform constant from
the earlier one-regime scalar argument, where
\(\kappa_0=1.391010896\ldots\) solves
\(\log[\kappa_0(\kappa_0-1)]+2-\kappa_0=0\); it is superseded here by the
exact variational constant \(c_\star\).

For sharpness, take \(m=r\), \(T=m\),
\(\epsilon=me^{-T}\), and
\[
 S_m=\sum_{j=1}^{m-1}j^{-3/2},\qquad
 a_i={T\over S_m}\sum_{j<i}j^{-3/2},\qquad w_i=e^{-a_i}.          \tag{17}
\]
The first accurate central parameter lies in \((T-1,T]\).  Its arc has
length \(\Omega(m\log m)\), while (7) has value
\(\Theta(m\sqrt{\log m})\).

## 4. A discrete central-neighborhood separation

For the family (17), consider feasible iterates \(Z_k\), arbitrary real
central labels \(s_k\), fixed \(\delta<\infty\), and \(R<1\), satisfying
\[
 Z_0=0,
 \qquad
 d_\phi(Z_k,X(e^{s_k}))\le\delta,\qquad
\|Z_{k+1}-Z_k\|_{Z_k}\le R.
                                                                    \tag{18}
\]
If its final iterate is actually \(\epsilon\)-accurate, then the sequence
needs
\[
                         N=\Omega_{R,\delta}(m\log m)              \tag{19}
\]
rounds.  In contrast, the optimal arbitrary noncentral sequence has
\[
                         T_R^\star(\epsilon)
                           =\Theta_R(m\sqrt{\log m}).              \tag{20}
\]

There is no hidden stopping-label assumption in (19).  Accuracy and the
Fan--von Neumann inequality give
\(\sum_iw_i[1-\sigma_i(Z_N)]\le\epsilon\), hence
\(\sigma_1(Z_N)\ge1-\epsilon\) because \(w_1=1\).  The singular-value
contraction (5) and (18) imply
\[
 \rho(r(e^{s_N}))\ge\rho(1-\epsilon)-\delta
                    \ge m-\log m-\delta.
\]
On the other hand, the first transformed central coordinate is at most
\(1/\sqrt2+\max\{s_N,0\}\).  Hence
\(s_N\ge m-\log m-\delta-1/\sqrt2>a_J\) for large \(m\), because
\(m-a_J=\Theta(m^{2/3})\).
Conversely, the tube condition at \(Z_0=0\) gives
\(d_\phi(0,X(e^{s_0}))\le\delta\).  Hence either \(s_0\le0\), or
\(s_0\le\delta/v_0\), so the initial clipped progress is only
\(O_\delta(1)\).  No start-label assumption is hidden either.

The proof uses (5): one round moves consecutive exact centers by at most
\(2\delta-\log(1-R)\).  In the first \(j\) resolved directions, each
\(\rho\)-velocity is bounded below by a constant, so every positive
log-parameter advance is \(O_{R,\delta}(1/\sqrt j)\).  The first
\(J=\lfloor m^{2/3}\rfloor\) threshold gaps in (17) are bounded below by a
constant.  Hence each round advances only \(O_{R,\delta}(1)\) in the
potential
\[
 {\cal P}(s)=\int_0^{\min\{\max\{s,0\},a_J\}}
                  \sqrt{|\{i:a_i\le u\}|}\,du,
 \]
whereas \({\cal P}(a_J)=\Omega(m\log m)\).  Negative label moves have
nonpositive potential increment, so summing only positive increments proves
the same lower bound without a label-monotonicity assumption.  Equivalently,
clipping both labels to \([0,a_J]\), ordering the clipped pair, and applying
(5) shows directly that the absolute potential change in every round is
\(O_{R,\delta}(1)\); this also covers jumps across either clipping point.

The contract in (18) is explicit and important: this is not a lower bound
for every possible IPM neighborhood definition or quantum oracle model.
The sharp family has sparse data in its singular frame:
\(C=\operatorname{Diag}(w)\) has only \(m\) nonzeros, and the conic form
adds only \(t=1\).  No claim is made that access to the spectral cone is a
free sparse oracle.
The proof remains quantitative for a growing tube radius
\(\delta_m=o(m^{2/3})\).  With
\(C_m=2\delta_m-\log(1-R)\), it gives
\[
 N=\Omega_R\!\left(
 {m\log m\over C_m\sqrt{1+C_m}}
 \right).                                                       \tag{20a}
\]
Thus the overhead over optimal noncentral movement still diverges for
\(\delta_m=o((\log m)^{1/3})\).

It does, however, include the conventional Newton-decrement neighborhood.
For
\[
 f_\eta(Z)=\phi(Z)-\eta\mathop{\rm Re}\operatorname{tr}(C^*Z),
 \qquad
 \lambda_\eta(Z)=\|\nabla f_\eta(Z)\|_{Z,*},                   \tag{21}
\]
standard self-concordance and the existence of the minimizer \(X(\eta)\)
give
\[
 \|Z-X(\eta)\|_Z\le{\lambda_\eta(Z)\over1-\lambda_\eta(Z)}.  \tag{22}
\]
Consequently, for any fixed \(\beta<1/2\),
\[
 \lambda_\eta(Z)\le\beta
 \quad\Longrightarrow\quad
 d_\phi(Z,X(\eta))
 \le\log{1-\beta\over1-2\beta}=:\delta_\beta.                \tag{23}
\]
The proof of (22) compares the Hessian along the segment from \(Z\) to
the minimizer and uses local Cauchy--Schwarz; (23) then follows from the
straight-segment metric bound.  Taking \(\delta=\delta_\beta\) in
(18)--(20) shows that every forward-
\(R\) sequence satisfying the fixed neighborhood
\(\lambda_{e^{s_k}}(Z_k)\le\beta<1/2\) needs
\(\Omega_{R,\beta}(m\log m)\) rounds before returning an actually
\(\epsilon\)-accurate iterate, even if its reference labels move backward.
Thus the sharp
\(\Omega(\sqrt{\log m})\) overhead is a separation for a standard
short-step IPM neighborhood, subject to the same explicit-family and
fixed-radius qualifications.
More generally, the growing-tube result allows
\(\beta_m\uparrow1/2\) whenever
\(\log[(1-\beta_m)/(1-2\beta_m)]=o((\log m)^{1/3})\), and the overhead
still diverges.

The conclusion transfers to feasible primal--dual path following on the
conic homogenization with the affine slice \(t=1\).  A bounded full
product-Dikin chord bounds its matrix-ball primal component, and a final
feasible duality gap at most \(\epsilon\) implies primal
\(\epsilon\)-accuracy.  Thus the same \(\Omega_{R,\beta}(m\log m)\) count
holds for full primal--dual chords under the stated primal decrement
neighborhood.  This does not cover infeasible-start or unbounded-update
QIPMs.

Equivalently, the decrement hypothesis may be stated as a standard conic
primal--dual residual.  With cost \(c=(0,-C)\), equality \(t=1\), slack
\(q=c-A^*y\), and \(z=(1,X)\),
\[
 \|q+\mu\nabla F(z)\|_{z,*}\le\beta\mu
 \quad\Longrightarrow\quad
 \lambda_{1/\mu}(X)\le\beta.                                   \tag{23a}
\]
Indeed, restrict the residual covector to \(\Delta t=0\); dual norm cannot
increase under this restriction, and its matrix component divided by
\(\mu\) is \(\nabla\phi(X)-C/\mu\).  Hence the full-chord lower bound
holds under this conventional feasible primal--dual short-step
neighborhood as well.

## 5. Literature and novelty boundary

The matrix-ball barrier and its parameter are classical.  The spectral
Hessian ingredient in (6) is a specialization of Lewis and Sendov,
[“Twice Differentiable Spectral Functions”](https://doi.org/10.1137/S089547980036838X)
(2001); an
[author-hosted copy](https://people.orie.cornell.edu/aslewis/publications/01-twice.pdf)
is open.

Nesterov and Nemirovski,
[“Primal Central Paths and Riemannian Distances for Convex Sets”](https://doi.org/10.1007/s10208-007-9019-4),
prove a general \(O(\nu^{1/4})\) comparison for bounded convex sets.
Nesterov and Todd,
[“On the Riemannian Geometry Defined by Self-Concordant Barriers”](https://doi.org/10.1007/s102080010032),
develop the general self-concordant Riemannian framework.  Those results do
not state (4), the support-objective water filling (7)--(11), the matched
bounded-move law (12), or the sharp rank-sensitive factors (16), (19)--(20).
There is no conflict with the \(O(\nu^{1/4})\) theorem: the present result
is a sharper specialization to one standard barrier and uses objective rank
\(r\), while the general theorem covers arbitrary bounded domains and
barriers.

Hirai, Nieuwboer, and Walter,
[“Interior-Point Methods on Manifolds: Theory and Applications”](https://doi.org/10.1007/s10208-026-09756-8)
(2026), give Newton and path-following theory for optimization on a
Riemannian base manifold.  That is adjacent but does not compute the
barrier-Hessian matrix-ball distance or the central-versus-noncentral
separation here.

Broader LP path-complexity and iteration lower bounds are known:
Allamigeon--Benchimol--Gaubert--Joswig
([arXiv:1708.01544](https://arxiv.org/abs/1708.01544)),
Allamigeon--Gaubert--Vandame
([arXiv:2201.02186](https://arxiv.org/abs/2201.02186)), and the
straight-line-complexity framework of
Allamigeon--Dadush--Loho--Natura--Végh
([arXiv:2206.08810](https://arxiv.org/abs/2206.08810)).  They concern
different LP, neighborhood, or segment models and do not give the exact
spectral-ball distance-to-accuracy law or the matched
\(\Theta(\sqrt{\log r})\) forward-Dikin separation here.

A targeted local and open-web search did not locate this exact synthesis.
The safe candidate contribution is the standard matrix-ball distance,
objective water filling, optimal bounded-Dikin movement, and sharp
centrality-distortion package.  It is not a new barrier, spectral Hessian
formula, Bergman-distance identity, or generic QIPM runtime theorem.
Priority remains subject to specialist review.

## Audit record

Independent hostile audits checked:

- the Hermitian-dilation factors, nonnegative divided differences,
  repeated/zero singular values, and complex real-Hessian convention;
- the von Neumann reduction, strict convexity, KKT conditions, and
  Lambert-\(W\) equations;
- both Dikin denominators and the product-metric extension;
- the decreasing-velocity prefix inequality and
  \(\Gamma_r^2=1+\frac14\log r+O(1)\);
- the exact-coordinate elasticity argument and its original certified
  \(\kappa_0\Gamma_r\) same-accuracy constant; a later independent audit of
  the exact scalar-dilation note verifies the sharper
  \(c_\star\Gamma_r<(69/50)\Gamma_r\) constant;
- the exact \(\epsilon=me^{-T}\) convention, location of the first accurate
  center, and both sides of the \(\Theta(\sqrt{\log r})\) theorem;
- the threshold-crossing and progress-potential proof of the discrete
  central-neighborhood separation, including arbitrary backward and clipped
  reference-label jumps; and
- the conversion of actual endpoint accuracy into terminal clipped progress
  and of the analytic-center start into \(O_\delta(1)\) initial progress,
  eliminating assumed start and end labels; and
- the Newton-decrement-to-geodesic-tube conversion, including its
  iterate-based norm and the constant
  \(\log((1-\beta)/(1-2\beta))\); and
- the growing-tube round tradeoff and its
  \(o((\log m)^{1/3})\) diverging-overhead regime; and
- the feasible primal--dual conic transfer through the \(t=1\) Hessian
  restriction and weak duality, including the standard scaled centrality
  residual and its pullback dual-norm contraction.

The audits found no substantive defect.  A text-escaping defect in an
intermediate draft of the multiscale construction was repaired by replacing
the entire affected block; control-character, duplicate-tag, and diff
checks passed afterward.
