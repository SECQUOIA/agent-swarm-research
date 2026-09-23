# Independent full audit: five-exception pooling hardness

Date: 2026-09-05. Reviewer: `pooling_degree_two`.

**PASS** for the complete construction in
[the five-exception note](pooling-fixed-exception-hardness-refinement.md),
including the final compiler and the redundant-capacity certificate.
This full audit replaces neither the separate author's local-transformation
review nor the requested second independent audit.

## Comparison replacement and the previously missing private sources

The exact source on `u,s,2-v` has supply two precisely when `u+s=v`.
Since both endpoint signals lie in `[0,2]`, a feasible slack in that
same range exists exactly for `u<=v`. This preserves every compiled
source-cone or threshold row without a hidden side constraint.

I independently identified why this change alone would not suffice:
the original compiler creates a separate variable-supply source for
every unused port occurrence. The final construction correctly groups
those ports by their exact gate source. A requested full port and its
unused complement sum to two; a half-port pair sums to one. Therefore
the complementary group's supply is exactly the sum of port capacities
minus the original gate supply. This adds no restriction beyond the
original gate equation. In particular, complementary addition and slack
comparison groups have supply four, not two. Zero and unit groups have
supplies two and one respectively.

The group identities rely on the closed-copy formulas, but those formulas
do not rely on the unused private source supplies. Exact middle supplies,
exact output demands, and closed zero-quality links force all homogeneous
upper-quality residuals to zero. This direction of the argument avoids
circularity. The full, half, and two intake-conversion formulas are the
ones already independently checked in the constant-data construction.

## Splitting, exact qualities, and complete exception count

For any three-port exact source with supply `S` and port capacities
`c_h`, the replacement sources have exact supplies `c_h` and send residuals
`c_h-f_h` to one collector. Collector demand `sum c_h-S` is equivalent
to the original source equation in both directions. This holds for
supply four as well as supply two. Every new demand remains two or four;
every replacement input has degree two and the collector has degree three.
Its quality equality is automatic because all feeding sources have the
same known quality.

Closed-copy quality tightness permits exact quality requirements at every
ordinary gadget output. It includes the conversion gadgets whose endpoint
qualities are one and 33. The two private positive-endpoint conversion
fillers remain variable sources and are explicitly counted; they are
not grouped with quality-three gate ports. Together with the anchor
they give three exceptional inputs. Only the two primary outputs have
variable demand or nonexact quality. Thus the complete network has
exactly five exceptions, independent of circuit length and coefficient
encoding. I found no other variable-supply source type in the compiler.

The pool still has two feed and two unit-capacity outlet arcs. Hence its
upper bound two is redundant directly from the outlet capacities, with
lower bound zero. This is the same certified redundancy allowed by the
positive theorem; no assumption about a circuit-implied intake total is
needed for this particular capacity check.

## Physical and complexity preservation

All input total out-degrees, including pool feeds, are at most two.
Every output total in-degree is at most three. Distinct gadgets supply
distinct ports, and the splitter uses one new collector with separate
replacement sources, so no parallel arc is introduced. The flow palette
remains `{0,1,2,3,4}`; the quality palette is the unchanged fixed seven
values, optionally divided by 33.

The modifications are linear in the number of gate occurrences. The
reviewed binary circuit encodes source coefficients with polynomial
topology, so the complete reduction has polynomial size and fixed
numerical data. The Matsui decision equivalence is unchanged because
every local modification is an exact feasibility projection. Its positive
threshold remains a physical comparison circuit. No economic threshold
or nonphysical global row is introduced. The conclusion is strong
NP-hardness, and the reviewed single-quality linear-fiber certificate
supplies NP membership for the bounded physical model.

I inspected
[the separate compiler](../code/pooling_bypass_copy/check_fixed_exception_hardness.py).
It implements exact slack comparisons, groups complementary ports before
splitting, permits supplies two and four in the splitter, keeps the two
converter fillers private, and asserts the complete exception count and
degree/palette restrictions. Its solver receives original arc flows and
physical mass/quality rows, without cone or gate equations supplied
directly. The reported sixteen small global solves are numerical support,
not asymptotic or exact arithmetic certificates. I did not duplicate
those solves; this audit checks the full reduction independently.

The result gives the proposed degree-two versus degree-three feasibility
boundary for a fixed exception count. It does not prove hardness with all
flow lower bounds zero, and does not establish general pooling priority.
The source audit must distinguish this precise contracted class from
previous one-pool hardness claims.
