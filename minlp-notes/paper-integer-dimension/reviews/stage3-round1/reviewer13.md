# Stage 3, round 1 — reviewer 13

Major findings: 0
Minor findings: 0

I found no concrete defect requiring correction in the frozen stage. The rational MILP encoding lower bound and the four-binary MISOCP construction survive independent reconstruction, including the unbounded-integer-witness and zero-weight cases. This is a bounded review, not a guarantee of correctness or publication priority.

## Scope and method

I read the entire 1,564-line `sections/03-scalar-nonlinear.tex`, the stage task and lenses, process and review protocol, snapshot, bibliography, and coverage inventory. I checked the accepted foundations and finite-quadratic dependencies relevant to graph containment, arbitrary convex integer lifts, binary linear lifts, parity packing, covariance/determinant volume bounds, unconditional bodies, and the rational scalar allocation oracle. I did not treat stage 4, which remains unwritten, as part of this stage's proof obligation.

For coverage, I compared the eleven canonical stage-3 result statements and their distinct bounds/constructions with the manuscript. I checked that the supporting developments have substantive counterparts: scalar two-bit comparison; the raw-curvature and coefficient-allocation obstructions; signed and positive curvature integration; generic indexed compilation; feature-curve geometry; rational allocation repair; Stieltjes approximation; the general signed rational endpoint gadget; relative-error boundaries; and the rational root-graph encoding barrier. I found no omitted stage-3 development in that comparison. This was not a new exhaustive search through every repository audit or a complete rereading of every original canonical proof.

The deepest source comparison was against `results/small-exponent-milp-soc-encoding-separation.md`, `notes/small-exponent-rational-formulation-barrier.md`, the first and second conic separation reviews, and the conic separation novelty note. I also read `notes/shared-prefix-rational-interpolation-gadget.md`. Existing audits were leads; the mathematical conclusions below come from reconstruction of the manuscript arguments. I inspected primary cached evidence for Sagraloff–Mehlhorn Theorem 36, Simchowitz et al. Lemma 2.1, and Bonito–Pasciak equation (37)/Lemma 3.4. In particular, I did not use the latter's different quadrature theorem as a substitute for proving the manuscript's Stieltjes construction. I did not independently audit all historical priority or bibliography metadata, and did not conduct a new literature search.

## Detailed assessment of lens 13

1. **MILP lower bound, lines 1400–1444.** Freezing an arbitrary integer witness only enlarges right-hand-side numerators after the original rational rows are cleared. It does not enlarge continuous coefficient denominators. The LP with `w >= 1/4` has finite attained minimum `0 < v <= 2^{-D}`. Splitting free variables and adding slacks permits an optimal standard-form basis even when the original polyhedron has no vertex. If the input variable is a difference of two nonnegative coordinates, its optimum still has a denominator dividing the same basis determinant. The row-wise bound on the sum of coefficient bit lengths and nonzero counts gives `log_2 |det B| = O(s)`, rather than a bound involving the integer witness. Thus the linear lower bound in numerical `D` is justified.

2. **Four-binary rational upper bound, lines 1446–1464.** With knots `(j/16)^D`, concavity and monotonicity place the root graph between the interpolated height and that height plus `1/16`. The graph point at every input is retained, while the entire admitted vertical interval stays within the required absolute error. Sixteen continuous selectors constrained by their four matching literals select exactly one segment. The number of rows and variables is constant; rational knot numerators and denominators have `O(D)` bits. This proves the matching encoding order without asserting a short binary-exponent MILP.

3. **Conic value lemma, lines 1479–1502.** Positive weights can be divided out, and primal–dual equality forces the claimed value. At weight zero, pairing a homogeneous primal direction with an original dual feasible point gives `c^T z >= 0`; pairing the homogeneous dual equations with an original primal feasible point gives `b^T u <= 0`. Equality forces both to zero. Zero variables furnish the converse. This rules out a spurious nonzero value from recession directions and does not require bounded optimizer sets.

4. **Explicit squaring-chain dual, lines 1514–1538.** The rotated cone convention is self-dual. Writing `v_i = a^{2^i}` and `lambda_i = 2 v_i lambda_{i+1}`, the proposed slack belongs to the cone since its quadratic inequality holds at equality. Each pairing is `lambda_i (z_i + v_{i-1}^2 - 2 v_{i-1} z_{i-1})`. Intermediate variable coefficients cancel. The identity `lambda_i v_i = 2 lambda_{i+1} v_{i+1}` makes the remaining constant `-v_B`, leaving `z_B - v_B`. This supplies an attained dual certificate directly, including `B=1`. Its potentially long rational coordinates are witnesses and are absent from the formulation data. The stated increasing interpolation from `a` toward one is strictly feasible.

5. **Conic graph assembly and size, lines 1540–1564.** The homogeneous gadgets are applied to the two nonnegative weights in each segment. Inactive selectors have zero weights and therefore zero output contributions by the preceding lemma. Endpoint constants zero and one use direct equations. Constantly many chains give `O(B)` short numerical coefficients and `O(B log(B+2))` ordinary sparse encoding bits. The manuscript explicitly separates MISOCP from `p_bin`, and separates exact feasibility and equality from numerical robustness or exact-output complexity. The claimed comparison therefore does not imply an unsupported algorithmic or linear-lift result.

## Whole-stage reconstruction

I checked the scalar chord/refinement and maximal packing arguments; the local curvature remainder and telescoping mass bounds; the two degree-gap examples; conditional Boolean-wire integrality and exact interpolation products; certified integration, root separation, quadrature conditioning and the quantile inverse modulus; repeated/reversed knot coverage and output-band slack; the large-grid greedy/hybrid split; separable product packing and Jensen superadditivity; positive allocation support and covariance reductions; dyadic layers and sparse rounded powers; scaled power inequalities; Stieltjes tails, panel error and rational normalization; rational endpoint recurrences; integer/rational inverse-power evaluation; and the relative-error residue obstruction.

Specific checks included the compiled mass interval bound `133/320`, its chord bound `81529/102400 < 13/16`, the hybrid total below `1458 * 2^{p_conv}`, and the separable constants derived from scalar capacities 12, 481, and 5832. The finite-existence claims and rational construction claims retain different hypotheses. Dense numerical degree dependence is not silently converted to polynomial dependence on binary exponent length. The denominator hypothesis in the general `P/Q` gadget is supplied as a certificate and is not claimed to be automatically computable for unrestricted input.

## Executed checks and limits

- Recomputed SHA-256 for all seven frozen files; all match the snapshot.
- Ran `python code/small_exponent_soc/check_first_review.py`: `PASS: 105 exact SOCP primal/dual/Slater certificates; 16 selector codes`.
- Checked all 45 stage-3 cross-reference targets and all 13 citation keys: none missing.
- Checked all 239 distinct relative source paths linked by `coverage.md`: none missing.

The finite exact-arithmetic checker corroborates the certificate algebra; it does not prove the theorem for unbounded `B`. The general proof is assessed above. I did not rerun the LaTeX build or claim machine-checked proof verification. No manuscript, bibliography, research, or other review report was edited.

## Findings

None. No repair is requested.

## Frozen manuscript hashes

All paths below are relative to `paper-integer-dimension` and match `reviews/stage3-round1/snapshot.json`.

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |
