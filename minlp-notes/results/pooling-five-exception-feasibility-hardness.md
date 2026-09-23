# Strong pooling feasibility hardness with five contract exceptions

Date: 2026-09-05. Status: two independent full mathematical audits PASS,
including the original-network compiler. A bounded primary-source search
found no matching theorem with the combined restrictions; this does not
certify publication priority.

The independent audits are by
[pooling_degree_two](../notes/review-pooling-fixed-exception-hardness-degree-two-agent.md)
and [benders_review](../notes/review-pooling-fixed-exception-hardness-benders.md).

## 1. Statement

Consider standard one-pool pooling with direct input-output arcs and one
scalar conserved quality. Call an external node exceptional if an input
does not have an exact total supply, or an output does not have both an
exact demand and an exact quality. The following feasibility problem is
**strongly NP-complete** under the following restrictions:

- The pool has exactly two feed arcs and two outlet arcs.
- Every input has total out-degree at most two; every output has total
  in-degree at most three.
- There are at most five exceptional nodes: three inputs and two outputs.
  All other inputs have exact supplies. All other outputs have exact demand
  and exact quality.
- Every flow bound is in `{0,1,2,3,4}`. The pool has lower bound zero and
  redundant upper bound two, certified by its two unit-capacity outlets.
- All input qualities and all specified output quality bounds belong to
  the fixed set `{0,1/66,1/33,1/22,1/11,1/2,1}`. Exceptional outputs have
  upper quality bounds only.
- No economic objective or external threshold row is required.

Exact flow and quality contracts are essential hypotheses of this
statement. It does not claim all lower bounds are zero. The bypass degree
is at most two at inputs and at most three at outputs. The comparison
with a bypass-degree-two polynomial algorithm concerns this difference
in output degree, with the same fixed exception count and scalar quality.

## 2. Starting reduction and retained physical interface

Use Sections 1--4 of the reviewed
[constant-data two-feed reduction](../results/pooling-constant-data-two-feed-np-completeness.md),
before its contract-completion objective is introduced. The explicit
Matsui source construction gives a rational simplex polytope `P`, positive
factors `U,V`, and threshold `K`. Dyadic normalization yields coefficients
`a_i in [1,19)`, positive `b_i`, and dyadic
`r_i=(a_i-1)/32 in [0,1)`, all with polynomial binary encoding.

The signal circuit imposes the source cone on `x>=0`, `T=sum_i x_i<=2`,
`h=sum_i r_i x_i`, `l+h=T`, and the affine comparison
`sum_i b_i x_i>=K`. All signals lie in `[0,2]`; coefficient magnitudes are
encoded by polynomially many binary averaging gates. The only actual
pool intakes are `l,h`, from qualities one and 33. Therefore their quality
mass is `l+33h=sum_i a_i x_i`.

The first unit-capacity primary output combines pool flow with a
zero-quality anchor of capacity one and has upper quality one. The second
unit-capacity output has redundant upper quality 33. For an active
mixture `z=x/T`, the maximum feasible radial throughput is
`1+1/a(z)`. Hence the contracted network is feasible exactly when

```
there exists z in P with b(z)(1+1/a(z)) >= K,
```

which the starting reduction proves equivalent to `U(z)V(z)<=K`.
The positive threshold is already encoded by a physical gate circuit;
it is not supplied as an extra optimization or nonlinear constraint.
It excludes zero intake. The source reduction and all these equivalences
are unchanged by the exact projection transformations below.

## 3. Replace every variable comparison source

The existing comparison gate `u<=v` uses a source on ports `u,2-v`
with supply interval `[0,2]`. Replace it by an exact-supply-two source
on `u,s,2-v`, where `s` is a new ordinary signal in `[0,2]`. This gives
the exact equation `u+s=v`. The extension exists exactly when `u<=v`,
since its unique slack `v-u` then belongs to `[0,2]`.

Apply this replacement to all source-cone and threshold comparisons.
Equality gates retain exact supply two; averaging, addition, full/half
coupling, zero, and unit gates already have exact supplies. A fresh slack
signal uses the same closed copy cycle as every other signal. Thus the
replacement introduces polynomially many ordinary physical nodes.

## 4. Group unused ports by their gate

The starting compiler feeds each unused positive-quality port from a
separate variable private input. These inputs cannot remain if the
exception count is to be fixed.

For an exact gate source with quality three, requested port capacities
`c_h`, requested flows `f_h`, and exact supply `S`, the unused complementary
ports have flows `c_h-f_h`. Full-port pairs have total two; half-port pairs
have total one. Group these unused ports under one additional quality-three
source of exact supply `sum_h c_h-S`. Its source equation follows from
`sum_h f_h=S`, and conversely imposes no new condition on the requested
port assignment.

The supplies remain constant:

| Gate | Requested port capacities | Supply | Complement supply |
|---|---|---:|---:|
| Average or full/half coupling | 2, 1, 1 | 2 | 2 |
| Addition or slack comparison | 2, 2, 2 | 2 | 4 |
| Equality | 2, 2 | 2 | 2 |
| Zero | 2 | 0 | 2 |
| Unit | 2 | 1 | 1 |

Grouping is exact in both directions once the copy formulas hold. Those
formulas do not rely on a private source's throughput: the closed-cycle
proof uses exact middle supplies, exact output demands, and exact
zero-quality links. Its sum of nonnegative quality residuals is zero,
forcing each residual to vanish. Thus there is no circular dependence
between grouping and the copy identities.

