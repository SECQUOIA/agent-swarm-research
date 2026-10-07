# Independent review: the treewidth-three strictness barrier

Date: 2026-10-02. Verdict: **PASS**. The reviewer read the actual
[reduction](../new-direction/strict-copositive-width3-barrier.md) and
inspected its [exact checker](../new-direction/check_strict_copositive_width3.py).
This review checks the mathematical reduction and its scope. A separate
literature audit is responsible for priority and comparison with existing
bounded-width copositivity results.

Every displayed summand is nonnegative on the nonnegative orthant.
The square terms give an explicit rational PSD part; the remaining
`z_i*w_i` terms give an entrywise nonnegative matrix with off-diagonal
entries `1/2`. Thus every instance is already certified SPN and copositive.
The reduction is about strictness, not membership in the copositive cone.

At a zero, all summands vanish separately. If `t=0`, nonnegativity and
`z_i+w_i=t` force both variables in each pair to vanish. The running-sum
relations and `y_0=0` then force all remaining variables to vanish.
Consequently a nonzero zero has `t>0`; complementarity implies
`z_i/t` is exactly zero or one, and the final sum gives the specified
SUBSET SUM equality. Conversely, any solving subset gives the stated
rational zero with `t=1`. These arguments prove the equivalence without
an approximation tolerance or a penalty weight argument.

When there is no subset, the form is positive on every nonzero orthant
vector. Continuity and compactness of the nonnegative unit sphere give
a positive margin, but no uniform numerical lower bound follows.
Complement SUBSET SUM therefore reduces to strict copositivity. This
is weak coNP-hardness; the binary-weight source does not establish strong
hardness. Squaring input integers only doubles their bit lengths, so the
reduction itself has polynomial encoding and construction cost.

The proposed bags cover every square's scope and every product term.
All nonzero off-diagonal entries, including positive ones, are therefore
covered. The articulation variable `t` occurs in every bag, each running
sum variable in consecutive path bags, and each `z_i` in its path and
attached leaf bag. Running intersection holds and maximum bag size is
four, proving treewidth at most three. The proof does not need equality
in that bound.

The large-block claim also checks for the stated positive weights and
positive target. The edges in
`t,z_1,y_1,z_2,y_2,...,z_n,y_n,t` have respectively nonzero coefficients
from the complementarity squares, the recurrence squares, and the final
target square. No other terms cancel them. This is a simple cycle on
`2n+1` vertices, contained in one biconnected block. Hence the bounded
articulation-block recognition result does not cover this growing family.

The product Hessians act on disjoint `(z_i,w_i)` pairs and have minimum
eigenvalue minus one. All other Hessian contributions are PSD, so the
full Hessian is at least `-I`. This does not bound negative curvature
divided by the positive growth margin: that margin can vanish on subset
instances and is not uniformly controlled on the strict instances.

Homogeneity permits every nonzero orthant zero to be scaled into the unit
box. Thus the same reduction makes uniqueness of the origin as a box
minimizer hard. The origin is nevertheless an explicit global optimizer
of value zero on every instance, with the displayed nonnegativity proof.
The note correctly avoids turning strictness/uniqueness hardness into
hardness of finding an optimizer or certifying the minimum value.

The checker author separately reported a successful run of
`python3 -B research-20261002/new-direction/check_strict_copositive_width3.py`:
49 constructions, 246 bags, 49 exact Gram identities for `Hessian+I`,
1,568 expansion checks, 1,044 scaled subset checks, 35 nonzero box-zero
witnesses, and one five-pivot shifted-PD check. Those are the checker
author's results, not a fresh run by this reviewer. The finite checks
support formulas and graph bookkeeping; the universal zero-set proof
establishes the reduction. No duplicate optimization tests, project-wide
checks, CI inspection, external search, or index edits were performed.
