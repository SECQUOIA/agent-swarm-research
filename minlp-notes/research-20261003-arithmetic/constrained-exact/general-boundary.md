# The remaining arbitrary-polyhedron exact-comparison boundary

Date: 2026-10-03. Status: unresolved boundary with a proved transfer
criterion. This note records what the new positive results do and do not
establish.

For a globally strongly convex rational quartic over an arbitrary rational
polyhedron, the current general upper bound remains the unambiguous oracle
classification in the
[existing constrained note](../../research-20260927/polyhedral-strong-quartic-unambiguous-upper.md).
The new [quadratic-subproblem transfer](structural-newton.md) and its
[network-flow specialization](network-flow.md) do not establish
deterministic \(\mathrm P^{\mathrm{PosSLP}}\) for all polyhedra.

## 1. What the Newton route removes

Let \(p\) minimize \(f\) on a closed convex polyhedron \(P\), and
write \(H_x=\nabla^2f(x)\). The exact constrained Newton point
\[
 N(x)=\arg\min_{y\in P}
 \{\nabla f(x)^T(y-x)+\tfrac12(y-x)^TH_x(y-x)\}
\]
satisfies
\[
 \|N(x)-p\|\le \frac{M}{2\mu}\|x-p\|^2
\]
whenever \(H_x\succeq\mu I\) and \(M\) bounds Hessian
Lipschitz variation along the segment \([x,p]\). The proof adds the
two first-order variational inequalities and applies the Taylor remainder
bound. It does not need strict complementarity, identification of the
active face, or a lower bound on a nonzero slack.

The difficulty is therefore not the local convergence estimate. It is
computing the exact rational quadratic minimizer after the iterate and its
Taylor coefficients acquire exponentially many expanded bits. The needed
subroutine must have polynomial arithmetic/comparison complexity on the
particular quadratic models, or another verified circuit-compatible
complexity guarantee. A polynomial-time algorithm measured in the expanded
rational input length does not supply that guarantee.

In the network-flow result, the exact strongly polynomial separable
quadratic-flow algorithm provides this subroutine. For an arbitrary
polyhedron and its varying circuit Hessian, no such dependency is proved in
this work. The general question remains open here.

## 2. Why a direct squared-penalty reduction does not close the gap

Consider the one-dimensional example
\[
 \min_{x\ge0}\tfrac12(x+1)^2.
\]
Its constrained minimizer is \(p=0\). Penalizing the violated inequality
by a squared hinge gives the unconstrained function
\[
 F_\lambda(x)=\tfrac12(x+1)^2+
                    \tfrac\lambda2\max\{0,-x\}^2,
 \qquad \lambda>0.
\]
Its unique minimizer is
\[
                 p_\lambda=-\frac1{1+\lambda}.
\]
Indeed, on \(x<0\) the derivative is \(1+(1+\lambda)x\),
whose zero is negative, while on \(x\ge0\) the derivative is positive.
Consequently, making the coordinate error at most \(g\) requires
\(\lambda\ge g^{-1}-1\). If the general algebraic separation target
is \(g=2^{-2^{a(I)}}\), printing this penalty coefficient can require
exponentially many bits in \(I\).

Repeated squaring can represent such a coefficient by a short circuit, but
the existing unconstrained comparison theorem accepts explicitly encoded
polynomials and uses polynomial-bit rational weak optimization for its
warm start. Its running-time bound cannot simply be reinterpreted as a
bound in circuit length. Moreover, the squared hinge is piecewise
quadratic, not a globally polynomial objective. Thus this direct penalty
argument fails to meet two hypotheses of that theorem.

This example is easy to solve exactly and is not a complexity lower bound.
It identifies the missing justification in the proposed reduction. Other
penalty methods or circuit algorithms could still succeed.

## 3. Accuracy-driven barrier iteration is also insufficient by itself

An iteration bound polynomial in \(\log(1/\varepsilon)\) is an
appropriate approximation theorem. Substituting
\(\varepsilon=2^{-2^{a(I)}}\) gives an exponential bound in \(I\).
Storing its accuracy parameter as a circuit does not reduce its number of
iterations. A barrier proposal therefore needs an additional rapid
refinement or exact-termination argument whose iteration bound is
polynomial in the original input length. No general such argument is
supplied here.

These failures are limitations of specific proof routes. They do not rule
out deterministic \(\mathrm P^{\mathrm{PosSLP}}\) for general
polyhedral strongly convex quartic comparison and do not establish a
hardness separation from that class.

## 4. Verification record

The penalty minimizer and error bound follow by the displayed exact
one-variable differentiation. The constrained Newton inequality is proved
in the transfer note and checked on boundary instances in the targeted
network-flow check. This diagnostic does not require additional software
tests. No project-wide verification or CI inspection was performed.
