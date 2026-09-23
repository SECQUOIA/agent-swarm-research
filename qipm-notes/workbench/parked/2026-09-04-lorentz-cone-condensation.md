# Winner condensation on a product of Lorentz cones

Status: Proved SOCP corollary; parked after internal novelty collision  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; not a new headline result  
Question: Does the mass--conditioning--visibility transition found for
trace-coupled SDPs have an intrinsically second-order-cone analogue?

## Model and exact central point

Let

\[
 \mathcal L_D=\{(t,z)\in\mathbb R\times\mathbb R^{D-1}:t\geq\|z\|_2\},
 \qquad D\geq3.
\]

Consider \(G\) Lorentz blocks \(x_g=(t_g,z_g)\), constrained by

\[
 x_g\in\mathcal L_D,\qquad \sum_{g=1}^G t_g=1.
\]

One hidden winner \(w\) has cost \(c_w=(a,ae_1)\), where \(a>0\), and every
loser has cost \(c_g=(\delta,0)\), where \(\delta>0\). The optimum is the
winner boundary ray \(t_w=1,z_w=-e_1\), with every loser zero. Use the product
Lorentz barrier

\[
 F(x)=-\sum_g\log(t_g^2-\|z_g\|_2^2).
\]

Let \(\lambda>0\) be the multiplier shift for the trace constraint. Since
\(-\nabla F(t,z)=2(t,-z)/(t^2-\|z\|^2)\), stationarity gives
\(x_g=2\mu(c_g+\lambda e_0)^{-1}\) in the Lorentz Jordan algebra. Therefore
the winner mass \(p=t_w\) and each loser mass \(q=t_g\) are exactly

\[
 p=\mu\left(\frac1\lambda+\frac1{2a+\lambda}\right),
 \qquad q=\frac{2\mu}{\delta+\lambda},
\]

where \(\lambda\) is the unique positive solution of

\[
 p+(G-1)q=1.
\]

In orthonormal light-cone coordinates

\[
 u=(t+z_1)/\sqrt2,\qquad v=(t-z_1)/\sqrt2,
\]

the winner is

\[
 u_w=\frac{\sqrt2\mu}{2a+\lambda},\qquad
 v_w=\frac{\sqrt2\mu}{\lambda},\qquad z_{w,\perp}=0.
\]

## Capacity transition

Set \(\mu=\alpha/G\), with fixed \(\alpha>0\), and let \(G\to\infty\). The
critical capacity is

\[
 \boxed{\alpha_*=\delta/2.}
\]

The exact equation above gives the three regimes

\[
 \begin{array}{c|c|c}
 \text{regime}&\lambda&p\\ \hline
 \alpha<\delta/2&
 \displaystyle \lambda\sim
 \frac{\alpha}{(1-2\alpha/\delta)G}&
 \displaystyle p\to1-\frac{2\alpha}{\delta}\\[2mm]
 \alpha=\delta/2&
 \displaystyle \lambda\sim\frac{\delta}{\sqrt{2G}}&
 \displaystyle p\sim\frac1{\sqrt{2G}}\\[2mm]
 \alpha>\delta/2&
 \displaystyle \lambda\to2\alpha-\delta&
 \displaystyle p=\Theta(G^{-1}).
 \end{array}
\]

Thus the Lorentz central path has the same constant / square-root / inverse-
linear winner-mass transition as block log-det condensation, but its Hessian
has a distinct Peirce-
\(1/2\) transverse scale.

## Reduced-Hessian phase law

At the winner, the barrier Hessian eigenvalues in the orthonormal coordinates
\((u,v,z_\perp)\) are

\[
 A=\frac{(2a+\lambda)^2}{2\mu^2},\qquad
 B=\frac{\lambda^2}{2\mu^2},\qquad
 C=\frac{\lambda(2a+\lambda)}{2\mu^2}
 \quad(D-2\text{ copies}).
\]

Every loser Hessian is scalar with eigenvalue

\[
 E=\frac{(\delta+\lambda)^2}{2\mu^2}.
\]

Restrict to the tangent space \(\sum_g h_{t,g}=0\). Loser transverse and
difference modes retain eigenvalue \(E\). In the symmetric trace sector,
eliminating the average loser \(t\)-coordinate gives the two-variable Rayleigh
quotient

