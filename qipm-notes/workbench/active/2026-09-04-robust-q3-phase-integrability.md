# A robust phase-integrability obstruction for approximate \(Q_3\) contact factors

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High under the stated boundary-factor and conditioning hypotheses

## Result in one line

An exact globally \(C^1\), nonzero \(Q_3\) contact factor has a mixed-
curvature rank dropout somewhere on every sphere \(S^{N-1}\), \(N\geq3\).
This remains quantitatively true for an approximate contact factor.  If its
diagonal contact defect is at most \(\epsilon\), its defect derivative is at
most \(\eta\), and its radial log-scale derivative is at most \(K\), then at
some contact point its mixed channel has norm at most

\[
                         K\eta+K^2\epsilon.                    \tag{1}
\]

Consequently a channel which is uniformly \(\delta\)-close to rank-one
positive forms whose nonzero eigenvalue is at least \(\mu\) must satisfy

\[
                 \boxed{\delta+K\eta+K^2\epsilon\geq\mu.}      \tag{2}
\]

Unlike the frame/parallelizability obstruction, (2) holds also in body
dimensions \(N=4,8\).  It is channelwise: under the hypotheses, every
globally labelled channel must incur the threshold, not merely one of the
\(N-1\) channels.

For the capacity-saturated case of exactly \(n=N-1\) channels, the spectral
floor need not be assumed.  If their sum is \(\xi\)-close to the sphere
metric and every channel is \(\delta\)-close to some rank-one positive form,
then

\[
             \boxed{\xi+(n+1)\delta+K\eta+K^2\epsilon\geq1}    \tag{2a}
\]

under common conditioning bounds.  Thus a saturated approximate
factorization cannot simultaneously have small contact error, controlled
radial scale, a stable \(C^1\) modulus, near-Parseval aggregate curvature,
and uniformly rank-one channels.

## Coordinate-free theorem

Let \(M\) be a closed, connected, simply connected smooth manifold with a
Riemannian metric.  The factor maps below need only be \(C^1\).  The intended case is
\(M=S^{N-1}\), \(N\geq3\).  Write

\[
 Q_3=\{(t,z)\in\mathbb R\oplus\mathbb R^2:t\geq\|z\|_2\}.
\]

Let

\[
        A,B:M\longrightarrow\partial Q_3\setminus\{0\}        \tag{3}
\]

be \(C^1\).  Define the nonnegative diagonal contact defect and the mixed
channel by

\[
 \sigma(x)=\langle A(x),B(x)\rangle,
 \qquad
 C_x(u,v)=-\langle dA_xu,dB_xv\rangle.                         \tag{4}
\]

Here \(C_x\) is allowed to be a nonsymmetric bilinear form.  All norms below
are the operator norms induced by the Riemannian metric and the standard
Euclidean structure of the self-dual Lorentz cone.

Write the two nonzero boundary maps uniquely as

\[
 A=a(1,p),\qquad B=b(1,-q),qquad
 a,b>0,\quad p,q:M\to S^1,                                   \tag{5}
\]

and put

\[
 K_A=\sup_M\|d\log a\|,qquad
 K_B=\sup_M\|d\log b\|,qquad K=\min\{K_A,K_B\}.              \tag{6}
\]

### Theorem 1 (robust phase dropout)

If

\[
             0\leq\sigma\leq\epsilon,qquad
             \|d\sigma\|\leq\eta,                            \tag{7}
\]

then there is \(x_*\in M\) such that

\[
                       \|C_{x_*}\|\leq K\eta+K^2\epsilon.     \tag{8}
\]

For \(\mu>0\), let

\[
 \mathcal R_\mu(T_xM)=
 \{\lambda\,\omega\otimes\omega:
      \omega\in T_x^*M,\ \|\omega\|=1,\ \lambda\geq\mu\}   \tag{9}
\]

be the well-conditioned rank-one positive forms.  Then

\[
 \sup_{x\in M}\operatorname{dist}
       \bigl(C_x,\mathcal R_\mu(T_xM)\bigr)
 \geq \bigl[\mu-K\eta-K^2\epsilon\bigr]_+.                  \tag{10}
\]

In particular, uniform distance at most \(\delta\) from
\(\mathcal R_\mu\) implies (2).

### Proof

Because \(M\) is simply connected, the primal phase has a \(C^1\) lift
\(p=e^{\mathrm i\theta}\) with \(\theta:M\to\mathbb R\).  Compactness
gives a maximum \(x_A\) of \(\theta\), where
\(d\theta=0\), hence \(dp=0\).  At this point differentiation of (5) gives

\[
 dA=\alpha\otimes A,qquad \alpha=d\log a.                    \tag{11}
\]

Differentiating \(\sigma=\langle A,B\rangle\) and using (11) gives

