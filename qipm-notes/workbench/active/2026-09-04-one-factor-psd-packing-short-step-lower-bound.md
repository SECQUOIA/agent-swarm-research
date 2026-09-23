# One PSD factor still forces square-root-many short-step rounds

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Fix \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(a=\dim_{\mathbb R}\mathbb F\), and let

\[
                       C=\prod_{j=1}^h B_2^{s_j}.                       \tag{1}
\]

Choose \(p\geq\max_j\lceil s_j/a\rceil\), embed each
\(\mathbb R^{s_j}\) isometrically in \(\mathbb F^p\), and collect the
embedded coordinates as columns \(w_j\) of
\(W\in\mathbb F^{p\times h}\).  The one-factor packed lift is

\[
 \Omega=\left\{(S,W):
 Z=\begin{pmatrix}S&W^*\\W&I_p\end{pmatrix}\succ0,
 \quad S_{jj}=1\ (j=1,\ldots,h)\right\}.                              \tag{2}
\]

It projects exactly onto the interior of (1).  Use the restricted standard
barrier

\[
              F(S,W)=-\log\det Z=-\log\det(S-W^*W).                    \tag{3}
\]

For each source choose a unit objective vector \(c_j\), and maximize

\[
                         \ell(W)=\sum_{j=1}^h c_j^Tw_j.                 \tag{4}
\]

Although (2) has only **one PSD cone factor**, bounded local-norm steps
cannot reach an accurate point quickly, even with no central-neighborhood
assumption.  Start at the analytic center

\[
                         W_0=0,\qquad S_0=I_h.                         \tag{4a}
\]

Let an outer round contain at most \(m\) arbitrary substeps, each of local
\(F\)-norm at most \(R<1\), measured at its starting point.  If the final
point has \(h-\ell(W_T)\leq\epsilon<h/2\), then

\[
 \boxed{\displaystyle
   T\geq {\sqrt h\over m\log(1/(1-R))}
               \log{h\over2\epsilon}.}                               \tag{4b}
\]

The intermediate and outer points may be anywhere in \(\Omega\), and the
directions are unrestricted.  Thus (4b) is a path-independent
bounded-Dikin-step lower bound, not merely a central-path length statement.

For comparison, a late-start tube theorem below gives the scale

\[
                  \boxed{\displaystyle
                  \Omega\!\left(\sqrt h\log(\Delta/\epsilon)\right)}  \tag{5}
\]

outer rounds to reach objective error \(\epsilon\).  Both bounds hold
uniformly over the three division algebras.  They show that factor-count
compression by PSD column sharing does not imply a comparable reduction in
optimization rounds: the exact
restricted parameter and barrier geometry remain controlled by the number
\(h\) of independently tight source balls.

More precisely, let \(z(\tau)\) minimize \(F-\tau\ell\) on \(\Omega\).
Fix constants \(\alpha>0\),
\(0\leq\rho<\gamma_\alpha\), \(0<R<1\), and integer \(m\geq1\), where

\[
                   \gamma_\alpha=1+\alpha-\sqrt{1+\alpha^2}.           \tag{6}
\]

Suppose accepted outer iterates obey

\[
 \alpha\leq\tau_0\leq\cdots\leq\tau_T,
 \qquad \|z_j-z(\tau_j)\|_{z(\tau_j)}\leq\rho,                        \tag{7}
\]

and each outer transition is a chain of at most \(m\) substeps, each of
local Hessian norm at most \(R\), measured at the substep's starting point.
The intermediate points may leave the tube.  Put \(\Delta=h/\tau_0\).  If

\[
                              h-\ell(z_T)\leq\epsilon,                  \tag{8}
\]

then

\[
 T\geq c_{\alpha,\rho,R,m}\sqrt h
       \log\!\left({(\gamma_\alpha-\rho)\Delta\over\epsilon}\right)   \tag{9}
\]

whenever the logarithm is positive.  The explicit constant is

