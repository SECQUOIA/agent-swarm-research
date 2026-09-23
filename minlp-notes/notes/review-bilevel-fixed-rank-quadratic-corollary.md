# Independent audit: supplied diagonal-plus-fixed-rank quadratic coupling

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

**PASS.** The [corollary](bilevel-fixed-rank-quadratic-corollary.md) is a correct exact rational LP specialization of the reviewed fixed-aggregate theorem. No correction is required. Affine constraints are understood as the usual closed linear inequalities and equalities.

With `w=U^Tz`, the follower gradient is

```
Diag(d)z + c + Cx + UHw.
```

For `d_i>0`, its box normal-cone condition is exactly

```
z_i=clip(-(c_i+C_i x+U_i H w)/d_i).
```

The sign and divisor are correct. Although `w` itself contains `z_i`, this is a simultaneous KKT fixed-point equation, not a coordinate-minimization formula obtained by freezing `w` independently. Enforcing `w=U^Tz` restores the full gradient. Positive definiteness of `Q` makes these KKT conditions sufficient and gives a unique follower response. `H` need not itself be positive semidefinite, and no such extra assumption is used.

The two thresholds per coordinate are affine in the fixed-dimensional vector `(x,w)`. Their realizable sign cells number `N^{O(r+k)}`. On each closed cell the clipping formula is affine, including at boundaries where the adjacent formulas agree. Constant thresholds, coincident hyperplanes, rank-deficient `U`, and lower-dimensional leader sets cause no gap. Consistency, affine upper constraints, and the affine objective remain linear after substitution.

Every resulting LP-feasible point yields the actual follower response, and every feasible bilevel pair belongs to one of the LPs. Thus follower-dependent affine upper constraints are retained exactly; no approximation margin is required.

The displayed aggregate bounds follow directly from `0<=z_i<=1`. Together with the leader bounds, they make every closed cell LP compact. Feasible LPs attain rational optima, including degenerate cases. Rational substitutions and LP vertices have polynomial encoding length: divisions are by supplied nonzero rational `d_i`, and the aggregate equations contain only sums and products of polynomially encoded rationals. Comparing the polynomially many rational objective values gives exact global optimization and recovery. The empty leader or upper-feasible domain is detected by LP infeasibility. The cases `k=0` or `r=0` reduce directly to the same argument.

I also checked the source context directly: Megiddo and Tamir's *Linear Time Algorithms for Some Separable Quadratic Programming Problems*, section 2, derives clipped-affine responses in a fixed-dimensional multiplier space and the associated threshold hyperplanes. This supports the candidate's explicit credit for the classical cell mechanism; the present review does not assert a separate novelty claim. [Author manuscript](https://theory.stanford.edu/~megiddo/pdf/qtranrev.pdf).

The decomposition is supplied. The corollary does not find a diagonal-plus-fixed-rank representation of an arbitrary Hessian. Its comparison with arbitrarily small general coupling is therefore correctly qualified, and no contradiction with the near-identity hardness theorem follows.
