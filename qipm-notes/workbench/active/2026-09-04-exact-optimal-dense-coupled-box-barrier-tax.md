# An exact-optimal dense-coupled box barrier retains the sharp centrality tax

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the algebra and asymptotic proof; targeted literature screen complete, priority not claimed

## Result

Let \(r\geq2\), \(K=(-1,1)^r\), and put
\[
 U(x)=-\sum_{i=1}^r\log(1-x_i^2),\qquad
 \beta={1\over4r},\qquad
 F(x)=U(x)+{\beta\over2}({\bf1}^Tx)^2.                         \tag{1}
\]
Then \(F\) is a genuinely dense-coupled self-concordant barrier on the
cube with the **exact optimal parameter**
\[
                              \boxed{\nu(F)=r}.                \tag{2}
\]
It is invariant under coordinate permutations and the global sign change
\(x\mapsto-x\), although not under independent coordinate sign changes.

For its positive-objective central paths,
\[
 \boxed{\displaystyle
 \sup_{w_i>0,\ s_0<s_1}
 {L_F(x_w|_{[s_0,s_1]})\over d_F(x_w(s_0),x_w(s_1))}
 \ \geq\ \Gamma_r,}\qquad
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
             ={1\over4}\log r+O(1).                           \tag{3}
\]
Thus genuine dense coupling can be added without spending even one unit
of barrier parameter, yet it does not reduce the sharp
\(\Theta(\sqrt{\log r})\) separable centrality tax.

This is an explicit existence result.  It neither proves the tax for every
optimal box barrier nor rules out another custom coupled barrier with
uniformly smaller worst central paths.

## 1. Standard self-concordance survives the dense quadratic

Write \(u(t)=-\log(1-t^2)\).  Since the added quadratic has zero third
derivative,
\[
 D^3F(x)[h,h,h]=D^3U(x)[h,h,h].                                \tag{4}
\]
The standard self-concordance of \(U\) and
\(\nabla^2F=\nabla^2U+\beta{\bf1}{\bf1}^T\succeq\nabla^2U\)
therefore imply
\[
 |D^3F(x)[h,h,h]|
 \leq2\bigl(h^T\nabla^2U(x)h\bigr)^{3/2}
 \leq2\bigl(h^T\nabla^2F(x)h\bigr)^{3/2}.                    \tag{5}
\]
The quadratic is finite on the closed cube, while \(U\) blows up on its
boundary, so \(F\) is a standard self-concordant barrier once its gradient
parameter is bounded.

## 2. Exact parameter by Sherman--Morrison

