# Congruence condition--recovery frontier for sparse QIPM Newton states

Date: 2026-09-02

## Result in one sentence

For every scalar block-diagonal SPD congruence on the active/inactive split of
a coupled strictly complementary LP normal matrix, the product of the square
root of the transformed condition number and the direct physical-state
recovery sensitivity is at least order \(\mu^{-1}\). The power scalings are
exactly the order-optimal interpolation between the two costs.

This is a theorem about a specified congruence family and output map. It is not
a lower bound against arbitrary preconditioners or arbitrary quantum linear
system algorithms.

## Setting

Let the fixed real Euclidean space decompose orthogonally as

\[
 \mathbb R^r=U\oplus K,
 \qquad Q=\Pi_U,
 \qquad R=\Pi_K.
\]

For \(0<\mu\leq\mu_0\), suppose

\[
 H_\mu=\mu^{-1}C_\mu+\mu D_\mu                                      \tag{1}
\]

is symmetric positive definite and satisfies:

1. \(C_\mu=QC_\mu Q\), and the restriction of \(C_\mu\) to \(U\)
   converges to \(C\succ0\).
2. \(D_\mu\succeq0\), \(\sup_\mu\|D_\mu\|<\infty\), and the
   \(K\)-restriction \(D_{KK,\mu}=RD_\mu R|_K\) converges to
   \(D_{KK}\succ0\).
3. All other blocks of \(D_\mu\) converge. Write their limits as
   \(D_{UU},D_{UK},D_{KU}\).
4. The right-hand side \(f\in U\) is fixed and nonzero.

These assumptions are the fixed-instance normal-equation asymptotics of a
strictly complementary LP when \(U\) is the range of the columns whose primal
variables stay positive. They also state explicitly what is needed below; no
uniform convergence in a growing dimension is claimed.

Define

\[
 p=C^{-1}f,
 \qquad
 g=D_{KK}^{-1}D_{KU}p.                                    \tag{2}
\]

The frontier is nontrivial when

\[
 g\neq0.                                                   \tag{3}
\]

Condition (3) says that the exact-centering solve has a leading inactive
component. It is the same generic active--inactive coupling that causes the
second-inverse obstruction for the unscaled normal equations.

For a fixed \(0\leq\gamma\leq1\), define

\[
 T_{\mu,\gamma}
 =\mu^{\gamma/2}Q+\mu^{-\gamma/2}R,
 \qquad
 G_{\mu,\gamma}=T_{\mu,\gamma}H_\mu T_{\mu,\gamma}.        \tag{4}
\]

Here \(\gamma\), rather than \(\beta\), is used for the scaling exponent so
that it is not confused with LP nondegeneracy constants.

Let

\[
 \eta_\mu=H_\mu^{-1}f,
 \qquad
 z_{\mu,\gamma}=T_{\mu,\gamma}^{-1}\eta_\mu.              \tag{5}
\]

Then \(z_{\mu,\gamma}\) is the solution of

\[
 G_{\mu,\gamma}z=T_{\mu,\gamma}f.
\]

Because \(f\in U\), the normalized transformed right-hand side is exactly the
normalized original right-hand side. Thus the tradeoff below is not caused by
a change in right-hand-side state preparation.

## Recovery map and its condition number

The normalized contraction representing recovery is

\[
 \mathsf R_{\mu,\gamma}
 :=\frac{T_{\mu,\gamma}}{\|T_{\mu,\gamma}\|}
 =\mu^\gamma Q+R.                                         \tag{6}
\]

For a unit vector \(w\) with \(\mathsf Rw\neq0\), define the normalized-state
recovery map

\[
 \Phi_{\mu,\gamma}(w)
 =\frac{\mathsf R_{\mu,\gamma}w}
        {\|\mathsf R_{\mu,\gamma}w\|}.                   \tag{7}
\]

Its local Euclidean condition number at a unit input \(w\) is

\[
 \chi_{\mu,\gamma}(w)
 :=\left\|
 D\Phi_{\mu,\gamma}(w)\big|_{w^\perp}
 \right\|_{2\to2}.                                       \tag{8}
\]

