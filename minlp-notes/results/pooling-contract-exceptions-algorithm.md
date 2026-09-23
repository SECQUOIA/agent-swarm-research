# Polynomial pooling optimization with bounded contract exceptions

Date: 2026-09-05. Status: two fresh full independent proof audits PASS.
The scalar and fixed-rank dependencies also have two written audits each.
The precise pooling classification has no matching theorem in the bounded
primary-source search; exhaustive priority is not established.

## 1. Main statement

Consider standard one-pool input--pool--output pooling with direct bypass
arcs and no pool-to-pool arcs. The bypass graph has maximum degree two.
Every individual arc has finite rational lower and upper flow bounds
including nonnegativity. Input qualities and all economic data are
rational. The number of feeds, outlets, inputs, outputs, quality
coordinates, and the affine rank of the input-quality vectors may grow.

Designate exceptional sets `E_I,E_J` of external nodes, with
`s=|E_I|+|E_J|` fixed. Nonexceptional inputs have exact total supplies
`a_i`. Nonexceptional outputs have exact demands `b_j` and exact quality
vectors `B_j`. Exceptional inputs may have ordinary supply intervals;
exceptional outputs may have ordinary demand and quality intervals.
Quality requirements use their homogeneous mass form, including zero
throughput. Costs are standard input unit production costs and output
unit revenues applied to total node throughput.

Common pool-throughput bounds are redundant: the lower bound is zero,
and the upper bound may be omitted or certified by the minimum of total
input-throughput upper bounds, total feed-arc upper bounds, and total
outlet-arc upper bounds. Individual pool-arc bounds remain unrestricted.
This does not include a restrictive additional common pool bound.

**Theorem.** For fixed `s`, exact feasibility and standard
economic optimization are computable in polynomial rational bit time.
When feasible, an optimal original flow has a constructible common
real-algebraic representation of polynomial encoding length. No fixed
quality count or affine-rank assumption is needed. The exponent may
depend on `s`; no practical-runtime or quadratic-field guarantee is
asserted.

If the pool has no allowed feed or no allowed outlet, force all its
incident flows to zero, reject incompatible incident lower bounds,
retain every external requirement, and solve the remaining LP. Assume
both kinds of pool arc exist below.

The proof divides according to whether any ordinary contracted output
receives positive pool flow. Such an output restricts the entire pool
quality vector to an affine space of dimension at most two. If none
does, only the fixed set of exceptional outputs can receive pool flow,
so output fractions give a different fixed-dimensional representation.

## 2. Existing fixed-dimensional quality-chart lemma

The reviewed
[fixed-rank proof](../notes/pooling-fixed-rank-contract-exceptions-algorithm.md)
uses a quality vector in a fixed number of affine coordinates. Its
incidence-flow argument does not require the source vectors to belong
to that parameter space. More precisely, let `C_i,B_j in Q^K` be arbitrary
ambient vectors, and restrict pool quality to

```
q=q_0+D eta,
```

where the rational matrix `D` has independent columns and a fixed
number `d` of columns. Then the same proof gives polynomial optimization
for this restricted class, with a core of dimension at most `d+5s`.
Here is the additional encoding and coverage argument when `K` grows.

Handle every full source-vector value `q=C_i` belonging to the selected
affine space and quality box by the original fixed-quality LP. The
membership checks are rational linear algebra and coordinate comparisons. For every other quality vector use directions

```
beta(k)=(1,k,...,k^(K-1)),
k=1,..., |I|*(K-1)+1.                               (1)
```

Every nonzero vector `C_i-q` excludes at most `K-1` values of `k`, so
one direction has `gamma_i=beta·(C_i-q)!=0` for every input. There are
polynomially many directions. Although their entries need not be small,
their bit lengths are `O(K log(|I|K+1))`, hence polynomial. For `K=1`
one direction suffices; with no quality coordinates the model is an LP.

After substituting the affine expression for `q`, every `gamma_i` is
affine in the fixed-dimensional `eta`. The transformed flow
`w_ij=gamma_i z_ij` gives a constant incidence matrix. At a two-inlet
ordinary output, each additional quality coordinate is exactly

```
a_h(q) w_1=f_h(q),
a_h=(C_1h-q_h)gamma_2-(C_2h-q_h)gamma_1,
f_h=gamma_1[b_j(B_jh-q_h)gamma_2-(C_2h-q_h)R_j],
R_j=b_j beta·(B_j-q).                               (2)
```

The quadratic terms in `a_h` cancel. The bracket in `f_h` is also affine
after cancellation, so `a_h` is affine and `f_h` quadratic in `eta`.
These identities hold for arbitrary ambient vectors, regardless of
whether they lie in the selected quality space. All `K` equations are
retained. A nonzero `a_h` supplies a rational arc equality bound; zero
`a_h` requires `f_h=0`. One- and zero-inlet cases retain their full
quality equations as in the reviewed proof.

