# Central-path condensation and conditioning in the winner-take-all SDP

Date: 2026-09-02

## Main result

This note solves the root central path of the winner-take-all holonomy SDP
when all \(G\) path parities are even and when exactly one is odd.  Let
\(\tau=\mu P\) be the barrier coefficient after each length-\(P\) path is
eliminated, and scale

\[
                              \alpha=\tau G.                  \tag{1}
\]

With one odd group, there is a sharp condensation threshold

\[
                              \boxed{\alpha_*=\frac2{45}}.    \tag{2}
\]

If \(p_G\) is the trace mass carried by the unique odd, lower-cost group,
then for fixed \(\alpha>0\) and \(G\to\infty\),

\[
 p_G\longrightarrow1-\frac{45}{2}\alpha
          \quad(0<\alpha<\alpha_*),                           \tag{3}
\]

\[
 \sqrt G\,p_G\longrightarrow\frac{\sqrt{33}}9
          \quad(\alpha=\alpha_*),                             \tag{4}
\]

whereas for \(\alpha>\alpha_*\),

\[
 Gp_G\longrightarrow \alpha A(x_\alpha),\qquad
 B(x_\alpha)=\frac1\alpha.                                  \tag{5}
\]

The reduced log-barrier Hessian on the global-trace tangent undergoes a
matching transition:

\[
 \kappa_{\rm red}=\begin{cases}
  \Theta(G),&0<\alpha\le\alpha_*,\\
  \Theta(1),&\alpha>\alpha_*.
 \end{cases}                                                  \tag{6}
\]

In contrast, on the all-even input every group has trace exactly \(1/G\)
and \(\kappa_{\rm red}=\Theta(1)\) for every fixed \(\alpha>0\).

There is also a finite, assumption-light implication: if the unique winner
has trace mass at least any fixed \(p_0>0\), then

\[
                              \boxed{\kappa_{\rm red}=\Omega_{p_0}(G).}    \tag{7}
\]

Thus a central point that already assigns constant probability to the
eventual winning block cannot simultaneously have a uniformly conditioned
Euclidean reduced Hessian.  This mass--conditioning implication is a
trajectory obstruction; the separate state-output consequence below also
has raw-query content.

Both conclusions are robust.  A dimensionless local centrality residual
\(\eta<1\) gives a Loewner sandwich around the resolvent center.  Below the
correspondingly shifted capacity threshold it preserves constant winner mass,
and any approximately central point with constant winner mass still has
Euclidean reduced-Hessian condition number \(\Omega(G)\).  Trace-distance
error in the output state subtracts only that error from winner-sampling
probability.

There is a complementary access theorem.  Measuring a root or physical
central state proposes the winner with probability exactly \(p_G\).  Verified
sampling therefore costs \(O(1/p_G)\) state preparations, while coherent
amplitude amplification costs \(O(1/\sqrt{p_G})\) preparation-unitary calls.
However, at \(\tau\le1/(90G)\), where \(p_G\ge3/4\) and the duality gap is at
most \(1/30\), preparing a central state to any fixed trace error below
\(1/32\) already requires \(\Omega(N\sqrt G)\) raw queries.  Trace error
\(1/20\) has the same lower bound at \(\tau\le1/(135G)\).  Thus continuation
run only to identify the active component cannot beat direct
\(O(N\sqrt G)\) search-then-crossover.

There is also a direct state-output consequence.  Two independent samples
from the public group register have a constant collision-probability gap
between the all-even and exactly-one-odd promises once the winner mass is
constant.  Therefore preparing the root or physical primal central density
state costs
\[
                              \boxed{\Omega(N\sqrt G)}       \tag{7a}
\]
raw or canonical coefficient queries in the condensed regime for \(G\ge2\).
For example,
\(\tau\le1/(90G)\) permits every fixed trace error below \(1/32\), while
the slightly later schedule \(\tau\le1/(135G)\) permits trace error
\(1/20\).  This decoder needs no \(N\)-query verification of a sampled
candidate.

## 1. Root barrier problem

The path construction and sparse global-trace accumulator are given in
`2026-09-02-winner-take-all-global-trace-holonomy-sdp.md`.  After eliminating
the public accumulators and the signed copy paths, its root barrier problem is

\[
 \begin{aligned}
 \text{minimize}\quad&
  \sum_{g=1}^G\langle\overline C_{h_g},Z_g\rangle
  -\tau\sum_{g=1}^G\log\det Z_g,\\
 \text{subject to}\quad&Z_g\succ0,\qquad
                     \sum_g\operatorname{tr}Z_g=1,
 \end{aligned}                                                \tag{8}
\]

where

\[
 \operatorname{spec}(\overline C_+)=\{16/5,29/10,29/10\},
 \qquad
 \operatorname{spec}(\overline C_-)=\{31/10,31/10,14/5\}.   \tag{9}
\]

The parameter is \(\tau=\mu P\), not \(\mu\), because every root matrix is
copied to \(P\) physical PSD blocks.

Let \(\lambda\) be the multiplier for the total trace under the sign
convention

\[
                  \overline C_{h_g}-\lambda I-\tau Z_g^{-1}=0.
\]

The unique central point is

\[
                  \boxed{Z_g(\tau)=
                  \tau(\overline C_{h_g}-\lambda I)^{-1}},   \tag{10}
\]

where \(\lambda<\min_g\lambda_{\min}(\overline C_{h_g})\) is the unique
solution of

\[
                  \tau\sum_g\operatorname{tr}
                  (\overline C_{h_g}-\lambda I)^{-1}=1.       \tag{11}
\]

Existence and uniqueness follow because the left side is continuous and
strictly increasing in \(\lambda\), tends to zero as
\(\lambda\to-\infty\), and diverges at the smallest cost eigenvalue.

## 2. All-even central path

If every \(h_g=+1\), symmetry and uniqueness give equal blocks and

\[
                              \operatorname{tr}Z_g=\frac1G    \tag{12}
\]

exactly, for every \(G\) and \(\tau\).  Put

\[
                              y=\frac{29}{10}-\lambda>0.
\]

Equation (11) becomes

\[
 1=\tau G\left(\frac2y+\frac1{y+3/10}\right).                \tag{13}
\]

For \(\alpha=\tau G\), its positive solution is

\[
 y_\alpha=\frac{3\alpha-3/10+
  \sqrt{(3/10-3\alpha)^2+(12/5)\alpha}}{2}.                  \tag{14}
\]

