# Second independent review: one-pool bypass copy hardness

Date: 2026-09-05. Verdict: **PASS**, with the empty-source objective
identity clarified during review. The proof establishes the stated
ordinary NP-hardness. It does not establish strong hardness, an
upper-flow-bound-only variant, or first-in-literature priority.

Reviewed: [bypass-copy candidate](pooling-one-pool-bypass-copy-hardness.md),
including the revised zero-profit term for an empty source polytope and
the input-cost/nonnegative-revenue variant. The reviewer reconstructed
the assembled-network projection before inspecting the author's test code.

## 1. Four-port algebra and composition

At one gadget output, exact demand four and exact quality at the midpoint
give `(alpha-beta)(u-v)/2=0`. Distinct endpoint qualities imply `u=v=x`.
The middle flow is consequently `4-2x`. Endpoint arc bounds imply
`0<=x<=2`, making that middle flow nonnegative and at most four.
The second output has the same structure, and exact total middle supply
four forces the parameters to sum to two. Thus the four-port relation is
both necessary and sufficient, including its endpoint cases.

An exact-supply-two input joining a complement port of one gadget to a
positive port of the next enforces `(2-x)+x'=2`, hence `x'=x`.
Its outgoing arcs carry the same prescribed quality zero, so sharing the
source is physically valid. A chain supplies distinct quality-two positive
and complement ports without adding any mixing pools.

There is a concrete allocation without duplicate arcs or shared ports.
For each variable, make at least as many ordinary gadgets as the larger
of its total positive and negative coefficient multiplicities. Assign
quality-two positive ports to positive row occurrences and complement
ports to negative row occurrences, each once. Unassigned ports have
separate private sources. Connect consecutive quality-zero ports by
distinct exact-supply-two sources. This uses polynomially many gadgets
when the total coefficient magnitude is polynomial.

The last conversion gadget uses qualities zero and `a_i`, which are
distinct because the source construction gives `a_i>1`. Its complement
port has quality `a_i` and flow `2-x_i`. An input of that quality with
exact supply two, outgoing only to this port and the mixing pool, therefore
has pool intake exactly `x_i`. The other conversion port has a private
source and carries the same `x_i`; it cannot create an additional pool
intake. The initial/final zero-quality ports and all unused ports require
only capacities two, so they introduce no further signal restrictions.

Equal quality labels on distinct inputs do not force those inputs to be
merged. In particular, a conversion middle quality that happens to equal
some ordinary port quality causes no accidental coupling.

## 2. Constraint-source capacities encode the entire cone

A row source has outgoing flow
`sum_i c_i*x_i + 2*sum_{c_i<0}(-c_i)`. Its stated upper capacity is
exactly equivalent to `c*x<=0`. Every outgoing arc is a distinct
quality-two port, matching the source quality. The source has no other
outlet. Zero-capacity rows and rows with only one coefficient sign work
under the same identity. Opposite inequalities encode equality.

Together with the chain and conversion equations, the projection onto
pool-intake coordinates is exactly
`{x in [0,2]^m : Cx<=0}` before imposing the pool's own throughput
and output constraints. Necessity follows from each ordinary source's
capacity. Sufficiency follows by filling all displayed port/middle flows
and assigning every private source its required nonnegative flow. There
is no unaccounted mass source, auxiliary pool, or route around the row
capacities.

## 3. Matsui source size and coefficient signs

