# Independent review of rank-one algorithms and certificates

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed: Theorem 2 and Corollary 2 in `results/rank-one-row-column-hardness.md`.

## Verdict

The fixed-parameter algorithm and the existence of polynomial-size quadratic exact
optimizers are correct. The decision problem is in NP and, using the independently
audited reduction in Theorem 1, strongly NP-complete. A stronger conclusion holds:
every yes instance with rational threshold has a polynomial-size **rational**
feasible certificate. Exact optimizers need not be rational.

The rational-certificate strengthening was developed during this review and checked
independently by `audit_rank_one`. It has been incorporated into Corollary 2.
This note is a proof audit, not a separate literature assessment.

## Simultaneous vertex patterns exist at a positive optimum

Finite bounds make the original matrix set compact. If zero is optimal, it gives a
rational optimizer. Otherwise fix a globally optimal positive total `S*` and an
optimal pair of margins. With the column margin fixed, minimize the linear
numerator over the row box intersected with its total equation; an optimal vertex
exists, and replacing the row margin cannot improve on the global optimum, so it
preserves optimality. Now minimize over the column margin with that row fixed and
choose a column vertex. This also preserves global optimality.

A vertex of a box intersected with one sum equation has at most one coordinate
strictly between its bounds. Two such coordinates admit opposite sufficiently small
perturbations preserving the sum, contradicting extremality. An all-bound vertex
can be described by choosing any coordinate as the designated free coordinate.
Thus both margins admit the claimed patterns simultaneously; there is no assumption
that the same patterns remain optimal at other totals.

For row free coordinate `k` and column free coordinate `h`, write

```
r(S) = e_k S + b,    c(S) = e_h S + d.
```

The other entries of `b,d` are input bounds, while the free entries are negatives
of the sums of the other entries. The common feasible totals form a closed rational
interval `J`. The objective is

```
r(S)ᵀ C c(S)/S = α S + β + γ/S,
α = C_kh,
β = e_kᵀ C d + bᵀ C e_h,
γ = bᵀ C d.
```

Since this interval family contains a global optimizer, its minimum equals the
original global minimum. Its positive candidates are rational endpoints and, for
`α,γ>0`, the stationary point `sqrt(γ/α)` when feasible. If both coefficients are
negative the stationary point is a maximum. Zero coefficients give monotone or
constant functions; a constant family admits a rational feasible total.

## Zero endpoints are harmless

Whenever `0∈J`, nonnegativity and total zero force `r(0)=c(0)=0`. Hence `b=d=0` in
that pattern family, and the objective is simply `αS`. In particular its limit is
zero. More generally every feasible nonnegative matrix satisfies
`|⟨C,W⟩|≤max_ij|C_ij| S`, which establishes the same continuous extension independently
of its pattern. Zero is feasible exactly when all lower bounds vanish.

A pattern interval that is the singleton `{0}` contributes only zero. A positive
singleton is rational and is checked as an endpoint. Thus no unattained positive
infimum or missing zero case invalidates the candidate argument.

## Polynomial bit length and exact comparisons

The fixed-degree formulas above give polynomial bit bounds directly: `b,d` use
sums of input bounds, and the objective coefficients use sums of products of at
most one cost coefficient and two such bound expressions. This is stronger than
relying on an unrestricted claim that polynomially many arithmetic operations
always preserve polynomial bit length, which would be false under repeated squaring.

Each stationary total is the square root of a positive rational number of
polynomial bit length. The margins and matrix entries are rational expressions
in that same square root. Dividing by the positive total does not enlarge the field:
`1/sqrt(a)=sqrt(a)/a`. Thus every entry has the form `u+v sqrt(a)`, with polynomial
bit length.

Objective candidates are rational or `β+2 sqrt(αγ)` with `α,γ>0`. Comparing two
candidates reduces to comparing an expression with two rational square roots;
sign checks and at most two squarings decide its sign exactly with polynomial bit
complexity. Comparing a positive square root with a rational interval endpoint
requires a sign check and one squaring. No numerical tolerance is needed.

## The algorithm is FPT in the smaller dimension

After transposing to put the smaller dimension `m` in rows, there are at most
`m 2^(m−1)` row patterns. For each pattern the column objective weights are affine
in `S`. Their pairwise rational crossings partition the validity interval into
`O(N²)` pieces. A fixed index order resolves identically equal weights.

On each piece, continuous knapsack fills column capacities in one fixed order.
At most `N` cumulative-capacity thresholds change the column pattern, yielding
`O(N³)` subintervals per row pattern. Greedy orders adjacent to a crossing are both
optimal at the crossing, so checking closed endpoints loses no optimum; validity
intervals consisting of a single point can be checked directly. Sorting and
forming each interval description take polynomial time with exponent independent
of `m`. Together with the exact scalar minimizations, this proves a running time
of the form `m 2^m poly(n1,n2,B)`, as claimed.

## Stronger rational certificates for rational thresholds

Take the patterns at a positive optimizer whose objective is at most rational `t`.
For positive totals the threshold condition is equivalent to

```
q(S) = αS² + (β−t)S + γ ≤ 0,    S∈J.
```

This rational quadratic has a rational minimizer on its rational closed interval:
an endpoint, or `(t−β)/(2α)` when `α>0` and that stationary point lies in the interval.
All these numbers have polynomial bit length.

If its minimum is negative, the minimizing total is positive, since `q(0)=0`
whenever zero belongs to `J`. If its minimum is zero, the original positive witness
is also a minimizer. A minimizing positive endpoint is rational. A minimizing
interior point is the rational stationary point unless the polynomial is constant;
in the constant case any positive rational point in `J` works. This also covers
the possible minimum at zero without mistakenly using zero for a positive witness.

The resulting margins and matrix are rational with polynomial bit length. The
verifier can read the two bound patterns and the rational positive total,
reconstruct the margins, and check their bounds, totals, and `rᵀCc≤tS` using rational
arithmetic. It need not verify optimality. The zero matrix has its own immediate
certificate when its lower-bound and threshold conditions hold.

## Irrational exact optima really occur

Use a `2×2` identity cost matrix, fixed `r_0=c_0=1`, and remaining margins in `[0,1]`.
Equal totals force `r_1=c_1=S−1`, with `S∈[1,2]`. The objective is
`S−2+2/S`, uniquely minimized at `S=sqrt(2)` with value `2sqrt(2)−2`.
Every matrix optimizer therefore has irrational total. Rational certificates for
rational thresholds do not imply rational exact optimizers.
