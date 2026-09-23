# Barrier-independent central-path conditioning: the sublevel chord law

Date: 2026-09-02
Status: proved and adversarially audited (independent referee audit of the
LP dichotomy found no errors in the main theorems; its repairs are applied
here; the chord-law generalization was developed after that audit and
self-checked plus numerically verified in six regimes/families).

## Summary

Every conditioning result previously in this repository fixes the
logarithmic barrier and varies coordinates, congruences, or access models.
This note varies the barrier itself and answers the question completely, up
to instance constants: **the condition number of the reduced central-path
Hessian is governed by a purely geometric quantity — the diameter of the
objective sublevel set at the current duality gap — for every
self-concordant barrier, and the canonical log/log-det barrier already
achieves that floor.**

Main statements, for a compact convex feasible region \(P\), objective
\(c\), gap \(g=c^\top x-\mathrm{OPT}\), and sublevel diameter
\(D(g)=\operatorname{diam}\{y\in P:c^\top y\le\mathrm{OPT}+g\}\):

1. **Chord-law floor (Theorem A).** For every \(\nu\)-self-concordant
   barrier \(F\) for \(P\) and every exact \(F\)-central point with gap
   \(g\),
   \[
     \kappa_{\rm red}\;\ge\;
     \left(\frac{D(g)\,\|\Pi_Vc\|_2}{2(\nu+2\sqrt\nu)\,g}\right)^{\!2}.
   \]
   No threshold on \(\mu\), no nondegeneracy, no strict-complementarity
   assumption, any convex \(P\) (LP, SDP, anything).
2. **Canonical achievability (Theorem B).** For LP with the log barrier and
   SDP with the log-det barrier, \(\kappa_{\rm red}\le(SnD(g)/g)^2\) at
   gap \(g\) on the central-path tail. Hence the canonical barrier is
   within a \(\mu\)-independent instance factor of the best possible
   barrier at every gap: **barrier redesign can never improve central-path
   conditioning by more than a constant.**
3. **Regime trichotomy (Corollary C).** \(D(g)\) is the (Hölder) sharpness
   modulus of the optimization problem, so
   \(\kappa_{\rm red}\asymp(D(g)/g)^2\) turns error-bound exponents into
   conditioning laws:
   - optimal face of dimension \(\ge1\): \(D(g)=\Theta(1)\), so
     \(\kappa=\Theta(1/g^2)=\Theta(1/\mu^2)\) for **every** barrier
     (the original dichotomy Theorem 1 below, now with a two-line proof);
   - LP with a unique optimum (nondegenerate **or degenerate** vertex):
     weak sharp minimum, \(D(g)=\Theta(g)\), so the log barrier keeps
     \(\kappa=O(1)\);
   - curved boundary / generic unique nondegenerate SDP optimum:
     quadratic growth, \(D(g)=\Theta(\sqrt g)\), so
     \(\kappa=\Theta(1/g)=\Theta(1/\mu)\) for the canonical barrier and
     \(\Omega(1/g)\) for every barrier.

All three regimes are verified numerically, with the floor constants
observed to be exactly tight in the leading families.

## Setup

\(P\subset\mathbb R^n\) compact convex, \(\operatorname{aff}(P)=x^0+V\),
relative interior \(P^\circ\neq\emptyset\); objective \(c\) with
\(\Pi_Vc\neq0\) (\(c\) nonconstant on \(P\)); \(\mathrm{OPT}=\min_Pc^\top
x\), optimal face \(\Phi\). For standard-form LP,
\(P=\{x:Ax=b,x\ge0\}\), \(V=\ker A\), \(P^\circ=\{x\in P:x>0\}\).

\(F\) is any \(\nu\)-self-concordant barrier with
\(\operatorname{dom}F=P^\circ\) (relatively open in the slice; Hessians are
bilinear forms on \(V\); \(Z\) is an orthonormal basis of \(V\)). Since
\(P\) is bounded, \(F''\succ0\) on \(V\) and the central point
\(x_F(\mu)=\arg\min_{P^\circ}c^\top x+\mu F(x)\) exists and is unique.
\(\kappa_{\rm red}=\kappa(Z^\top F''(x_F(\mu))Z)\). Gap
\(g=g_F(\mu)=c^\top x_F(\mu)-\mathrm{OPT}\in(0,\nu\mu]\) (proof in
Theorem A, Step 0).

Sublevel sets and chord functions:
\[
  L(g)=\{y\in P:\ c^\top y\le\mathrm{OPT}+g\},\qquad
  D(g)=\operatorname{diam}L(g),\qquad
  \ell(x)=\sup_{y\in L(c^\top x-\mathrm{OPT})}\|y-x\|_2 .
\]
For a central \(x\) with gap \(g\): \(x\in L(g)\), so
\(D(g)/2\le\ell(x)\le D(g)\).

## Classical facts used