The signs of polynomially many affine functions partition a fixed-
dimensional parameter domain into polynomially many cells, including
lower-dimensional cells. On each cell, connected path/cycle cuts cross
at most two edges. Polynomially many rational bound candidates per
edge therefore still give only polynomially many expanded cuts.
Clearing at most two selected affine denominators preserves constant
degree and polynomial coefficient length. The ambient dimension adds
rows and polynomial-bit coefficients, not retained variables.

All exceptional rows and the global mass and all `K` quality equations
are retained in the fixed core. The same equations prove actual pool
balance for every local lift. Standard profit is affine in the core.
The attainable-value and common-field recovery arguments in the reviewed
proof therefore apply unchanged.

## 3. An active contracted product gives a two-dimensional quality space

For an ordinary output `j` with exact demand `b_j` and exact quality
`B_j`, actual mass and quality conservation give

```
v_j + sum_i z_ij=b_j,
v_j*q + sum_i C_i*z_ij=b_j*B_j.
```

If `v_j>0`, then `b_j>0` and

```
q=(b_j/v_j) B_j - sum_i(z_ij/v_j) C_i.               (3)
```

The coefficients in (3) sum to one. At most two bypass input vectors
occur because the output's bypass degree is at most two. Thus

```
q in aff({B_j} union {C_i : bypass arc i->j exists}), (4)
```

an affine space of dimension at most two. This uses the exact product
quality and demand contract; an upper specification alone does not give
this identity.

For each positive-demand ordinary output, compute a rational affine
basis of (4) and apply Section 2 with `d<=2`. The basis has polynomial
encoding length. Restrict actual qualities coordinatewise between the
minimum and maximum allowed feed qualities. Intersect this box with
the affine space. Since `D` has independent columns, choose independent
coordinate rows to express `eta` as a rational affine function of those
quality coordinates; this yields polynomial-bit finite bounds on `eta`.
Retain all the other box rows too. No convex-hull intersection algorithm
is needed: an active pool's actual balance equations already force its
quality to be a convex average of the intake vectors.

There are only polynomially many candidate spaces. Dimension zero is
simply a fixed-quality LP. Empty intersections contribute no candidate.
It is unnecessary to impose `v_j>0` in its branch. Every branch retains
the complete original constraints, so every computed point is physically
feasible even if that particular outlet is inactive. Completeness follows
because any feasible flow with some active ordinary outlet belongs to
at least one enumerated space by (3).

## 4. When only exceptional products receive pool flow

For the remaining branch, force every pool outlet at an ordinary output
to zero, respecting its individual lower bounds. Every ordinary output
then receives bypass flow only. Let `r<=|E_J|` be the number of allowed
pool arcs to exceptional outputs. If `r=0`, force all pool arcs to zero
and solve the remaining original LP, keeping all external requirements.

Otherwise retain all pool feed arcs incident to exceptional inputs,
all `r` exceptional outlet flows `v_j`, every bypass arc incident to
an exceptional node, and `r` output fractions `theta_j`. There are
at most `3|E_I|+4|E_J|` retained coordinates: at most `|E_I|` exceptional
feeds, at most `2|E_I|+2|E_J|` exceptional incident bypasses, and `2r`
outlet/fraction coordinates. An arc is counted only once.

Exceptional input throughput `A_i=y_i+sum_j z_ij` is a core expression.
Retain all its original supply bounds, all retained arc bounds, and all
exceptional output requirements.
At an ordinary input eliminate `y_i=a_i-sum_j z_ij` with its inlet
bounds, using zero for an absent inlet. At an ordinary output impose
the exact bypass-only rows

```
sum_i z_ij=b_j,
sum_i C_i*z_ij=b_j B_j.
```

These are rational linear rows on at most two bypass variables; their
coefficients have no quality parameter. Delete the exceptional nodes
and apply the reviewed compact two-variable boundary projection to the
remaining paths, cycles, and isolated components. Its size and coefficient
length are polynomial. All boundary flows stay in the core.

Define affine core expressions

```
S = sum_ordinary_inputs a_i + sum_exception_inputs A_i,
G = sum_ordinary_inputs C_i*a_i + sum_exception_inputs C_i*A_i,

T = S - sum_ordinary_outputs b_j
      - sum_(bypass arcs into exceptional outputs) z_ij,
Q = G - sum_ordinary_outputs b_j B_j
      - sum_(bypass arcs into exceptional outputs) C_i*z_ij. (5)
```

Summing the exact ordinary product rows proves that `T,Q` equal the
actual summed intake mass and vector-quality mass for every local lift.
In particular, detached components may have different individual feed
flows but contribute the same total masses fixed by their contracts.

Impose

```
theta_j>=0, sum_j theta_j=1,
v_j=theta_j*T.
```

At each exceptional output use the actual quality mass
`theta_j*Q+sum_i C_i*z_ij` and actual total throughput
`v_j+sum_i z_ij`, retaining every demand and quality bound. These rows
have degree at most two in the fixed core, irrespective of `K`.
At positive `T`, the actual pool quality is `Q/T`; at zero `T`, all
nonnegative reconstructed intakes vanish and therefore `Q=0`. Fractions
are then immaterial. Summing `v_j=theta_j T` gives actual mass balance.

