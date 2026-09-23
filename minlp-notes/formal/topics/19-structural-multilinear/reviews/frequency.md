# Independent review of the frequency-two proof

Reviewed 2026-09-20 against Q03–Q05 and C03 in [CLAIMS.md](../CLAIMS.md),
[the monomial source](../../../../results/positive-multilinear-frequency-two-gap.md),
and [the cardinality source](../../../../results/convex-cardinality-frequency-two-gap.md).
The reviewer did not author or modify the reviewed proof modules.

## Mathematical result

No mathematical or statement defect was found in the reviewed construction.
The public theorem derives the required finite extreme-point decomposition
and odd-cycle layouts from the actual frequency-at-most-two hypothesis.
Neither an odd-cycle decomposition nor a rounding inequality is assumed as
an undisclosed premise. The proof follows the more general cardinality
argument, which also preserves the baseline required for monomial gaps.

The principal declaration chain is:

| Obligation | Declarations |
|---|---|
| Tight-row rank and incidence counting | `FrequencySlab.exists_symmetric_perturbation`, `extreme_kernel_eq_zero`, `fractional_card_le_active_card`, `two_le_active_fractional_card`, `extreme_fractional_degree_two` |
| Half-integral extreme points | `extreme_active_fractional_sum_one`, `extreme_half_integral`, `extreme_fractional_eq_half`, `active_of_fractional_incident` |
| Compact slab and finite decomposition | `slab_compact`, `slab_convex`, `extremePoints_finite`, `convexHull_extremePoints_eq`, `exists_extreme_law` |
| Actual fractional components | `extreme_no_parallel_fractional`, `fractionalGraph_neighbors`, `fractionalGraph_isCycles`, `fractionalGraph_component_cycle` |
| Odd cycles and complete indexing | `extreme_indexed_cycle_odd`, `indexedFractionalCycle_of_walk`, `exists_indexed_cycle_family`, `exists_frequencyCycleLayout` |
| Explicit rounding | `StructuralFrequencyCycle.roundingLaw_mean`, `roundingLaw_coverage`, `roundingLaw_incidentCount`; `Law.pi` and `expect_pi_coordinate` |
| Original-coordinate assembly and curvature | `FrequencyCycleLayout.law_hasMeans`, `countOn_row`, `law_cardinality_row`, `hullGap_row`, `law_cardinality_loss` |
| Correct averaging | `cardinalityLower_average`, `upperEnvelope_average_le`, `cardinalityGaps_average_le`, `cardinality_gap_of_slab_rounding` |
| Discharge of structural premises | `exists_frequency_slab_layouts`, `frequencyTwo_cardinality_three_halves`, `frequencyTwo_cardinality_oddGirth`, `frequencyTwo_cardinality_bipartite` |

## Extreme-point structure

A tight lower and upper constraint on the same row is counted once.
`exists_symmetric_perturbation` uses finite intersections of neighborhoods
to keep all nontight constraints feasible, while directions on integral
coordinates and tight rows vanish. Thus a nonzero kernel direction
contradicts extremality without assuming a full-dimensional polytope or
strictly separated row bounds.

The active fractional-column matrix is proved injective. Its dimension
inequality gives `|fractional edges| ≤ |active rows|`. Every active row
contains at least two fractional edges, since one strictly fractional
coordinate cannot sum to an integer after removing binary coordinates.
Double counting, together with the at-most-two occurrence hypothesis,
forces equality throughout. Consequently every active row has exactly two
fractional coordinates, and every fractional coordinate has exactly two
active endpoints. `active_of_fractional_incident` also proves there is no
extra slack endpoint overlooked by the restricted matrix.

This handles private and unused coordinates directly, without adding dummy
rows: a coordinate occurring zero or one times cannot be fractional at an
extreme point. The separately defined dual graph may add private dummy
endpoints for interpretation, but the analytic theorem does not depend on
adding their constraints. Parallel input coordinates retain distinct labels;
a difference of two identical active columns is a forbidden kernel
direction. Only after proving that fact does the proof use a simple graph
for fractional components. Two parallel fractional edges are therefore
excluded rather than silently collapsed.

At each active row the two fractional values sum to one. Applying kernel
injectivity to the direction `x_e - 1/2` on fractional coordinates proves
half integrality directly. The odd-cycle argument is still supplied
separately: a finite degree-two component is given an actual simple cycle
by Mathlib's `IsCycles` component theorem, and an even indexed cycle would
have a nonzero alternating-sign kernel direction. The proof checks every
row, including rows outside the indexed cycle.

`exists_indexed_cycle_family` chooses one cycle per connected component,
proves row disjointness from disjoint components, and proves that every
fractional coordinate appears. It does not merely select some cycles.
`frequencyCycleLayout_of_indexed_cycles` then derives global edge
injectivity, the exact two incident fractional edges at each cycle row,
and integrality of all coordinates and rows outside the cycles.

Compactness and convexity apply to the whole integer slab, including
empty and lower-dimensional cases. Half integrality gives finitely many
extreme points; their convex hull is closed, so the compact-convex
extreme-point theorem gives a finite convex hull rather than only its
closure. `exists_extreme_law` converts membership into a genuine finite
probability law with exactly the required barycenter.

## Rounding and original-factor semantics

For each odd cycle of length `L=2k+3`, the code constructs the alternating
matching indexed by its omitted vertex, then chooses that matching or its
complement with equal probability. Adjacent-edge identities prove one
missed vertex for the matching, no missed vertices for the complement,
edge mean `1/2`, and coverage `1-1/(2L)`.