Equivalently, if \(\widehat y=\Phi(w)\),

\[
 \chi_{\mu,\gamma}(w)
 =\frac{
 \left\|(I-\widehat y\widehat y^\top)
 \mathsf R_{\mu,\gamma}(I-ww^\top)\right\|
 }{\|\mathsf R_{\mu,\gamma}w\|}.                        \tag{9}
\]

This definition makes “recovery sensitivity” precise. It measures the largest
first-order error in the recovered normalized state per unit error tangent to
the input state.

## Theorem

Under assumptions (1)--(3), for every fixed \(\gamma\in[0,1]\), as
\(\mu\downarrow0\):

1. The congruence-scaled condition number satisfies

   \[
   \boxed{
   \kappa_2(G_{\mu,\gamma})
   =\Theta\!\left(\mu^{-2(1-\gamma)}\right).
   }                                                        \tag{10}
   \]

2. The physical and transformed solutions have the expansions

   \[
   \eta_\mu
   =\mu\binom{p}{-g}+o(\mu),                              \tag{11}
   \]

   \[
   z_{\mu,\gamma}
   =\binom{
      \mu^{1-\gamma/2}(p+o(1))
   }{
      -\mu^{1+\gamma/2}(g+o(1))
   }.                                                       \tag{12}
   \]

   Thus the inactive-to-active amplitude ratio in the transformed solution is
   \(\Theta(\mu^\gamma)\), although the inactive component has constant
   relative weight in the physical solution.

3. If \(\widehat z=z/\|z\|\), then

   \[
   \Phi_{\mu,\gamma}(\widehat z)
   =\frac{\eta_\mu}{\|\eta_\mu\|}                         \tag{13}
   \]

   exactly. A direct block-encoding/postselection implementation of
   \(\mathsf R_{\mu,\gamma}\) succeeds with probability

   \[
   \boxed{
   P_{\rm rec}
   =\|\mathsf R_{\mu,\gamma}\widehat z\|^2
   =\Theta(\mu^{2\gamma}).
   }                                                        \tag{14}
   \]

4. The normalized recovery map has local condition number

   \[
   \boxed{
   \chi_{\mu,\gamma}(\widehat z)
   =\Theta(\mu^{-\gamma}).
   }                                                        \tag{15}
   \]

   Therefore producing the physical state to error \(O(\epsilon)\) from an
   otherwise unstructured approximation to \(\widehat z\) requires transformed
   state error \(O(\epsilon\mu^\gamma)\) in the worst local direction. This
   accuracy dependence is also attained, not merely bounded above.

Consequently,

\[
\boxed{
 \sqrt{\kappa_2(G_{\mu,\gamma})}\,
 \chi_{\mu,\gamma}(\widehat z)
 =\Theta(\mu^{-1})
 =\Theta\!\left(\sqrt{\kappa_2(H_\mu)}\right).
}                                                           \tag{16}
\]

Equivalently, direct amplitude amplification of the recovery flag obeys

\[
 \sqrt{\kappa_2(G_{\mu,\gamma})}\,P_{\rm rec}^{-1/2}
 =\Theta(\mu^{-1}).                                        \tag{17}
\]

Equations (16)--(17) are structural products, not generic QLS runtime
formulas. A conventional block-encoded QLS algorithm can depend linearly on
\(\kappa(G)\), while special positive-definite, factorized, filtered, or
variable-time algorithms can have different instance-dependent parameters.

The endpoints are transparent. At \(\gamma=0\), there is no scaling and
recovery is stable, while \(\kappa(H_\mu)=\Theta(\mu^{-2})\). At
\(\gamma=1\), the congruence-scaled matrix is uniformly conditioned, but
direct recovery succeeds with probability \(\Theta(\mu^2)\) and has local
condition number \(\Theta(\mu^{-1})\).

## Proof

### Condition number

Use \(U\oplus K\) blocks and put

\[
 a_\mu=\mu^{-(1-\gamma)},
 \qquad
 b_\mu=\mu^{1-\gamma}=a_\mu^{-1}.
\]

Equation (4) gives

