# A factor-three gap for nonnegative binary payoffs at incidence treewidth two

Date: 2026-09-04. Status: explicit counterexample and graph-family extension independently checked;
written review is linked below. No literature priority is claimed for the construction.
It refutes the proposed general-factor upper bound two at incidence treewidth two.
It does not refute the separate positive-monomial conjecture.

## The precise comparison

Let binary variables `X_i` have fixed singleton means `x_i`, and let each factor
`g_e:{0,1}^e→R_+` be a nonnegative payoff on its scope `e`. Define

```
T = Σ_e max{E[g_e(X_e)] : E[X_i]=x_i for i∈e},
H = max{E[Σ_e g_e(X_e)] : E[X_i]=x_i for every i}.
```

Different factors in `T` may choose different joint distributions with the same
singleton marginals. The maximization in `H` uses one common joint distribution.
The incidence graph has one node per variable and one node per factor, with
variable-factor edges indicating scope membership. Its treewidth is the graph
parameter used here; it is not the treewidth of the primal variable graph.

## Six fair variables and three factors

Use six variables, each with mean `1/2`, grouped into pairs

```
(X_AB,1,X_AB,2), (X_BC,1,X_BC,2), (X_CA,1,X_CA,2).
```

For brevity, `AB equal` means the first pair has equal bits, and `AB unequal`
means it has unequal bits; use the same convention for the other two pairs.
Define

```
g_A = 1[AB equal   and CA equal],
g_B = 1[AB unequal and BC equal],
g_C = 1[BC unequal and CA unequal].
```

Every factor is zero-one valued, has arity four, and shares exactly two variables
with each of the other factors. Every variable occurs in exactly two factors.

### Separate factor optima

Each factor has at least one satisfying assignment. Its payoff is unchanged when
all of its bits are complemented, since equality and inequality of a pair are
both preserved by complementation. Put probability one half on a satisfying
assignment and one half on its complement. This gives every bit mean one half
and makes the factor equal to one almost surely. Since no factor exceeds one,
each local maximum is exactly one. Therefore

```
T=3.
```

### Global optimum

No two factors can equal one in the same assignment:

- `g_A` and `g_B` demand opposite parities on the `AB` pair.
- `g_B` and `g_C` demand opposite parities on the `BC` pair.
- `g_C` and `g_A` demand opposite parities on the `CA` pair.

Thus `g_A+g_B+g_C≤1` pointwise, which implies `H≤1` for every global law.
The global law assigning probability one half to the all-zero vector and one
half to the all-one vector has all required means and gives `g_A=1` almost surely.
Consequently

```
H=1,       T/H=3.
```

### Exact incidence treewidth

A tree decomposition consists of a central bag `{A,B,C}` and six leaf bags:

```
{A,B,X_AB,1}, {A,B,X_AB,2},
{B,C,X_BC,1}, {B,C,X_BC,2},
{C,A,X_CA,1}, {C,A,X_CA,2}.
```

Attach every leaf bag directly to the central bag. Each incidence edge lies in
a leaf bag. Each variable appears in one bag; bags containing a given factor
form a connected star through the central bag. Every bag has size three, so the
width is at most two. The incidence graph contains the four-cycle through
`A,X_AB,1,B,X_AB,2`, so it is not a forest and has treewidth at least two.
Its treewidth is therefore exactly two.

This disproves both the factor-two claim at width two and the proposed general
upper formula `2^(k−1)` for all incidence widths `k`, already at `k=2`.

## It is also an exact factorwise envelope-width gap

For each binary payoff take its unique multilinear extension to the unit box.
Write

```
E(u,v)=1−u−v+2uv,
N(u,v)=u+v−2uv.
```

These are the multilinear extensions of equality and inequality. Both lie in
`[0,1]` on the unit square. Then the three continuous factor functions are

```
g_A(x)=E(x_AB,1,x_AB,2) E(x_CA,1,x_CA,2),
g_B(x)=N(x_AB,1,x_AB,2) E(x_BC,1,x_BC,2),
g_C(x)=N(x_BC,1,x_BC,2) N(x_CA,1,x_CA,2).
```

They remain nonnegative on the box and are multilinear because their two pairs
of variables are disjoint. Their coefficients in the monomial basis have mixed
signs.

