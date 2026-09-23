# Stage 3 round 1 — reviewer06

Major findings: 0

Minor findings: 0

I found no concrete mathematical, encoding, or attribution defect requiring a correction in the frozen stage. This verdict follows a full-stage proof reconstruction, with additional scrutiny of the indexed compiler and rational encoding. It is a bounded review, not formal verification or a publication-priority determination.

## Coverage and snapshot

I read all 1,564 lines of `sections/03-scalar-nonlinear.tex`, the task, lenses and review protocol, `PROCESS.md`, the coverage inventory, the bibliography, macros and main file. I revisited the accepted stage-1 representation model, parity-contact lemma, finite disjunction and binary-product constructions, and covariance-volume inequality; and the accepted stage-2 rational logdet allocation proof, including its interior ball, weak separator and exact rational repair. I had independently reviewed the full accepted dependencies in the preceding stage rounds; this review concentrates on their actual stage-3 uses.

I compared all eleven canonical stage-3 results with their manuscript statements and proofs. I also inspected the substantive supporting developments: the scalar two-bit lemma; positive and signed monotone-curvature integration; indexed rational knots; raw-curvature and allocation-gap obstructions; feature-curve geometry; Stieltjes approximation; the finite pure-power theorem; rational log-product allocation; relative-error obstructions; the root-power encoding barrier; and the signed rational endpoint interpolation gadget. Earlier source-note verdicts were not used as proof. Later-stage vector results remain outside this review and were not treated as missing stage-3 material.

All seven source hashes were computed against `snapshot.json` and matched, including a second check before writing this report:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |

## Reconstruction of the compiler and encoding arguments

At lines 192–221, fixing the external index bits makes every acyclic AND/NOT gate uniquely Boolean by induction. The interpolation hull then forces each product to equal the same continuous parameter times its output bit. Fixed-denominator decoding is linear, including signed coordinates after a fixed offset. The common denominator must cover the indexed family, as stated and used in the proof; polynomial output precision alone would not justify decoding arbitrary index-dependent denominators. The manuscript supplies the needed fixed denominators in its applications. A comparison circuit excludes unused codes, and fixed-time flags preserve uniform circuit generation. Zero-bit input has one constant cell and causes no additional integrality obligation. The assertion concerns integer-feasible points and makes no unwarranted ideal-relaxation claim.

For the curvature and hybrid applications, I checked that the integral procedures have polynomial worst-case bit bounds before invoking the circuit lemma. The hybrid chooses a piece by comparing one global index with cumulative counts, so it encodes the sum of cell counts. Rational affine maps of local dyadic knots fit the stated common denominator: a product over only polynomially many piece-endpoint denominators, multiplied by one sufficiently fine power of two. Dense evaluation and downward rounding of signed endpoint values also have polynomial bit length. Shared endpoint computations are deterministic. Reversed or duplicate knots retain graph coverage because each local polygonal path joins the required endpoints; no monotonicity of the computed knot list is silently required.

For the sparse implementation at lines 892–939, the invariant for rounded exponentiation is an error at most `(k-1) 2^{-P}`. Although this bound depends on the numerical exponent, the necessary precision depends on its logarithm. Exact dyadic input endpoints use `J_i+L_i+1` fractional bits; every listed monomial uses one common interpolation parameter for its coordinate. No unlisted powers need be enumerated. The resulting band has coordinate error at most `(Cp)_j/2` and uses precisely the layer and cell bits already counted.

For lines 1152–1328, I checked both distinct endpoint mechanisms. The signed `P/Q` recurrence forces `v_k=t^k v_0`, then `Q(t)v_0=theta`; the supplied positive denominator certificate makes the bounded-variable formulation exact. It handles constant polynomials, zero depth, signed coefficients and zero interpolation weight. The integer inverse algorithm safely terminates on an uncertain comparison using its explicit derivative lower bound. The rational-exponent algorithm evaluates rational log and exponential series to fixed precision. Its final exact exponentiation has exponent `M=O(L)`, so numerator and denominator lengths remain polynomial. Endpoint normalization and dyadic padding are explicit. The factor `min(1,alpha-1)` is included both in the geometry and the inverse accuracy for exponents between one and two.

## Reconstruction beyond the primary lens

The scalar geometry at lines 1–181 correctly separates finite real-coefficient existence from construction. I checked the three-interval refinement of a concave chord gap, closed parity spans, trimming of interval covers, existence of finite maximal incompatible sets, and the constants in both degree-gap examples. For the truncated curvature mass I reconstructed the local remainder bound `E <= m^2+3m/2`, the two cases in the potential inequality, and the telescoping bound `M <= 24N`. Their tolerance scaling gives the claimed comparison with unrestricted integer lifts.