Let
\[
 D=\nabla^2U(x)=\operatorname{Diag}(u''(x_i)),\quad
 q=\nabla U(x),\quad t={\bf1}^Tx,
\]
and define
\[
 A={\bf1}^TD^{-1}{\bf1},\qquad
 B={\bf1}^TD^{-1}q,\qquad
 C=q^TD^{-1}q.                                                  \tag{6}
\]
Sherman--Morrison gives the exact squared local dual gradient norm
\[
\begin{aligned}
 Q(x)&=\nabla F(x)^T\nabla^2F(x)^{-1}\nabla F(x)\\
 &=C+{\beta(2tB-B^2)+\beta^2t^2A\over1+\beta A}.              \tag{7}
\end{aligned}
\]
For the interval summand,
\[
 {u'(x_i)^2\over u''(x_i)}={2x_i^2\over1+x_i^2},
\]
so, on putting
\[
 M=r-C=\sum_i{1-x_i^2\over1+x_i^2},                            \tag{8}
\]
direct calculation yields
\[
 |B|\leq M,\qquad A\leq{M\over2},\qquad |t|<r.                \tag{9}
\]
Indeed,
\[
 D_{ii}^{-1}q_i={x_i(1-x_i^2)\over1+x_i^2},\qquad
 D_{ii}^{-1}={(1-x_i^2)^2\over2(1+x_i^2)}.
\]
Dropping the nonpositive term \(-\beta B^2\) and using (9), the correction
in (7) is at most
\[
 \left(2\beta r+{\beta^2r^2\over2}\right)M
 ={17\over32}M<M.                                               \tag{10}
\]
Consequently \(Q(x)<C+M=r\) everywhere in the cube, proving
\(\nu(F)\leq r\).

The reverse inequality follows either from the cube's simple-vertex lower
bound or directly along \(x=(1-\tau){\bf1}\).  The quadratic remains
bounded while
\(U(x)=-r\log\tau+O(1)\); hence the one-dimensional squared local gradient
norm tends to \(r\).  Thus the supremum of \(Q\) is \(r\), proving (2).

## 3. Multiscale central path

Put
\[
 \alpha_i=\sqrt i-\sqrt{i-1},\qquad
 w_i(T)=e^{T\alpha_i},\qquad i=1,\ldots,r.                     \tag{11}
\]
Let \(x_T(s)\) solve
\[
                    \nabla F(x_T(s))=e^s w(T),\qquad s\leq0. \tag{12}
\]
Every weight is positive, so the linear objective has the unique closed-cube
optimizer \({\bf1}\).  The coupling gradient and Hessian obey the global
bounds
\[
 \|\beta({\bf1}^Tx){\bf1}\|_\infty\leq\beta r={1\over4},
 \qquad0\preceq\beta{\bf1}{\bf1}^T\preceq{1\over4}I.          \tag{13}
\]

Set \(z=e^sw(T)\), \(D=\nabla^2U(x_T(s))\), and
\(H=D+\beta{\bf1}{\bf1}^T\).  Differentiating (12) gives
\[
 \|\dot x_T(s)\|_{F,x_T(s)}^2=z^TH^{-1}z.                    \tag{14}
\]
For any coordinate subset \(A\), restrict the inverse-quadratic variational
formula to trial vectors supported on \(A\), and then use (13):
\[
 z^TH^{-1}z
 \geq z_A^TH_{AA}^{-1}z_A
 \geq\sum_{i\in A}{z_i^2\over u''(x_{T,i})+1/4}.             \tag{15}
\]
Stationarity says
\[
                    u'(x_{T,i})=z_i-\beta{\bf1}^Tx_T,
\]
and the subtracted term has magnitude at most \(1/4\).  Since
\[
 {u'(x)^2\over u''(x)}={2x^2\over1+x^2}\longrightarrow1
 \quad(x\uparrow1),                                           \tag{16}
\]
for every \(\delta>0\) there is a fixed \(Z=Z(\delta)>1\) such that
\[
 z_i\geq Z\quad\Longrightarrow\quad
 {z_i^2\over u''(x_{T,i})+1/4}\geq1-\delta.                  \tag{17}
\]

The activation times \(\tau_i=\log Z-T\alpha_i\) are ordered.  Integrating
(14)--(17) over the successive prefix-activation intervals gives
\[
\begin{aligned}
 L_F(x_T|_{(-\infty,0]})
 &\geq\sqrt{1-\delta}\left[
 \sum_{j=1}^{r-1}\sqrt j\,T(\alpha_j-\alpha_{j+1})
 +\sqrt r(T\alpha_r-\log Z)\right]\\
 &=\sqrt{1-\delta}
          \left[T\Gamma_r^2-\sqrt r\log Z\right].            \tag{18}
\end{aligned}
\]

## 4. Endpoint distance in the actual coupled metric

Let
\[
 \rho(x)=\int_0^x\sqrt{u''(a)}\,da,
 \qquad y_{T,i}=\rho(x_{T,i}(0)).                              \tag{19}
\]
The bounded coupling gradient, (11)--(12), and
\(\rho((u')^{-1}(e^a))=a+c+o(1)\) give, for fixed \(r\),
\[
 y_{T,i}=T\alpha_i+O_r(1),\qquad
                       \|y_T\|_2=T\Gamma_r+O_r(1).            \tag{20}
\]
For all large \(T\), every terminal coordinate is positive.  Join the
origin to \(x_T(0)\) by the coordinatewise \(U\)-geodesic
\[
                    \rho(\gamma_i(q))=q y_{T,i},\qquad0\leq q\leq1.
                                                                    \tag{21}
\]
Its \(U\)-length is \(\|y_T\|_2\).  The quadratic-metric contribution is
\[
 \int_0^1\sqrt\beta\,|{\bf1}^T\dot\gamma(q)|\,dq
 =\sqrt\beta\,{\bf1}^Tx_T(0)
 \leq\sqrt\beta\,r={\sqrt r\over2}.                          \tag{22}
\]
Therefore
\[
 d_F(0,x_T(0))
 \leq L_F(\gamma)
 \leq T\Gamma_r+O_r(1).                                      \tag{23}
\]
Divide (18) by (23), send \(T\to\infty\), and then
\(\delta\downarrow0\).  This proves (3).  The analytic-center start is the
limit \(s_0\to-\infty\); finite starts approximate the same ratio.

## Scope and novelty boundary

The result is a primal Hessian-metric, exact-central-path comparison with
the shortest path to the same endpoint.  It is not a distance-to-accuracy,
central-neighborhood iteration, finite-bit, or query lower bound.  The
barrier is permutation invariant and centrally symmetric, but not invariant
under arbitrary independent coordinate sign changes; it must not be called
hyperoctahedrally invariant.

The interval barrier, convex quadratic perturbation, and
Sherman--Morrison identity are standard.  The candidate contribution is the
exact-parameter coupled construction and its sharp surviving tax.  A targeted
search found no matching statement, but priority requires specialist review.

### Targeted primary-source screen (2026-09-04)

Quadratic augmentation of a self-concordant barrier is established prior
art.  Nesterov--Vial,
[*Augmented Self-Concordant Barriers and Nonlinear Optimization Problems
with Finite Complexity*](https://doi.org/10.1007/S10107-003-0392-8),
study \(F(x)+\frac12\langle Qx,x\rangle\) for an arbitrary positive
semidefinite \(Q\) and develop central-path and analytic-center complexity.
Their base domain is a cone and they stress that a nonzero quadratic makes
the augmented function self-concordant but not a self-concordant *barrier*
in the bounded-gradient-parameter sense on that unbounded domain.  The
paper is nevertheless the direct antecedent for the PSD-quadratic
perturbation idea and the Hessian-order argument in (5).

Even closer, Castro--Cuesta,
[*Quadratic Regularizations in an Interior-Point Method for Primal
Block-Angular Problems*](https://doi.org/10.1007/s10107-010-0341-2),
Section 4.1, study on a box
\[
 {1\over2}x^TQx-\sum_i\log x_i-\sum_i\log(u_i-x_i)
\]
with diagonal \(Q\succeq0\).  Their Lemma 4 proves exact scalar barrier
parameter one when \(0\le q_i\le1/u_i^2\), hence exact parameter \(r\) for
the resulting separable product.  Castro--Cuesta,
[*Existence, Uniqueness, and Convergence of the Regularized Primal--Dual
Central Path*](https://doi.org/10.1016/j.orl.2010.07.010), then studies the
associated regularized primal--dual path.  These sources mean that neither
“quadratic regularization of a box barrier” nor “small quadratic
regularization preserving the optimal parameter” can be claimed as new.
Their regularizer is diagonal, so its Hessian and barrier remain separable;
they do not treat the dense rank-one coupling in (1) or central-arc versus
same-endpoint distance.

Papa Quiroz--Oliveira's
[*New Self-Concordant Barrier for the
Hypercube*](https://doi.org/10.1007/s10957-007-9220-2) is another explicit
nonstandard but separable cube barrier.  Nesterov--Todd's product metric
examples and Nesterov--Nemirovski's general bounded-domain
\(O(\nu^{1/4})\) comparison supply the classical Riemannian framework.
The universal and entropic barriers have optimal parameter \(r\), but both
factor coordinatewise on a Cartesian box and hence do not supply a dense
coupled comparator.

The targeted search did not locate a dense non-diagonal quadratic
augmentation of the standard box barrier with a proved exact unchanged
parameter \(r\), nor the same construction combined with the sharp
\(\Gamma_r\) multiscale distortion.  The conservative label is therefore
**candidate dense-coupled optimal-parameter specialization and sharp
centrality-tax synthesis**.  Its defensible distinction is the conjunction
of dense coupling, exact optimal parameter, and \(\Gamma_r\) same-endpoint
distortion—not quadratic augmentation or exact parameter preservation by
itself.  This was a targeted screen through 2026, not an exhaustive novelty
or priority determination.

## Audit targets

1. Recompute (7) and the bounds (8)--(10), especially the exact parameter.
2. Verify that increasing the Hessian while leaving the third derivative
   unchanged preserves standard self-concordance.
3. Check (15), including the restricted inverse variational formula.
4. Verify the activation integral and summation by parts in (18).
5. Confirm that (21)--(23) bound distance in the actual coupled metric and
   that the symmetry claim is not overstated.

## Independent hostile audit record

**PASS.**  Expanding Sherman--Morrison gives (7) exactly: after placing
the terms over \(1+\beta A\), all mixed
\(\beta^2tAB\) and cubic \(\beta^3t^2A^2\) terms cancel.  The coordinate
formulas below (9) imply \(|B|\leq M\) and \(A\leq M/2\), so the positive
part of the correction is at most \(17M/32\).  Hence the full local
gradient norm is strictly below \(r\) in the interior.  Along the positive
vertex ray the directional local gradient norm tends to \(r\), proving
the exact supremum rather than only an upper parameter certificate.

The added quadratic has identically zero third derivative and a positive
semidefinite Hessian, so (5) is a valid direct proof of standard
self-concordance.  Its Hessian has sole nonzero eigenvalue
\(\beta r=1/4\), and its coordinate gradient magnitude is at most \(1/4\),
which verifies every perturbation bound in (13)--(17).  Restricting the
variational inverse formula to active-coordinate trial vectors proves the
first inequality in (15); inverse Loewner order proves the second.  The
prefix interval lengths and summation by parts in (18) give exactly
\(T\Gamma_r^2-\sqrt r\log Z\).

Finally, the coordinatewise \(U\)-geodesic is only a comparison path.  For
large \(T\), all its coordinates increase from zero, so its added quadratic
metric length is exactly the endpoint sum in (22), \(O_r(1)\).  Thus (23)
is an upper bound in the actual \(F\)-metric.  The construction uses all
strictly positive weights and reaches \(\Gamma_r\), but its symmetry group
contains permutations and global sign reversal only; the note correctly
does not claim independent-sign, hyperoctahedral invariance.  No
distance-to-accuracy, discrete-round, finite-bit, or all-barrier conclusion
is implicit.