The stronger incident-count identity is exact for any count table: after
adding `m` selected integral coordinates, the count is `m+1` except at the
uniform exceptional vertex, where it is `m` or `m+2` with equal
probability. Independent component laws are assembled by a proved finite
product and pushed to the original coordinate type. Globally injective
edge labels make that pushforward unambiguous. Integral coordinates remain
fixed, including unused coordinates, and `law_hasMeans` proves every
prescribed mean.

`countOn_row` retains the full integral contribution; it does not ignore
other selected edges incident to a cycle row. Using the exact cardinality
lower and upper envelopes gives local gap
`[φ(m)+φ(m+2)]/2 - φ(m+1)` and rounding loss exactly that gap divided by
`L`. Rows outside cycles retain their count exactly. Convexity is required
only on attainable counts, and tables may be negative or decreasing.
Nonnegative weights can be absorbed into the count tables.

The decomposition used by the integrated theorem has bounds
`floor(mean count)` and `floor(mean count)+1`. At an integer mean this is
slightly wider than the source's floor/ceiling slab. It is sufficient:
consecutive-integer interpolation is affine on that entire closed slab,
including the upper endpoint, so its expected value is exactly preserved.
No step substitutes a Jensen inequality with the wrong direction.
Concavity of each upper graph envelope supplies the complementary upper
averaging inequality. Combining the two yields the correct inequality
for the expected local gap, and a finite mixture of the constructed laws
has the original means.

This route preserves the monomial baseline through exact envelope
arithmetic. Independently, `StructuralFrequency` explicitly proves the
coverage identity `gap = cap - baseline`, that baseline is the largest
failure marginal, and `failureBaseline_le_expect`.
`FrequencySlab.expect_cap` proves exact cap averaging on the source's
floor/ceiling slab. Thus no unshifted coverage approximation is used to
stand in for the baseline-subtracted gap.

## Girth, bipartite equality, and boundaries

`FrequencyOddGirthAtLeast` quantifies over actual simple odd cycles with
injective row and coordinate labels and original incidence membership.
It preserves parallel-edge semantics. Each extracted fractional layout
provides precisely those data, so its length bound is derived from the
input girth predicate. The girth parameter may be any integer lower bound
greater than one; it need not itself be an attained odd-cycle length.

`FrequencyBipartite` colors adjacent distinct factor rows oppositely. It
is bipartiteness of the dual row graph, not of the always-bipartite
variable-factor incidence graph. Private dummy vertices cannot lie in
cycles and their colors can be chosen opposite their sole neighbor.
The bipartite hypothesis excludes every fractional odd-cycle component;
the resulting decomposition is integral. The public `frequencyTwo_cardinality_bipartite` theorem combines
`sum local gaps ≤ full gap` with the independent `hullGap_factorSum_le`
to give exact equality, including zero-gap points.

Empty row or coordinate types, empty scopes, constants, singleton factors,
boundary means, no fractional components, parallel integral edges, and
zero curvature are admitted. An empty product of component laws is the
one-state deterministic product, not an empty probability law. No gap
ratio is formed in the public inequality and no positivity of the hull
gap is assumed. Sharpness witnesses, box transfer, and algorithmic
complexity are outside this bounded review.

## Targeted verification

The following independent targeted checks passed from `formal/`:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake --wfail build Formal.MultilinearGap.StructuralFrequencyTheorem
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-frequency-review.lean
```

It printed axioms for 22 declarations covering active-row injectivity,
incidence degree counts, half integrality, extreme-point decomposition,
actual component cycles, exclusion of even cycles, complete cycle layouts,
rounding marginals and coverage, product marginals, original-coordinate
means, curvature gaps and losses, exact lower averaging, upper-envelope
averaging, and all public cardinality gap theorems. Each listed only
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.
A generic Lean example also checked exact bipartite equality directly by
combining the public upper direction with `hullGap_factorSum_le`.

The warning-failing build passed (8739 dependency jobs) after the author's
ancestor-warning cleanup. The final axiom/example audit was rerun against
that stable build. No project-wide check or CI inspection was performed,
and this reviewer changed no proof file.

Reviewed SHA-256 values:

```text
d8f6fd24610580f954e5d5a68b2ff0d0a38d1bf814ca579745a04ea17e5e9fdf  StructuralFrequencySlab.lean
c7f5a535b8ab431182f4775a8958f584a0c59678d73c76397979a512b9477fa5  StructuralFrequencyComponents.lean
7023f9600701c327155002b9112b48e1e9ee05e04251f717c61dc8c18140460a  StructuralFrequencyOddCycle.lean
e3932de1122fdea25e531dbab6ab03116aa061b74652e3e125bc59c0758444c8  StructuralFrequencyLayout.lean
006c71081776904e34dd9ad886739606efae201d2ce26b2acbade59e677da5f9  StructuralFrequencyLayoutAssembly.lean
f8b036afbeb78e7113b40612e8eb279ff359a5ff13940210076924ab928098d1  StructuralFrequencyCycle.lean
31c9d9680673d24b5c5e181cc1758ac3011158aeaee984955258ee67f15b25a0  StructuralFrequencyLocal.lean
22d992a7ffa5cb2d0d6ee849e6c636a294ed9102c7102a9374291bbbaf5ca10e  StructuralFrequencyRounding.lean
c11a801c98972b2e62e8f8be961b05794c591f9682df38b23b374b5edf4443a3  StructuralFrequencyProduct.lean
fd0a5972dc79c93d7e1ed1c8906381974112cc54c146a3c3614a1de6c032580c  StructuralFrequencyTheorem.lean
```