\[
 G_{\mu,\gamma}
 =\begin{pmatrix}
 a_\mu C_\mu+\mu^{1+\gamma}D_{UU,\mu}
     &\mu D_{UK,\mu}\\
 \mu D_{KU,\mu}
     &b_\mu D_{KK,\mu}
 \end{pmatrix}.                                           \tag{18}
\]

The upper-left block \(A_\mu\) has all eigenvalues
\(\Theta(a_\mu)\). Its Schur complement is

\[
 S_\mu
 =b_\mu D_{KK,\mu}
  -\mu^2D_{KU,\mu}A_\mu^{-1}D_{UK,\mu}.                  \tag{19}
\]

Since \(\|A_\mu^{-1}\|=O(b_\mu)\), the second term in (19) is
\(O(\mu^2b_\mu)\). Hence

\[
 S_\mu=\Theta(b_\mu)I_K                                  \tag{20}
\]

in Loewner order for sufficiently small \(\mu\). The block elimination
factor has off-diagonal norm
\(\|A_\mu^{-1}\mu D_{UK,\mu}\|=O(\mu b_\mu)=o(1)\).
Therefore (18) is uniformly well-conditioned, by a near-identity congruence,
to \(\operatorname{diag}(A_\mu,S_\mu)\). It follows that

\[
 \lambda_{\max}(G)=\Theta(a_\mu),
 \qquad
 \lambda_{\min}(G)=\Theta(b_\mu),
\]

which proves (10). Taking \(\gamma=0\) also proves
\(\kappa_2(H_\mu)=\Theta(\mu^{-2})\).

### Solution asymptotics

The \(K\)-block of \(H_\mu\eta_\mu=f\) gives exactly

\[
 \eta_{K,\mu}
 =-D_{KK,\mu}^{-1}D_{KU,\mu}\eta_{U,\mu}.                \tag{21}
\]

Substitution into the \(U\)-block gives

\[
 \left[\mu^{-1}C_\mu+\mu E_\mu\right]\eta_{U,\mu}=f,    \tag{22}
\]

where

\[
 E_\mu=D_{UU,\mu}
 -D_{UK,\mu}D_{KK,\mu}^{-1}D_{KU,\mu}
\]

is bounded. Thus

\[
 \eta_{U,\mu}
 =\mu(C_\mu+\mu^2E_\mu)^{-1}f
 =\mu(p+o(1)).                                             \tag{23}
\]

Equations (21), (23), and the block convergence assumptions prove (11).
Applying \(T^{-1}\) proves (12).

### Success probability

The squared norms following from (11)--(12) are

\[
 \|\eta_\mu\|^2
 =\mu^2\left(\|p\|^2+\|g\|^2+o(1)\right),                \tag{24}
\]

\[
 \|z_{\mu,\gamma}\|^2
 =\mu^{2-\gamma}
 \left(\|p\|^2+\mu^{2\gamma}\|g\|^2+o(1)
       +o(\mu^{2\gamma})\right).                         \tag{25}
\]

The separate little-oh terms in (25) only record the two convergent block
expansions; for \(\gamma=0\), their sum is simply \(o(1)\).

Because \(\mathsf R=T/\|T\|\),

\[
 \mathsf R_{\mu,\gamma}z_{\mu,\gamma}
 =\mu^{\gamma/2}\eta_\mu.                                \tag{26}
\]

This proves exact recovery (13), and (24)--(26) give

\[
 \|\mathsf R\widehat z\|
 =\mu^\gamma
 \frac{(\|p\|^2+\|g\|^2+o(1))^{1/2}}
      {(\|p\|^2+\mu^{2\gamma}\|g\|^2+o(1))^{1/2}}
 =\Theta(\mu^\gamma).                                    \tag{27}
\]

Squaring proves (14). Notice that (27) equals one identically at
\(\gamma=0\), as it must.

### Sharp local recovery sensitivity

Differentiating (7) gives (9), so immediately

\[
 \chi_{\mu,\gamma}(\widehat z)
 \leq\|\mathsf R\widehat z\|^{-1}
 =O(\mu^{-\gamma}).                                       \tag{28}
\]