\[
 R_G(u,v)=
 \frac{Au^2+Bv^2+\dfrac{E}{2(G-1)}(u+v)^2}
      {u^2+v^2+\dfrac1{2(G-1)}(u+v)^2}.
\]

Together with the transverse winner eigenvalue \(C\), this determines the
extreme eigenvalues. An exact full-spectrum description is as follows. Put

\[
 A_0=(A+B)/2,\quad B_0=(A-B)/2,\quad
 \beta_G=\sqrt{(G-1)/G}.
\]

Then \(E\) has multiplicity \(GD-D-1\), \(C\) has multiplicity \(D-2\),
and the last two eigenvalues are those of

\[
 \begin{bmatrix}
 \beta_G^2A_0+E/G&\beta_GB_0\\
 \beta_GB_0&A_0
 \end{bmatrix}.
\]

The multiplicities sum to the tangent dimension \(GD-1\). Substitution of the three
asymptotic regimes gives

\[
 \lambda_{\max}(H_{\rm red})=\Theta(G^2)
\]

in all three regimes, while

\[
 \lambda_{\min}(H_{\rm red})=
 \begin{cases}
 \Theta(G),&\alpha<\delta/2,\\
 \Theta(G),&\alpha=\delta/2,\\
 \Theta(G^2),&\alpha>\delta/2.
 \end{cases}
\]

Hence

\[
 \boxed{
 \kappa_{\rm red}=
 \begin{cases}
 \Theta(G),&\alpha\leq\delta/2,\\
 \Theta(1),&\alpha>\delta/2.
 \end{cases}}
\]

At criticality the sharper constants predicted by the quotient are

\[
 \lambda_{\min}/G\to2,
 \qquad
 \lambda_{\max}/G^2\to
 \max\{8a^2/\delta^2,2\}.
\]

Below capacity, writing \(r=1-2\alpha/\delta\), the predicted constants are

\[
 \frac{\lambda_{\min}}G\to
 \min\left\{\frac{a}{r\alpha},\frac{\delta^2}{4\alpha^2}\right\},
\]

\[
 \frac{\lambda_{\max}}{G^2}\to
 \max\left\{\frac{2a^2}{\alpha^2},
              \frac{\delta^2}{2\alpha^2}\right\}.
\]

These formulas and constants have been checked independently from the exact
KKT system and the tangent-space eigendecomposition.

## Visibility and sparse-query implication

For the Euclidean normalized primal vector, the winner probability is exactly

\[
 P_w=\frac{\lambda^{-2}+(\lambda+2a)^{-2}}
 {\lambda^{-2}+(\lambda+2a)^{-2}+2(G-1)(\delta+\lambda)^{-2}}.
\]

Below capacity the
winner has asymptotically all normalized-vector mass. At criticality,

\[
 \|x_w\|_2^2\sim G^{-1},\qquad
 \sum_{g\ne w}\|x_g\|_2^2\sim G^{-1},
\]

so \(P_w\to1/2\). Above capacity \(P_w=\Theta(1/G)\). More precisely, with
\(L=2\alpha-\delta\),

\[
 GP_w\to2\alpha^2\left(L^{-2}+(L+2a)^{-2}\right).
\]

If the winner marker is supplied
by a local block oracle, preparing a constant-error primal state below or at
the transition therefore costs \(\Omega(\sqrt G)\) queries by unstructured
search; Grover search followed by the exact formulas matches this exponent.

The single dense trace equality can be replaced by a public accumulator chain,
giving constant row and column incidence with free auxiliary scalars. The cone
blocks have fixed size. This makes the family a genuinely sparse SOCP rather
than an LP embedding.

## Novelty audit and collision

The calculation is useful but not a distinct headline theorem. For \(D=3\),
\(\mathcal Q_3\) is linearly isomorphic to \(\mathbb S_+^2\); under the
standard map the winner has eigenvalues \(\{0,2a\}\) and each loser has
eigenvalues \(\{\delta,\delta\}\). The threshold and condition phases are
therefore already instances of the block log-det condensation theorems in
`paper/sections/06-condensation.tex`. Higher \(D\) adds the standard rank-two
Peirce-\(1/2\) multiplicity \(D-2\), not a new mechanism. The note is retained
as an explicit SOCP corollary and exact spectral calculation only.
