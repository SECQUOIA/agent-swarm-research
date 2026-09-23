# Independent review: constant-data hardness with two pool feeds

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the complete mathematical construction passes this independent
audit, including its strong NP-completeness conclusion.** This reviews
[the candidate](pooling-constant-data-two-feed-hardness.md). I also
inspected the assembled original-network implementation and independently
ran 20 physical network solves, all passing. My separate exact arithmetic
checker passed 1,460 dyadic-multiplier and signed-row cases and two
normalizations of the actual source-factor bounds.

The proposed strong NP-completeness claim is supported by the proof.
Large source
numbers are encoded by polynomially many constant-data gates; they do
not appear as physical coefficients. The decision threshold is at most
four times the number of contracted nodes. The construction has one pool
with exactly two incoming and two outgoing arcs, input total out-degree
at most two, output total in-degree at most three, one scalar upper-only
quality, and no positive lower flow bounds in its final instance.

## Source normalization

The previously checked Matsui generator bounds are adequate. For
`D` the largest power of two not exceeding `u0/2`,
`2D<=u0<4D`. Since `u0>P4`, this gives `D>P4/4`; also `D<P4`.
The bound `s<p^n` implies
`U_i<2P4+s p^(2n)+2s p^(3n)<5P4`, so `2<=U_i/D<20`.
Likewise `V_i<3P4`, and consequently `D V_i<K` on every unrestricted
simplex generator. Negative generator values of `V_i` cause no problem
for this upper bound or the resulting strict positivity of `b_i`.

Thus `a_i=U_i/D-1` lies in `[1,19)`, while
`b_i=K-DV_i` is a positive integer. The weights
`r_i=(U_i-2D)/(32D)` are nonnegative dyadic rationals less than one.
The powers, denominators, and integer rewards all have polynomial binary
length in the source instance. Exact checks at source sizes 5 and 6
also confirmed these inequalities; their `D` values have 29,025 and
80,403 bits, illustrating why numerical magnitudes must be encoded in
circuits rather than inserted into the physical data.

## Circuit arithmetic and physical realization

The dyadic multiplication recurrence has the correct bit order. After
processing bits `c_0,...,c_(k-1)` from least to most significant, its
value is
`x*(sum_(h<k) 2^h c_h)/2^k`. The next averaging gate gives the same
identity for `k+1`. All intermediate values are averages of signals in
`[0,2]`, so no port range is violated. Zero coefficients need only a
zero signal, and a unit coefficient can copy the input signal.

For a signed integer row, choose `B>sum|c_i|+|d|` as a power of two.
Place its positive terms on one side, negative terms on the other, and
move the signed constant appropriately. Each side is at most
`(2 sum|c_i|+|d|)/B<2`, regardless of which terms have which signs.
Since terms are nonnegative, every partial sum is also below 2. The
addition gates therefore impose no extra restriction on a feasible
bounded signal assignment. Conversely, their exact supply equations
force the intended sum, and the final comparison is precisely the
original row after multiplication by positive `B`.

The zero row, zero constant, negative constant, and repeated signal
occurrences are harmless under the explicit port-allocation convention.
Every occurrence receives its own gadget. Source qualities match because
all arithmetic ports come from ordinary quality-three gadgets, while
the separate quality-one and quality-33 conversion gadgets are used
only for actual pool feeds. The already reviewed closed full/half cycles
force the required equalities from upper quality bounds. They remain
valid with a unit signal forced by an exact-one source.

The numbers of gates and port occurrences are polynomial in the binary
length of the rational row description: denominator clearing has
polynomial bit cost, the chosen power-of-two exponent is polynomial,
and every multiplier uses one gate per bit. Copying repeated gate uses
also has polynomial size. No physical arc gets an exponentially large
capacity or a tiny rational coefficient from this arithmetic encoding.

## Two-feed interface and product threshold

The sum gates impose `T=sum x_i<=2` and `h=sum r_i x_i`; their feasible
partial sums never exceed `T`, because all terms are nonnegative and
`r_i<=1`. The equation `l+h=T` has a nonnegative solution `l` in the
same signal range. Only these two signals are converted into actual
pool intakes. Their fixed qualities give
`l+33h=T+32h=sum a_i x_i` exactly.

The pool therefore has the same total intake and quality mass as the
old many-feed reduction. For a positive source total and normalized
mixture `z=x/T`, its two outlets and anchor permit precisely the radial
throughput bound `T<=1+1/a(z)`, where `a(z)>=1`. The boundary case
`a(z)=1` is valid: throughput 2 is attained with no anchor needed.

The circuit constraint `sum b_i x_i>=K` forces positive total intake.
The homogeneous source rows then give `z in P`, and positivity of
`b(z)` allows comparison with the maximal radial throughput. The identity

```
(K-DV(z)) * (U(z)/D)/(U(z)/D-1) >= K
iff U(z)V(z)<=K
```