For the matching lower bound, first suppose \(\gamma>0\), put
\(k=g/\|g\|\in K\), and project \(k\) onto
\(\widehat z^\perp\). By (12), the resulting unit tangent vector is
\(k+o(1)\). The recovered physical state converges to

\[
 \widehat\eta_0
 =\frac{(p,-g)}{\sqrt{\|p\|^2+\|g\|^2}}.
\]

Since \(p\neq0\), the component of \(k\) orthogonal to
\(\widehat\eta_0\) has norm at least

\[
 \frac{\|p\|}{\sqrt{\|p\|^2+\|g\|^2}}>0.                \tag{29}
\]

The numerator of (9) is therefore bounded below by a positive constant.
Combining this with (27) proves the lower bound in (15). For \(\gamma=0\),
\(\mathsf R=I\) and \(\chi=1\) directly. This completes the proof.

## Exact two-sparse LP witness

Consider the fixed standard-form LP

\[
 \begin{aligned}
 \min_{x\geq0}\quad &x_2+x_3\\
 \text{subject to}\quad
 &x_1+x_2=1,\\
 &x_2-x_3=0.
 \end{aligned}                                             \tag{30}
\]

Thus

\[
 A=\begin{pmatrix}1&1&0\\0&1&-1\end{pmatrix},
 \qquad
 b=\binom10,
 \qquad
 c=\begin{pmatrix}0\\1\\1\end{pmatrix}.                \tag{31}
\]

Every row and column of \(A\) has at most two nonzeros. The unique primal
optimum is \(x^*=(1,0,0)\). The central path has

\[
 x_2=x_3=t_\mu,
 \qquad
 x_1=1-t_\mu,                                              \tag{32}
\]

and, by symmetry and complementarity,

\[
 s_2=s_3=q_\mu,
 \qquad
 s_1=\frac{\mu}{1-t_\mu},
 \qquad
 t_\mu q_\mu=\mu,                                        \tag{33}
\]

\[
 q_\mu=1+\frac{\mu}{2(1-t_\mu)}.                         \tag{34}
\]

Indeed, dual feasibility gives
\(s_1=-y_1\), \(s_2=1-y_1-y_2\), and \(s_3=1+y_2\).
Equations \(x_2=x_3\) and \(x_is_i=\mu\) imply
\(s_2=s_3\), hence \(y_2=-y_1/2\) and (34). Since
\(q_\mu\geq1\), (33)--(34) give

\[
 t_\mu=\mu+O(\mu^2),
 \qquad
 q_\mu=1+O(\mu).                                         \tag{35}
\]

The normal matrix is

\[
 H_\mu=A(XS^{-1})A^\top
 =\frac{(1-t_\mu)^2}{\mu}
   \begin{pmatrix}1&0\\0&0\end{pmatrix}
 +\frac{t_\mu^2}{\mu}
   \begin{pmatrix}1&1\\1&2\end{pmatrix}.                \tag{36}
\]

Taking \(U=\operatorname{span}\{e_1\}\), \(K=\operatorname{span}\{e_2\}\),
equation (36) has exactly the form (1), with

\[
 C_\mu=(1-t_\mu)^2e_1e_1^\top\longrightarrow e_1e_1^\top,
\]

\[
 D_\mu=\left(\frac{t_\mu}{\mu}\right)^2
 \begin{pmatrix}1&1\\1&2\end{pmatrix}
 \longrightarrow
 \begin{pmatrix}1&1\\1&2\end{pmatrix}.                 \tag{37}
\]

For the exact-centering right-hand side \(f=b=e_1\),

\[
 p=1,
 \qquad
 g=D_{KK}^{-1}D_{KU}p=\frac12\neq0.                       \tag{38}
\]

Thus this single two-row, three-variable, two-sparse LP realizes every exponent
in (10), (14), and (15). In particular,

\[
 H_\mu^{-1}b
 =\mu\binom{1}{-1/2}+o(\mu),                             \tag{39}
\]

and at \(\gamma=1\) the scaled condition number converges to a finite positive
constant while the recovery amplitude is asymptotic to
\(\sqrt{5/4}\,\mu\).

## Extension to every scalar block-diagonal SPD congruence

