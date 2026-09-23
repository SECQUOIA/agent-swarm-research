# Stage 2, round 1 — reviewer 10

I read the complete `sections/02-quadratic-finite.tex` (lines 1–1546), the relevant corrected stage-1 dependencies, the stage instructions and protocol, process status, bibliography, and the stage-2 coverage/dependency mappings. My additional focus was PSD blocks, diagonal structure, unconditional error bodies, the direct logdet oracle, commuting Hessians, and determinant certificates.

The stage appears mathematically sound within the verification limits below. I found no false main theorem, material missing hypothesis, or substantive proof gap. In particular, the direct logdet oracle supplies the explicit interior ball and exact repair its polynomial rational guarantee needs. The block and diagonal improvements use the original domain correctly, and the commuting-Hessian argument uses geometric means in a way that remains valid for indefinite Hessians.

Major findings: 0

Minor findings: 1

1. **MINOR — ambiguous and literally false gradient-variation wording.** In `sections/02-quadratic-finite.tex`, lines 1045–1048, the preceding subject is the independent-coordinate gradient of `g`, followed by “Its variation is at most `1/4`.” The proof needs the variation of the objective `g` from the center, not the variation of its gradient. The latter need not be at most `1/4`. For example, take one scalar block, the zero linear map (`c=1`), `rho_0=2`, and the permitted choice `delta=1/2`. Then `P_0=1/4` and `sigma=1/64`. Between `P_0` and `P_0-sigma`, the gradient of `log P` changes by `1/(15/64)-1/(1/4)=4/15>1/4`. The intended objective estimate is valid: integrating the stated gradient bound along the segment gives `|g(P)-g(P_0)| <= (8N/delta) sigma <= 1/4`. Suggested repair: replace the sentence with “Hence `g` differs from its value at the center by at most `1/4`.” This is a local exposition defect and does not invalidate the ball inclusion or the allocation theorem.

Verification and coverage:

- Reconstructed the complete finite covariance lower/upper argument, including the factors 4 and 8, covariance caps, rotated interval widths, graph containment, shared monomial errors, finite count, and volume correction for restricted domains. Checked the graph LP, commuting reduction, one-Hessian allocation, and the covariance-benchmark gap example.
- Checked the determinant certificate through geodesic convexity of its Lagrangian, the relative spectral interval, nonnegative slack, and the exact rational identity `||P^(1/2) R P^(1/2)||_F^2 = tr(PRPR)`. No necessity of KKT conditions is silently used.
- Checked the rational nc-rank construction against the stage-1 principal restriction and symmetric shrinking lemmas, including preservation of zero blocks by nonorthonormal rational bases, exact interval normalization, dyadic depths, the `D_H^(-2r)` capacity scaling, and endpoint-denominator volume lower bound. The stage-1 rational preview now has its promised proof.
- Reconstructed the rational Jacobi contraction and denominator-growth argument, spectral function estimates, exact penalty, normalized gradients, polynomial metric radius, inexact recurrence, branch and rounding budgets, rational feasibility repair, and the final covariance sandwich. Checked the grouped and l1 extensions, the effective nonlinear output image, and the common-input-kernel quotient with its affine fibers and product-domain normalization.
- For the specialist material, checked the independent-entry coordinate factor, lower spectral cap excluding no optimizer, every interior-ball inequality, valid rational tangent, weak-optimization parameters, and central-ball repair. The argument really allows nonsymmetric or unbounded `K` in the oracle lemma: compactness comes from matrix caps, and the repair uses convexity and the known inner ball. Positivity and unconditionality enter later, precisely where coordinatewise domination of the expected Jensen vector and the final grid error is used.
- Checked the block determinant inequality, blockwise kernel quotient, loss `sum r_b log(r_b+1)`, diagonal bound `A_r^tr<4r`, scalar log-coordinate algorithm, integer-feature volume minor, forest tiling formula including isolated components, thin-domain counterexample, and both Max-Cut packing reductions. The hardness statements distinguish fixed sublinear powers from a sharp linear barrier.
- Compared the specialist proofs with `results/block-psd-quadratic-precision.md`, `results/block-psd-unconditional-error-precision.md`, `results/diagonal-psd-quadratic-linear-dimension-precision.md`, and supporting notes on the block logdet oracle, commuting covariances, and optimality certificates. Also compared relevant finite-covariance and grouped-budget original proofs and inspected the earlier unconditional-block audit after independently reconstructing its argument. These were targeted comparisons, not a new exhaustive audit of every historical note.

Primary sources were checked directly in the cached texts: GLS (1981), definitions (5)–(7) on p.172 and Theorem (3.1); Dadush–Peikert–Vempala, Theorem B.5; Zhang–Sra, Corollary 8; Criscitiello–Boumal, Appendix I and Proposition I.1; IQS, Theorem 1.5 and Lemma 5.3; and GGOW, Theorem 2.18. I also visually inspected the cached GLS p.172 image: its weak optimization compares against all points of the original body, and its weak-separator norm convention is at least one. Those are the interfaces used in the manuscript. I did not conduct a complete publication-priority or bibliography-metadata audit, or independently reprove the imported general algorithms.

Executed checks:

- `check_block_logdet_repair.py`: passed 24 rational repairs, with exact spectral/body/objective bounds and high-precision logdet checks.
- `check_block_psd_precision.py`: passed 36 exact block determinant/cap/trace checks and noncommuting PSD shared-residual bounds.
- `check_unconditional_allocation_repair.py`: passed 24 rational scalar central-ball repairs.
- `check_nonlinear_input_rank.py`: passed 21 quotient/affine-fiber identities and 21 rational LDL normalization/inverse-map cases.
- An independent inline NumPy checker passed 100 signed commuting-Hessian cases in dimensions 2–6, applying all coordinate-flip geometric means and checking determinant preservation, cap and energy feasibility, and final diagonality to numerical tolerances. An exact `Fraction` calculation verified the `4/15` gradient-variation example above.

These finite checks supplement the proofs; they do not implement the complete classical oracle or geodesic optimization algorithms. No manuscript/research files were edited, no subagents were used, and no whole-paper compilation was performed.

All six frozen file hashes were recomputed with SHA-256 and matched `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |
