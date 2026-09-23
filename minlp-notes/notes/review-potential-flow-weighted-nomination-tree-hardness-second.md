# Second independent audit of weighted-nomination hardness on trees

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`, independent of
the author and first reviewer.

Reviewed: [the weighted-nomination tree construction](potential-flow-weighted-nomination-tree-hardness.md).

**Verdict: PASS.** The passive-tree representation, NP-completeness on
the specified family, constant absolute gap, and rational near-witness
rounding argument are correct. The result concerns a weighted potential
objective with growing support, not a prescribed pairwise pressure
difference. The continuous knapsack mechanism is prior work; a direct
primary reference is recorded below.

## Tree and physical representation

The backbone and its distinct attached leaves form a connected simple
tree on `2n` vertices. Internal backbone vertices have degree three,
endpoints degree at most two, and leaves degree one. For `n=1` the
construction is just an edge, so there is no exceptional graph defect.
Every resistance is positive rational data of polynomial encoding length.

The exact root injection and leaf withdrawal intervals impose precisely
`0<=y_i<=w_i` and `sum y_i=K`. Since `0<K<sum w_i`, this polytope is
nonempty. On the tree, conservation uniquely fixes each leaf flow to
`y_i` and each backbone flow to the sum of its downstream withdrawals.
All these flows are nonnegative. Their potential drops are therefore
their resistance times their squared flow; the tree has no further cycle
equations to impose. Choosing one reference potential and summing drops
constructs the unique potentials up to a common constant.

Rational nominations produce rational flows and potential differences
with polynomial encoding length. The physical model requires no zero
resistance, no active element, and no extra pressure constraint.

## Weighted objective and the reduction

All backbone and leaf vertices are distinct. Thus the objective
`sum_i(pi_v_i-pi_l_i)` has exactly one coefficient `+1` at every backbone
vertex and one `-1` at every leaf. Its coefficient sum is zero, so it is
independent of the chosen potential reference. Its support is `2n`.

Applying the individual leaf laws gives exactly

```
F(y)=sum_i y_i^2/w_i.
```

There is no contribution from backbone pressure drops to this functional.
For `0<=y_i<=w_i`, one has `y_i^2/w_i<=y_i`, with equality only at an
endpoint. Since all deficits are nonnegative, `F(y)=K` occurs exactly
when every coordinate is zero or its upper bound. Such a feasible vector
is exactly a target subset. Hence the threshold reduction is correct.

Restricting the source to `0<K<W` preserves hardness by deciding trivial
targets first and mapping them to the stated fixed yes/no instances.
The output graph has linear size, and all nomination bounds, resistances,
and the threshold have polynomial binary encoding length.

## Vertices and NP membership

The feasible capped simplex is compact, and its continuous convex objective
attains a maximum at a vertex. This follows directly by expressing any
point as a convex combination of vertices and applying convexity.

A vertex has at most one coordinate strictly between its bounds. If
two coordinates were interior, small opposite perturbations would remain
feasible in both directions, contradicting extremality. Every remaining
coordinate is zero or its integer upper bound. The possible last coordinate
equals `K` minus a sum of integer upper bounds, so it too is an integer.
Here an interior coordinate is not a noninteger coordinate; the draft
explicitly explains that convention when it uses the word fractional.

An integer maximizing vertex therefore supplies a polynomial-size
certificate for attainment of any rational threshold on this specified
family. The verifier checks its bounds, sum, and the rational objective.
Denominators can be combined with polynomial bit length, since the product
of all input weights has bit length at most their total input length.
No algebraic physical-state certificate is needed. This establishes NP
membership and, with the reduction, NP-completeness.

The argument does not establish NP membership for every arbitrary
weighted-potential optimization problem on every tree; its stated family
is sufficient for the claimed theorem.

## Constant absolute gap

On a no instance, an optimal vertex cannot consist entirely of endpoints,
so it has exactly one interior coordinate. This coordinate is an integer
`r` satisfying `1<=r<=w_i-1`, which implies `w_i>=2`. The other coordinates
have zero deficit. The remaining deficit satisfies

```
r-r^2/w_i=r*(w_i-r)/w_i
 >=(w_i-1)/w_i>=1/2.
