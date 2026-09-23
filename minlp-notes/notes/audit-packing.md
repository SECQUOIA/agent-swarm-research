# Packing audit and a possible follow-up

Date: 2026-09-04. The independent audit corrected
`results/point-packing-relaxations-anstreicher-conjecture-4.md`.
The four exact values are correct but already published by
[Khajavirad (2024), Propositions 1 and 3](https://arxiv.org/html/2404.03091v1).
The original paper explicitly uses ceilings. An erroneous factor of two in the draft's
opening averaging inequality was corrected; the subsequent main formulas were unaffected.
The solver script initially had an incorrect default symmetry convention and final
comparison column, and its ordering option omitted lifted products. A subsequent
maintenance pass corrected these issues, as detailed below.

## Verification script correction

The corrected [script](../code/point_packing/pp_relaxations.py) defaults to the published
ceiling convention, displays the four correct Conjecture 4 formulas, and suppresses the
SYM formula claims below `n=5`. A repository usage search found no callers of its
`ord_` option; the option was removed because mean ordering alone is not the published
ORD relaxation. Explicit `floor` and `round` symmetry choices remain available only as
clearly labelled exploratory variants. Both solver functions now require optimal status
and a finite objective before returning a value.

On 2026-09-04 the default run in `~/miniconda3/envs/minlp-notes/bin/python` checked
`n=2,…,14`, using Gurobi and CVXPY/Clarabel. Every applicable formula comparison
passed at absolute and relative tolerances `10⁻⁶`; this includes the unchanged
SDP+RLT values and, for `n≥5`, SDP+SYM+RLT. The result note's table matches the
rerun. During development, the extra SDP+SYM+RLT solve at `n=4` returned
`optimal_inaccurate`, which the new status guard rejected. The default check now runs
that extra model only for `n≥5`, where the cited symmetry formula applies. No numerical
optimality claim is made for the omitted solve. Floating-point verification supplements
the analytic proof and the earlier exact rational construction checks.

The following observation is a candidate extension, not a novelty claim. Its argument was
developed during this audit and has not yet had a second independent review. It is
separate from the independently audited formulas above.

## Exact obstruction for convexification of bounded-size point subsets

For `m ≥ 2` and dimension `d ≥ 1`, let

```
p_m = max { min_{i<j} ||z_i-z_j||² : z_1,…,z_m ∈ [0,1]^d }.
```

Fix integers `2 ≤ k ≤ n`. For each point subset `S ⊆ [n]` of size at most `k`, let

```
F_S = { ((z_i)_{i∈S}, θ) : z_i∈[0,1]^d,
          ||z_i-z_j||² ≥ θ for all distinct i,j∈S }.
```

Define the relaxation in the original variables by imposing
`((z_i)_{i∈S},θ) ∈ conv(F_S)` for every such subset and maximizing the common `θ`.
Then its exact optimum is `p_k`, independently of `n`.

Proof. Any subset of size `k` gives the valid inequality `θ ≤ p_k`, which survives
convexification. For the reverse inequality, take an optimal `k`-point packing, which
exists by compactness. Average its uniform coordinate reflections: for each coordinate,
apply either `t ↦ t` or `t ↦ 1−t` to every point. Each of the `2^d` reflected packings
has the same pairwise distances and common `θ=p_k`; their mean places every labelled
point at the cube centre. Thus centre coordinates with `θ=p_k` belong to the convex
hull for each `k`-point subset. For a smaller subset use any corresponding restriction
of this reflected packing; its distances still meet `p_k`. The same global centre
point therefore satisfies every local convex hull. This proves equality.

This statement concerns convex hulls taken separately before intersection. It does not
say that the convex hull of the full `n`-point feasible set has value `p_k`.

## The same construction survives consistency of full local distributions

A stronger formulation can associate a probability measure `μ_S` on the coordinates
of every subset `S`, `|S|≤k`, require agreement of overlapping marginals, and require
that each measure is supported on packings with pairwise squared distances at least
a common deterministic `θ`. This hierarchy also has exact optimum `p_k`.

For the lower bound, first form a random `k`-tuple by uniformly permuting the labels
of an optimal `k`-point packing. Let `ν_r` be the distribution of its first `r` entries.
Exchangeability means that the marginal on any `r` coordinates is `ν_r` after putting
those coordinates in a fixed order. Give every size-`r` subset the law `ν_r`.
These laws agree under restriction and each is supported on feasible configurations
at `θ=p_k`. The upper bound follows from any measure on a subset of size `k`, since
no configuration in its required support can have `θ>p_k`.

This formulation need not have a global joint distribution on all `n` coordinates.
It is precisely that missing extension requirement that makes the construction possible.
It also does not automatically satisfy a global semidefinite moment matrix spanning
all `n` points. Accordingly, this is not a lower bound for every SDP or SOS hierarchy.

## Consequence and research status

For fixed `k,d`, `p_k>0`, but `p_n→0` as `n→∞`. To see the latter without relying
on packing asymptotics, partition the cube into `q^d` boxes of side `1/q`; if `n>q^d`,
two points lie in one box and have squared distance at most `d/q²`. Thus exact local
convexification of any fixed number of point variables leaves a nonvanishing bound
while the true optimum vanishes. Letting `q` be the largest integer with `q^d<n`
gives the explicit ratio lower bound `p_k q²/d` whenever `q≥1`.

The argument is elementary and related to local marginal consistency and finite
exchangeability. Its novelty has not been searched. The most promising substantive
follow-up would quantify what additional global consistency, moment information,
or growing subset size is necessary to make the bound vanish. Merely presenting this
observation as a new solution of the original Anstreicher conjectures would be wrong.
