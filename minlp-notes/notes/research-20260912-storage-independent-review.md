# Independent mathematical review of the retained storage example

Date: 2026-09-12. **Verdict: the retained mathematical claims pass.** No
correction to the `9/8` gap, the sharp unweighted or weighted coefficients, or
the stated complexity conclusions is required. The accompanying script passes
within its actual scope. Its coverage is narrower than the full argument;
the distinctions below should remain explicit.

I independently derived the claims in
[the research note](research-20260912-energy-opportunities.md) and inspected and
ran [the exact arithmetic script](../code/research_20260912/storage_balance_perspective_gap.py).
This review covers the retained nonlinear example, inequalities (1)--(3), their
assumptions, and the complexity statements about (3). It does not review
publication novelty, the literature comparisons, or the discarded alphabet
proposal as a candidate theorem. No author files or literature records were
changed, and no new external source was needed for this mathematical audit.

| Claim | Result |
| --- | --- |
| Membership of the displayed mean in the full linear trajectory hull | Pass: an explicit feasible six-trajectory decomposition includes the mode and state coordinates. |
| Exact local state-and-cost hull value `16/75` | Pass: valid perspective lower bounds and explicit attaining local mixtures agree. |
| Exact full-trajectory epigraph value `6/25` and ratio `9/8` | Pass: a convex valid inequality supplies the lower bound, and the six-trajectory mixture attains it. |
| Sharp unweighted mean-zero inequality | Pass for every integer `n >= 2`, including vectors with zero entries. |
| Sharp weighted coefficient | Pass for `n >= 2` and strictly positive weights, including partial supports. |
| PARTITION reduction and fixed-number-of-weight-types algorithm | Pass for exact computation with an explicitly listed rational weight vector. |
| Script as a complete verification of the above | Limited: it verifies the main six-trajectory arithmetic and finite sign-count checks, but not the local state-and-cost mixtures or weighted result. |

Write `z=(e,c,d,delta)` and let `G` be the convex hull after adding the full
quadratic cost epigraph. The exact value reviewed here is
`min {Q : (bar z,Q) in G}` at the specified mean. The relaxation value is at
that same fixed mean. Thus `9/8` is a pointwise convexification gap; it is not
a reported solver gap or the ratio of the unconstrained global minima of two
dispatch problems.

For each of the six stated schedules, the cumulative states lie between
`1/10` and `9/10`, the final state is `1/2`, and each increment has magnitude
at most `2/5`. Taking `c=max(x,0)`, `d=max(-x,0)`, and `delta=1` exactly for
positive increments satisfies the binary mode bounds. There are no zero
increments in these schedules, so the possible ambiguity of the idle mode
does not enter this witness.

In any fixed period, averaging the six schedules gives one positive increment
`2/5`, two positive increments `1/5`, and their three negative counterparts.
Consequently `bar c=bar d=2/15` and `bar delta=1/2`. Every mean increment is
zero, so the common initial state and the linear state equations give
`bar e_1=bar e_2=1/2`. This proves membership in the exact linear trajectory
hull, including all coordinates claimed in the note. Each schedule has cost
`(2/5)^2+2(1/5)^2=6/25`.

The local hull claim requires an argument beyond substituting into a
perspective formula. For any mixture of feasible one-period points, charging
is confined to the atoms with `delta=1`. Cauchy--Schwarz on these atoms gives

\[
\mathbb E[c^2]\ge \frac{(\mathbb E[c])^2}{\mathbb E[\delta]}.
\]

Applying the same argument to discharging gives the other perspective term.
At the proposed means their sum is `16/225` in every period. This lower bound
is valid even when the state variables and the appropriate fixed endpoint
are included in the local hull.

To attain it, use equal weights on increments `+4/15` and `-4/15`, with the
corresponding binary modes. For periods one and two, both atoms start at
`1/2`, and their end states are `23/30` and `7/30`. For period three, the
charging atom starts at `7/30` and the discharging atom starts at `23/30`;
both end at `1/2`. All powers satisfy the `2/5` limit, all states satisfy
their bounds, and each atom costs `16/225`. Each local mean has both endpoint
states equal to `1/2` and the required charge, discharge, and mode means.
The sum `16/75` is therefore the exact value in the intersection of these
local epigraph hulls and the linear trajectory hull at this point.

These local witnesses are legitimate despite their incompatible state
distributions: the intersection identifies the shared state coordinates,
which are means. For example, the first local mixture has a two-point end
state distribution, whereas the second has a deterministic start state.
The claimed relaxation does not identify these distributions.

For the unweighted inequality, take a nonzero vector with zero sum, let
`W=sum |x_t|`, and let `p,q` count its strictly positive and strictly negative
entries. Both counts are positive. Each sign carries mass `W/2`, so

\[
\sum_t x_t^2\ge\frac{W^2}{4p}+\frac{W^2}{4q}.
\]

Increasing either positive count decreases this coefficient. Its minimum
over `p+q <= n` therefore uses all `n` coordinates. With `p+q=n`, the
coefficient is `n/(4pq)`, minimized by maximizing `pq`; this gives
`p=floor(n/2)`, `q=ceil(n/2)` and the stated
`kappa_n=n/(4 floor(n^2/4))`. Giving each positive entry value `W/(2p)` and
each negative entry value `-W/(2q)` attains equality. The zero vector
satisfies the inequality directly. This establishes both validity and
sharpness without relying on the script's finite enumeration.

On every feasible cyclic storage trajectory, complementarity makes
`c_t+d_t=|x_t|` and `c_t^2+d_t^2=x_t^2`. The full epigraph therefore lies in
the convex set

