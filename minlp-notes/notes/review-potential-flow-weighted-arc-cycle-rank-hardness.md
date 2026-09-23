# Independent audit: weighted arc-flow hardness at global cycle rank two

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** I independently reviewed
[the weighted-arc candidate](potential-flow-weighted-arc-cycle-rank-hardness.md).
Its connected theta construction proves the stated discrete-resistance
hardness for a linear objective on two arc flows. The no-instance gap,
integer encoding, NP/coNP membership, and rank-one positive boundary
are correct. This review concerns mathematical correctness; the separate
source audit must assess priority.

## Physical graph and objective

With `a=x_02` and `q=x_23`, the remaining displayed flows give net
nominations `(4,-4,3,-3)` exactly. Expanding the equality of the outer
source-to-sink drops gives

```
-a^2+2aq+18a-q^2-10q-9=0.
```

Substituting `a=q+9-2u` reduces this to
`4(2q-u^2+18)=0`, confirming the selected branch
`u=sqrt(2q+18)`. On `q in [0,3]`, its derivative satisfies
`0<a'(q)<1`, and all four outer flows are strictly positive by the
endpoint and explicit bounds in the candidate. The alternative algebraic
branch need not be analyzed: the selected branch will give a valid
physical solution, whose uniqueness excludes any second physical state.

The cross drop is `16-8a(q)`, so the residual
`theta q^2+8a(q)-16` is strictly increasing on `[0,3]`. At zero it is
negative, since `a(0)<2`; at three it is positive, since `a(3)>2`.
For every positive `theta` there is therefore one root in `(0,3)`.
The resulting flows obey conservation and both independent cycle
equations. They determine consistent potentials, and strict convexity
of the passive-flow energy makes them the unique physical state.

The two-arc objective has the exact identity

```
-9a+5q=-9/2-2(sqrt(2q+18)-9/2)^2.
```

Its peak is `-9/2` and occurs exactly at
`q=a=9/8`, with `theta=448/81`. I verified the peak and both claimed
rational endpoint states symbolically, including their objective values
`-37/8`. The objective is a linear functional of flows; the squared
performance curve arises from the physical equations, not from a
nonlinear upper objective.

## Discrete series encoding

All internal vertices of the uncertain cross path have zero nomination,
so every path edge carries the same signed flow. Their drops add to the
law with resistance equal to the sum of selected edge resistances.
The proposed options give

```
theta=(224/81)(1+sum_i a_i sigma_i/K).
```

Thus its value is the unique maximizing `448/81` exactly for a target
Subset-Sum selection. The first edge on the subdivided path supplies
the objective's `q` coordinate without adding any objective terms.

For `n` path edges, the graph has `n+3` vertices and `n+4` edges, so its
global cycle rank is two. Vertices 2 and 3 have degree three; all other
vertices have degree two. It remains simple when `n=1` and after any
further subdivision. The four original nominations stay fixed and all
new ones are zero. The resistance choices occur on the uncertain cross
edges; the four outer resistances are fixed.

Positive input items and positive `K` are assumed. Immediately decidable
cases, including `K>S`, can map to fixed yes/no instances as described.
The displayed fixed theta values do provide such outputs. No growing
nomination coefficient is used in this base reduction.

## Gap and threshold directions

Subtracting the cross equation at the peak from its equation at a physical
point gives exactly the candidate's equation (5). In a no instance,
`q=q*` is impossible. Its denominator bracket is positive, because the
secant slope of `a` is in `(0,1)`. Moreover,

```
|theta-theta*|>=224/(81K)>2/K,
(q*)^2>1,
theta(q+q*)+8 secant <5theta+8,
5theta+8<=23+15S/K.
```

With `H=23K+15S`, these inequalities imply
`|q-q*|>2/H`. Since `sqrt(2q+18)+9/2<10`, rationalizing the square
roots gives `|u-u*|>2/(5H)`. Therefore the objective deficit is strictly
greater than `8/(25H^2)`, which is greater than
`Delta=1/(4H^2)`.

The peak threshold `-9/2` is attained in a yes instance and is never
attained in a no instance. For robust upper bounds use
`J=-9/2-Delta/2`: a yes instance has a strict violation, whereas every
no-instance scenario satisfies the limit strictly. Hence complements
have the claimed orientation. Absolute value error below `Delta/4`
separates the two maximum-value cases. If a feasible resistance witness
is within that tolerance of the optimum in a yes instance, it must itself
be a target subset, since every non-target scenario has the same gap.

## Encoding and the two different scalings

Every coefficient and the gap have polynomial binary length. Scaling all
resistances by `81nK` gives the listed positive integer options and outer
resistances. Under a common positive resistance scaling the physical flow
does not change; all potential differences receive that factor. Thus
this scaling leaves the linear arc objective and its gap unchanged.