The reviewer previously read Sections 2–3 and Theorem 3.1 of
[Matsui's primary manuscript](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf)
and checked its explicit bounded base-variable construction again for this
reduction. Its large numbers occur in affine objective factors, while
the base polytope has the stated unit-cube, McCormick, and zero-one matrix
constraints. Eliminating its affine auxiliary variables gives the required
positive-product source with polynomial coefficient bit lengths.

After `w_h=s*z_h` and homogenization at `T=sum x_i`, a cube upper bound
becomes `s*x_h-T<=0`; a McCormick lower bound becomes
`s*x_i+s*x_j-s*x_ij-T<=0`; and a source row becomes
`s*sum_i M_ri*x_i-T=0`. Coefficients have magnitude at most `s+1`.
There are polynomially many rows and coordinates, so replicating ports
according to coefficient magnitudes remains polynomial. This step does
not attempt to copy the exponentially large numerical values in the
product objective.

On the unrestricted simplex generators, the first factor is at least
`2*p^(4n)-p>2`. The second is at most
`2*p^(4n)-p+s*p^(2n)`. From `s<p^(2n)`, this is less than
`3*p^(4n)`, hence less than `K=4*p^(8n)`. Thus every individual
conversion quality `a_i=U_i-1` exceeds one and every reward `b_i=K-V_i`
is positive. The required powers have polynomial binary length even though
their values are large. Positive `V` on the actual source polytope is
supplied by Matsui's theorem.

## 4. Pooling optimum and zero throughput

At positive pool throughput, the copied intake vector satisfies `Cx<=0`,
so `z=x/T` belongs to the embedded source polytope. The pool's quality is
the actual intake average `a(z)`. It sends flow only to the two designated
outputs, and only the stated anchor can bypass into the first output.
Consequently its output-1 quality constraint gives `y_1<=D_1/a(z)`.
With both output capacities one and nonnegative reward,
`profit=b(z)*T<=b(z)*(1+1/a(z))`.

Conversely, the proposed saturated-output routing realizes every source
point's displayed value. Its pool intakes are at most two, and the exact
copy-network projection established above extends these intakes to all
gadget demands and source contracts. Hence the scalar optimum identity
and the positive-product threshold equivalence are valid.

At zero pool throughput, all copied signals are zero, but their complement
ports still carry two. Middle sources send four to their positive-side
outputs and zero to their complement-side outputs; chain connectors,
conversion inputs, row sources, and private inputs all remain feasible.
The profit is zero. This handles empty source polytopes without a
preprocessing oracle. The displayed optimum must therefore include zero
explicitly, as the revised draft now does; an unqualified maximum over an
empty source polytope would not have been the correct identity.

## 5. Quality semantics, economics, and scope

The construction uses exact quality only at ordinary bypass-only gadget
outputs, where demands are positive. Exact quality is represented by one
physical quality with matching lower and upper bounds. Its conversion to
two upper-bound coordinates is valid: negate the quality for the lower
bound, and use a redundant upper bound in this second coordinate where
no original lower bound was imposed. Per-coordinate shifts and positive
scaling then put all quality data in `[0,1]` with polynomial bit length.
These transformations preserve midpoint equalities and all mass balances.

Moving reward `-b_i` from the mixing-pool intake arc to the private input
serving the conversion gadget's positive `a_i` port is valid because that
private input has exactly one outgoing flow, equal to `x_i`. Thus costs
may be attached to inputs rather than depend on the outgoing arc selected.
Adding a common charge `B>=max_i b_i` to all input production costs and
paying revenue `B` on every output's inflow cancels by total conservation.
It yields nonnegative production costs and revenues without changing profit.

The fixed middle supplies, fixed connector/conversion supplies, and fixed
gadget demands are essential to this proof. The statement correctly does
not remove those lower flow requirements. There is exactly one pool and
only two pool-to-output arcs; every other output receives direct input
arcs only. Counts of bypass arcs, inputs, and gadget outputs grow
polynomially. The construction therefore does not contradict a theorem
that additionally bounds the coupling through bypasses.

## 6. Independent assembled-network checks

The [reviewer's separate implementation](../code/pooling_bypass_copy/independent_review.py)
creates ordinary input nodes, output nodes, and physical arcs. It inserts
only source supplies/capacities, output demands, ordinary quality equations,
and arc capacities. It inserts **no** signal-copy equalities or cone rows
in the network LP.

The deterministic run passed 56 copy-network projection optimizations
against explicit cone LPs with separate random linear objectives. It also
passed 110 complete pooling LPs at fixed compositions, including 60
compositions excluded by the source cone. The latter LPs include the actual
two pool outputs, anchor, pool balance, and quality bounds; fixing composition
makes these particular verification subproblems linear. Both original and
shifted quality values were tested. These checks do not claim to solve the
unrestricted nonlinear instance globally.

A negative control replaces each exact middle supply by its upper bound.
For a cone enforcing `x0=x1`, the maximum of `x0-x1` changes from zero to
two. This detects the principal escape route that the fixed middle supply
must prevent.

Run output:

```
PASS: 56 full copy-network projection LPs against explicit cones.
PASS: 110 full pooling fixed-composition LPs, including 60 excluded compositions.
Negative control: weakening middle fixed supplies changes max(x0-x1) from -0 to 2.
Both original and shifted qualities tested; no cone rows or signal-copy equalities inserted in network LP.
```

The numerical tolerance was `1e-8`. These checks support the exact proof;
they are not formal certificates of the source hardness theorem.