Verified against primary sources (Nesterov 2004 [N04] / 2018 [N18],
Nemirovski's IPM notes, Renegar 2001) by a dedicated fact audit:

- (F1) Dikin containment ([N04] Thm 4.1.5(1)): \(\|y-x\|_x<1\Rightarrow
  y\in\operatorname{dom}F\), for standard self-concordant \(F\) (closed
  function, open domain — the barrier property, definitional here).
- (F2) Semiboundedness ([N04] Thm 4.2.4): \(\langle
  F'(x),y-x\rangle\le\nu\) for \(y\in\overline{\operatorname{dom}F}\).
- (F3) Asymmetric containment ([N04] Thm 4.2.5, [N18] Thm 5.3.8 — the
  two-point theorem, not the analytic-center corollary): if
  \(y\in\overline{\operatorname{dom}F}\) and \(\langle
  F'(x),y-x\rangle\ge0\) then \(\|y-x\|_x\le\nu+2\sqrt\nu\).
- (F4) Affine restriction preserves the barrier property with parameter
  \(\le\nu\) ([N04] Thm 4.2.3).
- (F5) Central gap bound \(g\le\nu\mu\) ([N04] Thm 4.2.7); reproved
  inline.
- \(\nu\ge1\) for any barrier on a proper domain ([N18] Cor 5.4.1); used
  silently in constant clean-ups.

## Theorem A (sublevel chord law: floor for every barrier)

For every \(\nu\)-self-concordant barrier \(F\) for \(P^\circ\), every
\(\mu>0\), at \(x=x_F(\mu)\) with gap \(g\):

(a) \(\displaystyle\lambda_{\max}(Z^\top F''(x)Z)\ \ge\
\frac{\|\Pi_Vc\|_2^2}{g^2}\);

(b) \(\displaystyle\lambda_{\min}(Z^\top F''(x)Z)\ \le\
\frac{(\nu+2\sqrt\nu)^2}{\ell(x)^2}\);

(c) \(\displaystyle\kappa_{\rm red}\ \ge\
\left(\frac{\ell(x)\|\Pi_Vc\|_2}{(\nu+2\sqrt\nu)\,g}\right)^{\!2}\ \ge\
\left(\frac{D(g)\|\Pi_Vc\|_2}{2(\nu+2\sqrt\nu)\,g}\right)^{\!2}\),
and since \(g\le\nu\mu\) and \(D\) is nondecreasing, also
\(\displaystyle\kappa_{\rm red}\ \ge\
\left(\frac{D(g)\|\Pi_Vc\|_2}{2(\nu+2\sqrt\nu)\,\nu\mu}\right)^{\!2}.\)

### Proof

**Step 0 (gap).** Optimality gives \(c+\mu F'(x)\perp V\). For
\(y\in\overline{P^\circ}=P\), \(y-x\in V\) and (F2) give
\(c^\top(x-y)=\mu\langle F'(x),y-x\rangle\le\mu\nu\); take \(y\in\Phi\) to
get \(g\le\nu\mu\). If \(g=0\) then \(x\in\Phi\cap\operatorname{relint}P\),
which forces \(c\) constant on \(P\), excluded; so \(g>0\).

**(a).** Let \(\hat h=-\Pi_Vc/\|\Pi_Vc\|\) and \(t^*=g/\|\Pi_Vc\|\). Then
\(c^\top(x+t^*\hat h)=\mathrm{OPT}\) and \(x+t^*\hat h\in
x^0+V\). If \(x+t^*\hat h\in P^\circ\) it would be a relative-interior
minimizer of the linear \(c\), forcing \(c\) constant on \(P\); so
\(x+t^*\hat h\notin\operatorname{dom}F\). By (F1),
\(\|t^*\hat h\|_x\ge1\), i.e.
\(\langle F''(x)\hat h,\hat h\rangle\ge1/(t^*)^2=\|\Pi_Vc\|^2/g^2\).

**(b).** Let \(y\in L(g)\) (allowed in the closure by (F3)). Then
\(y-x\in V\) and
\(\langle F'(x),y-x\rangle=-\tfrac1\mu\,c^\top(y-x)\ge0\) since
\(c^\top y\le c^\top x\). By (F3), \(\|y-x\|_x\le\nu+2\sqrt\nu\), so for
the unit vector \(v=(y-x)/\|y-x\|_2\),
\(\langle F''(x)v,v\rangle\le(\nu+2\sqrt\nu)^2/\|y-x\|_2^2\). Take the
supremum over \(y\).

**(c).** Divide, then use \(\ell(x)\ge D(g)/2\) and \(g\le\nu\mu\).
\(\square\)

Note what is *not* assumed: no strict complementarity, no polyhedrality,
no face-dimension hypothesis, no \(\mu\) threshold. The floor is active at
every point of every central path.

## Theorem B (the canonical barrier achieves the floor)

**(LP).** Let \(P=\{x:Ax=b,x\ge0\}\) be compact with \(P^\circ\ne\emptyset\)
and let \(x(\mu)\) be the log-barrier central path
(\(F=-\sum_j\log x_j\), \(x_j(\mu)s_j(\mu)=\mu\), \(g=n\mu\)). Let
\(S=\sup_{0<\mu\le\bar\mu}\max_j s_j(\mu)<\infty\) (finite on any tail by
central-path convergence; McLinden 1980, Megiddo 1988). Then for
\(0<\mu\le\bar\mu\):
\[
  \lambda_{\min}\ \ge\ \frac1{\ell(x(\mu))^2},\qquad
  \lambda_{\max}\ \le\ \frac{S^2}{\mu^2}=\frac{S^2n^2}{g^2},\qquad
  \kappa_{\rm red}\ \le\ \Big(\frac{S\,n\,D(g)}{g}\Big)^{\!2}.
\]

**(SDP).** Same statement for \(\min\langle C,X\rangle\),
\(\mathcal A(X)=b\), \(X\succeq0\), compact and strictly feasible, with
\(F=-\log\det\), \(S(\mu)=\mu X(\mu)^{-1}\), \(g=r\mu\) (\(r\) the block
size), \(S=\sup_{0<\mu\le\bar\mu}\|S(\mu)\|_2<\infty\), and Frobenius
geometry.

### Proof

**\(\lambda_{\min}\) (the chord converse).** Take any unit \(h\in V\),
signed so that \(c^\top h\le0\). Since \(P\) is compact, the ray
\(x+th\) exits \(P\): for LP, at
\(t_{\rm exit}=\min\{x_j/|h_j|:h_j<0\}\) (a negative component exists,
else the ray stays feasible forever); for SDP, at
\(t_{\rm exit}=1/\lambda_{\max}(-X^{-1/2}HX^{-1/2})\), which is finite for
the same reason. The exit point \(y=x+t_{\rm exit}h\) lies in \(P\) and has
\(c^\top y\le c^\top x\), so it is a sublevel point:
\(t_{\rm exit}\le\ell(x)\). For the log barrier,
\(\langle F''h,h\rangle=\sum_j(h_j/x_j)^2\ge\max_j(h_j/x_j)^2
\ge1/t_{\rm exit}^2\ge1/\ell(x)^2\); for log-det,
\(\langle F''H,H\rangle=\|X^{-1/2}HX^{-1/2}\|_F^2
\ge\lambda_{\max}(-X^{-1/2}HX^{-1/2})^2=1/t_{\rm exit}^2\ge1/\ell(x)^2\).
The form is even in \(h\), so this bounds \(\lambda_{\min}\).

**\(\lambda_{\max}\).** \(x_j(\mu)=\mu/s_j(\mu)\ge\mu/S\) (resp.
\(\lambda_j(X)=\mu/\lambda_j(S)\ge\mu/S\)), so
\(\langle F''h,h\rangle\le S^2/\mu^2\) on unit vectors. Combine with
\(\ell(x)\le D(g)\) and \(\mu=g/n\) (resp. \(g/r\)). \(\square\)

## Theorem B′ (universal \(\lambda_{\min}\) rigidity)

The chord converse in Theorem B is not special to the log barrier: for
**every** \(\nu\)-self-concordant barrier \(F\) for \(P^\circ\) and every
\(x\in P^\circ\) (central or not),
\[
  \lambda_{\min}(Z^\top F''(x)Z)\ \ge\ \frac1{\ell(x)^2}.
\]
Proof: for unit \(h\in V\) with the sign chosen so \(c^\top h\le0\), the
ray \(x+th\) exits \(\operatorname{dom}F=P^\circ\) at some finite
\(t_{\rm exit}\) (compactness), the exit point is a sublevel point, so
\(t_{\rm exit}\le\ell(x)\); and by Dikin containment (F1), the exit point
cannot lie in the open unit Dikin ball, so
\(\langle F''(x)h,h\rangle\ge1/t_{\rm exit}^2\ge1/\ell(x)^2\). The form
is even in \(h\). \(\square\)

Combined with Theorem A(b), at every central point
\[
  \frac1{\ell(x)^2}\ \le\ \lambda_{\min}\ \le\
  \frac{(\nu+2\sqrt\nu)^2}{\ell(x)^2}:
\]
the flat edge of the central-path spectrum is pinned to the sublevel
chord for every barrier — it is geometry, not design. Only
\(\lambda_{\max}\) is barrier-dependent, it has the universal floor
A(a), and by Theorem B the canonical barrier attains that floor up to
instance constants. This is the cleanest formulation of why barrier
design cannot help.

## Theorem W (width-spectrum rigidity: the whole spectrum is geometry)

The edge results extend to every eigenvalue. At a central point \(x\)
with gap \(g\), for a unit \(h\in V\) let \(t_{\rm exit}(h)\) be the exit
time of the ray \(x+th\) from \(P^\circ\) with the sign of \(h\) chosen
so \(c^\top h\le0\) (so the exit point is a sublevel point, and
\(t_{\rm exit}(h)\le\ell(x)\)). Define the two width profiles of the
sublevel geometry seen from \(x\) (\(d=\dim V\), eigenvalues ascending):
\[
  w_j^-(x)=\inf_{\substack{W\subseteq V\\ \operatorname{codim}W=j-1}}
  \ \sup_{h\in W,\|h\|=1}t_{\rm exit}(h),\qquad
  w_j^+(x)=\sup_{\substack{S\subseteq V\\ \dim S=j}}
  \ \inf_{h\in S,\|h\|=1}t_{\rm exit}(h)
\]
(inf/sup rather than min/max: \(t_{\rm exit}\) is discontinuous across
the equator \(\{c^\top h=0\}\), where either sign qualifies — fix any
convention there; every step below is a pointwise inequality plus
inf/sup passage, so attainment is not needed, and
\(t_{\rm exit}\in(0,\ell(x)]\) always).
Then for **every** \(\nu\)-self-concordant barrier,
\[
  \frac1{w_j^-(x)^2}\ \le\ \lambda_j\big(Z^\top F''(x)Z\big)\ \le\
  \frac{(\nu+2\sqrt\nu)^2}{w_j^+(x)^2},\qquad j=1,\dots,d.
\]
Proof: Courant--Fischer twice. Lower:
\(\lambda_j=\max_{\operatorname{codim}W=j-1}\min_{h\in W}\langle
F''h,h\rangle\ge\max_W\min_{h\in W}t_{\rm exit}(h)^{-2}
=1/(w_j^-)^2\) by Dikin (F1), which needs no centrality. Upper:
\(\lambda_j=\min_{\dim S=j}\max_{h\in S}\langle F''h,h\rangle\), and for
each unit \(h\) the sublevel exit point \(y=x+t_{\rm exit}(h)h\) has
\(\langle F'(x),y-x\rangle=-c^\top(y-x)/\mu\ge0\), so (F3) gives
\(\langle F''h,h\rangle\le(\nu+2\sqrt\nu)^2/t_{\rm exit}(h)^2\); minimax
over \(S\) yields the claim (this half uses centrality). \(\square\)

Consequences: (i) Theorem A(a,b) and Theorem B′ are the \(j=d\) and
\(j=1\) cases — for A(b) via the bridge \(w_1^+\ge\ell(x)\): for any
sublevel point \(y\), the direction \(h=(y-x)/\|y-x\|\) has
\(c^\top h\le0\) and \(t_{\rm exit}(h)\ge\|y-x\|\), because the segment
from a relative-interior point to any point of a convex set lies in the
relative interior except possibly its endpoint, so
\([x,y)\subset P^\circ\); and \(w_j^+\le w_j^-\) holds by the
standard dimension count (a \(\dim\)-\(j\) subspace \(S\) and a
codim-\((j-1)\) subspace \(W\) intersect in a unit vector \(h_0\), so
\(\inf_S t\le t(h_0)\le\sup_W t\)); (ii) the *entire* spectral profile — cluster structure,
intra-cluster spread, effective spectral dimension, hence the
classical Krylov solve cost (for the quantum polynomial route the
width profile matters differently: see the companion note's Theorem Q,
where off-spectrum boundedness keeps a \(\kappa\)-scale cost for
plain block-encodings and \(\sqrt\kappa\) under factor access, even
on clustered widths) — of every barrier's reduced
central Hessian is pinned, up to \((\nu+2\sqrt\nu)^2\) and the
\(w^+_j\le w^-_j\) width gap, to the chord-width profile of the sublevel
body. Barrier design cannot reshape the spectrum, only shift it within
the \(\nu\)-window; instances like adlittle (single 9-decade spread, see
the Netlib survey note) have that spread *because their sublevel bodies
have geometrically spread widths*, and no barrier can fix it. For
ellipsoidal sublevel geometry both widths coincide with the semiaxis
profile and the sandwich is tight up to \((\nu+2\sqrt\nu)^2\).

For every \(\nu\)-self-concordant barrier \(F\) for the same LP (or SDP)
and any two central points of \(F\) and of the canonical barrier at equal
gap \(g\le g(\bar\mu)\):
\[
  \kappa_{\rm red}^{\log}(g)\ \le\
  \left(\frac{2\,S\,n\,(\nu+2\sqrt\nu)}{\|\Pi_Vc\|_2}\right)^{\!2}
  \kappa_{\rm red}^{F}(g).
\]
So no self-concordant barrier improves reduced central-path conditioning
over the canonical one by more than a \(\mu\)-independent instance factor,
in any regime. (The comparison is gap-matched, which is the natural
parameterization; different barriers traverse gaps at different \(\mu\).)

## Corollary C (regimes: error-bound exponents become conditioning laws)

\(D(g)\) is exactly the diameter modulus of the problem's Hölder error
bound: if \(\operatorname{dist}(y,\Phi)\le\gamma^{-1}(c^\top
y-\mathrm{OPT})^\theta\) on \(P\), then
\(D(g)\le\operatorname{diam}\Phi+2\gamma^{-1}g^\theta\), and conversely
\(D(g)\ge\) both \(\operatorname{diam}\Phi\) and \(g/\|\Pi_Vc\|\).

1. **Positive-dimensional optimal face** (\(\dim\Phi\ge1\)):
   \(D(g)\ge\operatorname{diam}\Phi>0\), so Theorem A gives, for **every**
   \(\nu\)-self-concordant barrier and every \(\mu\),
   \[
     \kappa_{\rm red}\ \ge\
     \left(\frac{\operatorname{diam}\Phi\cdot\|\Pi_Vc\|_2}
     {2(\nu+2\sqrt\nu)\,\nu\,\mu}\right)^{\!2}
     =\Omega\!\left(\frac1{\nu^4\mu^2}\right),
   \]
   and Theorem B shows the log barrier matches \(\Theta(1/\mu^2)\) (LP
   error bound: \(\theta=1\) by Burke--Ferris weak sharp minima, so
   \(D(g)=\Theta(1)\) here and \(\kappa^{\log}=O(1/g^2)\)). This is the
   original barrier-independence theorem of this note, now for arbitrary
   compact convex \(P\) (SDP included) with a two-line proof and no
   Goldman--Tucker input.
2. **LP with a unique optimal solution** \(x^*\) — including degenerate
   vertices: the LP solution set is a weak sharp minimum (Burke--Ferris
   1993, Thm 3.5; Mangasarian--Meyer 1979), so
   \(\|y-x^*\|\le\gamma^{-1}(c^\top y-\mathrm{OPT})\) on \(P\) and
   \(D(g)\le2g/\gamma\). Theorem B:
   \(\kappa_{\rm red}^{\log}\le(2Sn/\gamma)^2=O(1)\) on the tail.
   (The explicit nondegenerate-vertex limit constant is Theorem 2 below;
   the degenerate-vertex case is confirmed numerically, \(\kappa\to1.2\)
   on a \(|{\rm supp}\,x^*|<m\) instance.)
3. **Curved boundary / generic SDP**: with quadratic growth
   (\(\theta=1/2\); for SDP under strict complementarity and unique
   optimum this is the generic case, cf. Sturm-type error bounds),
   \(D(g)=\Theta(\sqrt g)\), hence for every barrier
   \(\kappa_{\rm red}=\Omega(1/(\nu^3 g))\) and the canonical barrier
   gives \(\Theta(1/g)=\Theta(1/\mu)\). Verified: unit disk
   (\(\kappa\cdot\mu\to1.0000\) for the circle barrier) and the trace-one
   spectrahedron with \(C=\operatorname{diag}(0,1,2)\), unique rank-one
   nondegenerate optimum (\(\kappa\cdot\mu\to2.87\) for log-det). Note the
   corrected folklore: the reduced primal log-det Hessian at a unique
   nondegenerate SDP optimum is \(\Theta(1/\mu)\), not \(\Theta(1/\mu^2)\);
   the \(1/\mu^2\) rate is the \(\lambda_{\max}\) scale, but the flat
   winner--loser rotation chord keeps \(\lambda_{\min}\) at \(1/\mu\).

So for LP the dichotomy is complete and exact: bounded conditioning
(achieved by the log barrier) iff the optimum is unique; \(\Theta(1/\mu^2)\)
for every barrier iff \(\dim\Phi\ge1\). For SDP the new phenomenon is the
intermediate \(\Theta(1/\mu)\) law at generic unique optima.

## Corollary D (fractional conditioning laws from singularity degree)

The chord law converts *any* attained Hölder error-bound exponent into a
barrier-independent conditioning law: if the instance's sublevel sets
satisfy \(D(g)\ge c\,g^\theta\) for \(\theta\in[0,1]\), then every
\(\nu\)-self-concordant barrier has
\(\kappa_{\rm red}=\Omega(g^{2\theta-2}/\mathrm{poly}(\nu))\). For SDPs,
facial-reduction singularity degree \(d\) generically corresponds to
\(\theta=2^{-d}\) (Sturm-type error bounds), giving the hierarchy
\[
  d=0:\ \Theta(1),\qquad d=1:\ \Omega(1/g),\qquad d=2:\ \Omega(g^{-3/2}),
  \qquad d\to\infty:\ \to\Omega(1/g^2),
\]
with the positive-dimensional-face case as the \(\theta=0\) endpoint.

Explicit witness for \(d=2\): \(\min X_{22}\) over
\(\operatorname{tr}X=1\), \(X_{33}=X_{12}\), \(X\succeq0\) (\(3\times3\)).
The optimum \(X^*=e_1e_1^\top\) is unique, but the error-bound chain
degrades in two steps: \(X_{22}\le g\Rightarrow|X_{12}|\le\sqrt{g}
\Rightarrow X_{33}\le\sqrt g\Rightarrow|X_{13}|\le g^{1/4}\), and the
sublevel set genuinely contains \(X_{13}=\pm\Theta(g^{1/4})\) points
(take \(X_{22}=g\), \(X_{12}=X_{33}=\sqrt g/2\),
\(X_{13}=t\) with \(t^2\le cX_{11}\sqrt g\); the \(3\times3\) determinant
stays positive with explicit constants), so \(D(g)=\Theta(g^{1/4})\) and
every barrier has \(\kappa_{\rm red}=\Omega(g^{-3/2}/\mathrm{poly}(\nu))\).
Numerically the log-det barrier attains it:
\(\kappa\cdot\mu^{3/2}\to0.40\) stably over
\(\mu\in[10^{-4},10^{-1}]\), while \(\kappa\mu^2\to0\) and
\(\kappa\mu\to\infty\) — a clean non-integer conditioning exponent, which
would be hard to guess without the chord law and is strong evidence of its
sharpness. QIPM reading: the facial-reduction complexity of a sparse SDP
prices its central-path conditioning barrier-independently; singularity
degree, previously a feasibility/error-bound quantity, is also a
conditioning obstruction for every barrier method.

## Corollary E (near-degeneracy plateaus)

If \(P\) has a \(\theta\)-nearly-optimal face of diameter
\(\Theta(1)\) — i.e. \(D(g)=\Theta(g/\theta)\) for \(g\lesssim\theta\)
and \(\Theta(1)\) for \(g\gtrsim\theta\) — then the chord law predicts
\(\kappa\) grows like \((D(g)/g)^2\sim1/g^2\) down to \(g\approx\theta\)
and then **plateaus at height \(\Theta(1/\theta^2)\)**. Verified: on
\(\min\ x_3+\theta x_2\) over the simplex slice (unique vertex optimum,
face \(\{x_3=0\}\) is \(\theta\)-nearly optimal), the log-barrier
\(\kappa_{\rm red}\) follows \(\approx0.2/g^2\) through the crossover and
freezes at exactly \((4/3)\theta^{-2}\), for both \(\theta=10^{-2}\) and
\(10^{-3}\) (`notes/scripts/barrier_chord_law_check.py`, last section). QIPM
reading: the conditioning plateau that practitioners observe at high
accuracy is quantitatively the reciprocal-squared near-optimality gap of
the second-best face — computable from problem data, barrier-independent
as a floor, and the right number to use in resource estimates instead of
an unbounded \(1/\mu^2\) extrapolation.

## Real-instance validation (Netlib afiro)

`notes/scripts/afiro_chord_check.py` runs the log-barrier central path on the
repository's standard-form Netlib instance afiro (presolved to
\(9\times18\)), estimating \(\ell(x)\) by 40 random-direction LPs over
the sublevel polytope. Over \(\mu=1\dots10^{-5}\): (i)
\(\kappa\cdot g^2\approx5\times10^5\) is constant across four decades —
afiro has a positive-dimensional optimal face and obeys the \(1/g^2\)
law; (ii) \(\lambda_{\min}\ell^2\in[3.6,6.6]\), inside the theoretical
window \([1,(\nu+2\sqrt\nu)^2]=[1,701]\) and near its lower edge; (iii)
\(\lambda_{\max}g^2/\|\Pi_Vc\|^2\approx376\ge1\); (iv) CG solves the
reduced Newton systems to \(10^{-8}\) in 11--39 iterations even at
\(\kappa=8\times10^{13}\), confirming the *classical* two-cluster
benignity on real data
(2026-09-02-two-cluster-central-hessian-benign-kappa.md; note its
Theorem Q — the benignity does not transfer to single-polynomial QSVT).

## Theorem 1 (LP positive-dimensional face; original audited version)

Retained for its explicit strict-complementarity constants; superseded in
generality by Theorem A + Corollary C.1. Under: \(P\) compact,
\(P^\circ\ne\emptyset\), \(c\) nonconstant on \(P\), \(\dim\Phi\ge1\)
with a segment of half-length \(\delta_0\) in \(\Phi\); Goldman--Tucker
strictly complementary dual slack \(s^*\), \(\alpha=\min_{i\in N}s^*_i\),
\(c_i=\max\{|h_i|:h\in V,\|h\|=1\}\) for a fixed \(i\in N\); any
\(\nu\)-SCB \(F\); \(\Gamma=c^\top\hat x-\mathrm{OPT}\) for a fixed
\(\hat x\in P^\circ\), \(D_P=\operatorname{diam}P\). For
\(\mu\le\mu_0=\min\{\Gamma,\delta_0\Gamma/(2\nu D_P)\}/\nu\):
\[
  \kappa_{\rm red}(\mu)\ \ge\
  \frac{c_i^2\alpha^2\delta_0^2}{16(\nu+2\sqrt\nu)^2\nu^2\mu^2}.
\]
Proof as in the audited version: gap \(\le\nu\mu\); \(x_i\le\nu\mu/\alpha\)
via \(c^\top x-\mathrm{OPT}=(s^*)^\top x\ge\alpha x_i\); Dikin blow-up
along \(\hat h\) with \(|\hat h_i|=c_i\) (the step to \(x_i=0\) leaves
\(P^\circ\)); flat direction \(y=(1-\theta)T_\sigma+\theta\hat x\) with
\(\theta=g/(2\Gamma)\), \(T_\sigma\in\Phi\),
\(\langle F'(x),y-x\rangle=g/(2\mu)>0\), \(\|y-x\|\ge\delta_0/4\), then
(F3). Referee-audit notes applied: the exit-time parenthetical is
unnecessary (the zero-coordinate point is already outside \(P^\circ\));
the \(\theta\le\delta_0/(4D_P)\) arithmetic uses \(\nu\ge1\); the
\(\operatorname{relint}\Phi\) choice of the anchor is superfluous.

## Theorem 2 (nondegenerate vertex, explicit limit constant; essentially known)

Scope note: this theorem *replaces* assumption (A3)/\(\dim\Phi\ge1\) with a
unique nondegenerate vertex; it keeps compactness and full row rank. The
content is essentially prior art (Forsgren--Gill--Wright 2002 Thm 4.2;
Terlaky-group QIPM statements); stated for the \(\ker A\)-reduced
formulation and the dichotomy.

If the optimum is a unique nondegenerate vertex (\(|B|=m\), \(A_B\)
nonsingular, \(x^*_B>0\), unique dual, \(s^*_N>0\)), then for the log
barrier
\[
  \limsup_{\mu\to0}\kappa_{\rm red}(\mu)\le
  (1+\|A_B^{-1}A_N\|_2^2)
  \Big(\frac{\max_{i\in N}s^*_i}{\min_{i\in N}s^*_i}\Big)^{\!2},
\]
using \(h_B=-A_B^{-1}A_Nh_N\) on \(\ker A\),
\(\langle F''h,h\rangle=\sum_N h_i^2s_i(\mu)^2/\mu^2+\sum_B h_j^2/x_j^2\),
and \((x(\mu),s(\mu))\to(x^*,s^*)\) (McLinden 1980; Megiddo 1988 — central
path converges to the analytic centers of the optimal faces; here both are
singletons). For a unique but *degenerate* vertex, \(A_B\) is still
injective (a kernel vector of \(A_B\) would generate a segment in
\(\Phi\)), the same computation runs with \(s^*\) the dual analytic
center, and boundedness persists — Corollary C.2 gives the general proof
and the numerics confirm it.

## Corollary (approximate centrality)

If \(\lambda_\mu(x)=\|c/\mu+F'(x)\|^*_x\le\rho\le1/6\) on \(V\), then
\(\|x-x_F(\mu)\|_{x_F(\mu)}\le\rho/(1-\rho)^2\le1/4\) (via
\(f(x)-f^*\le\omega_*(\rho)\) and \(\omega(\|x-x^*\|_{x^*})\le f(x)-f^*\);
the bound \(\omega^{-1}(\omega_*(\rho))\le\rho/(1-\rho)^2\) was verified on
\((0,0.95)\)), and Hessians within local distance \(r\le1/4\) are
\((1-r)^{\pm2}\)-comparable, so every short-step iterate inherits the
chord-law floor up to a factor \((3/4)^4\). The floor is not a knife-edge
property of exact centers.

## QIPM interpretation (scoped)

1. For QLSA/tomography-based QIPMs that solve barrier Newton systems, the
   late-path condition number is dictated by problem geometry, not barrier
   choice: degenerate (positive-dimensional-face) sparse LPs/SDPs force
   \(\kappa=\Omega(1/\mu^2)\) for every barrier; generic unique-optimum
   SDPs force \(\Omega(1/\mu)\); and for unique-optimum LPs conditioning
   was never the obstruction (which is exactly why this repository's
   condition-one hard families all have vertex optima, and their hardness
   had to live in loading/recovery instead).
2. Scope: condition-number-free quantum IPM lines (Apers--Gribling
   arXiv:2311.03215, arXiv:2311.03977; Apers--Gribling--Nieuwboer--Walter
   arXiv:2510.06115) do not solve these systems and are untouched. Scalar
   congruences and end-to-end preconditioning accounting are treated in
   2026-09-02-congruence-condition-recovery-frontier.md and
   2026-09-02-parity-preconditioner-dichotomy.md; Theorem A composes with
   those but does not subsume arbitrary preconditioned systems.
3. In accuracy terms: reaching gap \(\varepsilon\) means
   \(\kappa=\Omega((D(\varepsilon)\|\Pi_Vc\|/\varepsilon)^2/\nu^2)\)
   for every barrier — e.g. \(\Omega(\varepsilon^{-2})\) on degenerate
   instances — so "pick a better barrier" is now a closed escape route,
   complementing the closed "pick a better scalar congruence" route.

## Sharpness and observed exact constants

- Simplex family (\(\min x_3\), face dim 1): observed
  \(\lambda_{\max}\mu^2\to2/3=\|\Pi_Vc\|^2\) with \(g\to\mu\) — Theorem
  A(a) is *exactly* tight there for both tested barriers; \(\kappa\mu^2\to
  1/6\) (log), \(0.033\) (weighted), \(1/6\) (log+extra), \(1/3\)
  (volumetric, referee's test), \(0.048,\ 0.017,\ 0.083\) (referee's
  log+quadratic, weight-10, cross-term barriers). Rate never moves.
- Disk: \(\kappa\mu\to1.0000\); chord prediction
  \(\ell^2\approx2g\Rightarrow\kappa\gtrsim2/((\nu+2\sqrt\nu)^2g)\) —
  matching rate, constants within the \((\nu+2\sqrt\nu)^2\) slack.
- SDP unique nondegenerate optimum: \(\kappa\mu\to2.87\); the
  \(\lambda_{\min}\) direction is the winner--loser off-diagonal rotation
  \(1/(d_1d_2)=\Theta(1/\mu)\), exactly the sublevel chord.
- Vertex family: \(\kappa\to4=(s^*_4/s^*_3)^2\), within Theorem 2's bound
  8; degenerate-vertex family (\(n=5,m=3,|B|=2\)): \(\kappa\to1.2\).
- Log-barrier upper: \(S\) must be a tail supremum
  (\(\sup_{0<\mu\le\bar\mu}\)); the unrestricted sup diverges as
  \(\mu\to\infty\) (referee repair applied).

Scripts: `notes/scripts/barrier_dichotomy_check.py` (simplex + vertex families,
four barriers; note the "weight 0.01" barrier there is illustrative only —
weights below 1 are **not** self-concordant, referee repair applied) and
`notes/scripts/barrier_chord_law_check.py` (degenerate vertex, SDP face via
finite-difference Hessians, disk, SDP unique optimum via the explicit
resolvent path).

## Novelty calibration (audit completed for the dichotomy; chord law inherits)

- Log-barrier prior art: M. Wright 1994/1998; Forsgren--Gill--Wright 2002
  (Thm 4.2 eigenvalue split under nondegeneracy); Terlaky-group QIPM
  papers (arXiv:2307.14445, 2412.11307, 2512.06224): \(O(1/\mu^2)\),
  \(O(1/\mu)\) upper bounds for specific log-barrier systems and the
  degenerate/nondegenerate \(\kappa\) statements — none quantify over
  barriers.
- All-barriers precedent: Allamigeon--Gaubert--Vandame (STOC 2022,
  arXiv:2201.02186) — iteration/curvature lower bounds over all
  self-concordant barriers via tropical geometry; different quantity
  (path geometry, not Hessian conditioning). Must be cited and
  differentiated.
- A dedicated search found no published condition-number lower bound over
  all self-concordant barriers, and nothing resembling the sublevel chord
  law \(\kappa\asymp(D(g)/g)^2\) or the gap-matched near-optimality of the
  canonical barrier. The bridge to weak-sharp-minima/error-bound moduli
  (Burke--Ferris; Sturm-type SDP bounds) appears new in this conditioning
  context. Honest caveats: the ingredients are classical one-liners from
  self-concordance theory (Dikin/asymmetric containment plus
  \(\nabla F(x_\mu)=-c/\mu\); the containment facts appear as-is in
  standard notes, e.g. Hildebrand's and Lee--Yue's); a referee may call
  Theorem A shallow-but-unstated. Evidence of apparent novelty, not
  proof of priority.
- Chord-law-specific sweep (completed after the dichotomy sweep): no
  prior universal-over-barriers conditioning bound and no prior "log
  barrier is a near-optimal barrier for conditioning" claim found. Two
  precedents to cite for the \(\Theta(1/\mu)\) phenomenon: M. Wright
  (Math. Prog. 67, 1994) proves the \(\Theta(1/\mu)\) structured
  log-barrier Hessian conditioning at nondegenerate **NLP** optima with
  \(1\le m_a<n\) active inequality constraints — the
  inequality-constraint analog of our curved-boundary/unique-SDP regime,
  for the log barrier only; and Augustino--Nannicini--Terlaky--Zuluaga
  (arXiv:2112.06025, §7) derive \(1/\mu^2\)-type bounds for the
  **primal--dual Schur complement**, a different matrix — the contrast
  between the two is exactly the reduced-primal-vs-Schur distinction this
  note's SDP observation turns on. No statement was found that
  restricting \(X^{-1}\otimes X^{-1}\) to \(\ker\mathcal A\) at a unique
  nondegenerate SDP optimum kills the \(1/\mu^2\) block leaving
  \(\Theta(1/\mu)\). Related SDP path asymptotics to cite: Lu--Monteiro
  (2004, "Error bounds and limiting behavior of weighted paths associated
  with the SDP map \(X^{1/2}SX^{1/2}\)") prove a
  \(\Theta(\nu)\)-versus-\(\Theta(\sqrt\nu)\) dichotomy for weighted
  central-path convergence under strict complementarity — a
  path-geometry parallel of the \(D(g)\sim g\) versus \(\sqrt g\)
  sublevel dichotomy here, again without conditioning statements or
  barrier quantification.

## Verification record

1. Numerical verification: six families, eleven barriers total (including
   the referee's volumetric barrier with analytic derivatives), three
   regimes; exact-constant tightness of A(a) observed on the simplex
   family.
2. Fact audit against primary sources ([N04]/[N18]/Nemirovski/Renegar,
   Burke--Ferris, Hoffman lineage): all statements, constants, and sign
   conventions confirmed; citation numbers corrected (4.2.5, not 4.2.6).
3. Independent adversarial referee audit of Theorems 1, 2, Corollary:
   verdict "correct as stated, proofs sound, no counterexample"; repairs
   applied: tail-sup for \(S\); the \(\lambda_{\min}\ge1/D^2\) claim now
   proved by the chord argument (which the referee independently proposed
   and which grew into Theorem B); Theorem 2 assumption scoping and
   McLinden/Megiddo citations; non-SC adversarial barrier relabeled;
   \(\nu\ge1\) usage stated.
4. Novelty audits completed for both the dichotomy and the chord law
   (reports summarized above); the Wright-1994 NLP precedent and the
   Augustino et al. Schur-complement contrast are the required prior-art
   citations for the \(\Theta(1/\mu)\) regime.
5. Post-audit additions received their own external referee pass:
   Theorem W verdict **sound** (Courant--Fischer indexing, both bound
   directions, sign choices, and edge cases verified; numerical sandwich
   confirmed on the simplex family with \(1/(w_d^-)^2\) matching the
   A(a) floor exactly at 98.88; the audit's three cosmetic repairs —
   inf/sup convention with the equator ambiguity, the
   \(w_1^+\ge\ell(x)\) bridge, and the \(w_j^+\le w_j^-\) dimension
   count — are applied in the current text). Theorem B′, Corollary E,
   and the afiro validation remain one-step specializations of the
   audited machinery, numerically verified.