For the separate constant absolute-error result, scale nominations by
`M=16H^2`. The quadratic laws then have flows scaled by `M` and potentials
scaled by `M^2`, with the resistances unchanged. The objective scales
linearly by `M`. Its no-instance deficit becomes greater than four, so
an absolute-error-one estimate distinguishes the cases at the scaled
peak minus two. This retains the fixed coefficients `(-9,5)` but gives
large nominations. It proves the stated unnormalized absolute-error
hardness, not fixed-small-nomination constant-error hardness.

The numbers still have polynomial binary encoding length. Neither this
scaling nor the original Subset-Sum reduction establishes strong
NP-hardness, a fixed relative approximation gap, or hardness under
uniformly bounded numerical inputs.

## Exact membership and rank boundary

For any fixed global rank and fixed rational nomination/resistance
scenario, a spanning-tree representation uses only that fixed number
of circulation coordinates. Edge flows are affine rational functions.
On their polynomially many sign cells, cycle consistency consists of
rational quadratic equations in fixed dimension. The linear arc objective
is affine in the same variables. Every physical flow is bounded by total
positive nomination, giving finite rational circulation bounds.
Fixed-dimensional real algebra therefore evaluates and compares the
unique physical objective exactly in polynomial bit time.

Consequently a nondeterministic certificate needs only one listed
resistance choice per uncertain edge. A deterministic verifier computes
the objective and checks either a weak target threshold or a strict
upper-limit violation exactly. This proves NP membership for the
existential problems and coNP membership for robust upper-limit
satisfaction on the fixed-global-rank class. Combined with the two
thresholds above, it proves the claimed rank-two completeness statements.
No independently supplied large algebraic-state certificate is needed.

For a connected rank-one graph and fixed nominations, all bridge flows
are fixed and all cycle freedom is one scalar `q`. Thus any linear
arc-flow objective is `Aq+C` with rational `A,C`. If `A=0`, it is
constant. Otherwise optimizing it is equivalent to maximizing or
minimizing one cycle-edge flow, using a chord coordinate or reversing
the optimization direction. A unicyclic graph is series-parallel, so the
reviewed finite-resistance arc-extremum theorem applies. Its exact
endpoint-scenario recovery supplies an optimizer as well as the value.
Rank zero is immediate from conservation.

For continuous resistance intervals at any fixed global rank and fixed
nominations, circulation coordinates form the fixed core. Each
resistance interval is a scalar polyhedral leaf, and cycle equations give
a fixed number of aggregate constraints with quadratic core coefficients.
The weighted arc objective is affine in the core. This is exactly within
the reviewed fixed-core theorem. It justifies the continuous/discrete
comparison but does not extend the theorem to arbitrary nomination
uncertainty or unbounded global rank.

## Checks and final scope

I independently expanded the outer polynomial, completed-square
objective, and three rational physical states with exact SymPy
arithmetic. I also reran
`code/potential_flow_mpd/weighted_arc_cycle_rank_hardness_checks.py`.
It passed three symbolic identities, three exact theta states, and 1,778
scenarios across 40 instances, including 43 target subsets. Its maximum
full physical residual was approximately `9.60e-83`.

I suggested making the standard connected-graph/balanced-nomination
convention explicit and saying that each **uncertain** edge has two
options, since outer resistances are fixed. The construction and proofs
already use exactly those assumptions. No substantive defect remains.

## Positive throughput objectives and unit coefficients

The positive two-arc variant also passes. Conservation gives
`x_03=4-x_02`, so
`9x_03+5x_23=F+36`. Its peak is `63/2` and its gap is unchanged.
Both selected flows are strictly positive in every theta scenario.
After nomination scaling by `M`, the shift is `36M`, as required.

I also checked the author's subdivision giving a unit coefficient on
every arc. Replace the `0->3` edge by `9n+1` edges with total resistance
one. Replace the cross path by `5n` edges: `4n` fixed resistances
`28/(81n)` and `n` uncertain pairs
`{112/(81n),112/(81n)+224a_i/(81K)}`. Their total is exactly the
previous effective cross resistance. The sum of all oriented arc flows is

```
(9n+1)(4-a)+a+(a+3-q)+(1-a+q)+5nq
=nF+36n+8.
```

Its peak is `(63n+16)/2` and its no-case deficit is at least `n Delta`.
The resulting graph has `14n+4` edges and `14n+3` vertices, retaining
global rank two and maximum degree three. Its orientation is acyclic,
and every physical edge flow is positive by the verified theta bounds.
Thus the same expression is also the sum of absolute arc flows.

Common resistance scaling by `81nK(9n+1)` gives integer data: each
`0->3` subdivision edge becomes `81nK`, fixed cross edges become
`28K(9n+1)`, and uncertain cross options become
`{112K(9n+1),112K(9n+1)+224n(9n+1)a_i}`. Other outer resistances receive
that common factor, with the resistance-two edge receiving twice it.
Flows and objective values are unchanged. These corollaries introduce no
new gap or encoding defect.