Thus (10), together with the eigenspaces of \(\overline C_+\), is an exact
closed form for every all-even central block.

## 3. Exactly one odd group

Assume group one is odd and the other \(G-1\) groups are even.  Put

\[
                              x=\frac{14}{5}-\lambda>0        \tag{15}
\]

and define

\[
 A(x)=\frac1x+\frac2{x+3/10},\qquad
 B(x)=\frac1{x+2/5}+\frac2{x+1/10}.                          \tag{16}
\]

The odd cost gaps above \(\lambda\) are
\(x,x+3/10,x+3/10\).  Each even cost has gaps
\(x+1/10,x+1/10,x+2/5\).  Hence the exact scalar central-path equation is

\[
                  \boxed{1=\tau\{A(x)+(G-1)B(x)\}.}           \tag{17}
\]

It has a unique positive solution.  The winner and total-loser trace masses
are exactly

\[
                  \boxed{p_G=\operatorname{tr}Z_1=\tau A(x),
                  \qquad 1-p_G=\tau(G-1)B(x).}               \tag{18}
\]

Equations (10), (15)--(18) are the exact central path.  No asymptotic
approximation is used in these formulas.

Two finite-\(G\) bounds are useful below.  Since \(B\) is decreasing and
\(B(0)=45/2\),
\[
                 \boxed{p_G\ge
                 1-\frac{45}{2}\tau(G-1).}                  \tag{18a}
\]
Also \(A(x)\le3/x\) and \(B(x)\ge3/(x+2/5)\).  Thus, whenever
\(p_G\ge p_0>0\),
\[
 x\le\frac{3\tau}{p_0},\qquad
 1-p_G\ge
 \frac{3\tau(G-1)}{\,2/5+3\tau/p_0\,}.                     \tag{18b}
\]
In particular, for \(G\ge2\) and \(0<\varepsilon<1\),
\[
 \tau\le\frac{2\varepsilon}{45(G-1)}
       \quad\Longrightarrow\quad p_G\ge1-\varepsilon,       \tag{18c}
\]
while, when \(G-1-\varepsilon/(1-\varepsilon)>0\),
\[
 p_G\ge1-\varepsilon
       \quad\Longrightarrow\quad
 \tau\le
 \frac{2\varepsilon}
 {15\{G-1-\varepsilon/(1-\varepsilon)\}}.                  \tag{18d}
\]
These constants are not asymptotically tight against each other, but they
give a completely nonasymptotic proof that constant winner concentration
requires \(\tau=O(1/G)\), while the transition itself occurs on the
\(\Theta(1/G)\) scale.

For fixed \(G\), direct expansion of (17) at \(\tau=0\) gives
\[
 x=\tau+\frac{135G-95}{6}\tau^2+O_G(\tau^3),\qquad
 p_G=1-\frac{45}{2}(G-1)\tau
        +\frac{825}{4}(G-1)\tau^2+O_G(\tau^3).              \tag{18e}
\]

## 4. Condensation transition

The loser resolvent density at the winning edge is

\[
 B(0)=\frac1{2/5}+\frac2{1/10}=\frac{45}{2}.                 \tag{19}
\]

This gives the critical scaled barrier \(\alpha_*=1/B(0)=2/45\).

### 4.1 Subcritical regime

Fix \(0<\alpha<2/45\) and put \(\tau=\alpha/G\).  Equation (17) forces
\(x\to0\); otherwise its winner term vanishes and its loser term tends to at
most \(\alpha B(0)<1\).  Since

\[
 A(x)=\frac1x+O(1),\qquad B(x)=B(0)+O(x),
\]

(17)--(18) give

\[
 p_G\to1-\alpha B(0)=1-\frac{45}{2}\alpha,qquad
 \frac{x}{\tau}\to\frac1{1-(45/2)\alpha}.                   \tag{20}
\]

This proves (3).  A constant fraction of the total trace has condensed onto
the unique future optimizer even though the barrier is still positive.

### 4.2 Supercritical regime

Fix \(\alpha>2/45\).  Since \(B\) decreases continuously from \(45/2\) to
zero, there is a unique \(x_\alpha>0\) satisfying

\[
                              B(x_\alpha)=\frac1\alpha.       \tag{21}
\]

Equation (17) gives \(x\to x_\alpha\), and (18) yields

\[
                              Gp_G\to\alpha A(x_\alpha).      \tag{22}
\]

Thus the winner has only the same \(\Theta(1/G)\) trace scale as an ordinary
group.

### 4.3 Critical regime

At \(\alpha=2/45\), write

\[
 \beta=-B'(0)=\frac1{(2/5)^2}+\frac2{(1/10)^2}
              =\frac{825}{4}.                               \tag{23}
\]

Expanding (17) at zero gives the leading balance

\[
                              \frac{\tau}{x}\sim\alpha_*\beta x.
\]

Since \(\tau=\alpha_*/G\),

\[
 \sqrt G\,x\longrightarrow\frac1{\sqrt\beta}
          =\frac2{\sqrt{825}},\qquad
 \sqrt G\,p_G\longrightarrow\alpha_*\sqrt\beta
          =\frac{\sqrt{33}}9.                               \tag{24}
\]

This proves (4) and identifies the critical exponent \(1/2\).

## 5. Exact reduced Hessian

Define

\[
                              D_g=\overline C_{h_g}-\lambda I.
\]

At (10), the root log-barrier Hessian is the block-diagonal operator

\[
                  \boxed{\mathcal H_\tau[Y]_g
                         =\frac1\tau D_gY_gD_g}               \tag{25}
\]

on the global-trace tangent

\[
                  \mathcal T=\{Y=(Y_1,\ldots,Y_G):
                                  \sum_g\operatorname{tr}Y_g=0\}.         \tag{26}
\]

The condition number below is the Euclidean Frobenius condition number of
the quadratic form (25) restricted to \(\mathcal T\).  Public accumulator
variables have already been eliminated.  No condition claim is made for the
ambient singular free-variable Hessian or the full saddle KKT matrix.

### 5.1 All-even conditioning

On an all-even input the eigenvalues of every \(D_g\) are
\(y_\alpha,y_\alpha,y_\alpha+3/10\).  For \(G\ge2\), both ambient extreme
curvatures are attained on \(\mathcal T\): use an off-diagonal direction in
the two-dimensional minimum eigenspace for the lower extreme, and opposite
rank-one maximum-eigenvector directions in two groups for the upper extreme.
Therefore