\[
 c_{\alpha,\rho,R,m}=
 { (1-\rho)\sqrt{1-(1+\alpha^2)^{-1/2}} \over
   (1-R)^{-m}-1+\frac{\rho}{(1-\rho)^2}
 [1+(1-R)^{-m}]}.                                  \tag{10}
\]

## Path-independent barrier-height proof

At any feasible point put

\[
                 \delta_j=1-c_j^Tw_j\geq0,
                 \qquad q_j=D_{jj}=1-\|w_j\|^2.                         \tag{10a}
\]

Since \(c_j\) is a unit vector and \(\|w_j\|<1\),

\[
                  q_j=(1-\|w_j\|)(1+\|w_j\|)
                       \leq2\delta_j.                                  \tag{10b}
\]

If \(h-\ell(W)=\sum_j\delta_j\leq\epsilon\), Hermitian Hadamard and
AM--GM give, using the Moore determinant over \(\mathbb H\),

\[
              \det D\leq\prod_jq_j
                    \leq\prod_j2\delta_j
                    \leq\left({2\epsilon\over h}\right)^h.            \tag{10c}
\]

Thus every \(\epsilon\)-accurate point has

\[
                         F\geq h\log{h\over2\epsilon},                 \tag{10d}
\]

whereas the analytic center (4a) has \(F=0\).

The exact restricted gradient parameter of \(F\) is \(h\).  Hence along a
substep \(\Delta\) with \(r=\|\Delta\|_x\leq R<1\), the gradient
inequality and self-concordant Hessian comparison give

\[
 \begin{aligned}
 |F(x+\Delta)-F(x)|
 &\leq\sqrt h\int_0^1\|\Delta\|_{x+t\Delta}\,dt\\
 &\leq\sqrt h\int_0^1{r\over1-tr}\,dt
  =\sqrt h\log{1\over1-r}
  \leq\sqrt h\log{1\over1-R}.                          \tag{10e}
 \end{aligned}
\]

Telescoping absolute barrier changes from (4a) to (10d) requires at least
\(\sqrt h\log[h/(2\epsilon)]/\log[1/(1-R)]\) substeps.  At most \(m\)
substeps per outer round proves (4b).

## Exact packed central path

Put \(D=S-W^*W\).  Stationarity in every free off-diagonal entry of \(S\)
forces \(D^{-1}\), hence \(D\), to be diagonal.  Stationarity in column
\(w_j\) then gives

\[
                    {2w_j\over q_j}=\tau c_j,qquad
                    q_j=D_{jj}=1-\|w_j\|^2.                            \tag{11}
\]

Thus every column has the same scalar profile

\[
 \begin{aligned}
 d(\tau)&=\sqrt{1+\tau^2},\\
 q(\tau)&={2\over d(\tau)+1},\\
 r(\tau)&={\tau\over d(\tau)+1},\\
 w_j(\tau)&=r(\tau)c_j,\\
 D(\tau)&=q(\tau)I_h,\\
 S(\tau)&=W(\tau)^*W(\tau)+q(\tau)I_h.
 \end{aligned}                                                         \tag{12}
\]

In particular,

\[
 \ell(z(\tau))=hr(\tau),\qquad
 g(\tau):=h-\ell(z(\tau))=h(1-r(\tau)),                              \tag{13}
\]

and

\[
                    {\tau g(\tau)\over h}
                    =1+\tau-\sqrt{1+\tau^2}=\gamma_\tau.              \tag{14}
\]

The function \(\gamma_\tau\) increases to one, so
\(\tau g(\tau)\geq\gamma_\alpha h\) for \(\tau\geq\alpha\).

