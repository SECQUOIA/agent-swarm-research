# Diagonal box followers: bounded leader components versus a path

Date: 2026-09-05. Status: reviewed predecessor of the
[promoted supporting boundary](../results/bilevel-leader-vertex-integrity-boundary.md). The positive algorithm reuses the local
vertex and fixed-dimensional cell method from
[the fixed-core polyhedral theorem](../results/fixed-core-block-polyhedral-optimization.md).
The path reduction uses the classical Subset Sum problem. Neither technique
is claimed as a new general algorithmic principle.

## 1. Model and proposed structural boundary

The leaders are `x in [0,1]^r`, with `r` part of the input. Their unique
follower minimizes

```
(1/2)sum_i d_i z_i^2 + sum_i(c_i+C_i x)z_i,
z in [0,1]^N,   d_i>0.
```

All data are rational. The leader minimizes an affine objective in `(x,z)`
and has no other constraints. Dividing each affine follower coefficient by
its positive `d_i` gives the response representation

```
z_i(x)=clip_[0,1](alpha_i+beta_i^T x).
```

Thus the upper objective is a sum of signed capped affine functions and an
affine leader term. Define the leader interaction graph by joining any two
leader coordinates that occur together with nonzero coefficients in one
follower affine form.

**Positive candidate.** If a supplied set of at most `c` leaders leaves
connected components of size at most `h`, exact global optimization and
rational optimizer recovery are polynomial in the rational input length
for fixed `c,h`. This includes a supplied fixed-size vertex cover by taking
`h=1`. A suitable set can also be found by enumerating all leader subsets
of size at most `c`, so a supplied decomposition is unnecessary for fixed
`c,h`. This is a polynomial algorithm for fixed parameters, not a claim
of fixed-parameter tractability.

**Negative candidate.** With no bound on component size, exact threshold
decision is NP-complete even when this interaction graph is a path, `Q=I`,
all follower affine coefficients have magnitude at most one, and all upper
affine coefficients have magnitude at most two. The reduction is weak
numeric hardness: its bounded-coefficient version has an exponentially
small possible value gap. Scaling the upper objective gives a constant
gap with potentially large numerical coefficients.

## 2. Component minima have affine candidate locations

Write the core coordinates as `u in [0,1]^c` and each remaining component
as `v_b in [0,1]^(h_b)`, where `h_b<=h`. Every follower affine form involves
only core coordinates and at most one component, by the graph definition.
Assign core-only terms to `H_0(u)` and all other terms to their component:

```
H(u,v)=H_0(u)+sum_b H_b(u,v_b).
```

Fix `u`. The clipping thresholds and the component box partition its space
into bounded polyhedral cells. The objective is affine on each cell, so
some component minimizer is a vertex of this arrangement. Every vertex is
determined by `h_b` independent active hyperplanes, chosen from the two
thresholds per local ramp and the component box faces. Their coefficients
in `v_b` are fixed rational numbers; their right-hand sides are affine in
`u`.

Enumerate every independent `h_b`-row subset. Solving its constant
nonsingular coefficient matrix gives a candidate

```
v_(b,l)(u)=P_(b,l)u+q_(b,l),
```

with rational affine coordinates. Discard singular subsets. Box-face
subsets include the component corners, so some candidate is available for
every core input. A candidate is retained at `u` exactly when it lies in
the component box. The selected clipping hyperplanes are present in the
arrangement for every `u`, so no additional sign assumption is needed to
make such a feasible intersection an arrangement vertex. In fact soundness
needs only box feasibility, since evaluating any such point gives a valid
leader choice.

If component `b` has `m_b` ramp terms, it has at most
`(2m_b+2h_b)^(h_b)` candidates. For fixed `h`, the number and bit lengths of
all affine candidates are polynomial. An arrangement cell may be lower
dimensional; its vertices still have a set of `h_b` independent active
normals because it is bounded. Terms with zero component normal cannot
contribute to an independent selected system and cause no difficulty.

## 3. A fixed-dimensional core arrangement selects all component minima

Collect the following affine hyperplanes in core space:

- each candidate coordinate at zero and one, to fix its box feasibility;
- every local ramp evaluated at every candidate, at its two clipping
  thresholds, to make its value affine;
- the thresholds of all core-only ramps.

There are polynomially many hyperplanes for fixed `h`. Enumerate their
realizable sign cells, including zero signs and lower-dimensional cells,
and intersect with the core box. On each such cell, the set of box-feasible
candidates is fixed, and every candidate objective value is an explicitly
known rational affine function of the core.

For this cell add all pairwise equality hyperplanes between objective
values of feasible candidates belonging to the same component. Their
number is polynomial. Enumerate the further cells. On each, choose a
minimum-value candidate for each component. The total upper objective,
including the core-only terms, is now affine. Minimize it by rational LP
over the closure of the final cell within the core box.