has a strictly positive denominator and is correct. For a source yes
point, the maximal-throughput construction keeps every original signal
and all partial sums within their bounds. The reverse implication uses
only the exact gate equations, perfect mixing, and primary output bounds.
The contracted network may now be infeasible when the source instance
is no; no zero-intake feasible repair is assumed or needed.

## Degree reduction and finite data

The addition source's three ports have capacities `(2,2,2)` and exact
supply 2. Splitting it into three same-quality exact-two sources and
a collector of exact demand 4 is the same complement-flow identity as
the previously reviewed `(2,1,1)` splitter. Every original feasible
port assignment extends, and collector mass recovers its original sum.
New source out-degrees are two, and the collector in-degree is three.
All other gate, cycle, conversion, and private source types meet the
claimed degree bounds. Repeated operands do not introduce parallel arcs.

The listed seven quality values cover ordinary full/half gadgets, both
feed conversions, collectors, and primary outputs. The capacity alphabet
`{0,1,2,3,4}` covers all gates, unit/zero sources, cyclic links, collectors,
and pool/primary bounds. Rescaling all qualities by 33 produces another
fixed rational alphabet. No unlisted source coefficient is left in a
quality, capacity, cost, or revenue field.

## Completion objective and strong NP-completeness

Each exact positive source or output contract appears once in the list
`Ew=e`, with `e_j in {1,2,3,4}`. After deleting its lower bound, the
corresponding upper bound ensures a nonnegative deficit. Therefore
`sum E_j w<=sum e_j`, and equality is equivalent to zero deficit in
every contract. An optimum reaching that known ceiling is exactly a
feasible contracted network. This argument does not require a Hoffman
bound, a limiting argument, or any promise that the contracted system
is nonempty.

Counting source/output incidences gives an ordinary linear arc objective
with coefficients at most two. Equivalently, cost minus one on contracted
inputs and revenue one on contracted outputs produces precisely contract
completion. Adding one to all input costs and all output revenues cancels
through total mass conservation, including the actual pool. The final
input costs are 0 or 1, and output revenues are 1 or 2; the threshold
is unchanged. Primary outputs with no demand contract do not receive
an accidental extra completion reward after this cancellation.

The transformed network has polynomial size. Every numerical parameter
is from a fixed finite alphabet except its integer threshold, which
is linear in node count. Its unary encoding therefore remains polynomial.
This is enough to transfer NP-hardness to the strongly bounded family,
even though the starting positive-product construction used large
binary numbers: those numbers have been replaced by polynomial-size
topology. The previously audited one-pool/one-quality LP-fiber certificate
supplies NP membership. Thus the stated strong NP-completeness conclusion
follows from the complete construction; priority remains a separate
literature question.

## Independent arithmetic validation

The [exact arithmetic checker](../code/pooling_bypass_copy/check_constant_data_arithmetic_review.py)
uses `Fraction` arithmetic. It checks 960 dyadic multipliers with varying
bit lengths, 500 signed rows including negative constants and bounded
partial sums, and the two actual source normalizations described above.
All passed.

## Independent original-network validation

I inspected [the assembled checker](../code/pooling_bypass_copy/check_constant_data.py).
It compiles signals and gates to physical source/output nodes, closes
full and half cycles, installs only the two fixed-quality pool feeds,
and applies the source splitter. Its solver uses the original physical
flow and upper-quality constraints with all positive lower flow bounds
removed. It inserts no intended gate equation or source-cone row directly.
With zero intake rewards, its objective is negative total contract
deficit, exactly the completion objective minus its known ceiling.

The independent run with seed 71 and five randomized trials passed
14 global solves: yes/no threshold pairs and four source/boundary
cases. These include an empty source polytope and the `a=1` endpoint.
The program checks the fixed quality and capacity alphabets, two pool
inputs and outputs, input degree at most two, output degree at most
three, and absence of parallel arcs. Weakening only the final threshold
comparison's upper supply from 2 to 4 turns a no case into a completion
yes case: its minimum deficit changes from approximately `0.10714286`
to zero. This detects the intended role of the threshold circuit.

Six further independently chosen solves test longer dyadic multipliers,
three original input signals, and a non-dyadic rational source row before
denominator clearing. They use, respectively, `a=(9/8,75/4)` with equal
mixture signals; `a=(3/2,17/4,2)` with the first two signals equal; and
the source inequality `(2/5)z_1<=1/7`. Each family was tested immediately
below and above its exact rational reference optimum. All passed.

The [randomized/boundary log](../code/pooling_bypass_copy/constant_data_independent_review_output.txt)
and [additional cases](../code/pooling_bypass_copy/constant_data_independent_edge_cases.txt)
are retained. These are small physical circuit instances, not a numerical
run of the enormous source-size-five network. The polynomial-size and
strong-hardness statements rest on the independently checked reduction,
not extrapolation from solver runs. No outstanding mathematical defect
was found in this audit.
