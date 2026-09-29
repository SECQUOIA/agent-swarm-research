# Independent review of the binary-separator forest extension

Research date: 2026-09-27. Reviewer:
`/root/frontier_cube/four_star_route/four_star_bound_bridge`.
Reviewed artifact: [binary-separator-forest-hull.md](binary-separator-forest-hull.md).
Verdict: no defect found in the stated theorem or corollary, conditional on
the proved binary-leaf star theorem. This review does not establish priority.

## Incidence graph and conditional gluing

Because the continuous vertex set \(C\) is stable, every edge is either
continuous–binary or binary–binary. Relabel a continuous vertex \(c\)
as its star-bag node, keeping all incident edges to binary neighbors.
Subdivide each binary–binary edge once, using its edge-bag node as the
subdivision vertex. These operations give exactly the incidence graph
described in the proof; therefore it is a forest. Several bags sharing
one binary vertex simply give several edges incident to the same
original binary node. They do not introduce a cycle.

After rooting a nontrivial component at a bag, every new bag has exactly
one already sampled variable, its parent binary separator. Any other
already sampled neighbor would supply a second path in the incidence
graph and hence a cycle. Matching the separator mean matches its entire
Bernoulli law. Sampling from the child's conditional law therefore
preserves that child's full distribution. It also leaves all variables
sampled earlier unchanged, so their joint distribution is preserved.

If a separator value has zero marginal probability, it is never reached
under the existing distribution. The conditional law assigned there can
be arbitrary without changing any distribution or retained moment.
Finitely supported local distributions and finitely many bags give a
finitely supported global distribution. Isolated binary vertices use
their Bernoulli laws; isolated continuous bags use the zero-leaf star
hull. Disconnected components may be sampled independently.

## Projected full-SDP equality and objective exactness

A global PSD moment matrix restricts to a PSD principal submatrix on
each star; its full RLT inequalities include every required local
leaf–leaf inequality. Each binary–binary edge yields the displayed four
nonnegative joint probabilities. Thus every global feasible point lies
in the exact local projection and has a representing distribution for
the retained coordinates. Convex combinations of global rank-one
matrices prove the reverse inclusion. No auxiliary nonedge product is
claimed to survive this reconstruction.

Raising \(X_{bb}\) to \(\mu_b\) for every binary-designated vertex
adds a nonnegative diagonal matrix. PSD and every RLT bound are
preserved. None of the retained coordinates changes. For a quadratic
objective with \(d_b\leq0\), this operation can only decrease its
linearized value. The reconstructed distribution consequently proves
the required lower bound for the original point. The sign of each
edge coefficient is irrelevant to this argument.

The independence condition on the positive-diagonal vertices is used
precisely to ensure that every continuous variable belongs to a single
star bag and every separator is binary. The proof supplies no claim for
adjacent continuous vertices or for cyclic incidence structures.

## Representation size

Each continuous-star bag with degree \(d_c\) has a PSD matrix of order
\(d_c+2\) and \(O((d_c+1)^2)\) scalar variables and RLT constraints.
Since \(C\) is stable,

\[
\sum_{c\in C}d_c\leq |E|\leq |V|-1
\]

for a nonempty forest, with the sharper component adjustment when
needed. Consequently
\(\sum_c(d_c+1)^2\leq(\sum_c(d_c+1))^2=O(|V|^2)\).
The additional edge bags and isolated vertices preserve the stated
quadratic bound. This is a bound on an explicit conic representation,
not a claim about exact-arithmetic SDP solution complexity.

## Independent primary-source comparison

The reviewer opened both specified current versions directly.
Khajavirad's
[*Tight semidefinite programming relaxations for sparse box-constrained
quadratic programs*, arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2)
has the cited complete-overlap/no-plus-loop decomposition in Lemma 4.
Its Corollary 2 requires stable plus-loop vertices, logarithmically
bounded treewidth, and logarithmically bounded plus-loop degrees to
obtain a polynomial-size SOC formulation.

Dey and Khajavirad's
[*A second-order cone representable class of nonconvex quadratic
programs*, arXiv:2508.18435v2](https://arxiv.org/html/2508.18435v2)
Proposition 8 gives the cited forest result with stable plus-loop
vertices and logarithmically bounded plus-loop degrees. The reviewed
note correctly distinguishes its arbitrary-degree polynomial-size SDP
claim from those polynomial-size SOC claims. It does not prove removal
of the degree condition for SOC formulations.

The exact-square moment hull and the positive-loop epigraph hull are
also correctly distinguished. Adding independent nonnegative slack to
each retained continuous-square coordinate yields the epigraph
version: convexification commutes with addition of this fixed convex
cone.

## Verification limits

This was an analytic adversarial review plus direct primary-source
inspection. No numerical solver, exhaustive graph test, Lean proof,
project-wide verification, or CI inspection was used. The review leaves
the priority question and equivalent formulations in other literature
unresolved.
