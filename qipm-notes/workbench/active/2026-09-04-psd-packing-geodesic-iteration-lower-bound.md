# A path-independent iteration lower bound for cross-packed PSD lifts

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Cross-packing many ball groups into dense PSD completion blocks does not
create a shortcut in the standard restricted log-determinant metric.  The
off-diagonal completion variables may move arbitrarily, yet every algorithm
built from bounded Dikin chords needs

\[
                 \Omega\!\left(\sqrt H\log{b\over\epsilon}\right)
\]

moves from the analytic center, where \(b\) is the number of source balls
and \(H\) is the total number of packed group columns.  This is an actual
small-step lower bound for the fixed lift and barrier, not an inference from
their barrier parameter.

Partition each of the \(b\) copies of \(B_2^s\) into \(h\) nonempty
coordinate groups, so \(H=bh\).  Pack the group columns into arbitrary
blocks \(\ell\), with \(c_\ell\) columns in block \(\ell\) and
\(\sum_\ell c_\ell=H\).  The relative-open packed slice is

\[
 \Omega=\left\{(S_\ell,W_\ell)_\ell:
 D_\ell:=S_\ell-W_\ell^TW_\ell\succ0,\quad
 \sum_{\gamma:a(\gamma)=a}(S_{\ell(\gamma)})_{\gamma\gamma}=1
 \ (a\in[b])\right\},                                  \tag{1}
\]

with standard restricted barrier

\[
                         F=-\sum_\ell\log\det D_\ell.     \tag{2}
\]

Write the concatenated projected vector of source ball \(a\) as \(w_a\).
For unit vectors \(c_a\), maximize

\[
                         \ell(w)=\sum_{a=1}^bc_a^Tw_a.    \tag{3}
\]

Let \(z(\tau)\) minimize \(F-\tau\ell\).  At \(z(\tau_0)\), every
completion block satisfies

\[
 D_\ell=q_0I_{c_\ell},\qquad
 q_0={2\over\sqrt{h^2+\tau_0^2}+h}.                      \tag{4}
\]

Fix \(\epsilon>0\), \(0\leq\rho<1\), \(0<R<1\), and an integer
\(m\geq1\).  Start at any \(x_0\in\Omega\) with
\(\|x_0-z(\tau_0)\|_{z(\tau_0)}\leq\rho\).  Suppose each of \(T\) outer
rounds contains at most \(m\) feasible chords, each of starting-point local
norm at most \(R\).  No centrality condition is imposed after \(x_0\).  If
the last point has objective gap at most \(\epsilon\), then

\[
 \boxed{
 T\geq {\left[
       \sqrt H\log\!\left({q_0H\over2\epsilon}\right)
       -\log{1\over1-\rho}\right]_+
       \over m\log{1\over1-R}}.}                         \tag{5}
\]

All local norms and distances are induced by the Hessian of (2) after
restriction to the affine hull of (1).

At the analytic center \(\tau_0=0\), \(q_0=1/h\), so (5) becomes

\[
 T\geq {\left[
       \sqrt H\log\!\left({b\over2\epsilon}\right)
       -\log{1\over1-\rho}\right]_+
       \over m\log{1\over1-R}}.                         \tag{6}
\]

The bound is independent of the packing pattern and the off-diagonal
completion dimension.  In particular it applies to the one-block
order-\((s+b)\) lift with \(h=1\), \(H=b\), as well as to capped
multi-block column packing.

The same restricted standard barrier has exact parameter \(H\), so its
usual short-step upper bound is
\(O(\sqrt H\log(b/\epsilon))\) from the analytic center, up to standard
constant-neighborhood conventions.  Hence (6) matches the generic
short-step dependence on \(H\) and \(\epsilon\) inside this movement model;
packing reduces factor count, not the number of small metric moves.

## 1. The log-determinant metric controls determinant change

For one block, along an affine tangent \((\dot S,\dot W)\), put
\(\dot D=\dot S-\dot W^TW-W^T\dot W\).  Direct differentiation of
\(-\log\det(S-W^TW)\) gives

