# An exact global-central Newton step on the linear-volume parity LP

Date: 2026-09-02

## Result

A public reweighting of the objective in the linear-volume plateau-gain LP
makes one standard infeasible-start Newton correction land at a **genuine
global central point with one common complementarity parameter**.  The start
is public, strictly positive, and has exactly constant coordinatewise
complementarity.  Preparing the exact normalized primal Newton direction to
constant trace error still requires

\[
                 \Omega(N)=\Omega(P)
\]

raw sparse-coefficient queries, where the LP has \(P=17N+1\) nodes and
\(4P\) variables.  All constraint coefficients remain in
\(\{0,\pm1,\pm2\}\), and the only new input numbers are public
\(O(\log N)\)-bit objective coefficients.

This removes the local-\(\mu_i\) prefix caveat from
`2026-09-02-plateau-gain-newton-initialization.md`.  The price is a public
set of only \(O(\log N)\) small-scale curvature outliers: the entire
\(\Theta(N)\)-dimensional plateau block of the reduced Hessian is exactly a
scalar identity, while the un-deflated global reduced condition number is
\(\Theta(N)\).

## 1. Feasible set and public objective weights

Use exactly the constraints and notation of
`2026-09-02-linear-size-robust-gain-parity-lp.md`.  At node \(i\),

\[
 H_i=2^{\min\{i,T\}},\qquad
 T=\left\lceil\tfrac12\log_2N\right\rceil,
 \qquad H=2^T,
\]

and feasibility fixes

\[
 d_i=u_i-v_i=H_i\tau_i,\qquad h_i=H_i,
 \qquad q_i+t_i=2H_i,
\tag{1}
\]

where \(q_i=u_i+v_i\) and \(\tau_i\) is the appropriate prefix parity.
There are \(K=16N\) output-copy nodes, all with \(H_i=H\) and
\(\tau_i=\tau_N\).

Change only the objective at node \(i\) to

\[
 (1+w_i)u_i+(1+w_i)v_i+h_i+t_i,
 \qquad w_i=\frac7{36H_i}.
\tag{2}
\]

On the feasible line this is \(w_iq_i+3H_i\).  Hence the unique optimum is
still \(q_i=H_i\), and all primal regularity properties of the original
construction are unchanged.  The reduced cost of the zero member of the
signed pair is \(2w_i>0\), so strict complementarity and dual
nondegeneracy also remain valid for every fixed \(N\).  The relevant positive
reduced-cost margin is not uniform in the family: \(2w_i=\Theta(N^{-1/2})\)
on the plateau.  It is the smallest added weight/reduced cost, not the
smallest objective coefficient (the objective coefficients are at least one).
All of these rational coefficients have \(O(\log N)\)-bit exact
representations.
More explicitly, “nondegenerate” here uses the standard-form/simplex
terminology: the \(3P\) positive optimal variables form a nonsingular
\(3P\times3P\) column basis (primal nondegeneracy), and each of the remaining
\(P\) nonbasic variables has strictly positive reduced cost (dual
nondegeneracy).  These support and reduced-cost statements should be used if a
source adopts a different conic nondegeneracy convention.

### Why changing the objective is substantive

For the original unweighted objective, no different public
complementarity-centered start
can make one Newton step land at its exact common-\(\mu\) central point on
two distinct gain scales (once both pair orientations are possible).
Here is a short obstruction.

