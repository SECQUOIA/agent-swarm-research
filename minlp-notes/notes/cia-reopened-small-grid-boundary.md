# Exact five-cell, three-mode CIA worst case with two switches

Date: 2026-09-07. Status: finite integer proof and
[independent review](review-cia-reopened-small-grid.md) complete. The independent
checker enumerates all 14,400 candidate floor histories without importing the
author implementation and confirms the same 396 nonempty strict chambers. Source
scope independently checked by the literature reviewer.

[Lean topic 01](../formal/topics/01-switching-control/COVERAGE.md) also proves
the exact value for every positive cell width and measurable input, and its
continuous three-mode two-switch consequence `T/5`. Its finite proof checks
coverage by explicit schedules; the chamber counts and optimal-switch
histograms remain outside that formal guarantee. The linked verification
record retains the completed Lean checks.

**Theorem.** For three modes on five equal grid cells of length `Delta>0`, with
at most two switches at cell boundaries, the exact worst-case cumulative CIA
error is

\[
 \boxed{F^{\mathrm{grid}}_{3,2}(5\Delta)=\Delta.}
\]

The supremum includes arbitrary measurable simplex-valued relaxed profiles;
their cell averages suffice. This is a finite computer-assisted theorem with
integer arithmetic, not a numerical minimax estimate.

## Reduction to cumulative floor chambers

Scale to unit cell length. Write `a_{i,j}>=0`, `sum_i a_{i,j}=1`, and
`A_i(k)=sum_{j<=k} a_{i,j}`. For an integer word `w in {0,1,2}^5`, write `W_i(k)`
for its prefix occupation count. Its error equals

\[
 D(a,w)=\max_{i=0,1,2;\ k=1,\ldots,5}|A_i(k)-W_i(k)|.
\]

For an arbitrary measurable control with those cell averages, discrepancy of a
selected mode is nonincreasing inside its cell, and that of every other mode is
nondecreasing. Thus the endpoint expression also controls the entire trajectory.

First suppose every `A_i(k)` is nonintegral. Set `b_i(k)=floor(A_i(k))`. Since
`sum_i A_i(k)=k` and all three fractional parts belong to `(0,1)`,

\[
 \sum_i b_i(k)\in\{k-1,k-2\}.
\]

A word has `D(a,w)<1` exactly when

\[
 b_i(k)\le W_i(k)\le b_i(k)+1\quad\text{for all }i,k. \tag{1}
\]

Indeed an integer differs from a strictly nonintegral number by less than one
if and only if it is its floor or ceiling. Consequently all profiles with the
same cumulative floor arrays admit exactly the same error-below-one words.

## An exact test for possible chambers

For a partial floor history through prefix `ell`, let `V` be **all** integer
words whose prefix counts satisfy (1) through `ell`. If that history contains a
strictly nonintegral relaxed profile, then every coordinate `W_i(k)`, `k<=ell`,
attains both `b_i(k)` and `b_i(k)+1` among the words in `V`.

To prove necessity, use the standard integral-prefix-flow polytope. Each cell
supplies one unit to a mode's chain at that cell; the outgoing chain flow at
prefix `k<=ell` has integer lower and upper bounds `b_i(k),b_i(k)+1`. Other chain
arcs may have bounds `0,5`. The original fractional allocations and cumulative
sums form a feasible flow. Integer capacities and supplies imply that this flow
is a convex combination of integral flows. Each integral flow assigns every
cell to exactly one mode and hence represents a word in `V`. A coordinate of
the original profile strictly between two consecutive integers must therefore
have an integral vertex on each side; both endpoints occur in `V`.

Conversely, if every constrained coordinate attains both endpoints among the
words in `V`, the equally weighted average of all their cell allocations lies
strictly between those endpoints in every constrained coordinate. It is a
simplex-valued relaxed profile realizing the partial floor history. Thus the
criterion precisely identifies nonempty strict cumulative-floor chambers.
It does not require every individual cell rate to be strictly positive.

## Exhaustive integer certificate

The standalone checker

```
python code/cia_reopened/small_grid_boundary.py
```

uses only Python's standard library. Its enumeration is as follows:

1. Generate all `3^5=243` integer words, their integer prefix counts, and their
   switch counts.
2. At each prefix `k`, try all triples `b_i in {0,...,k}` whose sum is `k-1` or
   `k-2`.
3. Keep exactly those previously available words satisfying the new floor and
   ceiling bounds.
4. Discard a branch if no word remains, or if some coordinate at any prefix seen
   so far fails to attain both integer endpoints among the remaining words.
5. At every retained depth-five leaf, verify that at least one available word
   has at most two switches.

All operations are integer comparisons and finite set operations. The exhaustive
case counts are:

| Prefix depth | Nonempty strict floor histories |
| --- | ---: |
| 0 | 1 |
| 1 | 1 |
| 2 | 4 |
| 3 | 18 |
| 4 | 84 |
| 5 | 396 |

Among the 396 final chambers, the minimum feasible switch count is zero in
3 chambers, one in 138 chambers, and two in 255 chambers. No chamber needs more
than two switches. There are 720 empty-word prunes and 1,206 missing-endpoint
prunes. The case counts help detect accidental changes; the proof is the complete
enumeration and the exact branch criterion, not the counts alone.

This proves `D(a,w)<1` for every nonintegral cumulative profile.

## Boundary profiles and sharpness

To cover profiles with some integral prefix values, choose the constant rates
`v=(1/7,2/7,4/7)`, whose every cumulative coordinate is nonintegral at prefixes
`1,...,5`. Approximate any cell matrix `a` by `(1-epsilon)a+epsilon v`. Each
formerly integral coordinate moves immediately off the integer, and every other
coordinate can meet an integer only at finitely many parameter values. Hence a
sequence `epsilon->0` avoids all integral prefixes.

Each perturbed profile admits one of the finite collection of words with at
most two switches and discrepancy below one. Some word occurs infinitely often;
continuity of its discrepancy in the cell matrix gives discrepancy at most one
for `a`. Equivalently, the minimum over this finite collection is continuous.

For the reverse bound, take the pure word `(0,1,0,1,0)` as the relaxed control.
Every prefix allocation is integral. Any integer schedule with discrepancy
strictly less than one would have to match every prefix occupation exactly,
therefore match all five entries and incur four switches. Thus every schedule
with at most two switches has discrepancy at least one. The checker also
exhaustively verifies a matching error-one schedule for this witness.
Rescaling by `Delta` proves the theorem.

## Consequence for a published lower bound

Sager and Zeile, *On mixed-integer optimal control with constrained total
variation of the integer control*, final published Corollary 5, printed p.611,
asserts

\[
 \theta_{\max}\ge
 \frac{N+\sigma_{\max}+1}{3+2\sigma_{\max}}\,\bar\Delta
\]

for `1<=sigma_max<=N-2` and `n_omega>2`, with no congruence restriction on `N`.
[Final published PDF](https://link.springer.com/content/pdf/10.1007/s10589-020-00244-5.pdf).
At `N=5`, `sigma_max=2`, and `n_omega=3`, its right side is `8 Delta/7`,
whereas the exact value above is `Delta`. These parameters satisfy every stated
range restriction. This is a counterexample to that lower-bound statement as written.

The preceding Corollary 4, printed p.610, only gives attainment at grid lengths
`N=k(3+2 sigma_max)+sigma_max+2`; that condition is absent from Corollary 5.
The theorem above establishes a contradiction to the unrestricted statement,
not a complete replacement for its full parameter range. The corresponding
source caution and exact provenance are recorded in
[the reopening literature audit](cia-reopened-literature.md).