\[
Q\ge\kappa_n\left(\sum_t(c_t+d_t)\right)^2.
\]

Its convexity ensures validity on `G`. Equivalently, Jensen's inequality
applied to throughput in any trajectory mixture proves the same statement.
At the displayed mean the throughput is `4/5`, so the bound is
`(3/8)(4/5)^2=6/25`. The six feasible trajectories attain this bound with
identical individual throughput and cost. This proves the exact full-hull
value and `(6/25)/(16/75)=9/8`.

For an explicit conic representation, use the rotated cone convention
`2uv >= w^2`, `u,v >= 0`, with
`(u,v,w)=(Q,1/(2 kappa_n),sum_t(c_t+d_t))`. This also confirms the stated
second-order-cone representability without requiring irrational constants.

For the weighted inequality, set `r_t=1/a_t>0` and `A=sum r_t`. For a nonzero
zero-sum vector with positive support `P` and negative support `N`, weighted
Cauchy--Schwarz gives

\[
\sum_t a_t x_t^2\ge
\frac{W^2}{4}\left(\frac1{A_P}+\frac1{A_N}\right).
\]

If some entries of `x` vanish, assign their indices to either sign group to
obtain a full partition `P',N'`. Each reciprocal-weight sum can only
increase, so the displayed coefficient can only decrease. This supplies the
detail behind the note's sentence about zero entries: restricting the search
for the best universal coefficient to full partitions is valid. For a full
partition the coefficient is

\[
\frac14\left(\frac1{A_P}+\frac1{A-A_P}\right)
=\frac{A}{4A_P(A-A_P)}.
\]

Minimizing it gives exactly (3). For any maximizing partition, choose

\[
x_t=\begin{cases}
W r_t/(2A_P),&t\in P,\\
-W r_t/(2(A-A_P)),&t\notin P.
\end{cases}
\]

This vector has zero sum, absolute mass `W`, and equality in both weighted
Cauchy--Schwarz bounds. Every entry is nonzero when `W>0`. It establishes
sharpness over all real zero-sum vectors. As a check on an unequal-weight
edge case, for `n=2` this reduces to `(a_1+a_2)/4`, exactly the coefficient
obtained by substituting `x=(u,-u)` directly.

The complexity argument follows from
`A_P(A-A_P)=A^2/4-(A_P-A/2)^2`. Thus `kappa(a)=1/A` holds exactly when a
nonempty proper subset of the reciprocal weights sums to `A/2`. From a
positive-integer PARTITION instance `b_1,...,b_n`, produce
`a_t=1/b_t`. This is a polynomial-size rational encoding and proves the
stated NP-hardness of exact coefficient computation. It does not by itself
establish strong NP-hardness or any hardness of approximating the coefficient,
and the note does not claim either conclusion.

For a fixed number `K` of distinct weights with multiplicities
`n_1,...,n_K`, enumerate the subset counts `k_j=0,...,n_j`, omitting the empty
and full subsets. There are `product_j(n_j+1) <= (n+1)^K` combinations.
Each reciprocal-weight sum and comparison can be performed exactly with
polynomial bit complexity. This is polynomial for constant `K` when the
`n` weights are explicitly listed, as in the note. If multiplicities were
instead given in a compressed binary encoding, the same enumeration would
not establish a polynomial bound in that different input size.

The stated limits survive adversarial checks. In particular, a mixture of
the noncyclic trajectories `x=(1/10,1/10,1/10)` and its negative, each starting
at `1/2`, has equal mean initial and final states and respects the stated
state and power bounds. Its cost is `3/100`, but the cyclic cut would demand
`27/800 > 3/100`. Thus equality of endpoints only in the mean is insufficient.
Likewise, with standing factor `rho=4/5`, constant state `e_t=1/2` requires
the positive increment `1/10` each period and gives the same violation.
The zero-sum hypothesis must hold for the actual internal increments of
every trajectory to which the cut is applied. The even/odd coefficient
comparison in the note is correct. A universal sharp coefficient need not
be sharp for every additional collection of storage state and power bounds;
the six-trajectory construction separately establishes attainability in
this particular storage instance.

I ran the author's script with Python `3.13.11`; it passed. I also ran separate
exact `Fraction` checks of all three two-atom local state-and-cost witnesses,
all six full trajectories including their state means and individual costs,
and eight weighted cases. Those cases included equal weights, heavily
unequal weights, arbitrary positive rational weights, equal-partition and
unequal-partition instances, and `n=2`. Direct enumeration checked 552
zero-sum integer vectors, including zero entries and partial supports,
against the weighted inequality; all checks passed. Attaining vectors for
each weighted case also gave exact equality. These are regression checks;
the derivations above establish the general claims.

The only correction recommended is to keep the verification description
precise. The current author script directly asserts charge, discharge, and
mode means; it does not directly calculate or assert the state means. It
checks the average cost rather than asserting the cost of each individual
schedule. Its generated schedules make the missing facts straightforward,
and this independent review checked them explicitly, so these are coverage
limitations rather than mathematical failures. It also does not construct
the local epigraph witnesses or test (3), the latter already disclosed in
the note. If stronger executable coverage is wanted, these are the useful
additional checks; a larger finite sign-count range would not replace them
or strengthen the general proof.

Reviewed source snapshots, before any subsequent author revisions:

```text
6caffbc0c8d7b42f6e7bbf19aa0ff13b356c56e661154517a3ec26c59b59038e  notes/research-20260912-energy-opportunities.md
4194a15ae30ca747c134211956f768caad8b75a48f7bbfc12e940bd3a2078bdf  code/research_20260912/storage_balance_perspective_gap.py
```
