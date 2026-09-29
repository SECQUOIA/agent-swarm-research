# Adjacent positive diagonal entries: source audit and obstruction

Date: 2026-09-27. Investigator: `/root/positive_pair_sdp_frontier/positive_pair_prior`.

The stable-set condition on the positive diagonal entries cannot be replaced
by a bound of two on the size of their connected components. A direct
corollary of a published preprint's certificate gives a gap with two adjacent
positive diagonal entries on a four-vertex path. The continuous two-variable
block can even be positive definite. This is an obstruction to the standard
SDP relaxation, not to polynomial-time optimization of the class.

## Primary sources examined

- Zhang and Wang, [*On the Ω(n) SDP relaxation gap for Submodular
  Box-Constrained Quadratic Programming*, arXiv:2609.03617v2](https://arxiv.org/html/2609.03617v2),
  September 7, 2026: equation (5), Proposition 2 and its certificate, and
  Section 2.2. I first inspected v1, then checked the current v2; the relevant
  certificate is unchanged. Their example has four positive diagonal entries.
  The reduction below replaces two outer squares by their secants at a
  certificate where their diagonal upper bounds are tight.
- Burer, Natarajan, and Willemsen, [*On the Semidefinite Representability of
  Continuous Quadratic Submodular Minimization With Applications to Pricing
  and Moment Problems*, arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3):
  Theorem 1 proves exactness in dimension at most three for PSD plus upper
  RLT; Example 4 provides a four-variable failure. Consequently, the
  four-variable obstruction below is dimension-minimal. It also fails the
  stronger full-RLT relaxation.
- Tardella, [*Connections between continuous and combinatorial optimization
  problems through an extension of the fundamental theorem of Linear
  Programming*](https://doi.org/10.1016/j.endm.2004.03.054), 2004:
  Theorem 3 on page 225 of the open [CTW04 proceedings](https://www.lix.polytechnique.fr/~liberti/ctw04proc.pdf)
  was inspected visually in the previously downloaded primary PDF. It gives
  polynomial-time submodular box minimization when the residual minimum
  after fixing coordinatewise quasiconcave variables at endpoints is
  polynomially evaluable. This already covers bounded-size positive-diagonal
  components. It also covers a jointly convex residual block through convex
  quadratic optimization. It does not assert exactness of the standard SDP.

The journal article related to Tardella's proceedings paper was not needed
for this audit. No claim is made about its uninspected theorem numbering.

## Two adjacent positive entries suffice

Write the variables as \((u,s,t,v)\in[0,1]^4\), and set

\[
 p(u,s,t,v)=s^2+t^2-us-2st-tv+\tfrac34u+s+\tfrac14v.
 \tag{1}
\]

This is submodular. Its interaction graph is the path
\(u-s-t-v\), and only \(s,t\) have positive diagonal coefficients.
It is affine in each endpoint variable. Its four endpoint restrictions are

| \((u,v)\) | \(p(u,s,t,v)\) |
|---|---|
| \((0,0)\) | \((s-t)^2+s\) |
| \((1,0)\) | \((s-t)^2+3/4\) |
| \((0,1)\) | \((s-t+1/2)^2\) |
| \((1,1)\) | \((s-t)^2+1-t\) |

These are nonnegative on the square. Multilinear interpolation in \((u,v)\)
therefore proves \(p\geq0\) on the cube, with equality at the origin.
This proof is independent of the cited nonnegativity proof.

Let \(\gamma=2-\sqrt3\). Specializing Zhang–Wang's Proposition 2 to
\(a=b=1/2\) gives the following moment point:

\[
 \mu=\begin{pmatrix}2\gamma/3\\1/3\\2/3\\1-2\gamma/3\end{pmatrix},
 \qquad
 X=\begin{pmatrix}
 2\gamma/3&2\gamma/3&2\gamma/3&2(1-3\gamma)/3\\
 2\gamma/3&(1-\gamma)/3&1/3&1/3\\
 2\gamma/3&1/3&(2-\gamma)/3&2/3\\
 2(1-3\gamma)/3&1/3&2/3&1-2\gamma/3
 \end{pmatrix}.
 \tag{2}
\]

The lifted matrix \(Y=\begin{pmatrix}1&\mu^T\\\mu&X\end{pmatrix}\)
is PSD, and all unit-box RLT inequalities hold, including their diagonal
instances. In particular, \(X_{uu}=\mu_u\) and \(X_{vv}=\mu_v\).
The linearized value of (1) is

\[
 L_{\mu,X}(p)=\sqrt3-\tfrac74<0.
 \tag{3}
\]

The connection to the source is exact: (1) is its objective at
\(a=b=1/2\), plus \(\tfrac14u(1-u)+\tfrac14v(1-v)\).
These added terms have zero linearized value at (2). The source's lower
bound for its relaxation also transfers, because both added diagonal RLT
slacks are nonnegative. Thus the full-RLT optimum in (3) is exact, not only
an upper bound on the relaxed optimum.

## Strict diagonal signs and a positive definite continuous block

The obstruction is not caused solely by zero endpoint curvature or a
singular continuous block. For any \(\eta>0\), adding

\[
 \eta\{u(1-u)+v(1-v)\}
\]

preserves the true optimum zero and the relaxed value in (3), while making
the endpoint diagonal coefficients strictly negative. Adding in addition
\(\delta(s^2+t^2)\) makes the continuous block

\[
 \begin{pmatrix}1+\delta&-1\\-1&1+\delta\end{pmatrix}
\]

positive definite whenever \(\delta>0\). For sufficiently small positive
\(\delta\), the same certificate still has negative objective.

The parent investigator obtained a simpler rational certificate by using
\(\gamma=4/15\) in (2), for which the relaxed value of (1) is \(-1/60\).
Its diagonal sum is \(X_{ss}+X_{tt}=37/45\), so the choice
\(\delta=1/100\) gives relaxed value \(-19/2250\). The parent's separate
note and fresh review supply the exact rational PSD verification; this
audit independently checked the algebraic source certificate (2).

## Scope, priority, and verification

The two-positive-entry example is an immediate transformation of
Zhang–Wang's published formula. It should be credited as a corollary of that
example, not presented as an independent major counterexample. The
strict-curvature perturbation is elementary. Their useful role is to give
a sharp boundary to the proposed stable-positive-diagonal theorem and
prevent an incorrect extension to adjacent convex blocks.

Additional searches used combinations of `submodular`, `positive diagonal`,
`two`, `SDP`, `quadratic box`, and Tardella's title. They located no separate
claim resolving the exact two-positive-entry formulation. This unsuccessful
search does not establish novelty. Sources outside the primary papers
listed above were not used as evidence for a mathematical claim.

A targeted inline Python/SymPy calculation checked all 31 nonempty
principal minors of the 5-by-5 matrix in (2), all 64 RLT slacks including
diagonal cases, its rank three, and the exact objective (3). Every check
passed using exact expressions in \(\mathbb Q(\sqrt3)\). This independently
validates the particular certificate, not the source's general gap bounds
or the stable-set theorem. No project-wide checks or CI checks were run.
