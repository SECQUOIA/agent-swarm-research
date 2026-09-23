# Flat-chain network–simplex threshold

Status: complete. All 60 mathematical obligations are covered. The original
2026-09-19 delivery had 144 modules and an axiom audit of 4,197 declarations.
The package now has 145 modules: `ThreeCircuitForms` adds the named
seven/five/three/one classification for FC38. Historical delivery checks and
checks of this addition are recorded separately in [VERIFICATION.md](VERIFICATION.md).
The new module passed its warning-free build and kernel replay; the extended
axiom audit passed for 4,261 declarations in 145 modules.
Independent source review found no remaining mathematical issue in the addition.

This package verifies the mathematical claims in
[Section 7 of the manuscript](../../../paper-network-simplex/sections/07-fixed-state-chains.tex),
including the fixed-state determinant bound, exact circuit counts, the sharp
three-label unit-coefficient result, four-label obstruction, rational separation
and recovery, and observed-label reduction. The
[claim inventory](CLAIMS.md) identifies the specific supporting results from
Sections 1, 4, and 6. It does not include the rest of the manuscript.

Start here:

- [Coverage](COVERAGE.md): all 60 mathematical obligations and their Lean declarations.
- [Algorithms](ALGORITHMS.md): executable interfaces, output representations, and cost models.
- [Review](REVIEW.md): independent findings and their resolutions.
- [Verification](VERIFICATION.md): targeted commands, logs, axiom audit, and source fingerprints.
- [Proof module list](verification/modules.txt): all topic-owned modules in `Formal/NetworkSimplex`.

The earlier [fixed-state note](../../../results/network-simplex-flat-chain-fixed-states.md)
is context. The manuscript's residual-eliminated description is sharper; the
unreduced and reduced circuit libraries are verified separately.

The principal results are organized as follows:

| Development | Main modules |
|---|---|
| General finite hull description and determinant coefficient bound | `ThresholdBoundedDescription`, `ThresholdGeneralSourceDescription`, `ThresholdHadamard` |
| Exact reduced and unreduced circuit classification | `ThresholdSmallClassification`, `ThresholdClassification`, `ThresholdUnreducedResults` |
| Finite unit descriptions for zero through three labels | `ThresholdSmallDescription`, `ThresholdUnitDescription`, `ThresholdAmbientDescription` |
| Actual four-label obstruction and unbounded coefficient ratios | `ThresholdOriginalObstruction`, `ThresholdUnusedObstruction`, `ThresholdStarObstruction` |
| Complete membership and separating-cut interfaces | `ThresholdResults`, `ThresholdSeparation`, `ThresholdUnitOracle` |
| Graph witnesses, positive-state output, and bit bounds | `ThresholdWitness`, `ThresholdPositiveAtoms`, `ThresholdPipelineSize` |
| Exact state merging and observed-label compression | `ThresholdConvexMerge`, `ThresholdObservedFiniteDescription`, `ThresholdObservedSeparation`, `ThresholdObservedRecovery` |

The description bounds concern flow and observed-product coefficients; simplex
coefficients are unrestricted. The affine expressions retain both gadget arc
coordinates. The main interfaces evaluate on the original balance equations;
`ThresholdAmbientDescription` makes the substitution explicit, and the balance
equations themselves have unit coefficients. The manuscript assumes at least
one gadget. Some algebraic interfaces also support zero gadgets; this is not a
claim about a distinct-source-and-sink graph with no gadgets.

Complexity results use stated rational-arithmetic and indexed-operation models.
They include actual intermediate bit bounds, but do not verify Lean's compiled
rational backend or repository Python implementations. Historical experiments,
literature attribution, and novelty are outside the mathematical audit.

Local checks are targeted to this package. CI handles project-wide verification;
it is neither run locally nor inspected.
