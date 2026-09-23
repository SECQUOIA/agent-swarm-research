# Audit of the proposed fixed-exception degree-three hardness refinement

Date: 2026-09-05. Status: this preliminary local audit is retained as a
development record. The complete construction subsequently passed two
fresh full audits and was promoted as
[the five-exception theorem](../results/pooling-five-exception-feasibility-hardness.md).

The starting point is the reviewed
[constant-data two-feed reduction](../results/pooling-constant-data-two-feed-np-completeness.md).
The proposed refinement keeps exact contracts, makes almost every source
throughput exact, and makes every nonprimary product quality exact. Its
purpose is to compare with the new polynomial algorithms when the bypass
graph has maximum degree two and only a fixed number of contracts vary.

## 1. Comparisons can use exact supply gates

For signals `u,v` in `[0,2]`, the inequality `u<=v` is equivalent to
the existence of a signal `s in [0,2]` with `u+s=v`. The existing exact
addition gate implements this equation using the three full ports
`u,s,2-v` and a quality-three source of exact supply two. Conversely,
nonnegative `s` implies the comparison. The bound on `s` follows from
`0<=v-u<=2`. Its signal-copy cycle and any subsequent splitting introduce
only linearly many additional nodes per comparison. No nonphysical row
is needed. Existing equality, zero, and unit gates retain exact supplies.

## 2. Unused ports must also receive exact supplies

Replacing comparison sources alone is insufficient: the current compiler
creates a separate variable private source for each unused positive-quality
port. The number of such sources is unbounded.

Group unused complementary ports by their original exact gate source.
Suppose that source has quality three, exact supply `S`, requested port
flows `f_h`, and port capacities `c_h`. The corresponding unused ports
have flows `c_h-f_h`: this follows from the full and half copy formulas,
with full capacity two and half capacity one. An additional quality-three
source of exact supply

```
S_complement = sum_h c_h - S
```

can feed precisely those unused ports. Its supply equation follows from
the original gate equation `sum_h f_h=S`. Conversely it adds no new
restriction to an assignment already satisfying that equation.

The relevant values are:

| Gate | Requested capacities | Exact supply | Complement supply |
|---|---|---:|---:|
| Average or full/half coupling | 2, 1, 1 | 2 | 2 |
| Addition, including slack addition | 2, 2, 2 | 2 | 4 |
| Equality | 2, 2 | 2 | 2 |
| Zero | 2 | 0 | 2 |
| Unit | 2 | 1 | 1 |

In particular, complementary addition sources have exact supply four.
The existing splitter's assertion that every three-port source has supply
two must be generalized in the new compiler.

## 3. The generalized splitter preserves degree and constant data

For a source with three outgoing ports of capacities `c_h` and exact
supply `S`, replace it by three same-quality sources of exact supplies
`c_h`. Source `h` sends `f_h` to the original port and `c_h-f_h` to one
new collector. Give the collector exact demand `sum_h c_h-S` and exact
quality equal to the source quality. Its demand equation is exactly
`sum_h f_h=S`. All new input degrees are two and the collector degree
is three.

For the original and complementary gates in the table, collector demands
are two or four and all supplies and capacities remain in `{0,1,2,3,4}`.
Two-port and one-port sources need no splitting. Every port occurrence
uses its own output, so grouping does not require duplicate physical arcs.

## 4. Exact qualities and the remaining exceptions

The closed-cycle proof already forces every full-gadget quality bound
tight, including the intake conversion gadgets. The same holds for
half gadgets. This argument uses the exact demands, middle supplies,
and closed zero-quality links; it does not assume any particular total
of a private positive-port source. Thus making these product qualities
explicitly exact before or after the grouping is equivalent. Collector
products receive only a single quality, so their exact quality also
adds no restriction.

The two conversion gadgets each still have one variable private input
on the unused positive endpoint. Together with the zero-quality anchor
and the two primary products, these give at most five exceptional
external nodes. All other inputs have exact supplies; all other outputs
have exact demand and quality. The tentative count of three exceptions
was incorrect because it omitted the two converter sources and the
unbounded ordinary private fillers before grouping.

## 5. Remaining checks and scope

The final implementation must count exceptions after all splitting and
must check its original physical network, without adding gate equations
directly to the solver. It must preserve the threshold comparison through
the slack gate. The common pool-capacity condition is explicitly redundant:
the two unit-capacity primary outlet arcs already imply pool throughput
at most two. Thus the original common pool upper bound two can remain,
preserving the numerical palette. More generally, the minimum of the
total source upper throughput, the sum of feed-arc capacities, and the
sum of outlet-arc capacities is a valid redundancy certificate. The
algorithm statements can use this certificate without adding any global
aggregate constraint to their projected models.

The local transformations introduce polynomially many constant-data
nodes and preserve the source reduction. They support the strong
NP-completeness result with five exceptions and output degree three.
The two subsequent full-construction audits are linked from the promoted
result above.
