# Robust rank-\(r\) phase obstruction from forbidden sphere submersions

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High under the stated global-boundary and one-sided-derivative hypotheses

## Main theorem

Let \(1\leq r<n\), let \(K\subset V\) be a proper cone of dimension
\(m=r+2\), and choose \(\ell\in\operatorname{int}K^*\).  Its normalized
base

\[
 D=\{z\in K:\ell(z)=1\}
\]

is a compact \((r+1)\)-dimensional convex body.  Assume that
\(J=\partial D\) is \(C^1\).  Let

\[
 A:S^n\to\partial K\setminus\{0\},\qquad
 B:S^n\to\partial K^*\setminus\{0\}                           \tag{1}
\]

be globally \(C^1\), and define

\[
 \begin{aligned}
 \sigma(x)&=\langle A(x),B(x)\rangle,\\
 C_x(u,v)&=-\langle dA_xu,dB_xv\rangle,\\
 g_B(x)(v)&=\langle A(x),dB_xv\rangle .
 \end{aligned}                                                \tag{2}
\]

Write

\[
 a=\ell(A)>0,\qquad p={A\over a}:S^n\to J,
 \qquad K_A=\sup_{S^n}\|d\log a\|,\qquad
 \eta_B=\sup_{S^n}\|g_B\|.                                  \tag{3}
\]

The Riemannian metric identifies bilinear forms with operators
\(T_xS^n\to T_x^*S^n\).  Let \(s_j(T)\) denote singular values in decreasing
order, and let

\[
 \mathcal S_{r,\mu}(T_xS^n)=
 \{R:\operatorname{rank}R=r,\ s_r(R)\geq\mu\}.               \tag{4}
\]

### Theorem 1 (one-sided robust submersion obstruction)

If

\[
                    (n,r)\notin\{(3,2),(7,4),(15,8)\},        \tag{5}
\]

then there is \(x_*\in S^n\) such that

\[
                         s_r(C_{x_*})\leq K_A\eta_B.           \tag{6}
\]

Consequently, if every \(C_x\) is within operator norm \(\delta\) of some
\(R_x\in\mathcal S_{r,\mu}(T_xS^n)\), then

\[
                         \boxed{\delta+K_A\eta_B\geq\mu.}     \tag{7}
\]

The conclusion also holds in one of the three dimensions in (5) whenever
the particular normalized ray map \(p\) has a critical point.  What fails
in those dimensions is only the universal topological guarantee: the
complex, quaternionic, and octonionic Hopf maps are submersions for

\[
                      (n,r)=(3,2),(7,4),(15,8).               \tag{8}
\]

### Proof

Radial projection from an interior point of \(D\) gives a \(C^1\)
diffeomorphism \(J\cong S^r\).  If \(p\) had rank \(r\) everywhere, its
composition with this diffeomorphism would be a \(C^1\) submersion
\(S^n\to S^r\).  The Browder--Serre classification rules this out outside
(8).  Hence there is \(x_*\) with

\[
                           \operatorname{rank}dp_{x_*}\leq r-1. \tag{9}
\]

Put \(\alpha=d\log a\).  Differentiating \(A=ap\) gives the coordinate-free
bundle identity

\[
                           dA=\alpha\otimes A+a\,dp.           \tag{10}
\]

At \(x_*\), split the mixed channel as

\[
 \begin{aligned}
 C&=L+E,\\
 L(u,v)&=-a\langle dp(u),dB(v)\rangle,\\
 E(u,v)&=-\alpha(u)\langle A,dB(v)\rangle
        =-(\alpha\otimes g_B)(u,v).
 \end{aligned}                                                \tag{11}
\]

Equation (9) gives \(\operatorname{rank}L\leq r-1\), while

\[
                              \|E\|\leq K_A\eta_B.             \tag{12}
\]

The Eckart--Young singular-value formula, or its elementary min--max
proof, now gives

\[
 s_r(C)\leq\operatorname{dist}
       (C,\{T:\operatorname{rank}T\leq r-1\})
       \leq\|C-L\|\leq K_A\eta_B,                             \tag{13}
\]

where the first displayed inequality is in fact equality.  If
\(\|C-R\|\leq\delta\), singular-value perturbation gives
\(\mu\leq s_r(R)\leq s_r(C)+\delta\).  Combining with (13) proves
(7). \(\square\)

Thus a locally capacity-saturating \((r+2)\)-dimensional block cannot keep
an everywhere well-conditioned rank-\(r\) mixed channel across a forbidden
contact sphere unless its one-sided contact derivative or radial gauge
becomes large.

## Symmetric primal--dual version

Assume additionally that a normalized base of \(K^*\) has \(C^1\) boundary.
Choose \(\ell^*\in\operatorname{int}K\), and write

\[
 b=\ell^*(B),\qquad q={B\over b},\qquad
 K_B=\sup\|d\log b\|,qquad
 g_A=dA^*B,qquad \eta_A=\sup\|g_A\|.                         \tag{14}
\]

