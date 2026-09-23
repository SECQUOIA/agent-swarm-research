# Independent audit: fixed-dimensional quadratic follower blocks

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the fixed-block response extension](bilevel-fixed-block-response-extension.md). The active-normal compression is valid with arbitrarily many local constraints, and the resulting rational response representation preserves the polynomial exact bilevel algorithm. No substantive correction was needed.

## Independent active normals and local optimality

At a global follower KKT point, subtracting the shared resource-multiplier terms leaves a normal-cone condition for each block's local polyhedron. The effective linear cost includes the aggregate derivative evaluated at the proposed global aggregate. Together with the positive definite local Hessian, this is exactly the sufficient KKT condition for the stated strictly convex local quadratic program. The full follower objective can remain nonconvex; only this auxiliary local program is asserted to be convex.

Choosing a row basis for local equalities is legitimate because all original equality rows remain as feasibility tests. In particular, linearly dependent equality rows with inconsistent leader-dependent right-hand sides are detected rather than silently discarded.

In the quotient by the equality row space, every needed inequality-normal contribution has a nonnegative conic representation on active rows. If its positive-support generators are linearly dependent, choose a dependence with at least one positive coefficient and subtract the largest permissible positive multiple from the conic coefficients. All coefficients remain nonnegative, at least one vanishes, and the represented quotient vector is unchanged. Repetition leaves independent quotient generators. This works even if the cone has lineality or includes zero generators. Lifting back gives rows independent together with the equality basis, with at most `d_b-t_b` selected inequality rows.

Therefore the enumerated independent subsets contain a representation of every local optimizer. No nondegeneracy, strict complementarity, or Slater condition is required. A lower-dimensional or singleton local polyhedron causes no exception. The empty active subset is allowed.

## Cramer representation and feasibility tests

The saddle-point matrix is nonsingular on the leader set: its homogeneous equations give `y^T Q_b y=0` and hence `y=0`, after which independent constraint rows give zero multipliers. This proves invertibility without assuming a sign for its determinant.

Multiplying a Cramer numerator and denominator by the determinant gives the same rational function over a strictly positive squared determinant. All primal feasibility and inequality-multiplier sign tests can therefore be cleared without reversing inequalities. Active equalities and stationarity already hold by the solved linear system. A passing candidate is a KKT point of a strictly convex local program, hence its unique optimizer. Different passing branches may have different multipliers but must return the same follower block.

These assertions are used only for leaders in `C`, where positive definiteness guarantees nonzero denominators. Sign conditions outside `C` can be retained without changing the final formula, which includes the leader-domain condition.

## Joint regimes and encoding complexity

For fixed local dimension, each block has polynomially many independent active subsets. Each associated matrix has bounded dimension, so its determinants, adjugates, Cramer numerators, and cleared feasibility tests have degree `O(d delta)` and polynomial coefficient bit length. Including every original local row in every branch test still gives polynomial total input growth because the exponent depends only on fixed `d`.

All tests live in the same fixed-dimensional global compressed vector. Their realizable joint sign conditions have polynomial count and polynomial enumeration cost. On a sign condition intersecting `C`, branch validity is fixed. Selecting the first valid local branch in each block loses no follower point by local uniqueness. This is the step that avoids an exponential product of independent block lists.

Taking a product of the selected positive denominators gives common numerators whose degree is polynomial in the block count and actual input degree. Expanding them is polynomial because the compressed dimension is fixed. Clearing the shared constraints, complementarity, follower value, and explicit upper polynomials preserves polynomial degree, formula length, and coefficient encoding. No local block coordinate or local multiplier is added to the globally quantified variable list.

## Global response, algebraic recovery, and attainment

Every global follower minimizer has polyhedral multipliers and therefore appears in the compressed representation. Every represented point is follower-feasible. Universal comparison with all represented KKT points consequently selects precisely the globally minimizing follower responses, as in the independently reviewed scalar theorem. It does not use local convexity to assert global convexity.

The same fixed-total-dimension quantifier-elimination and sampling results give exact feasibility and algebraic optimization. All recovered follower coordinates are rational functions in one common fixed-dimensional algebraic sample. The number of coordinates may grow, but their joint field degree and total encoding remain polynomial.

The full collection of local, shared, and coordinate-bound normals is independent of the leader. Its row count may grow with the instance; Hoffman's constant needs only to be uniform over right-hand sides for each one instance. The previously checked Hoffman argument therefore proves closedness of the global-response graph. Polynomial coordinate bounds over compact `C` give uniform boundedness, and closed upper inequalities give a compact optimistic feasible set. The upper optimum is attained whenever feasible.

The proof depends on fixed local dimension for the active-subset count and on positive definiteness for unique rational local response. Growing local dimension, changing constraint normals, and nonlinear local response functions require separate arguments. The candidate states these boundaries accurately. The local active-set technique is correctly attributed as established; this audit does not certify novelty of the full bilevel combination.
