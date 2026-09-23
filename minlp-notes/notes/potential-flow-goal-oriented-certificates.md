# Conservation-aware certificates for linear flow goals

Date: 2026-09-06. Status: implemented and [independently reviewed](review-potential-flow-goal-oriented-certificates.md), including integration with the original-instance envelope pipeline. The review caught a zero-load producer fallback regression during integration; it was corrected and all final checks passed.

Formal verification follow-up (2026-09-20): [Lean topic 16](../formal/topics/16-potential-flow-certificates/COVERAGE.md) proves support soundness and rational completeness, quantitative support convergence, curvature bounds, the optimal constrained factor and its zero-curvature obstruction, and the two-path comparison. The decidable goal predicate checks a supplied `C(v)`; separate theorems establish the optimal factor `C_*`. The Python implementation, original uncertainty-to-envelope mapping, bit-complexity claims, and Moore–Penrose/effective-resistance reformulation are outside this formal coverage.

This note adds two useful certificate formats to the deterministic passive-flow
solver components. They apply to arbitrary finite loopless graphs, including
parallel edges, with positive rational asymmetric quadratic coefficients. The
first bounds a linear goal by optimizing over an energy sublevel set. The second
uses a constrained weighted Laplacian solve to exploit conservation in an
existing energy-gap certificate. Neither requires a series-parallel graph.

These are applications of established convex duality, functional a posteriori
error estimation, and electrical-network projection. The contribution being
preserved here is the explicit rational verification mechanism, treatment of
zero curvature, and demonstrable benefit over independently bounded edges. A
new general error-bound or duality theorem is not claimed.

## Setup

Use the incidence convention that an oriented edge contributes +1 at its tail
and -1 at its head. Let

\[
 E(x)=\sum_e E_e(x_e),\qquad
 E_e(t)=\frac13\begin{cases}c_e^+t^3&t\ge0,\\c_e^-(-t)^3&t<0,\end{cases}
 \qquad c_e^+,c_e^->0.
\]

For a feasible load vector b, the physical flow x* is the unique minimizer of E
subject to Ax=b. Strict convexity gives uniqueness; coercivity gives existence.
An exactly conserved rational flow y provides the upper energy bound E(y).
The requested quantity is w^T x*, with rational w. An individual edge, a sum of
flows through equipment, or a net cut flow are special cases.

## Certificate A: support of a conserved energy sublevel set

Define the compact convex set S(y)={x: Ax=b, E(x)<=E(y)}. It contains x*.
For any rational lambda>0 and any rational node vector v, put

\[
 s_e=w_e-(A^Tv)_e,\qquad
 R_e\ge\sqrt{\frac{|s_e|^3}{\lambda c_e^{\operatorname{sgn}s_e}}}.
\]

Here R_e is nonnegative and rational, verified by squaring. Then

\[
 w^Tx^*\le U_w=
 \lambda E(y)+v^Tb+\frac23\sum_eR_e. \tag{1}
\]

Indeed, the conjugate of lambda E_e at s is
(2/3)sqrt(|s|^3/(lambda c_e^{sgn s})). Apply Fenchel's inequality on every edge,
then Ax=b and E(x)<=E(y). Applying (1) to -w gives a lower bound.

At lambda=0, the certificate is valid exactly when w=A^Tv; then
w^Tx*=v^Tb. This captures all cut functionals, and therefore any bridge flow,
without an energy calculation. The code verifies this identity exactly.

When E(y)>E(x*), relative Slater feasibility on Ax=b gives equality between the
support maximum and the infimum of the unrounded dual expression. If w is
nonconstant on the conservation affine space, an optimal multiplier has
lambda>0. Approximating such dual data rationally and refining upward square
roots gives arbitrarily close upper bounds. If the goal is constant, lambda=0
already certifies it. This is a completeness statement for the support problem,
not a bit-complexity claim for the certificate producer.

The cubic energy modulus gives a quantitative bound for every z in S(y). If
beta_L>0 is a lower bound on all edge coefficients, then

\[
 |z_e-x_e^*|^3\le\frac{6(E(y)-E(x^*))}{\beta_L}
 \quad\text{for every edge }e.
\]