\[
 \langle A,dB\rangle=d\sigma-\sigma\alpha,
 \qquad
 C=-\alpha\otimes(d\sigma-\sigma\alpha).                    \tag{12}
\]

Therefore

\[
                         \|C_{x_A}\|
 \leq K_A\eta+K_A^2\epsilon.                                 \tag{13}
\]

The dual phase \(q\) also lifts to a real \(C^1\) phase.  At a critical
point \(x_B\), write \(\beta=d\log b\).  Then

\[
 dB=\beta\otimes B,qquad
 C=-(d\sigma-\sigma\beta)\otimes\beta,                        \tag{14}
\]

and

\[
                         \|C_{x_B}\|
 \leq K_B\eta+K_B^2\epsilon.                                 \tag{15}
\]

The right side is increasing in the nonnegative scale bound, so choosing
the better of (13) and (15) proves (8).  Every
\(R\in\mathcal R_\mu\) has \(\|R\|\geq\mu\).  The reverse triangle
inequality at \(x_*\) proves (10).  This uses only first derivatives. \(\square\)

The proof is coordinate-free on \(M\): (11)--(14) are identities of bundle
maps.  It is also invariant under a constant reciprocal factor gauge
\(A\mapsto cA\), \(B\mapsto c^{-1}B\), since \(\sigma,C\), and the two
log-scale derivatives do not change.

## The saturated near-Parseval theorem

The lower spectral mass in Theorem 1 follows automatically when the local
curvature budget is saturated.

### Theorem 2 (robust saturated phase obstruction)

Let \(M=S^n\), \(n\geq2\), and let \((A_i,B_i)_{i=1}^n\) satisfy (3)--(7),
with parameters \(\epsilon_i,\eta_i,K_i\).  Put

\[
 C_i=-dA_i^*dB_i,
 \qquad E_i=K_i\eta_i+K_i^2\epsilon_i.                        \tag{15a}
\]

Suppose that at every \(x\)

\[
 \left\|\sum_{i=1}^n C_i(x)-I_{T_xM}\right\|\leq\xi          \tag{15b}
\]

and, for some \(\delta_i\geq0\), there are rank-one positive forms
\(R_i(x)=\lambda_i(x)\omega_i(x)\otimes\omega_i(x)\), with
\(\|\omega_i(x)\|=1\), such that

\[
                         \|C_i(x)-R_i(x)\|\leq\delta_i.        \tag{15c}
\]

No continuity of the choices \(R_i\) is required.  Set
\(\Delta=\sum_i\delta_i\).  Then, for every \(i\),

\[
                 \boxed{\xi+\Delta+\delta_i+E_i\geq1.}        \tag{15d}
\]

In particular, if \(\delta_i\leq\delta\) and \(E_i\leq E\), then

\[
                         \boxed{\xi+(n+1)\delta+E\geq1.}      \tag{15e}
\]

#### Proof

Equations (15b)--(15c) imply

\[
                  \left\|\sum_iR_i-I\right\|\leq\xi+\Delta.  \tag{15f}
\]

If \(\xi+\Delta\geq1\), (15d) is immediate.  Otherwise fix \(i\) and a
point \(x\).  Choose a unit vector \(v\in T_xM\) orthogonal to the at most
\(n-1\) covectors \(\omega_j\), \(j\ne i\).  From (15f),

\[
 1-\xi-\Delta
 \leq \left\langle\sum_jR_jv,v\right\rangle
 =\lambda_i\omega_i(v)^2
 \leq\lambda_i.                                               \tag{15g}
\]

Thus every \(R_i(x)\) has spectral mass at least
\(\mu=1-\xi-\Delta\).  Theorem 1 supplies a point where
\(\|C_i\|\leq E_i\), while (15c) gives
\(\mu\leq\|R_i\|\leq E_i+\delta_i\).  Rearrangement proves
(15d), and the common-bound version gives (15e). \(\square\)

This argument is stronger than merely using invertibility of
\(\sum_iR_i\).  Saturation by exactly \(n\) rank-one forms forces a lower
mass bound for each individual form; its phase critical point then forces
that same channel to become small.

At \(\epsilon=\xi=\delta_i=0\), this is the \(Q_3\), rank-one specialization
of the independently proved
[saturated-factor submersion
theorem](2026-09-04-saturated-factor-submersion-obstruction.md).  That exact
theorem is stronger in cone scope: it treats arbitrary three-dimensional
proper cones and mixed saturated rank profiles.  The present theorem makes
a different advance: for the smooth Lorentz boundary, it retains the phase
argument under explicitly quantified contact, curvature, and conditioning
errors.  It does not claim a robust version for arbitrary proper cones.

## Getting \(\eta\) from genuinely \(C^1\) data