\[
                  \boxed{\kappa_{\rm even}
                  =\left(\frac{y_\alpha+3/10}{y_\alpha}\right)^2}         \tag{27}
\]

for \(G\ge2\).  It is independent of \(G\) at fixed \(\alpha>0\).

### 5.2 One-odd conditioning transition

For one odd group, the Hessian weights in simultaneous eigen-coordinates are
pairwise products of

\[
 \{x,x+3/10,x+3/10\}\quad\text{in the winner},
\]

and

\[
 \{x+1/10,x+1/10,x+2/5\}\quad\text{in every loser},          \tag{28}
\]

all divided by \(\tau\).

For \(G\ge2\), the restriction to the trace tangent can be bounded sharply
at finite \(G\).
Put
\[
 b=x+\frac1{10},\qquad c=x+\frac3{10},\qquad e=x+\frac25.
\]
Diagonal and off-diagonal symmetric coordinates are orthogonal invariant
subspaces of the Hessian.  On the off-diagonal subspace the smallest weight is
exactly \(\min\{xc,b^2\}/\tau\).  For the diagonal subspace, write the soft
winner coordinate as \(a\) and the remaining \(3G-1\) coordinates as \(z\).
The tangent constraint gives \({\bf1}^Tz=-a\), hence
\(\|z\|_2^2\ge a^2/(3G-1)\).  All entries of \(z\) have weights between
\(b^2\) and \(e^2\).  Conversely, one may cancel \(a\) equally over the
\(2(G-1)\) minimum-eigenvalue coordinates of the losers.  Therefore the
smallest diagonal eigenvalue \(\lambda_{\rm diag}\) obeys
\[
 \frac1\tau\frac{(3G-1)x^2+b^2}{3G}
 \le\lambda_{\rm diag}\le
 \frac1\tau\frac{2(G-1)x^2+b^2}{2(G-1)+1}.                 \tag{28a}
\]
For \(G\ge2\), these bounds and the off-diagonal weights give the uniform
two-sided laws
\[
 \lambda_{\min}(\mathcal H_\tau|_{\mathcal T})
 \asymp \frac1\tau\min\left\{x\left(x+\frac3{10}\right),
                    x^2+\frac{(x+1/10)^2}{G}\right\},       \tag{28b}
\]
\[
 \lambda_{\max}(\mathcal H_\tau|_{\mathcal T})
 \asymp\frac{(x+2/5)^2}{\tau}.                              \tag{28c}
\]
The constants are absolute.  For (28c), the upper bound is the largest ambient
weight, while a trace-zero direction inside the repeated stiff winner
eigenspace has weight \(c^2/\tau\), and \(c/e\ge3/4\).  Consequently
\[
 \boxed{
 \kappa_{\rm red}\asymp
 \frac{(x+2/5)^2}{
   \min\{x(x+3/10),\ x^2+(x+1/10)^2/G\}}.}                  \tag{28d}
\]
This finite formula also identifies which tangent mode controls each regime;
it avoids treating the infeasible soft diagonal coordinate as an eigenvector.
It also gives an assumption-light coarse phase law in the original parameters.
If \(\tau G/(1/10)\to0\), equation (17) gives \(x/\tau\to1\), and (28d)
gives
\[
                         \kappa_{\rm red}=\Theta((1/10)/\tau).
\tag{28e}
\]
If \(\tau G/(1/10)\to\infty\), the elementary resolvent bounds
\[
 {3G\over x+2/5}\le A(x)+(G-1)B(x)\le{3G\over x}
\]
give \(x=\Theta(\tau G)\), and (28d) gives
\(\kappa_{\rm red}=\Theta(1)\).  The fixed-scale critical window
\(\tau=\alpha/G\) is resolved more sharply below.

Fix \(0<\alpha<2/45\).  Then \(x=\Theta(1/G)\) and
\(\tau=\Theta(1/G)\).  Every loser curvature and every winner curvature not
involving the soft eigendirection is \(\Theta(G)\), while a winner
soft--stiff off-diagonal curvature is \(\Theta(1)\).  The winner soft
diagonal alone has curvature \(\Theta(1/G)\), but it is not in
\(\mathcal T\).  If its diagonal coefficient is \(a\), the other diagonal
coefficients sum to \(-a\).  Their weights are at least \(cG\), and
Cauchy--Schwarz gives

\[
 cG\sum_{j\ne\mathrm{soft}}z_j^2
 \ge \frac{cG}{3G-1}a^2=\Omega(a^2).                         \tag{29}
\]

Thus the restricted smallest eigenvalue is \(\Theta(1)\), while the largest
is \(\Theta(G)\).  At \(\alpha=2/45\), one has
\(x=\Theta(G^{-1/2})\).  The soft diagonal curvature is then already
\(\Theta(1)\), all other curvatures are at least this large, and a feasible
soft-diagonal direction balanced across the losers has \(O(1)\) Rayleigh
quotient.  The maximum remains \(\Theta(G)\).  Hence

\[
                  \boxed{\kappa_{\rm one\ odd}=\Theta(G)
                  \quad(0<\alpha\le2/45).}                   \tag{30}
\]

For fixed \(\alpha>2/45\), (21) gives \(x\to x_\alpha>0\).  Every curvature
in (28) is then \(\Theta(G)\), with ratios bounded by constants depending
only on \(\alpha\).  Restriction to \(\mathcal T\) preserves these upper and
lower bounds, so

\[
                  \boxed{\kappa_{\rm one\ odd}=\Theta(1)
                  \quad(\alpha>2/45).}                        \tag{31}
\]

This proves (6).

## 6. Constant winner mass forces linear conditioning

The asymptotic phase theorem has a useful finite converse.

> **Theorem (mass--conditioning obstruction).**  Fix \(0<p_0\le1\).  For all
> sufficiently large \(G\), if the exactly-one-odd center has
> \(p_G\ge p_0\), then its reduced Hessian on \(\mathcal T\) satisfies
> \(\kappa_{\rm red}\ge c(p_0)G\).

**Proof.**  From (16), \(A(x)\le3/x\).  Therefore

\[
 p_0\le p_G=\tau A(x)\le\frac{3\tau}{x},
 \qquad x\le\frac{3\tau}{p_0}.                              \tag{32}
\]

Also \(B(x)\ge3/(x+2/5)\).  Equation (17) gives

