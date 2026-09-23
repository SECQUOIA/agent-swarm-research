# Second independent audit: bilinear graph integer complexity

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Reviewed source: `results/bilinear-graph-binary-complexity.md`, including the
proposed extension from mixed-binary linear lifts to arbitrary mixed-integer
convex lifts. This is a mathematical audit, not a literature-priority audit.

## Verdict

The stated finite bounds, unequal-accuracy LP comparison, compact shared
expansion, and common-accuracy asymptotic are correct. The proposed extension
to the number of unrestricted integer coordinates in an arbitrary convex
lift is also correct. It requires the parity argument below, in place of
counting integer assignments. I found no counterexample to the theorem.

The number of continuous lift coordinates and the number or type of convex
constraints need not be bounded. Neither polyhedrality nor closedness of the
convex lifting set is needed for the lower bound.

## Complete check of the parity extension

Let `K` be any convex set in the coordinates `(x,w,y,z)`, with `z` having
`p` coordinates, and set

```
R = {(x,w): there exist y and z in Z^p with (x,w,y,z) in K}.
```

Assume graph containment and the componentwise error requirement stated in
the result. For each `eta in {0,1}^p`, let `T_eta` consist of all `x` in
the unit cube whose exact graph point admits a lift with `z mod 2 = eta`.
These sets cover the cube. For any `a,b in T_eta`, choose their respective
lifts. Convexity puts the midpoint of the lifts in `K`; its integer
coordinates are integral because both selected lifts have the same parity.
Its projection therefore belongs to `R`, and its `x` coordinate is in the
unit cube. The error requirement implies, for every edge,

```
|(a_i-b_i)(a_j-b_j)| <= 4 epsilon_ij.
```

This proof does not require any boundedness of `z`, and the selected lifts
need not have the same integer values.

Define `S_eta = closure(T_eta)` in the unit cube. These are compact and
cover the cube. The pairwise inequalities pass to the closures by continuity
(use a separate convergent sequence for each member of a pair). Thus no
measurability or projection-closedness assumption is required. The existing
coordinate-width argument applies unchanged to these sets. There are at
most `2^p` of them, yielding

```
1 <= sum_eta volume(S_eta) <= 2^p 2^(-L_20),
```

and hence `p >= ceil(L_20)`. Empty supports can be discarded. A support
with any zero coordinate width has zero full-dimensional volume; otherwise
all logarithms used in the LP argument are finite.

This proves the lower bound for every such mixed-integer convex
representation. The MILP construction proves the same upper bound for this
larger class, so its optimal integer-coordinate count has the same stated
finite interval and common-accuracy leading coefficient.

## Checks of the finite bounds and construction

- From `d_i d_j <= 20 epsilon_ij` and `0 < d_i <= 1`, the substitution
  `s_i = -log2(d_i)` satisfies both nonnegativity and the clipped edge
  constraints, including when `20 epsilon_ij >= 1`.
- The feasible region of each LP is nonempty and has a finite optimum;
  nonnegative objective coefficients prevent escape at a finite improving
  value. Isolated vertices may be assigned zero.
- For `p_i = ceil(s_i)`, the shared binary expansion covers every point of
  `[0,1]`. The endpoint 1 is represented by all binary digits equal to 1
  and residual `r_i = 2^(-p_i)`. If `p_i = 0`, the residual alone ranges
  over `[0,1]`.
- The product expansion is algebraically exact except for the residual
  product: writing the binary prefix as `b_i`, it uses
  `x_i x_j = b_i x_j + r_i b_j + r_i r_j`. It neither omits nor double
  counts the binary-prefix cross terms.
- Each auxiliary binary-times-continuous variable has a valid finite
  nonnegative bound, respectively 1 or `h_i`, so the indicated four
  inequalities are exact at integral binary values.
- The McCormick envelope over a nonnegative rectangle of side lengths
  `h_i,h_j` has maximum vertical error `h_i h_j/4`. After normalization,
  the lower envelope is `max(0,u+v-1)` and the upper is `min(u,v)`;
  subtracting `uv` shows both deviations are at most `1/4`.
