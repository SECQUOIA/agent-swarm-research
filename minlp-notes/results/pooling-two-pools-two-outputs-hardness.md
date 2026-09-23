# Pooling is NP-complete with two pools and two outputs on a tree

Date: 2026-09-05. Status: two independent mathematical reviews PASS; novelty qualified.

The result is ordinary NP-completeness of standard pooling with exactly
two pools and two outputs, arbitrarily many inputs and quality coordinates,
no direct arcs, only upper flow bounds in `{1,2}`, and only upper quality
bounds. One pool has just one input and serves only one output. Replacing
that pool by a direct arc gives hardness with one pool, two outputs, and
one direct input-output arc. No strong-hardness or approximation claim is
made.

NP membership follows from the reviewed
[fixed-pool/fixed-output fraction parameterization](fixed-parameter-linear-fibers-np-membership.md):
there are at most four pool-output split parameters, and all remaining
constraints form bounded linear fibers when those fractions are fixed.
The attribute count may be unbounded. This upper bound also applies to
the one-pool/two-output/one-bypass corollary. The reduction below proves
the hardness direction.

## Source problem and preparation

Matsui proves NP-hardness of minimizing a product of two strictly positive
linear functions over a rational polytope. His reduction uses bounded
variables in `[0,1]` and coefficients of polynomial encoding length, despite
their large magnitudes. See [Matsui, METR95-13](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf),
Sections 2–3 and Theorem 3.1; the journal version is *Journal of Global
Optimization* 9 (1996), 113–119. The decision question is

```
does some w in P0 satisfy U(w)V(w) <= K ?
```

Here `P0` is a bounded rational polytope, `U,V` are strictly positive affine
functions on it, and `K>0`. It suffices to use Matsui's explicit bounded
family. Empty `P0` can be detected by LP and mapped to a fixed no instance.
Compute the positive minimum `u_min` of `U` over `P0` by rational LP. Replace
`U` by `2U/u_min` and `V` by `u_min V/2`; their product is unchanged and now
`U>=2`. Add the inequality `V<=K` to obtain `P`. This preserves the yes/no
answer because `UV<=K` and `U>=2` imply `V<=K/2`. If `P` is empty, again
return a fixed no instance. All these operations have polynomial bit
complexity.

Represent `P` inside a probability simplex:

```
P = { z >= 0 : sum_i z_i = 1, A_r z <= d_r for r=1,...,R }.
```

For the source with `w in [0,1]^s`, set `z_i=w_i/s` for `i=1,...,s` and
`z_0=1-sum_i w_i/s`; impose `z_i<=1/s` and transform the original
inequalities using `w_i=s z_i`. Every affine function becomes linear in
`z` because `sum z_i=1`. This is an injective affine representation with
polynomial size; its simplex vertices need not themselves belong to `P`.
Define linear functions on this simplex by

```
a(z) = U(z)-1 = sum_i a_i z_i,
b(z) = K-V(z) = sum_i b_i z_i.
```

For every `z in P`, `a(z)>=1` and `b(z)>=0`. Individual coefficients
`a_i,b_i` need not share these signs; only feasible mixtures use the bounds.

## Pooling instance

There is one input `i` for each simplex coordinate and an anchor input `h`.
All variable inputs feed only pool `L`, with capacity 2 on each input and
intake arc; `L` has throughput capacity 2. The anchor feeds only pool `H`,
with input, intake arc, and pool capacities 1. Pool `L` feeds outputs `1,2`;
pool `H` feeds only output `1`. Each outgoing arc and each output has
capacity 1. There are no other arcs and no positive lower flow bounds.

Give variable intake arc `i -> L` cost `-b_i`. All other costs are zero.
Thus profit is `sum_i b_i x_i`, the negative of the minimization objective.

Use the following quality coordinates and upper bounds:

| Coordinate | Variable input i | Anchor input h | Output 1 bound | Output 2 bound |
|---|---:|---:|---:|---:|
| distinguished quality | `a_i` | `0` | `1` | `max(0,max_i a_i)` |
| polytope row r | `A_ri` | `d_r` | `d_r` | `d_r` |

The first output-1 inequality bounds distinguished quality by one. The
corresponding output-2 bound is redundant for all possible mixtures. Row coordinates encode all of `P`,
including the safe inequality `V<=K`. Negative quality values can be
removed by adding a common rational constant to every input value and both
output bounds of each coordinate; conservation makes this an equivalent
instance. Hence nonnegative input qualities and bounds can also be required.

## Exact objective identity

**Lemma.** For nonempty `P`, the maximum pooling profit is

```
max_{z in P} b(z) * (1 + 1/a(z)).                         (1)
```

**Proof.** Consider a feasible solution with positive throughput `T` through
`L`; let `z_i=x_i/T` be its input proportions. Let `y_1,y_2` be its two
outflows, let `h` be the anchor outflow, and write `D_1=y_1+h`, `D_2=y_2`.
For any row coordinate, output 1's constraint is

```
(A_r z)y_1 + d_r h <= d_r(y_1+h),
```

so `y_1>0` implies `A_r z<=d_r`. Output 2 implies the same inequality
whenever `y_2>0`. Since `T=y_1+y_2>0`, all the defining rows of `P` hold.
Thus `z in P`, `a(z)>=1`, and `b(z)>=0`, regardless of whether individual
input coefficients have those properties.