Indeed, apply the modulus at the physical minimizer to the feasible flow z,
then use E(z)<=E(y). This is proved by
[`Network.supportSet_cubic_bound`](../formal/Formal/PotentialFlow/SupportComplete.lean).
As feasible trial energies approach E(x*), the whole support set therefore
approaches {x*}, and the exact support intervals converge for every fixed goal.
This includes zero physical edge flows, where a positive curvature bound may
be unavailable. The estimate is in terms of energy error; it gives no rate in
producer runtime or certificate size.

The cubic energy epigraph is representable by the same second-order-cone
construction used for the existing energy solver, so support bounds are
computable by conic optimization. The new code supplies the exact verifier and
accepts any proposed rational dual data; it does not yet supply a generic conic
producer for those data. Numerical solver status is never part of verification.
The demonstration produces sharp dual data analytically.

## Certificate B: a weighted Laplacian bound using edge intervals

Suppose an existing verified energy certificate gives

\[
 0\le E(y)-E(x^*)\le g,
\]

and certified intervals [l_e,u_e] contain both y_e and x*_e. The existing
Bregman certificate supplies such intervals. Define

\[
 h_e=\begin{cases}
 2c_e^+l_e&l_e>0,\\
 -2c_e^-u_e&u_e<0,\\
 0&l_e\le0\le u_e.
 \end{cases}
\]

These are lower bounds on E_e'' throughout the interval. Since the physical
gradient is a node-potential difference and A(y-x*)=0,

\[
 \frac12\sum_e h_e(y_e-x_e^*)^2
 \le D_E(y,x^*)=E(y)-E(x^*)\le g. \tag{2}
\]

Choose any rational v such that

\[
 s_e=w_e-(A^Tv)_e=0\quad\text{whenever }h_e=0,
 \qquad C(v)=\sum_{e:h_e>0}\frac{s_e^2}{h_e}.
\]

Conservation and weighted Cauchy–Schwarz in (2) give

\[
 |w^T(x^*-y)|\le\sqrt{2gC(v)}. \tag{3}
\]

A rational radius r is accepted if r>=0 and r^2>=2gC(v). All checks are rational.
If g=0, strict convexity already gives x*=y, so every goal is exact without any
curvature condition; the implementation handles this case separately.

**Optimal choice within this bound.** Let P be the positive-curvature edges,
Z the zero-curvature edges, D=diag(1/h_e:e in P), and A_P,A_Z the corresponding
incidence columns. Minimizing C subject to A_Z^Tv=w_Z is a convex quadratic
problem. Its stationarity equations are

\[
 \begin{bmatrix}A_PD A_P^T&A_Z\\ A_Z^T&0\end{bmatrix}
 \begin{bmatrix}v\\\eta\end{bmatrix}
 =\begin{bmatrix}A_PD w_P\\w_Z\end{bmatrix}. \tag{4}
\]

The implementation solves (4) by exact rational elimination, allowing singular
potential gauges and redundant constraints. If the zero-edge equations are
inconsistent, this Hessian bound cannot control the goal. Precisely, the
obstruction is a circulation supported entirely on zero-curvature edges on
which w is nonzero. This limitation belongs to the quadratic modulus; the
energy-sublevel bound remains valid. Returning an arbitrary regularized or
rounded solution that violates a zero-edge equation would invalidate (3), so
the verifier explicitly rejects it.

For positive h, C(v) is minimized by a weighted Laplacian solve. With
L=A H^{-1}A^T, the optimal value is

\[
 C_* = w^TH^{-1}w-(AH^{-1}w)^TL^+(AH^{-1}w).
\]

For a single edge e=(u,v), this equals
1/h_e-R_eff(u,v)/h_e^2, where the auxiliary electrical network has edge
conductance 1/h_e. It vanishes for bridges. This is the standard weighted
projection onto the circulation space expressed as a goal-error constant.

The dense Fraction solver is suitable for modest certificate sizes. No claim
of scalable sparse rational linear algebra is made. When all h are positive,
a sparse approximate solve can supply v followed by rational rounding: it need
not minimize C to yield a valid certificate. Zero-curvature equality constraints
must be preserved exactly.

## Quantified benefit: long parallel paths

Take two disjoint length-L paths from source to sink, all c=1, source injection
2, and zero internal injections. The exact physical flow is 1 on every edge.
Use y=1+epsilon along one path and y=1-epsilon along the other. For
0<epsilon<1 the exact energy gap is g=2L epsilon^2. The true physical potential
vector is integral, so it supplies an exact dual energy value without root
rounding error.

