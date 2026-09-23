# Independent second audit: quality-scaled path flows

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS for the stated fully contracted model.** I independently
checked the complete proof in
[the candidate note](pooling-quality-scaled-path-flow.md), including its
final capacity-candidate conjunction and fixed-boundary formulation.
This is a polynomial bit-time feasibility result with a common field of
degree at most two for one recovered feasible flow. The common pool
throughput restriction and exact external contracts are substantive.
Priority of the pooling specialization is not established by this audit.

## Physical equivalence

Eliminating each intake and outlet by its local mass equation is exact,
including an absent arc, which imposes zero rather than deleting the
corresponding contract. Summing these equations gives the pool mass
balance from the global equality of supplies and demands. Summing the
output quality equations gives the pool quality balance from the global
quality-mass equality. Thus neither balance has been silently dropped.
At zero pool throughput every nonnegative intake and outlet is zero;
the quality-mass identity still holds. The pool quality may then be any
point in the allowed feed-quality interval. If no feed or no outlet is
allowed, forcing all pool arcs to zero, checking their lower bounds, and
retaining the external contracts is the correct LP preprocessing.

For a nonsingular quality, multiplying a bypass flow by `gamma_i=C_i-q`
is invertible. Keeping its original orientation and allowing signed
transformed flow is essential. Multiplying an input total interval or an
arc interval reverses its endpoints exactly when `gamma_i<0`. Inputs
therefore have affine divergence bounds and outputs have the exact
divergence `-b_j(B_j-q)`.

I independently solved the two-inlet output equations. If the qualities
differ, writing `R=b_j(B_j-q)` and the total bypass flow as `s` gives

```
w_1=(C_1-q)[R-(C_2-q)s]/(C_1-C_2).
```

Its coefficient of `s` is nonzero with a fixed sign between consecutive
input qualities. An outlet-total interval is consequently equivalent to
one extra interval on `w_1`, with quadratic endpoints. The output
divergence equation and both original arc intervals remain. Equal
qualities instead give the pure parameter test that `R` lies between
`gamma L` and `gamma U`. One-inlet and zero-inlet outputs are correctly
handled separately. These arguments cover zero demand, absent outlets,
negative qualities, and either sign of the scaling factors.

Every singular input quality, and every endpoint of the quality search
interval, is handled by an original fixed-quality physical LP. There
is no division by zero or lost isolated feasible parameter.

## Signed cuts and candidate expansion

For outgoing-minus-incoming divergence, the necessary and sufficient
conditions are exactly

```
alpha(S) <= u(delta+ S)-ell(delta- S),
beta(S)  >= ell(delta+ S)-u(delta- S).
```

For sufficiency, add a root-to-vertex arc with bounds `[alpha_v,beta_v]`.
Conservation at the vertex identifies this new arc's flow with its
original divergence. Apply the circulation cut inequality that lower
outgoing flow is at most upper incoming flow. Cuts excluding the root
give the second displayed inequality; complementary cuts give the
first. This also accounts for total divergence zero. Negative arc and
node bounds cause no difficulty: lower-bound shifting reduces the
circulation problem to the usual nonnegative-capacity form.

I checked the primary statement in Schrijver, *Combinatorial
Optimization*, [Corollary 11.2i, printed page 175](https://www.lamsade.dauphine.fr/~cornaz/Enseignement/M2_MODO/DATA/A1.PDF).
It supplies the established signed interval-imbalance criterion with
the opposite imbalance convention. The candidate's sign conversion is
correct. The network-flow theorem itself is not a new result.

Decomposing any vertex subset into the connected components of its
induced subgraph makes both sides of each cut inequality additive.
Consequently connected induced subsets suffice. A path or cycle has
quadratically many; disconnected bypass components and isolated nodes
remain covered. The whole-component inequalities must be retained and
are retained.

Each such cut crosses at most two edges. The attainable upper cut sum
is the minimum over all upper-outgoing/lower-incoming candidate
combinations; the attainable lower cut sum is the corresponding
maximum. Requiring the appropriate inequality for every combination is
therefore exactly equivalent, not a relaxation. Candidate lists have
constant size, so this produces only a constant factor more rows.
Every lower candidate must also be at most every upper candidate on its
edge. This removes all capacity max/min expressions without a new
parameter partition.

## Complexity and recovery

On each of linearly many input-quality intervals there are polynomially
many quadratic inequalities with rational coefficients of polynomial
bit length. This follows directly from the output formulas, the fixed
nonzero quality differences in their denominators, and polynomially
many cut sums. Isolating and ordering quadratic roots and testing all
open cells and boundary points decides feasibility in polynomial bit
time. Feasible open cells admit rational samples of polynomial encoding
length by algebraic root separation. Isolated feasible points have
degree at most two. No enumeration of flow bases is part of the
algorithm.

At a selected quality, all bounds belong to the single represented
ordered field `Q(q)`. A circulation algorithm uses addition,
subtraction, and comparisons in this field. For example, a polynomial
augmenting-path maximum-flow algorithm after the standard lower-bound
reduction does not introduce additional algebraic extensions. An
incidence-system vertex has coordinates that are rational linear
combinations of its bounds, giving polynomial encoding length.
Recovering `z=w/(C_i-q)` remains in the same field, and inversion has
polynomial bit complexity in fixed degree. Singular-quality recovery
uses a rational LP. These facts justify the constructive witness claim;
they do not assert that some instance requires an irrational witness.

## Fixed boundaries and scope

Deleting a prescribed boundary arc of transformed flow `t` shifts the
adjacent node interval by `-sigma*t`, where `sigma` is its incidence
sign. All bounds on the deleted arc must be retained separately. The
remaining connected-cut rows are quadratic in `q` and linear in the
prescribed transformed flows. The physical identity
`t=(C_i-q)z` is bilinear. The constant-size candidate expansion applies
to the remaining internal arcs, so no capacity partition involving
boundary coordinates is necessary.

This verifies the boundary ingredient, not an unspecified pooling
extension: any extension must separately recover the global mass and
quality balances and enforce its remaining contracts. In particular a
restrictive common pool capacity is not recovered from these cut rows.
The theorem assumes that common bound is redundant. It does not claim
polynomial optimization with arbitrary dense arc costs.

## Computational support

I inspected the independent quantities used in
[the author's checker](../code/pooling_bypass_paths/check_quality_scaled_cuts.py).
It computes transformed bounds and candidate-cut identities with exact
rational arithmetic, compares them with the original physical fixed-
quality LP, and separately compares connected cuts with every subset
cut on signed path/cycle systems. The LP comparisons use numerical
HiGHS and support the mapping and cut implementation; they do not
implement the symbolic parameter algorithm or certify its bit bound.
The mathematical audit above is independent of those numerical solves.

My rerun passed 247 nonsingular transformed-cut versus original physical
LP comparisons (86 feasible), 84 singular-quality LP cases, and 84
generic signed path/cycle comparisons among connected cuts, all subset
cuts, and LP feasibility. All candidate-cut identities in the checker
were evaluated exactly.