The dual normalized map \(q:S^n\to S^r\) also has a critical point outside
the Hopf pairs.  There

\[
 C=-b\,dA^*dq-g_A\otimes d\log b,                             \tag{15}
\]

so the same proof gives

\[
 \boxed{
 \delta+\min\{K_A\eta_B,K_B\eta_A\}\geq\mu.
 }                                                            \tag{16}
\]

The two critical points need not coincide.  Taking the minimum is valid
because each side independently supplies a point where \(s_r(C)\) has the
corresponding upper bound.

## Deriving the one-sided derivative from \(C^1\) contact data

The parameter \(\eta_B\) is a genuine diagonal *partial* derivative:

\[
 g_B(x)=d_y\langle A(x),B(y)\rangle\big|_{y=x}.                \tag{17}
\]

It follows quantitatively from contact defect plus a uniform \(C^1\)
modulus.  Put

\[
 F(x,y)=\langle A(x),B(y)\rangle\geq0.                        \tag{18}
\]

Fix \(r_0\) below the injectivity radius of \(S^n\).  Suppose

\[
                         0\leq F(x,x)\leq\epsilon              \tag{19}
\]

and let \(\omega_B(t)\) be a uniform modulus of continuity, in the second
variable, for \(d_yF(x,y)\) along geodesics of length at most \(t\), with
the first variable held fixed and covectors compared by parallel transport
along the geodesic.  Define

\[
 \bar\omega_B(s)={1\over s}\int_0^s\omega_B(t)\,dt,
 \qquad
 \eta_{B,C^1}(\epsilon)=
 \inf_{0<s\leq r_0}
 \left({\epsilon\over s}+\bar\omega_B(s)\right).              \tag{20}
\]

### Lemma 2 (one-sided near-contact interpolation)

Under (18)--(20),

\[
                              \eta_B\leq\eta_{B,C^1}(\epsilon). \tag{21}
\]

To prove this, fix \(x\), choose the sign of a unit \(v\in T_xS^n\) so
that \(g_B(x)(v)=|g_B(x)(v)|\), and move the second argument from \(x\) in
direction \(-v\).  Nonnegativity of \(F(x,\cdot)\), its starting value at
most \(\epsilon\), and integration of the derivative variation give

\[
        0\leq F(x,\exp_x(-sv))
        \leq \epsilon-s|g_B(x)(v)|+s\bar\omega_B(s).
\]

Rearrange and optimize over \(s\).  The same statement holds for
\(\eta_A\) using the first variable.

If the two partial derivatives are \(H_A,H_B\)-Lipschitz with
\(H_A,H_B>0\), and
\(\sqrt{2\epsilon/H_A},\sqrt{2\epsilon/H_B}\leq r_0\), then

\[
 \eta_A\leq\sqrt{2H_A\epsilon},\qquad
 \eta_B\leq\sqrt{2H_B\epsilon}.                              \tag{22}
\]

The symmetric threshold (16) becomes

\[
 \boxed{
 \delta+\min\{K_A\sqrt{2H_B\epsilon},
                K_B\sqrt{2H_A\epsilon}\}\geq\mu.
 }                                                            \tag{23}
\]

For equicontinuous \(C^1\) families, the right side of (20) tends to zero
with \(\epsilon\).  Therefore a sequence of approximate saturated channels
on a forbidden sphere must escape by rank-\(r\) approximation error,
singular-value collapse, radial ill-conditioning, or deterioration of a
one-sided \(C^1\) modulus.

## Relation to the rank-one \(Q_3\) formula

The rank-one Lorentz theorem required only the total diagonal derivative
\(d\sigma\), where \(\sigma(x)=F(x,x)\).  This simplification is special to
\(r=1\).  At a critical circle phase, \(dp=0\), so

\[
 dA^*B=\sigma\,d\log a,qquad
 g_B=d\sigma-\sigma\,d\log a.                                \tag{24}
\]

At that phase-critical point,
\(\|g_B\|\leq\eta+K_A\epsilon\).  Repeating (11)--(13) with this
pointwise bound recovers

\[
                 \delta+K_A\eta+K_A^2\epsilon\geq\mu.        \tag{25}
\]

For \(r>1\), a critical point gives only \(\operatorname{rank}dp<r\), not
\(dp=0\).  In general

\[
 dA^*B=\sigma\,d\log a+a\,dp^*B,qquad
 g_B=d\sigma-dA^*B.                                          \tag{26}
\]

The tangential term \(a\,dp^*B\) can be large and can cancel \(g_B\) in
the total derivative.  Therefore a bound only on \(d\sigma\) does **not**
imply (7) for rank \(r>1\).  One must control a one-sided partial derivative
as in (17), its \(C^1\) modulus as in (20), or an equivalent normal-
alignment error.

For example, if \(\|d\sigma\|\leq\eta\) and