\[
 \nabla^2F_\ell[(\dot S,\dot W)]^2
 =\operatorname{tr}\!\left((D_\ell^{-1}\dot D_\ell)^2\right)
  +2\operatorname{tr}\!\left(
       D_\ell^{-1}\dot W_\ell^T\dot W_\ell\right).       \tag{7}
\]

The second term is nonnegative.  With
\(A_\ell=D_\ell^{-1/2}\dot D_\ell D_\ell^{-1/2}\), trace
Cauchy--Schwarz gives

\[
 \nabla^2F_\ell[(\dot S,\dot W)]^2
 \geq\operatorname{tr}(A_\ell^2)
 \geq{1\over c_\ell}(\operatorname{tr}A_\ell)^2
 ={1\over c_\ell}\left({d\over dt}\log\det D_\ell\right)^2. \tag{8}
\]

Therefore, for every piecewise \(C^1\) curve from \(x\) to \(y\), its
barrier-metric length is at least

\[
 \left(\sum_\ell{1\over c_\ell}
   \left[\log\det D_\ell(y)-\log\det D_\ell(x)\right]^2
       \right)^{1/2}.                                    \tag{9}
\]

This inequality includes arbitrary off-diagonal auxiliary motion.  Such
motion only adds the second nonnegative term in (7).

## 2. Accuracy forces total determinant collapse

For an \(\epsilon\)-accurate point \(y\), put

\[
 \delta_a=1-c_a^Tw_a(y),\qquad
 d_\gamma=(D_{\ell(\gamma)}(y))_{\gamma\gamma}.
\]

Feasibility and the affine equations in (1) give

\[
 \sum_{\gamma:a(\gamma)=a}d_\gamma
 =1-\|w_a(y)\|^2
 \leq1-(c_a^Tw_a(y))^2
 \leq2\delta_a.                                        \tag{10}
\]

Moreover, \(\delta_a\geq0\) and \(\sum_a\delta_a\leq\epsilon\).
Hadamard's determinant inequality, followed by AM--GM within each source
ball and then across the \(b\) source gaps, yields

\[
\begin{aligned}
 \prod_\ell\det D_\ell(y)
 &\leq\prod_\gamma d_\gamma\\
 &\leq\prod_{a=1}^b\left({2\delta_a\over h}\right)^h
 \leq\left({2\epsilon\over bh}\right)^{bh}
 =\left({2\epsilon\over H}\right)^H.                  \tag{11}
\end{aligned}
\]

At the center (4),

\[
                 \prod_\ell\det D_\ell(z(\tau_0))=q_0^H. \tag{12}
\]

Apply weighted Cauchy--Schwarz to (9):

\[
 \left|\sum_\ell\Delta\log\det D_\ell\right|
 \leq\sqrt{\sum_\ell c_\ell}
       \left(\sum_\ell{(\Delta\log\det D_\ell)^2\over c_\ell}
       \right)^{1/2}.
\]

Together with (11)--(12), this proves the distance bound

\[
 d_F\bigl(z(\tau_0),\{y:b-\ell(y)\leq\epsilon\}\bigr)
 \geq\left[\sqrt H\log{q_0H\over2\epsilon}\right]_+.   \tag{13}
\]

This is the step that rules out off-diagonal completion shortcuts.

## 3. Center and bounded-move conversion

For fixed projected columns and fixed diagonal of every \(D_\ell\),
Hadamard's inequality shows that (2) is minimized when every \(D_\ell\)
is diagonal.  Partial minimization over the completion variables therefore
reduces (2) to the grouped barrier

\[
                 -\sum_\gamma\log(s_\gamma-\|w_\gamma\|^2).
\]

Its stationarity equations give (4), including at \(\tau_0=0\).

Finally, a chord of starting local norm \(r\leq R<1\) lies in the Dikin
ellipsoid.  Self-concordant Hessian comparison bounds the length of its
straight segment by

\[
                       -\log(1-r)\leq\log{1\over1-R}.     \tag{14}
\]

An initial center-norm error at most \(\rho\) costs at most
\(\log(1/(1-\rho))\) by the same estimate and the triangle inequality.
Concatenating at most \(mT\) chords with (13) proves (5).

