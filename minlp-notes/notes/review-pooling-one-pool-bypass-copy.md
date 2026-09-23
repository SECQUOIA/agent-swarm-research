# Independent review: one-pool bypass-copy hardness

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the reduction is correct under its stated flow-contract model.**
I independently checked [the candidate](pooling-one-pool-bypass-copy-hardness.md),
its source reduction, the composition of the physical network, and original-model
computations. This is an ordinary NP-hardness result with one mixing pool, one
physical quality allowing lower and upper specifications, arbitrary bypasses,
and exact supplies and demands. The pool has only two outgoing arcs. Equivalently,
two quality coordinates with upper specifications suffice. Novelty and priority
are separate questions; prior broad hardness assertions prevent a first-result
claim without further literature work.

## Mathematical checks

At either gadget output, exact demand 4 and midpoint quality force the two
endpoint flows to coincide. Exact supply 4 at the private midpoint source then
forces the endpoint parameters at the two outputs to sum to 2. Conversely the
displayed assignment is feasible for every parameter in `[0,2]`. This argument
uses both fixed midpoint supply and exact output demand.

A quality-zero chain source with exactly two arcs and exact supply 2 equates
successive parameters because it supplies a complement and the next signal.
Every row occurrence uses a distinct quality-two port. The row-source capacity
is exactly the homogeneous inequality after adding the sum of complement
constants. The final conversion source has exactly two arcs: its complement
port and its pool intake. Exact supply 2 therefore forces the intake to equal
the copied signal. Its quality is precisely the required mixing quality.

The revised draft explicitly makes midpoint sources private to their gadget,
chain sources private to their two joined ports, conversion sources private to
their two arcs, and unused sources private to their single port. Equal qualities
do not merge nodes. These source identities rule out flow escape and accidental
sharing. All gadget arcs are ordinary input-to-output bypasses, and no extra
pool or intermediate mixing operation is introduced.

The simplex embedding has polynomial dimension. Homogenizing Matsui's cube,
McCormick, and zero-one source-equation constraints produces integer coefficients
of magnitude at most `s+1`. Consequently the total number of signal-port copies
is polynomial. This bounded-coefficient argument is essential: the copying
construction would be pseudopolynomial on arbitrary binary integer rows.

The direct Matsui factor formulas give `a_i=U_i-1>1` and `b_i=K-V_i>0` at
every unrestricted simplex generator. The bound on a positive coefficient of
`V` uses `s p^(2n)`, while its other nonconstant generator coefficients are
negative; thus no large-coefficient feasibility cut is needed. The numbers have
polynomial binary length. The source NP-hardness and factor positivity were
also checked against the primary Matsui report in the earlier
[two-pool reduction audit](review-pooling-two-pools-two-outputs-hardness.md).

For positive pool throughput `T`, copied row constraints give `z=x/T` in the
source polytope. Main-output capacities and the first output's one-sided quality
bound imply `T <= 1+1/a(z)`. Nonnegative `b(z)` gives the objective upper bound;
the stated full-output construction attains it. Since `a(z)>1`, all individual
intakes and the total throughput obey their bounds. Every gadget can then be
filled from its signal without adding any constraint to the main construction.

I flagged the empty-source case during review. It is now corrected: the exact
objective is the maximum of zero and the source-point values. Zero signal leaves
the copy network feasible through complementary flows, even when the source
polytope is empty. Its profit is zero, below the positive threshold `K`.

Moving the negative cost to the private input supplying the conversion gadget's
signal port preserves the objective. Adding a common charge to every input and
the same unit revenue to every output cancels by total mass conservation,
including mandatory gadget flows. Thus nonnegative input costs and output
revenues are available without relying on arc-specific production costs.
Global positive quality scaling and shifts preserve the construction. A negative
duplicate quality converts lower specifications to upper specifications.

## Independent original-network checks

Using the project Python environment, I ran the author's
[checker](../code/pooling_bypass_copy/check_copy_reduction.py) with seed 17 and
10 trials. All 20 original-network solves, including shifted qualities, matched
the exact rational reference values. I also ran eight additional solves, at
quality shifts 0 and 7, covering no cone rows, an empty source polytope, zero
reward, and a repeated-copy equality system. Their reference values were,
respectively, `15/2`, `0`, `0`, and `16/3`.

The last system used `a=(2,5,3)`, `b=(7,1,4)`, and rows
`(3,-3,0)x<=0`, `(-3,3,0)x<=0`, `(2,-1,-1)x<=0`. It exercises both signs,
repeated ports, equality encoded by opposite rows, and reuse along chains.
The checker contains physical network constraints only; it does not directly
insert the intended copied equalities or cone inequalities. Removing the
midpoint supply lower bound changes a negative-control optimum from 10 to 20,
confirming that the tests detect the essential supply contract.

The independent logs are retained:

- [20 randomized and shifted solves](../code/pooling_bypass_copy/independent_review_output.txt).
- [Eight boundary and repeated-copy solves](../code/pooling_bypass_copy/independent_edge_cases_output.txt).

These small global solves corroborate the construction, but the mathematical
reduction supplies the hardness proof. This review does not establish strong
NP-hardness, hardness with upper flow bounds alone, or priority over prior work.