Let \(H_\tau=\nabla^2F(z(\tau))\) on the affine hull of (2).  The
central-path identity \(H_\tau z'(\tau)=\nabla\ell\) gives the exact
logarithmic-parameter speed without needing to invert the packed Hessian:

\[
 \begin{aligned}
 \beta(\tau)^2
  &:=\left\|{dz\over d\log\tau}\right\|_{z(\tau)}^2
    =\tau^2{d\over d\tau}\ell(z(\tau))\\
  &=h\left(1-{1\over\sqrt{1+\tau^2}}\right).
 \end{aligned}                                                         \tag{15}
\]

Consequently, for \(\tau\geq\alpha\),

\[
       b_\alpha\sqrt h\leq\beta(\tau)<\sqrt h,qquad
       b_\alpha=\sqrt{1-(1+\alpha^2)^{-1/2}}.                          \tag{16}
\]

This is exactly the speed scale of \(h\) direct one-ball barriers, even
though all columns share one PSD factor.

## Bounded-substep lower bound

The remainder is a general self-concordant metric argument.  It is stated
and audited in full in
[A genuine short-step iteration lower bound for grouped ball
lifts](2026-09-04-grouped-ball-short-step-iteration-lower-bound.md).
Only (14)--(16) are formulation-specific.

For completeness, set

\[
 B_\rho={\rho\over(1-\rho)^2},\qquad
 A=(1-R)^{-m}-1+B_\rho[1+(1-R)^{-m}].                                  \tag{17}
\]

Tube centrality, Hessian comparison, and the geometric sum over at most
\(m\) substeps imply

\[
          (\tau_{j+1}-\tau_j)\|\nabla\ell\|_{z_j,*}\leq A.             \tag{18}
\]

The lower speed bound and tube comparison give

\[
       \tau_j\|\nabla\ell\|_{z_j,*}
             \geq(1-\rho)b_\alpha\sqrt h.                             \tag{19}
\]

Hence each outer round changes \(\log\tau\) by at most
\(A/[(1-\rho)b_\alpha\sqrt h]\).  At the endpoint, Cauchy--Schwarz in
the center metric and \(\beta(\tau_T)\leq\sqrt h\) give

\[
 |\ell(z_T)-\ell(z(\tau_T))|
       \leq{\rho\sqrt h\over\tau_T}.
\]

Combining this with (8), (14), and \(\sqrt h\leq h\) yields

\[
                         \tau_T\geq
                         { (\gamma_\alpha-\rho)h\over\epsilon}.        \tag{20}
\]

Telescoping the per-round logarithmic change from
\(\tau_0=h/\Delta\) to (20) proves (9)--(10).

## Barrier and scope

The packed barrier (3) has exact restricted gradient parameter \(h\), as
proved in
[Private-nullity law for Hermitian PSD lifts of products of
balls](2026-09-04-hermitian-product-ball-private-nullity.md).  Thus (9)
matches its usual square-root parameter scale, but unlike a parameter-only
statement it is an actual lower bound for the explicitly defined
bounded-substep tube class.

The stronger bound (4b) permits arbitrary directions and arbitrary
computation inside a round and imposes no tube or path-parameter condition.
It does require the analytic-center start, the fixed standard barrier,
substeps of local norm below one, and a bounded number of such substeps per
round.  The late-start bound (9) replaces the analytic-center assumption by
the tube and path-parameter assumptions.  Neither result covers an
unbounded number of substeps, a different barrier or lift, higher-order
predictor arcs not decomposed into bounded local steps, or general IPMs and
QIPMs.

## Audit record

An independent hostile audit checked projection exactness, stationarity in
all real components of the free Hermitian off-diagonal entries, the
real/complex/quaternionic gradient normalization, formulas (11)--(16), and
the use of the full packed Hessian in the speed identity.  It also checked
the endpoint scaling from (14), the tube-to-center norm comparison, and the
constant in (9)--(10).  The audit found and repaired one corrupted `\frac`
in (10); it found no mathematical defect.

A second hostile check verified the path-independent strengthening
(10a)--(10e): Hermitian Hadamard including the quaternionic Moore
determinant, the objective-gap bound on every diagonal residual, the exact
restricted gradient parameter, and the integrated Dikin norm comparison.
It found no correction.