At the center of the box each factor has convex-envelope value zero and
concave-envelope value one. The upper value was proved above; the lower value
follows by mixing any falsifying binary assignment with its complement.
The sum has concave-envelope value one. Its convex-envelope value is zero:
the assignment with pair values `AB=01`, `BC=01`, `CA=00`, together with its
complement, has fair means and makes every payoff zero.

Hence the full sum's graph-hull fiber is `[0,1]`, whereas the relaxation using
each of these three factors' exact envelopes has fiber `[0,3]`. Its width ratio
is exactly three. The standard envelope/coupling identity applies because all
these functions are multilinear: any point of the graph is a convex combination
of corner graph points obtained by independent Bernoulli rounding.

This comparison uses these three structured factors. It is not the relaxation
obtained by independently convexifying every monomial in their expanded
mixed-sign polynomial, and it is not a positive-coefficient monomial example.

## An independent-set family explaining the construction

The example is the triangle case of a general construction. Take any finite
simple graph `G=(V,E)` with nonnegative vertex weights `w_v`. For each edge `uv`,
create two fair binary variables. Give its endpoints opposite demanded parities
for that pair. Define the factor at `v` to be `w_v` times the indicator that
all pairs on edges incident to `v` have the parities demanded by `v`.

Every factor's local optimum is `w_v`, using a satisfying assignment and its
complement. For any complete assignment, satisfied factors form an independent
set: the endpoints of an edge demand opposite parity. Conversely, every independent
set can be made satisfied simultaneously, by selecting each edge parity to meet
its selected endpoint's demand when it has one. Mixing this assignment with its
complement preserves all selected factors and makes all singleton means fair.
Thus

```
T=Σ_v w_v,       H=α_w(G),
```

where `α_w(G)` is the maximum weight of an independent set. The argument remains
valid if additional unselected factors happen to be satisfied: their total weight
cannot exceed `α_w(G)`, while a maximum independent set already supplies that value.

The incidence graph replaces each edge of `G` by two internally disjoint paths
of length two. If `G` has an edge, its incidence treewidth is

```
max{2,tw(G)}.
```

For the upper bound, start with a tree decomposition of `G`, interpreting its
vertices as factor nodes. For each edge `uv`, attach two bags `{u,v,X_uv,r}` to
a bag containing both endpoints. For the lower bound, contracting one of the
two paths per edge and deleting the other exhibits `G` as a minor, and every
original edge also gives a four-cycle. Both lower bounds are therefore necessary.

Taking `G=K_(k+1)` with unit vertex weights for `k≥2` gives incidence treewidth `k`, factor arity `2k`,
variable frequency two, fair means, and ratio `k+1`. In particular the factor-three
obstruction at width two requires neither large arity nor high variable frequency.
This family is recorded as an elementary graph encoding, not as a new complexity
reduction or new independent-set result.

## Verification and literature positioning

All 64 binary assignments of the six-variable instance were enumerated. There
are exactly 16 assignments of each payoff type `(1,0,0)`, `(0,1,0)`, `(0,0,1)`,
and `(0,0,0)`. The complement-pair laws and all marginal equalities were checked
exactly. The argument above is a proof, not an inference from the enumeration.

The local-marginal relaxation and its exactness on incidence forests are established
graphical-model ideas. Relevant searches included CSP basic LPs, factor graph
treewidth, marginal consistency, and equality/disequality graph encodings. For
example, the introduction of
[Cai, Lu, and Xia, Dichotomy for Holant∗ Problems of Boolean Domain](https://pages.cs.wisc.edu/~jyc/papers/asymmetric-boolean-holant-star.pdf)
describes the broad framework of Boolean functions placed on graph incidences.
Such counting/partition-function results use different objectives from the
fixed-marginal payoff ratio here. No exhaustive priority search was performed for
this small obstruction, and no publication novelty is claimed.

The useful conclusion is precise: arbitrary nonnegative factors cannot replace
positive-monomial deficiencies in an incidence-width-two proof with constant two.
The latter question remains separate. Independent review:
[review-binary-factor-width-two-counterexample.md](../notes/review-binary-factor-width-two-counterexample.md).