There is also an exact variable-step tradeoff.  For arbitrary successive
starting-point chord norms \(r_j<1\),

\[
 \sum_j\log{1\over1-r_j}
 \geq\left[
   \sqrt H\log{q_0H\over2\epsilon}
       -\log{1\over1-\rho}\right]_+.                    \tag{15}
\]

Consequently, among \(M\) chords at least one satisfies

\[
 r_j\geq1-\exp\!\left(-{1\over M}\left[
   \sqrt H\log{q_0H\over2\epsilon}
       -\log{1\over1-\rho}\right]_+\right).             \tag{16}
\]

Any improvement over the \(\sqrt H\)-scale move count must therefore use
a chord approaching the unit Dikin radius; off-diagonal completion motion
does not change this tradeoff.

## 4. Heterogeneous groups and objective weights

The determinant argument also gives an entropy-sensitive heterogeneous
form.  Let source ball \(a\) have \(h_a\geq1\) packed group columns, put

\[
 H=\sum_ah_a,\qquad p_a={h_a\over H},\qquad
 \ell_\lambda(w)=\sum_a\lambda_ac_a^Tw_a,\qquad\lambda_a>0. \tag{17}
\]

and define

\[
                 \Delta_{\rm eff}
                    =\prod_a\left({\lambda_a\over p_a}\right)^{p_a}.
                                                                    \tag{18}
\]

At the analytic center, the diagonal residuals belonging to source \(a\)
equal \(1/h_a\).  If
\(e_a=\lambda_a(1-c_a^Tw_a)\) and \(\sum_ae_a\leq\epsilon\), the same
Hadamard and source-wise AM--GM argument gives

\[
 \prod_\ell\det D_\ell
 \leq\prod_a\left({2e_a\over\lambda_ah_a}\right)^{h_a}.
\]

Under \(\sum_ae_a\leq\epsilon\), the right side is maximized at
\(e_a=\epsilon p_a\).  Comparing with the center determinant
\(\prod_ah_a^{-h_a}\) yields

\[
 d_F(\text{analytic center},\{\text{gap}\leq\epsilon\})
 \geq\left[\sqrt H\log{\Delta_{\rm eff}\over2\epsilon}\right]_+.
                                                                    \tag{19}
\]

The approximate-start and bounded-round conversion in (5) applies
unchanged with the logarithmic term from (19).  For equal weights,
\(\Delta_{\rm eff}=\exp(-\sum_ap_a\log p_a)\), so the scale is the
exponential entropy of the distribution of group counts.  Equal group
counts recover \(\Delta_{\rm eff}=b\).  An independent hostile audit
checked (17)--(19), including the endpoint maximization and all powers of
\(h_a\).

## Scope and novelty boundary

The result concerns the Hessian metric of the fixed standard restricted
log-determinant (2) on the packed affine slice (1).  It does not apply to
arbitrary custom barriers, steps of local norm at least one, rounds with an
unbounded number of uncounted substeps, or algorithms whose state is not a
sequence of feasible primal iterates.  Computation between counted moves is
unrestricted.

The affine-invariant log-determinant metric, Hadamard's inequality, and the
conversion from Riemannian distance to bounded Dikin moves are classical.
A targeted local search found no prior application combining them into
(5) for cross-packed product-ball PSD completions.  The potentially new
part is the exact distance-to-accuracy estimate, especially its immunity to
off-diagonal completion paths.  Priority remains subject to specialist
review.

## Independent audit

An independent hostile audit rederived (7) for arbitrary off-diagonal
\(S,W\) directions, checked Hadamard and both AM--GM steps in (11), and
verified the weighted Cauchy--Schwarz constant in (13).  It also derived
the center directly from the \(S\)- and \(W\)-stationarity equations and
confirmed that \(D_\ell=q_0I\) even when a block packs several source
balls.  Finally, it checked the approximate-start subtraction and
bounded-chord conversion.  No correction was required.  The audited
headline is deliberately over real symmetric PSD matrices; complex and
quaternionic analogues require their determinant and real-trace conventions
to be stated separately.