The power form in (4) is not needed. Retain assumptions (1)--(3), and let

\[
 T_\mu=t_U(\mu)Q+t_K(\mu)R,
 \qquad t_U(\mu),t_K(\mu)>0,                              \tag{40}
\]

with no regularity or power-law assumption on the two scalar functions. Put

\[
 r_\mu=\frac{t_U(\mu)}{t_K(\mu)},
 \qquad
 M_\mu=\max\left\{\frac{r_\mu}{\mu},
                         \frac{\mu}{r_\mu}\right\},
 \qquad
 K_\mu=\max\{r_\mu,r_\mu^{-1}\}.                         \tag{41}
\]

Multiplying \(T_\mu\) by any positive scalar changes neither the condition
number below nor the normalized recovery map. Thus \(r_\mu\), \(M_\mu\), and
\(K_\mu\) are invariant under the irrelevant choice of representation scale.
They are also unchanged by simultaneous orthogonal changes of basis within
\(U\) and \(K\). This is the representation invariance asserted here; arbitrary
nonorthogonal changes that mix the two subspaces are outside the theorem.

### General scalar-block frontier theorem

Let

\[
 \widetilde G_\mu=T_\mu H_\mu T_\mu,
 \qquad
 \widetilde z_\mu=T_\mu^{-1}\eta_\mu,
 \qquad
 \widehat{\widetilde z}_\mu
 =\frac{\widetilde z_\mu}{\|\widetilde z_\mu\|}.          \tag{42}
\]

Normalize the recovery contraction by

\[
 \widetilde{\mathsf R}_\mu
 =\frac{T_\mu}{\|T_\mu\|},
 \qquad
 \widetilde\Phi_\mu(w)
 =\frac{\widetilde{\mathsf R}_\mu w}
        {\|\widetilde{\mathsf R}_\mu w\|}.               \tag{43}
\]

Then, uniformly over every choice of positive \(t_U(\mu),t_K(\mu)\),

\[
 \boxed{
 \sqrt{\kappa_2(\widetilde G_\mu)}=\Theta(M_\mu).
 }                                                         \tag{44}
\]

\[
 \boxed{
 \widetilde P_{\rm rec}^{-1/2}
 :=\|\widetilde{\mathsf R}_\mu
       \widehat{\widetilde z}_\mu\|^{-1}
 =\Theta(K_\mu).
 }                                                         \tag{45}
\]

Also, with the local derivative defined as in (8),

\[
 \boxed{
 \widetilde\chi_\mu
 :=\left\|D\widetilde\Phi_\mu(
       \widehat{\widetilde z}_\mu)
       \big|_{\widehat{\widetilde z}_\mu^\perp}\right\|
 =\Theta(K_\mu).
 }                                                         \tag{46}
\]

The constants in these \(\Theta\)-relations depend only on the fixed limiting
blocks and \(f\), not on the two scaling functions. Consequently,

\[
 \boxed{
 \sqrt{\kappa_2(\widetilde G_\mu)}\,
 \widetilde\chi_\mu
 =\Theta(M_\mu K_\mu)
 \geq c\mu^{-1}
 =\Theta\!\left(\sqrt{\kappa_2(H_\mu)}\right).
 }                                                         \tag{47}
\]

The same inequality holds with \(\widetilde P_{\rm rec}^{-1/2}\) in place of
\(\widetilde\chi_\mu\). Moreover,

\[
 M_\mu K_\mu=\Theta(\mu^{-1})                            \tag{48}
\]

if and only if

\[
 r_\mu=\Omega(\mu)
 \quad\text{and}\quad
 r_\mu=O(1).                                              \tag{49}
\]

Thus (49) is the maximal order-optimal scalar-block class. Inside the central
window \(\mu\lesssim r_\mu\lesssim1\), condition improvement and recovery cost
trade exactly. Scaling more strongly in either direction makes their product
asymptotically worse:

\[
 M_\mu K_\mu
 =\begin{cases}
   \mu/r_\mu^2, & r_\mu<\mu,\\
   1/\mu,       & \mu\leq r_\mu\leq1,\\
   r_\mu^2/\mu, & r_\mu>1.
 \end{cases}                                               \tag{50}
\]