\[
 1\ge\tau(G-1)B(x)
 \ge\frac{3\tau(G-1)}{x+2/5}.
\]

Using (32),

\[
                  \tau\le
                  \frac{2/5}{3(G-1-1/p_0)}=O_{p_0}(1/G).     \tag{33}
\]

In any even loser, an off-diagonal direction inside its two-dimensional
minimum eigenspace is trace zero and has curvature

\[
                              \frac{(x+1/10)^2}{\tau}
                              \ge\frac1{100\tau}=\Omega_{p_0}(G).         \tag{34}
\]

Hence the restricted maximum eigenvalue has this lower bound.  In the odd
winner, a soft--stiff off-diagonal direction is trace zero and has curvature

\[
 \frac{x(x+3/10)}\tau
 \le\frac3{p_0}\left(\frac{3\tau}{p_0}+\frac3{10}\right)
 =O_{p_0}(1).                                                 \tag{35}
\]

Thus the restricted minimum eigenvalue is at most a constant depending only
on \(p_0\).  Dividing (34) by (35) proves (7).  For example, if
\(G\ge2+2/p_0\), then (33) gives
\(\tau\le4/(15G)\).  Equations (34)--(35) consequently give the fully
explicit bound
\[
             \boxed{\kappa_{\rm red}\ge
             \frac{p_0^2}{8(8+3p_0)}\,G.}                  \tag{35a}
\]
\(\square\)

The theorem says only that constant winner mass forces poor Euclidean
conditioning.  It does not rule out input-dependent preconditioning; the raw
cost of constructing and applying such a preconditioner is a separate access
question.

### 6.1 Robust approximate centrality

The mass and conditioning obstruction survives approximate centrality when
the residual is measured in the local barrier norm.  Let
\(\widetilde Z_g\succ0\), let \(\widetilde\lambda<14/5\), and put

\[
 D_g=\overline C_{h_g}-\widetilde\lambda I,qquad
 E_g={1\over\tau}\widetilde Z_g^{1/2}D_g
                 \widetilde Z_g^{1/2}-I.                    \tag{AC1}
\]

Assume

\[
 \max_g\|E_g\|_{\rm op}\le\eta<1,qquad
 \left|\sum_g\operatorname{tr}\widetilde Z_g-1\right|
 \le\zeta<1.                                               \tag{AC2}
\]

This dimensionless residual gives the exact Loewner sandwich

\[
 (1-\eta)\tau D_g^{-1}\preceq\widetilde Z_g
 \preceq(1+\eta)\tau D_g^{-1}.                            \tag{AC3}
\]

Indeed, \(I+E_g\) lies between \((1-\eta)I\) and
\((1+\eta)I\); congruence by \(\widetilde Z_g^{-1/2}\) and inversion give
(AC3).  If \(\widetilde T=\sum_g\operatorname{tr}\widetilde Z_g\), then

\[
 {\widetilde T\over(1+\eta)\tau}
 \le\sum_g\operatorname{tr}D_g^{-1}
 \le {\widetilde T\over(1-\eta)\tau}.                     \tag{AC4}
\]

Assume there is exactly one odd group and write
\(\widetilde x=14/5-\widetilde\lambda>0\).  Since
\(B(\widetilde x)\le B(0)=45/2\), the total even-group trace obeys

\[
 \sum_{g>1}\operatorname{tr}\widetilde Z_g
 \le(1+\eta)\tau(G-1)B(\widetilde x)
 \le(1+\eta){45\over2}\alpha.                            \tag{AC5}
\]

Consequently the winner probability in the trace-normalized root or physical
central state satisfies

\[
 \boxed{
 \widetilde p_G:={\operatorname{tr}\widetilde Z_1\over\widetilde T}
 \ge1-{(1+\eta)(45/2)\alpha\over1-\zeta}.}                 \tag{AC6}
\]

The physical statement follows because every root is copied through
trace-preserving orthogonal congruences.  If the prepared output state is
within trace distance \(\delta\) of this normalized state, measuring its
group register returns the winner with probability at least
\(\widetilde p_G-\delta\).  For example,

\[
 \eta\le{1\over10},qquad \zeta\le{1\over100},qquad
 \alpha\le{1\over100}                                    \tag{AC7}
\]

give \(\widetilde p_G\ge3/4\), and trace error \(1/100\) still leaves winner
probability at least \(0.74\).

Equation (AC6) quantifies the robust phase boundary.  Constant winner mass
is forced whenever

\[
                         (1+\eta)\alpha B(0)<1-\zeta.       \tag{AC8}
\]

Conversely, exact centers are admissible approximate centers, so every fixed
\(\alpha>2/45\) still admits winner mass \(\Theta(1/G)\).  More precisely,
(AC4) leaves an unavoidable uncertain critical window between

\[
 (1+\eta)\alpha B(0)=1-\zeta
 \quad\hbox{and}\quad
 (1-\eta)\alpha B(0)=1+\zeta.                             \tag{AC9}
\]

Below the first surface loser capacity is insufficient; above the second,
an edge-condensed approximate sequence is impossible.  No sharper universal
threshold follows from only the two-sided residual and trace bounds (AC2).

There is a matching approximate mass--conditioning obstruction.  Fix
\(p_0>0\) and \(\eta<1\), take \(\zeta=0\), and suppose
\(\operatorname{tr}\widetilde Z_1\ge p_0\).  From the upper sandwich and
\(A(x)\le3/x\),

\[
 \widetilde x\le{3(1+\eta)\tau\over p_0}.                 \tag{AC10}
\]

The lower sandwich on the \(G-1\) losers and
\(B(x)\ge3/(x+2/5)\) then imply

\[
 \tau\le {2/5\over
  3\{(1-\eta)(G-1)-(1+\eta)/p_0\}}
 =O_{p_0,\eta}(1/G)                                      \tag{AC11}
\]

for sufficiently large \(G\).  Consider the actual barrier Hessian at the
approximate point,

\[
 \widetilde{\mathcal H}[Y]_g
 =\tau\widetilde Z_g^{-1}Y_g\widetilde Z_g^{-1}.          \tag{AC12}
\]

In a loser, choose any Frobenius-unit off-diagonal direction in an eigenbasis
of \(\widetilde Z_g\).  It is trace zero.  Equation (AC3) gives
\(\lambda_{\max}(\widetilde Z_g)\le
(1+\eta)\tau/(\widetilde x+1/10)\), so its curvature is at least