At height \(G\), write \(z=rG\).  The unweighted central stationarity
condition is
\[
 F(r):=\frac1{2+r}+\frac1r-\frac1{1-r}=\frac G\mu.
\]
On the central interval, \(F'(r)<0\).  Define the scale-free pair ratio
\[
 k(r)=\frac{(L+S)^2}{LS}
     =\frac{4(1+r)^2}{r(2+r)}.
\]
Writing \(y=1+r\) gives \(k=4y^2/(y^2-1)\), so \(k'(r)<0\).
Consequently, for fixed common \(\mu\), two heights \(G_1<G_2\) have
\(r_{G_1}>r_{G_2}\) and hence \(k(r_{G_1})<k(r_{G_2})\).

Now let a public start have exact coordinatewise complementarity
\(x_j^0s_j^0=\mu_0\).  If a
signed pair starts at positive values \((a,b)\), its starting slacks are
\((\mu_0/a,\mu_0/b)\).  Because the hidden sign can swap \(L\) and \(S\),
the Newton secant for the first coordinate must be the same with endpoint
\(L\) or endpoint \(S\).  Their difference forces
\[
 a^2=\frac{\mu_0LS}{\mu}.
\]
The second coordinate similarly forces the same equation for \(b\), so
\(a=b\).  The common pair secant is therefore necessarily
\[
 C_G=\sqrt{\mu_0\mu}\,\frac{L+S}{\sqrt{LS}}
    =\sqrt{\mu_0\mu\,k(r_G)}.
\]
It is strictly different at distinct heights.  A standard Newton centering
equation has only one coordinate-independent secant
\(C=\mu_0+\widehat\mu\), proving the obstruction.  A public diagonal change
of variables cannot help because it leaves products and these primal-dual
cross terms invariant.  The inverse-height objective weights in (2)
genuinely alter the central path: they make \(r=1/4\), and hence the secant,
the same at every height.

## 2. A common exact central point

Set

\[
 \mu_1=\frac1{16},\qquad z_i=\frac{H_i}{4}.
\tag{3}
\]

The candidate central primal coordinates, up to the hidden swap of the first
two positions, are

\[
 L_i=\frac{9H_i}{8},\qquad S_i=\frac{H_i}{8},
 \qquad h_i=H_i,qquad t_i=\frac{3H_i}{4}.
\tag{4}
\]

They are strictly positive and feasible.  The only local null direction is
proportional to \((\tfrac12,\tfrac12,0,-1)\).  Its central stationarity
condition is

\[
 \frac{w_i}{\mu_1}
 =\frac1{2H_i+z_i}+\frac1{z_i}-\frac1{H_i-z_i}.
\tag{5}
\]

At \(z_i=H_i/4\), the right side is \(28/(9H_i)\), and (2)--(3) make
(5) exact.  Thus, with

\[
 s_j^1=\frac{\mu_1}{x_j^1},
\tag{6}
\]

we have \(W^T(c-s^1)=0\).  Since the displayed local directions form a basis
of \(\ker A\), this says \(c-s^1\in\operatorname{range}A^T\); full row rank
then gives a unique \(y^1\) satisfying \(A^Ty^1+s^1=c\).  Therefore
\((x^1,y^1,s^1)\) is the genuine global
\(\mu_1\)-central point, not merely a point that is central on the plateau.
In particular its average duality parameter is
\((x^1)^Ts^1/(4P)=\mu_1\), and its complementarity residual is zero.  It
therefore belongs to every standard \(N_2(\theta)\) and
\(N_\infty(\theta)\) central neighborhood, for every \(\theta\ge0\).

The scale-free secant ratio is

\[
 R:=\frac{\mu_1(L_i+S_i)^2}{L_iS_i}
   =\frac{25}{36}
\tag{7}
\]

at every node.  This is the reason for the inverse-height objective weights.

## 3. A public complementarity-centered infeasible start

Let

\[
 \alpha=\frac32,qquad
 \mu_0=\frac{R}{\alpha^2}=\frac{25}{81},
 \qquad C=\frac{R}{\alpha}=\frac{25}{54},
 \qquad \widehat\mu=C-\mu_0=\frac{25}{162}=\frac{\mu_0}{2}.
\tag{8}
\]

Initialize, at every node,

\[
 u_i^0=v_i^0=\frac{5H_i}{6},
 \qquad s_{u,i}^0=s_{v,i}^0=\frac{10}{27H_i},
\tag{9}
\]

and

\[
 h_i^0=\frac{20H_i}{27},\quad s_{h,i}^0=\frac5{12H_i},
 \qquad
 t_i^0=\frac{5H_i}{9},\quad s_{t,i}^0=\frac5{9H_i}.
\tag{10}
\]

Take \(y^0=0\).  This start is completely independent of the hidden signs,
strictly positive, and satisfies

\[
                  x_j^0s_j^0=\mu_0
\tag{11}
\]

for every coordinate.  This is exact *coordinatewise complementarity
centering*, not a central point: primal and dual feasibility both fail.

To fix the residual signs and the meaning of “standard,” the infeasible-start
primal--dual Newton system used here is

\[
\begin{aligned}
 A\Delta x&=b-Ax^0,\\
 A^T\Delta y+\Delta s&=c-A^Ty^0-s^0,\\
 S^0\Delta x+X^0\Delta s
   &=\widehat\mu\mathbf1-X^0s^0 .
\end{aligned}
\tag{11a}
\]

Since \(\mu_0=(x^0)^Ts^0/(4P)\), the choice
\(\widehat\mu=\mu_0/2\) is the usual target \(\sigma\mu_0\) with
\(\sigma=1/2\).

All three right-hand sides in (11a) are public.  In particular,
\(d_i^0=u_i^0-v_i^0=0\), so every hidden transition coefficient multiplies
zero in \(b-Ax^0\); the reference and cap residuals depend only on the public
heights.  Since \(y^0=0\), the dual residual is \(c-s^0\), and (11) fixes the
complementarity residual.  Thus the only hidden input in this Newton system is
the sparse coefficient matrix \(A\), not the supplied start or right-hand side.

### Theorem 1 (one exact Newton correction)

The unique infeasible-start primal-dual Newton correction from
\((x^0,y^0,s^0)\), with centering target \(\widehat\mu=\mu_0/2\), is

\[
 (\Delta x,\Delta y,\Delta s)
 =(x^1-x^0,y^1-y^0,s^1-s^0).
\tag{12}
\]

Consequently a full step lands exactly at the global \(\mu_1=1/16\)
central point.  The endpoint parameter \(\mu_1\) need not equal the
linearized target \(\widehat\mu\): the quadratic term
\(\Delta x_j\Delta s_j\), which (11a) omits, accounts for the difference.
This is a deliberately finite exact Newton step, not a local
quadratic-convergence statement.

#### Proof

Endpoint feasibility supplies the first two Newton equations in (11a).  It
remains to check the linearized complementarity equation.  For either hidden
orientation of the pair, direct substitution gives

\[
 \frac{10}{27H_i}\frac{9H_i}{8}
 +\frac{5H_i}{6}\frac1{18H_i}
 =
 \frac{10}{27H_i}\frac{H_i}{8}
 +\frac{5H_i}{6}\frac1{2H_i}
 =\frac{25}{54}.
\tag{13}
\]

The two remaining coordinates give the same cross term:

\[
 \frac5{12H_i}H_i+\frac{20H_i}{27}\frac1{16H_i}
 =
 \frac5{9H_i}\frac{3H_i}{4}
 +\frac{5H_i}{9}\frac1{12H_i}
 =\frac{25}{54}.
\tag{14}
\]

Thus \(s_j^0x_j^1+x_j^0s_j^1=C\) for every coordinate.  Using (11),

\[
 S^0\Delta x+X^0\Delta s
 =(C-2\mu_0)\mathbf1
 =(\widehat\mu-\mu_0)\mathbf1,
\tag{15}
\]

which is exactly the standard complementarity Newton equation.  Full row
rank and positivity make \(A(S^0)^{-1}X^0A^T\) positive definite, so the
Newton correction is unique. \(\square\)

## 4. Linear query lower bound for the exact direction state

Up to the hidden swap, the four primal direction coordinates at node \(i\)
are

\[
 \left(\frac7{24},-\frac{17}{24},
             \frac7{27},\frac7{36}\right)H_i.
\tag{16}
\]

Their squared norm is

\[
 D H_i^2,\qquad D=\frac{16139}{23328},
\tag{17}
\]

and the larger-minus-smaller squared pair mass is

\[
 \left[\left(\frac{17}{24}\right)^2
       -\left(\frac7{24}\right)^2\right]H_i^2
 =\frac5{12}H_i^2.
\tag{18}
\]

On an output \(u\)-coordinate report \(-1\), on an output \(v\)-coordinate
report \(+1\), and return a fair sign elsewhere.  Since

\[
 \sum_i H_i^2<\left(17N+\frac43\right)H^2,
\tag{19}
\]

the ideal decoder bias is strictly larger than

\[
 \frac{16N(5/12)H^2}
 {2D(17N+4/3)H^2}>\frac14
 \qquad(N\ge2).
\tag{20}
\]

### Theorem 2 (exact global-central direction-state hardness)

Any quantum algorithm whose unconditional output has trace distance at most
\(1/100\) from

\[
                |\Delta x/\|\Delta x\|_2\rangle
\tag{21}
\]

uses \(\Omega(N)=\Omega(P)\) raw sparse LP coefficient queries.  The same
holds for a fixed-probability heralded branch after charging repetition.

Indeed, trace-distance contraction reduces the bias in (20) by at most
\(1/100\).  The resulting measurement computes parity with constant bias.
Every sparse row, column, position, value, or objective query is simulated
with at most one hidden-sign query; objective queries are actually public.
Bounded-error quantum parity needs \(\Omega(N)\) queries.

The theorem charges arbitrary preprocessing, preconditioning, transformed
RHS formation, solving, and recovery whenever their input-dependent
operations are expanded into the raw sparse coefficient oracle.  It does not
claim hardness for a reduced-only output that omits the original-coordinate
loading map.

## 5. Reduced geometry and the exact tradeoff

For the public orthonormal local null vector

\[
 W_i=\sqrt{\frac23}
       \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right),
\tag{22}
\]

the reduced log-barrier Hessian at (4) is diagonal, with eigenvalue

\[
 \lambda_i
 =\frac23\mu_1
   \left(\frac1{4L_i^2}+\frac1{4S_i^2}+\frac1{t_i^2}\right)
 =\frac{182}{243H_i^2}.
\tag{23}
\]

Therefore the whole plateau subspace has **exactly condition one**, and its
dimension is \(17N-O(\log N)\).  All non-plateau eigenvalues are public and
belong to only the \(T=O(\log N)\) gain-prefix modes.  Exact deflation of
those public coordinate modes leaves a scalar reduced solve.  Without that
deflation,

\[
 \kappa(W^T\nabla^2f_{\mu_1}(x^1)W)=H^2=\Theta(N).
\tag{24}
\]

More strongly, the matrix in the actual null-space Newton solve at the public
start is already of the same publicly equilibrated form.  Since
\(s_j^0=\mu_0/x_j^0\), direct substitution of (9)--(10) gives
\[
 W^T(X^0)^{-1}S^0W
 =\frac{22}{27}\operatorname{diag}(H_i^{-2}).
\tag{24a}
\]
Thus the public symmetric scaling \(D_H=\operatorname{diag}(H_i)\) makes the
coefficient matrix of the reduced Newton solve exactly \((22/27)I\).  The
lower bound is therefore not caused by the condition number of that solve;
it survives even if this exact preconditioner and the reduced solve itself are
free.  The hidden work lies in the affine feasible translation and recovery
of the requested original-coordinate direction.

The same exact equilibration holds on the whole central path, not only at
\(\mu_1\).  For any \(\mu>0\), the unique central scalar has
\(z_i=r(\mu)H_i\), where the node-independent
\(r(\mu)\in(0,r_{\rm ac})\) is the unique solution of
\[
 \frac7{36\mu}
 =\frac1{2+r}+\frac1r-\frac1{1-r}.
\]
Here \(r_{\rm ac}=(\sqrt7-1)/3\).
Consequently
\[
 W^T\nabla^2 f_\mu(x(\mu))W
 =\gamma(\mu)\operatorname{diag}(H_i^{-2})
\]
for a public scalar \(\gamma(\mu)>0\), and \(D_H\) makes this matrix exactly
\(\gamma(\mu)I\) at every central parameter.  The raw orthonormal-coordinate
condition number remains \(H^2\); the condition-one statement is for the
explicit public symmetric preconditioner.

Thus exact global centrality and a public complementarity-centered start are
compatible with
linear-volume direction-state hardness.  This particular reweighting does
not also give a globally constant-conditioned *unpreconditioned* reduced
Hessian; it gives a
scalar hard plateau plus only logarithmically many explicit curvature
outliers.  The earlier unweighted construction instead has condition below
\(7/6\) on the entire late central tail but used local prefix parameters in
its exact one-step Newton endpoint.

### 5.1 Exact global equilibration as a standard-form LP

There is a precise way to remove even the public curvature outliers.  It
does not preserve the constant coefficient magnitudes, but it preserves
constant sparsity, exact common-\(\mu\) centrality, and the query lower bound.

Let
\[
 {\cal D}=\operatorname{diag}(H_i I_4)_{i=0}^{P-1}
\]
and make the public diagonal change of standard-form variables
\[
 x={\cal D}\bar x,\qquad
 \bar A=A{\cal D},\qquad \bar c={\cal D}c,
 \qquad \bar s={\cal D}s.
\tag{25}
\]
The transformed LP is
\(\min\{\bar c^T\bar x:\bar A\bar x=b,\bar x\ge0\}\).
This is an ordinary standard-form LP, not a weighted-barrier convention.
Its row and column sparsities are unchanged.  A transition row has current
coefficient \(H_i\) and previous coefficient
\(g_iH_{i-1}=H_i\), while a cap row has coefficients of magnitude at most
\(2H_i\).  Hence
\[
 \|\bar A\|_{\max}\le2H=\Theta(\sqrt N),\qquad
 \|\bar c\|_\infty\le H+7/36.
\tag{26}
\]
Every hidden entry is still only a public magnitude times one hidden sign,
so one transformed sparse-coefficient query is simulated with at most one
sign-oracle query.

The central endpoint and public start become, at every node and up to the
hidden pair swap,
\[
 \bar x^1=(9/8,1/8,1,3/4),\qquad
 \bar x^0=(5/6,5/6,20/27,5/9).
\tag{27}
\]
Their slacks are obtained from (6), (9), and (10) by multiplication by
\(H_i\).  Products and secant cross terms are invariant:
\[
 \bar x_j\bar s_j=x_js_j,\qquad
 \bar s_j^0\bar x_j^1+\bar x_j^0\bar s_j^1
 =s_j^0x_j^1+x_j^0s_j^1.
\tag{28}
\]
Therefore the transformed public start has complementarity \(\mu_0\), and
one standard Newton correction with target \(\widehat\mu\) lands exactly at
the transformed global \(\mu_1\)-central point.  Primal and dual
regularity are preserved by the invertible diagonal transformation.

The vectors (22) are still an orthonormal null basis for \(\bar A\).  All
central primal coordinates in (27) are now node-independent, so (23)
becomes
\[
 W^T\nabla^2 f_{\mu_1}(\bar x^1)W
 =\frac{182}{243}I_P.
\tag{29}
\]
Thus the global reduced Hessian has condition number exactly one.
The preceding formula for \(r(\mu)\) shows more: at every central parameter,
the transformed central coordinates are the same at every node, and the
transformed reduced Hessian is \(\gamma(\mu)I_P\).  Thus this is an
all-central-path condition-one statement, not only an endpoint statement.

This equilibration does not remove output hardness.  The transformed primal
direction is, up to the hidden swap,
\[
 \Delta\bar x_i=(7/24,-17/24,7/27,7/36)
\tag{30}
\]
at every node.  Its squared norm per node is the same constant \(D\) in
(17), and every output-copy node has correct-minus-incorrect pair mass
\(5/12\).  The fixed output-coordinate decoder therefore has bias
\[
 \frac{K(5/12)}{2DP}>\frac14\qquad(N\ge2).
\tag{31}
\]
Consequently, preparing
\(|\Delta\bar x/\|\Delta\bar x\|_2\rangle\) to trace distance \(1/100\)
also needs \(\Omega(N)=\Omega(P)\) transformed coefficient queries.

The robust approximate-update statement also survives this scaling.  If
\(e_i\) is a transformed difference-row residual, then
\[
 \bar d_i-a_i\bar d_{i-1}=e_i/H_i.
\]
The same weighted telescoping estimate used in the robust plateau theorem
gives \(|\bar d_i-\tau_i|<3/40\), and likewise
\(|\bar h_i-1|<3/40\), under the same relative residual threshold.
The transformed cap row gives
\(\bar q_i+\bar t_i-2\bar h_i=e_i^{\rm cap}/H_i\), so nonnegativity bounds
all four transformed coordinates by a constant.  Hence
\(\|\bar x\|_2^2<11P\), while the \(K=16N\) output nodes retain signed pair
mass at least \(K(37/40)^2\).  The original fixed decoder still has bias
greater than \(1/30\).  Thus a state close to any nonnegative transformed
update with residual at most \(\|b\|_2/100\) also costs \(\Omega(P)\)
queries.

Equivalently, on the bounded-coefficient formulation the public symmetric
preconditioner \(\operatorname{diag}(H_i)\) makes the reduced Hessian a
scalar identity.  The theorem shows why this does not contradict the lower
bound: conditioning the one-dimensional-per-node reduced solve does not
load the hidden affine feasible translation into the requested original
coordinates.  As an LP reformulation, exact global equilibration obeys the
explicit tradeoff
\[
 \text{coefficient scale }\Theta(H)=\Theta(\sqrt N),
 \qquad \kappa_{\rm red}=1,
\tag{32}
\]
whereas the bounded-coefficient representation has
\(\kappa_{\rm red}=H^2=\Theta(N)\).  This is a tradeoff for this diagonal
representation family, not a universal lower bound on all formulations.

There is also a continuous interpolation.  For
\({\cal D}_\eta=\operatorname{diag}(H_i^\eta I_4)\),
\(0\le\eta\le1\), the same covariance proof gives
\[
 B_\eta:=\max\{\|A{\cal D}_\eta\|_{\max},
                    \|{\cal D}_\eta c\|_\infty\}
       =\Theta(H^\eta),
 \qquad
 \kappa_\eta=H^{2(1-\eta)}.
\tag{33}
\]
The exact transformed direction at node \(i\) is (16) divided by
\(H_i^\eta\).  The \(K\) output copies still occupy a constant fraction of
its squared norm and retain constant decoding bias, so the \(\Omega(P)\)
query lower bound holds throughout this interpolation.  In particular,
\[
                 B_\eta^2\kappa_\eta=\Theta(H^2)=\Theta(N).
\tag{34}
\]
Equations (33)--(34) are exact asymptotic statements for this natural
diagonal equilibration family.  They should not be presented as an
oracle-independent condition-versus-normalization lower bound.

## 6. Novelty boundary and status

Inverse-height objective weighting is an elementary device, not itself a
novel algorithmic principle.  The claim worth auditing is the conjunction:

> a fixed-pattern, bounded-degree, linear-dimensional standard-form LP for
> which a public infeasible start with exact coordinatewise complementarity has one exact
> standard Newton correction to a genuine common-\(\mu\) central point, yet
> preparing the original-primal direction state to constant error has linear
> raw coefficient-query complexity; after removing only \(O(\log N)\) public
> modes, the reduced central Hessian is scalar.

The targeted audit below checks this exact Newton-direction formulation. The
parity lower bound, clock/plateau amplification, state decoder, and QLS-
hardness motifs all have prior art individually.

### Targeted primary-literature audit (through 2026-09-02)

No exact collision was found for the conjunction above. The nearest results
have different theorem contracts:

- Kerenidis--Prakash ([arXiv:1808.09266](https://arxiv.org/abs/1808.09266)),
  Casares--Martin-Delgado
  ([arXiv:1902.06749](https://arxiv.org/abs/1902.06749)), and Augustino et al.
  ([arXiv:2112.06025](https://arxiv.org/abs/2112.06025)) use a QLSA to prepare
  normalized Newton-direction states and tomography to recover updates. They
  prove upper bounds and convergence guarantees, not a coefficient-query lower
  bound for the direction at a specified iterate.
- Wu--Yang--Terlaky Algorithm 2 starts an infeasible QIPM at the public uniform
  point \((\omega_*\mathbf1,0,\omega_*\mathbf1)\), which already has constant
  coordinatewise complementarity, and their Theorem 1 upper-bounds the cost of
  a preconditioned transformed Newton solve
  ([arXiv:2412.11307](https://arxiv.org/abs/2412.11307)). Thus a public
  complementarity-centered infeasible start is not itself new. That paper does
  not construct a sparse family whose one-step direction encodes a hard
  function, does not make the full step land at a prescribed exact common-\(\mu\)
  central point, and proves no raw-input oracle lower bound.
- Mohammadisiahroudi--Fakhimi--Terlaky likewise give an inexact infeasible
  QIPM whose Algorithm 1 solves a modified normal-equation Newton system by
  QLSA plus tomography and whose Theorem 4.1 proves an iteration bound
  ([arXiv:2205.01220](https://arxiv.org/abs/2205.01220)). This is a direct
  algorithmic predecessor of the Wu--Yang--Terlaky formulation, but it has no
  hard fixed iterate or Newton-state query lower bound.
- Mohammadisiahroudi et al.'s 2025 review also proposes an ``almost-exact''
  dual-log-barrier QIPM: its Algorithm 1 takes a strictly dual-feasible point
  near a center, uses full inexact Newton steps, and its Theorems 1--4 give
  iteration and QRAM-query upper bounds
  ([arXiv:2512.06224](https://arxiv.org/abs/2512.06224)). Its start is an input
  promise rather than this explicit sign-independent primal--dual infeasible
  start, and it contains no lower bound or parity construction.
- Augustino et al. simulate the nonlinear central-path equations directly
  rather than successive Newton systems
  ([arXiv:2311.03977v2](https://arxiv.org/abs/2311.03977v2)). Gribling--Apers--
  Nieuwboer--Walter give a quantum annealing IPM for arbitrary self-concordant
  barriers whose Laplace--Beltrami spectral-gap bound has no condition-number
  dependence ([arXiv:2510.06115](https://arxiv.org/abs/2510.06115)). These are
  important alternative central-path algorithms, but neither asks for or
  lower-bounds the original-coordinate Newton-direction state in the sparse
  coefficient oracle used here.
- Apers--Gribling Theorem 8.4 proves
  \(\Omega(\sqrt{ndr})\) quantum row queries to determine the optimal value of
  a tall inequality LP to constant additive error
  ([arXiv:2311.03215v3](https://arxiv.org/abs/2311.03215v3)). It refines the
  optimal-value lower bound of van Apeldoorn--Gily\'en--Gribling--de Wolf,
  Theorem 29 and Corollary 30
  ([arXiv:1705.01843](https://arxiv.org/abs/1705.01843)). Their output is an
  optimal value, not a Newton state; their instances do not supply this public
  start/common-\(\mu\) endpoint; and their row-query model is not the bounded-
  degree sparse position/value model of Theorem 2. Neither direction of
  implication follows from the stated theorems. In the balanced regime
  \(n,d=\Theta(P)\) and \(r=O(1)\), however, their theorem already has the same
  \(\Omega(P)\) exponent. The novelty here is therefore not the existence of a
  linear-dimensional sparse-LP query lower bound, but the exact Newton-state
  and central-geometry promise under which it holds.
- The closest technical lower bounds are generic QLS results. Orsucci--Dunjko
  Propositions 6 and 17 give
  \(\widetilde\Omega(\min\{\kappa,D\})\) queries for a designated
  positive-definite QLS solution state, including constant-sparse matrix access
  ([arXiv:2101.11868](https://arxiv.org/abs/2101.11868)). Wang--Zhang prove
  \(\Omega(\kappa)\) query depth for designated QLS solution-state generation
  (Theorem 1 and its block-access corollary,
  [arXiv:2407.06012](https://arxiv.org/abs/2407.06012)). Mori et al. prove
  \(\Omega(\kappa\log(1/\epsilon))\) for constant sparsity (Theorem 1) and
  \(\Omega(\kappa\sqrt{s})\) for constant error (Theorem 2)
  ([arXiv:2601.16697v2](https://arxiv.org/abs/2601.16697v2)). Those theorems
  concern a supplied square QLS and its designated inverse state. They do not
  provide this standard-form LP, complementarity-centered start, exact Newton
  secant, common-\(\mu\) endpoint, or scalar deflated reduced Hessian. Theorem 2
  is therefore not a formal corollary; it is best described as an LP/KKT-native
  embedding of parity with a stronger optimization-specific promise.
- The amplification mechanism is prior art. Mori et al.'s construction uses a
  geometrically weighted inverse clock and a repeated clock interval carrying
  parity; Wang--Zhang use the same broad inverse-clock strategy. Biased
  Feynman--Kitaev clocks already realize geometric ground-state amplitudes in
  Caha--Landau--Nagaj, equations (18)--(19)
  ([arXiv:1712.07395](https://arxiv.org/abs/1712.07395)). Neither the gain
  prefix, plateau copies, nor parity decoding should be advertised as new in
  isolation. The candidate contribution is their realization through a
  bounded-degree LP and an exact globally central Newton endpoint.
- Somma--Subasi lower-bound verification of a supplied QLS solution state by
  \(\Omega(\kappa)\) uses of the right-hand-side preparation oracle in the
  worst case ([arXiv:2007.15698](https://arxiv.org/abs/2007.15698)). This is a
  verification/copy-access theorem, not coefficient-query generation hardness.
  Dalzell--Li--Su's beyond-condition-number QLS solver
  ([arXiv:2607.07691](https://arxiv.org/abs/2607.07691)) and Binkowski's
  benchmark-based “practical lower bounds”
  ([arXiv:2604.24362](https://arxiv.org/abs/2604.24362)) likewise do not collide:
  the former is a designated-state upper bound, and the latter is a resource
  estimate on empirical QIPM instances rather than an asymptotic oracle lower
  bound.

The literature evidence therefore supports a narrow novelty claim, not a
priority guarantee: **an exact common-\(\mu\), public-start, bounded-degree
LP Newton-direction state lower bound, with all but \(O(\log N)\) public reduced
modes forming a scalar Hessian block.** Do not claim novelty for public
infeasible starts, central-point simulation, QLS condition-number lower bounds,
parity clocks, or quantum LP lower bounds in general.

Two model qualifications should accompany the theorem. “Exactly centered” at
the start means only \(X^0S^0\mathbf1=\mu_0\mathbf1\); the point is intentionally
primal and dual infeasible and is not on the feasible central path. Also,
Theorem 1 proves the exact algebraic Newton correction and a positive full-step
endpoint. It does not by itself prove that a particular neighborhood/line-
search implementation would accept step length one. The public rational start
has \(O(\log N)\)-bit entries and is free in the coefficient-query model; a gate
complexity statement must separately charge its preparation.

Status: **independent algebra audit passed, including a direct numerical KKT
check on several sizes; targeted literature audit found no exact collision.
The claim remains confined to the stated raw-oracle direction-state
contract.**