The derivative hypothesis in (7) can be recovered quantitatively from a
small nonnegative defect and a modulus of continuity; no second derivative
is required.  Fix \(r_0\) below the normal radius of \(M\).  Let
\(\omega(r)\) be a uniform modulus for \(d\sigma\) along geodesics of
length at most \(r\), after parallel transport, and define

\[
 \bar\omega(r)={1\over r}\int_0^r\omega(t)\,dt,
 \qquad
 \eta_{C^1}(\epsilon)=
 \inf_{0<r\leq r_0}\left({\epsilon\over r}+\bar\omega(r)\right). \tag{16}
\]

### Lemma 3 (nonnegative \(C^1\) interpolation)

If \(0\leq\sigma\leq\epsilon\), then

\[
                         \|d\sigma\|\leq\eta_{C^1}(\epsilon). \tag{17}
\]

Indeed, at \(x\), choose the sign of a unit tangent \(v\) so that
\(d\sigma_x(v)=|d\sigma_x(v)|\), and integrate along the length-\(r\)
geodesic in direction \(v\).  The endpoint values differ by at most
\(\epsilon\), while the integrated derivative variation is at most
\(r\bar\omega(r)\).  Divide by \(r\) and optimize.

If \(d\sigma\) is \(H\)-Lipschitz with \(H>0\) and
\(\sqrt{2\epsilon/H}\leq r_0\), then

\[
 \omega(r)\leq Hr,qquad
 \eta_{C^1}(\epsilon)\leq\sqrt{2H\epsilon}.                   \tag{18}
\]

If \(H=0\), then \(d\sigma\) is parallel; it vanishes at an extremum of
\(\sigma\) and hence vanishes everywhere, so one may take \(\eta=0\).

Thus Theorem 1 gives the explicit threshold

\[
        \boxed{\delta+K\sqrt{2H\epsilon}+K^2\epsilon\geq\mu.} \tag{19}
\]

For a uniformly equicontinuous family of \(C^1\) defects,
\(\eta_{C^1}(\epsilon)\to0\) as \(\epsilon\to0\).  Equation (2) therefore
says that a convergent approximate factorization must escape through at
least one of four mechanisms: rank-one approximation error \(\delta\),
spectral-mass collapse \(\mu\downarrow0\), radial conditioning
\(K\uparrow\infty\), or deterioration of the \(C^1\) modulus.

## Corollary for an approximate ball slack factorization

Let \(M=S^{N-1}\), \(N\geq3\), and suppose globally labelled \(C^1\)
boundary factors

\[
 A_i,B_i:M\to\partial Q_3\setminus\{0\}
\]

satisfy

\[
 F(x,y)=\sum_{i=1}^k\langle A_i(x),B_i(y)\rangle,qquad
 0\leq F(x,x)\leq\epsilon.                                   \tag{20}
\]

For example, the second inequality follows on the contact diagonal from a
uniform \(\epsilon\)-approximation to the ball slack
\(1-\langle x,y\rangle\).  Lorentz self-duality makes every summand
nonnegative, so

\[
        0\leq\sigma_i(x)=\langle A_i(x),B_i(x)\rangle
        \leq\epsilon.                                         \tag{21}
\]

Apply Theorem 1 and Lemma 3 separately to each \(\sigma_i\).  If the
mixed channel

\[
                C_{i,x}=-dA_i(x)^*dB_i(x)                     \tag{22}
\]

is uniformly \(\delta_i\)-close to
\(\mathcal R_{\mu_i}(T_xM)\), then

\[
 \boxed{
 \delta_i+K_i\eta_{i,C^1}(\epsilon)+K_i^2\epsilon\geq\mu_i
 }
 \qquad\text{for every }i.                                   \tag{23}
\]

This is the robust analogue of the exact \(Q_3\) phase-integrability
obstruction.  In the exact case \(\epsilon=0\), every
\(\sigma_i\equiv0\), hence \(d\sigma_i=0\), and every channel has a point
where \(C_i=0\).  Thus no globally labelled collection of channels can be
everywhere rank-one positive with a nonzero spectral floor.

The nonzero-factor and derivative assumptions can be written in more
elementary conditioning terms.  On \(\partial Q_3\setminus\{0\}\),
\(\|A\|=\sqrt2\,a\).  Hence

\[
 \|A\|\geq m_A,\quad\|dA\|\leq L_A
 \quad\Longrightarrow\quad
 K_A\leq{L_A\over m_A},                                      \tag{24}
\]

Indeed, the two summands in
\(dA=da(1,p)+a(0,dp)\) are orthogonal, so
\(\|dA(u)\|^2=2|da(u)|^2+a^2\|dp(u)\|^2\).  The same argument applies to
\(B\).  One may therefore use

\[
 K_i\leq\min\left\{
 {L_{A,i}\over m_{A,i}},
 {L_{B,i}\over m_{B,i}}
 \right\}.                                                    \tag{25}
\]