\[
                         {1\over100(1+\eta)^2\tau}
 =\Omega_{p_0,\eta}(G).                                  \tag{AC13}
\]

In the winner, let \(z_{\max}\ge p_0/3\) be its largest eigenvalue.  Every
other eigenvalue is at least
\((1-\eta)\tau/(\widetilde x+3/10)\) by (AC3).  An
off-diagonal direction between a \(z_{\max}\)-eigenvector and any orthogonal
eigenvector is trace zero and has curvature at most

\[
 {3(\widetilde x+3/10)\over(1-\eta)p_0}
 =O_{p_0,\eta}(1).                                       \tag{AC14}
\]

Combining (AC13)--(AC14) proves

\[
 \boxed{\kappa(\widetilde{\mathcal H}|_{\mathcal T})
                         =\Omega_{p_0,\eta}(G).}            \tag{AC15}
\]

Thus approximate centrality in the local barrier norm preserves both winner
mass and the linear Euclidean-conditioning obstruction.  There is no
contradiction: local scaling makes (AC3) well conditioned by definition,
while the Frobenius-coordinate Hessian records the growing anisotropy needed
to concentrate trace into one group.  A small unscaled stationarity residual
does not imply (AC2) near the boundary, where multiplication by
\(\widetilde Z_g^{1/2}\) is essential.

## 7. Central-state winner extraction

The normalized root central density matrix is already

\[
                         \rho_\tau=\bigoplus_{g=1}^G Z_g(\tau),           \tag{36}
\]

because the global trace is one.  Measuring its component register returns
the unique odd winner with probability exactly \(p_G\).  The same statement
holds for the normalized physical primal density
\[
 \rho_\tau^{\rm phys}={1\over P}
   \bigoplus_{g=1}^G\bigoplus_{i=0}^{P-1}
        R_{g,i}Z_g(\tau)R_{g,i}^T.                         \tag{36a}
\]
It has trace one, and every orthogonal congruence preserves block trace, so
copying does not change the component-label marginal.

Under the promise that a winner exists, one measurement therefore returns a
winner with success \(p_G\).  To **identify** a winning label among several
samples, the raw path signs provide an exact test: for a measured label
\(g\), query its \(N\) signs and accumulate their parity.  Detecting only the
existence of a winner admits the verification-free collision decoder in
Section 7.2.

Suppose one preparation of a state \(\widetilde\rho_\tau\) satisfying

\[
                         D(\widetilde\rho_\tau,\rho_\tau)\le\epsilon<p_G  \tag{37}
\]

costs \(Q_\rho\) raw queries.  Component-label measurement then returns the
winner with probability at least \(p_G-\epsilon\).  Independent preparation,
measurement, and exact verification repeated

\[
 r=\left\lceil {\log(1/\delta)\over p_G-\epsilon}\right\rceil             \tag{38}
\]

times finds the winner with failure at most \(\delta\), up to an inessential
constant adjustment in (38).  It uses

\[
 O\left({Q_\rho+N\over p_G-\epsilon}\log{1\over\delta}\right)            \tag{39}
\]

raw queries.  Verification also handles the all-even case: it never accepts
a false winner, and after the prescribed trials the algorithm returns
`NONE`.

There is a quadratic improvement if the state comes with a coherent
preparation unitary and its inverse.  Assume

\[
 U_\tau|0\rangle=|\Psi_\tau\rangle,
 \qquad \operatorname{Tr}_{\rm env}|\Psi_\tau\rangle
          \langle\Psi_\tau|=\rho_\tau,                                  \tag{40}
\]

at query cost \(Q_U\).  The clean phase marker
\(|g\rangle\mapsto h_g|g\rangle\) costs \(N\) raw sign queries: loop once
over the \(N\) edges with the sign-oracle answer qubit in \(|-\rangle\), so
phase kickback multiplies the amplitude by the product of the signs and
leaves no parity garbage.  Fixed-point amplitude amplification using
\(U_\tau,U_\tau^\dagger\) and this marker finds the winner in

\[
 O\left({Q_U+N\over\sqrt{p_G}}\log{1\over\delta}\right)                  \tag{41}
\]

raw queries.  Standard doubling removes prior knowledge of \(p_G\) at
constant-factor or logarithmic overhead.

Equation (41) requires a coherent implementation guarantee.  Trace-distance
accuracy of the single output state does not control the unitary completion
off \(|0\rangle\), and is insufficient by itself for repeated uses of
\(U_\tau^\dagger\).  The copy bound (39) needs only the state guarantee (37).

### 7.1 Extraction across the condensation transition

For the exactly-one-odd promise, (3)--(5) turn (39)--(41) into the following
asymptotic phase table at fixed \(\alpha=\tau G\):

\[
\begin{array}{c|c|c|c}
\text{regime}&p_G&\text{verified state copies}&
                  \text{coherent amplification calls}\\ \hline
0<\alpha<2/45&\Theta(1)&\Theta(1)&\Theta(1)\\
\alpha=2/45&\Theta(G^{-1/2})&\Theta(G^{1/2})&\Theta(G^{1/4})\\
\alpha>2/45&\Theta(G^{-1})&\Theta(G)&\Theta(G^{1/2}).
\end{array}                                                               \tag{42}
\]

This table counts uses of an already available central-state primitive.  It
does not say that those states can be constructed cheaply from the raw
instance.

### 7.2 First-use preparation lower bound

Restrict the batch promise to either no odd group or exactly one odd group.
Deciding which case holds is the unique-search promise version of
\(\mathrm{OR}_G\circ\mathrm{PARITY}_N\), whose bounded-error quantum query
complexity is \(\Omega(N\sqrt G)\).  The explicit adversary in the companion
note proves this already on the stated promise.

A collision decoder removes the additive \(N\)-query verification cost in
the preceding extraction argument.  Prepare two independent copies of the
central density and measure their public group registers.  On an all-even
input, (12) gives collision probability, for \(G\ge2\),
\[
                              c_0={1\over G}.                              \tag{43}
\]
On a one-odd input it is
\[
 c_1=p_G^2+{(1-p_G)^2\over G-1},
 \qquad
 c_1-c_0={(Gp_G-1)^2\over G(G-1)}.                         \tag{44}
\]
This calculation applies equally to the reduced root density (36) and to
the density normalized over all physical copied blocks, because both have
the same group marginal.

