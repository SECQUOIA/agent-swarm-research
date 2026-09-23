# Many-leaf reciprocal-anchor hull

Status: complete. All 46 mathematical obligations are covered, with independent
reviews and passing targeted checks for 67 Lean modules. The declaration audit
passed for 1,936 declarations. See the [coverage map](COVERAGE.md),
[review record](REVIEW.md), and [verification evidence](VERIFICATION.md).

The source is the [full-hull result note](../../../results/common-factor-reciprocal-anchor-full-hull.md).
This package extends the existing [one-leaf hull](../05-reciprocal-anchor/README.md)
to arbitrarily many leaves sharing the same reciprocal anchor.

The central result is `ReciprocalAnchor.ManyLeaf.mem_hull_iff_bounds` in
[ManyResults.lean](../../Formal/ReciprocalAnchor/ManyResults.lean). It characterizes
the convex hull of the original graph, proves existence of the minimum law,
and constructs a hull witness with at most `2n+3` atoms. The zero-leaf case
retains explicit bounds on the common-factor mean.

The [claim inventory](CLAIMS.md) lists the full mathematical scope. The
[review record](REVIEW.md) links the independent reviews of the core theorem,
general probability laws, algorithms, oracle, and complete rational witness.
All review findings are resolved.

## Proof layout

All new Lean modules are in [Formal/ReciprocalAnchor](../../Formal/ReciprocalAnchor),
with names beginning `Many`. The existing one-leaf modules are reused.

| Part | Entry modules | Content |
|---|---|---|
| Graph and finite laws | `ManyModel`, `ManyLaws`, `ManyResults` | Actual graph hull, affine conditions, endpoint law, mixing, and final equivalence |
| Envelope construction | `ManyGeometry`, `ManyEnvelopeBound` | Convexity, exterior pieces, constructed slope-jump law, and sharp support count |
| Leaf realization | `ManyThreshold`, `ManySelection` | Attaining fractional tail selectors and simultaneous leaves |
| Integrals | `ManyIntegrals` | General second-derivative identity, reciprocal identity, and exact segment integrals |
| Arbitrary probability laws | `ManyProbability`, `ManyQuantile`, `ManyProbabilitySelection`, `ManyProbabilityIntegral`, `ManyProbabilityEndpoints` | Supported measures, actual quantiles, Fubini justification, and endpoint domination |
| Changes of coordinates | `ManyNormalization` | Positive anchor, arbitrary leaf boxes, fixed leaves, and fixed common factor |
| Special cases | `ManyOneLeaf`, `ManyExamples`, `ManyRationalExample` | One-leaf SOC hull and the exact two-leaf gap `1/50` |
| Rational algorithms | `ManyFastConstruction`, `ManyFastSegments`, `ManyFastEvaluation`, `ManyMembership`, `ManyOracle` | Executable slope sorting, stack envelope, clipping, integration, and Boolean hull membership |
| Rational cuts | `ManySeparation`, `ManyFastSeparation`, `ManyLinearSeparation` | Rational affine coefficients, global validity, and completeness even at real candidates |
| Rational witnesses | `ManyFastLaw`, `ManyRationalCandidate`, `ManyRationalSelector`, `ManyFastWitness` | Rational knots, masses, selections, mixtures, and size bounds |

The arithmetic and bit-work bounds are in `ManyBitCost`,
`ManyEvaluatorBitCost`, `ManyOracleBitCost`, and `ManyWitnessBitCost`, with separate proofs of operand
and coefficient sizes.

The finite envelope construction has dedicated modules for slope jumps,
reconstruction, positive-mass counting, and compression. The fast algorithm
has separate sorting, parallel-line elimination, stack geometry, and
rational-size proofs. These helpers are part of the topic's verification.

## Verification boundary

Local work uses targeted module builds and audits. Project-wide verification
belongs to CI; it is neither run locally nor inspected. The canonical Lean
project pins Lean and Mathlib through its existing toolchain and manifest.

The Lean algorithms do not verify the Python script or its numerical solver.
The script's reported LP comparisons, review history, attribution, and novelty
remain separate from the mathematical claims. Complexity statements must
identify their operation model; they do not measure the compiled Lean runtime.