The distinguished quality upper bound at output 1 gives

```
a(z)y_1 <= D_1, hence y_1 <= D_1/a(z).
```

This includes the case `D_1=0`. Because `D_1,D_2<=1`, profit is

```
b(z)T = b(z)(D_2+y_1) <= b(z)(D_2+D_1/a(z)) <= b(z)(1+1/a(z)).
```

Conversely fix any `z in P` and fill both outputs: choose
`D_1=D_2=1`, `y_1=1/a(z)`, `y_2=1`, `h=1-1/a(z)`,
`T=1+1/a(z)`, and `x_i=Tz_i`. Since `a(z)>=1`, every flow bound holds;
`T<=2` and `x_i<=2`. The construction satisfies every quality bound and
attains the right-hand objective in (1). If `L` is inactive, any remaining
anchor-only flow has zero profit. Since the right-hand side is nonnegative, this does not
change (1). Compactness of `P` and `a>=1` ensure a maximum exists. □

**Theorem.** Deciding whether this pooling profit is at least `K`
is NP-hard.

**Proof.** For any `z in P`, with `a=U-1>0` and `b=K-V`,

```
b(1+1/a) >= K
iff (K-V)U >= K(U-1)
iff UV <= K.
```

The source preparation preserves this decision and the lemma identifies
the exact pooling maximum. A fixed no instance needed above can retain the
same two-pool/two-output topology, give every arc zero cost, and use any
positive target profit. All coefficients and the number of coordinates
have polynomial encoding length. □

## Scope and model boundary

The construction has exactly two pools and two outputs; the counts of
inputs and qualities grow with the source. It does not conflict with
polynomial algorithms when the pool and quality counts are both fixed.
Although pool `H` has no mixing choice, it is an ordinary pool allowed by
the standard model. Suppressing that degree-one pool gives exactly one
direct arc and one mixing pool, so even this single bypass changes the
fixed-output complexity boundary.

The underlying undirected network is a tree: variable inputs are leaves at
`L`, the path `L--output 1--H--anchor` has no other connections, and output
2 is another leaf at `L`. Thus the result holds at undirected treewidth one
and with every input having out-degree one. Contracting the anchor pool
for the bypass variant also leaves a tree. Topological sparsity alone does
not ensure tractability when the quality dimension grows.

The proof uses upper quality bounds only, with one distinguished coordinate
and one coordinate per defining polytope inequality. No quality equality or
lower quality bound is needed. An affine shift can make all quality data
nonnegative. A subsequent positive rational scaling per coordinate puts
all its input values and output bounds in `[0,1]`: divide by the maximum
shifted value, or leave an all-zero coordinate unchanged. This preserves
the inequalities and polynomial encoding length. Flow capacities stay in
`{1,2}`. Costs and qualities are unrestricted rational numbers; strong
hardness is not established. Membership in NP for unrestricted pooling is
not needed and is not claimed here.

Nonnegative production costs and nonnegative output revenues also suffice.
Choose `B>=max(0,max_i b_i)`. Charge variable inputs `B-b_i` per unit and
the anchor `B` per unit, and pay revenue `B` per unit at either output.
Total conservation cancels all `B` terms, leaving exactly the same profit.
All source and pool upper bounds are redundant given the output bounds, so
the result also applies when source availability and pool capacity bounds
are omitted. Alternatively requiring both output demands to equal one
preserves the same objective identity and hardness.

## Novelty and verification status

The published final Haugland discussion leaves open fixed numbers of pools
and outputs with unrestricted inputs and qualities; see
[[haugland2016-the-computational-complexity-of-the]] p.16 and the
[source audit](../notes/pooling-fixed-pools-qualities-source-audit.md). The theorem
addresses this case in the published discussion. The
[novelty search](../notes/pooling-two-pools-two-outputs-novelty.md) found no matching
open result in the sources checked; a comprehensive novelty claim is not
made.

[First independent review](../notes/review-pooling-two-pools-two-outputs-hardness.md):
PASS for the source reduction, polynomial preprocessing, single-upper-bound
refinement, dilution cancellation, objective identity, and stated model
extensions. [Second independent review](../notes/review-pooling-two-pools-two-outputs-second.md):
PASS, including an independent exact checker covering 78 fixed-composition
original-flow LPs and 36 threshold identities.

An independent rerun with another seed passed another 28 original-model
solves; its [log](../code/pooling_two_pools_two_outputs/independent_review_output.txt)
is retained.

The [checker](../code/pooling_two_pools_two_outputs/check_reduction.py)
compares original multiquantity pooling equations, solved globally with
Gurobi, against exact rational vertex enumeration on small source polytopes.
The reference enumeration is justified because `b(1+1/a)` is quasiconvex on
`a>=1,b>=0`: its nonnegative sublevel sets are
`b<=t*a/(a+1)`, hypographs of a concave function. The first run passed 40
original-model solves: twelve generated instances with signed input
coefficients, each tested in two-pool, shifted-quality, and single-bypass
forms, plus four boundary cases. A negative control removing the polytope
row specifications at output 1 changed the optimum from numerical zero to
10, confirming why both outputs require those rows. The
[run log](../code/pooling_two_pools_two_outputs/check_output.txt) records
results. These checks support implementation confidence and do not replace
the mathematical proof.