Conversely every original feasible flow in this branch gives these
coordinates, using `theta_j=v_j/T` when active and any legal simplex
point when inactive. This proves exact equivalence. Standard economics
reduces to the fixed ordinary throughputs plus the exceptional core
throughputs. Fixed-dimensional quadratic optimization and algebraic
lifting therefore solve this branch in polynomial bit time, even for
arbitrarily many quality coordinates.

## 5. Union, attainment, and limitations

The active-ordinary-product spaces and the exceptional-only branch
cover every original feasible flow. Each branch is sound. There are
polynomially many branches, and each uses a fixed-dimensional algebraic
procedure with polynomial encoding. Take the exact union of attainable
profit values and select its attained maximum. The original physical
flow model with a bounded pool-quality box is compact. Keep strict sign
conditions in chart cells; do not replace them by closures at a vanishing
denominator. The exceptional-only fraction branch is closed and bounded.

Reconstruction stays in one polynomial-degree real algebraic field.
The quality-chart branches use incidence-flow recovery and division by
nonzero `gamma_i`. The exceptional-only branch uses the reviewed rational
affine endpoint lifting and, if a reported active concentration is
needed, the single ratio `Q/T`. All original flows satisfy the actual
pool conservation and homogeneous product-quality requirements.

This theorem removes the fixed-rank restriction but retains the
fixed number of exceptional external nodes, exact ordinary contracts,
bypass-degree-two topology, and redundant common pool bounds. It does
not claim unrestricted degree-two pooling or dense arc-cost optimization.
The fixed-rank proof remains a verified supporting milestone. The
new obligations are the active-product affine-space observation, the
ambient-dimension chart encoding, and the exceptional-only branch;
each passed the fresh audits linked below.


## 6. Verification and attribution

The [first fresh full audit](../notes/review-pooling-contract-exceptions-arbitrary-qualities-benders.md)
and [second fresh full audit](../notes/review-pooling-contract-exceptions-arbitrary-qualities-second.md)
passed. They checked the active-product affine space, the ambient-quality
chart encoding, singular membership tests, all additional quality equations,
the exceptional-only branch, compact attainment, and exact algebraic recovery.
The second reviewer proposed the affine-space observation; the first
reviewer independently reconstructed the complete proof afterward.

The scalar and fixed-rank dependencies retain their own separate full
reviews. Their [vector-quality checker](../code/pooling_bypass_paths/check_fixed_rank_scaled_cuts.py)
passed 164 original physical LP fibers and 1,461 nonsingular chart comparisons;
193 source-vector singular cases used original LPs. Omitting extra quality
equations produced 678 false-positive chart cases. An independent symbolic
checker verified 45 residual/degree identities and 32 chart-cover cases.
The earlier [fixed-product substitution checker](../code/pooling_bypass_paths/check_fixed_product_contracts.py)
passed 90 original/substituted fixed-split comparisons. These finite checks
support distinct local mappings. They do not implement the full arbitrary-
quality branch enumeration or real-algebraic global optimization.

The algorithm combines established tools: signed circulation with interval
node imbalances, two-variable linear projection, rational affine algebra,
and fixed-dimensional real-algebraic decision. The exact circulation
criterion is stated in Schrijver, *Combinatorial Optimization*, Part I,
[Corollary 11.2i, printed page 175](https://www.lamsade.dauphine.fr/~cornaz/Enseignement/M2_MODO/DATA/A1.PDF).
The [bounded source audit](../notes/pooling-quality-scaled-contracts-novelty.md)
compares the pooling scope with checked primary work of Boland, Kalinowski
and Rigterink; Baltean-Lugojan and Misener; and Luedtke and coauthors.
Their checked statements do not supply this fixed-exception classification.
This is qualified evidence of a distinct result, not a proof of exhaustive
novelty. No novelty claim is made for the underlying circulation or
algebraic primitives.

## 7. A sharp feasibility boundary at output degree three

The separately doubly reviewed
[five-exception hardness theorem](pooling-five-exception-feasibility-hardness.md)
gives a matching negative result. With one pool, two actual feed arcs,
two actual outlet arcs, and input total out-degree at most two:

- If output total in-degree is at most two and the number of exceptional
  external nodes is fixed, feasibility is polynomial by the present
  theorem. It allows arbitrary quality count and input-quality rank.
- If output total in-degree is at most three, feasibility is strongly
  NP-complete already with one scalar quality and five exceptions:
  three variable-supply inputs and two primary products. Every other
  source and product has its exact flow/quality contracts. All flow
  bounds and qualities come from fixed finite sets, and the pool bound
  two is redundant because it has two unit-capacity outlets.

This compares total output degrees; the positive theorem actually needs
only bypass degree at most two. The hard instance includes ordinary
three-inlet bypass products, so it lies outside that positive scope.
The hardness concerns ordinary feasibility with positive exact contracts,
not a hidden profit threshold. Its source threshold is implemented by
the physical circuit. Neither branch claims hardness for the all-zero-
lower-bound feasibility model, where zero flow is feasible.