Since \(B(x)\le B(0)=45/2\), equation (18) gives the finite bound
\[
                    1-p_G\le {45\over2}\tau(G-1).           \tag{44a}
\]
Thus \(\tau\le1/(90G)\) implies \(p_G\ge3/4\).  For every
\(G\ge2\), (44) then gives
\[
                              c_1-c_0\ge{1\over8};           \tag{44b}
\]
the worst case is \(G=2,p_G=3/4\).  If each prepared state is within trace
distance \(\epsilon\) of its exact target, the corresponding two-copy
product state is within trace distance at most \(2\epsilon\).  The collision
probability under each promise therefore moves by at most \(2\epsilon\),
and the promise gap remains at least
\[
                              {1\over8}-4\epsilon.           \tag{44c}
\]
Every fixed \(\epsilon<1/32\) leaves a constant gap; at
\(\epsilon=1/100\) the gap is at least \(17/200=0.085\).

The earlier tolerance \(1/20\) is also available after moving only a
constant factor farther down the path.  If \(\tau\le1/(135G)\), then
(44a) gives \(p_G\ge5/6\), so the ideal collision gap is at least \(2/9\).
Trace error \(1/20\) in each state leaves gap at least
\[
                              {2\over9}-{1\over5}={1\over45}.             \tag{44d}
\]

A constant number of independent collision experiments using fresh
preparations now decides the composed promise without any raw-input query
beyond those used by the state preparations.  If one preparation costs
\(Q_\rho\) queries, the adversary
lower bound therefore yields, for either finite schedule and its stated
trace tolerance,
\[
                              \boxed{Q_\rho=\Omega(N\sqrt G)}.            \tag{44e}
\]
This holds for arbitrary mixed outputs, and for purification outputs whose
reduced system states satisfy the stated trace-distance contract: the decoder
reads only the reduced group registers.  It also transfers with no constant loss
to the canonical fixed-position coefficient oracle, whose hidden-input
query normalization is exactly one.

More generally, if \(p_G\ge p_0>0\) and \(G\ge2/p_0\), then (44) implies
\[
                              c_1-c_0\ge {p_0^2\over4}.       \tag{44f}
\]
Thus any fixed trace error \(\epsilon<p_0^2/16\) gives the same
\(\Omega(N\sqrt G)\) preparation lower bound.  In particular, for every
fixed subcritical scale \(\alpha=\tau G<2/45\), equation (3) supplies such
a constant \(p_0\) for all sufficiently large \(G\).  At criticality,
\(p_G=\Theta(G^{-1/2})\), and above it \(p_G=\Theta(G^{-1})\); the collision
gap then vanishes, so this constant-copy reduction deliberately stops at
the condensation transition.

For comparison, composing coherent amplification with the same lower bound
gives the mass--access tradeoff

\[
 {Q_U+N\over\sqrt{p_G}}=\Omega(N\sqrt G),
 \qquad Q_U+N=\Omega(N\sqrt{Gp_G}).                                      \tag{45}
\]

For copy-only state preparation, repetition gives the weaker but
completion-free relation

\[
                         Q_\rho+N=\Omega(p_GN\sqrt G).                    \tag{46}
\]

Thus the apparent improvements in the last two columns of (42) are offset by
state-construction work when the whole algorithm starts from raw
coefficients.  In the constant-mass regime, the collision theorem (44e) is
strictly stronger than the verification-based copy bound (46).  A supplied
central-state oracle or a QRAM containing group parities has already
performed that aggregation and lies outside (44e)--(46).

### 7.3 Matching coherent preparation upper bound on the unique-winner promise

On the promise of exactly one odd group, \(p_G\), \(x\), and the normalized
internal matrices
\[
 \omega_-={Z_-(\tau)\over p_G},\qquad
 \omega_+={Z_+(\tau)\over(1-p_G)/(G-1)}                    \tag{46a}
\]
are public functions of \((G,\tau)\); only the winner label is hidden.
Starting from the uniform group state, exact-parity marking costs \(N\) raw
queries.  Standard amplitude multiplication or fixed-point amplification
changes the marked probability from \(1/G\) to \(p_G\) using
\[
 O(\sqrt{Gp_G}+1)                                          \tag{46b}
\]
marker calls.  Conditional constant-dimensional rotations then purify
\(\omega_-\) on the marked branch and \(\omega_+\) on every unmarked branch.
Their eigenvalues and eigenvectors follow from the public matrices in (9)
and the scalar solution of (17), so these rotations use no raw input query.
Consequently a coherent purification of the root central density has query
upper bound
\[
 \boxed{Q_U=O\!\left(N(\sqrt{Gp_G}+1)\right)}.             \tag{46c}
\]
Together with (45), this is tight up to constants whenever \(Gp_G\to\infty\)
and the preparation error is a sufficiently small fraction of \(p_G\).
It gives \(\Theta(N\sqrt G)\) below the transition,
\(\Theta(NG^{1/4})\) at criticality, and \(O(N)\) above the transition.
The last bound is an upper bound; (45) becomes vacuous up to its additive
\(N\) term when \(Gp_G=\Theta(1)\).

### 7.4 Exact root-state distance visibility threshold

Let \(\rho_0\) be the public all-even root central density at the same
\((G,\tau)\), and let \(\rho_1\) be the root density with one fixed odd
group and winner mass \(p_G\).  Their exact distance satisfies
\[
 \boxed{p_G-{1\over G}\ \le
 D_{\rm tr}(\rho_0,\rho_1)\ \le p_G.}                     \tag{46d}
\]
For the lower bound, measure the group register: its distinguished-group
probability changes from \(1/G\) to \(p_G\).  For the upper bound, first
note that the unique-winner trace multiplier \(\lambda_1\) is smaller than
the all-even multiplier \(\lambda_0\).  This is immediate if
\(\lambda_0\ge14/5\); otherwise, writing \(x=14/5-\lambda_0>0\), direct
algebra gives
\[
 A(x)-B(x)=
 {3/250\over x(x+1/10)(x+3/10)(x+2/5)}>0,                \tag{46e}
\]
so replacing one even resolvent by an odd one increases the trace at fixed
\(\lambda_0\), forcing \(\lambda_1<\lambda_0\).  Hence every losing block
of \(\rho_1\) is Loewner-smaller than the corresponding block of \(\rho_0\).
The winner-block trace-norm difference is at most \(p_G+1/G\), while the
sum of the loser-block trace-norm differences is exactly \(p_G-1/G\).
Dividing their sum by two proves (46d).

