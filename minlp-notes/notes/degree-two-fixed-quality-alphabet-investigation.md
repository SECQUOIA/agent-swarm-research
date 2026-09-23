# Two input qualities suffice for exponential bypass-path response

Date: 2026-09-05. Status: exact physical construction checked independently
by `pooling_degree_two`; 252 original-network exact positive dual
certificates pass. The exponential Klee–Minty shadow is known. This note
records a fixed-quality-alphabet physical realization and its consequences,
without claiming a new hardness theorem or established priority.

Restricting the number of distinct input qualities does not remove the
known exponential support-curve obstruction on degree-two blending paths.
An exact-demand relay copies a flow while resetting its input quality.
An explicit throughput penalty then removes every positive lower flow
bound in the linear instance, uniformly over the varying output price.

## 1. A quality-reset relay

Write `t_i` for the right arc flow of input `i`, whose exact supply is
`s_i`; its left arc flow is `s_i-t_i`. Adjacent inputs meet at an output.
There are two types of adjacency.

**Descending mixing step.** The preceding input has quality one and the
following input quality zero, with supply `s`. Give their shared output
capacity `s` and upper quality bound `1/2`. Its incoming flows are
`t_previous` and `s-t_next`. Capacity and quality give, respectively,

```
t_next >= t_previous,
t_next <= s-t_previous.
```

**Reset step.** The preceding input has quality zero and exact supply `s`.
Add a quality-one input of the same exact supply `s`. Give their shared
output exact demand `s` and the redundant upper quality bound one. Then

```
t_previous + (s-t_next) = s,
```

so `t_next=t_previous`. The signal is copied while the input quality
changes from zero to one. Every participating input and output has at
most two arcs. No pool, quality lower bound, or negative quality is used.

## 2. An affine copy of the Klee–Minty cube

Fix `n>=2`, `epsilon=1/4`, and free-coordinate supplies
`s_j=4^(j-n)`. Start with a quality-one input of supply `s_1`. For each
`j=2,...,n`, add a quality-zero input of supply `s_j` by a descending
mixing step. If `j<n`, follow it by a reset step of supply `s_j`.
The supply sequence along the physical path is

```
s_1, s_2, s_2, s_3, s_3, ..., s_(n-1), s_(n-1), s_n.
```

The endpoint outputs have upper capacities `s_1` and `s_n=1` and
redundant upper quality bounds one. Each source initially has its stated
exact supply. Reset outputs have their stated exact demands; descending
outputs have only upper flow bounds. All other arc lower bounds are zero.

Let `t_j` denote the right flow at the free-coordinate input, ignoring
the equal-flow reset duplicate. Set `x_j=t_j/s_j`. The resulting feasible
set is affinely bijective to

```
0 <= x_1 <= 1,
epsilon*x_(j-1) <= x_j <= 1-epsilon*x_(j-1),  j=2,...,n.
```

Indeed, each reset duplicates `t_j`, and the next descending step imposes
exactly the two displayed Klee–Minty inequalities. Conversely these
inequalities give all physical flows and satisfy every capacity and upper
quality row.

There are `m=2n-2` inputs, `m+1` outputs, and `N=2m=4n-4` arc variables.
The bypass graph is one path. Input qualities belong to `{0,1}` and
output quality bounds to `{1/2,1}`. Every flow upper bound is at most one.
The rational supply data have polynomial encoding length.

This also explains why counting strictly descending runs of quality
values cannot prove a bounded-complexity theorem: exact-demand reset
steps allow arbitrarily many separate descending steps using two values.

## 3. One varying output price

Use the known Klee–Minty shadow direction

```
c_j=epsilon^(3(n-j))  (j<n),  c_n=0,
lambda in [-1/15,1/15].
```