This use of closures is safe. A candidate feasible throughout a relative
sign cell remains box-feasible at its boundary. Clipping formulas agree
at thresholds, and weak objective comparisons persist. A candidate that
was infeasible in the relative cell can become feasible at its boundary,
but omitting it does not create an invalid solution: the candidates chosen
for that LP still give feasible leaders. Completeness follows because an
actual global optimum lies in one of the enumerated relative cells, where
all its available minimizing candidates are retained. Thus the best LP
value is exactly the global minimum.

For `c=0`, core space is a singleton and the same procedure reduces to
independent finite candidate comparisons. Constant tests are handled by
their signs. For any `c`, all LPs are bounded by the core box. Their optimal
core points, selected component candidates, and final clipped follower
responses are rational of polynomial bit length. Fixed-dimensional affine
arrangement enumeration and LP therefore prove the positive candidate.

This is a finite-piece extension of the earlier local-vertex method with
no aggregate constraints. It is not literally an instance of that theorem's
polyhedral-leaf statement, because the signed clipped local objective need
not be convex. The additional enumeration above handles that distinction;
no generic nonconvex oracle is assumed.

## 4. A normalized Subset Sum objective on a path

Take positive integers `a_1,...,a_n` and a target `T` with
`0<T<W=sum_i a_i`; trivial targets can be preprocessed. Set

```
r_i=a_i/W,   tau=T/W.
```

Use `n+1` leaders `x_0,...,x_n` in the unit interval, with no endpoint
constraints. For `r in (0,1]` and `t in [-1,1]`, define

```
rho_r(t)=min{|t|,|t-r|}
        =-t+2clip(t)-2clip(t-r/2)+2clip(t-r).       (1)
```

The equality follows from its slopes on the four intervals cut by
`0,r/2,r`. Every positive part in this identity is at most one on the
specified domain, so unit clipping is exactly the corresponding ReLU.
The objective is

```
H(x)=x_0+|x_n-tau|+sum_i rho_(r_i)(x_i-x_(i-1)).    (2)
```

It is nonnegative and at most `n+2` on the full leader box. For every
leader, choose `delta_i in {0,r_i}` nearest to its increment. Then
`rho_(r_i)=|x_i-x_(i-1)-delta_i|`, and telescoping plus the triangle
inequality gives

```
|sum_i delta_i-tau| <= H(x).                       (3)
```

The sum is a normalized subset sum. Conversely, for any subset set
`x_0=0` and choose successive `x_i` as its cumulative normalized selected
weights. All states belong to `[0,1]`, every increment penalty vanishes,
and (2) equals the normalized distance between its total and `T`. Hence

```
min H = (1/W) min_(S subset {1,...,n}) |sum_(i in S)a_i-T|.  (4)
```

This is an exact identity, not just a feasibility reduction. Yes instances
have optimum zero; no instances have optimum at least `1/W`.

## 5. Identity-Hessian follower realization and precision scope

Since `|x_n-tau|=tau-x_n+2clip(x_n-tau)`, telescoping (1) rewrites (2) as

```
H=2x_0-2x_n+tau+2clip(x_n-tau)
  +2sum_i[clip(x_i-x_(i-1))
          -clip(x_i-x_(i-1)-r_i/2)
          +clip(x_i-x_(i-1)-r_i)].                 (5)
```

Give each of these `3n+1` capped ramps an independent follower coordinate
minimizing `z^2/2-h(x)z` on `[0,1]`. The combined Hessian is exactly the
identity, and the unique response realizes (5). Every follower affine
coefficient has magnitude at most one. The upper coefficients have
magnitude at most two, including its direct leader terms and constant.
Each nonunary form involves exactly two consecutive leaders, so their
interaction graph is the path `0--1--...--n`. There are no extra upper
constraints. If a purely follower-linear objective is desired, add two
coordinates responding as `x_0,x_n`; a fixed-one coordinate can carry the
constant `tau`. These additions are unary and preserve the graph.

The construction has polynomial rational bit length in the Subset Sum
input. NP membership follows by guessing clipping regimes: their
inequalities and the threshold bound are rational affine inequalities in
all leaders, so a feasible instance has a polynomial-bit rational LP
witness. Thus the exact threshold problem is NP-complete even on a path.

The gap in the bounded-coefficient formulation is `1/W`, which can be
exponentially small in input bit length. Multiplying the upper objective
by `W` gives a zero-versus-at-least-one gap, with upper coefficients as
large as `2W`. This reduction does not establish strong NP-hardness with bounded numerical data,
and it does not exclude an additive scheme polynomial in inverse
tolerance. It does exclude polynomial time in input length and accuracy
bit count: an estimate with error less than `1/(2W)` distinguishes the
instances. The constant-gap scaled version and the bounded-coefficient
version must not be conflated.

## 6. Scope and source status

The positive statement bounds component size after deleting a fixed core;
it does not assume treewidth alone. The path family shows that a treewidth
bound of one cannot replace that stronger structural restriction for exact
rational optimization. This is a precision-based obstruction, compatible
with ordinary piecewise-linear dynamic programming whose state complexity
depends on numerical resolution.