Thus the root central density has constant zero-versus-one visibility
precisely in the condensed regime.  At criticality its distance from the
public all-even root state is \(\Theta(G^{-1/2})\), and above the transition
it is \(\Theta(G^{-1})\).  In particular, on the zero-or-one promise, if the
allowed trace error is at least \(p_G\), the zero-query public root output
\(\rho_0\) already satisfies the **reduced-root** state-approximation contract
on both cases.  This last zero-query statement is not automatically true in
the original sparse block coordinates: their copy-path rotations contain raw
prefix signs.  The access lower bounds therefore require error below the
winner-mass scale, outside the condensed regime; the constant-error collision
bound (44c) is accordingly confined to a condensed schedule.

### 7.5 Sparse-coordinate approximation costs

The root-versus-physical distinction admits an exact accounting.  On a raw
input \(\sigma\), lift the public all-even root center using that input's
actual copy-path rotations:

\[
 \widetilde\rho_{0,\sigma}^{\rm phys}
 ={1\over P}\bigoplus_{g,i}R_{g,i}E_0R_{g,i}^T,
 \qquad E_0=\tau(\overline C_+-\lambda_0I)^{-1}.            \tag{46f}
\]

For Hermitian root tuples the map in (46f) preserves trace norm exactly:
orthogonal congruence preserves each block norm, the \(P\) direct-sum copies
add, and the prefactor cancels them.  Hence (46d) also gives

\[
 D_{\rm tr}(\rho_1^{\rm phys},
             \widetilde\rho_{0,\sigma}^{\rm phys})\le p_G, \tag{46g}
\]

while on an all-even input (46f) is the exact physical center.

The reference (46f) has a QRAM-free preparation using exactly \(N\) raw
queries.  Prepare its public root purification and the public uniform block
index.  For \(j=1,\ldots,N\), query \(z_{g,j}\) in phase only when block \(i\)
lies beyond signed edge \(j\) and the matrix-system basis index is \(e_1\).
This applies \(R_{g,i}\) coherently for every \((g,i)\).  The answer qubit stays
in \(|-\rangle\), so there is no prefix garbage and no uncomputation pass.
Therefore, on the zero-or-one promise,

\[
 p_G\le\epsilon
 \quad\Longrightarrow\quad
 Q_\epsilon(\rho_{\rm central}^{\rm phys})\le N,
 \qquad
 Q_\epsilon(\rho_{\rm central}^{\rm root})=0.             \tag{46h}
\]

At criticality the condition holds for
\(G=\Omega(\epsilon^{-2})\); for fixed supercritical \(\alpha\), it holds
for \(G=\Omega_\alpha(\epsilon^{-1})\).  Thus fixed-error root-state
preparation changes from \(\Theta(N\sqrt G)\) below the threshold to zero
queries at and above it.  The physical state changes from
\(\Theta(N\sqrt G)\) to an \(O(N)\) upper bound; no matching
\(\Omega(N)\) claim is made.

For completeness, the condensed-phase upper bound here is for the full
zero-or-one promise, not only the exactly-one promise of Section 7.3: run
exact promised search in \(O(N\sqrt G)\) queries, use its verified `NONE` or
winner outcome to choose the public scalar solution (13) or (17), and then
apply the \(N\)-query prefix lift.  This prepares the exact appropriate
central state and matches (44e).

There is also a genuinely public physical approximation sufficiently far
toward the analytic-center side.  Let \(\omega=I/(3PG)\).  From (13), the
two low-cost eigenvalues of each normalized all-even root block have weight
\(\alpha/y_\alpha\), and the high-cost eigenvalue has weight
\(\alpha/(y_\alpha+3/10)\).  Direct summation gives

\[
 D_{\rm tr}(\rho_0^{\rm phys},\omega)
 =d_{\rm iso}(\alpha)
 :={1\over3}-{\alpha\over y_\alpha+3/10}
 ={1\over45\alpha}+O(\alpha^{-2}).                        \tag{46i}
\]

This distance is independent of the prefix rotations.  The triangle
inequality with (46g) yields

\[
 D_{\rm tr}(\rho_1^{\rm phys},\omega)
 \le d_{\rm iso}(\alpha)+p_G.                             \tag{46j}
\]

Thus \(d_{\rm iso}(\alpha)+p_G\le\epsilon\) is an explicit sufficient
condition for a zero-query physical-state approximation.  For fixed
\(\epsilon\), it holds once \(\alpha\) is a sufficiently large constant and
then \(G\) is sufficiently large.  For a general fixed supercritical
\(\alpha\), the robust statement is the \(N\)-query upper bound (46h), not a
zero-query claim.

## 8. QIPM continuation versus search-then-crossover

The product log-det barrier has parameter \(\nu=3GP\).  A standard short-step
path follower reducing \(\tau\) from a public constant scale to
\(1/(90G)\) takes

\[
                         O(\sqrt{GP}\log G)                               \tag{47}
\]

Newton steps.  This is only an iteration count: it omits coefficient access,
block-encoding, linear solves, state preparation, tomography, and recovery.
Moreover, the subcritical endpoint has constant winner mass but, by (30) and
the finite theorem in Section 6, Euclidean reduced-Hessian condition
\(\Theta(G)\).  Continuation has traded winner concentration for poor
conditioning.

If the central state was independently required and has already been paid
for, (39) or (41) legitimately uses it as a biased proposal distribution for
active-face identification.  If continuation is run only to discover the
winner, direct search is cleaner and asymptotically optimal.  The clean
parity marker followed by Grover search finds the odd group in

\[
                              O(N\sqrt G)                                 \tag{48}
\]

raw queries without traversing the global path.  Afterward, restrict to the
winning component and return its explicit root optimizer or run a local
component solver.  Recovering that component's original path coordinates
costs another \(O(N)\) queries.  The end-to-end architecture is

\[
 O(N\sqrt G)+T_{\rm component\ solve}+O(N)_{\rm recovery}.               \tag{49}
\]

This is best described as **search-then-crossover**, not as a faster QIPM
iteration.  The quantum gain is Grover search over components.  Central-state
sampling is valuable only as a marginal use of a state produced for another
purpose; the first-use lower bound (44e) prevents it from yielding a better
raw-query complexity on this family.

## 9. Interpretation and novelty calibration