- The LP constraints give `h_i h_j <= 4 epsilon_ij` when
  `epsilon_ij < 1/4`. For larger accuracy, `h_i h_j <= 1` suffices.
- All exact graph points lift simultaneously: use any valid shared
  expansions, exact binary products, and `q_ij = r_i r_j` on every edge.
  Thus coupling through the shared expansions creates no containment gap.
- There are `sum_i p_i` binary variables and `sum_i degree(i) p_i`
  binary-times-continuous auxiliaries. The stated linear size bound follows.
- The edge right-hand-side increase from `L_20` to `L_4` is at most
  `log2(5)`, including at the clipping threshold. Adding this number times
  any fractional vertex cover is therefore feasible. Summing its
  coordinates gives the stated additive comparison.
- With common `epsilon < 1/20`, scaling the fractional vertex-cover LP
  proves the exact identities for both `L_4` and `L_20`. Taking integer
  ceilings and adding at most one per vertex changes the result only by a
  constant depending on the fixed graph.

## Scope that must remain explicit

The lower bound needs containment of the entire graph over a
full-dimensional coordinate box. Arbitrary additional physical constraints
can invalidate that hypothesis. It also needs two-sided, componentwise
vertical accuracy on every feasible projected point whose `x` is in that
box. A scalar aggregate objective, an epigraph, a one-sided approximation,
or accuracy measured only on selected points is a different problem.

The integer-count lower bound concerns a representation by one convex
lifting set and integer coordinates. An external disjunction or other
discrete primitive cannot be left uncounted. An arbitrary collection of
convex sets without such a representation is not covered simply by calling
it a mixed-integer convex formulation.

No openness, strict convexity, rationality, bounded integer domains, or
finite inequality description is needed. Continuous lift dimension may be
arbitrary but finite, as conventionally understood in a formulation.

## A useful limitation on improving the geometric constant

The constant 5 in the coordinate-width lemma is valid. It cannot simply be
replaced by 4. An exact four-point counterexample has both coordinate widths
1 and pairwise coordinate-product distance `delta = sqrt(5)-2`:

```
r = (3-sqrt(5))/2,
t = (sqrt(5)-1)/2,
S = {(0,r), (1,t), (t,0), (r,1)}.
```

Here `r+t=1`, `t-r=rt=delta`, and direct enumeration of the six pairs
shows `|Delta x Delta y| = delta` for each pair. Consequently any universal
constant in `d_1 d_2 <= C delta` must satisfy

```
C >= 1/(sqrt(5)-2) = 2+sqrt(5).
```

I do not assert that `2+sqrt(5)` is sufficient. The existing constant 5
needs no change, and this example does not challenge any claimed theorem.

## Final reread and rational preprocessing audit

The updated result, now titled *Integer dimension of simultaneous bilinear
approximation*, was reread on 2026-09-05. The parity extension is implemented
correctly. The subsequently added **Rational preprocessing** paragraph also
passes this independent audit.

For positive rational `epsilon=A/B`, the demand is the least nonnegative
integer `d` for which `4 A 2^d >= B`. It can be found by exact integer
comparisons, and its magnitude is bounded by the binary input length up to
an absolute constant. Writing the original clipped demand as `c_e`, one
has `c_e <= d_e < c_e+1` unless `c_e` is integral, in which case the increase
is zero. Thus adding any feasible fractional vertex cover to an optimum
of `L_4` yields a feasible solution of the rational-demand LP. The bound
`L_20+n+tau*(G)(1+log2(5))` follows exactly as claimed.

For completeness, polynomial output length does not rely only on the
rational LP solver's representation size: if `D=max_e d_e` (take `D=0`
for no edges), assigning `s_i=D` at every vertex is feasible, so an optimum
has objective at most `nD`. Every nonnegative optimal coordinate is then
at most `nD`, and every chosen `p_i=ceil(s_i)` is polynomially bounded in
the input length. There are polynomially many dyadic coefficients, each
with polynomial denominator encoding length. Standard rational linear
programming therefore gives polynomial bit preprocessing and a polynomial
bit size explicit MILP, as stated.
