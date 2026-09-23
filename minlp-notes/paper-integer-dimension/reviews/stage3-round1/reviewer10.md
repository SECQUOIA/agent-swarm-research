# Stage 3 round 1 — reviewer 10

Major findings: 0
Minor findings: 0

I found no concrete defect requiring a change in the frozen stage. This is a bounded independent review, not formal verification, an external peer-review verdict, or a priority determination.

## Coverage and assessment

I read the entire `sections/03-scalar-nonlinear.tex` (lines 1–1564), the stage task, lenses, protocol and process, the coverage inventory, bibliography, main file and macros. I checked the accepted foundations used here: the definitions of convex versus binary linear lifts, parity contacts and finite convex combinations, finite disjunctions, covariance-volume bounds, binary-product identities, and the stage 2 scalar specialization of the rational block logdet oracle with central-ball repair. This is not another review of unrelated stage 1–2 theorems.

I compared all eleven canonical stage 3 results with their manuscript statements and proofs, and checked the substantive supporting developments: the continuous-convex scalar comparison, curvature truncation and its obstruction examples, positive and signed certified integration, feature geometry, log-product allocation, finite pure-power geometry, Stieltjes approximation, general rational endpoint products, compiled inverse knots, relative-error boundaries, and root-power encoding. The contribution mappings are present. The vector developments explicitly assigned to stage 4 remain outside this review; I did not count them as missing.

My independent reconstruction covered the following points.

1. **Scalar geometry and mass (lines 1–181).** Compact parity contacts give span chord bounds at doubled error. The three-part concave-gap refinement and maximal compatibility cover yield the stated factors. The local mass estimate uses the correct global density and the reverse estimate telescopes with a nonpositive final boundary contribution. The raw-arclength example and the finer-tolerance coefficient-allocation gap use different accuracy regimes consistently.
2. **Certification and compilation (lines 183–458).** Integral branch signs, omitted-mass budgets, positive Gaussian weights, Taylor remainder constants and polynomial node/weight precision are consistent. For signed curvature, failed-panel centers lie near root real parts, limiting failures per depth; the square-free discriminant bound limits depth. Small root separation enters through its logarithm. Input-accurate inverses use a positive interior density bound; the final mass-accurate compiler does not need one. Its uncertain comparisons, above-total-mass targets and endpoint forcing retain the displayed mass error. Continuous internal Boolean wires and interpolation products are exact after fixing the external bits. Common denominators and invalid indices are accounted for.
3. **Hybrid and separable bounds (lines 460–643).** Endpoint expansion controls rounded partitions; exact chord predicates support greedy maximal extensions. Failure after 9D cells implies the lower bound needed to absorb monotone-piece boundaries. Global indexing counts the sum of local cell counts. Jensen superadditivity follows from tent kernels, and the lattice deletion bound supplies the scalar-sum packing. I recomputed the capacities 481 and 5832 and their stated integer overheads.
4. **Positive mixtures (lines 645–939).** Nonnegative supporting normals can be chosen after removing zero output rows. The scalarized allocation has the same product optimum; its zero-weight input coordinates are retained with caps. The feature-coordinate volume proof does not assume that the change of coordinates preserves volume. Normalized layer curvature is uniformly bounded, including the final layer. Dense exact power recurrences and sparse rounded evaluation have different, correctly stated encoding guarantees. Their graph bands use the same input and interpolation weights and respect unconditional domination.
5. **Pure powers and inverse algorithms (lines 941–1328; primary lens).** For 1<alpha<2, the scale s=alpha−1 is required in both the Jensen lower bound and the chord upper bound. The proof handles the first cell separately, where curvature is unbounded at zero, and applies the ordinary curvature estimate only away from zero. With delta=sp/(16alpha) and h²≤p/16, the total band error is 4sh²+2alpha delta≤3sp/8. Approximate endpoint order is unnecessary: the deterministic polygonal path joins 0 to 1 and covers the input interval, and every segment satisfies the same error bound.

   For integer D, the rounded exponentiation induction gives error at most (D−1)2^(−P). The uncertain root enclosure is safe because both power values are at least u/2; the derivative lower bound then yields input error at most delta/8. Strict tests preserve the root bracket, and the finite bisection cap with common output padding handles the alternative termination. Required precision is O(log D+L+log(1/delta)), not O(D).

   For rational alpha, normalization has 1≤e≤L at interior indices. Monotonicity of the truncated logarithm gives A≤0, and beta<2 gives A≥−2L. The chosen power-of-two M makes q∈[−1/2,0]. The odd Taylor truncation is positive and below exp(q), so raising it to M controls error by M times the local error. M=O(L) also bounds the growth of exact rational numerator/denominator lengths. Endpoint and L=0 dispatch avoid normalization at zero. A rational exponent approaching one makes log(1/s) large only in proportion to its input bit length. The constants combine to the announced 7r+1 bound, or 13r/2+1 when all exponents are at least two.
