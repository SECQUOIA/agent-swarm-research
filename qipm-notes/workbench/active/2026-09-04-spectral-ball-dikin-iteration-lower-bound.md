# A path-independent bounded-Dikin lower bound for spectral-norm balls

Status: Proved and independently hostile-audited, including the full singular-weight extension  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated fixed-barrier movement model

## Result

Let \(\mathbb F=\mathbb R\) or \(\mathbb C\), let \(r_a\leq c_a\), put
\(R=\sum_{a=1}^k r_a\), and consider the product
of open spectral-norm balls

\[
 \Omega=\prod_{a=1}^k\{X_a\in\mathbb F^{r_a\times c_a}:
                                  \|X_a\|_{\rm op}<1\}.             \tag{1}
\]

Equip it with the standard reduced spectral-cone barrier

\[
 F(X)=-\sum_{a=1}^k\log\det D_a(X_a),
 \qquad D_a(X_a)=I_{r_a}-X_aX_a^*.                                 \tag{2}
\]

For the real-valued Frobenius pairing
\(\langle C,X\rangle_F=\operatorname{Re}\operatorname{tr}(C^*X)\),
choose a full-row-rank objective with compact SVD
\[
 C_a=U_a\operatorname{Diag}(w_{a,1},\ldots,w_{a,r_a})V_a^*,
 \qquad w_{a,i}>0,
\]
and minimize

\[
                         c(X)=-\sum_{a=1}^k
                                  \langle C_a,X_a\rangle_F.         \tag{3}
\]

The infimum (attained on the closed balls) is
\(-\sum_{a,i}w_{a,i}\).  Define

\[
 \overline w_{\rm geom}
    =\left(\prod_{a,i}w_{a,i}\right)^{1/R},
 \qquad
 \Delta_{\rm spec}=R\,\overline w_{\rm geom}.                      \tag{4}
\]

If a feasible interior endpoint has objective error at most \(\epsilon\),
then its Riemannian distance from the analytic center \(0\), in the Hessian
metric of \(F\), obeys

\[
 \boxed{
 d_F(0,X)\ \geq\
 \sqrt R\left[\log{\Delta_{\rm spec}\over2\epsilon}\right]_+.}     \tag{5}
\]

Consequently, any sequence \(X^0=0,X^1,\ldots,X^T\) ending at such a point
and satisfying the forward Dikin-chord contract

\[
                  \|X^{j+1}-X^j\|_{X^j}\leq\delta<1               \tag{6}
\]

requires

\[
 \boxed{
 T\ \geq\ {\sqrt R\over-\log(1-\delta)}
       \left[\log{\Delta_{\rm spec}\over2\epsilon}\right]_+.}     \tag{7}
\]

This is path-independent: the iterates need not follow, or remain near, the
central path.  It applies identically after any shared-scale grouping of the
matrix balls in the companion spectral-cone construction, because fixing the
group scales to one gives exactly (2).

The earlier block-weight form is the specialization
\(C_a=(\lambda_a/r_a)[I_{r_a}\ 0]\).  With
\(p_a=r_a/R\), (4) then becomes
\[
        \Delta_{\rm spec}
          =\prod_a\left({\lambda_a\over p_a}\right)^{p_a}.
                                                                    \tag{4a}
\]
For the normalized choice \(\lambda_a=p_a\), one has
\(\Delta_{\rm spec}=1\).  The exact central path has an explicit feasible
Dikin-chord partition that reaches error \(\epsilon\) in

\[
             O_\delta\!\left(\sqrt R\log{1\over\epsilon}\right)    \tag{8}
\]

moves.  Thus (7) has the correct order, including its \(\sqrt R\)
coefficient, for this fixed barrier and movement model.

## 1. Endpoint determinant collapse

Put \(z_{a,i}=\operatorname{Re}(u_{a,i}^*X_av_{a,i})\).  The objective
error is
\[
              e=\sum_{a,i}w_{a,i}(1-z_{a,i}).                     \tag{9}
\]
Every \(z_{a,i}<1\) at an interior point.  In the \(U_a\) basis, Hadamard's
determinant inequality and \(\|X_a^*u_{a,i}\|\geq
|u_{a,i}^*X_av_{a,i}|\) give
\[
\begin{aligned}
 \det D_a
 &\leq\prod_{i=1}^{r_a}u_{a,i}^*D_au_{a,i}\\
 &=\prod_i\left(1-\|X_a^*u_{a,i}\|^2\right)\\
 &\leq\prod_i\left(1-|u_{a,i}^*X_av_{a,i}|^2\right)\\
 &\leq2^{r_a}\prod_i(1-z_{a,i}).                                  \tag{10}
\end{aligned}
\]
The last step uses \(1-|z|^2\leq1-(\operatorname{Re}z)^2
\leq2(1-\operatorname{Re}z)\).

Set \(e_{a,i}=w_{a,i}(1-z_{a,i})>0\).  If \(e\leq\epsilon\), ordinary
AM--GM across all \(R\) singular directions gives
\[
 \prod_{a,i}(1-z_{a,i})
 ={\prod_{a,i}e_{a,i}\over\prod_{a,i}w_{a,i}}
 \leq {(\epsilon/R)^R\over\prod_{a,i}w_{a,i}}.                    \tag{11}
\]
Multiplying (10) over the blocks yields
\[
       \prod_a\det D_a
       \leq\left({2\epsilon\over\Delta_{\rm spec}}\right)^R.       \tag{12}
\]
Equations (2), (4), and (12) yield