The power family (4) has \(r_\mu=\mu^\gamma\). It traverses the whole central
window for \(0\leq\gamma\leq1\), and (44)--(46) reduce exactly to
(10), (14), and (15).

### Proof of the general theorem

First, (1) is uniformly spectrally equivalent to the uncoupled two-scale
operator

\[
 P_\mu=\mu^{-1}Q+\mu R.                                   \tag{51}
\]

Indeed, boundedness gives the upper inequality
\(H_\mu\preceq C_+P_\mu\). For the lower inequality, write a vector as
\(u+k\in U\oplus K\). Choose fixed \(c,d,M>0\) such that
\(C_\mu|_U\succeq cI\), \(D_{KK,\mu}\succeq dI\), and
\(\|D_{UK,\mu}\|\leq M\). Since the \(UU\) principal block of
\(D_\mu\succeq0\) is positive semidefinite, Young's inequality gives

\[
 \begin{aligned}
 (u+k)^\top H_\mu(u+k)
 &\geq \frac{c}{\mu}\|u\|^2
   +\mu d\|k\|^2-2\mu M\|u\|\|k\|\\
 &\geq
 \left(\frac{c}{\mu}-\frac{2M^2\mu}{d}\right)\|u\|^2
 +\frac{d\mu}{2}\|k\|^2.
 \end{aligned}
\]

For sufficiently small \(\mu\), the coefficient of \(\|u\|^2\) is at least
\(c/(2\mu)\). Hence constants
\(0<c_0<C_0<\infty\), independent of \(\mu\), satisfy

\[
 c_0P_\mu\preceq H_\mu\preceq C_0P_\mu.                 \tag{52}
\]

Congruence preserves Loewner order, so

\[
 c_0\left(\frac{t_U^2}{\mu}Q+\mu t_K^2R\right)
 \preceq \widetilde G_\mu
 \preceq
 C_0\left(\frac{t_U^2}{\mu}Q+\mu t_K^2R\right).          \tag{53}
\]

The ratio of the two displayed block eigenvalues is
\(r_\mu^2/\mu^2\). This proves (44), including arbitrarily severe
under-scaling \(r_\mu\ll\mu\) and over-scaling \(r_\mu\gg1\).

Next, (11) and the nonzero vectors \(p,g\) imply the uniform two-sided bounds

\[
 \|\eta_{U,\mu}\|=\Theta(\mu),
 \qquad
 \|\eta_{K,\mu}\|=\Theta(\mu).                           \tag{54}
\]

Therefore

\[
 \begin{aligned}
 \|\widetilde{\mathsf R}_\mu
       \widehat{\widetilde z}_\mu\|
 &=\frac{\|\eta_\mu\|}
 {\max\{t_U,t_K\}
  \sqrt{\|\eta_{U,\mu}\|^2/t_U^2+
        \|\eta_{K,\mu}\|^2/t_K^2}}\\
 &=\Theta(K_\mu^{-1}),
 \end{aligned}                                             \tag{55}
\]

which proves (45).

For the sharp sensitivity lower bound, restrict the input and output to the
two-dimensional plane spanned by
\(u_\mu=\eta_{U,\mu}/\|\eta_{U,\mu}\|\) and
\(k_\mu=\eta_{K,\mu}/\|\eta_{K,\mu}\|\). Put
\(a_\mu=\|\eta_{U,\mu}\|\) and
\(b_\mu=\|\eta_{K,\mu}\|\). Direct differentiation of the angle of the
normalized map induced by \(\operatorname{diag}(t_U,t_K)\) gives the tangent
gain

\[
 \frac{r_\mu^{-1}a_\mu^2+r_\mu b_\mu^2}
      {a_\mu^2+b_\mu^2}.                                  \tag{56}
\]

By (54), (56) is \(\Theta(K_\mu)\). This is a lower bound on the full
derivative norm. Conversely, differentiation as in (9) and (55) gives
\(\widetilde\chi_\mu=O(K_\mu)\). This proves (46).

Finally, the elementary three-case calculation in (50) proves (47)--(49).