Every conserved flow is constant along each path and has path flows t,2-t.
The energy sublevel is exactly t in [1-epsilon,1+epsilon]: the energy is convex,
symmetric about t=1, and increasing away from that point. Thus the target-edge
support interval has width 2epsilon. In contrast, as epsilon tends to zero for
fixed L, the separate-edge Bregman interval has width
2 sqrt(2L) epsilon + o(epsilon). The Laplacian certificate has width
2epsilon+o(epsilon). Therefore conservation can improve this certificate width
by an arbitrarily large factor as L increases, with epsilon sufficiently small
that the initial intervals remain separated from zero.

This example is evidence of information lost by independent edge bounds, not
a hard physical-flow instance: its exact solution is elementary. It gives an
exact benchmark for the certificate mechanism.

Run:

```sh
python code/potential_flow_mpd/goal_flow_certificate.py
```

With epsilon=1/1000, observed exact-certificate widths (rounded for display):

| Path length L | Separate-edge Bregman | Laplacian | Exact support | Bregman/Laplacian |
|---:|---:|---:|---:|---:|
| 2 | 0.00399800593 | 0.00200200435 | 0.002 | 1.997 |
| 8 | 0.00799603843 | 0.00200401743 | 0.002 | 3.990 |
| 32 | 0.0159922895 | 0.00200807006 | 0.002 | 7.964 |

The demonstrations verify inclusion of the known physical goal, sharp support
upper certificates, an exact zero-flow bridge, rejection of an uncontrolled
zero-curvature circulation, and 15 corrupted certificates. Both ordinary Python
and optimized Python should be run for review; validity checks use explicit
exceptions, not assertions.

These bounds need not individually dominate every existing Bregman interval.
Intersect separately verified bounds when useful. In particular the support set
contains arbitrary conserved low-energy flows, not only physical flows; it is
not justified to assume every point of that set also satisfies the physical
Bregman bounds centered at y.

## Literature and positioning

Open literature checked on 2026-09-06:

- Boyd and Vandenberghe, *Convex Optimization* (2004), especially conjugates,
  Lagrange duality, and Slater's condition. The authors provide the book openly
  at [their book page](https://www.seas.ucla.edu/~vandenbe/cvxbook.html).
  Equation (1) is a direct specialization of this theory.
- Bartels and Milicevic, *Primal-dual gap estimators for a posteriori error
  analysis of nonsmooth minimization problems*, ESAIM: M2AN 54 (2020),
  1635–1660, [open article](https://numdam.org/articles/10.1051/m2an/2019074/).
  It develops the established use of primal-dual gaps to control energy and
  uniformly convex error measures. The present finite-network calculation
  should be positioned within that tradition.
- Lyons and Peres, *Probability on Trees and Networks*, Chapter 2,
  [author-hosted text](https://rdlyons.pages.iu.edu/prbtree/book_pb.pdf).
  Electrical energy minimization, weighted cut/cycle projections, and effective
  resistance are classical ingredients of (3)–(4).

The scoped search did not locate this exact asymmetric-quadratic rational
certificate package. That is not a strong novelty claim: the individual
mathematical mechanisms are standard. The defensible paper role is an explicit
certified-computation component, accompanied by its assumptions, finite checks,
and example showing that conservation materially changes the useful accuracy.

## Existing saved certificate: an additional practical check

Applying the new Hessian producer to the repository's saved six-edge envelope
certificate requires no new physical-flow solve:

```sh
python code/potential_flow_mpd/goal_flow_certificate.py --certificate code/potential_flow_mpd/envelope_certificate_example.json
```

| Edge | Existing Bregman width | Laplacian width | Improvement factor |
|---:|---:|---:|---:|
| 0 | 1.78322417e-6 | 9.44682415e-7 | 1.888 |
| 1 | 1.12795378e-6 | 8.76740867e-7 | 1.287 |
| 2 | 2.06347457e-6 | 8.37955634e-7 | 2.463 |
| 3 | 1.76881726e-6 | 9.44682415e-7 | 1.872 |
| 4 | 2.89362482e-6 | 8.76740867e-7 | 3.300 |
| 5 | 1.10676256e-6 | 8.37955634e-7 | 1.321 |

All six new bounds are independently checked by exact arithmetic after
rechecking the base energy witness. Their maximum width is 9.447e-7, compared
with 2.894e-6 for the original intervals. These are certified enclosures, not
measurements of the actual numerical solution error. The small size of this
case does not establish large-network runtime.
