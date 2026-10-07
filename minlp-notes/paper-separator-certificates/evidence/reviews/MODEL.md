# Independent mathematical review: model section

Reviewed `sections/model.tex` against the assigned brief, notation contract, the certificate and configuration definitions in `research-20260929/theory-decomposition/decomposition-certificates.md`, and their use in `research-20261002/regridded-certificates/note.md`.

## Verdict

The mathematical foundation is sound. I found no defect in the conditional value recursion, continuity and attainment arguments, lower-certificate validity, consistent-point chain inequality, fixed-slope dynamic program, configuration unfolding, or current-center gradient cancellation. The manuscript usefully strengthens boundary conventions by retaining all nonempty touching intersections. No computational experiments or literature discovery were performed.

## One terminology correction

The sentence “The treewidth convention is $w=p-1$” can conflate the width of the supplied decomposition with the graph's minimum possible width. Replace it with:

> The width of this decomposition is $p-1$. The treewidth of an associated interaction graph may be smaller.

If the paper does not otherwise use $w$, simply omit the sentence and use $p$ consistently. This matters because the algorithm preserves the supplied decomposition and factor assignment rather than minimizing width.

## Verified arguments and edge cases

1. **Conditional decomposition.** Running intersection implies that any coordinate shared by two child subtrees belongs to the parent bag and to the relevant child separators. Once the parent bag point is fixed, the remaining child coordinates are disjoint, so the minima separate exactly. The box domain provides every separator value with the same compact product domain for the private variables. Continuity follows inductively from uniform continuity of the continuous local objective on the compact product box; minimum attainment is immediate.

2. **Validity.** For a point attaining the true conditional recursion, select any containing bag box and any containing child cells. Including every nonempty intersection ensures the child bounds apply even at partition faces. The direction of the inequalities is correct: $l\le\operatorname{Rel}\le a_t+\sum\phi_u$. The argument needs only the lower-model property, not the quadratic error contract, gradient regularity, or quadratic growth.

3. **Chain inequality.** The statement correctly holds for every selection of containing bag boxes. A direct equivalent proof is to sum the root inequality and all nonroot local inequalities, then use each parent child bound $\psi_{t,B_{\pi(t)}}(x_{S_t})\le l_{t,D_t}(x_{S_t})$ and cancel the nonroot affine functions. The existing recursive proof is valid.

4. **Fixed slopes.** The affine child function formed by the smallest intercept over all touching cells satisfies every child-bound inequality on its overlap. The set of touching cells is nonempty because the cells cover the full separator box. For every own cell $D$, at least one bag box projects onto a point of $D$; each nonempty intersection is compact, including intersections with fixed coordinates. Thus each displayed intercept minimum is finite and attained.

5. **Unfolding.** The child cell choice depends on its parent's selected box but not its parent's selected point. This precisely matches the configuration definition. Once the parent box and point are fixed, the separate child intercept minima are independent; recursive substitution introduces exactly one incoming minus-slope term and one outgoing plus-slope term for every nonroot edge. Finitely many compact configuration pieces ensure attainment and permit recovery from stored choices. No equality between the two separator copies is inadvertently imposed.

6. **Current-center slopes.** The coordinate-occurrence bags form a connected tree and hence have a unique highest bag. Its stored copy is in the original coordinate interval, so the consistent point belongs to $X$. Every path from that highest occurrence to a lower occurrence stays in the coordinate-occurrence subtree. Exchanging the finite sums yields the stated subtree gradient coefficients and the signs in the error identity. The proof does not use stationarity, an interior optimum, growth, or differentiability of a conditional value function.

7. **Empty separators and repeated/contained bags.** All statements remain valid when a separator has dimension zero: there is one cell, its slope is the unique empty vector, and its intercept is a scalar. When a bag is contained in its parent, its private-coordinate domain is a singleton; the conditional recursion is still a minimum over a fixed compact set. Repeated bags and $q=p$ introduce no obstruction. Empty bags after fixed-coordinate substitution are similarly harmless; if all coordinates are fixed the special evaluation case already disposes of the problem.

8. **Boundary and fixed coordinates.** Removing globally fixed coordinates before constructing partitions avoids the shell-partition issue found in the source notes. Subsequent local intersections may fix coordinates without invalidating any convex minimization or attainment statement. Boundary points satisfy all identities. The model intentionally uses full closed-overlap conditions rather than the optional source convention that omits touching pairs.

9. **Accounting.** The text correctly distinguishes partition size from local check count and numeric representation size. The phrase “These are convex minimization problems” describes the mathematical subproblems and does not claim an efficient oracle for arbitrary supplied convex functions. Later computational sections must maintain that distinction.

## Integration suggestions

- Keep the all-touching-pairs convention throughout the inexact and arithmetic sections; the exact configuration formula relies on it.
- State explicitly in a later algorithm that the slope pass also requires supplied bag gradient evaluations. The postorder accumulation alone is linear in coordinate incidences.
- Preserve the distinction between an upper bound certified by an enclosure and an exactly evaluated feasible objective value; the definition allows either because it only requires $\UB\ge f^*$.
- The local model contract is already bag-level. Any comparison with factorwise models should retain the factor-count dependence in evaluation and input-size accounting.

## Targeted checks

Only source and draft reading was used. No manuscript compilation, computational experiment, project-wide verification, or CI check was run for this review.