```

The middle inequality holds because the integer product `r*(w_i-r)`
is minimized at `r=1` or `r=w_i-1`. Thus the optimum is at most `K-1/2`.
This bounds all feasible points because some vertex attains the global
maximum; it is not merely a gap on a selected subset of candidate points.

An absolute-error estimate with error at most `1/8` separates the cases
by comparison with `K-1/4`. A certified feasible rational nomination
within `1/8` of optimum has value at least `K-1/8` on a yes instance,
while no feasible no-instance point exceeds `K-1/2`. Its objective can
be evaluated exactly as a rational number.

## Direct near-witness rounding

For any feasible point, set `m_i=min(y_i,w_i-y_i)`. Then

```
y_i-y_i^2/w_i=m_i*(1-m_i/w_i)>=m_i/2,
sum_i m_i<=2*(K-F(y)).
```

Rounding every coordinate to its nearest endpoint changes its value by
exactly `m_i`; either endpoint works in a tie. If the objective deficit
is less than `1/4`, the rounded sum differs from `K` by less than `1/2`.
Both sums are integers, so they agree exactly. A feasible `1/8`-optimal
nomination in a yes instance meets this condition and therefore produces
an exact subset. The rounding argument does not assume the near-optimal
point itself is a vertex or integer.

## Integer resistance scaling and scope

Let `P=prod_i w_i`. Multiplying all resistances by `P` makes every
backbone resistance `P` and each leaf resistance `P/w_i` a positive
integer. Conservation and physical flows do not change; all potentials
and the objective scale by `P`. Scaling the threshold accordingly preserves
the reduction, and the absolute gap grows to at least `P/2`. The bit
length of `P` is polynomial even though its numerical value can be large.

Thus the claims remain weak-hardness claims, not strong hardness or
hardness under normalized objective scales. The threshold grows with `K`,
so the constant absolute gap does not imply a constant relative gap.

The growing objective support is essential to the stated comparison with
the repository's positive results. The construction optimizes a sum of
leaf potential drops over nomination uncertainty. It has many objective
terminals despite having no cycles. It does not contradict algorithms for
one prescribed pressure difference, or for resistance uncertainty with
fixed nominations on trees. In the latter setting, flows are fixed and
the weighted objective is linear in the independent resistances.

For a process-network interpretation, this is an aggregate potential-loss
performance objective over multiple delivery branches. In the gas model
described by [Thürauf, Section 2](https://optimization-online.org/wp-content/uploads/2020/05/7803-1.pdf),
the potential represents squared pressure for horizontal pipes. Thus the
present functional should not silently be renamed either a single pressure
difference or an energy-consumption objective. The obstruction applies to
the explicitly stated weighted performance criterion, with no additional
operating limits.

## Primary predecessor and independent checks

[Levi, Perakis, and Romero (2014)](https://www-2.rotman.utoronto.ca/facbios/file/CKP%20ORL.pdf),
*A continuous knapsack problem with separable convex utilities*, Operations
Research Letters 42, 367–373, Proposition 1 on page 368, explicitly proves
NP-hardness by a Subset-Sum reduction with convex quadratic utilities and
endpoint deficits. Their preceding formulation explains extreme-point
attainment. Their displayed utility differs from `y_i^2/w_i`; this is a
direct predecessor for the combinatorial mechanism, not a source for the
passive comb-tree representation or its specific objective coefficients.

The candidate already disclaims novelty for that mechanism. It should
credit this primary paper explicitly while keeping the network interpretation
and the broader literature comparison separate.

I independently enumerated exact capped-simplex vertices for 2,784 small
instances: two through four weights, each between one and four, and every
nontrivial integer target. Rational arithmetic verified the optimum/subset
equivalence and the no-case gap for every instance. These checks support
the proof but are not its basis.