### Exact matching witness

The LP (30) matches the general theorem, not only its power-law corollary.
Equations (36)--(39) give (52) with fixed constants and give nonzero limiting
active and inactive physical solution components \(p=1\) and \(g=1/2\).
Consequently every positive pair \(t_U(\mu),t_K(\mu)\), including ratios that
oscillate or lie outside the central window, attains (44)--(50) up to fixed
constants on this same two-sparse central path.

## What the theorem does and does not imply

The theorem proves a sharp structural frontier for:

- the fixed active/inactive decomposition \(U\oplus K\);
- every scalar block-diagonal SPD congruence (40), with the power congruences
  (4) as the order-optimal interpolation;
- exact-centering right-hand sides in \(U\);
- a coupled physical solution, \(g\neq0\); and
- recovery of the complete normalized physical Newton state through (6).

It does **not** prove that every quantum preconditioner costs
\(\Omega(\mu^{-1})\). In particular:

1. A left preconditioner can preserve the solution ray without a recovery map.
   The direct stable active-subspace construction in
   `stable-active-subspace-qipm.md` does exactly this when the active projector
   and a favorable directly assembled block encoding are available.
2. A solver may directly prepare the physical state, estimate only an
   observable, or work with a rectangular factorization rather than recover
   from the congruence-scaled state.
3. Variable-time algorithms can assign different costs to spectral or flagged
   branches. Equation (14) is the cost of direct contraction and postselection;
   it is not by itself a query lower bound against every variable-time scheme.
4. The theorem does not charge construction of \(Q\), block-encoding
   normalization, changing-iterate updates, right-hand-side loading, norm
   estimation, or classical output.
5. If \(g=0\), the leading physical solution lies entirely in \(U\), and the
   success and sensitivity formulas (45)--(46) need not hold. Postselection
   loss can disappear, while worst-direction sensitivity depends on whether
   the solver error can populate \(K\). Higher-order coupling and
   subspace-preserving error promises then need a separate analysis.
6. The constants are fixed-dimension asymptotic constants. A growing sparse
   family needs uniform spectral bounds on \(C_\mu\), \(D_{KK,\mu}\), and the
   coupling.

## Literature and publishability assessment

The general ingredients are established. Quantum preconditioning has long
required efficient implementation of both the transformed system and its
solution map. Tong, An, Wiebe, and Lin analyze fast inversion and preconditioned
QLS methods ([arXiv:2008.13295](https://arxiv.org/abs/2008.13295)). Lapworth and
Sünderhauf show that block-encoding subnormalization can erase a classical
condition-number gain and distinguish separate product encodings from direct
encodings ([arXiv:2502.20908](https://arxiv.org/abs/2502.20908)). Low and Su
give optimal dependence on inverse success amplitude and a modern
variable-time/block-preconditioning framework
([arXiv:2410.18178](https://arxiv.org/abs/2410.18178)). Structured symmetric
preconditioning with direct encoding is also used for multilevel Poisson
systems ([arXiv:2505.06866](https://arxiv.org/abs/2505.06866)).

Against that literature, the algebraic observation that a nonunitary scaling
moves difficulty from conditioning into success probability is not, alone, a
publishable quantum-linear-systems result. The item not found in the reviewed
open literature is the exact QIPM specialization:

- the strict-complementarity exponents
  \(\mu^{-2(1-\gamma)}\), \(\mu^{2\gamma}\), and
  \(\mu^{-\gamma}\);
- the representation-invariant scalar-block inequality (47), its maximal
  equality class (49), and the power-law product (16);
- the sharp normalized-state derivative statement; and
- realization by one fixed two-sparse LP central path.

The appropriate assessment is therefore:

**Publishable as a structural lemma or obstruction inside a broader QIPM
paper, but not yet credible as a standalone universal lower bound.**

A stronger standalone result would need an oracle-model lower bound covering a
specified class of preconditioners and variable-time recovery algorithms, or a
dichotomy showing that every efficiently encodable strict-complementarity
preconditioner must pay in normalization, state recovery, projector access, or
output precision. The present theorem deliberately stops short of that claim.
