# Independent review of rational witnesses

The rational witness construction passes semantic and arithmetic-charge
review. The actual executable producer starts from a feasible rational
candidate and emits the masses and every graph coordinate. Its correctness,
support count, output size, and rational-operation charge are proved without
assuming a representing law or leaf selections. The final schoolbook
bit-cost composition also passes review in its explicitly stated mathematical
cost model. No remaining MR39–41 issue was found in that scope.

## Reviewed sources

- [ManyRationalLaw.lean](../../Formal/ReciprocalAnchor/ManyRationalLaw.lean)
- [ManyRationalBound.lean](../../Formal/ReciprocalAnchor/ManyRationalBound.lean)
- [ManyRationalWitness.lean](../../Formal/ReciprocalAnchor/ManyRationalWitness.lean)
- [ManyRationalMix.lean](../../Formal/ReciprocalAnchor/ManyRationalMix.lean)
- [ManyRationalMixCall.lean](../../Formal/ReciprocalAnchor/ManyRationalMixCall.lean)
- [ManyRationalCandidate.lean](../../Formal/ReciprocalAnchor/ManyRationalCandidate.lean)
- [ManyRationalThreshold.lean](../../Formal/ReciprocalAnchor/ManyRationalThreshold.lean)
- [ManyRationalSize.lean](../../Formal/ReciprocalAnchor/ManyRationalSize.lean)
- [ManyRationalSelector.lean](../../Formal/ReciprocalAnchor/ManyRationalSelector.lean)
- [ManyRationalProducer.lean](../../Formal/ReciprocalAnchor/ManyRationalProducer.lean)
- [ManyFastAtoms.lean](../../Formal/ReciprocalAnchor/ManyFastAtoms.lean)
- [ManyFastLaw.lean](../../Formal/ReciprocalAnchor/ManyFastLaw.lean)
- [ManyFastLawSize.lean](../../Formal/ReciprocalAnchor/ManyFastLawSize.lean)
- [ManyFastWitness.lean](../../Formal/ReciprocalAnchor/ManyFastWitness.lean)
- [ManyWitnessLists.lean](../../Formal/ReciprocalAnchor/ManyWitnessLists.lean)
- [ManyWitnessOperandSize.lean](../../Formal/ReciprocalAnchor/ManyWitnessOperandSize.lean)
- [ManyWitnessBitCost.lean](../../Formal/ReciprocalAnchor/ManyWitnessBitCost.lean)
- [ManyBitCost.lean](../../Formal/ReciprocalAnchor/ManyBitCost.lean)
- [ManyEuclidCost.lean](../../Formal/ReciprocalAnchor/ManyEuclidCost.lean)

The review also followed the partition producer, compression, slope-jump
count, and finite selection lemmas used by these files. This is a semantic
source review. Compilation results belong in the topic verification record;
this review did not run project-wide checks or inspect CI. It independently
imported the final witness-cost module and printed the axioms of
`fastWitnessOutput_complete` and `fastWitness_schoolbook_bound`; both use
only `propext`, `Classical.choice`, and `Quot.sound`.

## Mathematical conclusions

| Obligation | Reviewed result | Assessment |
|---|---|---|
| MR39 | `exists_rational_minimal_law`, `rationalMixWeight_bounds`, `rationalMixWeight_identity`, `rationalMix_mean`, and `rationalMix_reciprocal` | The input inequalities produce a rational minimal law. Endpoint interpolation preserves the mean and attains the requested reciprocal coordinate. |
| MR40 | `exists_rational_selection_bounded`, composed in `rational_candidate_witness` | Both tail thresholds are proved to exist over the rational field. Fractional boundary selections and interpolation attain every prescribed rational leaf mass and first moment. |
| MR41: existence | `rational_candidate_witness` and `rational_representation_mem_hull` | The candidate produces all masses, anchor locations, and leaf values with all required moment equations. Casting this witness gives membership in the actual real graph hull. |
| MR41: support | `exists_small_rational_law`, `exists_rational_minimal_law`, and `rationalMix_cardinality` | The compressed minimal law has at most `2*n+1` atoms. The terminal index type is `Fin K ⊕ Fin 2`, hence at most `2*n+3` graph atoms. Zero mixture masses and duplicate locations do not increase this bound. |
| MR41: output size | `rational_candidate_witness` and `candidateBits` | The theorem bounds the actual reduced numerator and denominator of each mass and every graph coordinate, including reciprocals and products, by an explicit polynomial in `n` and the input coordinate bit bound `B`. |