## 5. Split every three-port exact source

For a three-port source of exact supply `S` and capacities `c_h`, create
three same-quality sources of exact supplies `c_h`. Source `h` feeds its
original port with flow `f_h` and a new collector with flow `c_h-f_h`.
Give the collector exact demand `sum_h c_h-S` and exact quality equal to
the common source quality. This is equivalent to `sum_h f_h=S`.

This splitting applies to both supply-two and supply-four sources. The
collector demands are two or four; supplies and arc capacities are at
most two. It reduces every three-port input to inputs of out-degree two,
and the new collector has in-degree three. One-port and two-port sources
already satisfy the input bound. The construction uses distinct output
ports for each occurrence, so no parallel physical arc is needed.

## 6. Exact ordinary products and the five exceptions

The closed full-copy cycles force every output upper quality tight,
including the two conversion gadgets with endpoint qualities one and 33.
The half-copy cycles similarly force their quality bounds tight. We may
therefore impose those qualities exactly. Every collector receives only
one source quality, so its exact quality is also automatic.

After grouping and splitting, all gate, link, middle, and collector inputs
have exact supplies. The only remaining variable inputs are the private
positive-endpoint filler in each of the two conversion gadgets and the
zero-quality anchor. There are exactly three such inputs. The two primary
outputs have variable demands and upper quality specifications. Every
other output has exact demand and exact quality. This gives five exceptions.

Ordinary copy outputs have in-degree three. Splitting never increases
that degree, and collectors have in-degree three. Inputs have out-degree
at most two including their pool arcs. The pool still has two feed arcs
and two outlet arcs. The unit outlet capacities imply throughput at most
two, so the pool upper bound two is redundant independently of the circuit.

The unscaled quality alphabet remains
`{0,1/2,1,3/2,3,33/2,33}`. Dividing every quality by 33 gives the alphabet
in Section 1. All flow bounds remain in `{0,1,2,3,4}`. Exact quantities
zero and one are handled by their gates in the table; no positive lower
bound of variable magnitude is introduced.

## 7. Complexity and certification

Each modification has size linear in the number of affected ports or
gates. The starting binary circuit already has size polynomial in the
source instance. Thus the final network is polynomial-size and all its
numerical data come from fixed finite sets. Unary encoding remains
polynomial, proving strong NP-hardness by the source equivalence.

NP membership follows from the reviewed
[fixed-parameter linear-fiber lemma](../results/fixed-parameter-linear-fibers-np-membership.md):
fixing the single scalar pool quality makes the complete bounded-flow
physical feasibility model linear. Guess an active flow basis; Cramer
polynomials and fixed-dimensional algebraic feasibility give polynomial
verification. This is the same membership argument as for the starting
one-pool theorem, and does not require rational physical witnesses.

The [degree-two algorithm](../results/pooling-contract-exceptions-algorithm.md)
and this theorem therefore give a
matching output-degree boundary for feasibility with fixed contract
exceptions. No claim is made that the underlying copy, slack, circulation,
or source-splitting principles are themselves new. The bounded source
comparison in Section 9 qualifies priority for the combined restriction.

## 8. Original physical network checks

[The separate compiler and checker](../code/pooling_bypass_copy/check_fixed_exception_hardness.py)
uses the existing binary circuit front end but replaces its comparison
and port compilation. The solver receives only original input/output/arc
flow bounds, exact or upper quality rows, pool mass conservation, and
pool quality conservation. It receives no signal identities, cone rows,
threshold row, or comparator equation directly.

Sixteen original-network global feasibility solves matched exact rational
source-polytope reference values on both sides of the threshold. Cases
include an empty source polytope, an equality slice, threshold equality,
and the endpoint `a=1`. Every assembled network asserted exactly five
exceptions, the fixed quality/flow palettes, two actual feeds and outlets,
input degree two, output degree three, and distinct arcs. These are small
floating-point global solves, not exact symbolic certificates or a test
of the asymptotic reduction. Both independent full proof reviews passed. The numerical log is
[retained here](../code/pooling_bypass_copy/fixed_exception_hardness_output.txt).

## 9. Bounded source comparison

A focused open-source search on 2026-09-05 did not find the combined
five-exception, constant-data, one-pool degree restriction. This is a
bounded search result, not a certification of priority. The broad hardness
of pooling and the earlier constant-data construction are already known
within the source literature and this repository, respectively.

[Boland, Kalinowski, and Rigterink](https://arxiv.org/pdf/1508.03181),
Section 1, page 2, explicitly omit direct input-output arcs from their
complexity model. Replacing bypasses by auxiliary pools changes the
one-pool restriction, so their fixed-input polynomial result does not
apply to this network. Their survey also establishes that broad degree
restrictions alone have substantial earlier hardness literature.

[Baltean-Lugojan and Misener](https://pmc.ncbi.nlm.nih.gov/articles/PMC6417401/),
Assumption 2.2, keep fixed product demands but remove feed availability
and pool capacity constraints for their scalar-quality algorithms. That
assumption differs from the shared exact source supplies used here.
The present theorem should therefore be presented as a structural
refinement paired with the contract-exception algorithm, rather than
as a first proof of one-pool or scalar-quality hardness.
