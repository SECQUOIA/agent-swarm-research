The source claims are in the cubic section and finite certificate appendix of
`paper-relaxation-limits`. This package targets exact finite witnesses and their
supporting scalar certificates, not the entire paper.

The later [focused cubic completion](../11-cubic-completion/COVERAGE.md)
proves the universal 31/12 bound on nonnegative boxes, fixed-mixture
optimality, and the analytic family's refined supremum lower bound
1610000/743033. The exclusions below retain this earlier package's scope.

| Claim | Formal proof |
|---|---|
| Binary laws describe the full graph hull of a multilinear function on the cube | `Laws.lean`, `Hull.lean`: finite convex combinations and coordinate-by-coordinate interpolation |
| Elementary symmetric polynomial values depend only on success counts | `Counts.lean`: exact `choose(count, degree)` identity for all degrees |
| Count laws realize all individual marginals | `CountLaws.lean`: explicit uniform cyclic rotations; converse expected-count identity |
| Actual two- and three-group polynomials | `Polynomial.lean`, `Families.lean`: squarefree monomials, separate affineness, binary count identities |
| Polynomial expansion and coefficient scaling | `OrbitExpansion.lean`: actual families equal the support sums used in the termwise gaps; exact envelopes respect nonnegative scaling |
| All seven finite minorants and attaining count laws | `Finite.lean`, `LargeFinite.lean`, `LargeBridge.lean`: exact integer/rational checks |
| Exact convex envelopes for m=4,8,12,16 in the two-group family | `TwoResults.lean`: IsLeast of the actual cube graph-hull slice |
| Exact convex envelopes for m=6,8,64 in the three-group family | `ThreeResults.lean`: same full graph-hull statement |
| Exact concave envelopes | `CountUpper.lean`, `Threshold.lean`, `Maxima.lean`: universal bounds and attaining common-threshold laws |
| Exact hull gaps in the seven examples | `Results.lean`: sSup minus sInf of the actual graph-hull slice |
| Exact individual monomial lower envelopes used in these examples | `Termwise.lean`: explicit attaining laws on the ambient cube, with irrelevant coordinate means preserved |
| Exact monomial upper envelopes | `TermwiseUpper.lean`: minimum singleton mean, with ambient-cube attainment |
| Exact termwise gaps and all seven ratios | `TermwiseFamilies.lean`, `TermwiseFamilyUpper.lean`, `Ratios.lean`: sums of actual individual monomial envelope values |
| Explicit homogeneous unit-coefficient example | `HomogeneousSupports.lean`, `HomogeneousTermwise.lean`, `Homogeneous.lean`: 52 coordinates, 4320 distinct cubic supports, strictly interior means, exact termwise gap 2160 and actual T/H ≥ 2700/1343 > 2 |
| Two-level scalar minorant and attaining atoms | `Scalar.lean`: real polynomial identity, universal expectation bound 16/27, and attaining two-atom data |
| Stronger three-variable scalar minorant | `Bernstein.lean`: all five exact Bernstein rows, both completed-square bounds, and positive slack 901/120000 |

The large finite certificate enumerates 65³ count triples, covering all binary
vertices of the 192-variable polynomial through the proved count identity.
No solver output is used as a proof. The attaining laws establish that the
minorants are sharp in expectation; checking only a table of inequalities would
not establish that fact.

Not formalized by this package:

- The global cubic upper bound 31/12 and optimality of the three-law mixture.
- The strongest limiting lower bound on R3, including its limiting argument and the analytic family's finite-size estimates.
- The full two-level family ratio bounds for every m, its limiting ratio, or the threshold classification among all multiples of four.
- The 25-variable homogenization, randomized coefficient removal, and 25,000-variable existence example.
- The equal-mean theorems, degree-general results, and transfer to arbitrary nonnegative boxes.
- Any claim that R3 is determined exactly or that one of these dimensions is minimal.

The scalar inequalities supporting some excluded analytic results are proved
separately; that does not by itself formalize the complete analytic results.

The unbounded-ratio disproof for general-degree positive multilinear functions
is now formalized in the separate
[multilinear disproof package](../07-multilinear-disproof/README.md).
The exclusions above describe this cubic package; the sharp general-degree
upper bounds and asymptotics remain outside both packages.