All `2^n` vertices are uniquely exposed by some objective
`c*x+lambda*x_n`; see Gärtner, Helbling, Ota and Takahashi,
[Section 4 of the open manuscript](https://arxiv.org/pdf/1308.2495),
and the independently checked [source obstruction](parametric-path-lp-obstructions.md).

Give each free-coordinate input position the physical right-flow
coefficient `w_j=c_j/s_j=16^(j-n)` for `j<n`, and give the final position
coefficient `lambda`. Give reset duplicates coefficient zero. List these
coefficients in physical path order as `g_1,...,g_m`. Put base output
revenues

```
rho_0=1,
rho_i=1+sum_(h<=i) g_h,  i=1,...,m.
```

All base revenues lie in `[0,2]`, and only `rho_m` varies with `lambda`.
With zero source costs, exact source supplies `S_i` give total base revenue

```
C0 + c*x + lambda*x_n,
C0=sum_(i=1)^m rho_(i-1)*S_i.
```

The constant `C0` is independent of `lambda`. Hence a single physical
output price already exposes all `2^n` feasible operating vertices.

## 4. Remove all positive lower flow bounds

Let `Q` be the exact-contract path polytope in its `N` actual arc flows.
Its contracts are all source supplies and all reset-output demands.
Retain their upper bounds and drop their lower bounds. Write the contract
rows as `Ew=e`, the nonnegative deficits as `Delta=e-Ew`, and
`d=sum Delta`.

After clearing the factor two in descending quality rows, every physical
constraint coefficient is in `{-1,0,1}`. The exact-contract polytope is
nonempty. The reviewed [explicit polyhedral error bound](../results/pooling-one-pool-upper-bounds-np-completeness.md#2-explicit-rational-error-bound-for-restoring-contracts)
therefore gives an exact-contract point `w'` satisfying

```
||w'-w||_1 <= H*d,  H=N^N.
```

Every base arc-revenue coefficient lies in `[0,2]`. Choose `M=2H+1` and
reward every contracted source throughput and every contracted reset
output throughput by `M`. This has standard nonnegative economics:
leave source costs zero, add `M` to every output revenue, and add another
`M` to reset-output revenues. The first addition rewards total source
throughput by conservation.

If `S=sum e`, the new revenue is `base_revenue+M*(S-d)`. Repair loses at
most `2H*d` in base revenue and gains `M*d` in contract reward. Thus every
optimizer has zero deficit, uniformly in `lambda`, and

```
V_upper(lambda)=M*S+C0+max_(x in KM)(c*x+lambda*x_n).
```

This final physical model has no positive lower flow bound, only upper
bounds on one quality, two distinct input qualities, zero production
costs, positive output revenues, capacities at most one, and a path
bypass graph. Only its terminal output price varies. The penalty has
polynomial bit length. Every fixed-price instance is an LP.

The independent checker
[exact_fixed_alphabet_check.py](../code/parametric_path_lp/exact_fixed_alphabet_check.py)
uses the theoretical `M`, not a fitted numerical penalty. For every
vertex in dimensions two through seven it verifies all original physical
rows and constructs a square active-row basis with strictly positive
rational dual multipliers. The 252 resulting certificates prove unique
optimality in the actual upper-only network, including all relaxed reset
contracts. No hidden copy equation is included in these certificates.

## 5. Scope of the obstruction

The one-price support function has `2^n` distinct open affine pieces.
Any exact piecewise-affine table must therefore contain exponentially
many pieces. An exact quantifier-free description of its graph or bounded
epigraph using nonzero polynomials in the price and value coordinates
has total polynomial degree at least `2^n`: every open affine boundary
segment forces its distinct line to divide some defining polynomial.
This is the line-factor argument already checked in the source obstruction.

These conclusions exclude polynomial-size explicit elimination in those
formats. They do not exclude compact arithmetic circuits, extended linear
formulations, polynomial fixed-price optimization, or a polynomial
algorithm for one-pool degree-two optimization. In particular, the new
[endpoint-feasibility projection](pooling-degree-two-boundary-projection.md)
retains no dense objective coordinate and is compatible with this example.

## 6. Fixed-alphabet version of the vertex-forcing pool interface

The final input above has quality zero, so the independently reviewed
[one-pool interface](pooling-degree-two-vertex-forcing.md) attaches without
change. Its additional input qualities are zero, one, and two. The entire
network therefore has only three distinct input qualities. Keep the
explicit source, reset-output, terminal-output, waste-output, and pool
throughput contracts in this nonlinear extension; Section 4 does not
justify removing them from the nonlinear construction.

The interface makes every physical feasible flow correspond affinely to

```
x in KM,  x_n-x_n^2 <= z <= 1.
```

The path has source costs `S_i`, output revenue `S_(i+1)` before the
terminal output, and left-end output revenue `S_1`. Terminal and interface
revenues and costs remain those in the reviewed construction. The path's
net right-flow coefficient is `S_(i+1)-S_i`. This coefficient is zero
across every reset and is `3s_j` immediately before the next descending
step. Hence the total objective is still exactly

```
sum_(j<n) 3s_j*t_j-z
 = sum_(j<n) (1-epsilon)*epsilon^(2(n-j)-1)*x_j-z.
```

The `2^n` isolated optima, strict-local-maxima perturbation, and compact
exact LP convex hull from that construction all transfer by the affine
map. The graph still has input/output degrees at most two, pool input
and output degrees two, and one undirected cycle. This is a fixed-alphabet
geometric refinement, not a new hardness result. Arbitrary linear costs
in this particular nonlinear family remain polynomially optimizable via
its exact LP hull and an optimal vertex.