The support proof counts positive slope jumps, rather than all intervals in
an unnecessarily refined partition. Each positive jump has a distinct right
slope, and the initial slope contributes one additional distinct input slope.
This justifies the subtraction of one from the input-line count. Compression
preserves expectations and retains rational atom provenance.

The rational partition is extended to real thresholds by affine domination
at both endpoints of every interval. Thus its call identity is a real
identity, not merely an identity tested on rational thresholds. The terminal
proof then derives each rational leaf inequality from the corresponding
real envelope line and transfers it through the endpoint mixture.

The bit predicate bounds reduced fractions, not arbitrary unreduced
representations. `rationalBits_iff_size` identifies it with the corresponding
binary digit bound. Addition, multiplication, inversion, division, and finite
sums have proved size bounds. The terminal result includes leaf products as
well as leaf values. With at most `2*n+3` atoms and `2*n+3` rational entries
per atom when counting its mass and graph coordinates, these coordinate
bounds also give a polynomial total output length.

## Boundary cases checked

- `a > 0` and `a < b` justify the reciprocal and endpoint denominators.
  These are the nondegenerate source theorem's hypotheses.
- Coincident reciprocal extrema force the requested coordinate to equal
  both extrema; the interpolation weight is zero and its moment identity
  is proved separately.
- A zero threshold-atom mass forces the missing selected mass to be zero.
  Total division therefore does not conceal a failed mass equation.
- Coincident selectable moments use a separate interpolation branch.
- Leaf masses zero and one are admitted by the threshold existence and
  selection lemmas.
- Repeated slopes, redundant lines, and zero slope jumps are handled by
  partition existence and positive-mass compression.
- No nonempty leaf hypothesis is imposed. For zero leaves the explicit
  mean bounds in `LinearBounds` still apply.
- All leaves are selected on the same mixed scalar law. No independence
  premise or expansion into binary leaf patterns is used.

## Review of the executable construction

The later executable modules close two gaps in the initial review.
`buildAtoms` forms actual rational slope jumps of the stack returned by
`buildStack`. `fastLaw_moments_call`, `fastLaw_support`, and
`fastLaw_reciprocal_eq_fastLowerMoment` connect those emitted atoms to the
original envelope and reciprocal minimum. `fastLaw_length` proves the
`2*n+1` bound for that actual list. `buildAtoms_bits` bounds the emitted
masses and locations using retained input-line provenance. The noncomputable
`fastLawAsLaw` only casts these executable rational arrays to the real
specification; it does not choose their entries.

`rationalSelectorCounted_value` connects the counted selector's emitted list
to `rationalSelector`. The success specification proves that this actual
list has the requested mass, moment, coordinate range, and bit bound.
The two thresholds are obtained from `rationalThreshold`, whose finite
search is proved to succeed. The counted version shares the tail sums
through `cachedThresholdSelector` and shares the two moments and
interpolation ratio through `interpolatedSelection`. The stated charge
allows the additional selector evaluations in its list and moment traversals.
The bound `64*(K+1)^2` applies to the successful producer, rather than to
an unrelated hypothetical selector.

`mixedLaw_spec` and `rationalWitnessProducer_spec` establish the mixture
and simultaneous leaf moments. The final `fastWitnessOutput_spec` applies
these results to the actual `fastLaw` produced from the candidate.
`fastWitnessOutput_complete` then connects the emitted lists to the actual
real graph hull and bounds every emitted rational coordinate. Its inputs
are the original candidate coordinates, their size bounds, and the hull
inequalities; it has no supplied-law or supplied-selection premise.

`WitnessOutput` contains materialized mass, anchor-location, and inverse
vectors, together with all leaf and product lists. The inverse equation and
`fastWitnessOutput_products` prove that the output really contains `1/x`
and `x*y`, rather than only values from which those coordinates could in
principle be reconstructed. All optional leaf and product lists are proved
to succeed on feasible input.