This is the requested explicit error/conditioning tradeoff: quantitatively
nonzero boundary factors and bounded first derivatives turn phase
integrability into a lower bound on either channel error or rank-one
spectral degeneration.

## What the theorem does not say

1. It does not rule out arbitrary approximate \(Q_3\)-lifts.  It concerns
   globally labelled, nonzero, \(C^1\) boundary factor selections on the
   full contact sphere.
2. A bound only on the *sum* of the diagonal derivatives does not control
   the individual \(d\sigma_i\); cancellations are possible.  Formula
   (16), an individual derivative bound, or an equicontinuous family is
   essential.
3. Nonzero factor norms alone do not control \(K\).  A boundary factor may
   change radial scale rapidly.  The ratios in (25), or direct log-scale
   bounds, are genuine conditioning hypotheses.
4. Mere closeness to the set of rank-at-most-one forms is insufficient:
   the approximating form may have vanishing mass.  The floor \(\mu>0\) is
   essential.
5. The theorem does not require the channels to sum approximately to the
   sphere metric or use a saturated block count; Theorem 2 adds those
   hypotheses only to derive the spectral floor rather than assume it.
6. The conclusion is about unnormalized mixed-curvature bilinear forms.  It
   is not by itself an invariant condition-number lower bound for a KKT
   matrix under arbitrary cone reparameterizations.

## Literature boundary

Gouveia--Parrilo--Thomas established the relation between cone lifts and
slack factorizations in
[*Lifts of Convex Sets and Cone
Factorizations*](https://doi.org/10.1287/moor.1120.0575).  Their later work
on
[*Approximate Cone Factorizations and Lifts of
Polytopes*](https://arxiv.org/abs/1308.2162)
relates approximate slack factorizations to geometric approximations, but
does not impose globally smooth contact selections or derive a differential
phase obstruction.  Fawzi showed that second-order-cone rank can obstruct
SOC representations in
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://doi.org/10.1007/s10107-018-1233-0); that is an algebraic
factorization-rank argument rather than a robust contact-diagonal theorem.

The topological input is only covering-space lifting followed by the
extreme-value theorem and Fermat's critical-point argument.  More generally,
Tischler's theorem says that a compact manifold with a nowhere
vanishing closed one-form fibers over the circle; see the discussion and
references in
[*Euler Flows and Singular Geometric
Structures*](https://doi.org/10.1073/pnas.1902307116).  Here simple
connectivity gives the shorter proof: the circle-valued phase lifts to a
real function, which has an extremum.

The local exact antecedent is the
[saturated-factor submersion
theorem](2026-09-04-saturated-factor-submersion-obstruction.md), which turns
an exact saturated cone channel into a sphere-valued submersion.  Its
rank-one target is a circle and therefore has the same critical-phase
contradiction.  That theorem has no approximate conclusion; conversely,
the quantitative argument here relies on the explicit smooth circular
boundary of \(Q_3\).

A targeted search for combinations of approximate cone/slack
factorization, Lorentz boundary phases, smooth contact selections, and
quantitative critical-point stability found no theorem matching (2), (10),
or (23).  The proposed novelty is specifically the robust channelwise
error/conditioning inequality, not the standard lift--factorization
correspondence, approximate cone factorization framework, or critical-point
fact.  Novelty remains subject to specialist review.

The search also included Aubrun--La Piana--Müller-Hermes,
[*Factorization through Lorentz
cones*](https://arxiv.org/abs/2606.27825), which studies algebraic
factorization of positive maps through direct sums of Lorentz cones.  It
does not study globally \(C^1\) contact phases or a quantitative mixed-
curvature dropout.

## Audit checklist

- The proof uses \(C^1\), not hidden second derivatives; (18) is an optional
  stronger regularity corollary.
- Both primal and dual phase critical points were checked, giving the
  minimum in (6).
- The tensor order in (12) and (14) was checked against
  \(C(u,v)=-\langle dA(u),dB(v)\rangle\).
- The distance statement uses the operator norm of general bilinear forms,
  so it remains valid when \(C\) is nonsymmetric.
- The passage from (20) to (21) uses blockwise cone nonnegativity, not an
  unjustified derivative decomposition.
- The scope excludes zero boundary factors, uncontrolled radial gauges,
  vanishing rank-one mass, and arbitrary nonsmooth approximate lifts.
- An independent hostile audit attacked the boundary restriction, tensor
  order, minimum radial gauge, \(C^1\) interpolation constant, and the
  spectral-floor inference in Theorem 2.  It found the core theorem sound.
  The audit prompted the explicit no-boundary hypothesis, the boundary-map
  declaration in (20), the \(H=0\) case, and the sharper constant in
  (24)--(25).
