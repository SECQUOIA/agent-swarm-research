# Four-block reach investigation

The first proved candidate from this investigation is
[the five-mode four-block reach result](../results/cia-five-mode-four-block-reach.md).
Its exact rational certificate checker passes, and
[independent review](review-cia-five-mode-four-block.md) found no unresolved issue.

## General sufficient inequality

For `n>=5`, write `P_i` for the best two-mode reach excluding `i`, and `Q_ij` for
the best two-mode reach excluding both `i,j`. For a three-element mode subset `S`,
consider

```
H_S = sum_{i in S}(P_i + sum_{j!=i} Q_ij).
```

If every such subset satisfies `H_S>=3nB_2`, where
`B_j=nE*((n/(n-1))^j-1)`, then the four-block prefix theorem follows. Indeed, for
the global three-block maximum `G` and excluded three-block maxima `N_i`, endpoint
inequalities and monotonicity give

```
(n-2)N_i >= nE+P_i+sum_{j!=i}Q_ij-G.
```

A maximizing triple with mode set `S` implies `N_i=G` outside `S`. Summing yields

```
sum_i N_i >= (n-3-3/(n-2))*G+(3nE+H_S)/(n-2).
```

The coefficient of `G` is positive for `n>=5`. The established three-block theorem
gives `G>=B_3` in the uncapped contradiction case. Substitution then gives
`sum_i N_i>=nB_3`, which is the required four-block aggregate. This recurrence was
derived by the CIA research agent and checked independently here.

The five-mode certificates alone do not prove the general weighted inequality. A
subsequent symmetry reduction now gives
[a certificate proof for every `n>=5`](../results/cia-general-four-block-reach.md),
described below. The general proof has passed independent review.

## Five-mode searches and the certificate construction

Twelve local nonlinear searches over eight equal-time intervals of piecewise-constant
simplex controls returned weighted objectives at least `42.1875008877`, close to the
uniform value `675/16=42.1875`. These searches used segmentwise inverse evaluations;
they were exploratory and are not evidence of exhaustive optimization.

A stronger event-order LP investigation sampled 2,000 admissible orders of five first
reaches and nine relevant excluded-pair maxima. Its smallest numerical bound was
`675/16`. This motivated dropping the unnecessary ordering of excluded-pair events.

The first partial-order LP kept only first-reach order, mass equations, pair endpoint
inequalities, and `Q_ij<=P_i`. Its optimum was `41.25`, below the desired bound. This
is a failure of that relaxation, not a counterexample control: it omits the relations
between allocations at many times.

Adding a global maximizing pair and the identities

```
Q_ij=M if {i,j} avoids the maximizing pair,
P_i=M if i avoids the maximizing pair
```

closed the gap in every case. There are only three maximizing-pair symmetry types
relative to `S`, combined with `5!=120` first-reach orders. The final 360 rational dual
certificates all give exactly `675/16`. Their standalone verifier reconstructs the
necessary constraints from integers and performs only exact rational arithmetic.
The final proof does not rely on the nonlinear searches or sampled event orders.

## Possible case reduction for larger mode counts

For fixed three-element `S`, a globally maximizing pair again has three symmetry
types. Within each type, permutations of indistinguishable indices need not produce
distinct first-reach orders. The respective orbit counts are

```
n!/[2!(n-3)!],  n!/[2!(n-4)!],  n!/[2!3!(n-5)!].
```

These follow by partitioning modes according to membership in `S` and membership in
the maximizing pair. For `n=5` their sum is 100, smaller than the 360 deliberately
redundant cases used in the saved checker. For fixed four-block reach, this reduction
would keep a direct higher-dimensional certificate search polynomial in `n`, although
it does not itself give uniform certificates or an analytic theorem for unbounded
`n`.

The one-sided five-mode result remains distinct from the separate heavy-mode and
all-light arguments for the two-sided three-switch CIA error.

## General-dimension certificate proof

The original partial-order LP was sampled in 300 cases for each `n=6,...,15`. Every
numerical optimum matched `3nB_2`. These samples suggested that the same constraints
could establish a dimension-independent theorem, but were not used as proof.

Inspection of the five-mode certificates showed identical first-root multipliers
`75/16`. The CIA agent conjectured the stronger bound

```
H_S >= 3n^2 E/(n-1) + 3n^2/(n-1)^2 * sum_{i!=z} R_i.
```

Subsequent LP reductions showed that this bound needs no first-root equations,
allocation variables at first reaches, or first-reach order. It holds for every
distinguished index `z` in a relaxation where all `R_i` are arbitrary nonnegative
numbers. Choosing a minimum actual first reach then uses the elementary inequality
`sum_{i!=z}R_i>=nE` to recover `H_S>=3nB_2`.

After fixing `S`, a global maximizing pair, and `z`, there are only ten membership
types. All other mode indices can be permuted. Convex averaging reduces each
auxiliary LP to a fixed number of variables. At most six indices remain individually
labeled, and each inequality involves at most three other indices. Thus its orbit
pattern stabilizes for `n>=9`. The inequality matrix is constant, the mass matrix
is affine in `n`, and the cleared objective vector is polynomial of degree at most
three.

Symbolic duals obtained from bases optimal at `n=12` satisfied exact identities but
some multiplier signs failed for larger `n`; those were not valid uniform proofs.
Instead, bases selected at the numerical parameter `n=1000` yielded ten exact
rational-function duals. In each case, a common positive polynomial denominator
turns the certificate into integer-polynomial identities. Nonnegative coefficients
after shifting `n=23+t` prove every required multiplier sign for all `n>=23`.

The remaining `n=5,...,22` require 179 finite symmetry cases. Each has an exact
integer certificate. All finite and polynomial certificates pass
`code/cia-distinct-reach/verify_general_four_block.py`, which uses only the standard
library. Numerical and symbolic solvers were used to discover certificates, not to
verify the final theorem. The saved certificate file is about 397 KB.

The resulting general proof supersedes the original five-mode argument as the
positive theorem, while that independently reviewed proof remains an additional
check with a different relaxation. The new proof gives the exact one-sided
three-switch minimax for every `n>=5`. A full two-sided consequence depends on the
separate heavy-mode theorem.