## Arithmetic-charge review

The terminal producer executes the fast envelope once and shares its atom
list. It materializes the mixed mass and location vectors before running
leaf selectors. This resolves the initial concern that function lookups
could repeatedly rebuild the envelope or repeat uncharged mixture work.
The quadratic mixture allowance explicitly permits recomputing the base
reciprocal sum for each mass entry. Source-line construction uses six
operations per entry, allowing both occurrences of the line formula to be
evaluated without relying on compiler projection optimizations.

`fastWitnessOutput_polynomial_work` bounds the producer's actual `work`
field by

```text
(2*n+2) * (log2(2*n+2) + 37)
  + (40+64*n) * (2*n+4)^2
  + 3*(n+1)*(2*n+3).
```

This includes the envelope charge, source coefficients, materialized mixed
arrays, the sum of charges returned by the actual leaf selectors, and the
inverse and product output coordinates. The bound is polynomial after
using `log2 N <= N`. List and index manipulation are separate from the
rational-operation model and use polynomially bounded traversals and
indices. This result is not a measured or formally refined runtime bound
for Lean's compiled backend.

The terminal module's author reported a successful targeted warning-free
build after freezing these definitions. The independent review inspected
the final definitions and theorem composition; it found no remaining
semantic or rational-operation accounting defect.

## Final bit-cost composition

`fastWitness_schoolbook_bound` now composes the materialized producer with
an explicit polynomial schoolbook budget. `fastWitness_work_bound` removes
the logarithm from the arithmetic-charge bound. The common operand width
`finalWitnessOperandBits` includes the fast-envelope width, the selector
width at `2*n+3` mixed atoms, the mixed-atom width, and a constant allowance.
All of these widths are explicit polynomials in `n` and the input bound `B`.

The final bound is

```text
witnessOperationBound n * 256 * (finalWitnessOperandBits n B + 1)^3.
```

This is supported by intermediate-size results, not merely by the output
size theorem:

- `fastWitness_base_bits` bounds the actual emitted slope-jump atoms.
- `fastWitness_reciprocal_partial_bits` bounds every reciprocal partial sum.
- `mixingTrace_bits` and `fastWitness_mixing_operand_bits` cover the secant,
  interpolation ratio, endpoint fractions, and mixed masses.
- `fastWitness_mixed_bits` and `fastWitness_materialized_bits` connect the
  mathematical mixed values to the stored arrays used by the selectors.
- `rationalThreshold_candidate_bits` bounds every visited threshold using
  its provenance as zero or a stored location, including comparison inputs.
- The tail, moment-product, moment-partial-sum, threshold-ratio, and
  interpolation-family lemmas in `ManyWitnessOperandSize` cover the
  selector's intermediate arithmetic. Their cardinality bounds transfer
  to the actual mixed arrays through `selector_le_finalWitnessOperandBits`.
- `witness_graph_coordinate_bits` covers emitted reciprocal and product
  coordinates. The corresponding terminal semantic equations identify the
  actual output lists.

The schoolbook model also controls rational normalization before reduction.
`raw_components_size` bounds actual unreduced integer components;
`countedEuclid_gcd` identifies the counted recursion with Euclid's algorithm,
and `countedEuclid_cost_size` proves at most two remainder divisions per
bit of its second operand. The primitive cost theorem combines those
results with the declared schoolbook multiplication and division charges.

The model uses proved arithmetic formula families and the producer's
explicit charge. It is not an operational trace extracted from Lean's
compiler and does not claim refinement of its `Rat` backend, hardware
instructions, or measured runtime. This boundary is explicit in the
source and is compatible with the paper's mathematical algorithm claim.
Individual family lemmas and the terminal composition must be cited
together; the budget inequality in isolation would not establish operand
bounds.

The algorithm owner reported the final targeted
`lake build Formal.ReciprocalAnchor.ManyWitnessBitCost --wfail` as passing.
The independent axiom checks also passed. The earlier findings concerning
existential law construction, selector refinement, repeated lookups,
emitted graph coordinates, and final bit-cost composition are resolved.
MR39, MR40, and MR41 pass this review within the stated mathematical cost
model.