The transition is the finite-dimensional log-det analogue of a condensation
phenomenon.  The \(G-1\) losing blocks have a finite total resolvent density
\(B(0)=45/2\) at the winner's spectral edge.  They can absorb all trace when
\(\tau G>1/B(0)\).  Below that value, their capacity is insufficient and the
remaining trace condenses into the winner's soft eigenmode.  At exact
capacity, the pole \(1/x\) balances the linear loss in \(B(x)\), producing
the square-root critical law.

Resolvent formulas for log-det central paths and secular equations are
classical.  For example, the semidefinite log-barrier central path and its
stationarity equations are reviewed in Section 11.6 of Boyd and Vandenberghe,
[*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf).
The product-cone barrier in (8) is just the sum of the block log-determinants;
neither that additivity nor (10)--(11) is a new barrier construction.  The
inverse-gap weights here are the log-barrier, or Burg, analogue of a soft
minimum.  They are not log-sum-exp weights: entropy regularization would give
exponential rather than resolvent weights.  Log-determinant regularization of
PSD matrices also predates this construction; see Moridomi, Hatano, and
Takimoto,
[*Online linear optimization with the log-determinant regularizer*](https://arxiv.org/abs/1710.10002).

Classical central-path asymptotics already cover each fixed instance.  Halicka,
[*Analyticity of the central path at the boundary point in semidefinite
programming*](https://optimization-online.org/2001/04/318/), proves analytic
extension to the boundary under strict complementarity, with finite
derivatives.  Chua,
[*Analyticity of weighted central path and error bound for semidefinite
programming*](https://optimization-online.org/2005/07/1168/), gives a related
weighted-path result over homogeneous cones.  These results explain ordinary
fixed-\(G\) first-order convergence to a strictly complementary optimum, but
they do not state the simultaneous \(G\to\infty\),
\(\tau=\alpha/G\) capacity law (19)--(24).  Accordingly, the word
``transition'' in this note means a large-\(G\) limit: for every finite
\(G\), the positive-barrier center is the unique analytic solution of (17),
not a finite-dimensional nonanalytic phase transition.

Nor is Hessian ill-conditioning near a low-rank SDP optimum new by itself.
Zhang and Lavaei,
[*Modified Interior-Point Method for Large-and-Sparse Low-Rank Semidefinite
Programs*](https://arxiv.org/abs/1703.10973), explicitly analyze the
low-rank perturbation responsible for an ill-conditioned SDP Newton Hessian
and construct a preconditioner.  General SDP central-path convergence and
possible failure of analytic-center convergence without strict
complementarity were studied by de Klerk, Halicka, and Roos,
[*On the convergence of the central path in semidefinite
optimization*](https://optimization-online.org/2001/06/353/).  Thus the
candidate new conditioning statement is only the exact family-specific
frontier (28d)--(31), and especially the finite implication (32)--(35) from
constant winner mass to \(\Omega(G)\) reduced Euclidean conditioning.  It is
not a general discovery that SDP Newton systems can become ill-conditioned.

On the quantum side, Augustino, Nannicini, Terlaky, and Zuluaga,
[*Quantum Interior Point Methods for Semidefinite
Optimization*](https://arxiv.org/abs/2112.06025), and Huang et al.,
[*A Faster Quantum Algorithm for Semidefinite Programming via Robust IPM
Framework*](https://arxiv.org/abs/2207.11154), give condition-dependent quantum
SDP interior-point upper bounds.  Neither source gives this block-resolvent
capacity threshold, a central-density-state output transition, or a raw
coefficient-query lower bound derived from it.  Generic quantum state-output
problems fall under Lee et al.,
[*Quantum query complexity of state conversion*](https://arxiv.org/abs/1011.3020),
but that framework does not supply the optimization-specific mass estimates
or access reduction.

There are already optimization-native quantum query lower bounds.  Van
Apeldoorn, Gilyén, Gribling, and de Wolf,
[*Quantum SDP-Solvers: Better upper and lower
bounds*](https://arxiv.org/abs/1705.01843), embed composed Boolean functions
into LP/SDP value estimation, and Apers and Gribling,
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215v3), Theorem 8.4, give
sparsity-aware coefficient-query lower bounds for LP value estimation.
Those results prevent any claim that Boolean composition or an
optimization-value query lower bound is new here.  They do not analyze the
trace-normalized primal central density, its resolvent mass transition, or
the two-copy central-state decoder (43)--(44e).

The query primitives used after the state is available are also established
ones.  Boyer, Brassard, Høyer, and Tapp,
[*Tight bounds on quantum searching*](https://arxiv.org/abs/quant-ph/9605034),
give search with an unknown number of marked items, and Yoder, Low, and Chuang,
[*Fixed-point quantum search with an optimal number of
queries*](https://arxiv.org/abs/1409.3305), give fixed-point amplification.
The \(\Omega(N\sqrt G)\) exponent in (44e) is the standard
\(\mathrm{OR}_G\circ\mathrm{PARITY}_N\) lower bound already proved in the
companion note, not a new adversary or composition theorem.  Equations
(43)--(44d) contribute an optimization-specific reduction: two central-state
copies expose the changed component-mass profile through a collision
measurement without separately verifying a parity.  The reduction is
elementary once the exact mass formulas are known, so novelty should be
claimed for its conjunction with this central path, not for collision testing
or amplitude amplification by themselves.  Likewise, the search-then-crossover
step in Section 8 is an architectural conclusion for this family, not a new
minimum-finding primitive.

The candidate new result is therefore the exact use of the classical
resolvent calculation in this sparse QIPM holonomy family, together with the
sharp winner-mass and reduced-conditioning large-\(G\) laws and the finite
mass--conditioning theorem, plus the central-density first-use reduction
(43)--(44e).  A targeted open-primary-source search through September 2, 2026
found no prior theorem with this conjunction.  This is
evidence against an obvious exact collision, not proof of priority.  The
claim of novelty is calibrated to the construction and uniform phase law, not
to log-det resolvents, strict-complementarity asymptotics, condensation
terminology, generic SDP ill-conditioning, OR-of-parities query complexity, or
standard amplification individually.

All conditioning statements use the natural Frobenius root coordinate after
the public copy and accumulator constraints are eliminated.  The complete
unreduced saddle matrix can be ill-conditioned, and the free accumulator
variables have no barrier Hessian.  The exactly-one-odd analysis is a promise
slice; multiple winners change the scalar equation and the critical capacity
proportionally.  That extension is straightforward but is not claimed here.