The local vertex method, capped-ramp representation, and Subset Sum source
are established. The [bounded source comparison](bilevel-leader-vertex-integrity-source-audit.md)
found no exact matching combined diagonal-box statement, but the established
techniques make supporting-corollary status appropriate. No publication
priority is claimed.

## 7. Unconditional exponential growth of an exact elimination message

For a fixed terminal state `t in [0,1]`, define

```
V_n(t)=min {x_0+sum_i rho_(r_i)(x_i-x_(i-1)):
            x_0,...,x_(n-1) in [0,1], x_n=t}.
```

Let `S` be the set of normalized subset sums. The same telescoping
argument proves `V_n(t)>=dist(t,S)`. For the converse, choose any subset,
set `x_0=0`, and set each intermediate `x_i`, `i<n`, to its normalized
partial sum. Set only the terminal state to `t`. Every earlier increment
penalty is zero, and the final penalty is at most the distance from `t`
to the chosen subset total, by choosing its final increment option in the
minimum defining `rho`. All states remain in the unit interval. Therefore

```
V_n(t)=dist(t,S).                                  (6)
```

In particular take `a_i=2^(i-1)` and `W=2^n-1`. Every integer between zero
and `W` is a subset sum, so

```
V_n(t)=dist(t,{0,1/W,2/W,...,1}).                  (7)
```

On every interval `[j/W,(j+1)/W]`, this function has slope `+1` up to its
midpoint and slope `-1` thereafter. Its exact intervalwise-affine
representation therefore needs exactly `2W=2(2^n-1)` maximal affine
pieces. There are only `n` local at-most-four-piece increment penalties and one
unary linear term, with `O(n^2)` total rational coefficient bits. Thus
exact piecewise-linear elimination messages can have superpolynomial
output size even on a path, independently of any complexity assumption.
This statement concerns an explicit intervalwise-affine message listing;
it does not exclude short implicit or compressed representations.

### Identical local factors and a fixed coefficient alphabet

The explicit-message lower bound does not require varying rational
weights. Use the same factor `rho_(1/2)` on the affine increment
`x_i-x_(i-1)/2` at every edge, and define

```
Vhat_n(t)=min {x_0+sum_i rho_(1/2)(x_i-x_(i-1)/2):
               x_0,...,x_(n-1) in [0,1], x_n=t}.
```

The zero-cost recurrence `x_i=x_(i-1)/2+delta_i`, with
`delta_i in {0,1/2}` and `x_0=0`, reaches exactly

```
S_n={j/2^n: j=0,...,2^n-1}.
```

For arbitrary states choose each nearest increment option and set
`e_i=x_i-x_(i-1)/2-delta_i`. Weighted telescoping gives

```
t-s = 2^(-n)x_0+sum_i 2^(-(n-i))e_i,
s=sum_i 2^(-(n-i))delta_i in S_n.
```

All weights are at most one, so `|t-s|` is at most the objective.
Conversely, realize any `s in S_n` by its zero-cost bit trajectory, keep
all states before the final one, and replace only the final state by `t`.
Its last penalty is at most `|t-s|`. Therefore

```
Vhat_n(t)=dist(t,S_n).                              (8)
```

There are two maximal affine pieces between each consecutive pair of
zeros, and one final increasing tail from `(2^n-1)/2^n` to one. The exact
number of pieces is thus `2^(n+1)-1`. The local affine arguments have
coefficients `1,-1/2` and shifts `0,-1/4,-1/2`, and the same at-most-four-
piece scalar penalty is used on every edge. The argument lies in
`[-1/2,1]`, so the capped-ramp representation remains valid. All model
coefficients come from a fixed finite set. The original description has
`O(n)` size in a structured path encoding and `O(n log(n+2))` bits when
indices are explicit.

This strengthens the output-size example without strengthening the
complexity reduction: optimizing this special uniform family has a
trivial zero-cost solution. It demonstrates exponential size of the
explicit intermediate function, not NP-hardness of that family or a
lower bound against implicit representations.

This comparison is relevant to
[Meuleau, Morris and Yorke-Smith (2008), *A Variable Elimination Approach for Optimal Scheduling with Linear Preferences*](https://homepage.tudelft.nl/0p6y8/papers/n58.pdf).
Their piecewise-linearity closure theorem and per-step analysis in terms
of current bucket pieces do not by themselves bound the growth of those
pieces in the original input length. The example concerns that output-size
dependence; it does not refute their closure theorem. If temporal-variable
bounds are represented by edges to a common fixed time origin, the
corresponding path-plus-origin graph has treewidth at most two, which is
still constant. The source audit records these scope distinctions.

## 8. Exact diagnostics

[The exact checker](../code/bilevel_vertex_integrity/check_structure_and_path.py)
compares the path optimum against exhaustive subset sums on four instances,
using 521 rational arrangement vertices. It also compares the two-stage
core-cell method with full three-dimensional arrangement enumeration on
three small instances, including zero component coefficients and boundary
intersections. These checks supplement the general proof.