The certified integration proof at lines 223–390 supplies the analytic and bit-complexity details needed by the compiler. Positive coefficients give the stated complex sector. With signed coefficients, the exact Taylor test and failed-center/root-distance argument give polynomially many active panels per depth; the square-free discriminant estimate bounds the depth polynomially. Intersections preserve the certified disk. Gaussian positivity and exactness, the explicit weight bounds, and rational value enclosures control both analytic and numerical error. The input-accurate inverse modulus and the later mass-accurate stopping rule serve different purposes and are correctly distinguished.

For lines 392–548, the mass certificate bounds every consecutive interval, regardless of orientation. The error budget is below the prescribed tolerance. In the hybrid, rounding an optimal fine partition down to the rational grid preserves a feasible partition after removing duplicates. Maximal feasible extensions minimize the grid count. Failure after `9D` cells implies `N_eta>D`, which absorbs the cost of the curvature split and gives the stated global count.

For lines 559–1040, I checked Jensen superadditivity by tent kernels and its extension to continuous convex functions. Product packing and the lattice deletion bound `6^r` give the separable count constants; the compiled capacities `481P` and `5832P` yield the stated overheads. The supporting scalarization uses a strictly feasible allocation and a valid nonnegative normal. Coordinates with zero scalarized coefficient have their allocation cap active. The transformed supports cover the transformed cube; no volume preservation under a nonlinear coordinate map is assumed. Expected Jensen domination and Hadamard's inequality justify the allocation lower bounds. Dyadic layer selectors are forced to unit vectors, and their exact products and prefix recurrences add no integer variables. The pure-power chord and scaled Jensen estimates cover their endpoint and exponent ranges.

For lines 1058–1150, I checked both Stieltjes tails, the uniform complex panel bound, positive quadrature, relative rationalization, coefficient magnitude bounds, and exact normalization. The dependence on numerical `D` is retained in the theorem. This construction is distinct from the later compiler with binary exponent complexity.

For lines 1337–1564, the residue argument uses a suitable integer modulus, so it applies to unrestricted integer witnesses and nonclosed convex lifts. The concave threshold and truncated-domain order have the correct tolerance scope. The rational MILP lower bound survives arbitrarily large integer witnesses: freezing them changes the integral right-hand side after row denominator clearing, while the basis determinant is controlled by the original row encoding. The four-bit upper construction matches the order. I separately checked the conic-value gadget at zero weight and the telescoping repeated-squaring dual certificate. Exponentially long witnesses are not confused with coefficients written in the short MISOCP.

## Primary-source checks

I directly inspected Avis–Bremner–Tiwary–Watanabe, Section 3 and Lemma 1, in the local primary text. It proves the required forced-wire property and explicitly credits Valiant. Adams–Henry, cached primary text Section 2, supplies finite-function values and products with a bounded continuous weight using the index binaries; its general enumeration size is not confused with the compact computable-family claim here.

I also inspected Sagraloff–Mehlhorn Theorem 36 and its integer-polynomial complexity bound, Simchowitz et al. Lemma 2.1, and Bonito–Pasciak equation (37) and Lemma 3.4 in the primary cached texts. Their uses are consistent with the manuscript's square-free preprocessing, chord/midpoint comparison, and positive-resolvent attribution. The manuscript proves its own quadrature conditioning, rationalization and endpoint normalization. This was a bounded attribution check, not an exhaustive literature or bibliographic audit.

## Executed checks and limits

All checks below passed:

- `code/quadratic_rank/check_compiled_knots_second.py`: 65 exact integer root enclosures, 75 exact rounded-power bounds, 8 large-exponent comparisons at 300-digit precision, and 40 rational-exponent comparisons at 300-digit precision.
- `code/quadratic_rank/check_sparse_positive_polynomial_circuits.py`: 56 exact rounded-power enclosures and 12 numerical endpoint/band cases at 120-digit precision, through exponent `2^120+11`.
- `paper-integer-dimension/verification/check_general_rational_interpolation.py`: 465 exact signed rational interpolation cases, including depths 0–4; 333 computed values illustrate the need to retain original input bounds in the general gadget.
- `paper-integer-dimension/verification/check_manuscript.py --snapshot reviews/stage3-round1/snapshot.json`: 198 labels, 32 bibliography entries, no duplicate or unresolved keys, and no snapshot mismatch.

These tests supplement the written proofs. They do not implement or certify the complete Boolean compiler, the full certified quadrature/oracle construction, or universal approximation guarantees. I did not perform a new complete LaTeX build or inspect every rendered page. I made no manuscript, research, bibliography or other reviewer edits and spawned no subagents.

## Findings

No MAJOR, MINOR or QUESTION finding is asserted.