\[
                    F(X)\geq
       R\log{\Delta_{\rm spec}\over2\epsilon}.                     \tag{13}
\]

The positive part in (5) only discards a vacuous negative right-hand side;
indeed \(F(X)\geq F(0)=0\).

## 2. Barrier height controls metric distance

The barrier (2) is an \(R\)-self-concordant barrier.  Equivalently,

\[
                   \|\nabla F(X)\|_{X,*}\leq\sqrt R.               \tag{14}
\]

For one block, an SVD with singular values \(\sigma_i\) gives the exact
squared local dual gradient norm
\(\sum_i2\sigma_i^2/(1+\sigma_i^2)<r_a\); summing over blocks proves the
constant \(R\) in (14).

For every piecewise \(C^1\) curve \(\gamma\) from \(0\) to \(X\),

\[
 F(X)-F(0)
 =\int\langle\nabla F(\gamma),\dot\gamma\rangle
 \leq\sqrt R\int\|\dot\gamma\|_\gamma.                          \tag{15}
\]

Taking the infimum over curves and using \(F(0)=0\) proves (5).

If a chord starts at \(Y\) with \(d=X-Y\) and
\(\|d\|_Y\leq\delta<1\), self-concordant Hessian comparison along
\(Y+td\) gives

\[
 \int_0^1\|d\|_{Y+td}\,dt
 \leq\int_0^1{\delta\over1-t\delta}\,dt
 =-\log(1-\delta).                                                  \tag{16}
\]

The triangle inequality, (5), and (16) prove (7).

## 3. Exact central path and matching construction

Now set \(\lambda_a=p_a=r_a/R\), and define the central point at parameter
\(\tau\geq0\) as the minimizer of \(F+\tau c\).  Orthogonal invariance and
strict convexity give

\[
 X_a(\tau)=r(\tau/R)E_a,
 \qquad
 r(z)={z\over\sqrt{1+z^2}+1},                                     \tag{17}
\]

because each active singular coordinate satisfies

\[
                         {2r\over1-r^2}={\tau\over R}.              \tag{18}
\]

The analytic-center limit \(\tau=0\) is \(r=0\), and the objective error is
exactly \(1-r\).  Along this curve the metric line element is

\[
 ds=\sqrt{2R}\,{\sqrt{1+r^2}\over1-r^2}\,dr.                      \tag{19}
\]

Writing

\[
 y={r\over\sqrt{1+r^2}},\qquad
 \Phi(y)=\sqrt2\,\operatorname{artanh}(\sqrt2y)
                         -\operatorname{artanh}(y),                 \tag{20}
\]

the exact arc length from \(r=0\) to \(r=1-\epsilon\), for
\(0<\epsilon<1\), is

\[
 L_\epsilon=\sqrt{2R}\,
 \Phi\!\left({1-\epsilon\over\sqrt{1+(1-\epsilon)^2}}\right)
 =\Theta\!\left(\sqrt R\log{1\over\epsilon}\right).             \tag{21}
\]

Partition this central arc into pieces of metric length at most
\(\log(1+\delta)\).  Norm transport along a curve segment of length \(a\)
implies that its endpoint chord, measured at its initial point, is at most
\(e^a-1\).  Hence every resulting chord satisfies (6), and the number of
pieces is at most

\[
                    \left\lceil{L_\epsilon\over\log(1+\delta)}
                    \right\rceil,                                  \tag{22}
\]

which proves (8).

## Scope and novelty boundary

The theorem concerns the fixed standard determinant barrier (2), exact-real
feasible iterates, and forward Dikin chords of fixed radius.  It is not an
iteration lower bound for arbitrary barriers, long-step algorithms,
infeasible iterates, coherent-state trajectories, or every QIPM.  Nor does
it imply a per-iteration arithmetic or query lower bound.

The spectral-norm-cone barrier, affine restriction, self-concordant metric
comparison, and scalar determinant AM--GM inequality are classical.  The
candidate contribution is their combination into a path-independent,
singular-scale-sensitive iteration lower bound for products of rectangular
spectral-norm balls, together with the shared-scale invariance and matching
central-path construction.  Priority remains subject to specialist review.

## Audit targets

1. Check the general full-row-rank objective normalization and every
   inequality in (9)--(12), over both \(\mathbb R\) and \(\mathbb C\).
2. Check the geometric-mean scale in (4), including specialization (4a).
3. Verify that the parameter \(R\), rather than \(2R\), is valid in (14).
4. Check the Dikin-chord conversion in both directions, especially (22).
5. Recompute the central path, metric line element, and asymptotic in
   (17)--(21).

## Independent audit record

An independent hostile audit passed the original block-weight version of
all five targets.  It checked its endpoint trace bound, weighted allocation,
and factor \(2\), the exact reduced parameter \(R\), the barrier-height
distance bound, and both Dikin-chord conversions.  It also recomputed
(17)--(21);
the leading central-arc length is
\(\sqrt R\log(1/\epsilon)+O(\sqrt R)\), so the lower-bound coefficient is
asymptotically attained.  No mathematical correction was required.

A follow-up audit passed the full singular-weight extension over both
\(\mathbb R\) and \(\mathbb C\).  It verified Hermitian Hadamard in the
left-singular basis, all inequalities for arbitrary nonaligned endpoints,
and AM--GM on \(e_{a,i}=w_{a,i}(1-z_{a,i})\).  This gives exactly
\(\Delta_{\rm spec}=R(\prod_{a,i}w_{a,i})^{1/R}\), with no hidden
alignment, phase, or rectangular-null-space assumption.