\[
                         \|a\,dp^*B\|\leq\tau,                \tag{27}
\]

then (26) gives

\[
 \eta_B\leq\eta+K_A\epsilon+\tau,
\]

and Theorem 1 yields the directly analogous threshold

\[
 \boxed{
 \delta+K_A\eta+K_A^2\epsilon+K_A\tau\geq\mu.
 }                                                            \tag{28}
\]

The extra \(\tau\) is not a proof artifact: it records the tangential
normal-misalignment channel that vanishes automatically only in the exact
rank-one phase argument.

## Capacity-saturated product corollary

Suppose an approximate contact factorization on \(S^n\) satisfies the
hypotheses of Theorem 1 blockwise: it has globally labelled, nonzero
\(C^1\) boundary factors through proper cones \(K_i\) of dimensions
\(r_i+2\), each normalized primal base boundary is \(C^1\), and the local
capacity budget is saturated:

\[
                              \sum_i r_i=n.                   \tag{29}
\]

For every block with \(0<r_i<n\) whose dimension pair \((n,r_i)\) is not
one of the Hopf pairs, Theorem 1 applies independently.  Thus if its mixed
channel is uniformly \(\delta_i\)-close to rank-\(r_i\) forms with
\(s_{r_i}\geq\mu_i\), then

\[
                   \delta_i+K_{A,i}\eta_{B,i}\geq\mu_i.       \tag{30}
\]

Even in the Hopf source dimensions \(n=3,7,15\), the only proper target
dimensions allowed by topology are respectively \(2,4,8\).  Those values
cannot sum to \(3,7,15\).  Hence every saturated rank profile containing at
least two positive blocks has at least one forbidden block and therefore
at least one channel satisfying (30).  A single full-capacity block
\(r_i=n\) is not obstructed.

Under common bounds \(\delta_i\leq\delta\),
\(K_{A,i}\leq K\), \(\eta_{B,i}\leq\eta_\partial\), and
\(\mu_i\geq\mu\), every nontrivial saturated product profile obeys

\[
                         \boxed{\delta+K\eta_\partial\geq\mu.} \tag{31}
\]

This is a robust blockwise counterpart of the exact theorem that a globally
smooth saturated product must consist of one full-capacity block.

## Scope and literature boundary

This theorem assumes globally labelled, nonzero \(C^1\) boundary factors,
a \(C^1\) normalized cone-base boundary, controlled radial scale, and a
one-sided contact derivative or its modulus.  It does not assert that an
arbitrary approximate lift supplies those selections.  It does not rule out
nonsmooth norm trees, cone-coordinate chart changes, zero factors,
uncontrolled radial gauges, polyhedral approximations, or a single block of
full curvature capacity.  The conclusion concerns mixed-channel singular
values, not an invariant KKT condition number under arbitrary cone
reparameterization.

The exact factor-to-submersion bridge is proved in
[*Saturated cone factors force sphere-to-sphere
submersions*](2026-09-04-saturated-factor-submersion-obstruction.md).
The sphere-pair classification and its primary sources are recorded in
[*Sphere submersions force a strict curvature-capacity
gap*](2026-09-04-sphere-submersion-curvature-gap.md).  In particular, it
uses Browder's theorem on fibers of sphere fibrations, the Serre spectral
sequence, Ehresmann's theorem, and the three Hopf constructions.  General
cone lifts and slack factorizations are related by
[Gouveia--Parrilo--Thomas](https://doi.org/10.1287/moor.1120.0575), while
their
[*Approximate Cone Factorizations and Lifts of
Polytopes*](https://arxiv.org/abs/1308.2162)
does not impose this global contact regularity or derive a singular-value
phase threshold.

A targeted search found no robust theorem combining forbidden sphere
submersions with approximate cone-contact factorization and the explicit
inequalities (7), (23), or (28).  The topology, singular-value perturbation,
and interpolation ingredients are classical; the candidate contribution is
their quantitative synthesis for saturated cone curvature channels.
Novelty remains subject to specialist review.

## Audit checklist

- The rank defect is in the normalized ray derivative \(dp\), while radial
  motion is isolated in the explicit rank-one error term in (11).
- The proof bounds the \(r\)-th singular value, not the full operator norm.
- No positivity or symmetry of \(C\) or its rank-\(r\) approximant is used.
- The Hopf pairs are exceptions, not impossibility claims.
- The one-sided derivative in (17) is stronger than the total diagonal
  derivative; (26) records why that strengthening is necessary.
- The product corollary excludes the unobstructed single full-capacity block.
- An independent hostile audit verified the normalized-base radial
  diffeomorphism, Browder--Serre dimension input, tensor order and rank in
  (11), Eckart--Young and perturbation constants, symmetric minimum,
  interpolation signs, rank-one specialization, and saturated-profile
  arithmetic.  It also confirmed that \(\partial K^*\) needs to be \(C^1\)
  only for the optional dual improvement.