6. **Reciprocal and conic boundaries (lines 1058–1229 and 1330–1564).** Stieltjes truncation, positive rationalization and exact normalization retain a uniform closed-interval guarantee, with numerical-degree complexity stated separately from the sparse inverse algorithm. The signed P/Q recurrence needs the supplied positive denominator bound and works with zero bits and zero interpolation weight. Arbitrary-modulus residue arguments prove the convex and concave relative-error obstructions with their distinct tolerance scopes. The truncated-domain order bound and root MILP denominator argument are valid with unbounded integer witnesses. The homogeneous primal-dual value construction forces t=0 at zero weight, and the displayed squaring-chain dual telescopes to the claimed optimum. Long conic witnesses are distinguished from short formulation coefficients and from numerical solution guarantees.

## Sources and limits

I inspected primary-source text for Avis–Bremner–Tiwary–Watanabe, Section 3, Lemma 1 and its proof (local fulltext, pp. 7–8), confirming the conditional Boolean-wire statement and its credit to Valiant; Adams–Henry, Section 2, for the finite logarithmic index formulation; and Sagraloff–Mehlhorn, Theorem 36 and its square-free context, for polynomial root isolation/refinement. The elementary log/exp algorithms and their conditioning are proved in the manuscript itself, rather than imported from a numerical library. Other attribution passages and bibliography entries were checked for consistency with the supplied source inventory and proof scope, not by a fresh exhaustive literature or metadata search. I used existing audits as leads, not as substitutes for these calculations.

No full MILP circuit generator, certified quadrature implementation, or separation/optimization oracle was built in this review. I did not rerun the LaTeX build or inspect every rendered page. The finite arithmetic tests below do not establish universal correctness or practical efficiency. No finding is being withheld as a speculative question.

## Executed checks

- Frozen snapshot: independently computed SHA-256 for all seven files; every hash matched.
- `python code/quadratic_rank/check_compiled_power_knots.py`: PASS — 1,479 exact rounded-power bounds; 60 integer inverses; 48 rational-exponent inverses; 1,158 scaled Jensen/chord cases. The noninteger geometric/reference checks use high-precision arithmetic and remain numerical evidence.
- `python code/quadratic_rank/check_compiled_knots_second.py`: PASS — 65 exact integer-root enclosures; 75 exact rounded-power bounds; 8 high-precision huge-exponent checks; 40 high-precision rational-exponent checks.
- `python paper-integer-dimension/verification/stage3-reviewer10-exact-inverse.py`: PASS — 432 exact rational-exponent enclosures and 216 exact integer-exponent enclosures, including L=0 and all endpoint indices. This new checker validates rational alpha=m/n through exact integer-power inequalities, (max(0,R−delta))^m≤t^(2n)≤(min(1,R+delta))^m, avoiding a floating-point reference. It exercises existing algorithm implementations; the proof reconstruction is independent of those implementations.

## SHA-256 record

Paths below are repository-relative. The first seven entries are the frozen manuscript inputs. Supporting-file hashes identify the versions inspected; source-paper hashes cover the local text files from which the identified passages were read.

| File | SHA-256 |
| --- | --- |
| `paper-integer-dimension/coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `paper-integer-dimension/macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `paper-integer-dimension/main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `paper-integer-dimension/references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `paper-integer-dimension/sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `paper-integer-dimension/sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `paper-integer-dimension/sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |
| `results/accuracy-dependent-curvature-precision.md` | `5028ba992bc3b0fe7ce15a100c96a28d96877886480c13ea4ba1d239e419809f` |
| `results/compiled-curvature-quantile-precision.md` | `302e4ff82d5714ffb3c2bd329050c0f895ca564c8c8871889e195b338456973c` |
| `results/convex-polynomial-compiled-integer-precision.md` | `b60d5641221983eacfeb14a668db8671c62df1f7947dbea6cf0a95ba94ddcc69` |
| `results/positive-polynomial-loglog-degree-precision.md` | `f539f67a03638e968c601e3ac47cd539fb7b273b2d1e2a271962db594d4d9b6e` |
| `results/positive-pure-power-linear-dimension-precision.md` | `5548f495aed87b68428704ea25bf3c56cfc758c22b93d02b2e503dd2b2ffc4fa` |
| `results/positive-separable-polynomial-integer-precision.md` | `c1b5d270a0ebb19ac97d88abeeff506c970e93b1860f9bcb76585b3ec4dc9d3d` |
| `results/positive-separable-unconditional-error-precision.md` | `c02a60f64134f11d16a67858940960e85e1d283fae2a363a6a63e830df16e8c3` |
| `results/rational-power-compiled-integer-precision.md` | `e5b7b1b4feb2f5d95ba3bed9b0036ebb7071e0dd7df898629fd18b11ca023316` |
| `results/separable-convex-graph-linear-dimension-precision.md` | `b6b2404b887ced53ee23c59e82d4361ae886b01c0e2046fc6ca1ef71dc9b61a2` |
| `results/small-exponent-milp-soc-encoding-separation.md` | `8fbddcccd9f75332c86cb4e98a8a9ce81969d6201ad7e6c514dc0ebbf29e94a5` |
| `results/sparse-positive-polynomial-circuit-precision.md` | `107f3873726bdb138b25ff19a7dd62b960a9e8f0ca06d5ac6eaadcaddcd4670e` |
| `paper-integer-dimension/reviews/STAGE3-TASK.md` | `f7685a797c7f1a59dfebd3ecccda4d494975e94f7e922f82469250308e9f2b73` |
| `paper-integer-dimension/reviews/STAGE3-LENSES.md` | `89c1278a7e45bdfe6a73dbe0694768b6dce31067041cb04792968c47e03faf9f` |
| `paper-integer-dimension/reviews/PROTOCOL.md` | `9ca1d0f1c48bf807c7634ccc5c93f541ac374a70b0d2be3875e57e74f6755d57` |
| `paper-integer-dimension/PROCESS.md` | `8c2706ee52911db92215c91e61d1e9445dfd4fc2dfe4de44f9ea49863fd2e1dd` |
| `paper-integer-dimension/verification/stage3-root-source-audit.md` | `0bd444fa310e7e6767ea91d41ad27527d8a4ba3de7f45f8f47cf82fb656da5e0` |
| `notes/compiled-rational-knot-formulations.md` | `61f6a27283204403983f3a82eb6edee0440404939ddf2568db7d6dbd5b7f6e2e` |
| `notes/review-compiled-rational-knots-bit-conditioning.md` | `5a3492921c6e0f71fd867268be83990f28d15811936d3228969c32cef41dac75` |
| `notes/certified-monotone-polynomial-curvature-quantiles.md` | `c3072da7cb0460b76c4bca294e3f36e470836a664c08270dc0d2906056829624` |
| `notes/certified-positive-polynomial-curvature-quantiles.md` | `8cbd3e16aae1ed520d438bbbc2a566ebc470ab4142b9b067ee7bb918140db92e` |
| `notes/positive-rational-stieltjes-power-approximation.md` | `6130d25ad74c5a73c514e781b87fd680cb4876ae7dd0443edd5436bc6da95fdd` |
| `notes/shared-prefix-rational-interpolation-gadget.md` | `004ca5182ad1455d1ac82c41ee58094e06f60d84c2a8689efc3ac5dede0d8af0` |
| `notes/curvature-arclength-precision-obstruction.md` | `5b36600047883df4b8fcf2cd2b3c307ec331db9d5adb04afd3276e764b337683` |
| `notes/positive-polynomial-allocation-degree-gap.md` | `586871f7f726250f5b980b4b8e8e4aa49a8381038680dbbf762508f3cd6f2ee2` |
| `notes/positive-polynomial-feature-curve-geometry.md` | `9b4a82b8af404e3518e17a156e128e7fc9c72d46375a246e007cf76968ae0d99` |
| `notes/scalar-convex-graph-two-bit-gap.md` | `e963f72e1e595e5370f1dd24bd17efdc2dcd6a77315c2324b80b51fd551638ba` |
| `notes/relative-power-graph-integer-obstruction.md` | `a948772bc3fbd827a3795384ec9cb4389a5fa581f9accb26e06338abe2720117` |
| `notes/small-exponent-rational-formulation-barrier.md` | `19954618cdd68849fcbe42aeb0c566bc621ce33188a76c436f5ca8218c5f49a5` |
| `notes/pure-power-degree-independent-integer-count.md` | `a01e65a0dffbcdc9b84146ef44473e8976fed6e1985966f3444dd205e0b1a7a6` |
| `notes/rational-log-product-convex-body-oracle.md` | `e59989616d29650075756416633242168375cf24609294234323b38a3cfd27e4` |
| `literature/AGENTS.md` | `40da10e6e5f7c5dd120f5c789bda7d20aae6b07acdb781aaec4c7b3f5af02916` |
| `literature/papers/avis2019-polynomial-size-linear-programs-for/fulltext.md` | `b213e881e98a46227fcbe7441fdcee54cabc460c2c4f35f3a9945213bc7542c4` |
| `paper-integer-dimension/build/source-cache/adams2012.txt` | `9f4f87926486514f9b1d6c2b85d6c587489709df4a23fcc3ae3fafe7bae6c6ea` |
| `paper-integer-dimension/build/source-cache/sagraloff-mehlhorn2015.txt` | `e2e9155a93d5c9235b517d515cd17f98acd3ba90a03f6c9f07b3a29726931834` |
| `code/quadratic_rank/check_compiled_power_knots.py` | `90ab84986941b17775025e04ab853cca8bb538986e809eada40133d1e5d565c5` |
| `code/quadratic_rank/check_compiled_knots_second.py` | `d9015ba1f5df6273ca05e9d99a1d0b237fe7bfd3953230c0cdc6465dfb65485e` |
| `paper-integer-dimension/verification/stage3-reviewer10-exact-inverse.py` | `c45044dc38caac56546b79b5826df2fdcc788b903c92c7a0682e0773dc6676d4` |
